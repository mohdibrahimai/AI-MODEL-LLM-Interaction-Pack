# Product Requirements Document: Interaction Pack

## Goal

Demonstrate how simple micro‑tools and editorial guidelines can measurably improve question‑answering quality on a small evaluation set.  The target is to raise citation fidelity from 0 to 100 percentage points on the evaluation split without increasing the average token count and while improving helpfulness.

## Success Metrics

- **Citation fidelity (C2 rate)** increases from baseline 0% to ≥95% for queries that expect citations.
- **Helpfulness** improves from baseline (<0.5) to ≥0.7 on average.
- **Token count** does not increase (ideally decreases) relative to baseline.

## Features

1. **Micro‑tools**: Implement `question_splitter`, `citation_deduper` and `tone_normalizer` to clean up queries and answers.
2. **Answer generation**: Provide canned responses for demonstration, keyed by query domain, and call micro‑tools to normalise tone and deduplicate citations.
3. **Scoring harness**: Compute per‑query metrics and aggregated metrics for each variant.  Export JSONL and CSV files for analysis.
4. **Documentation**: Include examples for bad→better→best flows, UX writing templates and a failure‑mode atlas.

## Non‑Goals

- Deploying a full conversational agent.
- Connecting to external APIs or real model endpoints.
- Covering every possible query type.

## Risks and Mitigations

- **Over‑fitting to the tiny dataset**: The improvements may not generalise.  Document clearly that this is a demo; encourage users to expand the dataset.
- **False sense of perfection**: Provide conservative examples and emphasise that real systems require more sophisticated evaluation.
- **Inaccurate canned answers**: Keep answers high‑level and reference source snippets provided in the repository.

## Roll‑Out Plan

1. Build the repository skeleton with datasets, tools, harness, docs and CI.  (This repository.)
2. Run baseline and improved evaluations locally; verify that metrics meet targets on the demo dataset.
3. Publish the repository and invite contributions to expand queries, improve tools, and refine scoring functions.

## Future Work

- Replace canned answers with calls to actual language models.
- Collect a larger and more diverse dataset with manual annotations.
- Develop richer metrics and integrate human evaluation.
- Automate CI badges that display current scores and trends over time.