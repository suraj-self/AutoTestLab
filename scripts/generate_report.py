"""
Script to generate combined HTML test report from API and UI tests
"""
import json
import os
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET


def parse_junit_report(report_path):
    """Parse JUnit XML report and extract test details"""
    try:
        tree = ET.parse(report_path)
        root = tree.getroot()
        
        testcases = []
        for testsuite in root.findall('testsuite'):
            suite_name = testsuite.get('name', 'Unknown')
            for testcase in testsuite.findall('testcase'):
                tc = {
                    'classname': testcase.get('classname', ''),
                    'name': testcase.get('name', ''),
                    'time': float(testcase.get('time', 0)),
                    'status': 'passed'
                }
                
                if testcase.find('failure') is not None:
                    tc['status'] = 'failed'
                    tc['error'] = testcase.find('failure').text
                elif testcase.find('error') is not None:
                    tc['status'] = 'error'
                    tc['error'] = testcase.find('error').text
                elif testcase.find('skipped') is not None:
                    tc['status'] = 'skipped'
                
                testcases.append(tc)
        
        total = len(testcases)
        passed = len([tc for tc in testcases if tc['status'] == 'passed'])
        failed = len([tc for tc in testcases if tc['status'] == 'failed'])
        errors = len([tc for tc in testcases if tc['status'] == 'error'])
        skipped = len([tc for tc in testcases if tc['status'] == 'skipped'])
        
        return {
            'testcases': testcases,
            'stats': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'errors': errors,
                'skipped': skipped
            }
        }
    except Exception as e:
        print(f"Error parsing {report_path}: {e}")
        return None


def generate_html_report(api_data, ui_data):
    """Generate combined HTML report"""
    
    api_stats = api_data['stats'] if api_data else {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'skipped': 0}
    ui_stats = ui_data['stats'] if ui_data else {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'skipped': 0}
    
    total_tests = api_stats['total'] + ui_stats['total']
    total_passed = api_stats['passed'] + ui_stats['passed']
    total_failed = api_stats['failed'] + ui_stats['failed']
    total_skipped = api_stats['skipped'] + ui_stats['skipped']
    
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - AutoTestLab</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .header p {{
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .summary-card .label {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        .total {{ color: #667eea; }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .test-suite {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }}
        
        .test-case {{
            display: flex;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            background: white;
        }}
        
        .test-case.passed {{
            border-left: 4px solid #28a745;
        }}
        
        .test-case.failed {{
            border-left: 4px solid #dc3545;
        }}
        
        .test-case.skipped {{
            border-left: 4px solid #ffc107;
        }}
        
        .test-status {{
            font-weight: bold;
            margin-right: 15px;
            text-transform: uppercase;
            font-size: 0.8em;
        }}
        
        .test-status.passed::before {{
            content: '✓';
            color: #28a745;
            margin-right: 5px;
        }}
        
        .test-status.failed::before {{
            content: '✗';
            color: #dc3545;
            margin-right: 5px;
        }}
        
        .test-status.skipped::before {{
            content: '⊘';
            color: #ffc107;
            margin-right: 5px;
        }}
        
        .test-name {{
            flex: 1;
            color: #333;
        }}
        
        .test-time {{
            color: #6c757d;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 2px solid #e9ecef;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Report</h1>
            <p>AutoTestLab - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="label">Total Tests</div>
                <div class="value total">{total_tests}</div>
            </div>
            <div class="summary-card">
                <div class="label">Passed</div>
                <div class="value passed">{total_passed}</div>
            </div>
            <div class="summary-card">
                <div class="label">Failed</div>
                <div class="value failed">{total_failed}</div>
            </div>
            <div class="summary-card">
                <div class="label">Skipped</div>
                <div class="value skipped">{total_skipped}</div>
            </div>
            <div class="summary-card">
                <div class="label">Pass Rate</div>
                <div class="value" style="color: #667eea;">{pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {pass_rate}%">{pass_rate:.1f}%</div>
        </div>
        
        <div class="content">
"""
    
    # Add API tests section
    if api_data:
        html += f"""
            <div class="section">
                <h2 class="section-title">📡 API Tests (JSONPlaceholder)</h2>
                <div class="test-suite">
                    <strong>Summary:</strong> {api_stats['total']} tests • 
                    <span class="passed">{api_stats['passed']} passed</span> • 
                    <span class="failed">{api_stats['failed']} failed</span> • 
                    <span class="skipped">{api_stats['skipped']} skipped</span>
                </div>
"""
        for tc in api_data['testcases']:
            html += f"""
                <div class="test-case {tc['status']}">
                    <span class="test-status {tc['status']}">{tc['status']}</span>
                    <span class="test-name">{tc['name']}</span>
                    <span class="test-time">{tc['time']:.2f}s</span>
                </div>
"""
        html += "            </div>"
    
    # Add UI tests section
    if ui_data:
        html += f"""
            <div class="section">
                <h2 class="section-title">🖥️ UI Tests (SauceDemo)</h2>
                <div class="test-suite">
                    <strong>Summary:</strong> {ui_stats['total']} tests • 
                    <span class="passed">{ui_stats['passed']} passed</span> • 
                    <span class="failed">{ui_stats['failed']} failed</span> • 
                    <span class="skipped">{ui_stats['skipped']} skipped</span>
                </div>
"""
        for tc in ui_data['testcases']:
            html += f"""
                <div class="test-case {tc['status']}">
                    <span class="test-status {tc['status']}">{tc['status']}</span>
                    <span class="test-name">{tc['name']}</span>
                    <span class="test-time">{tc['time']:.2f}s</span>
                </div>
"""
        html += "            </div>"
    
    html += """
        </div>
        
        <div class="footer">
            <p>Generated by Jenkins Pipeline | AutoTestLab</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    print("\n" + "="*60)
    print("Generating Combined Test Report...")
    print("="*60 + "\n")
    
    # Parse reports
    api_data = None
    ui_data = None
    
    api_report = Path('JsonPlaceholder-API-Automation-Suite/api_report.xml')
    ui_report = Path('SauceDemo-UI-Automation-Suite/ui_report.xml')
    
    if api_report.exists():
        print(f"✓ Found API report: {api_report}")
        api_data = parse_junit_report(str(api_report))
    else:
        print(f"✗ API report not found: {api_report}")
    
    if ui_report.exists():
        print(f"✓ Found UI report: {ui_report}")
        ui_data = parse_junit_report(str(ui_report))
    else:
        print(f"✗ UI report not found: {ui_report}")
    
    # Generate HTML
    html = generate_html_report(api_data, ui_data)
    
    # Save report
    output_file = 'combined_report.html'
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"\n✓ Report generated: {output_file}\n")
    print("="*60)


if __name__ == "__main__":
    main()
