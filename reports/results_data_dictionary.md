# Results Data Dictionary

Date: 2026-07-05

This generated dictionary summarizes the CSV outputs in `results/`. Expected columns come from `scripts/validate_csv_schemas.py`.

## `alternative_scorecards.csv`

Wide scorecard of all 0-5 criterion scores.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `license` |
| `maturity_level` |
| `source_confidence` |
| `implementation_ease` |
| `maturity` |
| `provider_portability` |
| `sandbox_isolation` |
| `persistence_memory` |
| `multi_agent` |
| `human_control` |
| `ci_pr` |
| `observability` |
| `security_governance` |
| `extensibility` |
| `deployment_flexibility` |
| `coding_fit` |
| `research_reproducibility` |

## `artifact_manifest.csv`

Generated CSV artifact.

| Column |
|---|
| `path` |
| `size_bytes` |
| `sha256` |

## `category_scores.csv`

Criterion-group scorecards independent of scenario weights.

| Column |
|---|
| `category` |
| `rank` |
| `alternative_id` |
| `alternative` |
| `score` |

## `criteria_definitions.csv`

Human-readable scoring criterion definitions.

| Column |
|---|
| `criterion` |
| `definition` |

## `criterion_spread_summary.csv`

Per-criterion score spread and candidate leaders or laggards.

| Column |
|---|
| `criterion` |
| `mean_score` |
| `min_score` |
| `max_score` |
| `score_spread` |
| `leaders` |
| `laggards` |

## `csv_schema_check.csv`

Generated CSV schema validation output.

| Column |
|---|
| `filename` |
| `ok` |
| `missing_columns` |
| `extra_columns` |
| `actual_column_count` |
| `required_column_count` |

## `custom_weights_example_rankings.csv`

Example deterministic rankings from custom weights.

| Column |
|---|
| `scenario` |
| `rank` |
| `alternative_id` |
| `alternative` |
| `score` |

## `decision_shortlist.csv`

Scenario shortlist combining deterministic and Monte Carlo evidence.

| Column |
|---|
| `scenario` |
| `deterministic_rank` |
| `alternative_id` |
| `alternative` |
| `deterministic_score` |
| `monte_carlo_mean_score` |
| `monte_carlo_mean_rank` |
| `win_rate` |
| `top3_rate` |

## `deterministic_rankings.csv`

Base weighted rankings by scenario.

| Column |
|---|
| `scenario` |
| `rank` |
| `alternative_id` |
| `alternative` |
| `score` |

## `evidence_gap_analysis.csv`

Evidence risk signals and mitigation notes.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `evidence_risk_score` |
| `evidence_risk_band` |
| `gaps` |
| `mitigation` |
| `adoption_implication` |

## `evidence_matrix.csv`

Source, metadata, notes, and evidence URLs by alternative.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `repo` |
| `url` |
| `license` |
| `primary_language` |
| `maturity_level` |
| `source_confidence` |
| `stars` |
| `created_at` |
| `last_pushed_at` |
| `latest_release` |
| `summary` |
| `implementation_notes` |
| `risk_notes` |
| `evidence_urls` |

## `github_metadata_check.csv`

Live GitHub repository metadata check.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `repo` |
| `ok` |
| `dataset_license` |
| `live_license` |
| `license_matches` |
| `archived` |

## `implementation_effort_estimates.csv`

Prototype and hardening effort estimates.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `prototype_complexity_score` |
| `prototype_effort` |
| `hardening_complexity_score` |
| `hardening_effort` |
| `first_slice` |
| `adoption_note` |

## `license_audit.csv`

Permissive-license audit.

| Column |
|---|
| `alternative` |
| `status` |
| `is_permissive` |
| `license` |
| `repo` |
| `url` |
| `reason` |

## `local_artifact_reference_check.csv`

Local Markdown artifact reference check.

| Column |
|---|
| `source_file` |
| `reference` |
| `resolved_path` |
| `exists` |

## `monte_carlo_summary.csv`

Monte Carlo score and rank stability by scenario.

| Column |
|---|
| `scenario` |
| `alternative_id` |
| `alternative` |
| `mean_score` |
| `p10_score` |
| `p90_score` |
| `mean_rank` |
| `win_rate` |
| `top3_rate` |
| `trials` |

## `operational_cost_estimates.csv`

Relative monthly operating effort, token pressure, latency risk, and cost-risk bands.

| Column |
|---|
| `operating_profile` |
| `operating_profile_name` |
| `alternative_id` |
| `alternative` |
| `monthly_task_volume` |
| `review_hours` |
| `admin_hours` |
| `governance_hours` |
| `failure_buffer_hours` |
| `monthly_operational_hours` |
| `hours_per_task` |
| `relative_token_pressure` |
| `latency_risk_score` |
| `operational_friction_score` |
| `cost_risk_band` |
| `main_cost_driver` |

