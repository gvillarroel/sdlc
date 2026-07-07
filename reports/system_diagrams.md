# System Diagrams

Date: 2026-07-06

These diagrams connect the repository concepts, tools, generated artifacts, and validation loops. Read every arrow as "feeds", "generates", "validates", or "informs" depending on the label.

## 1. Full Connected Map

This is the highest-level map: every repository area connects back to the same decision evidence loop.

```mermaid
flowchart LR
    Request["Original evaluation request"]
    Scope["Permissive OSS orchestrator scope"]
    Concepts["Concept model: candidates, criteria, scenarios, risks, pilots"]
    Inputs["data/*.json"]
    Tools["scripts/*.py and scripts/*.ps1"]
    Results["results/*.csv and results/all_results.json"]
    Reports["reports/*.md and reports/assets/*.svg"]
    Templates["templates/*.md and templates/*.csv"]
    Examples["examples/*.json, *.csv, *.py"]
    Tests["tests/*.py"]
    CI["ci/validate-workflow.example.yml"]
    Decision["Adoption decision, shortlist, pilot plan, no-go gates"]
    Maintenance["Maintenance refresh workflow"]

    Request --> Scope --> Concepts
    Concepts --> Inputs
    Inputs --> Tools
    Tools --> Results
    Results --> Reports
    Reports --> Decision
    Templates --> Decision
    Examples --> Tools
    Results --> Tests
    Reports --> Tests
    Inputs --> Tests
    Tools --> Tests
    Tests --> CI
    CI --> Maintenance
    Maintenance --> Tools
    Reports --> Maintenance
    Decision --> Templates
    Decision --> Examples
    Templates --> Tools
    Examples --> Results
```

## 2. Data And Concept Model

The core concepts are stored as structured JSON first, then transformed into rankings, diagnostics, reports, and pilot evidence.

```mermaid
flowchart TD
    Alternatives["data/alternatives.json<br/>17 included alternatives<br/>2 excluded alternatives"]
    Criteria["14 scoring criteria<br/>0-5 rubric"]
    Rubric["data/scoring_rubric.json<br/>score anchors"]
    Scenarios["data/scenario_profiles.json<br/>5 decision scenarios"]
    Weights["scenario weights<br/>generated in results/scenario_weights.csv"]
    Sandbox["data/sandbox_evaluation.json<br/>sandbox candidates, scenarios, threats"]
    Risks["data/risk_register.json<br/>adoption risks and mitigations"]
    Assumptions["data/simulation_assumptions.json<br/>validity threats and stress tests"]
    Cost["data/operational_cost_model.json<br/>operating profiles"]
    PilotTasks["data/pilot_tasks.json<br/>20 pilot tasks"]
    PilotDecision["data/pilot_decision_model.json<br/>post-pilot gates and weights"]
    SampleSize["data/pilot_sample_size_model.json<br/>task-count assumptions"]
    Taxonomy["data/candidate_taxonomy.json<br/>adoption-shape groups"]
    Traceability["data/traceability_matrix.json<br/>requirements to artifacts"]
    Fixtures["data/security_evaluation_fixtures.json<br/>security gate cases"]

    Alternatives --> Criteria
    Rubric --> Criteria
    Criteria --> Weights
    Scenarios --> Weights
    Weights --> Rankings["scenario rankings and shortlists"]
    Alternatives --> Rankings
    Assumptions --> Rankings
    Sandbox --> SandboxRankings["sandbox rankings and threat coverage"]
    Risks --> RiskMatrix["risk validation matrix"]
    Fixtures --> RiskMatrix
    Cost --> OperationalFit["operational cost and adjusted rankings"]
    PilotTasks --> PilotProtocol["pilot protocol and templates"]
    SampleSize --> PilotProtocol
    PilotDecision --> PilotProtocol
    Taxonomy --> Reports["taxonomy, brief, decision reports"]
    Traceability --> Validation["traceability and validation summary"]
    Rankings --> Reports
    SandboxRankings --> Reports
    RiskMatrix --> Reports
    OperationalFit --> Reports
    PilotProtocol --> Reports
```

## 3. Tool Pipeline

The scripts are grouped by job so the workflow is easier to follow without losing connectivity.

