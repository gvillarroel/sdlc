# Sandbox Evaluation Report

Date: 2026-07-05

## Executive Summary

Sandbox choice is not a single technology decision. For AI coding agents, the right boundary depends on whether the workload is local development, autonomous pull requests, arbitrary user code, high-scale evaluations, or enterprise self-hosted control.

The simulation ranks sandbox options across five scenarios using 14 criteria: isolation strength, workspace reset, network control, secret boundary, filesystem mount control, dependency support, agent SDK fit, observability, startup speed, horizontal scale, self-hosting control, operational ease, cost predictability, and maturity. Local and self-hosted scenarios also apply an explicit managed-service dependency penalty.

Generated outputs:

| File | Purpose |
|---|---|
| `results/sandbox_deterministic_rankings.csv` | Weighted sandbox ranking by scenario. |
| `results/sandbox_monte_carlo_summary.csv` | Ranking stability under score and weight uncertainty. |
| `results/sandbox_threat_coverage.csv` | Threat-to-control coverage by sandbox option. |
| `results/sandbox_decision_matrix.csv` | Scenario shortlist with recommendation posture and caveats. |
| `results/sandbox_source_matrix.csv` | Official source URLs used by the sandbox dataset. |

## Recommendations

| Scenario | Recommendation | Why |
|---|---|---|
| Local developer agents | Flue virtual sandbox / Daytona sandboxes / Kubernetes hardened pods | No decisive single winner; run a head-to-head pilot because the top cluster is close under uncertainty. |
| Autonomous PR security | Daytona sandboxes | Score 4.165; 94% top-3 stability; Agent workflows that need a developer-like machine with programmatic file and command control. |
| Untrusted user code | Daytona sandboxes | Score 4.199; 93% top-3 stability; Agent workflows that need a developer-like machine with programmatic file and command control. |
| Evals and RL scale | Daytona sandboxes | Score 4.264; 99% top-3 stability; Agent workflows that need a developer-like machine with programmatic file and command control. |
| Enterprise self-hosted | Kubernetes hardened pods | Score 4.082; 99% top-3 stability; Enterprise platform teams that already operate Kubernetes and need central policy, admission, and audit controls. |

## Scenario Decision Matrix

