# Jira Xray Dashboard Generator - PowerShell Script
# Usage: .\run_dashboard.ps1 -CsvFile "path\to\file.csv" [-OutputFile "dashboard.html"]

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to the Xray CSV report file")]
    [string]$CsvFile,
    
    [Parameter(Mandatory=$false, HelpMessage="Output HTML file path")]
    [string]$OutputFile = "dashboard.html",
    
    [Parameter(Mandatory=$false, HelpMessage="Open dashboard in browser after generation")]
    [switch]$OpenBrowser
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Jira Xray Dashboard Generator" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if CSV file exists
if (-not (Test-Path $CsvFile)) {
    Write-Host "Error: CSV file not found: $CsvFile" -ForegroundColor Red
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Using $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Processing: $CsvFile" -ForegroundColor Yellow
Write-Host ""

# Run the dashboard generator
$arguments = @(
    "generate_dashboard.py",
    $CsvFile,
    "-o",
    $OutputFile
)

$process = Start-Process -FilePath "python" -ArgumentList $arguments -NoNewWindow -Wait -PassThru

if ($process.ExitCode -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "Dashboard generated successfully!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output file: $OutputFile" -ForegroundColor Cyan
    
    if ($OpenBrowser) {
        Write-Host "Opening dashboard in browser..." -ForegroundColor Yellow
        Start-Process $OutputFile
    } else {
        Write-Host ""
        Write-Host "To open the dashboard, run:" -ForegroundColor Yellow
        Write-Host "  Start-Process $OutputFile" -ForegroundColor White
        Write-Host ""
        Write-Host "Or use the -OpenBrowser switch next time:" -ForegroundColor Yellow
        Write-Host "  .\run_dashboard.ps1 -CsvFile '$CsvFile' -OpenBrowser" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "Error: Dashboard generation failed with exit code $($process.ExitCode)" -ForegroundColor Red
    exit $process.ExitCode
}
