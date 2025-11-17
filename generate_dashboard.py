#!/usr/bin/env python3
"""
Generate Requirements Traceability Dashboard from Jira Xray Report
Reads the Requirement Traceability Report CSV and creates an interactive HTML dashboard.
"""

import csv
from collections import defaultdict
from pathlib import Path
import re


def natural_sort_key(text):
    """Create a key for natural sorting (handles numeric prefixes)."""
    parts = []
    for part in re.split(r'(\d+)', str(text)):
        if part.isdigit():
            parts.append(int(part))
        else:
            parts.append(part.lower())
    return parts


def parse_traceability_report(csv_file):
    """Parse the Requirements Traceability Report CSV."""
    epics = {}
    stories = {}
    tests = {}
    project_name = None
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            parent_key = (row.get('Parent Requirement Key') or '').strip()
            parent_summary = (row.get('Parent Requirement Summary') or '').strip()
            req_key = (row.get('Requirement Key') or '').strip()
            req_summary = (row.get('Requirement Summary') or '').strip()
            req_status = (row.get('Requirement Status') or '').strip()
            test_key = (row.get('Test Key') or '').strip()
            test_summary = (row.get('Test Summary') or '').strip()
            test_status = (row.get('Test Status') or '').strip()
            
            # Extract project name from first row with data
            if project_name is None:
                project_name = (row.get('Project name') or row.get('Project key') or '').strip()
                # If no project field, extract from issue key (e.g., TML40 from TML40-531)
                if not project_name and req_key:
                    parts = req_key.split('-')
                    if len(parts) >= 2:
                        project_name = parts[0]
            
            # Handle epics (parent requirements without parents)
            if parent_key and parent_key not in epics:
                epics[parent_key] = {
                    'summary': parent_summary,
                    'stories': {}
                }
            
            # Handle stories (requirements)
            if req_key:
                if parent_key:
                    # Story with a parent (epic)
                    if req_key not in stories:
                        stories[req_key] = {
                            'epic_key': parent_key,
                            'summary': req_summary,
                            'status': req_status,
                            'tests': {}
                        }
                    
                    # Add story to epic
                    if parent_key in epics:
                        if req_key not in epics[parent_key]['stories']:
                            epics[parent_key]['stories'][req_key] = {
                                'summary': req_summary,
                                'status': req_status,
                                'tests': {}
                            }
                else:
                    # Story without a parent (is itself an epic)
                    if req_key not in epics:
                        epics[req_key] = {
                            'summary': req_summary,
                            'stories': {}
                        }
            
            # Handle tests
            if test_key and req_key:
                # Normalize test status
                status_upper = test_status.upper()
                if 'PASS' in status_upper or status_upper == 'DONE':
                    normalized_status = 'PASSED'
                elif 'FAIL' in status_upper:
                    normalized_status = 'FAILED'
                elif 'NOTRUN' in status_upper or 'NOT RUN' in status_upper:
                    normalized_status = 'NOTRUN'
                else:
                    normalized_status = 'TO DO'
                
                if test_key not in tests:
                    tests[test_key] = {
                        'summary': test_summary,
                        'status': normalized_status,
                        'stories': set()
                    }
                
                tests[test_key]['stories'].add(req_key)
                
                # Add test to story
                if req_key in stories:
                    stories[req_key]['tests'][test_key] = {
                        'summary': test_summary,
                        'status': normalized_status
                    }
                    
                    # Add test to epic's story
                    epic_key = stories[req_key]['epic_key']
                    if epic_key in epics and req_key in epics[epic_key]['stories']:
                        epics[epic_key]['stories'][req_key]['tests'][test_key] = {
                            'summary': test_summary,
                            'status': normalized_status
                        }
                elif req_key in epics:
                    # Test linked directly to an epic
                    if '_direct_tests' not in epics[req_key]:
                        epics[req_key]['_direct_tests'] = {}
                    epics[req_key]['_direct_tests'][test_key] = {
                        'summary': test_summary,
                        'status': normalized_status
                    }
    
    return epics, stories, tests, project_name or 'Project'


