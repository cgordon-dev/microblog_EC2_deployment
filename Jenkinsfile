pipeline {
  agent any
    stages {
        stage ('Build') {
            steps {
                echo 'Setting up the Python virtual environment...'
                sh '''#!/bin/bash
                    python3.9 -m venv venv
                    source venv/bin/activate
                '''

                echo 'Installing Python dependencies...'
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install gunicorn pymysql cryptography
                    pip install pytest
                '''
                echo 'Setting environmental variables...'
                sh '''
                    export FLASK_APP=microblog.py
                '''

                echo 'Upgrading the database...'
                sh '''
                    flask db upgrade
                '''
            }
        }
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
                py.test ./tests/unit/ --verbose --junit-xml test-reports/results.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
                success {
                    echo 'All tests passed successfully.'
                }
                failure {
                    echo 'Some tests have failed, check the test reports for details.'
                }
            }
        }
      stage ('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
      stage ('Clean') {
            steps {
                sh '''#!/bin/bash
                if [[ $(ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2) != 0 ]]
                then
                ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2 > pid.txt
                kill $(cat pid.txt)
                exit 0
                fi
                '''
            }
        }
      stage ('Deploy') {
            steps {
                sh '''#!/bin/bash
                <enter your code here>
                '''
            }
        }
    }
}