```mermaid
flowchart LR
    Data["Structured inputs<br/>data/*.json"]

    Sim["Simulation tools<br/>simulate_alternatives.py<br/>simulate_sandboxes.py<br/>stress_test_simulation.py<br/>rank_with_custom_weights.py"]
    Analysis["Analysis tools<br/>analyze_score_drivers.py<br/>analyze_evidence_gaps.py<br/>estimate_implementation_effort.py<br/>estimate_operational_costs.py<br/>estimate_pilot_sample_sizes.py"]
    Builders["Report builders<br/>build_scenario_playbooks.py<br/>build_recommendation_rationale.py<br/>build_risk_validation_matrix.py<br/>build_results_data_dictionary.py<br/>build_github_metadata_report.py<br/>build_report_bundle.py"]
    QA["Quality tools<br/>license_audit.py<br/>check_sources.py<br/>refresh_github_metadata.py<br/>check_local_artifact_references.py<br/>validate_markdown_tables.py<br/>validate_csv_schemas.py<br/>validate_artifacts.py<br/>generate_artifact_manifest.py"]
    Assets["Asset tool<br/>generate_charts.py"]
    Pilot["Pilot tool<br/>score_pilot_results.py"]
    Runner["run_all_checks.py<br/>run_all_checks.ps1"]

    RankingResults["Ranking results<br/>deterministic, Monte Carlo, sensitivity, regret, Pareto, stability"]
    SandboxResults["Sandbox results<br/>rankings, threat coverage, decision matrix, source matrix"]
    AnalysisResults["Analysis results<br/>score drivers, effort, cost, sample size, evidence gaps, rationale"]
    QAResults["QA results<br/>license, sources, metadata, schemas, references, manifest"]
    PilotResults["Pilot score results<br/>pilot_decision_scores.example.csv"]
    Reports["Markdown reports<br/>decision, methodology, pilot, risk, validation"]
    Charts["SVG charts<br/>reports/assets/*.svg"]

    Data --> Sim --> RankingResults
    Data --> Sim --> SandboxResults
    Data --> Analysis --> AnalysisResults
    RankingResults --> Analysis
    SandboxResults --> Analysis
    Data --> Builders
    RankingResults --> Builders
    AnalysisResults --> Builders
    SandboxResults --> Builders
    Builders --> Reports
    Assets --> Charts
    RankingResults --> Assets
    AnalysisResults --> Assets
    Data --> QA
    Reports --> QA
    RankingResults --> QA
    SandboxResults --> QA
    AnalysisResults --> QA
    QA --> QAResults
    Pilot --> PilotResults
    Templates["templates/*.csv and templates/*.md<br/>including templates/pilot_run_log.csv"] --> Pilot
    Examples["examples/*.csv and examples/*.json"] --> Pilot
    Runner --> Sim
    Runner --> Analysis
    Runner --> Builders
    Runner --> Assets
    Runner --> QA
    Runner --> Pilot
    QAResults --> Reports
```

## 4. Result Families

The generated `results/` directory is not one flat pile; it has connected families that answer different decision questions.

