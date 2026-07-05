# Permissive Open-Source AI Orchestrator Alternatives

This repository contains a reproducible evaluation of permissive open-source alternatives from the shared ChatGPT discussion about AI coding-agent orchestrators.

Included artifacts:

- `data/alternatives.json` - curated dataset, source links, license filter, and 0-5 criterion scores.
- `data/scoring_rubric.json` - calibration guide for the 0-5 scoring model.
- `data/scenario_profiles.json` - plain-English scenario definitions and intended shortlists.
- `data/pilot_tasks.json` - 20-task pilot suite for moving from simulated ranking to execution evidence.
- `data/pilot_decision_model.json` - post-pilot scoring weights and gates.
- `data/pilot_sample_size_model.json` - pilot task-count planning assumptions for close-candidate comparisons.
- `data/decision_tree.json` - machine-readable guided selection tree.
- `data/risk_register.json` - actionable adoption risks, mitigations, and required evidence.
- `data/simulation_assumptions.json` - structured threats to validity and mitigation coverage for the simulation.
- `data/operational_cost_model.json` - operating profiles and assumptions for relative cost/latency planning.
- `data/security_evaluation_fixtures.json` - security fixtures for sandbox, secret, network, prompt-injection, and approval testing.
- `data/candidate_taxonomy.json` - candidate groups by adoption shape.
- `data/traceability_matrix.json` - requirement-to-artifact traceability map.
- `scripts/simulate_alternatives.py` - deterministic weighted ranking, Monte Carlo uncertainty simulation, and sensitivity analysis.
- `scripts/stress_test_simulation.py` - stress tests for scenario weights, maturity discounts, source confidence, sandbox assumptions, and uncertainty.
- `scripts/analyze_score_drivers.py` - candidate score-driver and criterion-spread summary.
- `scripts/build_scenario_playbooks.py` - scenario-specific decision playbook builder.
- `scripts/estimate_implementation_effort.py` - reproducible prototype and hardening effort estimates from the scoring dataset.
- `scripts/estimate_operational_costs.py` - relative operating-cost, token-pressure, latency-risk, and operation-adjusted ranking model.
- `scripts/estimate_pilot_sample_sizes.py` - pilot task-count simulation for distinguishing close shortlist candidates.
- `scripts/analyze_evidence_gaps.py` - evidence-gap review for maturity, confidence, release, traction, and freshness risks.
- `scripts/build_recommendation_rationale.py` - generated scenario recommendation rationale from ranking, stability, risk, effort, and operational signals.
- `scripts/build_risk_validation_matrix.py` - risk-to-evidence pilot validation matrix builder.
- `scripts/rank_with_custom_weights.py` - deterministic ranking for user-provided scenario weights.
- `scripts/check_local_artifact_references.py` - offline check for local artifact references in README and reports.
- `scripts/validate_markdown_tables.py` - Markdown table column consistency check for README and reports.
- `scripts/validate_csv_schemas.py` - generated CSV header/schema validation.
- `scripts/generate_artifact_manifest.py` - SHA-256 manifest generator for repository artifacts.
- `scripts/refresh_github_metadata.py` - optional live GitHub metadata checker for repository, license, star, push, and release signals.
- `scripts/build_github_metadata_report.py` - generated Markdown summary for the latest GitHub metadata CSV.
- `scripts/check_sources.py` - optional live source URL checker for the report and dataset.
- `scripts/license_audit.py` - permissive-license audit for included and excluded alternatives.
- `scripts/validate_artifacts.py` - offline consistency validation for generated artifacts and report references.
- `scripts/generate_charts.py` - SVG chart generator for report visualizations.
- `scripts/build_results_data_dictionary.py` - generated CSV results data dictionary builder.
- `scripts/build_report_bundle.py` - generated one-file final report bundle builder.
- `scripts/score_pilot_results.py` - post-pilot candidate scoring calculator.
- `scripts/run_all_checks.py` - one-command local regeneration and validation workflow.
- `scripts/run_all_checks.ps1` - PowerShell wrapper for the full local workflow.
- `tests/test_simulation_model.py` - validation tests for the scoring model and dataset.
- `results/` - generated CSV and JSON simulation outputs, including category scorecards and a scenario shortlist.
- `templates/` - pilot run log, reviewer scorecard, security gate checklist, and scenario workshop templates.
- `examples/pilot_candidate_summary.example.csv` - example input for post-pilot scoring.
- `examples/custom_weights.example.json` - example custom scenario weights.
- `examples/pilot_adapter_contract.py` - minimal Python adapter contract for comparable pilot runs.
- `reports/ai_orchestrator_frameworks_report.md` - final English report.
- `reports/final_report_bundle.md` - generated one-file bundle of the main report and key appendices.
- `reports/adoption_decision_record.md` - proposed adoption decision record and no-go conditions.
- `reports/executive_brief.md` - short decision brief for quick review.
- `reports/release_notes.md` - reviewer-oriented summary of delivered artifacts and current validation status.
- `reports/candidate_taxonomy.md` - grouping of candidates by adoption shape and workflow fit.
- `reports/environment_prerequisites.md` - local environment requirements for reproducing checks.
- `reports/exclusions.md` - rationale for excluded non-matching items from the shared discussion.
- `reports/faq.md` - answers to common scope, weighting, exclusion, and pilot questions.
- `reports/evidence_gap_analysis.md` - evidence-gap findings for low-confidence or immature candidates.
- `reports/recommendation_rationale.md` - generated scenario-by-scenario recommendation rationale.
- `reports/operational_cost_model.md` - generated operating-cost and operation-adjusted ranking appendix.
- `reports/github_metadata_check.md` - live GitHub metadata verification summary.
- `reports/glossary.md` - definitions for scoring, simulation, security, and orchestration terms.
- `reports/security_evaluation_fixtures.md` - reusable security fixture catalog for pilot gates.
- `reports/requirements_traceability.md` - coverage map from the original request to artifacts and validation commands.
- `reports/validation_summary.md` - latest validation and QA summary for generated artifacts and tests.
- `reports/results_data_dictionary.md` - generated data dictionary for CSV outputs.
- `reports/residual_risks.md` - residual risks that require pilot or legal/security evidence.
- `reports/risk_validation_matrix.md` - generated mapping from adoption risks to pilot evidence.
- `reports/maintenance_guide.md` - procedure for refreshing sources, scores, candidates, and generated artifacts.
- `reports/methodology_appendix.md` - scoring formulas, Monte Carlo assumptions, and customization notes.
- `reports/simulation_assumptions.md` - assumptions, stress tests, and interpretation of ranking fragility.
- `reports/score_driver_summary.md` - generated explanation of candidate strengths, weaknesses, and high-spread criteria.
- `reports/artifact_index.md` - navigation guide for all report, data, result, template, and script artifacts.
- `reports/scenario_playbooks.md` - generated per-scenario execution playbooks.
- `reports/pilot_protocol.md` - step-by-step protocol for executing the recommended pilot.
- `reports/pilot_sample_size.md` - generated task-count planning appendix for the pilot.
- `reports/implementation_blueprints.md` - implementation notes for the main pilot candidates.
- `reports/decision_tree.md` - guided shortlist selection tree.
- `reports/presentation_outline.md` - stakeholder presentation outline.
- `ci/validate-workflow.example.yml` - GitHub Actions workflow template for the full local check workflow and committed-output validation.

