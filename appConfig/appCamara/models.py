from django.db import models

# Create your models here.

class Camara(models.Model):
    nombre = models.CharField( null = True, blank = True, max_length=100, default = None, verbose_name = 'Nombre')
    descripcion = models.CharField(max_length=255, null = True, blank = True, default = None, verbose_name = 'Descripcion')
    m2 = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True, default = None, verbose_name = 'Metros Cuadrados')
    m3 = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True, default = None, verbose_name = 'Metros Cubicos')
    uf = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True, default = None, verbose_name = 'UF')
    valorNeto = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True, default = None, verbose_name = 'Valor Neto')
    valorIva = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True, default = None, verbose_name = 'Valor IVA')
    guia = models.FileField(upload_to ='guias/camaras/', null = True, blank = True, default = None)
    ### Datos de Log ###
    registroActivo = models.BooleanField( default = True, verbose_name = 'Registro Activo' )
    registroFechaCreacion = models.DateTimeField( null=False, blank=False, auto_now_add=True, verbose_name = 'Fecha de Creación')
    registroFechaModificacion = models.DateTimeField( null=False, blank=False, auto_now=True, verbose_name = 'Fecha de Modificación')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Camara'
        verbose_name_plural = 'Camaras'

    def __str__(self):
        return self.nombre