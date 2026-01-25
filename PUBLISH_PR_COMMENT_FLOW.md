# publish_pr_comment.py Execution Flow - Detailed

## 1. ENTRY POINT: You Execute Script

```bash
$ python3 scripts/publish_pr_comment.py [STATUS]
                                        │
                                        └─ Optional: "RUNNING", "SUCCESS", "FAILED"
                                           (Default: "RUNNING")
```

## 2. INITIALIZATION

### 2.1 Logger Setup
```python
_LOG_PATH = Path("execution.log")
logger = logging.getLogger("pr_publisher")
# Logs ALL actions to: execution.log + console
# Levels: DEBUG, INFO, WARNING, ERROR
```

### 2.2 Main Function Called
```python
def main():
    status = sys.argv[1] if len(sys.argv) > 1 else "RUNNING"
    # Extract first argument or default to "RUNNING"
```

---

## 3. GENERATE PR COMMENT

### Step 3.1: Check if Report Files Exist
```python
api_report = Path("JsonPlaceholder-API-Automation-Suite/api_report.xml")
ui_report = Path("SauceDemo-UI-Automation-Suite/ui_report.xml")

if api_report.exists():
    api_stats = parse_junit_report(str(api_report))
    # Returns: {total: 6, passed: 6, failed: 0, skipped: 0, time: 6.82}
else:
    logger.warning(f"API report not found: {api_report}")
    # Still continues, shows "No results yet"
```

**What each part means:**
- `total`: Number of test cases
- `passed`: Passed tests (tests - failures - errors)
- `failed`: Failed tests (failures + errors)
- `skipped`: Skipped tests
- `time`: Total execution time in seconds

### Step 3.2: Parse JUnit XML
```python
def parse_junit_report(report_path):
    tree = ET.parse(report_path)
    root = tree.getroot()
    
    # Root IS a testsuite element (not nested)
    if root.tag == "testsuite":
        testsuite = root
    else:
        testsuite = root.find("testsuite")
    
    # Extract stats from XML attributes
    stats = {
        "total": int(testsuite.get("tests", 0)),
        "passed": int(tests) - failures - errors,
        "failed": int(failures) + int(errors),
        "skipped": int(skipped),
        "time": float(time)
    }
    return stats
```

**Example XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="..." tests="6" failures="0" errors="0" skipped="0" time="6.82">
  <testcase classname="test_comments" name="test_get_comments" time="1.5"/>
  <testcase classname="test_posts" name="test_get_posts" time="2.1"/>
  ...
</testsuite>
```

### Step 3.3: Build Markdown Comment
```python
comment = "## 🧪 Test Report\n\n"
comment += f"**Status:** {status}\n"
comment += f"**Timestamp:** {datetime.now()...}\n\n"

# If API stats found, add them
if api_stats:
    comment += "### API Tests (JSONPlaceholder)\n"
    comment += f"- **Total:** {api_stats['total']}\n"
    comment += f"- **✅ Passed:** {api_stats['passed']}\n"
    # ... more fields

# If UI stats found, add them
if ui_stats:
    comment += "### UI Tests (SauceDemo)\n"
    # ... same as above

# Add Jenkins build link if available
jenkins_url = os.getenv("BUILD_URL", "")
if jenkins_url:
    comment += f"[View Full Report]({jenkins_url}Test_Report)\n"

return comment
```

**Output:**
```
## 🧪 Test Report

**Status:** RUNNING
**Timestamp:** 2026-01-25 12:42:30 UTC

### API Tests (JSONPlaceholder)
- **Total:** 6
- **✅ Passed:** 6
- **❌ Failed:** 0
- **⏭️ Skipped:** 0
- **⏱️ Duration:** 6.82s

### UI Tests (SauceDemo)
- **Total:** 5
- **✅ Passed:** 5
- **❌ Failed:** 0
- **⏭️ Skipped:** 0
- **⏱️ Duration:** 45.32s
```

---

## 4. PUBLISH TO GITHUB

### Step 4.1: Fetch Credentials
```python
github_token = os.getenv("GITHUB_TOKEN")
github_repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_PR_NUMBER")

# Must have ALL THREE to proceed
if not all([github_token, github_repo, pr_number]):
    logger.warning("GitHub environment variables not fully set")
    return  # Exit silently, no error
```

**What you set manually:**
```bash
export GITHUB_TOKEN=<your-personal-access-token>
export GITHUB_REPOSITORY=suraj-self/AutoTestLab
export GITHUB_PR_NUMBER=19
```

### Step 4.2: Build GitHub API Request
```python
# GitHub API endpoint for posting comments
url = f"https://api.github.com/repos/{github_repo}/issues/{pr_number}/comments"
# Result: https://api.github.com/repos/suraj-self/AutoTestLab/issues/19/comments

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}

