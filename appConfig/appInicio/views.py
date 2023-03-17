from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

## NEW
from email.message import EmailMessage
import smtplib

# APP's
from appCamara.models import Camara
from appInicio.models import Region, Provincia, Comuna
from appCliente.models import Cliente


# Create your views here.

def inicio(request):
    _data = []
    _camaras = Camara.objects.filter(registroActivo=True)
    _regiones = Region.objects.filter(registroActivo=True)
    _comunas = Comuna.objects.filter(registroActivo=True)
    for _camara in _camaras:
        _neto = ('{:,.0f}'.format(_camara.valorNeto)).replace(',', '.')
        _iva = ('{:,.0f}'.format(_camara.valorIva)).replace(',', '.')
        _item = {
            'nombre': _camara.nombre,
            'm2': str(_camara.m2).replace('.', ','),
            'm3': str(_camara.m3).replace('.', ','),
            'valorNeto': _neto,
            'valorIva': _iva,
        }
        _data.append(_item)
        
    _context = {
        'camaras': _data,
        'regiones': _regiones,
        'comunas': _comunas,
    }
    return render(request, "inicio.html", context=_context)

def sendEmail(correo, camara, cliente=None):
    _subject = 'Cotización de Camara de Frío'
    _context = {
        'dominio': 'localhost:8000',
        'protocolo': 'http',
        'correo': correo,
        'camara': camara,
    }
    _plantilla = render_to_string('email/email_cotizacion.html', context = _context)
    _receivers_list = [correo]
    _respuesta = send_mail(
        subject = _subject,
        message = strip_tags(_plantilla),
        from_email = 'contacto@camarasdefrio.com',
        recipient_list = _receivers_list,
        fail_silently = False,
        html_message = _plantilla,
    )
    return _respuesta

def enviarCorreoCliente(request):
    _respuesta = 0
    _nombre_cliente = ''
    if request.method == 'POST':
        _correo = request.POST.get('correo-cliente')
        _camara = Camara.objects.get(id=int(request.POST.get('numero-camara')))
        _checkbox = request.POST.get('check-datos-cliente')
        if _checkbox is None: # Cuando solo se debe enviar correo sin datos de cliente
            print('none type es ')
            # sendEmail(_correo, _camara)
            _respuesta = 1
        else:
            _nombre = request.POST.get('nombre')
            _rut = request.POST.get('rut')
            _giro = request.POST.get('giro')
            _region = Region.objects.get(id=request.POST.get('region'))
            _comuna = Comuna.objects.get(id=request.POST.get('comuna'))
            _direccion = request.POST.get('direccion')
            _telefono = request.POST.get('telefono')
            _correo = request.POST.get('correo-cliente')
            try:
                _cliente = Cliente.objects.get(rut=_rut)
                _cliente.nombre = _nombre
                _cliente.giro = _giro
                _cliente.region = _region
                _cliente.comuna = _comuna
                _cliente.direccion = _direccion
                _cliente.telefono = _telefono
                _cliente.save()
                _respuesta = 2
            except Cliente.DoesNotExist:
                _cliente = Cliente.objects.create(nombre=_nombre, rut=_rut, giro=_giro, region=_region, comuna=_comuna, direccion=_direccion, telefono=_telefono, correo=_correo)
                _respuesta = 3  
            _nombre_cliente = _cliente.nombre
            # sendEmail(_correo, _camara, _cliente)
    json = { 'respuesta': _respuesta, 'cliente': _nombre_cliente }
    return JsonResponse(json, safe=False)

def guardarCamaraFrio(request):
    _respuesta = False
    if request.method == 'POST':
        _nombre = request.POST.get('nombre-camara')
        _m2 = request.POST.get('metro-cuadrado')
        _m3 = request.POST.get('metro-cubico')
        _valor = Decimal(request.POST.get('valor'))
        _iva = Decimal(_valor*Decimal(1.19))
        try:
            _camara = Camara.objects.create(nombre=_nombre, m2=_m2, m3=_m3, valorNeto=_valor, valorIva=_iva)
            _respuesta = True
        except:
            _respuesta = False
    json = { 'accionEjecutada': _respuesta }
    return JsonResponse(json, safe=False)

