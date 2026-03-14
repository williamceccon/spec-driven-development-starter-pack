param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$skillsSource = Join-Path $repoRoot 'skills'
$codeHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$skillsTarget = Join-Path $codeHome 'skills'
New-Item -ItemType Directory -Force -Path $skillsTarget | Out-Null

Get-ChildItem $skillsSource -Directory | ForEach-Object {
  $target = Join-Path $skillsTarget $_.Name
  if (Test-Path $target) {
    Remove-Item -Recurse -Force $target
  }
  Copy-Item -Recurse -Force $_.FullName $target
  Write-Host "Installed $($_.Name) to $target"
}

Write-Host 'Restart Codex to pick up new skills.'
