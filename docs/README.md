# Requirements Traceability Dashboard

🌐 **Live Dashboard:** [https://gligorisaev.github.io/jira_report/](https://gligorisaev.github.io/jira_report/)

Upload your Jira Requirements Traceability Report CSV and generate an interactive dashboard instantly!

## Features

- 📊 Interactive coverage metrics and charts
- 🔍 Real-time search and filtering
- 📈 Test status breakdown
- 🎨 Color-coded coverage levels
- 📱 Responsive design
- 🔐 Privacy-first (all processing client-side)
- 🌐 No installation required - runs in browser

## Usage

### Online (Recommended)

1. Visit [https://gligorisaev.github.io/jira_report/](https://gligorisaev.github.io/jira_report/)
2. Drag and drop your Requirements Traceability Report CSV
3. Explore your interactive dashboard!

### Local Setup

Clone the repository and open `index.html` in your browser:

```bash
git clone https://github.com/gligorisaev/jira_report.git
cd jira_report
# Open index.html in your browser
```

### Python Generator (For Automation)

```bash
# Place your CSV as traceability_report.csv
python generate_dashboard.py
# Or on Windows:
generate.bat
```

## How to Get Your CSV

1. Go to Jira/Xray
2. Navigate to **Reports** → **Requirement Traceability Report**
3. Configure filters (project, version, etc.)
4. Click **Export** and save as CSV
5. Upload to the dashboard

## Dashboard Statistics

The dashboard displays:
- Total Epics & Stories
- Test Coverage Percentage
- Test Status (Passed, Failed, Not Run, To Do)
- Detailed epic/story/test relationships

## Privacy

All CSV processing happens in your browser - your data never leaves your computer!

## Documentation

- [Quick Start Guide](QUICK_START.md)
- [Full Documentation](README.md)
- [Start Here](START_HERE.md)

## License

MIT License - Feel free to use and modify!
