# Artifact Index

Date: 2026-07-05

Use this index to choose the right file quickly.

## Read First

| Need | Artifact |
|---|---|
| Quick decision summary | `reports/executive_brief.md` |
| Delivery summary | `reports/release_notes.md` |
| Common questions | `reports/faq.md` |
| Proposed adoption decision record | `reports/adoption_decision_record.md` |
| Scenario execution playbooks | `reports/scenario_playbooks.md` |
| Candidate taxonomy | `reports/candidate_taxonomy.md` |
| Environment prerequisites | `reports/environment_prerequisites.md` |
| Exclusion rationale | `reports/exclusions.md` |
| Guided shortlist selection | `reports/decision_tree.md` |
| Full analysis | `reports/ai_orchestrator_frameworks_report.md` |
| One-file report bundle | `reports/final_report_bundle.md` |
| Requirement coverage | `reports/requirements_traceability.md` |
| Validation and QA summary | `reports/validation_summary.md` |
| Results data dictionary | `reports/results_data_dictionary.md` |
| Residual risks | `reports/residual_risks.md` |
| Risk-to-evidence matrix | `reports/risk_validation_matrix.md` |
| Maintenance procedure | `reports/maintenance_guide.md` |
| Glossary | `reports/glossary.md` |
| Scoring formula and assumptions | `reports/methodology_appendix.md` |
| Simulation assumptions and stress tests | `reports/simulation_assumptions.md` |
| Score driver explanation | `reports/score_driver_summary.md` |
| Operational cost and latency model | `reports/operational_cost_model.md` |
| Evidence-gap findings | `reports/evidence_gap_analysis.md` |
| Scenario recommendation rationale | `reports/recommendation_rationale.md` |
| GitHub metadata verification | `reports/github_metadata_check.md` |
| Security fixture catalog | `reports/security_evaluation_fixtures.md` |
| Pilot execution protocol | `reports/pilot_protocol.md` |
| Pilot sample-size planning | `reports/pilot_sample_size.md` |
| Candidate implementation notes | `reports/implementation_blueprints.md` |
| Stakeholder presentation outline | `reports/presentation_outline.md` |
| Report charts | `reports/assets/rank_stability.svg`, `reports/assets/scenario_regret.svg`, `reports/assets/operational_hours.svg`, `reports/assets/criterion_spread.svg` |

## Data Inputs

| Need | Artifact |
|---|---|
| Candidate list, scores, source links, and notes | `data/alternatives.json` |
| Score calibration anchors | `data/scoring_rubric.json` |
| Scenario definitions and shortlists | `data/scenario_profiles.json` |
| Pilot task suite | `data/pilot_tasks.json` |
| Post-pilot decision model | `data/pilot_decision_model.json` |
| Pilot sample-size assumptions | `data/pilot_sample_size_model.json` |
| Machine-readable decision tree | `data/decision_tree.json` |
| Adoption risk register | `data/risk_register.json` |
| Simulation assumption register | `data/simulation_assumptions.json` |
| Operational cost model assumptions | `data/operational_cost_model.json` |
| Security evaluation fixtures | `data/security_evaluation_fixtures.json` |
| Candidate taxonomy data | `data/candidate_taxonomy.json` |
| Requirement traceability matrix | `data/traceability_matrix.json` |

## Generated Results

| Need | Artifact |
|---|---|
| Scenario rankings | `results/deterministic_rankings.csv` |
| Monte Carlo stability | `results/monte_carlo_summary.csv` |
| Sensitivity to criterion weights | `results/sensitivity_summary.csv` |
| Category strengths | `results/category_scores.csv` |
| Practical shortlist | `results/decision_shortlist.csv` |
| Scenario playbook summary | `results/scenario_playbook_summary.csv` |
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
| Candidate score drivers | `results/score_driver_summary.csv` |
| Criterion score spread | `results/criterion_spread_summary.csv` |
| Prototype and hardening effort estimates | `results/implementation_effort_estimates.csv` |
| Relative operating-cost estimates | `results/operational_cost_estimates.csv` |
| Operation-adjusted scenario rankings | `results/operational_fit_rankings.csv` |
| Pilot sample-size estimates | `results/pilot_sample_size_estimates.csv` |
| Evidence-gap risk analysis | `results/evidence_gap_analysis.csv` |
| Scenario recommendation rationale | `results/recommendation_rationale.csv` |
| Risk validation matrix | `results/risk_validation_matrix.csv` |
| License audit | `results/license_audit.csv` |
| URL health check | `results/source_check.csv` |
| GitHub metadata check | `results/github_metadata_check.csv` |
| Local artifact reference check | `results/local_artifact_reference_check.csv` |
| Markdown table consistency check | `results/markdown_table_check.csv` |
| Generated CSV schema check | `results/csv_schema_check.csv` |
| Artifact SHA-256 manifest | `results/artifact_manifest.csv` |
| Complete machine-readable output | `results/all_results.json` |

