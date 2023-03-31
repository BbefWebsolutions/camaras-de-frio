### django
from django.urls import path
### APP's
from appInicio import views, dx

urlpatterns = [
    path('', views.inicio, name='inicio'),
    ### CAMARA
    path('guardar-camara-frio/', views.guardarCamaraFrio, name='guardar-camara-frio'),
    path('cambiar-valor-km/', views.cambiarValorKm, name='cambiar-valor-km'),
    path('cambiar-precio-camara/', views.cambiarPrecioCamara, name='cambiar-precio-camara'),
    ### EMAIL
    path('envio-correo-prueba/', views.enviarCorreoCotizacion, name='envio-correo-prueba'),
    path('envio-correo-cliente/', views.enviarCorreoCliente, name='envio-correo-cliente'),
    ### JSON
    path('json-listar-comuna/<int:id>', dx.jsonListarComunas, name='json-listar-comunas'),
    path('json-listar-camaras/', dx.jsonListarCamaras, name='json-listar-camaras')
]