# Report Library

This directory contains the decision narratives, technical analysis, methodology, pilot guidance, and validation records for the AI coding-agent orchestrator evaluation.

## Primary Reading Path

| Order | Report | Purpose | Status |
|---:|---|---|---|
| 1 | [`executive_brief.md`](executive_brief.md) | Fast decision summary and recommended next step | Authored |
| 2 | [`final_global_report.md`](final_global_report.md) | Primary narrative across candidates, security, market, maintenance, and pilot planning | Authored |
| 3 | [`ai_orchestrator_frameworks_report.md`](ai_orchestrator_frameworks_report.md) | Detailed candidate evaluation, scoring evidence, scenario results, and caveats | Authored |
| 4 | [`methodology_appendix.md`](methodology_appendix.md) | Scoring formulas, uncertainty model, and customization guidance | Authored |
| 5 | [`pilot_protocol.md`](pilot_protocol.md) | Controlled process for replacing screening assumptions with execution evidence | Authored |

For a single offline document, use [`final_report_bundle.md`](final_report_bundle.md). It is generated from the source reports and should not be edited directly.

## Report Types

### Decision and Executive Reports

| Report | Question answered | Status |
|---|---|---|
| [`executive_brief.md`](executive_brief.md) | What should decision-makers know first? | Authored |
| [`adoption_decision_record.md`](adoption_decision_record.md) | What decision and no-go conditions are proposed? | Authored |
| [`candidate_taxonomy.md`](candidate_taxonomy.md) | Which adoption shape does each candidate represent? | Authored |
| [`decision_tree.md`](decision_tree.md) | Which shortlist fits a stated operating need? | Authored |
| [`recommendation_rationale.md`](recommendation_rationale.md) | Why does each scenario shortlist have its current order? | Generated |
| [`scenario_playbooks.md`](scenario_playbooks.md) | How should each scenario move from shortlist to pilot? | Generated |
| [`presentation_outline.md`](presentation_outline.md) | How can the findings be presented to stakeholders? | Authored |
| [`exclusions.md`](exclusions.md) | Why were boundary cases excluded or retained? | Authored |

### Methodology and Quantitative Analysis

| Report | Focus | Status |
|---|---|---|
| [`methodology_appendix.md`](methodology_appendix.md) | Scoring, normalization, Monte Carlo, sensitivity, and custom weights | Authored |
| [`simulation_assumptions.md`](simulation_assumptions.md) | Threats to validity and deterministic/uncertainty stress tests | Authored |
| [`score_driver_summary.md`](score_driver_summary.md) | Candidate strengths, weaknesses, and high-spread criteria | Generated |
| [`evidence_gap_analysis.md`](evidence_gap_analysis.md) | Low-confidence, immature, or stale evidence risks | Generated |
| [`operational_cost_model.md`](operational_cost_model.md) | Relative operating hours, token pressure, latency risk, and adjusted fit | Generated |

### Security, Sandboxing, and Risk

| Report | Focus | Status |
|---|---|---|
| [`sandbox_report.md`](sandbox_report.md) | Isolation options, threat coverage, and scenario-specific sandbox posture | Generated |
| [`security_evaluation_fixtures.md`](security_evaluation_fixtures.md) | Reusable prompt-injection, secret, network, and boundary fixtures | Authored |
| [`risk_validation_matrix.md`](risk_validation_matrix.md) | Required pilot evidence and pass conditions for each adoption risk | Generated |
| [`residual_risks.md`](residual_risks.md) | Risks that remain after repository-level screening | Authored |
| [`ai_code_trust_matrix.md`](ai_code_trust_matrix.md) | When code must be read and when verification gates may carry trust | Authored |

### Pilot and Implementation

| Report | Focus | Status |
|---|---|---|
| [`pilot_protocol.md`](pilot_protocol.md) | Task execution, evidence capture, gates, and decision rules | Authored |
| [`pilot_sample_size.md`](pilot_sample_size.md) | Task-count estimates for close-candidate comparisons | Generated |
| [`implementation_blueprints.md`](implementation_blueprints.md) | Initial integration slices for leading candidates | Authored |
| [`environment_prerequisites.md`](environment_prerequisites.md) | Local, CI, live-check, and optional POC requirements | Authored |

### Market, Maintenance, and Product Strategy

| Report | Focus | Status |
|---|---|---|
| [`market_maintenance_synthesis.md`](market_maintenance_synthesis.md) | Integrated go/no-go model across market, maintenance, and trust | Authored |
| [`market_entry_barriers_shift.md`](market_entry_barriers_shift.md) | How AI-native creation changes entry barriers and defensibility | Authored |
| [`market_fragmentation_user_share.md`](market_fragmentation_user_share.md) | Fragmentation, retention, and competition for workflow share | Authored |
| [`long_term_ai_app_maintenance.md`](long_term_ai_app_maintenance.md) | Support capacity and technical-debt risk for AI-built applications | Authored |

### Internal Benchmark Research

| Report | Focus | Status |
|---|---|---|
| [`internal_benchmark_harnesses.md`](internal_benchmark_harnesses.md) | Architecture and governance for private agent-harness benchmarks | Authored |
| [`internal_benchmark_papers.md`](internal_benchmark_papers.md) | Prioritized, annotated research bibliography | Authored |