data = {"body": comment}  # The markdown comment built above
```

### Step 4.3: POST Request
```python
response = requests.post(
    url,                      # GitHub API endpoint
    headers=headers,          # Auth headers with token
    json=data,                # Comment markdown
    timeout=30                # Wait max 30 seconds
)

if response.status_code == 201:
    logger.info("✅ Comment posted successfully")
    print("✅ Comment posted successfully to GitHub PR")
elif response.status_code == 403:
    logger.error(f"403 Forbidden: Token lacks permissions")
    # Issue: Token needs repo + write:discussion scopes
elif response.status_code == 404:
    logger.error(f"404 Not Found: PR doesn't exist")
    # Issue: PR #19 doesn't exist in that repo
```

**GitHub Response Timeline:**
```
Your request:
POST /repos/suraj-self/AutoTestLab/issues/19/comments
Authorization: token github_pat_...
{"body": "## 🧪 Test Report\n..."}
         │
         ├─ GitHub validates token
         ├─ GitHub checks if user can comment on PR
         ├─ GitHub validates PR exists
         ├─ GitHub stores comment in database
         └─ GitHub returns 201 Created ✓
         
Your comment now appears on GitHub PR #19
```

---

## 5. COMPLETE FLOW DIAGRAM WITH TIMING

```
START: python3 scripts/publish_pr_comment.py
   │
   ├─ [Logger setup] ........... 0.01s
   │
   ├─ [Read environment vars]... 0.01s
   │  └─ GITHUB_TOKEN
   │  └─ GITHUB_REPOSITORY
   │  └─ GITHUB_PR_NUMBER
   │
   ├─ [Parse api_report.xml].... 0.05s
   │  └─ ET.parse()
   │  └─ Extract <testsuite> stats
   │  └─ Return {total, passed, failed, skipped, time}
   │
   ├─ [Parse ui_report.xml]..... 0.05s
   │  └─ ET.parse()
   │  └─ Extract <testsuite> stats
   │  └─ Return {total, passed, failed, skipped, time}
   │
   ├─ [Build markdown comment].. 0.02s
   │  └─ String concatenation
   │  └─ Format timestamps
   │  └─ Add test results
   │
   ├─ [Print to console]........ 0.01s
   │  └─ User sees the comment preview
   │
   ├─ [POST to GitHub API]...... 1-3s (network depends)
   │  ├─ requests.post()
   │  ├─ GitHub validates
   │  ├─ GitHub stores comment
   │  └─ GitHub returns 201
   │
   └─ [Success message]......... 0.01s
      └─ "✅ Comment posted successfully to GitHub PR"

TOTAL TIME: ~1-3 seconds
```

---

## 6. ERROR HANDLING AT EACH STEP

```python
try:
    # Parse API report
    api_stats = parse_junit_report(api_report)
    # May fail with:
    # - FileNotFoundError: api_report.xml missing
    # - ET.ParseError: XML is invalid
    # - Exception: Any other error
    
    # If error: logger.error(...), returns None
    # Script CONTINUES (doesn't crash)
    
    if api_stats is None:
        # Shows "No results yet" in comment instead
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    # exc_info=True includes full stack trace in log
```

**Log output:**
```
2026-01-25 12:42:30 DEBUG pr_publisher [parse_junit_report]: Parsing JUnit report: SauceDemo-UI-Automation-Suite/ui_report.xml
2026-01-25 12:42:30 DEBUG pr_publisher [parse_junit_report]: JUnit report parsed successfully: 5 total, 5 passed, 0 failed
2026-01-25 12:42:30 INFO  pr_publisher [generate_pr_comment]: PR comment generated successfully
2026-01-25 12:42:30 INFO  pr_publisher [publish_to_github]: Publishing comment to GitHub
2026-01-25 12:42:31 DEBUG pr_publisher [publish_to_github]: Sending POST request to GitHub API
2026-01-25 12:42:32 INFO  pr_publisher [publish_to_github]: ✅ Comment posted successfully to GitHub PR
```

---

## 7. WHY JENKINS AUTOMATES THIS

### Without Jenkins (Manual - You Now)
```
You                    Script                GitHub              PR
 │                        │                     │                 │
 ├─ Run command            │                     │                 │
 │  python3 script.py      │                     │                 │
 │                         │                     │                 │
 │                    Parse reports             │                 │
 │                    Build comment             │                 │
 │                         │                     │                 │
 │                    POST comment              │                 │
 │                         ├─────────────────────────POST────────→ │
 │                         │              201 OK   │                │
 │                    Success logged    │                         ✓
 │                         │                     │                 │
 │  Get notification        │                     │                 │
 └─ Click GitHub PR       Comment posted!        │                 │

Issues:
- You must remember to run
- You must set env vars
- You must create report files
```

### With Jenkins (Automated)
```
GitHub Webhook          Jenkins Pipeline           GitHub          PR
       │                       │                      │              │
