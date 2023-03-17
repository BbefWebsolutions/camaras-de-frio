from django.http import JsonResponse
from appCamara.models import Camara

def jsonListarCamaras(request):
    _data = []
    _camaras = Camara.objects.filter(registroActivo=True)
    for _camara in _camaras:
        _item = {
            'nombre': _camara.nombre,
            'm2': _camara.m2,
            'm3': _camara.m3,
            'neto': _camara.valorNeto,
            'iva': _camara.valorIva,
        }
        _data.append(_item)
    return JsonResponse(_data, safe=False)
