"""
Script to publish test results as a GitHub PR comment
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests library not found. Installing...")
    os.system("pip3 install requests")
    import requests


def parse_json_report(report_path):
    """Parse pytest JSON report"""
    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        total = data.get('summary', {}).get('total', 0)
        passed = data.get('summary', {}).get('passed', 0)
        failed = data.get('summary', {}).get('failed', 0)
        skipped = data.get('summary', {}).get('skipped', 0)
        duration = data.get('summary', {}).get('duration', 0)
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'duration': duration
        }
    except Exception as e:
        print(f"Error parsing {report_path}: {e}")
        return None


def parse_junit_report(report_path):
    """Parse JUnit XML report"""
    try:
        from xml.etree import ElementTree as ET
        
        tree = ET.parse(report_path)
        root = tree.getroot()
        
        testsuite = root.find('testsuite')
        if testsuite is None:
            return None
        
        stats = {
            'total': int(testsuite.get('tests', 0)),
            'passed': int(testsuite.get('tests', 0)) - int(testsuite.get('failures', 0)) - int(testsuite.get('errors', 0)),
            'failed': int(testsuite.get('failures', 0)) + int(testsuite.get('errors', 0)),
            'skipped': int(testsuite.get('skipped', 0)),
            'time': float(testsuite.get('time', 0))
        }
        
        return stats
    except Exception as e:
        print(f"Error parsing {report_path}: {e}")
        return None


def generate_pr_comment(status='RUNNING'):
    """Generate PR comment with test results"""
    
    api_stats = None
    ui_stats = None
    
    api_report = Path('JsonPlaceholder-API-Automation-Suite/api_report.xml')
    ui_report = Path('SauceDemo-UI-Automation-Suite/ui_report.xml')
    
    if api_report.exists():
        api_stats = parse_junit_report(str(api_report))
    
    if ui_report.exists():
        ui_stats = parse_junit_report(str(ui_report))
    
    # Build comment
    comment = f"## 🧪 Test Report\n\n"
    comment += f"**Status:** {status}\n"
    comment += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    
    if api_stats:
        comment += "### API Tests (JSONPlaceholder)\n"
        comment += f"- **Total:** {api_stats['total']}\n"
        comment += f"- **✅ Passed:** {api_stats['passed']}\n"
        comment += f"- **❌ Failed:** {api_stats['failed']}\n"
        comment += f"- **⏭️ Skipped:** {api_stats['skipped']}\n"
        comment += f"- **⏱️ Duration:** {api_stats['time']:.2f}s\n\n"
    else:
        comment += "### API Tests\n- No results yet\n\n"
    
    if ui_stats:
        comment += "### UI Tests (SauceDemo)\n"
        comment += f"- **Total:** {ui_stats['total']}\n"
        comment += f"- **✅ Passed:** {ui_stats['passed']}\n"
        comment += f"- **❌ Failed:** {ui_stats['failed']}\n"
        comment += f"- **⏭️ Skipped:** {ui_stats['skipped']}\n"
        comment += f"- **⏱️ Duration:** {ui_stats['time']:.2f}s\n\n"
    else:
        comment += "### UI Tests\n- No results yet\n\n"
    
    # Add links to reports
    jenkins_url = os.getenv('BUILD_URL', '')
    if jenkins_url:
        comment += "### 📊 Detailed Reports\n"
        comment += f"[View Full Report]({jenkins_url}Test_Report)\n"
    
    return comment


def publish_to_github(comment):
    """Publish comment to GitHub PR"""
    
    # Get required environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('GITHUB_PR_NUMBER')
    
    if not all([github_token, github_repo, pr_number]):
        print("Warning: GitHub environment variables not set")
        print(f"Token: {bool(github_token)}, Repo: {github_repo}, PR: {pr_number}")
        print("Skipping GitHub comment publication")
        return
    
    # GitHub API endpoint
    url = f"https://api.github.com/repos/{github_repo}/issues/{pr_number}/comments"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {"body": comment}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print("✅ Comment posted successfully to GitHub PR")
        else:
            print(f"❌ Failed to post comment: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error posting comment: {e}")


def main():
    status = sys.argv[1] if len(sys.argv) > 1 else 'RUNNING'
    
    print(f"\n{'='*60}")
    print("Generating PR comment with test results...")
    print(f"{'='*60}\n")
    
    comment = generate_pr_comment(status)
    print("Generated Comment:\n")
    print(comment)
    
    # Only publish to GitHub if token is available
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        print("\n" + "="*60)
        print("Publishing to GitHub...")
        print("="*60 + "\n")
        publish_to_github(comment)
    else:
        print("\n⚠️  GITHUB_TOKEN not set - comment not published to GitHub")
        print("For local testing, comment preview shown above")


if __name__ == "__main__":
    main()
