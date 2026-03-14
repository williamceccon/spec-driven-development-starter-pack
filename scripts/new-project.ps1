param(
  [Parameter(Mandatory=$true)][string]$Name,
  [Parameter(Mandatory=$true)][string]$TargetPath
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$profile = Join-Path $repoRoot 'profiles\python-fastapi-nextjs'
$targetRepo = Join-Path $TargetPath $Name
if (Test-Path $targetRepo) { throw "Target repo already exists: $targetRepo" }
New-Item -ItemType Directory -Path $targetRepo | Out-Null
Copy-Item -Recurse -Force (Join-Path $profile '*') $targetRepo
(Get-Content (Join-Path $targetRepo 'workflow-pack.json') -Raw).Replace('REPLACE_ME',$Name) | Set-Content (Join-Path $targetRepo 'workflow-pack.json') -Encoding utf8
if (-not (Test-Path (Join-Path $targetRepo '.git'))) { git init $targetRepo | Out-Null }
python (Join-Path $repoRoot 'skills\specify-workflow-pack\scripts\install_workflow_pack.py') --repo $targetRepo --config (Join-Path $targetRepo 'workflow-pack.json')
Write-Host "Project created at $targetRepo"
Write-Host 'Next steps:'
Write-Host '  1. Review workflow-pack.json and install runtime dependencies.'
Write-Host '  2. Run /brief "initial feature idea" inside the new repo.'
Write-Host '  3. Run /workflow <slug> using the slug written to BRIEF.md.'
