param()

$ErrorActionPreference = 'Stop'
$tools = @('git','python','node','npm','specify')
$missing = @()
foreach ($tool in $tools) {
  if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
    $missing += $tool
  }
}
if ($missing.Count -gt 0) {
  Write-Host 'Missing tools:'
  $missing | ForEach-Object { Write-Host "- $_" }
  exit 1
}
Write-Host 'Machine doctor passed.'