## `operational_fit_rankings.csv`

Scenario rankings adjusted by operating-profile friction.

| Column |
|---|
| `scenario` |
| `operating_profile` |
| `rank` |
| `alternative_id` |
| `alternative` |
| `simulation_rank` |
| `simulation_score` |
| `operational_friction_score` |
| `monthly_operational_hours` |
| `relative_token_pressure` |
| `latency_risk_score` |
| `adjusted_score` |
| `rank_delta_vs_simulation` |

## `pareto_frontier.csv`

Raw-criteria Pareto dominance analysis.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `is_pareto_frontier` |
| `dominated_by_count` |
| `dominated_by` |

## `pilot_decision_scores.example.csv`

Example post-pilot decision score output.

| Column |
|---|
| `rank` |
| `candidate` |
| `eligible` |
| `final_score` |
| `gate_failures` |
| `task_success_rate` |
| `review_acceptance_rate` |
| `safety_score` |
| `artifact_completeness` |
| `cost_latency_score` |
| `setup_maintenance_score` |
| `notes` |

## `pilot_sample_size_estimates.csv`

Pilot task-count simulation for separating close shortlist candidates.

| Column |
|---|
| `scenario` |
| `top_candidate` |
| `comparison_rank` |
| `comparison_candidate` |
| `score_gap` |
| `estimated_top_success_rate` |
| `estimated_comparison_success_rate` |
| `tasks_per_candidate` |
| `simulation_trials` |
| `top_wins_probability` |
| `tie_probability` |
| `decision_confidence_target` |
| `recommendation` |

## `rank_stability.csv`

Cross-scenario deterministic and Monte Carlo rank stability.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `mean_deterministic_rank` |
| `best_deterministic_rank` |
| `worst_deterministic_rank` |
| `top3_scenarios` |
| `top3_scenario_rate` |
| `mean_monte_carlo_rank` |
| `mean_top3_rate` |

## `regret_analysis.csv`

Score gaps versus scenario winners.

| Column |
|---|
| `scenario` |
| `alternative_id` |
| `alternative` |
| `deterministic_rank` |
| `deterministic_score` |
| `regret_vs_best` |
| `monte_carlo_mean_rank` |
| `win_rate` |
| `top3_rate` |

## `scenario_weights.csv`

Raw and normalized weights by scenario and criterion.

| Column |
|---|
| `scenario` |
| `criterion` |
| `raw_weight` |
| `normalized_weight` |

## `score_driver_summary.csv`

Per-candidate top strengths, weaknesses, and best or worst scenario ranks.

| Column |
|---|
| `alternative_id` |
| `alternative` |
| `maturity_level` |
| `source_confidence` |
| `top_strengths` |
| `top_weaknesses` |
| `best_scenario` |
| `best_rank` |
| `worst_scenario` |
| `worst_rank` |
| `mean_score` |
| `score_spread` |

## `sensitivity_summary.csv`

Criterion weight sensitivity results.

| Column |
|---|
| `scenario` |
| `criterion` |
| `base_top` |
| `half_weight_top` |
| `double_weight_top` |
| `half_weight_top3_overlap` |
| `double_weight_top3_overlap` |

## `source_check.csv`

Live external source URL check.

| Column |
|---|
| `url` |
| `ok` |
| `status` |
| `elapsed_ms` |
| `final_url` |
| `error` |

## `stress_test_rankings.csv`

Full deterministic rankings under stress cases.

| Column |
|---|
| `stress_case` |
| `scenario` |
| `rank` |
| `alternative_id` |
| `alternative` |
| `score` |

## `stress_test_summary.csv`

Deterministic stress-test summary.

| Column |
|---|
| `stress_case` |
| `scenario` |
| `rank1` |
| `rank2` |
| `rank3` |
| `baseline_rank1` |
| `rank1_changed` |
| `top3_overlap` |
| `rank1_margin` |

## `uncertainty_stress_details.csv`

Full Monte Carlo rows under alternate uncertainty cases.

| Column |
|---|
| `uncertainty_case` |
| `scenario` |
| `alternative_id` |
| `alternative` |
| `mean_score` |
| `mean_rank` |
| `win_rate` |
| `top3_rate` |
| `trials` |

## `uncertainty_stress_summary.csv`

Monte Carlo summary under alternate uncertainty cases.

| Column |
|---|
| `uncertainty_case` |
| `scenario` |
| `weight_sigma` |
| `score_sigma_multiplier` |
| `rank1` |
| `rank2` |
| `baseline_rank1` |
| `rank1_changed` |
| `win_rate` |
| `top3_rate` |
| `win_rate_margin` |
| `trials` |
