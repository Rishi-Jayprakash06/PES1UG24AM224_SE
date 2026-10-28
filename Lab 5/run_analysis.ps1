$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

py -m pip install --upgrade pylint bandit flake8
if ($LASTEXITCODE -ne 0) {
    throw 'Tool installation failed. Check your Python and internet connection.'
}

py .\run_analysis.py
if ($LASTEXITCODE -ne 0) {
    throw 'Static analysis could not be completed.'
}

Write-Host 'Reports are in reports/before and reports/after.'
Write-Host 'Read report.md and verify the Pylint score is greater than 9.5.'
