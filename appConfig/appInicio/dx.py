from django.http import JsonResponse
from appInicio.models import Comuna
from appCamara.models import Camara

def jsonListarComunas(request, id):
    _data = []
    _respuesta = False
    try:
        _comunas = Comuna.objects.filter(registroActivo=True, provincia__region__id=id)
        for _comuna in _comunas:
            _item = {
                'id': _comuna.id,
                'nombre': _comuna.nombre,
            }
            _data.append(_item)
        _respuesta = True
    except ValueError:
        print('Ha ocurrido un error en la view de app inicio!!!')

    _context = {
        'respuesta': _respuesta,
        'data': _data
    }
    return JsonResponse(_context, safe=False)

def jsonListarCamaras(request):
    _data = []
    try:
        _camaras = Camara.objects.filter(registroActivo=True)
        for _camara in _camaras:
            _item = {
                'id': _camara.id,
                'nombre': _camara.nombre if _camara.nombre else '',
                'm2': _camara.m2 if _camara.m2 else '',
                'm3': _camara.m3 if _camara.m3 else '',
                'uf': _camara.uf if _camara.uf else '',
                'neto': _camara.valorNeto if _camara.valorNeto else '',
                'iva': _camara.valorIva if _camara.valorIva else '',
                'ficha': 'media/'+str(_camara.ficha),
            }
            _data.append(_item)
    except ValueError:
        print('Ha ocurrido un error en la view de app inicio!!!')
    return JsonResponse(_data, safe=False)

