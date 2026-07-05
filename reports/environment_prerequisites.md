# Environment Prerequisites

Date: 2026-07-05

## Required

| Requirement | Notes |
|---|---|
| Python 3.12 or newer | The scripts use only the Python standard library. |
| PowerShell | Used by the documented Windows commands and `scripts/run_all_checks.ps1`. |
| Git | Required for reviewing diffs, committing, and pushing report updates. |

## Optional Live Checks

| Capability | Used by |
|---|---|
| Internet access | `scripts/check_sources.py` and `scripts/refresh_github_metadata.py` |
| GitHub API access | `scripts/refresh_github_metadata.py`; unauthenticated public API access is usually enough for the current 17 repos. |
| GitHub token with `workflow` scope | Only needed if copying `ci/validate-workflow.example.yml` into `.github/workflows/`. |

## Standard Commands

Run the offline workflow:

```powershell
python scripts/run_all_checks.py
```

Or from PowerShell:

```powershell
.\scripts\run_all_checks.ps1
```

Run live checks when network access is available:

```powershell
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
```

## Dependency Policy

The repository intentionally avoids third-party Python dependencies for the report-generation and validation path. That keeps the evaluation reproducible in a fresh Python environment and avoids mixing dependency installation risk into the analysis itself.
