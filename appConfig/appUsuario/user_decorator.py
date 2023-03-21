from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import PermissionDenied

def validarPermisosEcosapp(primerLogin=False, contratoConfidencialidad=False, permisos=[]):
    """
    función que se opera como decorador sobre los views para validar las reglas de ejecución de las funciones view.
    reglas implementadas:\n
    (1) comprobamos que el usuario se encuentre logueado, en caso contrario se redirige a interfaz de login \n
    (2) comprobamos si es un usuario de tipo CLIENTE. El usuario NO es staff (usuario I+D ECOS) o superuser (usuario Equipo ECOS) \n
    (3) comprobamos que el usuario haya cambiado su contraseña por defecto \n
    (4) comprobamos que el usuario haya aceptado los acuerdos de confidencialidad \n
    """
    def wrap_view(view_function):
        """ función que recibe como parametro la función view """

        def validarReglas(request,*args, **kwargs):
            usuario_cliente = not any([request.user.is_staff, request.user.is_superuser])
            if request.user.is_authenticated: # (1)
                print('conectado')
            else:
                return redirect('login')
            
            # si todo es válido retornamos la función view con sus parametros request, *args y **kwargs
            return view_function(request, *args, **kwargs)
        
        validarReglas.__name__ = view_function.__name__
        validarReglas.__dict__ = view_function.__dict__
        validarReglas.__doc__ = view_function.__doc__

        return validarReglas
    
    return wrap_view