```mermaid
flowchart TD
    Results["results/"]
    Base["Base ranking family<br/>deterministic_rankings.csv<br/>monte_carlo_summary.csv<br/>sensitivity_summary.csv<br/>category_scores.csv<br/>decision_shortlist.csv"]
    Stability["Stability family<br/>regret_analysis.csv<br/>pareto_frontier.csv<br/>rank_stability.csv<br/>stress_test_summary.csv<br/>stress_test_rankings.csv<br/>uncertainty_stress_summary.csv<br/>uncertainty_stress_details.csv"]
    Explanation["Explanation family<br/>criteria_definitions.csv<br/>evidence_matrix.csv<br/>alternative_scorecards.csv<br/>score_driver_summary.csv<br/>criterion_spread_summary.csv"]
    Scenario["Scenario family<br/>scenario_weights.csv<br/>scenario_playbook_summary.csv<br/>recommendation_rationale.csv<br/>custom_weights_example_rankings.csv"]
    Ops["Operational family<br/>implementation_effort_estimates.csv<br/>operational_cost_estimates.csv<br/>operational_fit_rankings.csv"]
    Pilot["Pilot family<br/>pilot_sample_size_estimates.csv<br/>pilot_decision_scores.example.csv"]
    Risk["Risk and evidence family<br/>evidence_gap_analysis.csv<br/>risk_validation_matrix.csv<br/>license_audit.csv<br/>source_check.csv<br/>github_metadata_check.csv"]
    Sandbox["Sandbox family<br/>sandbox_deterministic_rankings.csv<br/>sandbox_monte_carlo_summary.csv<br/>sandbox_threat_coverage.csv<br/>sandbox_decision_matrix.csv<br/>sandbox_source_matrix.csv"]
    QA["Repository QA family<br/>local_artifact_reference_check.csv<br/>markdown_table_check.csv<br/>csv_schema_check.csv<br/>artifact_manifest.csv<br/>all_results.json"]
    Reports["reports/"]

    Results --> Base
    Base --> Stability
    Base --> Explanation
    Base --> Scenario
    Scenario --> Ops
    Scenario --> Pilot
    Risk --> Scenario
    Sandbox --> Risk
    Stability --> Reports
    Explanation --> Reports
    Scenario --> Reports
    Ops --> Reports
    Pilot --> Reports
    Risk --> Reports
    Sandbox --> Reports
    QA --> Reports
    Reports --> QA
```

## 5. Decision Flow

This diagram connects the concepts a reviewer uses to move from static research to a real adoption decision.

```mermaid
flowchart TD
    CandidateUniverse["Candidate universe from shared conversation"]
    LicenseFilter["Permissive OSS filter<br/>MIT or Apache-2.0"]
    ScoredCandidates["Scored candidates<br/>14 criteria"]
    ScenarioFit["Scenario fit<br/>5 scenario profiles"]
    Deterministic["Deterministic score"]
    MonteCarlo["Monte Carlo stability"]
    Sensitivity["Weight sensitivity"]
    Regret["Regret and Pareto checks"]
    Operational["Operational cost and effort"]
    Evidence["Evidence confidence and freshness"]
    SandboxGate["Sandbox and security gate"]
    Shortlist["Scenario shortlist"]
    Pilot["Pilot execution"]
    HumanReview["Human code review and scorecards"]
    RiskEvidence["Risk validation evidence"]
    NoGo["No-go conditions"]
    Adoption["Adoption decision record"]

    CandidateUniverse --> LicenseFilter --> ScoredCandidates
    ScoredCandidates --> ScenarioFit
    ScenarioFit --> Deterministic
    ScenarioFit --> MonteCarlo
    ScenarioFit --> Sensitivity
    Deterministic --> Regret
    MonteCarlo --> Shortlist
    Sensitivity --> Shortlist
    Regret --> Shortlist
    Operational --> Shortlist
    Evidence --> Shortlist
    SandboxGate --> Shortlist
    Shortlist --> Pilot
    Pilot --> HumanReview
    Pilot --> RiskEvidence
    RiskEvidence --> NoGo
    HumanReview --> Adoption
    NoGo --> Adoption
```

## 6. Validation And Maintenance Loop

The repository is designed so generated artifacts can be refreshed and checked as a repeatable local or CI workflow.

```mermaid
flowchart LR
    Change["Change data, scripts, templates, examples, or reports"]
    UnitTests["python -m unittest discover -s tests"]
    Regenerate["python scripts/run_all_checks.py"]
    Generated["Regenerated results, reports, charts, and manifest"]
    ReferenceCheck["check_local_artifact_references.py"]
    TableCheck["validate_markdown_tables.py"]
    SchemaCheck["validate_csv_schemas.py"]
    ArtifactCheck["validate_artifacts.py"]
    Manifest["generate_artifact_manifest.py"]
    CI["ci/validate-workflow.example.yml"]
    Summary["reports/validation_summary.md"]
    MaintenanceGuide["reports/maintenance_guide.md"]

    Change --> UnitTests
    UnitTests --> Regenerate
    Regenerate --> Generated
    Generated --> ReferenceCheck
    Generated --> TableCheck
    Generated --> SchemaCheck
    Generated --> Manifest
    ReferenceCheck --> ArtifactCheck
    TableCheck --> ArtifactCheck
    SchemaCheck --> ArtifactCheck
    Manifest --> ArtifactCheck
    ArtifactCheck --> CI
    ArtifactCheck --> Summary
    Summary --> MaintenanceGuide
    MaintenanceGuide --> Change
```

