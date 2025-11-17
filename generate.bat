@echo off
echo.
echo ========================================
echo  Requirements Traceability Dashboard
echo ========================================
echo.

if not exist "traceability_report.csv" (
    echo ERROR: traceability_report.csv not found!
    echo.
    echo Please export the Requirement Traceability Report from Jira/Xray
    echo and save it as "traceability_report.csv" in this directory.
    echo.
    pause
    exit /b 1
)

echo Generating dashboard...
echo.
python generate_dashboard.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo.
    echo Dashboard generated: dashboard.html
    echo.
    echo Opening dashboard in your browser...
    start dashboard.html
) else (
    echo.
    echo ERROR: Failed to generate dashboard.
    echo.
    pause
)
