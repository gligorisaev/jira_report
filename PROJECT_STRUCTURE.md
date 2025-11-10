# Project Structure

```
jira_report/
│
├── generate_dashboard.py      # Main Python script - generates HTML dashboards
├── run_dashboard.bat          # Windows batch script for easy execution
├── run_dashboard.ps1          # PowerShell script with more options
├── config.json                # Configuration file (for future use)
├── requirements.txt           # Python dependencies (none required!)
│
├── README.md                  # Complete documentation
├── QUICKSTART.md              # Quick start guide
├── PROJECT_STRUCTURE.md       # This file
│
├── sample_data.csv            # Sample CSV for testing
├── sample_dashboard.html      # Example generated dashboard
│
└── .gitignore                 # Git ignore rules

```

## File Descriptions

### Core Files

#### `generate_dashboard.py`
The main Python script that:
- Parses Xray CSV reports (semicolon-delimited)
- Calculates coverage metrics (epics, stories, tests)
- Generates a beautiful HTML dashboard
- Uses only Python standard library (no dependencies!)

**Key Classes:**
- `XrayDashboardGenerator`: Main class handling all operations
  - `parse_csv()`: Parses CSV and builds data structures
  - `calculate_summary_stats()`: Computes overall metrics
  - `generate_html()`: Creates the HTML dashboard

**Usage:**
```bash
python generate_dashboard.py input.csv [-o output.html]
```

#### `run_dashboard.bat`
Windows batch script for one-click dashboard generation.

**Usage:**
```cmd
run_dashboard.bat "path\to\report.csv"
```
or drag & drop a CSV file onto the script.

#### `run_dashboard.ps1`
PowerShell script with additional features:
- Better error handling
- Optional browser auto-open
- Colored console output

**Usage:**
```powershell
.\run_dashboard.ps1 -CsvFile "report.csv" -OpenBrowser
```

### Configuration

#### `config.json`
Configuration file for future enhancements:
- Theme colors
- Chart settings
- Feature toggles
- CSV column mappings

Currently not used by the script, but ready for future versions.

### Documentation

#### `README.md`
Complete documentation including:
- Features overview
- Installation instructions
- Detailed usage examples
- CSV format specification
- Dashboard components
- Troubleshooting guide
- Customization tips

#### `QUICKSTART.md`
Quick start guide for users who want to get started immediately:
- Three methods to run the generator
- Common usage patterns
- Tips for regular use
- Quick troubleshooting

### Sample Files

#### `sample_data.csv`
A small sample CSV file for testing:
- Contains 3 epics
- Mix of covered and uncovered stories
- Various test statuses (PASSED, TO DO, NOTRUN)
- Demonstrates the expected CSV format

#### `sample_dashboard.html`
Pre-generated dashboard from sample data:
- Shows what the output looks like
- Can be used as a reference
- Demonstrates all features

## Data Flow

```
CSV Report (Jira Xray)
        ↓
[parse_csv()]
        ↓
Data Structures (epics dict)
        ↓
[calculate_summary_stats()]
        ↓
Summary Metrics
        ↓
[generate_html()]
        ↓
HTML Dashboard
```

## Key Data Structures

### Epic Dictionary
```python
epics = {
    'TML40-82': {
        'summary': 'Epic name',
        'stories': {
            'TML40-161': {
                'summary': 'Story name',
                'status': 'NOTRUN',
                'tests': [
                    {'key': 'TML40-162', 'status': 'TO DO'}
                ],
                'has_tests': True
            }
        },
        'total_stories': 4,
        'covered_stories': 4,
        'uncovered_stories': 0,
        'total_tests': 4,
        'passed_tests': 1,
        'failed_tests': 0,
        'todo_tests': 3,
        'notrun_tests': 0
    }
}
```

## Dashboard Components

### HTML Structure
```
Dashboard
├── Header (Title + Timestamp)
├── Stats Grid (4 cards)
│   ├── Coverage Card (highlighted)
│   ├── Epics Card
│   ├── Tests Card
│   └── Uncovered Card
├── Charts Container
│   ├── Coverage Doughnut Chart
│   └── Test Status Bar Chart
└── Epic Details Table
    ├── Epic Rows (expandable)
    └── Story Details (nested)
```

### Technologies Used
- **Python 3.6+**: Script language
- **Chart.js 4.4.0**: Interactive charts (loaded from CDN)
- **Pure CSS**: Modern styling with gradients
- **Vanilla JavaScript**: Interactive functionality

## Metrics Calculated

### Coverage Metrics
- **Story Coverage**: % of stories with at least one test
- **Epic Coverage**: Individual coverage per epic
- **Overall Coverage**: Project-wide coverage percentage

### Test Metrics
- **Total Tests**: Count of all test cases
- **Test Status Distribution**: PASSED, FAILED, TO DO, NOTRUN
- **Tests per Story**: Average and individual counts

### Story Metrics
- **Total Stories**: All requirements tracked
- **Covered Stories**: Stories with tests
- **Uncovered Stories**: Stories without tests

## Future Enhancements

### Planned Features
- [ ] PDF export functionality
- [ ] Historical trend tracking
- [ ] Multiple report comparison
- [ ] Advanced filtering and search
- [ ] Custom branding/themes
- [ ] Email report delivery
- [ ] Integration with Jira API
- [ ] Real-time dashboard updates

### Possible Improvements
- [ ] Add defect tracking metrics
- [ ] Include sprint/release filtering
- [ ] Add team/assignee breakdown
- [ ] Generate executive summaries
- [ ] Add risk assessment visualization
- [ ] Include test execution time metrics

## Development

### Adding New Features

1. **New Metrics**: Update `calculate_summary_stats()`
2. **New Charts**: Modify `generate_html()` and add Chart.js code
3. **New Styling**: Update CSS in the HTML template
4. **New Config**: Add to `config.json` and parse in script

### Testing

```bash
# Test with sample data
python generate_dashboard.py sample_data.csv

# Test with your data
python generate_dashboard.py "your_report.csv"

# Test PowerShell script
.\run_dashboard.ps1 -CsvFile sample_data.csv -OpenBrowser
```

## Troubleshooting

### Common Issues

1. **CSV Parsing Errors**: Check delimiter (should be semicolon)
2. **Missing Data**: Verify CSV column names match expected format
3. **Encoding Issues**: Ensure CSV is UTF-8 encoded
4. **Empty Dashboard**: Check that CSV contains parent-child relationships

### Debug Mode

Add print statements in `parse_csv()` to see what's being parsed:
```python
print(f"Epic: {parent_key}, Story: {req_key}, Test: {test_key}")
```

## License

Open source - Free to use within your organization.

---

**Last Updated**: November 10, 2025
