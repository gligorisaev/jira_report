# 📊 Requirements Traceability Dashboard - Quick Reference

## 🌐 Access Online

### Option 1: Use GitHub Pages (Recommended)

**URL:** https://gligorisaev.github.io/jira_report/

1. Visit the URL in any browser
2. Drag & drop your CSV file
3. Done! Dashboard appears instantly

**Enable GitHub Pages (First Time Only):**
- Go to: https://github.com/gligorisaev/jira_report/settings/pages
- Source: **Deploy from a branch**
- Branch: **main** / Folder: **/docs**
- Click **Save**
- Wait 1-2 minutes for deployment

---

### Option 2: Local Browser

1. Open `index.html` in your browser
2. Upload CSV file
3. View dashboard

---

### Option 3: Python Generator

```bash
# Place CSV as traceability_report.csv
python generate_dashboard.py
# or
generate.bat
```

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| **docs/app.html** | GitHub Pages dashboard |
| **index.html** | Local dashboard with upload |
| **generate_dashboard.py** | Python generator |
| **generate.bat** | Windows quick launcher |

---

## 🔄 Update Live Dashboard

```bash
# Update the code
# ... make changes to index.html ...

# Deploy to GitHub Pages
Copy-Item index.html docs/app.html
git add docs/
git commit -m "Update dashboard"
git push
```

Wait 1-2 minutes, then refresh: https://gligorisaev.github.io/jira_report/

---

## ✅ Features

- ✅ No installation required
- ✅ Works 100% in browser
- ✅ Privacy-first (client-side processing)
- ✅ Real-time search & filtering
- ✅ Interactive charts
- ✅ Export from Jira → Upload → Done!

---

## 📖 Documentation

- [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) - Detailed GitHub Pages setup
- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [README.md](README.md) - Full documentation
- [START_HERE.md](START_HERE.md) - Overview and file guide
