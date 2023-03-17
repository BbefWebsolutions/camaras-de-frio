from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.contrib.auth.models import User

from appConfig.settings import INSTALLED_APPS, BASE_DIR
from appInicio.models import Region, Provincia, Comuna

import csv
import os


class Command(BaseCommand):
    help = 'Creación de datos iniciales para el levantamiento del sistema'

    def handle(self, *args, **options):
        try:
            _usuarioAdmin = User.objects.get(is_staff=True)
            _fechaEjecucion = timezone.now()
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No existe un super usuario para ejecutar la acción solicitada'))
            raise CommandError('SuperUsuario no existe')

        # creación de los permisos por cada app registrada en ECOS_APPS de SETTINGS
        # try:
        #     _mensaje = permisosIniciales(_usuarioAdmin, _fechaEjecucion)
        #     self.stdout.write(self.style.SUCCESS(_mensaje))
        # except:
        #     self.stdout.write(self.style.ERROR('FAIL: Error al crear los PERMISOS'))

        # Crear Regiones
        try:
            _mensaje = regionesIniciales(_usuarioAdmin, _fechaEjecucion)
            self.stdout.write(self.style.SUCCESS(_mensaje))
        except:
            self.stdout.write(self.style.ERROR('FAIL: Error al crear las REGIONES'))

        # Crear Provincias
        try:
            _mensaje = provinciasIniciales(_usuarioAdmin, _fechaEjecucion)
            self.stdout.write(self.style.SUCCESS(_mensaje))
        except:
            self.stdout.write(self.style.ERROR('FAIL: Error al crear las PROVINCIAS'))

        # Crear Comunas
        try:
            _mensaje = comunasIniciales(_usuarioAdmin, _fechaEjecucion)
            self.stdout.write(self.style.SUCCESS(_mensaje))
        except:
            self.stdout.write(self.style.ERROR('FAIL: Error al crear las COMUNAS'))



def regionesIniciales(usuario, fecha):
    _rutaArchivo = os.path.join(BASE_DIR, os.path.normcase('appInicio/archivosTablasIniciales/regionesIniciales.csv'))

    with open(_rutaArchivo, 'r', encoding='utf-8') as _regiones:
        _listaRegiones = list(csv.DictReader(_regiones))

    _mensaje = ''
    if Region.objects.all().exists():
        _mensaje = 'OK: Ya existen registros en el modelo REGION'
    else:
        for _region in _listaRegiones:
            _region['registroActivo'] = True
            _region['registroFechaCreacion'] = fecha
            # _region['registroUsuarioCreacion'] = usuario
            # _region['registroUsuarioModificacion'] = usuario
            Region.objects.create(**_region)
        _mensaje = 'DONE: Regiones Creadas'

    return _mensaje


def provinciasIniciales(usuario, fecha):
    _rutaArchivo = os.path.join(BASE_DIR, os.path.normcase('appInicio/archivosTablasIniciales/provinciasIniciales.csv'))

    with open(_rutaArchivo, 'r', encoding='utf-8') as _provincias:
        _listaProvincias = list(csv.DictReader(_provincias))

    _mensaje = ''
    if Provincia.objects.all().exists():
        _mensaje = 'OK: Ya existen registros en el modelo PROVINCIA'
    else:
        for _registroProvincia in _listaProvincias:
            _registroProvincia['region'] = Region.objects.get(codigo_iso=_registroProvincia.pop('codigo_iso'))
            _registroProvincia['registroActivo'] = True
            _registroProvincia['registroFechaCreacion'] = fecha
            # _registroProvincia['registroUsuarioCreacion'] = usuario
            # _registroProvincia['registroUsuarioModificacion'] = usuario

            Provincia.objects.create(**_registroProvincia)
        _mensaje = 'DONE: Provincias Creadas'

    return _mensaje


def comunasIniciales(usuario, fecha):
    _rutaArchivo = os.path.join(BASE_DIR, os.path.normcase('appInicio/archivosTablasIniciales/comunasIniciales.csv'))

    with open(_rutaArchivo, 'r', encoding='utf-8') as _comunas:
        _listaComunas = list(csv.DictReader(_comunas))

    _mensaje = ''
    if Comuna.objects.all().exists():
        _mensaje = 'OK: Ya existen registros en el modelo COMUNA'
    else:
        for _registroComuna in _listaComunas:
            _registroComuna['provincia'] = Provincia.objects.get(nombre=_registroComuna.pop('nombreProvincia'))
            _registroComuna['registroActivo'] = True
            _registroComuna['registroFechaCreacion'] = fecha
            # _registroComuna['registroUsuarioCreacion'] = usuario
            # _registroComuna['registroUsuarioModificacion'] = usuario

            Comuna.objects.create(**_registroComuna)
        _mensaje = 'DONE: Comunas Creadas'

    return _mensaje


