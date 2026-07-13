# Release Notes

Date: 2026-07-13

## Purpose

This page summarizes the current repository state for a reviewer opening the GitHub project after the report refresh.

## Delivered Scope

| Area | Delivered artifacts |
|---|---|
| Repository organization | Active CI under `.github/workflows/`, curated sources under `data/sources/`, pilot examples under `examples/pilot/`, canonical site assets under `docs/assets/`, and report navigation in `reports/README.md` |
| Final English report | `reports/ai_orchestrator_frameworks_report.md`, `reports/final_report_bundle.md`, `reports/executive_brief.md` |
| Reproducible simulations | `scripts/simulate_alternatives.py`, `scripts/stress_test_simulation.py`, `results/all_results.json` |
| Dedicated sandbox analysis | `reports/sandbox_report.md`, `data/sandbox_evaluation.json`, `results/sandbox_decision_matrix.csv` |
| Market and maintenance addenda | `reports/market_maintenance_synthesis.md`, `reports/market_entry_barriers_shift.md`, `reports/market_fragmentation_user_share.md`, `reports/long_term_ai_app_maintenance.md`, `reports/ai_code_trust_matrix.md`, `data/sources/market_maintenance_source_matrix.csv` |
| Decision rationale | `reports/scenario_playbooks.md`, `reports/recommendation_rationale.md`, `reports/adoption_decision_record.md` |
| Implementation complexity | `reports/implementation_blueprints.md`, `reports/operational_cost_model.md`, `results/implementation_effort_estimates.csv` |
| Evidence and risk | `reports/evidence_gap_analysis.md`, `reports/github_metadata_check.md`, `reports/risk_validation_matrix.md` |
| Pilot path | `reports/pilot_protocol.md`, `reports/pilot_sample_size.md`, `templates/pilot_run_log.csv`, `templates/security_gate_checklist.md` |
| Reproducibility and QA | `reports/validation_summary.md`, `reports/results_data_dictionary.md`, `results/artifact_manifest.csv` |
| English-content policy | `scripts/check_english_content.py`, `tests/test_english_content.py` |

## Current Validation Snapshot

| Check | Current result |
|---|---|
| Unit tests | 162 tests passed |
| English-only content | 211 repository text files scanned, 0 findings |
| Copilot SDK POC | 24 tests passed; 3 registry agents validated |
| Generated CSV schemas | 41 schemas checked, 0 failures |
| Local artifact references | 889 references checked, 0 missing |
| Markdown tables | 386 tables checked, 0 failures |
| External source URLs | 89 URLs checked, 89 OK |
| GitHub metadata | 17 repos checked, 0 failures, 0 license mismatches |
| Artifact manifest | 218 report, data, result, script, test, template, site, and CI rows |

## Review Entry Points

Start with `reports/executive_brief.md` for the decision summary, then use `reports/recommendation_rationale.md` to see why each scenario shortlist is a pilot candidate, head-to-head candidate, fallback, or watchlist item. Use `reports/validation_summary.md` before relying on a refreshed checkout.

## Refresh Notes

The local workflow is `python scripts/run_all_checks.py`. Live URL and GitHub checks are intentionally separate because they depend on network and API-limit behavior. If GitHub API refreshes return `http_403` or `http_401`, follow the operational notes in `reports/maintenance_guide.md` before replacing `results/github_metadata_check.csv`.
