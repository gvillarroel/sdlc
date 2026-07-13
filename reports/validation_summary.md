# Validation Summary

Date: 2026-07-13

## Purpose

This page summarizes the current quality checks for the report repository. It is a human-readable companion to `scripts/run_all_checks.py`, `results/csv_schema_check.csv`, `results/local_artifact_reference_check.csv`, `results/source_check.csv`, and `results/github_metadata_check.csv`.

## Latest Validation Results

| Check | Command | Latest result |
|---|---|---|
| Unit tests | `python -m unittest discover -s tests` | 162 tests passed. |
| English-only content | `python scripts/check_english_content.py` | 211 repository text files scanned, 0 findings. |
| Full local workflow | `python scripts/run_all_checks.py` | Passed. |
| Copilot SDK POC | `npm test` and `npm run validate` in `examples/copilot-sdk-dynamic-agents/` | 24 tests passed; 3 registry agents validated. |
| Offline artifact validation | `python scripts/validate_artifacts.py` | Passed. |
| Generated CSV schemas | `python scripts/validate_csv_schemas.py` | 41 CSV schemas checked, 0 failures. |
| Local artifact references | `python scripts/check_local_artifact_references.py` | 889 local references checked, 0 missing. |
| Markdown tables | `python scripts/validate_markdown_tables.py` | 386 tables checked, 0 failures. |
| External source URLs | `python scripts/check_sources.py --timeout 20` | 89 URLs checked, 89 OK. |
| GitHub metadata | `python scripts/refresh_github_metadata.py --timeout 20` | 17 repos checked, 0 failures, 0 license mismatches. |
| Artifact manifest | `python scripts/generate_artifact_manifest.py` | 218 repository artifacts hashed. |
| Static site rendering | Browser comparison at 1280 px | Layout preserved after CSS and asset consolidation; a local favicon prevents request errors. |
| Whitespace | `git diff --check` | Passed. |

## What The Validation Covers

| Area | Coverage |
|---|---|
| Data shape | Required generated result files exist and row counts match the expected number of alternatives, scenarios, operating profiles, and stress cases. |
| Language policy | `scripts/check_english_content.py` scans repository-authored text and rejects likely non-English prose while excluding locks, vendor trees, and binary assets. |
| License filter | `results/license_audit.csv` keeps the included set at 17 permissive MIT or Apache-2.0 alternatives and 2 excluded entries. |
| Source availability | `results/source_check.csv` verifies that report and dataset URLs respond successfully. |
| Sandbox sources | `results/sandbox_source_matrix.csv` records 27 official sandbox documentation or repository URLs used by the dedicated sandbox dataset. |
| GitHub metadata | `results/github_metadata_check.csv` verifies repository reachability, live SPDX license match, archive status, stars, push date, and latest release tag. |
| Repository references | `results/local_artifact_reference_check.csv` verifies local artifact references across repository Markdown files. |
| Markdown tables | `results/markdown_table_check.csv` verifies table column consistency across repository Markdown files. |
| CSV contracts | `results/csv_schema_check.csv` verifies expected headers for generated CSV artifacts. |
| Score drivers | `results/score_driver_summary.csv` and `results/criterion_spread_summary.csv` verify candidate and criterion explanation outputs. |
| Scenario playbooks | `results/scenario_playbook_summary.csv` verifies the per-scenario execution guidance output. |
| Risk validation | `results/risk_validation_matrix.csv` verifies the risk-to-evidence pilot gate mapping. |
| Operational model | `results/operational_cost_estimates.csv` and `results/operational_fit_rankings.csv` verify the cost/latency tie-breaker model shape. |
| Recommendation rationale | `results/recommendation_rationale.csv` verifies that each scenario shortlist has a posture, evidence-risk band, effort estimate, and operational rank context. |
| Sandbox evaluation | `results/sandbox_decision_matrix.csv` and `results/sandbox_threat_coverage.csv` verify scenario-specific sandbox posture and threat-control coverage. |
| Pilot sample size | `results/pilot_sample_size_estimates.csv` verifies the task-count planning simulation shape. |
| Artifact manifest | `results/artifact_manifest.csv` records SHA-256 hashes and byte sizes for committed report, data, script, test, and template artifacts. |
| Simulation reproducibility | Unit tests cover deterministic scoring, Monte Carlo reproducibility, stress tests, custom weights, effort estimation, evidence-gap analysis, risk registers, decision tree, and artifact validation. |
| Copilot SDK POC | Node.js tests cover registry mutations, parsing, permission isolation, runtime skill invocation, result sanitization, and chain ordering. |

## Known Validation Boundaries

- The unit tests and offline runner do not execute real candidate agents.
- The Copilot SDK unit tests and registry validation are offline; authenticated smoke tests still require GitHub Copilot access.
- The live source and GitHub checks depend on network availability and should be rerun before final adoption; sandbox-specific official URLs are recorded separately in `results/sandbox_source_matrix.csv`.
- `.github/workflows/validate.yml` is the active CI definition for both the Python evaluation workflow and the offline Node.js proof-of-concept checks.
- Simulation outputs are screening evidence; the pilot protocol is still required before choosing a production foundation.