def calculate_metrics(epics):
    """Calculate coverage metrics for each epic."""
    metrics = {}
    
    for epic_key, epic_data in epics.items():
        total_stories = len(epic_data['stories'])
        covered_stories = sum(1 for s in epic_data['stories'].values() if s['tests'])
        uncovered_stories = total_stories - covered_stories
        
        # Count tests
        test_counts = defaultdict(int)
        seen_tests = set()
        
        for story in epic_data['stories'].values():
            for test_key, test_data in story['tests'].items():
                if test_key not in seen_tests:
                    seen_tests.add(test_key)
                    test_counts[test_data['status']] += 1
        
        # Add direct tests (if any)
        if '_direct_tests' in epic_data:
            for test_key, test_data in epic_data['_direct_tests'].items():
                if test_key not in seen_tests:
                    seen_tests.add(test_key)
                    test_counts[test_data['status']] += 1
        
        total_tests = sum(test_counts.values())
        coverage_percent = (covered_stories / total_stories * 100) if total_stories > 0 else 0
        
        metrics[epic_key] = {
            'total_stories': total_stories,
            'covered_stories': covered_stories,
            'uncovered_stories': uncovered_stories,
            'coverage_percent': coverage_percent,
            'total_tests': total_tests,
            'passed_tests': test_counts.get('PASSED', 0),
            'failed_tests': test_counts.get('FAILED', 0),
            'notrun_tests': test_counts.get('NOTRUN', 0),
            'todo_tests': test_counts.get('TO DO', 0)
        }
    
    return metrics


