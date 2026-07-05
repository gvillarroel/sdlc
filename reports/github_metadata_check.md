# GitHub Metadata Check

Date: 2026-07-05

## Objective

This live check compares the repository metadata in `data/alternatives.json` against the current public GitHub API response. It verifies that the canonical repositories still resolve and that the live SPDX license still matches the permissive license used by the report.

Generated output: `results/github_metadata_check.csv`

Run:

```powershell
python scripts/refresh_github_metadata.py --timeout 20
python scripts/build_github_metadata_report.py
```

## Latest Result

The latest run checked 17 GitHub repositories:

- 17 responded successfully.
- 0 license mismatches were detected.
- 0 repositories were archived.
- Star deltas were minor and do not change the recommendation.

Largest star deltas in the latest run:

| Candidate | Dataset stars | Live stars | Delta |
|---|---:|---:|---:|
| OpenCode | 182,587 | 182,610 | +23 |
| Omnigent | 6,304 | 6,314 | +10 |
| Deep Agents | 25,715 | 25,721 | +6 |
| Codex CLI | 95,651 | 95,656 | +5 |
| Sandcastle | 6,638 | 6,641 | +3 |
| Cline / Cline SDK | 64,315 | 64,318 | +3 |
| Aider | 47,082 | 47,084 | +2 |
| mini-SWE-agent | 5,578 | 5,579 | +1 |

## Interpretation

The live metadata check supports the dataset used in the report:

1. The included GitHub repositories are reachable.
2. Live GitHub license metadata matches the permissive license screen.
3. Current star changes are too small to affect the model.
4. Latest release tags mostly match the dataset; missing latest-release API responses for projects without GitHub Releases remain expected and are handled in `reports/evidence_gap_analysis.md`.

This check should be rerun before a final adoption decision or whenever the dataset is more than 30 days old.
