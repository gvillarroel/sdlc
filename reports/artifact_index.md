# Artifact Index

Date: 2026-07-05

Use this index to choose the right file quickly.

## Read First

| Need | Artifact |
|---|---|
| Quick decision summary | `reports/executive_brief.md` |
| Proposed adoption decision record | `reports/adoption_decision_record.md` |
| Guided shortlist selection | `reports/decision_tree.md` |
| Full analysis | `reports/ai_orchestrator_frameworks_report.md` |
| Requirement coverage | `reports/requirements_traceability.md` |
| Validation and QA summary | `reports/validation_summary.md` |
| Glossary | `reports/glossary.md` |
| Scoring formula and assumptions | `reports/methodology_appendix.md` |
| Simulation assumptions and stress tests | `reports/simulation_assumptions.md` |
| Evidence-gap findings | `reports/evidence_gap_analysis.md` |
| GitHub metadata verification | `reports/github_metadata_check.md` |
| Security fixture catalog | `reports/security_evaluation_fixtures.md` |
| Pilot execution protocol | `reports/pilot_protocol.md` |
| Candidate implementation notes | `reports/implementation_blueprints.md` |
| Report charts | `reports/assets/rank_stability.svg`, `reports/assets/scenario_regret.svg` |

## Data Inputs

| Need | Artifact |
|---|---|
| Candidate list, scores, source links, and notes | `data/alternatives.json` |
| Score calibration anchors | `data/scoring_rubric.json` |
| Scenario definitions and shortlists | `data/scenario_profiles.json` |
| Pilot task suite | `data/pilot_tasks.json` |
| Post-pilot decision model | `data/pilot_decision_model.json` |
| Machine-readable decision tree | `data/decision_tree.json` |
| Adoption risk register | `data/risk_register.json` |
| Simulation assumption register | `data/simulation_assumptions.json` |
| Security evaluation fixtures | `data/security_evaluation_fixtures.json` |
| Requirement traceability matrix | `data/traceability_matrix.json` |

## Generated Results

| Need | Artifact |
|---|---|
| Scenario rankings | `results/deterministic_rankings.csv` |
| Monte Carlo stability | `results/monte_carlo_summary.csv` |
| Sensitivity to criterion weights | `results/sensitivity_summary.csv` |
| Category strengths | `results/category_scores.csv` |
| Practical shortlist | `results/decision_shortlist.csv` |
| Regret versus scenario winner | `results/regret_analysis.csv` |
| Pareto dominance | `results/pareto_frontier.csv` |
| Cross-scenario rank stability | `results/rank_stability.csv` |
| Deterministic assumption stress summary | `results/stress_test_summary.csv` |
| Deterministic assumption stress rankings | `results/stress_test_rankings.csv` |
| Monte Carlo uncertainty stress summary | `results/uncertainty_stress_summary.csv` |
| Monte Carlo uncertainty stress details | `results/uncertainty_stress_details.csv` |
| Example post-pilot decision scores | `results/pilot_decision_scores.example.csv` |
| Example custom-weight rankings | `results/custom_weights_example_rankings.csv` |
| Model weights | `results/scenario_weights.csv` |
| Criteria definitions | `results/criteria_definitions.csv` |
| Source/evidence table | `results/evidence_matrix.csv` |
| Alternative scorecards | `results/alternative_scorecards.csv` |
| Prototype and hardening effort estimates | `results/implementation_effort_estimates.csv` |
| Evidence-gap risk analysis | `results/evidence_gap_analysis.csv` |
| License audit | `results/license_audit.csv` |
| URL health check | `results/source_check.csv` |
| GitHub metadata check | `results/github_metadata_check.csv` |
| Local artifact reference check | `results/local_artifact_reference_check.csv` |
| Generated CSV schema check | `results/csv_schema_check.csv` |
| Complete machine-readable output | `results/all_results.json` |

## Pilot Execution

| Need | Artifact |
|---|---|
| Capture candidate/task metrics | `templates/pilot_run_log.csv` |
| Human code-review assessment | `templates/reviewer_scorecard.md` |
| Security gate assessment | `templates/security_gate_checklist.md` |
| Example post-pilot candidate summary | `examples/pilot_candidate_summary.example.csv` |
| Example custom scenario weights | `examples/custom_weights.example.json` |
| Minimal pilot adapter contract | `examples/pilot_adapter_contract.py` |

## Scripts

| Need | Artifact |
|---|---|
| Regenerate rankings and simulations | `scripts/simulate_alternatives.py` |
| Run simulation stress tests | `scripts/stress_test_simulation.py` |
| Estimate implementation effort | `scripts/estimate_implementation_effort.py` |
| Analyze evidence gaps | `scripts/analyze_evidence_gaps.py` |
| Rank with custom weights | `scripts/rank_with_custom_weights.py` |
| Regenerate license audit | `scripts/license_audit.py` |
| Check external source URLs | `scripts/check_sources.py` |
| Refresh GitHub metadata check | `scripts/refresh_github_metadata.py` |
| Check local artifact references | `scripts/check_local_artifact_references.py` |
| Validate generated CSV schemas | `scripts/validate_csv_schemas.py` |
| Validate generated artifacts offline | `scripts/validate_artifacts.py` |
| Generate report SVG charts | `scripts/generate_charts.py` |
| Score pilot results | `scripts/score_pilot_results.py` |
| Run all local checks | `scripts/run_all_checks.py` |

## Maintenance

Run the core validation set:

```powershell
python -m unittest discover -s tests
python scripts/run_all_checks.py
```

Or run the core deterministic pieces manually:

```powershell
python scripts/simulate_alternatives.py --trials 5000 --seed 7331
python scripts/stress_test_simulation.py --trials 1500 --seed 9011
python scripts/estimate_implementation_effort.py
python scripts/analyze_evidence_gaps.py
python scripts/rank_with_custom_weights.py
python scripts/license_audit.py
python scripts/check_local_artifact_references.py
python scripts/validate_csv_schemas.py
python scripts/validate_artifacts.py
```

Run live source verification when network access is available:

```powershell
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
```
