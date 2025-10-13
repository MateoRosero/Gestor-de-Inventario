"""Settings para CI/Jenkins - Fuerza SQLite en lugar de PostgreSQL"""
from .settings import *

# Forzar base de datos SQLite en CI (no requiere servidor PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # BASE_DIR viene de settings.py
    }
}

# Relajar hosts para CI
ALLOWED_HOSTS = ["*"]

# Mantener DEBUG en False para simular producción (pero con SQLite)
DEBUG = False