## Pilot Execution

| Need | Artifact |
|---|---|
| Capture candidate/task metrics | `templates/pilot_run_log.csv` |
| Human code-review assessment | `templates/reviewer_scorecard.md` |
| Security gate assessment | `templates/security_gate_checklist.md` |
| Select scenario and weights | `templates/scenario_selection_workshop.md` |
| Example post-pilot candidate summary | `examples/pilot_candidate_summary.example.csv` |
| Example custom scenario weights | `examples/custom_weights.example.json` |
| Minimal pilot adapter contract | `examples/pilot_adapter_contract.py` |

## Scripts

| Need | Artifact |
|---|---|
| Regenerate rankings and simulations | `scripts/simulate_alternatives.py` |
| Run simulation stress tests | `scripts/stress_test_simulation.py` |
| Analyze score drivers | `scripts/analyze_score_drivers.py` |
| Build scenario playbooks | `scripts/build_scenario_playbooks.py` |
| Estimate implementation effort | `scripts/estimate_implementation_effort.py` |
| Estimate operational cost and latency risk | `scripts/estimate_operational_costs.py` |
| Estimate pilot sample sizes | `scripts/estimate_pilot_sample_sizes.py` |
| Analyze evidence gaps | `scripts/analyze_evidence_gaps.py` |
| Build recommendation rationale | `scripts/build_recommendation_rationale.py` |
| Build risk validation matrix | `scripts/build_risk_validation_matrix.py` |
| Rank with custom weights | `scripts/rank_with_custom_weights.py` |
| Regenerate license audit | `scripts/license_audit.py` |
| Check external source URLs | `scripts/check_sources.py` |
| Refresh GitHub metadata check | `scripts/refresh_github_metadata.py` |
| Build GitHub metadata report | `scripts/build_github_metadata_report.py` |
| Check local artifact references | `scripts/check_local_artifact_references.py` |
| Validate Markdown tables | `scripts/validate_markdown_tables.py` |
| Validate generated CSV schemas | `scripts/validate_csv_schemas.py` |
| Generate artifact SHA-256 manifest | `scripts/generate_artifact_manifest.py` |
| Validate generated artifacts offline | `scripts/validate_artifacts.py` |
| Generate report SVG charts | `scripts/generate_charts.py` |
| Build results data dictionary | `scripts/build_results_data_dictionary.py` |
| Build one-file report bundle | `scripts/build_report_bundle.py` |
| Score pilot results | `scripts/score_pilot_results.py` |
| Run all local checks | `scripts/run_all_checks.py` |
| Run all local checks from PowerShell | `scripts/run_all_checks.ps1` |

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
python scripts/analyze_score_drivers.py
python scripts/build_scenario_playbooks.py
python scripts/estimate_implementation_effort.py
python scripts/estimate_operational_costs.py
python scripts/estimate_pilot_sample_sizes.py
python scripts/analyze_evidence_gaps.py
python scripts/build_recommendation_rationale.py
python scripts/build_risk_validation_matrix.py
python scripts/rank_with_custom_weights.py
python scripts/license_audit.py
python scripts/check_local_artifact_references.py
python scripts/validate_markdown_tables.py
python scripts/validate_csv_schemas.py
python scripts/generate_artifact_manifest.py
python scripts/build_results_data_dictionary.py
python scripts/build_github_metadata_report.py
python scripts/build_report_bundle.py
python scripts/validate_artifacts.py
```

Run live source verification when network access is available:

```powershell
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
```
