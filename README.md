// This repository demonstrates an example of AI interaction design evaluation for question answering flows.

# Interaction Pack

This repository is a **minimal yet functional** starter kit for evaluating and improving AI question‑answering interactions.  It bundles a tiny dataset, rubric‑driven scoring harness, and micro‑tools that clean up answers.  The goal is to show a clear **before → after → measurable lift** using reproducible evaluation rather than to offer a production system.

![Banner](docs/assets/banner.png)

## Quickstart

Run the evaluation harness on the included evaluation split.  First install any Python dependencies (this repository is intentionally light and should run in a vanilla Python 3.11 environment):

```bash
python -m harness.run gen --config harness/config.yaml --split eval --variant baseline
python -m harness.run gen --config harness/config.yaml --split eval --variant improved
python -m harness.run score --split eval --variants baseline,improved
python -m harness.run leaderboard --split eval
```

After running the commands above, the **leaderboard** file will appear in `harness/outputs/leaderboard.csv` and a simple HTML report at `harness/outputs/report.html`.

## Repository layout

- **data/** – JSON Lines datasets and tiny source snippets for deterministic demonstration.
- **rubrics/** – YAML rubric definitions for helpfulness and citation fidelity.
- **flows/** – Three example flows (direct answer, partial answer + next step, disagreement/abstain) each with bad→better→best examples and commentary.
- **tools/** – Small Python scripts that implement transformations used by the improved variant (question splitting, citation deduplication, tone normalization) and their unit tests.
- **harness/** – The evaluation harness with CLI commands for generation, scoring and reporting.  Includes a simple configuration file and test stubs.
- **docs/** – Background documentation: a UX writing one‑pager, a mock PRD and a failure‑mode atlas describing common mistakes and fixes.
- **.github/workflows/** – CI configuration that runs tests and a quick smoke evaluation.
- **scripts/** – Stub scripts for updating badges and creating GIFs (placeholders for your own automation).

## Example results

The included evaluation split contains only a handful of sample queries.  A typical run might produce the following metrics (numbers here are illustrative):

| Metric               | Baseline | Improved |
|----------------------|---------:|---------:|
| Helpfulness (avg)    |      2.0 |      4.5 |
| Citation fidelity (%)|        0 |      100 |
| Groundedness         |      0.0 |      1.0 |
| Avg token count      |       10 |        5 |

For details see the generated `leaderboard.csv` and the per‑query breakdown in `outputs/run_*` files.

## Note

This repository is intentionally lightweight; it serves as a demonstration of structure and evaluation principles rather than a full‑fledged production system.  Feel free to extend the datasets, improve the tools, flesh out the harness and CI, and integrate your own models.