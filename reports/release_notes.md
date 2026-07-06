# Release Notes

Date: 2026-07-05

## Purpose

This page summarizes the current repository state for a reviewer opening the GitHub project after the report refresh.

## Delivered Scope

| Area | Delivered artifacts |
|---|---|
| Final English report | `reports/ai_orchestrator_frameworks_report.md`, `reports/final_report_bundle.md`, `reports/executive_brief.md` |
| Reproducible simulations | `scripts/simulate_alternatives.py`, `scripts/stress_test_simulation.py`, `results/all_results.json` |
| Dedicated sandbox analysis | `reports/sandbox_report.md`, `data/sandbox_evaluation.json`, `results/sandbox_decision_matrix.csv` |
| Market and maintenance addenda | `reports/market_maintenance_synthesis.md`, `reports/market_entry_barriers_shift.md`, `reports/market_fragmentation_user_share.md`, `reports/long_term_ai_app_maintenance.md`, `reports/ai_code_trust_matrix.md`, `results/market_maintenance_source_matrix.csv` |
| Decision rationale | `reports/scenario_playbooks.md`, `reports/recommendation_rationale.md`, `reports/adoption_decision_record.md` |
| Implementation complexity | `reports/implementation_blueprints.md`, `reports/operational_cost_model.md`, `results/implementation_effort_estimates.csv` |
| Evidence and risk | `reports/evidence_gap_analysis.md`, `reports/github_metadata_check.md`, `reports/risk_validation_matrix.md` |
| Pilot path | `reports/pilot_protocol.md`, `reports/pilot_sample_size.md`, `templates/pilot_run_log.csv`, `templates/security_gate_checklist.md` |
| Reproducibility and QA | `reports/validation_summary.md`, `reports/results_data_dictionary.md`, `results/artifact_manifest.csv` |

## Current Validation Snapshot

| Check | Current result |
|---|---|
| Unit tests | 141 tests passed |
| Generated CSV schemas | 41 schemas checked, 0 failures |
| Local artifact references | 853 references checked, 0 missing |
| Markdown tables | 313 tables checked, 0 failures |
| External source URLs | 62 URLs checked, 62 OK |
| GitHub metadata | 17 repos checked, 0 failures, 0 license mismatches |
| Artifact manifest | 170 report, data, result, script, test, template, and CI rows |

## Review Entry Points

Start with `reports/executive_brief.md` for the decision summary, then use `reports/recommendation_rationale.md` to see why each scenario shortlist is a pilot candidate, head-to-head candidate, fallback, or watchlist item. Use `reports/validation_summary.md` before relying on a refreshed checkout.

## Refresh Notes

The local workflow is `python scripts/run_all_checks.py`. Live URL and GitHub checks are intentionally separate because they depend on network and API-limit behavior. If GitHub API refreshes return `http_403` or `http_401`, follow the operational notes in `reports/maintenance_guide.md` before replacing `results/github_metadata_check.csv`.
