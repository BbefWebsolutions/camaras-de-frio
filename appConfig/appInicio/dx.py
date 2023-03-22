from django.http import JsonResponse
from appInicio.models import Comuna

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