def generate_html_dashboard(epics, metrics, output_file, project_name='Project', csv_filename='traceability_report.csv'):
    """Generate an interactive HTML dashboard."""
    
    from datetime import datetime
    generation_time = datetime.now().strftime('%b %d, %Y, %I:%M:%S %p')
    
    # Sort epics by summary using natural sort
    sorted_epics = sorted(epics.items(), key=lambda x: natural_sort_key(x[1]['summary']))
    
    # Calculate overall stats
    total_epics = len(epics)
    total_stories = sum(m['total_stories'] for m in metrics.values())
    covered_stories = sum(m['covered_stories'] for m in metrics.values())
    total_tests = sum(m['total_tests'] for m in metrics.values())
    passed_tests = sum(m['passed_tests'] for m in metrics.values())
    failed_tests = sum(m['failed_tests'] for m in metrics.values())
    notrun_tests = sum(m['notrun_tests'] for m in metrics.values())
    todo_tests = sum(m['todo_tests'] for m in metrics.values())
    overall_coverage = (covered_stories / total_stories * 100) if total_stories > 0 else 0
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Requirements Traceability Dashboard</title>
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
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: #2d3748;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #718096;
            font-size: 16px;
            margin-top: 5px;
        }}
        
        .header .timestamp {{
            color: #a0aec0;
            font-size: 14px;
            margin-top: 5px;
            font-style: italic;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-card.highlight {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .stat-card .label {{
            font-size: 14px;
            color: #718096;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .stat-card.highlight .label {{
            color: rgba(255,255,255,0.9);
        }}
        
        .stat-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .stat-card.highlight .value {{
            color: white;
        }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .chart-card h3 {{
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 18px;
        }}
        
        .epics-container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .epic-card {{
            border-bottom: 1px solid #e2e8f0;
            transition: all 0.3s;
        }}
        
        .epic-card:last-child {{
            border-bottom: none;
        }}
        
        .epic-header {{
            padding: 20px 25px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }}
        
        .epic-header:hover {{
            background: #f7fafc;
        }}
        
        .epic-title {{
            flex: 1;
        }}
        
        .epic-key {{
            font-weight: bold;
            color: #667eea;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        
        .epic-summary {{
            color: #2d3748;
            font-size: 16px;
        }}
        
        .epic-stats {{
            display: flex;
            gap: 20px;
            align-items: center;
        }}
        
        .badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .badge.stories {{
            background: #e6fffa;
            color: #234e52;
        }}
        
        .badge.tests {{
            background: #faf5ff;
            color: #553c9a;
        }}
        
        .badge.coverage-high {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .badge.coverage-medium {{
            background: #feebc8;
            color: #7c2d12;
        }}
        
        .badge.coverage-low {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .badge.no-stories {{
            background: #e2e8f0;
            color: #4a5568;
        }}
        
        .expand-icon {{
            color: #cbd5e0;
            font-size: 20px;
            transition: transform 0.3s;
        }}
        
        .epic-card.expanded .expand-icon {{
            transform: rotate(180deg);
        }}
        
        .epic-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }}
        
        .epic-card.expanded .epic-content {{
            max-height: 5000px;
        }}
        
        .epic-details {{
            padding: 0 25px 25px 25px;
            background: #f7fafc;
        }}
        
        .stories-list {{
            margin-top: 15px;
        }}
        
        .story-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .story-item.covered {{
            border-left-color: #48bb78;
        }}
        
        .story-item.uncovered {{
            border-left-color: #f56565;
        }}
        
        .story-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .story-key {{
            font-weight: 600;
            color: #667eea;
            font-size: 13px;
        }}
        
        .story-summary {{
            color: #4a5568;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        
        .tests-list {{
            margin-top: 10px;
            padding-left: 20px;
        }}
        
        .test-item {{
            padding: 8px 12px;
            background: #f7fafc;
            border-radius: 6px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
        }}
        
        .test-key {{
            font-weight: 600;
            color: #553c9a;
            margin-right: 10px;
        }}
        
        .test-summary {{
            flex: 1;
            color: #4a5568;
        }}
        
        .status-badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .status-badge.passed {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .status-badge.failed {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .status-badge.notrun {{
            background: #feebc8;
            color: #7c2d12;
        }}
        
        .status-badge.todo {{
            background: #e6fffa;
            color: #234e52;
        }}
        
        .no-tests {{
            color: #a0aec0;
            font-style: italic;
            font-size: 13px;
            padding: 10px;
        }}
        
        .search-box {{
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.2s;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {project_name} - Requirements Traceability</h1>
            <p class="subtitle">Source: {csv_filename}</p>
            <p class="timestamp">Generated: {generation_time}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card highlight">
                <div class="label">Total Epics</div>
                <div class="value">{total_epics}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Stories</div>
                <div class="value">{total_stories}</div>
            </div>
            <div class="stat-card">
                <div class="label">Covered Stories</div>
                <div class="value">{covered_stories}</div>
            </div>
            <div class="stat-card">
                <div class="label">Coverage</div>
                <div class="value">{overall_coverage:.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Tests</div>
                <div class="value">{total_tests}</div>
            </div>
            <div class="stat-card">
                <div class="label">Passed</div>
                <div class="value">{passed_tests}</div>
            </div>
            <div class="stat-card">
                <div class="label">Failed</div>
                <div class="value">{failed_tests}</div>
            </div>
            <div class="stat-card">
                <div class="label">Not Run</div>
                <div class="value">{notrun_tests}</div>
            </div>
        </div>
        
        <div class="charts-container">
            <div class="chart-card">
                <h3>📈 Coverage Overview</h3>
                <canvas id="coverageChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>🧪 Test Status Distribution</h3>
                <canvas id="testsChart"></canvas>
            </div>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search epics, stories, or tests...">
        </div>
        
        <div class="epics-container" id="epicsContainer">
"""
    
    # Generate epic cards
    for epic_key, epic_data in sorted_epics:
        m = metrics[epic_key]
        
        # Determine coverage badge
        if m['total_stories'] == 0:
            coverage_badge = '<span class="badge no-stories">No Stories</span>'
        else:
            if m['coverage_percent'] >= 80:
                coverage_class = 'coverage-high'
            elif m['coverage_percent'] >= 50:
                coverage_class = 'coverage-medium'
            else:
                coverage_class = 'coverage-low'
            coverage_badge = f'<span class="badge {coverage_class}">{m["coverage_percent"]:.0f}%</span>'
        
        html += f"""
            <div class="epic-card" data-epic-key="{epic_key}">
                <div class="epic-header" onclick="toggleEpic(this)">
                    <div class="epic-title">
                        <div class="epic-key">{epic_key}</div>
                        <div class="epic-summary">{epic_data['summary']}</div>
                    </div>
                    <div class="epic-stats">
                        <span class="badge stories">{m['total_stories']} Stories</span>
                        <span class="badge tests">{m['total_tests']} Tests</span>
                        {coverage_badge}
                        <span class="expand-icon">▼</span>
                    </div>
                </div>
                <div class="epic-content">
                    <div class="epic-details">
"""
        
        if m['total_stories'] > 0:
            html += '<div class="stories-list">'
            
            # Sort stories by summary
            sorted_stories = sorted(
                epic_data['stories'].items(),
                key=lambda x: natural_sort_key(x[1]['summary'])
            )
            
            for story_key, story_data in sorted_stories:
                has_tests = len(story_data['tests']) > 0
                coverage_class = 'covered' if has_tests else 'uncovered'
                
                html += f"""
                    <div class="story-item {coverage_class}">
                        <div class="story-header">
                            <span class="story-key">{story_key}</span>
                            <span class="badge {'tests' if has_tests else 'no-stories'}">{len(story_data['tests'])} Tests</span>
                        </div>
                        <div class="story-summary">{story_data['summary']}</div>
"""
                
                if has_tests:
                    html += '<div class="tests-list">'
                    for test_key, test_data in story_data['tests'].items():
                        status_lower = test_data['status'].lower().replace(' ', '')
                        html += f"""
                            <div class="test-item">
                                <span class="test-key">{test_key}</span>
                                <span class="test-summary">{test_data['summary']}</span>
                                <span class="status-badge {status_lower}">{test_data['status']}</span>
                            </div>
"""
                    html += '</div>'
                else:
                    html += '<div class="no-tests">No tests linked to this story</div>'
                
                html += '</div>'
            
            html += '</div>'
        else:
            html += '<div class="no-tests">This epic has no stories</div>'
        
        # Add direct tests if any
        if '_direct_tests' in epic_data and epic_data['_direct_tests']:
            html += '<div class="tests-list" style="margin-top: 15px;">'
            html += '<div style="font-weight: 600; margin-bottom: 10px; color: #553c9a;">Direct Tests:</div>'
            for test_key, test_data in epic_data['_direct_tests'].items():
                status_lower = test_data['status'].lower().replace(' ', '')
                html += f"""
                    <div class="test-item">
                        <span class="test-key">{test_key}</span>
                        <span class="test-summary">{test_data['summary']}</span>
                        <span class="status-badge {status_lower}">{test_data['status']}</span>
                    </div>
"""
            html += '</div>'
        
        html += """
                    </div>
                </div>
            </div>
"""
    
    html += f"""
        </div>
    </div>
    
    <script>
        // Chart.js configuration
        const coverageCtx = document.getElementById('coverageChart').getContext('2d');
        new Chart(coverageCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Covered Stories', 'Uncovered Stories'],
                datasets: [{{
                    data: [{covered_stories}, {total_stories - covered_stories}],
                    backgroundColor: ['#48bb78', '#f56565'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        const testsCtx = document.getElementById('testsChart').getContext('2d');
        new Chart(testsCtx, {{
            type: 'bar',
            data: {{
                labels: ['Passed', 'Failed', 'Not Run', 'To Do'],
                datasets: [{{
                    label: 'Tests',
                    data: [{passed_tests}, {failed_tests}, {notrun_tests}, {todo_tests}],
                    backgroundColor: ['#48bb78', '#f56565', '#ed8936', '#4299e1'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            precision: 0
                        }}
                    }}
                }}
            }}
        }});
        
        // Toggle epic expansion
        function toggleEpic(header) {{
            const epicCard = header.closest('.epic-card');
            epicCard.classList.toggle('expanded');
        }}
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const epicCards = document.querySelectorAll('.epic-card');
            
            epicCards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }});
        
        // Expand all epics on load (optional)
        // document.querySelectorAll('.epic-card').forEach(card => card.classList.add('expanded'));
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """Main execution function."""
    csv_file = Path('traceability_report.csv')
    output_file = Path('dashboard.html')
    
    print("Generating Requirements Traceability Dashboard...")
    print(f"Reading: {csv_file}")
    
    # Parse the CSV
    epics, stories, tests, project_name = parse_traceability_report(csv_file)
    
    print(f"\nParsed:")
    print(f"   - {len(epics)} Epics")
    print(f"   - {len(stories)} Stories")
    print(f"   - {len(tests)} Tests")
    
    # Calculate metrics
    metrics = calculate_metrics(epics)
    
    # Generate HTML dashboard
    generate_html_dashboard(epics, metrics, output_file, project_name, csv_file.name)
    
    print(f"\nDashboard generated: {output_file}")
    print(f"\nOpen {output_file} in your browser to view the dashboard.")


if __name__ == '__main__':
    main()
