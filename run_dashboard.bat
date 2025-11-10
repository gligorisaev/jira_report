@echo off
REM Quick start script for generating the Jira Xray dashboard
REM Usage: run_dashboard.bat "path\to\your\csv\file.csv"

echo ================================
echo Jira Xray Dashboard Generator
echo ================================
echo.

if "%~1"=="" (
    echo Error: Please provide the CSV file path
    echo Usage: run_dashboard.bat "path\to\csv\file.csv"
    echo.
    echo Example: run_dashboard.bat "Requirement Traceability Report.csv"
    pause
    exit /b 1
)

if not exist "%~1" (
    echo Error: File not found: %~1
    pause
    exit /b 1
)

echo Processing: %~1
echo.

python generate_dashboard.py "%~1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================
    echo Dashboard generated successfully!
    echo ================================
    echo.
    echo Opening dashboard in browser...
    start dashboard.html
) else (
    echo.
    echo Error: Dashboard generation failed
    pause
)
