param(
  [string]$Name,
  [string]$TargetPath,
  [string]$Profile,
  [string[]]$Addons,
  [switch]$NoGitInit,
  [switch]$NoGitHubCi,
  [switch]$ListProfiles,
  [switch]$ListAddons
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$argsList = @((Join-Path $repoRoot 'scripts\new_project.py'))
if ($Name) { $argsList += @('--name', $Name) }
if ($TargetPath) { $argsList += @('--target-path', $TargetPath) }
if ($Profile) { $argsList += @('--profile', $Profile) }
if ($Addons -and $Addons.Count -gt 0) { $argsList += @('--addons', ($Addons -join ',')) }
if ($NoGitInit) { $argsList += '--no-git-init' }
if ($NoGitHubCi) { $argsList += '--no-github-ci' }
if ($ListProfiles) { $argsList += '--list-profiles' }
if ($ListAddons) { $argsList += '--list-addons' }

python @argsList
