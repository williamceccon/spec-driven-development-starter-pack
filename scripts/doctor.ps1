param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
python (Join-Path $repoRoot 'scripts\doctor.py') --repo $repoRoot