Push PR code ──webhook───→   Checkout              │              │
       │                       ├─ Fetch code         │              │
       │                       │                     │              │
       │                       ├─ Install deps       │              │
       │                       │                     │              │
       │                       ├─ Run API tests      │              │
       │                       │  (generates reports)               │
       │                       │                     │              │
       │                       ├─ Run UI tests       │              │
       │                       │  (generates reports)               │
       │                       │                     │              │
       │                  publish_pr_comment.py      │              │
       │                       ├─ Parse reports      │              │
       │                       ├─ Build comment      │              │
       │                       │                     │              │
       │                       ├─ POST comment       ├──POST───────→ │
       │                       │                 201 OK │            │
       │                  Log everything         ✓    │      ✅ Posted
       │                       │                     │              │
       └─ Jenkins notifies ← Success!              │              │
           (email/webhook)                         │              │

Benefits:
- Zero manual steps
- Automatic on every PR
- All logged
- One click to retry
```

---

## 8. EXAMPLE: FULL EXECUTION OUTPUT

```bash
$ export GITHUB_TOKEN=github_pat_...
$ export GITHUB_REPOSITORY=suraj-self/AutoTestLab
$ export GITHUB_PR_NUMBER=19
$ python3 scripts/publish_pr_comment.py

============================================================
Generating PR comment with test results...
============================================================

Generated Comment:

## 🧪 Test Report

**Status:** RUNNING
**Timestamp:** 2026-01-25 12:42:30 UTC

### API Tests (JSONPlaceholder)
- **Total:** 6
- **✅ Passed:** 6
- **❌ Failed:** 0
- **⏭️ Skipped:** 0
- **⏱️ Duration:** 6.82s

### UI Tests (SauceDemo)
- **Total:** 5
- **✅ Passed:** 5
- **❌ Failed:** 0
- **⏭️ Skipped:** 0
- **⏱️ Duration:** 45.32s


============================================================
Publishing to GitHub...
============================================================

✅ Comment posted successfully to GitHub PR
```

**Execution.log file:**
```
2026-01-25 12:42:30 DEBUG pr_publisher [<module>]: Logging initialized for PR publisher
2026-01-25 12:42:30 INFO  pr_publisher [main]: Starting PR comment publisher script
2026-01-25 12:42:30 INFO  pr_publisher [generate_pr_comment]: Generating PR comment with status: RUNNING
2026-01-25 12:42:30 DEBUG pr_publisher [generate_pr_comment]: API report found: JsonPlaceholder-API-Automation-Suite/api_report.xml
2026-01-25 12:42:30 INFO  pr_publisher [parse_junit_report]: Parsing JUnit report: JsonPlaceholder-API-Automation-Suite/api_report.xml
2026-01-25 12:42:30 DEBUG pr_publisher [parse_junit_report]: JUnit report parsed successfully: 6 total, 6 passed, 0 failed
2026-01-25 12:42:30 DEBUG pr_publisher [generate_pr_comment]: UI report found: SauceDemo-UI-Automation-Suite/ui_report.xml
2026-01-25 12:42:30 INFO  pr_publisher [parse_junit_report]: Parsing JUnit report: SauceDemo-UI-Automation-Suite/ui_report.xml
2026-01-25 12:42:30 DEBUG pr_publisher [parse_junit_report]: JUnit report parsed successfully: 5 total, 5 passed, 0 failed
2026-01-25 12:42:30 INFO  pr_publisher [generate_pr_comment]: PR comment generated successfully
2026-01-25 12:42:30 INFO  pr_publisher [publish_to_github]: Publishing comment to GitHub
2026-01-25 12:42:30 DEBUG pr_publisher [publish_to_github]: GitHub API URL: https://api.github.com/repos/suraj-self/AutoTestLab/issues/19/comments
2026-01-25 12:42:30 DEBUG pr_publisher [publish_to_github]: Sending POST request to GitHub API
2026-01-25 12:42:32 INFO  pr_publisher [publish_to_github]: ✅ Comment posted successfully to GitHub PR
2026-01-25 12:42:32 INFO  pr_publisher [main]: PR comment publisher script completed successfully
```

---

## Summary

| Stage | What Happens | Time | Logs To |
|-------|-------------|------|---------|
| 1. Init | Load logger, env vars | 0.02s | execution.log |
| 2. Parse API | Read XML, extract stats | 0.05s | execution.log + console |
| 3. Parse UI | Read XML, extract stats | 0.05s | execution.log + console |
| 4. Build Comment | String formatting | 0.02s | execution.log |
| 5. Display | Print to console | 0.01s | stdout |
| 6. GitHub POST | Network request + response | 1-3s | execution.log |
| 7. Success | Log completion | 0.01s | execution.log |

**Total: ~1-3 seconds end-to-end**

When Jenkins runs this: same process, just with:
- Env vars automatically set by Jenkins
- Reports generated by test stages
- Success/failure triggers post-build actions
