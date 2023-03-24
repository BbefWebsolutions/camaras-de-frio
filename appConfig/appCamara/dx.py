from django.http import JsonResponse
from django.db.models import Max
from appCamara.models import Camara, Cotizacion

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

def correlativoCotizacion():
    _correlativo = 0
    _cotizacion = Cotizacion.objects.filter(registroActivo=True).aggregate(maximo=Max('correlativo'))
    if _cotizacion['maximo']:
        _correlativo = _cotizacion['maximo'] + 1
    else:
        _correlativo = 3211
    return _correlativo