param()

$ErrorActionPreference = 'Stop'

Write-Host 'Checking Windows machine prerequisites...'

$tools = @('git','python','node','npm','uv','poetry','gh')
foreach ($tool in $tools) {
  if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
    Write-Warning "$tool not found on PATH"
  } else {
    Write-Host "Found $tool"
  }
}

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
  Write-Warning 'winget not found; install tools manually if missing.'
} else {
  Write-Host 'winget available'
}

Write-Host 'Recommended installs if missing:'
Write-Host '  winget install Git.Git'
Write-Host '  winget install Python.Python.3.12'
Write-Host '  winget install OpenJS.NodeJS.LTS'
Write-Host '  winget install AstralSoftware.Uv'
Write-Host '  winget install GitHub.cli'
Write-Host '  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -'
Write-Host '  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git'
Write-Host '  .\scripts\install-workflow-pack.ps1'
