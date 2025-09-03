import pytest

from harness.scorers import compute_metrics, aggregate_metrics


def test_compute_metrics_citation_match():
    record = {"gold_sources": ["a"], "expects_citation": True, "query": "Test"}
    ans = {"answer": "Test", "citations": ["a"]}
    metrics = compute_metrics(record, ans)
    assert metrics["citation_fidelity"] == 1.0
    assert metrics["groundedness"] == 1.0


def test_compute_metrics_missing_citation():
    record = {"gold_sources": ["a"], "expects_citation": True, "query": "Test"}
    ans = {"answer": "Test", "citations": []}
    metrics = compute_metrics(record, ans)
    assert metrics["citation_fidelity"] == 0.0


def test_aggregate_metrics():
    mlist = [
        {"helpfulness": 1.0, "citation_fidelity": 1.0, "groundedness": 1.0, "tokens": 2.0},
        {"helpfulness": 0.4, "citation_fidelity": 0.0, "groundedness": 0.0, "tokens": 3.0},
    ]
    agg = aggregate_metrics(mlist)
    assert agg["helpfulness"] == pytest.approx(0.7)
    assert agg["citation_fidelity"] == 0.5