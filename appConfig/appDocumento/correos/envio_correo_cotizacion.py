import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
from django.template.loader import render_to_string
from appDocumento.documentos.crear_cotizacion import crearCotizacion

remplazar_tildes = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )

def enviarCorreoCotizacion(_correo, _camara, _observacion, _descuento, _cliente=None):
    _respuesta = False
    # try:
    # Iniciamos los parámetros del script
    remitente = config('EMAIL_HOST_USER')
    destinatarios = [_correo]
    password = config('EMAIL_HOST_PASSWORD')
    asunto = 'Cotización de Camara de Frio'

    # Armar correo con html
    _context = {
        'camara': _camara,
        'correo': _correo,
        'cliente': _cliente,
    }
    cuerpo = render_to_string('email/email_cotizacion.html', context = _context)

    _nombre_camara = _camara.nombre.replace(' ','_').replace('.', '').replace(',', '')
    for a, b in remplazar_tildes:
        _nombre_camara = _nombre_camara.replace(a, b).replace(a.upper(), b.upper())

    # Buscar archivo correspondiente a la camara seleccionada
    ruta_ficha = (r'media/'+str(_camara.ficha))
    nombre_ficha = str(_nombre_camara)+'.pdf'

    # Crear cotización y buscar en la ruta del archivo creado
    crearCotizacion(_camara, _correo, _observacion, _descuento, _cliente);
    ruta_cotizacion = (r'media/cotizaciones/Cotizacion_camara.pdf')
    nombre_cotizacion = 'Cotizacion_de_camara.pdf'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'html'))
    
    # Abrimos el archivo que vamos a adjuntar
    ficha_adjunto = open(ruta_ficha, 'rb')
    adjunto_primero = MIMEBase('application', 'octet-stream')
    adjunto_primero.set_payload((ficha_adjunto).read())
    encoders.encode_base64(adjunto_primero)
    adjunto_primero.add_header('Content-Disposition', "attachment; filename= %s" % nombre_ficha)
    mensaje.attach(adjunto_primero)
    ficha_adjunto.close()

    # Abrimos cotización que vamos a adjuntar
    cotizacion_adjunto = open(ruta_cotizacion, 'rb')
    adjunto_segundo = MIMEBase('application', 'octet-stream')
    adjunto_segundo.set_payload((cotizacion_adjunto).read())
    encoders.encode_base64(adjunto_segundo)
    adjunto_segundo.add_header('Content-Disposition', "attachment; filename= %s" % nombre_cotizacion)
    mensaje.attach(adjunto_segundo)
    cotizacion_adjunto.close()
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT', cast=int))
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login(str(remitente), str(password))

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()
    _respuesta = True
    # except:
    #     print('No se ha enviado el correo')
    return _respuesta
