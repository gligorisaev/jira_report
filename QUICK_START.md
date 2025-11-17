# Quick Start Guide

## 📋 What You Need

- Python 3.7 or higher
- A Requirements Traceability Report from Jira/Xray (CSV format)

## 🚀 Steps to Generate Your Dashboard

### 1. Export the Report from Jira

1. Go to Jira/Xray
2. Navigate to **Reports** → **Requirement Traceability Report**
3. Configure your filters (project, version, etc.)
4. Click **Export** and save as CSV
5. Name the file: `traceability_report.csv`
6. Place it in this directory

### 2. Run the Generator

**Option A: Double-click the batch file**
```
generate.bat
```
This will automatically generate and open the dashboard.

**Option B: Run from PowerShell/Command Prompt**
```powershell
python generate_dashboard.py
```

### 3. View Your Dashboard

The script creates `dashboard.html` - open it in any modern browser.

## 📊 What the Dashboard Shows

### Summary Cards
- **Total Epics**: Number of parent requirements/epics
- **Total Stories**: Number of user stories/requirements
- **Covered Stories**: Stories that have at least one test
- **Coverage %**: Percentage of stories with test coverage
- **Total Tests**: Number of test cases
- **Passed/Failed/Not Run/To Do**: Test execution status breakdown

### Interactive Features
- **Click any epic** to expand and see stories and tests
- **Search box** to filter epics/stories/tests in real-time
- **Visual charts** showing coverage and test status distribution

### Color Coding
- 🟢 **Green**: High coverage (≥80%) or passed tests
- 🟡 **Yellow**: Medium coverage (50-79%) or not run tests
- 🔴 **Red**: Low coverage (<50%) or failed tests
- ⚪ **Gray**: No stories or to-do tests

## 🔧 Troubleshooting

### Python not found
Install Python from [python.org](https://www.python.org/downloads/)

### CSV file not found
Make sure `traceability_report.csv` is in the same directory as `generate_dashboard.py`

### Encoding errors
The script handles UTF-8 with BOM (Excel exports). If you still have issues, open the CSV in Notepad and save as UTF-8.

### Empty dashboard
Check that your CSV has the correct columns:
- Parent Requirement Key
- Parent Requirement Summary
- Requirement Key
- Requirement Summary
- Test Key
- Test Summary
- Test Status

## 💡 Tips

- **Run regularly**: Re-generate the dashboard whenever you update tests or requirements
- **Share easily**: The dashboard is a single HTML file - email it or share via network drive
- **Works offline**: No internet connection needed to view the dashboard (charts use CDN but will work without)
- **Version control**: Commit the Python script, not the generated HTML

## 📧 Support

For issues or questions, check the README.md file for more details.