| Scenario | Rank | Sandbox | Type | Score | Mean rank | Win | Top-3 | Posture | Main caveat |
|---|---:|---|---|---:|---:|---:|---:|---|---|
| Local developer agents | 1 | Flue virtual sandbox | agent_virtual_workspace | 3.965 | 3.67 | 31% | 60% | Pilot head-to-head | The virtual sandbox is not equivalent to hard OS isolation for arbitrary untrusted code execution. |
| Local developer agents | 2 | Daytona sandboxes | managed_agent_sandbox | 3.962 | 3.37 | 27% | 62% | Pilot head-to-head | Validate actual isolation, tenancy, credential flow, and pricing under sustained task volume. |
| Local developer agents | 3 | Kubernetes hardened pods | orchestrated_container_policy | 3.956 | 3.15 | 22% | 65% | Pilot head-to-head | A hardened pod is still container isolation unless combined with gVisor, Kata, or VM-backed runtime classes; policy drift is a real risk. |
| Local developer agents | 4 | Docker rootless containers | container_runtime | 3.922 | 4.65 | 8% | 36% | Fallback or benchmark | Container escapes remain a kernel/runtime risk; bind mounts, Docker socket exposure, privileged flags, and rootless-in-container workarounds can erase much of the benefit. |
| Local developer agents | 5 | Podman rootless containers | container_runtime | 3.896 | 5.96 | 3% | 19% | Watchlist | Rootless networking, storage drivers, UID/GID mapping, and enterprise desktop support need deliberate setup. |
| Autonomous PR security | 1 | Daytona sandboxes | managed_agent_sandbox | 4.165 | 1.61 | 64% | 94% | Primary candidate | Validate actual isolation, tenancy, credential flow, and pricing under sustained task volume. |
| Autonomous PR security | 2 | E2B sandboxes | managed_agent_sandbox | 4.114 | 2.44 | 25% | 82% | Pilot head-to-head | Managed-service dependency, data residency, cost, and secret-handling model must pass procurement and security review. |
| Autonomous PR security | 3 | Kubernetes hardened pods | orchestrated_container_policy | 4.045 | 4.04 | 4% | 43% | Fallback or benchmark | A hardened pod is still container isolation unless combined with gVisor, Kata, or VM-backed runtime classes; policy drift is a real risk. |
| Autonomous PR security | 4 | Modal Sandboxes | managed_cloud_sandbox | 4.044 | 4.43 | 4% | 38% | Fallback or benchmark | Managed-service dependency and platform-specific observability/cost model must match the workload. |
| Autonomous PR security | 5 | Firecracker microVMs | microvm_runtime | 3.995 | 6.08 | 0% | 10% | Security architecture option | It is a low-level building block: image lifecycle, networking, snapshots, storage, API service, and observability must be engineered. |
| Untrusted user code | 1 | Daytona sandboxes | managed_agent_sandbox | 4.199 | 1.74 | 57% | 93% | Primary candidate | Validate actual isolation, tenancy, credential flow, and pricing under sustained task volume. |
| Untrusted user code | 2 | E2B sandboxes | managed_agent_sandbox | 4.158 | 2.43 | 27% | 82% | Pilot head-to-head | Managed-service dependency, data residency, cost, and secret-handling model must pass procurement and security review. |
| Untrusted user code | 3 | Modal Sandboxes | managed_cloud_sandbox | 4.121 | 3.35 | 11% | 62% | Pilot head-to-head | Managed-service dependency and platform-specific observability/cost model must match the workload. |
| Untrusted user code | 4 | Kubernetes hardened pods | orchestrated_container_policy | 4.051 | 5.24 | 1% | 18% | Watchlist | A hardened pod is still container isolation unless combined with gVisor, Kata, or VM-backed runtime classes; policy drift is a real risk. |
| Untrusted user code | 5 | Firecracker microVMs | microvm_runtime | 4.045 | 5.62 | 0% | 12% | Security architecture option | It is a low-level building block: image lifecycle, networking, snapshots, storage, API service, and observability must be engineered. |
| Evals and RL scale | 1 | Daytona sandboxes | managed_agent_sandbox | 4.264 | 1.46 | 67% | 99% | Primary candidate | Validate actual isolation, tenancy, credential flow, and pricing under sustained task volume. |
| Evals and RL scale | 2 | Modal Sandboxes | managed_cloud_sandbox | 4.197 | 2.37 | 17% | 93% | Pilot head-to-head | Managed-service dependency and platform-specific observability/cost model must match the workload. |
| Evals and RL scale | 3 | E2B sandboxes | managed_agent_sandbox | 4.195 | 2.41 | 16% | 92% | Pilot head-to-head | Managed-service dependency, data residency, cost, and secret-handling model must pass procurement and security review. |
| Evals and RL scale | 4 | Vercel Sandbox | managed_microvm_sandbox | 4.032 | 5.59 | 0% | 6% | Watchlist | Platform dependency, region/control-plane constraints, and whether the product's network/secret policy is sufficient for enterprise autonomy. |
| Evals and RL scale | 5 | OpenHands runtime API sandbox | agent_runtime_sandbox | 4.012 | 6.07 | 0% | 4% | Watchlist | Runtime service availability, image control, credential handling, and the exact container isolation policy must be verified. |
| Enterprise self-hosted | 1 | Kubernetes hardened pods | orchestrated_container_policy | 4.082 | 1.41 | 68% | 99% | Primary candidate | A hardened pod is still container isolation unless combined with gVisor, Kata, or VM-backed runtime classes; policy drift is a real risk. |
| Enterprise self-hosted | 2 | Firecracker microVMs | microvm_runtime | 4.046 | 2.05 | 26% | 95% | Pilot head-to-head | It is a low-level building block: image lifecycle, networking, snapshots, storage, API service, and observability must be engineered. |
| Enterprise self-hosted | 3 | Kata Containers | vm_backed_container_runtime | 3.984 | 3.17 | 5% | 70% | Pilot head-to-head | RuntimeClass, image, networking, Kubernetes integration, performance overhead, and VMM backend choices add operational work. |
| Enterprise self-hosted | 4 | gVisor runsc | userspace_kernel | 3.918 | 4.65 | 0% | 17% | Watchlist | Syscall compatibility, filesystem performance, and debugging differences must be tested against real build/test workloads. |
| Enterprise self-hosted | 5 | Flue virtual sandbox | agent_virtual_workspace | 3.880 | 5.78 | 1% | 12% | Watchlist | The virtual sandbox is not equivalent to hard OS isolation for arbitrary untrusted code execution. |

