import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestPublicViews:
    """Tests para vistas públicas del sistema"""
    
    def test_registro_view_accessible(self):
        """Verifica que la vista de registro sea accesible sin autenticación"""
        client = Client()
        response = client.get(reverse('registro'))
        
        assert response.status_code == 200
        assert 'registro' in response.content.decode().lower()
    
    def test_login_view_accessible(self):
        """Verifica que la vista de login sea accesible sin autenticación"""
        client = Client()
        response = client.get(reverse('login'))
        
        assert response.status_code == 200

