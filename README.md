# 🎯 Jira/Xray Traceability Dashboard

A powerful, interactive dashboard for visualizing Jira/Xray traceability reports and requirements coverage analysis. Transform your CSV exports into actionable insights with beautiful charts, hierarchical views, and comprehensive analytics.


## ✨ Features

- **📊 Interactive Analytics** - Real-time metrics and coverage statistics
- **🌳 Hierarchical Visualization** - Parent-child requirement relationships
- **📋 Detailed Data Views** - Comprehensive requirement tables with filtering
- **🔍 Advanced Filtering** - Filter by status, parent groups, and more
- **📱 Responsive Design** - Works on desktop, tablet, and mobile
- **⚡ Fast Performance** - Built with React and optimized for large datasets

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ installed
- npm or yarn package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/jira-xray-dashboard.git
cd jira-xray-dashboard
```

2. **Install dependencies:**
```bash
npm install
npm install recharts lucide-react papaparse lodash tailwindcss postcss autoprefixer
```

3. **Start the development server:**
```bash
npm run dev
```

4. **Open your browser:**
Navigate to `http://localhost:5173`

### Using Your Own CSV Files

1. Export your traceability report from Jira/Xray as CSV
2. Ensure it has the following columns (semicolon-delimited):
   - Parent Requirement Key
   - Parent Requirement Summary
   - Requirement Key
   - Requirement Summary
   - Requirement Status
   - Test Key
   - Test Summary
   - Test Status
   - Defect Keys

3. Upload the CSV file using the "Upload CSV" button in the dashboard

## 📁 Project Structure

```
jira-xray-dashboard/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   └── Dashboard.jsx       # Main dashboard component
│   ├── App.jsx                 # App component
│   ├── index.js               # Entry point
│   └── index.css              # Global styles
├── package.json               # Dependencies and scripts
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # Tailwind CSS configuration
└── README.md                 # This file
```

## 🛠️ Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory for environment-specific settings:

```env
VITE_APP_TITLE=Jira/Xray Dashboard
VITE_API_BASE_URL=your-api-url
```

### Customizing Status Colors

Edit the `statusColors` object in `src/components/Dashboard.jsx`:

```javascript
const statusColors = {
  'UNCOVERED': '#ef4444',
  'NOTRUN': '#f97316', 
  'PASS': '#22c55e',
  'FAIL': '#dc2626',
  // Add your custom statuses here
};
```

## 📊 Dashboard Views

### Overview
- Key metrics and KPI cards
- Status distribution charts
- Coverage pie charts
- Parent group analysis

### Hierarchy
- Tree view of requirements
- Parent-child relationships
- Coverage indicators
- Expandable groups

### Details
- Comprehensive data table
- Sortable columns
- Requirement details
- Test coverage status

## 🌐 Deployment

### GitHub Pages

1. **Build the project:**
```bash
npm run build
```

2. **Deploy to GitHub Pages:**
```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json scripts:
"homepage": "https://yourusername.github.io/jira-xray-dashboard",
"predeploy": "npm run build",
"deploy": "gh-pages -d dist"

# Deploy
npm run deploy
```

### Netlify

1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Deploy automatically on push

### Vercel

1. Import repository to Vercel
2. Vercel auto-detects Vite configuration
3. Deploy with default settings

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `npm run test`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](https://github.com/yourusername/jira-xray-dashboard/wiki)
- 🐛 [Issue Tracker](https://github.com/yourusername/jira-xray-dashboard/issues)
- 💬 [Discussions](https://github.com/yourusername/jira-xray-dashboard/discussions)

## 🙏 Acknowledgments

- Built with [React](https://reactjs.org/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Charts powered by [Recharts](https://recharts.org/)
- Icons from [Lucide React](https://lucide.dev/)
- CSV parsing by [PapaParse](https://www.papaparse.com/)

---

Made with ❤️ for better requirements traceability
