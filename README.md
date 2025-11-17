# Requirements Traceability Dashboard

Generate an interactive HTML dashboard from Jira Xray Requirements Traceability Reports.

## 🌐 Live Demo

**Access the dashboard online:** [https://gligorisaev.github.io/jira_report/](https://gligorisaev.github.io/jira_report/)

No installation needed - just visit the URL and upload your CSV!

## Quick Start

### Option 1: In-Browser Upload (No Python Required)

1. Open `index.html` in your browser
2. Drag and drop your Requirements Traceability Report CSV file
3. Dashboard generates instantly!

### Option 2: Python Generator

1. Export the **Requirement Traceability Report** from Jira/Xray
2. Save it as `traceability_report.csv` in this directory
3. Run the generator:
   ```powershell
   python generate_dashboard.py
   ```
   or double-click `generate.bat`
4. Open `dashboard.html` in your browser

## Features

- **Epic Overview**: See all epics with their stories and test coverage
- **Coverage Metrics**: Visual charts showing covered vs uncovered stories
- **Test Status**: Track test execution status (Passed, Failed, Not Run, To Do)
- **Interactive**: Click to expand epics and see detailed story/test information
- **Search**: Filter epics, stories, and tests in real-time
- **Natural Sorting**: Items sorted intelligently (e.g., 1.1, 1.2, 1.10, 2.1)

## CSV Format

The script expects a semicolon-delimited CSV with these columns:
- `Parent Requirement Key` - Epic key (if story is under an epic)
- `Parent Requirement Summary` - Epic summary
- `Requirement Key` - Story key
- `Requirement Summary` - Story summary
- `Requirement Status` - Story status (e.g., COVERED, UNCOVERED)
- `Test Key` - Test case key
- `Test Summary` - Test case summary
- `Test Status` - Test execution status (e.g., PASSED, FAILED, TO DO, NOTRUN)
- `Defect Keys` - Linked defects (optional)

## Dashboard Statistics

The dashboard displays:
- **Total Epics**: Number of parent requirements
- **Total Stories**: Number of requirements/user stories
- **Covered Stories**: Stories with at least one test
- **Coverage %**: Percentage of stories with tests
- **Total Tests**: Number of test cases
- **Test Status Breakdown**: Passed, Failed, Not Run, To Do

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## File Structure

```
jira_report/
├── generate_dashboard.py      # Main generator script
├── traceability_report.csv    # Your Jira export (input)
├── dashboard.html             # Generated dashboard (output)
└── README.md                  # This file
```

## Notes

- The script handles UTF-8 with BOM (Excel CSV exports)
- Empty rows and malformed entries are automatically filtered
- Tests can be linked to stories or directly to epics
- Epic/story relationships are automatically inferred from the CSV
