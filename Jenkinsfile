pipeline {
  agent any
  stages {
    stage('Initializing') {
      steps {
        echo 'Initializing ...'
        sh 'echo "Working from $WORKSPACE"'
        sh '''echo "Your build number is: \\${BUILD_NUMBER} -> ${BUILD_NUMBER}"
echo "Your build number is: \\${REQUEST_ID} -> ${REQUEST_ID}"'''
      }
    }

    stage('Fetching Repos') {
      parallel {
        stage('Fetching API') {
          steps {
            echo 'Starting to fetch API from GitHub'
            echo 'Checking if BHT-EMR-API exists.'
            sh '[ -d "BHT-EMR-API" ] && echo "API already cloned." || git clone https://github.com/HISMalawi/BHT-EMR-API.git'
            echo 'Giving access to all users'
            sh 'cd $WORKSPACE && chmod 777 BHT-EMR-API'
            echo 'Fetching Tags'
            sh 'cd $WORKSPACE/BHT-EMR-API && git fetch --tags -f'
            echo 'Checking out to Latest Tag'
            sh '''#cd $WORKSPACE/BHT-EMR-API && git checkout v4.10.44
#$(git describe --tags `git rev-list --tags --max-count=1`)'''
            sh '#cd $WORKSPACE/BHT-EMR-API && git describe > HEAD'
          }
        }

        stage('Fetching Core') {
          steps {
            echo 'Starting to fetch Core from GitHub'
            echo 'Checking if HIS-Core exists.'
            sh '[ -d "HIS-Core" ] && echo "Core already cloned." || git clone https://github.com/HISMalawi/HIS-Core-release.git HIS-Core'
            echo 'Giving access to users'
            sh 'cd $WORKSPACE && chmod 777 HIS-Core'
            echo 'Fetching New Tags'
            sh 'cd $WORKSPACE/HIS-Core && git fetch --tags -f'
            echo 'Checking out to latest tag'
            sh '#cd $WORKSPACE/HIS-Core && git checkout $(git describe --tags `git rev-list --tags --max-count=1`)'
          }
        }

      }
    }

    stage('Shipping & Configurations') {
      parallel {
        stage('API') {
          steps {
            echo 'shipping & Configuring API'
            sh '''python3 api_shippingx.py



'''
          }
        }

        stage('HIS-Core ') {
          steps {
            echo 'Shipping & configuring Core & ART'
            sh '''python3 core_shippingx.py
'''
          }
        }

      }
    }

  }
  environment {
    REQUEST_ID = 'true'
    CLUSTER_ID = '12345'
  }
}