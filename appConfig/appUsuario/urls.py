from django.urls import path

from appUsuario import views
# from appInicio import dx

urlpatterns = [
    path('login', views.login, name='login'),
]