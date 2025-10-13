"""Settings específicos para tests - Usa SQLite en lugar de PostgreSQL"""
from .settings import *

# Sobrescribir la configuración de base de datos para usar SQLite en tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

