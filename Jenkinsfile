pipeline {
  agent any
  options { timestamps() }
  environment {
    VENV_DIR = '.venv'
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PYTHONIOENCODING = 'utf-8'
    // 👉 Ajusta si usas otra versión/ruta
    PYTHON_EXE = 'C:\\Users\\Alienware\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
  }
  stages {
    stage('Build & Migrate') {
      steps {
        checkout scm
        bat """
          if not exist %VENV_DIR% (
            "%PYTHON_EXE%" -m venv %VENV_DIR%
          )
          call %VENV_DIR%\\Scripts\\activate
          "%PYTHON_EXE%" -m pip install --upgrade pip
          if exist requirements.txt (
            pip install -r requirements.txt
          ) else (
            pip install Django pytest pytest-django pytest-cov
          )
          REM Si manage.py está en subcarpeta, haz: cd backend (por ejemplo) ANTES de la siguiente línea
          "%PYTHON_EXE%" manage.py migrate --noinput
        """
      }
    }

    stage('Tests & Reports') {
      steps {
        bat """
          call %VENV_DIR%\\Scripts\\activate
          if not exist reports mkdir reports
          REM Pytest usará el DJANGO_SETTINGS_MODULE de pytest.ini
          REM Si tu manage.py está en subcarpeta, haz: cd backend ANTES de pytest
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