## Sandbox Taxonomy

| Type | What it means | Typical examples |
|---|---|---|
| Process sandbox | Constrains one command or process using namespaces, cgroups, seccomp, chroot, or similar controls. | nsjail, bubblewrap |
| Container runtime | Provides disposable build/test environments with familiar images and tooling. | Docker rootless, Podman rootless |
| Userspace kernel | Inserts an application kernel between the workload and host kernel. | gVisor runsc |
| MicroVM or VM-backed containers | Uses hardware virtualization boundaries while preserving some container ergonomics. | Firecracker, Kata Containers, Vercel Sandbox |
| Managed agent sandbox | Provides API-driven sandbox lifecycle for agents. | E2B, Daytona, Modal, OpenHands runtime API |
| Agent control sandbox | Constrains an agent's tool calls through local workspace, network, and approval policy. | Codex sandbox, framework-level providers |

## Threat Coverage Highlights

| Threat | Strongest options | Weakest pattern to avoid |
|---|---|---|
| Agent-written code reads or modifies host files outside the intended workspace. | Firecracker microVMs; Vercel Sandbox; Daytona sandboxes | Docker rootless containers |
| Generated code scans private services or exfiltrates data through unrestricted outbound network access. | Kubernetes hardened pods; Codex sandbox and approvals; Daytona sandboxes | nsjail or bubblewrap process sandbox |
| Agent commands access API keys, CI secrets, cloud credentials, package tokens, or SSH material. | Codex sandbox and approvals; Daytona sandboxes; Kubernetes hardened pods | Docker rootless containers |
| A malicious dependency or generated program exploits the runtime boundary. | Firecracker microVMs; E2B sandboxes; Modal Sandboxes | Flue virtual sandbox |
| Long-running agent loops consume sandbox minutes, tokens, storage, or queue slots. | Flue virtual sandbox; Daytona sandboxes; Kubernetes hardened pods | nsjail or bubblewrap process sandbox |

## Implementation Guidance

1. Do not treat approval prompts as equivalent to hard isolation. Approval policy is useful, but it does not replace a host, kernel, filesystem, or network boundary.
2. Default to disposable workspaces. Long-lived sandboxes should be explicit exceptions with retention, quota, and credential rules.
3. Keep credentials outside the sandbox until a specific tool call needs them, and prefer short-lived scoped credentials.
4. Disable network by default for autonomous code execution, then add domain allowlists for package registries, Git remotes, and required APIs.
5. For arbitrary user code, prefer microVM, userspace-kernel, VM-backed container, or managed sandbox options over plain containers.
6. For local developer agents, combine rootless containers or Codex-style workspace/network policies with explicit mount rules and review checkpoints.
7. For self-hosted enterprise deployments, test Kubernetes hardened pods alone and with gVisor or Kata RuntimeClass before accepting container isolation as sufficient.

## Source Notes

The dataset uses official documentation and source repositories for Docker, Podman, gVisor, Firecracker, Kata Containers, nsjail, bubblewrap, E2B, Daytona, Modal, Vercel, OpenHands, Codex, Sandcastle, Flue, and Kubernetes. See `results/sandbox_source_matrix.csv` for the exact URLs.

## Validation Boundary

This report is a screening simulation. It does not prove that a particular hosted sandbox prevents escapes, protects secrets, or meets compliance needs. Before production use, run the security fixtures in `data/security_evaluation_fixtures.json`, add sandbox-specific escape and exfiltration tests, capture logs in `templates/pilot_run_log.csv`, and review the provider's legal and security documentation.
