# Permissive Open-Source AI Orchestrator Alternatives

This repository contains a reproducible evaluation of permissive open-source alternatives from the shared ChatGPT discussion about AI coding-agent orchestrators.

Included artifacts:

- `data/alternatives.json` - curated dataset, source links, license filter, and 0-5 criterion scores.
- `data/pilot_tasks.json` - 20-task pilot suite for moving from simulated ranking to execution evidence.
- `data/risk_register.json` - actionable adoption risks, mitigations, and required evidence.
- `scripts/simulate_alternatives.py` - deterministic weighted ranking, Monte Carlo uncertainty simulation, and sensitivity analysis.
- `scripts/check_sources.py` - optional live source URL checker for the report and dataset.
- `scripts/license_audit.py` - permissive-license audit for included and excluded alternatives.
- `scripts/validate_artifacts.py` - offline consistency validation for generated artifacts and report references.
- `tests/test_simulation_model.py` - validation tests for the scoring model and dataset.
- `results/` - generated CSV and JSON simulation outputs, including category scorecards and a scenario shortlist.
- `templates/` - pilot run log, reviewer scorecard, and security gate checklist templates.
- `reports/ai_orchestrator_frameworks_report.md` - final English report.
- `reports/executive_brief.md` - short decision brief for quick review.
- `reports/methodology_appendix.md` - scoring formulas, Monte Carlo assumptions, and customization notes.
- `reports/artifact_index.md` - navigation guide for all report, data, result, template, and script artifacts.
- `ci/validate-workflow.example.yml` - GitHub Actions workflow template for tests, deterministic artifact regeneration, and offline artifact validation.

Run the checks and simulations:

```powershell
python -m unittest discover -s tests
python scripts/simulate_alternatives.py --trials 5000 --seed 7331
python scripts/license_audit.py
python scripts/check_sources.py --timeout 20
python scripts/validate_artifacts.py
```

The shortlist excludes non-permissive or closed entries from the source conversation, including Claude Agent SDK and Codex app.

Generated result files:

- `results/deterministic_rankings.csv`
- `results/monte_carlo_summary.csv`
- `results/sensitivity_summary.csv`
- `results/category_scores.csv`
- `results/decision_shortlist.csv`
- `results/scenario_weights.csv`
- `results/criteria_definitions.csv`
- `results/evidence_matrix.csv`
- `results/alternative_scorecards.csv`
- `results/source_check.csv`
- `results/license_audit.csv`
- `results/regret_analysis.csv`
- `results/pareto_frontier.csv`
- `results/rank_stability.csv`
- `results/all_results.json`
