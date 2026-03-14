param()

$ErrorActionPreference = 'Stop'
$tools = @('git','python','node','npm','uv','poetry','gh','specify')
$missing = @()
foreach ($tool in $tools) {
  if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
    $missing += $tool
  }
}

$codeHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$skillsRoot = Join-Path $codeHome 'skills'
$requiredSkills = @('specify-workflow-pack','brainstorming','gh-fix-ci','gh-address-comments')
$missingSkills = @()
foreach ($skill in $requiredSkills) {
  $skillFile = Join-Path $skillsRoot "$skill\SKILL.md"
  if (-not (Test-Path $skillFile)) {
    $missingSkills += $skill
  }
}

if ($missing.Count -gt 0 -or $missingSkills.Count -gt 0) {
  if ($missing.Count -gt 0) {
    Write-Host 'Missing tools:'
    $missing | ForEach-Object { Write-Host "- $_" }
  }
  if ($missingSkills.Count -gt 0) {
    Write-Host 'Missing global skills:'
    $missingSkills | ForEach-Object { Write-Host "- $_" }
    Write-Host 'Run .\scripts\install-workflow-pack.ps1 after cloning the starter.'
  }
  exit 1
}

Write-Host 'Machine doctor passed.'
