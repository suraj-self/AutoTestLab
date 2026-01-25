"""Script to publish test results as a GitHub PR comment with comprehensive logging."""

import json
import logging
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

# Configure logging for scripts
_LOG_PATH = Path("execution.log")
logger = logging.getLogger("pr_publisher")
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s [%(funcName)s]: %(message)s"
    )
    fh = logging.FileHandler(str(_LOG_PATH), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.info("Logging initialized for PR publisher")


def parse_json_report(report_path):
    """Parse pytest JSON report with error handling."""
    logger.info(f"Parsing JSON report: {report_path}")
    try:
        with open(report_path, encoding="utf-8") as f:
            data = json.load(f)

        total = data.get("summary", {}).get("total", 0)
        passed = data.get("summary", {}).get("passed", 0)
        failed = data.get("summary", {}).get("failed", 0)
        skipped = data.get("summary", {}).get("skipped", 0)
        duration = data.get("summary", {}).get("duration", 0)

        result = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": duration,
        }
        logger.debug(
            f"JSON report parsed successfully: {total} total, {passed} passed, {failed} failed"
        )
        return result
    except FileNotFoundError as e:
        logger.warning(f"Report file not found: {report_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {report_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing {report_path}: {e}", exc_info=True)
        return None


def parse_junit_report(report_path):
    """Parse JUnit XML report with error handling."""
    logger.info(f"Parsing JUnit report: {report_path}")
    try:
        from xml.etree import ElementTree as ET

        tree = ET.parse(report_path)
        root = tree.getroot()

        # Handle both cases: root is testsuite or root contains testsuite elements
        if root.tag == "testsuite":
            testsuite = root
        else:
            testsuite = root.find("testsuite")

        if testsuite is None:
            logger.warning(f"No testsuite element found in {report_path}")
            return None

        stats = {
            "total": int(testsuite.get("tests", 0)),
            "passed": int(testsuite.get("tests", 0))
            - int(testsuite.get("failures", 0))
            - int(testsuite.get("errors", 0)),
            "failed": int(testsuite.get("failures", 0))
            + int(testsuite.get("errors", 0)),
            "skipped": int(testsuite.get("skipped", 0)),
            "time": float(testsuite.get("time", 0)),
        }

        logger.debug(
            f"JUnit report parsed successfully: {stats['total']} total, {stats['passed']} passed, {stats['failed']} failed"
        )
        return stats
    except FileNotFoundError as e:
        logger.warning(f"Report file not found: {report_path}")
        return None
    except ET.ParseError as e:
        logger.error(f"Invalid XML in {report_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing {report_path}: {e}", exc_info=True)
        return None


def generate_pr_comment(status="RUNNING"):
    """Generate PR comment with test results and error handling."""
    logger.info(f"Generating PR comment with status: {status}")
    try:
        api_stats = None
        ui_stats = None

        api_report = Path("JsonPlaceholder-API-Automation-Suite/api_report.xml")
        ui_report = Path("SauceDemo-UI-Automation-Suite/ui_report.xml")

        if api_report.exists():
            logger.debug(f"API report found: {api_report}")
            api_stats = parse_junit_report(str(api_report))
        else:
            logger.warning(f"API report not found: {api_report}")

        if ui_report.exists():
            logger.debug(f"UI report found: {ui_report}")
            ui_stats = parse_junit_report(str(ui_report))
        else:
            logger.warning(f"UI report not found: {ui_report}")

        # Build comment
        comment = f"## 🧪 Test Report\n\n"
        comment += f"**Status:** {status}\n"
        comment += (
            f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        )

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
        jenkins_url = os.getenv("BUILD_URL", "")
        if jenkins_url:
            comment += "### 📊 Detailed Reports\n"
            comment += f"[View Full Report]({jenkins_url}Test_Report)\n"

        logger.info("PR comment generated successfully")
        return comment
    except Exception as e:
        logger.error(f"Error generating PR comment: {e}", exc_info=True)
        raise


def publish_to_github(comment):
    """Publish comment to GitHub PR with error handling."""
    logger.info("Publishing comment to GitHub")
    try:
        # Get required environment variables
        github_token = os.getenv("GITHUB_TOKEN")
        github_repo = os.getenv("GITHUB_REPOSITORY")
        pr_number = os.getenv("GITHUB_PR_NUMBER")

        if not all([github_token, github_repo, pr_number]):
            logger.warning("GitHub environment variables not fully set")
            logger.warning(
                f"Token: {bool(github_token)}, Repo: {github_repo}, PR: {pr_number}"
            )
            logger.info("Skipping GitHub comment publication")
            return

        # GitHub API endpoint
        url = f"https://api.github.com/repos/{github_repo}/issues/{pr_number}/comments"
        logger.debug(f"GitHub API URL: {url}")

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        data = {"body": comment}

        try:
            logger.debug("Sending POST request to GitHub API")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 201:
                logger.info("✅ Comment posted successfully to GitHub PR")
                print("✅ Comment posted successfully to GitHub PR")
            else:
                logger.error(
                    f"Failed to post comment: {response.status_code} - {response.text}"
                )
                print(f"❌ Failed to post comment: {response.status_code}")
                print(response.text)
        except requests.exceptions.Timeout:
            logger.error("Request to GitHub API timed out")
            print("❌ Request to GitHub API timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while posting to GitHub: {e}", exc_info=True)
            print(f"❌ Error posting comment: {e}")
        except Exception as e:
            logger.error(f"Unexpected error posting to GitHub: {e}", exc_info=True)
            print(f"❌ Unexpected error: {e}")
    except Exception as e:
        logger.error(f"Error in publish_to_github: {e}", exc_info=True)
        raise


def main():
    """Main entry point for PR comment publisher."""
    try:
        logger.info("Starting PR comment publisher script")
        status = sys.argv[1] if len(sys.argv) > 1 else "RUNNING"

        print(f"\n{'='*60}")
        print("Generating PR comment with test results...")
        print(f"{'='*60}\n")

        comment = generate_pr_comment(status)
        print("Generated Comment:\n")
        print(comment)

        # Only publish to GitHub if token is available
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            print("\n" + "=" * 60)
            print("Publishing to GitHub...")
            print("=" * 60 + "\n")
            publish_to_github(comment)
        else:
            logger.info("GITHUB_TOKEN not set - skipping GitHub publication")
            print("\n⚠️  GITHUB_TOKEN not set - comment not published to GitHub")
            print("For local testing, comment preview shown above")
        logger.info("PR comment publisher script completed successfully")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
