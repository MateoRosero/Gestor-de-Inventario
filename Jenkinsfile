pipeline {
  agent any
  options { timestamps() }
  environment {
    VENV_DIR = '.venv'
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PYTHONIOENCODING = 'utf-8'
  }
  stages {
    stage('Build & Migrate') {
      steps {
        checkout scm
        bat """
          if not exist %VENV_DIR% (
            python -m venv %VENV_DIR%
          )
          call %VENV_DIR%\\Scripts\\activate
          python -m pip install --upgrade pip
          if exist requirements.txt (
            pip install -r requirements.txt
          ) else (
            pip install Django pytest pytest-django pytest-cov
          )
          python manage.py migrate --noinput
        """
      }
    }

    stage('Tests & Reports') {
      steps {
        bat """
          call %VENV_DIR%\\Scripts\\activate
          if not exist reports mkdir reports
          set DJANGO_SETTINGS_MODULE=gestor_inventario.settings_test
          pytest --junitxml=reports\\junit.xml --cov=. --cov-report=xml:reports\\coverage.xml
        """
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/junit.xml'
          publishCoverage adapters: [jacocoAdapter('reports/coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
          archiveArtifacts artifacts: 'db.sqlite3, reports/**', fingerprint: true, onlyIfSuccessful: false
        }
      }
    }
  }
  post { always { echo 'CI listo.' } }
}

