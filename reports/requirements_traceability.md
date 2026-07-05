# Requirements Traceability

Date: 2026-07-05

## Purpose

This document maps the original request to the repository artifacts that satisfy it. The machine-readable version is `data/traceability_matrix.json`.

## Coverage Matrix

| Requirement | Primary artifacts | Validation |
|---|---|---|
| Study the shared ChatGPT conversation and evaluate the listed alternatives. | `reports/ai_orchestrator_frameworks_report.md`, `data/alternatives.json`, `results/evidence_matrix.csv` | `python scripts/validate_artifacts.py` |
| Review the alternatives that are not copyleft and are open source. | `results/license_audit.csv`, `scripts/license_audit.py`, `data/alternatives.json` | `python scripts/license_audit.py` |
| Evaluate alternatives with Python simulations. | `scripts/simulate_alternatives.py`, `scripts/analyze_score_drivers.py`, `scripts/build_scenario_playbooks.py`, `results/deterministic_rankings.csv`, `results/monte_carlo_summary.csv`, `results/sensitivity_summary.csv`, `results/score_driver_summary.csv`, `results/criterion_spread_summary.csv`, `results/scenario_playbook_summary.csv`, `results/all_results.json` | `python scripts/simulate_alternatives.py --trials 5000 --seed 7331 && python scripts/analyze_score_drivers.py && python scripts/build_scenario_playbooks.py` |
| Review everything that can affect the simulation. | `reports/simulation_assumptions.md`, `data/simulation_assumptions.json`, `reports/operational_cost_model.md`, `scripts/stress_test_simulation.py`, `scripts/estimate_operational_costs.py`, `results/stress_test_summary.csv`, `results/uncertainty_stress_summary.csv`, `results/operational_fit_rankings.csv` | `python scripts/stress_test_simulation.py --trials 1500 --seed 9011 && python scripts/estimate_operational_costs.py` |
| Review how complicated it is to build something with the alternatives. | `reports/implementation_blueprints.md`, `reports/operational_cost_model.md`, `results/implementation_effort_estimates.csv`, `results/operational_cost_estimates.csv`, `scripts/estimate_implementation_effort.py`, `scripts/estimate_operational_costs.py` | `python scripts/estimate_implementation_effort.py && python scripts/estimate_operational_costs.py` |
| Check factors that can make the evaluation unreliable. | `reports/evidence_gap_analysis.md`, `results/evidence_gap_analysis.csv`, `results/source_check.csv`, `scripts/analyze_evidence_gaps.py`, `scripts/check_sources.py` | `python scripts/analyze_evidence_gaps.py` |
| Provide a way to move from simulated ranking to real evidence. | `reports/pilot_protocol.md`, `reports/pilot_sample_size.md`, `data/pilot_tasks.json`, `data/pilot_sample_size_model.json`, `data/security_evaluation_fixtures.json`, `templates/pilot_run_log.csv`, `templates/reviewer_scorecard.md`, `templates/security_gate_checklist.md`, `examples/pilot_adapter_contract.py`, `scripts/estimate_pilot_sample_sizes.py`, `scripts/score_pilot_results.py` | `python scripts/estimate_pilot_sample_sizes.py && python scripts/score_pilot_results.py --input examples/pilot_candidate_summary.example.csv --output results/pilot_decision_scores.example.csv` |
| Generate the final report in English. | `reports/ai_orchestrator_frameworks_report.md`, `reports/executive_brief.md`, `reports/artifact_index.md` | `python scripts/validate_artifacts.py` |
| Upload the tests and final report to GitHub. | `tests/`, `scripts/run_all_checks.py`, `ci/validate-workflow.example.yml` | `python scripts/run_all_checks.py` |

## Reproducibility Command

Run the full local validation workflow:

```powershell
python scripts/run_all_checks.py
```

The workflow runs unit tests, regenerates simulation outputs, stress tests, implementation effort estimates, operational cost estimates, evidence-gap analysis, license audit, charts, pilot score example, and offline artifact validation.

## GitHub Status

The repository includes the final report, generated result files, scripts, tests, templates, and CI workflow example. The generated `.github/workflows/` file is intentionally provided under `ci/validate-workflow.example.yml` because the current GitHub token cannot push workflow files without `workflow` scope.
