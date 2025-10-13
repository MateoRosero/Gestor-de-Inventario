pipeline {
  agent any
  options { timestamps() }
  environment {
    VENV_DIR = '.venv'
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PYTHONIOENCODING = 'utf-8'
    // Solo para crear el venv si quieres forzar Python 3.11:
    PY311 = 'C:\\Users\\Alienware\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
  }
  stages {
    stage('Build & Migrate') {
      steps {
        checkout scm
        bat """
          if not exist %VENV_DIR% (
            "%PY311%" -m venv %VENV_DIR%
          )
          call %VENV_DIR%\\Scripts\\activate
          rem A PARTIR DE AQUI, USA EL PYTHON DEL VENV
          python -m pip install --upgrade pip
          if exist requirements.txt (
            python -m pip install -r requirements.txt
          ) else (
            python -m pip install Django pytest pytest-django pytest-cov
          )
          rem Ejecuta manage.py con el python del venv
          python manage.py migrate --noinput
        """
      }
    }

    stage('Tests & Reports') {
      steps {
        bat """
          call %VENV_DIR%\\Scripts\\activate
          if not exist reports mkdir reports
          rem pytest del venv
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
