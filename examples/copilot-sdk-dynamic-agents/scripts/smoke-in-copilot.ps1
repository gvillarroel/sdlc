[CmdletBinding()]
param(
    [string]$Task = "Design a safe command-driven POC for dynamic agents."
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$resultPath = Join-Path $repoRoot "examples\copilot-sdk-dynamic-agents\results\copilot-skill-demo.latest.json"
$startedAt = (Get-Date).ToUniversalTime()
$runId = [guid]::NewGuid().ToString()
$environmentNames = @(
    "COPILOT_GITHUB_TOKEN",
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS"
)
$previousEnvironment = @{}

foreach ($name in $environmentNames) {
    $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, "Process")
}

try {
    [Environment]::SetEnvironmentVariable("COPILOT_GITHUB_TOKEN", $null, "Process")
    [Environment]::SetEnvironmentVariable("GH_TOKEN", $null, "Process")
    [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $null, "Process")
    [Environment]::SetEnvironmentVariable("GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS", "true", "Process")

    $prompt = @"
Use dynamic_agents_skill_demo exactly once with runId "$runId" for this task: $Task
Report the compact evidence returned by that tool. Do not call any other tool.
"@

    Push-Location $repoRoot
    try {
        & copilot --experimental --no-color `
            --allow-tool='custom-tool(dynamic_agents_skill_demo)' `
            --agent dynamic-agent-orchestrator `
            -p $prompt
        if ($LASTEXITCODE -ne 0) {
            throw "Copilot CLI exited with code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }

    if (-not (Test-Path -LiteralPath $resultPath)) {
        throw "Copilot did not create the expected result file: $resultPath"
    }
    $resultFile = Get-Item -LiteralPath $resultPath
    if ($resultFile.LastWriteTimeUtc -lt $startedAt) {
        throw "The result file was not refreshed by this smoke run."
    }

    $report = Get-Content -Raw -LiteralPath $resultPath | ConvertFrom-Json
    if ($report.schemaVersion -ne 2 -or $report.runId -ne $runId) {
        throw "The report does not belong to this smoke run (expected runId $runId)."
    }
    if ($report.source -ne "copilot-extension-tool") {
        throw "Unexpected result source '$($report.source)'."
    }
    if ($report.status -ne "passed" -or -not $report.generationProved -or -not $report.orderMatches) {
        throw "Dynamic-agent skill chain failed: status=$($report.status), generationProved=$($report.generationProved), orderMatches=$($report.orderMatches)."
    }
    $failedRuntimeChecks = @($report.runtimeChecks | Where-Object {
        -not $_.selectedAgentMatches -or
        -not $_.runtimeSkillAssigned -or
        -not $_.skillInvoked -or
        -not $_.skillEventObserved -or
        $_.trigger -ne "agent-invoked" -or
        -not $_.markerFound
    })
    if ($failedRuntimeChecks.Count -gt 0) {
        throw "Runtime proof failed for agent(s): $($failedRuntimeChecks.agent -join ', ')."
    }
    $nonCreated = @($report.generatedAgents | Where-Object { $_.action -ne "created" })
    if ($nonCreated.Count -gt 0) {
        throw "Demo agents were not freshly created: $($nonCreated.name -join ', ')."
    }

    Write-Host "PASS: dynamic agents generated and executed in order inside Copilot."
    Write-Host "Order: $($report.executionOrder -join ' -> ')"
    Write-Host "Runtime skills: $($report.runtimeChecks.skill -join ', ')"
    Write-Host "Run ID: $runId"
    Write-Host "Result: $resultPath"
}
finally {
    foreach ($name in $environmentNames) {
        [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], "Process")
    }
}
