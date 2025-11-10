#!/usr/bin/env python3
"""
Jira Xray Dashboard Generator
Generates an HTML dashboard from Xray requirement traceability reports
"""

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import argparse


class XrayDashboardGenerator:
    """Generate HTML dashboard from Xray CSV reports"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = []
        self.epics = defaultdict(lambda: {
            'stories': {},
            'total_stories': 0,
            'covered_stories': 0,
            'uncovered_stories': 0,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'todo_tests': 0,
            'notrun_tests': 0
        })
        
    def parse_csv(self):
        """Parse the CSV file and extract data"""
        print(f"Parsing CSV file: {self.csv_path}")
        
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            # Use semicolon as delimiter based on the CSV format
            reader = csv.DictReader(f, delimiter=';')
            
            for row in reader:
                self.data.append(row)
                
                parent_key = row.get('Parent Requirement Key', '').strip()
                parent_summary = row.get('Parent Requirement Summary', '').strip()
                req_key = row.get('Requirement Key', '').strip()
                req_summary = row.get('Requirement Summary', '').strip()
                req_status = row.get('Requirement Status', '').strip()
                test_key = row.get('Test Key', '').strip()
                test_status = row.get('Test Status', '').strip()
                
                # If there's a parent, it's an epic
                if parent_key and req_key:
                    epic = self.epics[parent_key]
                    epic['summary'] = parent_summary
                    
                    # Track story
                    if req_key not in epic['stories']:
                        epic['stories'][req_key] = {
                            'summary': req_summary,
                            'status': req_status,
                            'tests': [],
                            'has_tests': False
                        }
                        epic['total_stories'] += 1
                    
                    story = epic['stories'][req_key]
                    
                    # Track test
                    if test_key:
                        story['has_tests'] = True
                        story['tests'].append({
                            'key': test_key,
                            'status': test_status
                        })
                        epic['total_tests'] += 1
                        
                        # Count test statuses
                        if test_status == 'PASSED':
                            epic['passed_tests'] += 1
                        elif test_status == 'FAILED':
                            epic['failed_tests'] += 1
                        elif test_status == 'TO DO':
                            epic['todo_tests'] += 1
                        elif test_status == 'NOTRUN':
                            epic['notrun_tests'] += 1
                
                # Standalone story (no parent)
                elif req_key and not parent_key:
                    epic = self.epics['NO_EPIC']
                    epic['summary'] = 'Stories without Epic'
                    
                    if req_key not in epic['stories']:
                        epic['stories'][req_key] = {
                            'summary': req_summary,
                            'status': req_status,
                            'tests': [],
                            'has_tests': False
                        }
                        epic['total_stories'] += 1
                    
                    story = epic['stories'][req_key]
                    
                    if test_key:
                        story['has_tests'] = True
                        story['tests'].append({
                            'key': test_key,
                            'status': test_status
                        })
                        epic['total_tests'] += 1
                        
                        if test_status == 'PASSED':
                            epic['passed_tests'] += 1
                        elif test_status == 'FAILED':
                            epic['failed_tests'] += 1
                        elif test_status == 'TO DO':
                            epic['todo_tests'] += 1
                        elif test_status == 'NOTRUN':
                            epic['notrun_tests'] += 1
        
        # Calculate coverage
        for epic_key, epic in self.epics.items():
            for story_key, story in epic['stories'].items():
                if story['has_tests']:
                    epic['covered_stories'] += 1
                else:
                    epic['uncovered_stories'] += 1
        
        print(f"Parsed {len(self.data)} rows")
        print(f"Found {len(self.epics)} epics")
        
    def calculate_summary_stats(self):
        """Calculate overall summary statistics"""
        total_epics = len(self.epics)
        total_stories = sum(e['total_stories'] for e in self.epics.values())
        covered_stories = sum(e['covered_stories'] for e in self.epics.values())
        uncovered_stories = sum(e['uncovered_stories'] for e in self.epics.values())
        total_tests = sum(e['total_tests'] for e in self.epics.values())
        passed_tests = sum(e['passed_tests'] for e in self.epics.values())
        failed_tests = sum(e['failed_tests'] for e in self.epics.values())
        todo_tests = sum(e['todo_tests'] for e in self.epics.values())
        notrun_tests = sum(e['notrun_tests'] for e in self.epics.values())
        
        coverage_percent = (covered_stories / total_stories * 100) if total_stories > 0 else 0
        
        return {
            'total_epics': total_epics,
            'total_stories': total_stories,
            'covered_stories': covered_stories,
            'uncovered_stories': uncovered_stories,
            'coverage_percent': round(coverage_percent, 1),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'todo_tests': todo_tests,
            'notrun_tests': notrun_tests
        }
    
    def generate_html(self, output_path):
        """Generate HTML dashboard"""
        print(f"Generating HTML dashboard: {output_path}")
        
        summary = self.calculate_summary_stats()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jira Xray Test Coverage Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            color: #2d3748;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            color: #718096;
            font-size: 14px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card .label {{
            color: #718096;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}
        
        .stat-card .value {{
            color: #2d3748;
            font-size: 36px;
            font-weight: 700;
        }}
        
        .stat-card .subvalue {{
            color: #a0aec0;
            font-size: 14px;
            margin-top: 5px;
        }}
        
        .stat-card.coverage {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .stat-card.coverage .label,
        .stat-card.coverage .value,
        .stat-card.coverage .subvalue {{
            color: white;
        }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .chart-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .chart-card h3 {{
            color: #2d3748;
            font-size: 18px;
            margin-bottom: 20px;
        }}
        
        .chart-wrapper {{
            position: relative;
            height: 300px;
        }}
        
        .epics-table {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow-x: auto;
        }}
        
        .epics-table h3 {{
            color: #2d3748;
            font-size: 18px;
            margin-bottom: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: #f7fafc;
            color: #2d3748;
            font-weight: 600;
            text-align: left;
            padding: 12px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
            color: #4a5568;
        }}
        
        tr:hover {{
            background: #f7fafc;
        }}
        
        .progress-bar {{
            background: #e2e8f0;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            position: relative;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
            height: 100%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: 600;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .badge.covered {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .badge.uncovered {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .badge.partial {{
            background: #feebc8;
            color: #7c2d12;
        }}
        
        .epic-details {{
            display: none;
            background: #f7fafc;
            padding: 15px;
            margin-top: 10px;
            border-radius: 8px;
        }}
        
        .epic-details.show {{
            display: block;
        }}
        
        .story-item {{
            background: white;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        
        .story-item .story-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }}
        
        .story-item .story-key {{
            font-weight: 600;
            color: #2d3748;
        }}
        
        .test-list {{
            margin-top: 8px;
            padding-left: 20px;
            font-size: 13px;
            color: #718096;
        }}
        
        .expandable {{
            cursor: pointer;
        }}
        
        .expandable:hover {{
            background: #edf2f7;
        }}
        
        @media (max-width: 768px) {{
            .charts-container {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Jira Xray Test Coverage Dashboard</h1>
            <div class="timestamp">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card coverage">
                <div class="label">Test Coverage</div>
                <div class="value">{summary['coverage_percent']}%</div>
                <div class="subvalue">{summary['covered_stories']} of {summary['total_stories']} stories covered</div>
            </div>
            
            <div class="stat-card">
                <div class="label">Total Epics</div>
                <div class="value">{summary['total_epics']}</div>
                <div class="subvalue">With {summary['total_stories']} stories</div>
            </div>
            
            <div class="stat-card">
                <div class="label">Total Tests</div>
                <div class="value">{summary['total_tests']}</div>
                <div class="subvalue">
                    Passed: {summary['passed_tests']} | 
                    Failed: {summary['failed_tests']} | 
                    To Do: {summary['todo_tests']}
                </div>
            </div>
            
            <div class="stat-card">
                <div class="label">Uncovered Stories</div>
                <div class="value">{summary['uncovered_stories']}</div>
                <div class="subvalue">Stories without test cases</div>
            </div>
        </div>
        
        <div class="charts-container">
            <div class="chart-card">
                <h3>Coverage Overview</h3>
                <div class="chart-wrapper">
                    <canvas id="coverageChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>Test Status Distribution</h3>
                <div class="chart-wrapper">
                    <canvas id="testStatusChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="epics-table">
            <h3>Epic Details</h3>
            <table>
                <thead>
                    <tr>
                        <th>Epic Key</th>
                        <th>Epic Summary</th>
                        <th>Stories</th>
                        <th>Coverage</th>
                        <th>Tests</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add epic rows
        for epic_key in sorted(self.epics.keys()):
            epic = self.epics[epic_key]
            coverage_percent = (epic['covered_stories'] / epic['total_stories'] * 100) if epic['total_stories'] > 0 else 0
            
            if coverage_percent == 100:
                status_badge = '<span class="badge covered">Fully Covered</span>'
            elif coverage_percent > 0:
                status_badge = '<span class="badge partial">Partially Covered</span>'
            else:
                status_badge = '<span class="badge uncovered">Uncovered</span>'
            
            html_content += f"""
                    <tr class="expandable" onclick="toggleEpic('{epic_key}')">
                        <td><strong>{epic_key}</strong></td>
                        <td>{epic['summary']}</td>
                        <td>{epic['total_stories']} ({epic['covered_stories']} covered)</td>
                        <td>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {coverage_percent}%">
                                    {round(coverage_percent, 1)}%
                                </div>
                            </div>
                        </td>
                        <td>{epic['total_tests']}</td>
                        <td>{status_badge}</td>
                    </tr>
                    <tr>
                        <td colspan="6" style="padding: 0;">
                            <div id="epic-{epic_key}" class="epic-details">
