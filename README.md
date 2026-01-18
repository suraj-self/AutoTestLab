# AutoTestLab - Automation Frameworks

This repository includes comprehensive test automation frameworks for end-to-end testing using Python, pytest, and Selenium. It includes both API and UI test suites with integrated CI/CD via Jenkins.

## 📚 Test Suites

### 1. API Testing - JSONPlaceholder
- **Target**: [JSONPlaceholder API](https://www.jsonplaceholder.org/)
- **Framework**: pytest with requests
- **Features**:
  - JSON Schema validation
  - Multiple API endpoints testing
  - Custom pytest markers
  - HTML and JSON reports

### 2. UI Testing - SauceDemo
- **Target**: [SauceDemo Application](https://www.saucedemo.com/)
- **Framework**: Selenium with pytest
- **Features**:
  - Page Object Model design pattern
  - Selenium Grid support
  - Cross-browser testing capability
  - HTML reports

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- Python 3.8+

### 1. Local Setup (with Jenkins)

```bash
# Clone repository
git clone <repo-url>
cd AutoTestLab

# Run setup script
chmod +x setup-jenkins.sh
./setup-jenkins.sh
```

This starts:
- Jenkins on http://localhost:8080
- Selenium Hub on http://localhost:4444
- Chrome browser node

### 2. Run Tests Locally

```bash
# Start Docker containers (if not already running)
docker-compose up -d

# Run all tests
chmod +x run_tests.sh
./run_tests.sh all

# Run specific suite
./run_tests.sh api    # Only API tests
./run_tests.sh ui     # Only UI tests
```

### 3. Manual Test Execution

```bash
# API Tests
cd JsonPlaceholder-API-Automation-Suite
pip3 install -r requirements.txt
pytest tests/ -v --html=api_report.html

# UI Tests (with Selenium Grid)
cd SauceDemo-UI-Automation-Suite
export USE_GRID=true
export SELENIUM_HUB_URL=http://localhost:4444
pip3 install -r requirements.txt
pytest tests/ -v --html=ui_report.html
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│      GitHub Repository (with Webhooks)      │
│  (PR triggers Jenkins pipeline automatically) │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Jenkins Container (Orchestration & Reports) │
│  - Runs API Tests                            │
│  - Runs UI Tests (via Selenium Grid)         │
│  - Publishes results to PR                   │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────┴──────────┐
         ▼                    ▼
    ┌──────────┐        ┌───────────┐
    │ API Tests│        │Selenium   │
    │ JSONPlaceHolder  │ Hub & Chrome│
    └──────────┘        └───────────┘
```

## 📋 Project Structure

```
AutoTestLab/
├── JsonPlaceholder-API-Automation-Suite/
│   ├── tests/
│   ├── resource/          (JSON schemas)
│   ├── config.py
│   ├── requirements.txt
│   └── pytest.ini
│
├── SauceDemo-UI-Automation-Suite/
│   ├── tests/
│   ├── pages/             (Page Objects)
│   ├── utils/
│   │   └── browser.py     (WebDriver setup)
│   ├── conftest.py
│   └── requirements.txt
│
├── scripts/
│   ├── generate_report.py
│   ├── publish_pr_comment.py
│   └── requirements.txt
│
├── jenkins-init/
│   └── configure.groovy
│
├── Jenkinsfile            (CI/CD Pipeline)
├── docker-compose.yml     (Container setup)
├── setup-jenkins.sh       (Quick start script)
├── run_tests.sh           (Local test runner)
├── .env.example           (Configuration template)
├── JENKINS_SETUP.md       (Detailed setup guide)
└── README.md              (This file)
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Key variables:**
- `GITHUB_TOKEN`: GitHub Personal Access Token for PR comments
- `GITHUB_REPOSITORY`: Repository in format `owner/repo`
- `SELENIUM_HUB_URL`: Selenium Grid URL (default: http://localhost:4444)
- `USE_GRID`: Enable Selenium Grid (true/false)

### Jenkins Configuration

1. Access Jenkins: http://localhost:8080
2. Create new Pipeline job
3. Configure with GitHub repository URL
4. Set script path to `Jenkinsfile`
5. Add GitHub webhook for PR triggers

See [JENKINS_SETUP.md](JENKINS_SETUP.md) for detailed instructions.

## 📊 Reports

### Generated Reports

- **API Report**: `JsonPlaceholder-API-Automation-Suite/api_report.html`
- **UI Report**: `SauceDemo-UI-Automation-Suite/ui_report.html`
- **Combined Report**: `combined_report.html`
- **JUnit XML**: For CI/CD integration

### Viewing Reports

```bash
# Jenkins UI
# http://localhost:8080/job/AutoTestLab-Pipeline/

# Local reports (open in browser)
open combined_report.html
```

### GitHub PR Comments

Test results are automatically posted as PR comments when running via Jenkins with GitHub integration:

```
## 🧪 Test Report
**Status:** SUCCESS
**Timestamp:** 2024-01-18 10:30:45 UTC

### API Tests
- **Total:** 15 | **✅ Passed:** 15 | **❌ Failed:** 0

### UI Tests  
- **Total:** 6 | **✅ Passed:** 6 | **❌ Failed:** 0
```

## 🐳 Docker Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose stop

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart specific service
docker-compose restart jenkins

# Clean up
docker-compose down -v
```

## 🔍 Monitoring

### Selenium Grid Dashboard
- URL: http://localhost:4444/ui/index.html
- View active sessions, nodes, and capabilities

### Jenkins Dashboard
- URL: http://localhost:8080
- View job history, logs, and reports

### Container Logs
```bash
# Jenkins logs
docker logs -f jenkins

# Selenium Hub logs
docker logs -f selenium-hub

# Chrome node logs
docker logs -f selenium-chrome
```

## 🐛 Troubleshooting

### Selenium Hub not responding
```bash
# Check if hub is running
docker ps | grep selenium-hub

# Test connection
curl http://localhost:4444/wd/hub/status

# Check logs
docker logs selenium-hub
```

### Jenkins won't start
```bash
# Check logs
docker logs jenkins

# Increase timeout and retry
docker-compose restart jenkins
sleep 60
```

### Chrome tests failing
```bash
# Increase shared memory
# Edit docker-compose.yml: shm_size: 4gb

# Restart containers
docker-compose down
docker-compose up -d
```

See [JENKINS_SETUP.md](JENKINS_SETUP.md#troubleshooting) for more troubleshooting tips.

## 📚 Documentation

- [JENKINS_SETUP.md](JENKINS_SETUP.md) - Complete Jenkins setup guide
- [JsonPlaceholder-API-Automation-Suite/README.md](JsonPlaceholder-API-Automation-Suite/README.md) - API test suite details
- [SauceDemo-UI-Automation-Suite/README.md](SauceDemo-UI-Automation-Suite/README.md) - UI test suite details

## 🔑 Key Features

✅ **Automated Testing**
- API testing with schema validation
- UI testing with Page Object Model
- Parallel execution support

✅ **CI/CD Integration**
- GitHub webhook integration
- Automated PR comments with results
- Build artifact archiving

✅ **Containerization**
- Jenkins in Docker
- Selenium Grid with Chrome/Firefox nodes
- Isolated test environment

✅ **Reporting**
- HTML reports with trends
- JUnit XML for CI integration
- Combined multi-suite reports
- PR comments with test summary

✅ **Scalability**
- Multi-node Selenium Grid
- Parallel test execution
- Configurable browser instances

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request
5. Jenkins will automatically run tests and post results

## 📝 License

[Add your license information]

## 👥 Support

For issues, questions, or contributions:
- Check [JENKINS_SETUP.md](JENKINS_SETUP.md#troubleshooting)
- Review test logs in Jenkins UI
- Check Docker container logs

## 📦 Requirements

- Python 3.8+
- Docker 20.10+
- Docker Compose 1.29+
- Git

## 🔄 Updates

To update container images:

```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

---

**Last Updated:** January 18, 2024
