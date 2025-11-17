# Quick Start Guide

## 📋 What You Need

- A Requirements Traceability Report from Jira/Xray (CSV format)
- **Option A**: A web browser (Chrome, Firefox, Edge, Safari)
- **Option B**: Python 3.7+ (if using the Python generator)

## 🚀 Two Ways to Generate Your Dashboard

### ⚡ Option A: In-Browser Upload (Easiest - No Installation!)

1. **Export the Report from Jira**
   - Go to Jira/Xray
   - Navigate to **Reports** → **Requirement Traceability Report**
   - Configure your filters (project, version, etc.)
   - Click **Export** and save as CSV

2. **Open the Dashboard**
   - Open `index.html` in any web browser

3. **Upload Your File**
   - Drag and drop your CSV file onto the upload zone
   - OR click "Choose File" to browse for it
   - Dashboard generates instantly!

**Advantages:**
- ✅ No Python installation required
- ✅ Works on any device with a browser
- ✅ Instant generation
- ✅ Privacy - your data never leaves your computer

### 🐍 Option B: Python Generator (For Automation)

1. **Export the Report from Jira** (same as above)

2. **Save the File**
   - Name it `traceability_report.csv`
   - Place it in this directory

3. **Run the Generator**
   
   **Easy way - Double-click:**
   ```
   generate.bat
   ```
   
   **Or from PowerShell/Command Prompt:**
   ```powershell
   python generate_dashboard.py
   ```

4. **View Your Dashboard**
   - Opens `dashboard.html` automatically

**Advantages:**
- ✅ Can be automated/scripted
- ✅ Batch processing multiple files
- ✅ Integration with CI/CD pipelines

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
