param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$skillsSource = Join-Path $repoRoot 'skills'
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$targets = @(
  @{ Name = 'Codex'; Path = (Join-Path $codexHome 'skills') },
  @{ Name = 'Claude Code'; Path = (Join-Path $HOME '.claude\skills') },
  @{ Name = 'OpenCode'; Path = (Join-Path $HOME '.config\opencode\skills') },
  @{ Name = 'Generic Agents'; Path = (Join-Path $HOME '.agents\skills') }
)

foreach ($targetInfo in $targets) {
  New-Item -ItemType Directory -Force -Path $targetInfo.Path | Out-Null
  Get-ChildItem $skillsSource -Directory | ForEach-Object {
    $target = Join-Path $targetInfo.Path $_.Name
    if (Test-Path $target) {
      Remove-Item -Recurse -Force $target
    }
    Copy-Item -Recurse -Force $_.FullName $target
    Write-Host "Installed $($_.Name) to $target for $($targetInfo.Name)"
  }
}

Write-Host 'Restart the agent session you use so new global skills are discovered.'
