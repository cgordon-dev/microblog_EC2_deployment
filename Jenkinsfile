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
                if [[ $(pgrep gunicorn | wc -l) -gt 0 ]]
                then
                    pgrep gunicorn > pid.txt
                    kill $(cat pid.txt)
                    echo 'Gunicorn processes terminated.'
                else
                    echo 'No Gunicorn processes found.'
                fi
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application to EC2 instance...'
                
                sshagent(['EC2_SSH_Credentials']) { 
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@34.203.240.181 << 'EOF'
                            echo 'Pulling latest code...'
                            cd ~/microblog_EC2_deployment
                            git pull origin main

                            echo 'Activating virtual environment...'
                            source venv/bin/activate

                            echo 'Installing dependencies...'
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install gunicorn pymysql cryptography

                            echo 'Applying database migrations...'
                            flask db upgrade

                            echo 'Restarting Gunicorn service...'
                            sudo systemctl restart gunicorn

                            echo 'Deployment completed successfully.'
                        EOF
                    '''
                }
            }
            post {
                success {
                    echo 'Deployment stage completed successfully.'
                }
                failure {
                    echo 'Deployment stage failed.'
                }
            }
        }
    }
}
