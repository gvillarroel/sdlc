# Validation Summary

Date: 2026-07-05

## Purpose

This page summarizes the current quality checks for the report repository. It is a human-readable companion to `scripts/run_all_checks.py`, `results/csv_schema_check.csv`, `results/local_artifact_reference_check.csv`, `results/source_check.csv`, and `results/github_metadata_check.csv`.

## Latest Validation Results

| Check | Command | Latest result |
|---|---|---|
| Unit tests | `python -m unittest discover -s tests` | 128 tests passed. |
| Full local workflow | `python scripts/run_all_checks.py` | Passed. |
| Offline artifact validation | `python scripts/validate_artifacts.py` | Passed. |
| Generated CSV schemas | `python scripts/validate_csv_schemas.py` | 35 CSV schemas checked, 0 failures. |
| Local artifact references | `python scripts/check_local_artifact_references.py` | 713 local references checked, 0 missing. |
| Markdown tables | `python scripts/validate_markdown_tables.py` | 217 tables checked, 0 failures. |
| External source URLs | `python scripts/check_sources.py --timeout 20` | 41 URLs checked, 41 OK. |
| GitHub metadata | `python scripts/refresh_github_metadata.py --timeout 20` | 17 repos checked, 0 failures, 0 license mismatches. |
| Whitespace | `git diff --check` | Passed. |

## What The Validation Covers

| Area | Coverage |
|---|---|
| Data shape | Required generated result files exist and row counts match the expected number of alternatives, scenarios, operating profiles, and stress cases. |
| License filter | `results/license_audit.csv` keeps the included set at 17 permissive MIT or Apache-2.0 alternatives and 2 excluded entries. |
| Source availability | `results/source_check.csv` verifies that report and dataset URLs respond successfully. |
| GitHub metadata | `results/github_metadata_check.csv` verifies repository reachability, live SPDX license match, archive status, stars, push date, and latest release tag. |
| Report references | `results/local_artifact_reference_check.csv` verifies README and report references to local artifacts. |
| Markdown tables | `results/markdown_table_check.csv` verifies table column consistency in README and report Markdown files. |
| CSV contracts | `results/csv_schema_check.csv` verifies expected headers for generated CSV artifacts. |
| Score drivers | `results/score_driver_summary.csv` and `results/criterion_spread_summary.csv` verify candidate and criterion explanation outputs. |
| Scenario playbooks | `results/scenario_playbook_summary.csv` verifies the per-scenario execution guidance output. |
| Risk validation | `results/risk_validation_matrix.csv` verifies the risk-to-evidence pilot gate mapping. |
| Operational model | `results/operational_cost_estimates.csv` and `results/operational_fit_rankings.csv` verify the cost/latency tie-breaker model shape. |
| Recommendation rationale | `results/recommendation_rationale.csv` verifies that each scenario shortlist has a posture, evidence-risk band, effort estimate, and operational rank context. |
| Pilot sample size | `results/pilot_sample_size_estimates.csv` verifies the task-count planning simulation shape. |
| Artifact manifest | `results/artifact_manifest.csv` records SHA-256 hashes and byte sizes for committed report, data, script, test, and template artifacts. |
| Simulation reproducibility | Unit tests cover deterministic scoring, Monte Carlo reproducibility, stress tests, custom weights, effort estimation, evidence-gap analysis, risk registers, decision tree, and artifact validation. |

## Known Validation Boundaries

- The unit tests and offline runner do not execute real candidate agents.
- The live source and GitHub checks depend on network availability and should be rerun before final adoption.
- The committed CI file is under `ci/validate-workflow.example.yml` because pushing workflow files requires a token with GitHub `workflow` scope.
- Simulation outputs are screening evidence; the pilot protocol is still required before choosing a production foundation.
