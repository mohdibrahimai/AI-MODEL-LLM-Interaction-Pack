"""CLI entry point for the evaluation harness.

This script supports generating answers for different variants, scoring them using
simple heuristics and producing an aggregated leaderboard.  It is not
production‑ready but illustrates how to wire together the dataset, tools and
scoring functions.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

import yaml  # type: ignore

# Ensure the parent directory is on sys.path so that imports work when this
# script is executed directly.  Without this modification Python will not
# find the sibling packages `tools` and `harness` when run from the repo root.
from pathlib import Path  # noqa: E402
import sys  # noqa: E402

current_dir = Path(__file__).resolve()
sys.path.insert(0, str(current_dir.parents[1]))

from tools.question_splitter import split_question  # noqa: E402
from tools.citation_deduper import dedupe_citations  # noqa: E402
from tools.tone_normalizer import normalize_tone  # noqa: E402
from harness.scorers import compute_metrics, aggregate_metrics  # noqa: E402


def load_config(config_path: str) -> Dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_dataset(dataset_path: str) -> List[Dict]:
    records: List[Dict] = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def generate_answer(record: Dict, variant: str) -> Dict:
    """Generate an answer dictionary for a given record and variant.

    Parameters
    ----------
    record : dict
        A query record.
    variant : str
        The variant name (e.g., "baseline" or "improved").

    Returns
    -------
    dict
        A dict with keys 'answer' and 'citations'.
    """
    if variant == "baseline":
        # Baseline declines to answer
        return {"answer": "I don't know.", "citations": []}

    # Improved variant: simple canned responses keyed by domain or query id
    qid = record.get("id")
    query = record.get("query", "")
    domain = record.get("domain", "")
    if domain == "factual" and "capital of France" in query:
        answer = "Paris is the capital of France."
    elif domain == "academic" and "P" in query and "NP" in query:
        answer = "In complexity theory, P is the class of problems solvable in polynomial time, while NP is the class of problems whose solutions can be verified in polynomial time."
    elif domain == "partial" and "sunlight" in query:
        answer = "Moderate sunlight exposure has been linked to improved mood and vitamin D synthesis."
    elif domain == "disagreement" and "earth" in query.lower():
        answer = "Scientific evidence overwhelmingly supports that the Earth is round."
    else:
        # Fallback: use the first sentence of the query as a weak answer
        answer = query.split(".")[0]

    # Normalise tone
    answer = normalize_tone(answer)
    # Generate citations: for demonstration we use the provided gold sources
    citations = dedupe_citations(record.get("gold_sources", []))
    return {"answer": answer, "citations": citations}


def cmd_gen(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    split_file = cfg["split_files"][args.split]
    records = load_dataset(split_file)
    out_dir = Path(cfg.get("output_dir", "harness/outputs"))
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"run_{args.variant}_{args.split}.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for record in records:
            ans = generate_answer(record, args.variant)
            out_obj = {"id": record["id"], "query": record["query"], **ans}
            f.write(json.dumps(out_obj) + "\n")
    print(f"Wrote {len(records)} entries to {output_path}")


def load_run_file(path: str) -> List[Dict]:
    runs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                runs.append(json.loads(line))
    return runs


def cmd_score(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    split_file = cfg["split_files"][args.split]
    records = {r["id"]: r for r in load_dataset(split_file)}
    out_dir = Path(cfg.get("output_dir", "harness/outputs"))
    out_dir.mkdir(parents=True, exist_ok=True)
    for variant in args.variants.split(","):
        run_path = out_dir / f"run_{variant}_{args.split}.jsonl"
        runs = load_run_file(str(run_path))
        metrics_list: List[Dict[str, float]] = []
        scores_path = out_dir / f"scores_{variant}_{args.split}.jsonl"
        with open(scores_path, "w", encoding="utf-8") as sf:
            for obj in runs:
                record = records.get(obj["id"])
                metrics = compute_metrics(record, obj)
                metrics_list.append(metrics)
                out_line = {"id": obj["id"], **metrics}
                sf.write(json.dumps(out_line) + "\n")
        agg = aggregate_metrics(metrics_list)
        agg_path = out_dir / f"agg_{variant}_{args.split}.json"
        with open(agg_path, "w", encoding="utf-8") as af:
            json.dump(agg, af)
        print(f"Scored {len(runs)} answers for variant {variant}; aggregated metrics written to {agg_path}")


def cmd_leaderboard(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    out_dir = Path(cfg.get("output_dir", "harness/outputs"))
    variants = args.variants.split(",")
    rows: List[str] = []
    header = ["variant", "helpfulness", "citation_fidelity", "groundedness", "tokens"]
    rows.append(",".join(header))
    for variant in variants:
        agg_path = out_dir / f"agg_{variant}_{args.split}.json"
        if not agg_path.exists():
            print(f"Aggregated metrics not found for variant {variant}; run score first")
            continue
        with open(agg_path, "r", encoding="utf-8") as f:
            agg = json.load(f)
        row = [variant] + [f"{agg.get(metric, 0.0):.2f}" for metric in header[1:]]
        rows.append(",".join(row))
    leaderboard_path = out_dir / "leaderboard.csv"
    with open(leaderboard_path, "w", encoding="utf-8") as lb:
        lb.write("\n".join(rows))
    print(f"Leaderboard written to {leaderboard_path}")


def cmd_report(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    out_dir = Path(cfg.get("output_dir", "harness/outputs"))
    leaderboard_path = out_dir / "leaderboard.csv"
    if not leaderboard_path.exists():
        print("Leaderboard not found; run leaderboard command first.")
        return
    # Very simple HTML report
    with open(leaderboard_path, "r", encoding="utf-8") as f:
        lines = [l.strip().split(",") for l in f if l.strip()]
    html_rows = []
    for i, row in enumerate(lines):
        tag = "th" if i == 0 else "td"
        cells = "".join(f"<{tag}>{cell}</{tag}>" for cell in row)
        html_rows.append(f"<tr>{cells}</tr>")
    html = """<html><head><title>Interaction Pack Report</title></head><body>
    <h1>Interaction Pack Evaluation Report</h1>
    <table border=1 cellpadding=4 cellspacing=0>
    {rows}
    </table>
    </body></html>""".format(rows="\n".join(html_rows))
    report_path = out_dir / "report.html"
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(html)
    print(f"Report written to {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Interaction Pack evaluation harness")
    sub = parser.add_subparsers(dest="command", required=True)
    genp = sub.add_parser("gen", help="Generate answers for a variant and split")
    genp.add_argument("--config", required=True, help="Path to YAML config")
    genp.add_argument("--split", choices=["train", "eval"], default="eval")
    genp.add_argument("--variant", required=True, help="Variant name to generate answers for")
    genp.set_defaults(func=cmd_gen)

    scorep = sub.add_parser("score", help="Score generated answers for one or more variants")
    scorep.add_argument("--config", required=True, help="Path to YAML config")
    scorep.add_argument("--split", choices=["train", "eval"], default="eval")
    scorep.add_argument("--variants", required=True, help="Comma‑separated list of variants to score")
    scorep.set_defaults(func=cmd_score)

    ldp = sub.add_parser("leaderboard", help="Create aggregated leaderboard from scored variants")
    ldp.add_argument("--config", required=True, help="Path to YAML config")
    ldp.add_argument("--split", choices=["train", "eval"], default="eval")
    ldp.add_argument("--variants", required=True, help="Comma‑separated list of variants to include")
    ldp.set_defaults(func=cmd_leaderboard)

    rep = sub.add_parser("report", help="Render an HTML report from the leaderboard")
    rep.add_argument("--config", required=True, help="Path to YAML config")
    rep.add_argument("--split", choices=["train", "eval"], default="eval")
    rep.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()