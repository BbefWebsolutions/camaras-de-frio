from django.db import models
### APPS
from appInicio.models import Region, Comuna

# Create your models here.

class Cliente ( models.Model ):
    ### Atributos del Modelo ###
    nombre = models.CharField( max_length = 200, default = None, null=True, blank=True, verbose_name = 'Nombre' )
    rut = models.CharField( max_length = 200, default = None, null=True, blank=True, verbose_name = 'RUT' )
    giro = models.CharField( max_length = 200, default = None, null=True, blank=True, verbose_name = 'Giro Comercial' )
    region = models.ForeignKey(Region, on_delete = models.CASCADE, verbose_name = 'Región')
    comuna = models.ForeignKey(Comuna, on_delete = models.CASCADE, verbose_name = 'Comuna')
    direccion = models.CharField( max_length = 200, default = None, null=True, blank=True, verbose_name = 'Dirección' )
    telefono = models.CharField( max_length = 200, default = None, null=True, blank=True, verbose_name = 'Teléfono' )
    correo = models.CharField( max_length = 200, default = None, null=True, blank=True, verbose_name = 'Correo Electronico' )
    ### Datos de Log ###
    registroActivo = models.BooleanField( default = True, verbose_name = 'Registro Activo' )
    registroFechaCreacion = models.DateTimeField( null=False, blank=False, auto_now_add=True, verbose_name = 'Fecha de Creación')
    registroFechaModificacion = models.DateTimeField( null=False, blank=False, auto_now=True, verbose_name = 'Fecha de Modificación')
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre  
