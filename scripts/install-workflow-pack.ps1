param()

$ErrorActionPreference = 'Stop'
$skillSource = Join-Path $PSScriptRoot '..\skills\specify-workflow-pack'
$codeHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$skillTarget = Join-Path $codeHome 'skills\specify-workflow-pack'
New-Item -ItemType Directory -Force -Path (Split-Path $skillTarget -Parent) | Out-Null
Copy-Item -Recurse -Force $skillSource $skillTarget
Write-Host "Installed specify-workflow-pack to $skillTarget"
