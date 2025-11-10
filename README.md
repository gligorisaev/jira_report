# 📊 Jira Xray Dashboard Generator

A Python tool to generate beautiful HTML dashboards from Jira Xray requirement traceability reports, providing comprehensive test coverage insights for epics, stories, and test cases.

![Dashboard Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-success)
![License](https://img.shields.io/badge/license-open%20source-blue)

## Features

- 📊 **Visual Coverage Metrics** - Interactive charts showing test coverage percentages
- 🎯 **Epic-Level Analysis** - Drill down into each epic to see story and test details
- 📈 **Test Status Tracking** - Track passed, failed, to-do, and not-run tests
- 🎨 **Modern UI** - Clean, responsive design with gradient backgrounds and smooth animations
- 🔍 **Expandable Details** - Click on any epic to view detailed story and test information
- 📱 **Mobile Responsive** - Works perfectly on all device sizes

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone or download this repository
2. No additional installation needed - the script uses only Python standard library

## Usage

### Basic Usage

```bash
python generate_dashboard.py "path/to/your/xray_report.csv"
```

This will generate a `dashboard.html` file in the current directory.

### Custom Output Path

```bash
python generate_dashboard.py "path/to/your/xray_report.csv" -o "output/my_dashboard.html"
```

### Example

```bash
python generate_dashboard.py "Requirement Traceability Report 10-11-25 14_07_35.csv"
```

Then open `dashboard.html` in your web browser.

## CSV Format

The script expects Xray requirement traceability reports with the following columns (semicolon-delimited):

- `Parent Requirement Key` - Epic ID (e.g., TML40-119)
- `Parent Requirement Summary` - Epic description
- `Requirement Key` - Story ID (e.g., TML40-467)
- `Requirement Summary` - Story description
- `Requirement Status` - Story status (UNCOVERED, NOTRUN, OK, etc.)
- `Test Key` - Test case ID (e.g., TML40-473)
- `Test Summary` - Test case description
- `Test Status` - Test status (PASSED, FAILED, TO DO, NOTRUN)
- `Defect Keys` - Associated defects (optional)

## Dashboard Components

### 1. Summary Statistics
- **Test Coverage** - Percentage of stories with test cases
- **Total Epics** - Number of epics tracked
- **Total Tests** - Number of test cases
- **Uncovered Stories** - Stories without tests

### 2. Visual Charts
- **Coverage Overview** - Doughnut chart showing covered vs uncovered stories
- **Test Status Distribution** - Bar chart showing test execution status

### 3. Epic Details Table
- Expandable rows for each epic
- Progress bars showing coverage percentage
- Status badges (Fully Covered, Partially Covered, Uncovered)
- Detailed story and test information

## Features in Detail

### Test Coverage Calculation
- Stories are considered "covered" if they have at least one test case
- Coverage percentage = (Covered Stories / Total Stories) × 100

### Test Status Categories
- **PASSED** - Test executed successfully
- **FAILED** - Test execution failed
- **TO DO** - Test not yet executed
- **NOTRUN** - Test scheduled but not run

### Interactive Elements
- Click on any epic row to expand/collapse story details
- Hover effects on cards and table rows
- Responsive design adapts to screen size

## Example Output

The generated dashboard includes:

```
┌─────────────────────────────────────────────────┐
│  📊 Jira Xray Test Coverage Dashboard          │
│  Generated on November 10, 2025 at 2:07 PM     │
└─────────────────────────────────────────────────┘

┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Coverage   │ Total Epics │ Total Tests │  Uncovered  │
│    XX%      │     XX      │     XXX     │     XX      │
└─────────────┴─────────────┴─────────────┴─────────────┘

[Coverage Chart]        [Test Status Chart]

┌──────────────────────────────────────────────────┐
│  Epic Details                                    │
│  ─────────────────────────────────────────────  │
│  Epic Key  │  Summary  │  Coverage  │  Status   │
│  TML40-XX  │  ...      │  ████ XX%  │  Badge    │
└──────────────────────────────────────────────────┘
```

## Troubleshooting

### CSV File Not Found
Ensure the CSV file path is correct and the file exists.

### Encoding Issues
The script uses UTF-8 encoding. If you encounter issues, ensure your CSV file is UTF-8 encoded.

### Empty Dashboard
Check that your CSV file contains data in the expected format with semicolon delimiters.

## Customization

You can modify the `generate_dashboard.py` script to:
- Change color schemes (update CSS variables)
- Add additional metrics
- Modify chart types
- Customize the layout

## License

This project is open source and available for use in your organization.

## Support

For issues or questions, please refer to the documentation or contact your team lead.

## Roadmap

Future enhancements:
- [ ] Export to PDF
- [ ] Historical trend analysis
- [ ] Multiple report comparison
- [ ] Filtering and search functionality
- [ ] Custom branding options
- [ ] Email report delivery

---

**Generated with ❤️ for better test coverage visibility**