"""
            
            # Add story details
            for story_key in sorted(epic['stories'].keys()):
                story = epic['stories'][story_key]
                test_count = len(story['tests'])
                status = '✅ Covered' if story['has_tests'] else '❌ Uncovered'
                
                html_content += f"""
                                <div class="story-item">
                                    <div class="story-header">
                                        <span class="story-key">{story_key}</span>
                                        <span>{status}</span>
                                    </div>
                                    <div>{story['summary']}</div>
"""
                
                if story['tests']:
                    html_content += """
                                    <div class="test-list">
                                        <strong>Tests:</strong><br>
"""
                    for test in story['tests']:
                        html_content += f"                                        • {test['key']} - {test['status']}<br>\n"
                    
                    html_content += """
                                    </div>
"""
                
                html_content += """
                                </div>
"""
            
            html_content += """
                            </div>
                        </td>
                    </tr>
"""
        
        html_content += f"""
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        // Coverage Chart
        const coverageCtx = document.getElementById('coverageChart').getContext('2d');
        new Chart(coverageCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Covered Stories', 'Uncovered Stories'],
                datasets: [{{
                    data: [{summary['covered_stories']}, {summary['uncovered_stories']}],
                    backgroundColor: ['#48bb78', '#fc8181'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Test Status Chart
        const testStatusCtx = document.getElementById('testStatusChart').getContext('2d');
        new Chart(testStatusCtx, {{
            type: 'bar',
            data: {{
                labels: ['Passed', 'Failed', 'To Do', 'Not Run'],
                datasets: [{{
                    label: 'Number of Tests',
                    data: [{summary['passed_tests']}, {summary['failed_tests']}, {summary['todo_tests']}, {summary['notrun_tests']}],
                    backgroundColor: ['#48bb78', '#fc8181', '#f6ad55', '#a0aec0'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
        
        // Toggle epic details
        function toggleEpic(epicKey) {{
            const details = document.getElementById('epic-' + epicKey);
            details.classList.toggle('show');
        }}
    </script>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Dashboard generated successfully!")
        print(f"Open {output_path} in your browser to view.")


def main():
    parser = argparse.ArgumentParser(description='Generate HTML dashboard from Xray CSV reports')
    parser.add_argument('csv_file', help='Path to the Xray CSV file')
    parser.add_argument('-o', '--output', default='dashboard.html', help='Output HTML file path')
    
    args = parser.parse_args()
    
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        return 1
    
    generator = XrayDashboardGenerator(csv_path)
    generator.parse_csv()
    generator.generate_html(args.output)
    
    return 0


if __name__ == '__main__':
    exit(main())