## 7. Script-To-Artifact Index

| Tool | Primary input | Primary output |
|---|---|---|
| `scripts/simulate_alternatives.py` | `data/alternatives.json` and scenario weights | Base rankings, Monte Carlo, sensitivity, category scores, shortlist, `results/all_results.json` |
| `scripts/simulate_sandboxes.py` | `data/sandbox_evaluation.json` | Sandbox rankings, threat coverage, decision matrix, sandbox report |
| `scripts/stress_test_simulation.py` | `data/alternatives.json`, `data/simulation_assumptions.json` | Deterministic and uncertainty stress-test CSVs |
| `scripts/analyze_score_drivers.py` | Rankings and candidate scores | Score-driver and criterion-spread CSVs/report inputs |
| `scripts/build_scenario_playbooks.py` | Scenario outputs and shortlists | Scenario playbook CSV/report |
| `scripts/estimate_implementation_effort.py` | Candidate scores | Prototype and hardening effort estimates |
| `scripts/estimate_operational_costs.py` | `data/operational_cost_model.json` and rankings | Operational cost and adjusted ranking CSVs/report |
| `scripts/estimate_pilot_sample_sizes.py` | `data/pilot_sample_size_model.json` and shortlist comparisons | Pilot sample-size estimates/report |
| `scripts/analyze_evidence_gaps.py` | Candidate metadata and evidence confidence | Evidence gap CSV/report |
| `scripts/build_recommendation_rationale.py` | Rankings, risks, effort, cost, stability | Scenario recommendation rationale CSV/report |
| `scripts/build_risk_validation_matrix.py` | `data/risk_register.json` and security fixtures | Risk validation matrix CSV/report |
| `scripts/rank_with_custom_weights.py` | `examples/custom_weights.example.json` | Custom-weight ranking CSV |
| `scripts/license_audit.py` | Candidate license data | License audit CSV |
| `scripts/check_sources.py` | Evidence URLs | Source health CSV |
| `scripts/refresh_github_metadata.py` | GitHub repository metadata | GitHub metadata CSV |
| `scripts/build_github_metadata_report.py` | `results/github_metadata_check.csv` | GitHub metadata Markdown report |
| `scripts/check_local_artifact_references.py` | README and reports | Local artifact reference CSV |
| `scripts/validate_markdown_tables.py` | README and reports | Markdown table consistency CSV |
| `scripts/validate_csv_schemas.py` | Generated CSVs | CSV schema check CSV |
| `scripts/generate_artifact_manifest.py` | Repository artifacts | SHA-256 artifact manifest |
| `scripts/validate_artifacts.py` | Generated results, reports, local QA CSVs | Offline artifact validation |
| `scripts/generate_charts.py` | Ranking and operational CSVs | SVG charts in `reports/assets/` |
| `scripts/build_results_data_dictionary.py` | Generated CSV schemas | Results data dictionary report |
| `scripts/build_report_bundle.py` | Main reports and appendices | One-file final report bundle |
| `scripts/score_pilot_results.py` | Pilot candidate summary CSV | Post-pilot decision scores |
| `scripts/run_all_checks.py` | Whole repository | End-to-end regeneration and validation |
| `scripts/run_all_checks.ps1` | PowerShell shell entrypoint | Calls `scripts/run_all_checks.py` |

## 8. Where To Start

| Need | Start here | Then follow |
|---|---|---|
| Understand the whole system | This file | `reports/artifact_index.md`, then `reports/final_report_bundle.md` |
| Decide what to pilot | `reports/executive_brief.md` | `reports/recommendation_rationale.md`, `reports/scenario_playbooks.md`, `reports/pilot_protocol.md` |
| Audit methodology | `reports/methodology_appendix.md` | `reports/simulation_assumptions.md`, `reports/score_driver_summary.md` |
| Review safety | `reports/sandbox_report.md` | `reports/security_evaluation_fixtures.md`, `reports/risk_validation_matrix.md` |
| Refresh outputs | `reports/maintenance_guide.md` | `python scripts/run_all_checks.py` |
