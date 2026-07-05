# Artifact Index

Date: 2026-07-05

Use this index to choose the right file quickly.

## Read First

| Need | Artifact |
|---|---|
| Quick decision summary | `reports/executive_brief.md` |
| Full analysis | `reports/ai_orchestrator_frameworks_report.md` |
| Scoring formula and assumptions | `reports/methodology_appendix.md` |
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
| Adoption risk register | `data/risk_register.json` |

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
| Model weights | `results/scenario_weights.csv` |
| Criteria definitions | `results/criteria_definitions.csv` |
| Source/evidence table | `results/evidence_matrix.csv` |
| Alternative scorecards | `results/alternative_scorecards.csv` |
| License audit | `results/license_audit.csv` |
| URL health check | `results/source_check.csv` |
| Complete machine-readable output | `results/all_results.json` |

## Pilot Execution

| Need | Artifact |
|---|---|
| Capture candidate/task metrics | `templates/pilot_run_log.csv` |
| Human code-review assessment | `templates/reviewer_scorecard.md` |
| Security gate assessment | `templates/security_gate_checklist.md` |

## Scripts

| Need | Artifact |
|---|---|
| Regenerate rankings and simulations | `scripts/simulate_alternatives.py` |
| Regenerate license audit | `scripts/license_audit.py` |
| Check external source URLs | `scripts/check_sources.py` |
| Validate generated artifacts offline | `scripts/validate_artifacts.py` |
| Generate report SVG charts | `scripts/generate_charts.py` |

## Maintenance

Run the core validation set:

```powershell
python -m unittest discover -s tests
python scripts/simulate_alternatives.py --trials 5000 --seed 7331
python scripts/license_audit.py
python scripts/validate_artifacts.py
```

Run live source verification when network access is available:

```powershell
python scripts/check_sources.py --timeout 20
```
