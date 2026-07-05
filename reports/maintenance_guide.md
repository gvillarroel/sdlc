# Maintenance Guide

Date: 2026-07-05

## When To Refresh

Refresh the repository when any of these are true:

- More than 30 days have passed since the last source and GitHub metadata checks.
- A candidate has a major release, license change, repository move, or archive notice.
- A stakeholder wants different scenario priorities.
- Pilot results replace subjective scores.
- A new alternative from the source discussion becomes relevant.

## Standard Refresh Procedure

1. Refresh live evidence:

```powershell
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
```

2. Edit input data if evidence changed:

- `data/alternatives.json`
- `data/scoring_rubric.json`
- `data/scenario_profiles.json`
- `data/pilot_sample_size_model.json`
- `data/risk_register.json`
- `data/simulation_assumptions.json`
- `data/operational_cost_model.json`

3. Regenerate and validate offline artifacts:

```powershell
python scripts/run_all_checks.py
```

4. Review generated changes:

```powershell
git diff --stat
git diff --check
```

5. Re-read the decision documents:

- `reports/executive_brief.md`
- `reports/adoption_decision_record.md`
- `reports/simulation_assumptions.md`
- `reports/operational_cost_model.md`
- `reports/pilot_sample_size.md`
- `reports/evidence_gap_analysis.md`
- `reports/validation_summary.md`

## Updating Scores

When changing 0-5 criterion scores:

1. Update the score in `data/alternatives.json`.
2. Check the corresponding anchor in `data/scoring_rubric.json`.
3. Add or update the evidence note in `implementation_notes` or `risk_notes`.
4. Rerun `python scripts/run_all_checks.py`.
5. Review deterministic rank, Monte Carlo stability, stress-test output, regret, and Pareto changes.

Do not change scores only to force a preferred winner. If a score is uncertain, prefer updating `source_confidence`, stress-testing the assumption, or capturing pilot evidence.

## Adding A Candidate

Minimum required work:

1. Add the candidate to `data/alternatives.json` with MIT or Apache-2.0 license evidence.
2. Add source URLs and repository metadata.
3. Score every criterion.
4. Run `python scripts/license_audit.py`.
5. Run `python scripts/run_all_checks.py`.
6. Update narrative sections if the candidate enters a top cluster or changes a recommendation.

## Changing Scenario Weights

For exploratory changes, use:

```powershell
python scripts/rank_with_custom_weights.py --weights examples/custom_weights.example.json
```

For canonical scenario changes, edit the `SCENARIOS` map in `scripts/simulate_alternatives.py`, then rerun the full workflow.

## Incorporating Pilot Results

After a real pilot:

1. Fill `templates/pilot_run_log.csv`.
2. Summarize candidate-level metrics in a file shaped like `examples/pilot_candidate_summary.example.csv`.
3. Run:

```powershell
python scripts/score_pilot_results.py --input examples/pilot_candidate_summary.example.csv --output results/pilot_decision_scores.example.csv
```

4. Update `reports/adoption_decision_record.md` from Proposed to Accepted, Rejected, or Deferred.
5. Replace subjective notes in the main report with measured pilot evidence where appropriate.

## Release Checklist

Before sharing a refreshed report:

- `python scripts/run_all_checks.py` passes.
- `python scripts/check_sources.py --timeout 20` passes.
- `python scripts/refresh_github_metadata.py --timeout 20` passes.
- `git diff --check` passes.
- `reports/final_report_bundle.md` is regenerated.
- `reports/validation_summary.md` reflects the current test and schema counts.
- No generated `__pycache__` directories are left in the working tree.