### Reference, Traceability, and Maintenance

| Report | Purpose | Status |
|---|---|---|
| [`faq.md`](faq.md) | Scope, weighting, exclusion, and pilot answers | Authored |
| [`glossary.md`](glossary.md) | Common scoring, security, simulation, and orchestration terms | Authored |
| [`system_diagrams.md`](system_diagrams.md) | System, data-flow, decision-flow, and validation diagrams | Authored |
| [`requirements_traceability.md`](requirements_traceability.md) | Requirement-to-artifact coverage | Authored |
| [`validation_summary.md`](validation_summary.md) | Latest human-readable validation status | Authored snapshot |
| [`results_data_dictionary.md`](results_data_dictionary.md) | Column definitions for generated CSV outputs | Generated |
| [`github_metadata_check.md`](github_metadata_check.md) | Latest repository metadata verification summary | Generated |
| [`maintenance_guide.md`](maintenance_guide.md) | Refresh order, dependencies, and review procedure | Authored |
| [`release_notes.md`](release_notes.md) | Reviewer-oriented delivery summary | Authored snapshot |

## Structured Inputs

All authoritative machine-readable inputs live under `data/`.

| Input family | Files |
|---|---|
| Candidate catalog and taxonomy | `data/alternatives.json`, `data/candidate_taxonomy.json` |
| Scoring and scenario selection | `data/scoring_rubric.json`, `data/scenario_profiles.json`, `data/decision_tree.json` |
| Simulation and operating assumptions | `data/simulation_assumptions.json`, `data/operational_cost_model.json` |
| Pilot planning | `data/pilot_tasks.json`, `data/pilot_decision_model.json`, `data/pilot_sample_size_model.json` |
| Security and risk | `data/risk_register.json`, `data/security_evaluation_fixtures.json`, `data/sandbox_evaluation.json` |
| Traceability | `data/traceability_matrix.json` |
| Market, maintenance, and trust bibliography | `data/sources/market_maintenance_source_matrix.csv` |

## Generated Results

Everything under `results/` is reproducible output. Do not edit these files manually.

| Result family | Files |
|---|---|
| Complete machine output | `results/all_results.json` |
| Base rankings and scenario fit | `results/deterministic_rankings.csv`, `results/monte_carlo_summary.csv`, `results/sensitivity_summary.csv`, `results/category_scores.csv`, `results/decision_shortlist.csv`, `results/scenario_weights.csv` |
| Robustness and stability | `results/regret_analysis.csv`, `results/pareto_frontier.csv`, `results/rank_stability.csv`, `results/stress_test_summary.csv`, `results/stress_test_rankings.csv`, `results/uncertainty_stress_summary.csv`, `results/uncertainty_stress_details.csv` |
| Candidate evidence and explanation | `results/criteria_definitions.csv`, `results/evidence_matrix.csv`, `results/alternative_scorecards.csv`, `results/score_driver_summary.csv`, `results/criterion_spread_summary.csv`, `results/evidence_gap_analysis.csv` |
| Operations and implementation | `results/implementation_effort_estimates.csv`, `results/operational_cost_estimates.csv`, `results/operational_fit_rankings.csv` |
| Pilot and recommendation outputs | `results/scenario_playbook_summary.csv`, `results/pilot_sample_size_estimates.csv`, `results/pilot_decision_scores.example.csv`, `results/recommendation_rationale.csv`, `results/risk_validation_matrix.csv`, `results/custom_weights_example_rankings.csv` |
| Sandbox evaluation | `results/sandbox_deterministic_rankings.csv`, `results/sandbox_monte_carlo_summary.csv`, `results/sandbox_threat_coverage.csv`, `results/sandbox_decision_matrix.csv`, `results/sandbox_source_matrix.csv` |
| Source and license checks | `results/source_check.csv`, `results/github_metadata_check.csv`, `results/license_audit.csv` |
| Repository QA | `results/local_artifact_reference_check.csv`, `results/markdown_table_check.csv`, `results/csv_schema_check.csv`, `results/artifact_manifest.csv` |

## Pilot Resources

| Need | Artifact |
|---|---|
| Select a scenario and priorities | `templates/scenario_selection_workshop.md` |
| Record task-level execution | `templates/pilot_run_log.csv` |
| Review generated patches | `templates/reviewer_scorecard.md` |
| Apply security gates | `templates/security_gate_checklist.md` |
| Prepare candidate-level scoring input | `templates/pilot_candidate_summary.csv` |
| Start from a completed example | `examples/pilot/candidate_summary.example.csv` |
| Implement a common adapter | `examples/pilot/adapter.py` |
| Test stakeholder-specific weights | `examples/pilot/custom_weights.example.json` |

## Regeneration and Validation

Run the complete offline workflow from the repository root:

```powershell
python scripts/run_all_checks.py
```

The workflow regenerates results, generated reports, SVG charts, validation CSVs, and the artifact manifest. Optional live freshness checks are:

```powershell
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
```

For dependency order and maintenance rules, see [`maintenance_guide.md`](maintenance_guide.md).
