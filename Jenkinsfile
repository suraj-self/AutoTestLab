pipeline {
    agent any
    
    parameters {
        string(name: 'SELENIUM_HUB_URL', defaultValue: 'http://selenium-hub:4444', description: 'Selenium Hub URL')
        string(name: 'GITHUB_PR_NUMBER', defaultValue: '', description: 'GitHub PR number (optional)')
    }
    
    environment {
        DOCKER_NETWORK = 'jenkins-test-network'
        SELENIUM_HUB_URL = 'http://selenium-hub:4444'
        CHROME_DRIVER_URL = 'http://chrome:4444'
        PYTHONUNBUFFERED = '1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '========== Checking out code =========='
                checkout scm
                script {
                    // Get PR information if available
                    if (env.CHANGE_ID) {
                        echo "Building PR #${env.CHANGE_ID}"
                        env.GITHUB_PR_NUMBER = env.CHANGE_ID
                    }
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo '========== Setting up Python environment =========='
                sh '''
                    python3 --version
                    pip3 install --upgrade pip
                '''
            }
        }
        
        stage('Install API Dependencies') {
            steps {
                echo '========== Installing API test dependencies =========='
                sh '''
                    cd JsonPlaceholder-API-Automation-Suite
                    pip3 install -r requirements.txt
                    cd ..
                '''
            }
        }
        
        stage('Install UI Dependencies') {
            steps {
                echo '========== Installing UI test dependencies =========='
                sh '''
                    cd SauceDemo-UI-Automation-Suite
                    pip3 install -r requirements.txt
                    cd ..
                '''
            }
        }
        
        stage('Wait for Selenium Hub') {
            steps {
                echo '========== Waiting for Selenium Hub to be ready =========='
                sh '''
                    timeout 60 bash -c 'until curl -s http://selenium-hub:4444/wd/hub/status | grep -q "\"ready\":true"; do 
                        echo "Waiting for Selenium Hub..."
                        sleep 2
                    done'
                    echo "Selenium Hub is ready!"
                '''
            }
        }
        
        stage('Run API Tests') {
            steps {
                echo '========== Running API Tests =========='
                sh '''
                    cd JsonPlaceholder-API-Automation-Suite
                    python3 -m pytest tests/ -v --tb=short \
                        --html=api_report.html \
                        --json-report \
                        --json-report-file=api_report.json \
                        --junitxml=api_report.xml || true
                    cd ..
                '''
            }
        }
        
        stage('Run UI Tests') {
            steps {
                echo '========== Running UI Tests =========='
                sh '''
                    cd SauceDemo-UI-Automation-Suite
                    python3 -m pytest tests/ -v --tb=short \
                        --html=ui_report.html \
                        --junitxml=ui_report.xml || true
                    cd ..
                '''
            }
        }
        
        stage('Generate Combined Report') {
            steps {
                echo '========== Generating combined test report =========='
                sh '''
                    python3 scripts/generate_report.py
                '''
            }
        }
        
        stage('Publish PR Comment') {
            when {
                expression {
                    return env.GITHUB_PR_NUMBER != null && env.GITHUB_PR_NUMBER != ''
                }
            }
            steps {
                echo '========== Publishing results to GitHub PR =========='
                sh '''
                    python3 scripts/publish_pr_comment.py
                '''
            }
        }
    }
    
    post {
        always {
            echo '========== Archiving test reports =========='
            archiveArtifacts artifacts: '**/api_report.html, **/ui_report.html, **/api_report.json, **/combined_report.html', 
                             allowEmptyArchive: true
            
            junit testResults: '**/api_report.xml, **/ui_report.xml', 
                  allowEmptyResults: true
        }
        
        failure {
            echo '========== Build Failed =========='
            script {
                if (env.GITHUB_PR_NUMBER) {
                    sh 'python3 scripts/publish_pr_comment.py FAILED'
                }
            }
        }
        
        success {
            echo '========== Build Successful =========='
            script {
                if (env.GITHUB_PR_NUMBER) {
                    sh 'python3 scripts/publish_pr_comment.py SUCCESS'
                }
            }
        }
    }
}
