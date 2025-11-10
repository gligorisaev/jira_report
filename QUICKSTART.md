# Quick Start Guide

## Generate Your First Dashboard

### Option 1: Using PowerShell (Recommended)

```powershell
# Navigate to the project directory
cd c:\Users\DE00023567\jira_report

# Run the dashboard generator
python generate_dashboard.py "C:\Users\DE00023567\Downloads\Requirement Traceability Report 10-11-25 14_07_35.csv"
```

### Option 2: Using Batch File

```cmd
run_dashboard.bat "C:\Users\DE00023567\Downloads\Requirement Traceability Report 10-11-25 14_07_35.csv"
```

### Option 3: Drag and Drop

1. Drag your CSV file onto `run_dashboard.bat`
2. The dashboard will be generated automatically
3. Your browser will open with the dashboard

## Output

The script will create:
- `dashboard.html` - Your interactive dashboard (open this in a browser)

## Viewing the Dashboard

Simply double-click `dashboard.html` or open it in any modern web browser:
- Chrome
- Firefox
- Edge
- Safari

## Tips

### For Regular Use

Create a shortcut on your desktop:
1. Right-click `run_dashboard.bat`
2. Send to → Desktop (create shortcut)
3. Drag your CSV files onto the shortcut

### For Multiple Reports

```powershell
# Generate with custom output name
python generate_dashboard.py "report1.csv" -o "dashboard_sprint1.html"
python generate_dashboard.py "report2.csv" -o "dashboard_sprint2.html"
```

### Refresh Data

To update the dashboard with new data:
1. Export a new CSV from Jira Xray
2. Run the generator again
3. Refresh your browser

## What You'll See

Your dashboard will display:

1. **High-Level Metrics**
   - Overall test coverage percentage
   - Number of epics and stories
   - Total test count with status breakdown
   - Number of uncovered stories

2. **Visual Charts**
   - Coverage pie chart (covered vs uncovered stories)
   - Test status bar chart (passed, failed, todo, not run)

3. **Detailed Epic Table**
   - Click any epic row to expand details
   - See all stories and their associated tests
   - Visual progress bars for each epic
   - Color-coded status badges

## Troubleshooting

### "Python is not recognized"

Install Python from https://www.python.org/downloads/ or use:
```powershell
winget install Python.Python.3.12
```

### CSV Not Found

Make sure to use the full path in quotes:
```powershell
python generate_dashboard.py "C:\Full\Path\To\Your\File.csv"
```

### Browser Doesn't Open

Manually open `dashboard.html` by:
- Double-clicking the file
- Right-click → Open with → Your browser

---

**Need Help?** Check the full README.md for detailed documentation.
