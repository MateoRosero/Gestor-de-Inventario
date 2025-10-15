pipeline {
  agent any
  options { timestamps() }
  environment {
    VENV_DIR = '.venv'
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PYTHONIOENCODING = 'utf-8'
    PY311 = 'C:\\Users\\Alienware\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
    DJANGO_SETTINGS_MODULE = 'gestor_inventario.settings_ci'
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
          rem  Ejecuta migrate usando settings_ci.py (SQLite)
          python manage.py migrate --noinput --settings=%DJANGO_SETTINGS_MODULE%
        """
      }
    }

    stage('Tests') {
      steps {
        bat """
          call %VENV_DIR%\\Scripts\\activate
          if not exist reports mkdir reports
          rem  pytest usa settings_ci.py (SQLite)
          pytest --ds=%DJANGO_SETTINGS_MODULE% --junitxml=reports\\junit.xml --cov=. --cov-report=xml:reports\\coverage.xml
        """
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/junit.xml'
          archiveArtifacts artifacts: 'db.sqlite3, reports/**', fingerprint: true, onlyIfSuccessful: false
        }
      }
    }
  }
  post { always { echo 'CI listo.' } }
}
