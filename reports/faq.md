# FAQ

Date: 2026-07-05

## Why is there no single winner?

The alternatives solve different problems. A research harness, a local pair-programming CLI, a secure CI runner, and an enterprise control plane should not be ranked as if they had one shared objective. The report recommends scenario-specific pilot clusters instead of a universal winner.

## Why were Claude Agent SDK and Codex app excluded?

The request asked for non-copyleft open-source alternatives. The shared discussion framed Claude Agent SDK as an official Anthropic/Claude-centric SDK rather than a permissive OSS candidate, and Codex app as a closed/commercial desktop application. Codex CLI remains included because it is Apache-2.0.

## Why include CLIs and frameworks in the same evaluation?

Adoption decisions often mix both. A team deciding how to build or operate AI coding agents may compare a library, a CLI, an SDK, and a control-plane starter because each can satisfy the same workflow at different integration depths.

## Can the weights be changed?

Yes. Edit `examples/pilot/custom_weights.example.json` and run:

```powershell
python scripts/rank_with_custom_weights.py
```

The example output is `results/custom_weights_example_rankings.csv`.

## Are the simulations live coding benchmarks?

No. They are multi-criteria decision simulations over scored evidence. They narrow the field, expose sensitivity, and identify pilot candidates. Live task execution belongs in the pilot described by `reports/pilot_protocol.md`.

## What should be rerun before a real adoption decision?

Run:

```powershell
python scripts/check_sources.py --timeout 20
python scripts/refresh_github_metadata.py --timeout 20
python scripts/run_all_checks.py
```

Then review `reports/validation_summary.md`, `results/source_check.csv`, and `results/github_metadata_check.csv`.

## Which projects should not be primary candidates right now?

Anchor, OmniAgent, and Omni Agent should be treated as reference material unless fresh evidence and a successful spike change their status. Omnigent is worth tracking, but the report treats it as a second-phase candidate because it is alpha and broad in scope.

## What is the minimum next action?

Pick the target scenario, choose 2-3 candidates from the relevant shortlist, run the security fixtures, execute the pilot task suite, and score the results with `scripts/score_pilot_results.py`.
