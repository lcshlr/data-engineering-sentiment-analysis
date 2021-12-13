def sentiment_server_public_ip

pipeline {
   agent any
        environment {
        EC2_IP = sh(script: 'curl http://169.254.169.254/latest/meta-data/public-ipv4', returnStdout: true)
    }
    
    stages {
        stage('Clean Jenkins Workspace') {
            steps {
                cleanWs()
            }
        }
        
        stage('check Vars') {
            steps {
                sh "echo check first if vars are compliant"
                sh "echo ENV: $ENV"
            }
        }
        
        stage('checkout git') {
            steps {
                sh "pwd"
                dir("docker") {
                    sh "pwd"
                    git(
                        url: 'https://github.com/lcshlr/data-engineering-sentiment-analysis',
                        credentialsId: '30a16394-5cbc-4794-adeb-a048328f61fc',
                        branch: "${GitBranch}"
                    )
                    sh "ls"
                }
            }
        }
        
        stage('Create Server') {
            steps {
                dir("docker/devops") {
                        sh "pwd"
                        sh "ls"
                        script {
                               sh "ls"
                               sh "terraform init -backend-config='bucket=bucket-sentiment-server' -backend-config='key=$APP_NAME/$ENV/deploy_sentiment_server.tfstate' -backend-config='region=eu-west-3'"
                			   sh "terraform apply -auto-approve -var 'EC2_IP=$EC2_IP' "
                               sentiment_server_public_ip = sh(returnStdout: true, script: "terraform output --raw sentiment_server_public_ip").trim()
                        }
                }
            }
        }
        stage ("Launch docker playbook"){
            steps {
                dir("docker/devops") {
                        ansiblePlaybook(
                            playbook: 'launch_docker_compose.yml',
                            inventory: "${sentiment_server_public_ip},",
                            credentialsId: '0844dca1-b50c-4abf-8501-113b9ddcf408',
                            become: true,
                            disableHostKeyChecking: true,
                            extras: "-e public_ip='${sentiment_server_public_ip}'"
                        ) 
                        
                   }
            }
         }
        }
       
    }
