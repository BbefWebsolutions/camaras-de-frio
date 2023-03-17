from django.urls import path
from appCamara import dx

urlpatterns = [
    path('json-listar-camaras', dx.jsonListarCamaras, name='json-listar-camaras'),
]