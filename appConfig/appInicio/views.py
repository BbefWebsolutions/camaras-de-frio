from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from decouple import config

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
            'id': _camara.id,
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
        from_email = config('EMAIL_HOST_USER'),
        recipient_list = _receivers_list,
        fail_silently = False,
        html_message = _plantilla,
    )
    return _respuesta

def enviarCorreoCliente(request):
    _enviado = None
    _respuesta = 0
    _nombre_cliente = ''
    if request.method == 'POST':
        _correo = request.POST.get('correo-cliente')
        print(request.POST.get('numero-camara'))
        _camara = Camara.objects.get(id=int(request.POST.get('numero-camara')))
        print(_camara)
        _camara = []
        _checkbox = request.POST.get('check-datos-cliente')
        if _checkbox is None: # Cuando solo se debe enviar correo sin datos de cliente
            print('envio de correo prueba')
            _enviado = enviarCorreoCotizacion(_correo, _camara)
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
            _enviado = enviarCorreoCotizacion(_correo, _camara, _cliente)
    json = { 'respuesta': _respuesta, 'cliente': _nombre_cliente, 'enviado': _enviado }
    return JsonResponse(json, safe=False)

def guardarCamaraFrio(request):
    _respuesta = False
    if request.method == 'POST':
        _nombre = request.POST.get('nombre')
        _m2 = request.POST.get('m2')
        _m3 = request.POST.get('m3')
        _valor = Decimal(request.POST.get('neto'))
        _iva = Decimal(_valor*Decimal(1.19))
        _guia = request.FILES["guia"]
        try:
            _camara = Camara.objects.create(nombre=_nombre, m2=_m2, m3=_m3, valorNeto=_valor, valorIva=_iva, guia=_guia)
            _respuesta = True
        except:
            _respuesta = False
    json = { 'respuesta': _respuesta }
    return JsonResponse(json, safe=False)

def enviarCorreoCotizacion(_correo, _camara, _cliente=None):
    _respuesta = False
    try:
        # Iniciamos los parámetros del script
        remitente = config('EMAIL_HOST_USER')
        destinatarios = ['esalazar.in@gmail.com']
        password = config('EMAIL_HOST_PASSWORD')
        asunto = 'Cotización de Camara de Frio'

        # Armar correo con html
        _context = {
            'camara': _camara,
            'correo': _correo,
            'cliente': _cliente,
        }
        cuerpo = render_to_string('email/email_cotizacion.html', context = _context)

        # Buscar archivo correspondiente a la camara seleccionada
        ruta_adjunto = (r'media/'+_camara.guia)
        nombre_adjunto = str(_camara.guia)

        # Creamos el objeto mensaje
        mensaje = MIMEMultipart()
        
        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto
        
        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        
        # Abrimos el archivo que vamos a adjuntar
        archivo_adjunto = open(ruta_adjunto, 'rb')
        
        # Creamos un objeto MIME base
        adjunto_MIME = MIMEBase('application', 'octet-stream')

        # Y le cargamos el archivo adjunto
        adjunto_MIME.set_payload((archivo_adjunto).read())

        # Codificamos el objeto en BASE64
        encoders.encode_base64(adjunto_MIME)

        # Agregamos una cabecera al objeto
        adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)

        # Y finalmente lo agregamos al mensaje
        mensaje.attach(adjunto_MIME)
        
        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT', cast=int))
        
        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login(str(remitente),str(password))

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)

        # Cerramos la conexión
        sesion_smtp.quit()
        _respuesta = True
    except:
        print('No se ha enviado el correo')
    return _respuesta