Run the checks and simulations:

```powershell
python scripts/run_all_checks.py
```

PowerShell wrapper:

```powershell
.\scripts\run_all_checks.ps1
```

Or run individual steps:

```powershell
python -m unittest discover -s tests
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
python scripts/generate_charts.py
python scripts/build_results_data_dictionary.py
python scripts/build_github_metadata_report.py
python scripts/build_report_bundle.py
python scripts/score_pilot_results.py --input examples/pilot_candidate_summary.example.csv --output results/pilot_decision_scores.example.csv
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
python scripts/validate_artifacts.py
```

The shortlist excludes non-permissive or closed entries from the source conversation, including Claude Agent SDK and Codex app.

Generated result files:

- `results/deterministic_rankings.csv`
- `results/monte_carlo_summary.csv`
- `results/sensitivity_summary.csv`
- `results/category_scores.csv`
- `results/decision_shortlist.csv`
- `results/scenario_playbook_summary.csv`
- `results/scenario_weights.csv`
- `results/criteria_definitions.csv`
- `results/evidence_matrix.csv`
- `results/alternative_scorecards.csv`
- `results/score_driver_summary.csv`
- `results/criterion_spread_summary.csv`
- `results/implementation_effort_estimates.csv`
- `results/operational_cost_estimates.csv`
- `results/operational_fit_rankings.csv`
- `results/pilot_sample_size_estimates.csv`
- `results/evidence_gap_analysis.csv`
- `results/recommendation_rationale.csv`
- `results/risk_validation_matrix.csv`
- `results/custom_weights_example_rankings.csv`
- `results/local_artifact_reference_check.csv`
- `results/markdown_table_check.csv`
- `results/github_metadata_check.csv`
- `results/csv_schema_check.csv`
- `results/artifact_manifest.csv`
- `results/source_check.csv`
- `results/license_audit.csv`
- `results/regret_analysis.csv`
- `results/pareto_frontier.csv`
- `results/rank_stability.csv`
- `results/stress_test_summary.csv`
- `results/stress_test_rankings.csv`
- `results/uncertainty_stress_summary.csv`
- `results/uncertainty_stress_details.csv`
- `results/pilot_decision_scores.example.csv`
- `results/all_results.json`
