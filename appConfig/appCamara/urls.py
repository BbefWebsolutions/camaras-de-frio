from django.urls import path
from appCamara import dx

urlpatterns = [
    path('inicio-listar-camaras', dx.jsonListarCamaras, name='inicio-listar-camaras'),
]