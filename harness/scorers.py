"""Scoring functions for evaluating generated answers.

This module implements very simple scoring heuristics for demonstration.  In a
production system, rubric criteria would be applied by human annotators or
sophisticated classifiers.  Here we base scores on presence/absence of an
answer and correct citations.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def compute_metrics(record: Dict, answer_dict: Dict) -> Dict[str, float]:
    """Compute per‑query metrics.

    Parameters
    ----------
    record : dict
        A query record containing at least 'gold_sources' and 'expects_citation'.
    answer_dict : dict
        A dict with keys 'answer' (str) and 'citations' (list of str).

    Returns
    -------
    dict
        A mapping of metric names to numeric scores.  All scores are in the
        range [0, 1] except for 'tokens'.
    """
    gold = set(record.get("gold_sources") or [])
    citations = set(answer_dict.get("citations") or [])
    answer_text = answer_dict.get("answer") or ""
    metrics: Dict[str, float] = {}

    # Helpfulness: if there is any non‑empty answer, assign 0.4; assign 1.0 if the answer
    # contains at least one word from the gold source snippet (very naive).  Otherwise 0.
    if answer_text.strip():
        metrics["helpfulness"] = 0.4
    else:
        metrics["helpfulness"] = 0.0
    # If the answer mentions the subject of the query (first word) we treat as more helpful
    subject = (record.get("query") or "").split()[0].lower() if record.get("query") else ""
    if subject and subject in answer_text.lower():
        metrics["helpfulness"] = 1.0

    # Citation fidelity: 1.0 if citations match exactly the gold set when citation is expected,
    # else 0.0.  If citations are not expected, always assign 1.
    if record.get("expects_citation"):
        metrics["citation_fidelity"] = 1.0 if citations == gold and citations else 0.0
    else:
        metrics["citation_fidelity"] = 1.0

    # Groundedness: fraction of citations that are in gold.
    if citations:
        metrics["groundedness"] = len(citations & gold) / len(citations)
    else:
        metrics["groundedness"] = 0.0

    # Token count (not scaled)
    metrics["tokens"] = float(len(answer_text.split()))

    return metrics


def aggregate_metrics(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    """Aggregate a list of per‑query metrics into mean values.

    Parameters
    ----------
    metrics_list : list of dict
        Individual metrics for each query.

    Returns
    -------
    dict
        Mean of each metric across the list.
    """
    if not metrics_list:
        return {}
    agg: Dict[str, float] = {}
    keys = metrics_list[0].keys()
    for key in keys:
        agg[key] = sum(m.get(key, 0.0) for m in metrics_list) / len(metrics_list)
    return agg