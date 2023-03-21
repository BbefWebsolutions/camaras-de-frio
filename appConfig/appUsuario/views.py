from django.shortcuts import render, redirect
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import authenticate, get_user, login as auth_login, logout as auth_logout
# Create your views here.
def login(request):
    if request.method == 'POST':
        data = request.POST
        nombre_usuario, contrasena = data.get('username'), data.get('password')
        usuario = authenticate(username=nombre_usuario, password=contrasena)
        if usuario:
            print('usuario')
            auth_login(request, usuario)
            return redirect('inicio')
        else:
            print('no okta')
            msg = "Usuario y/o contraseña invalidos"
            # messages.error(request, msg)
    _context ={}
    return render(request, 'login/login.html', context = _context)