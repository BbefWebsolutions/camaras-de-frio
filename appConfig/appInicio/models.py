from django.db import models

# Create your models here.

class Region( models.Model ):
    ### Atributos del Modelo ###
    #https://en.wikipedia.org/wiki/ISO_3166-2:CL
    codigo_iso = models.CharField( max_length = 5, verbose_name = 'Código ISO 3166-2' )
    nombre = models.CharField( max_length = 100, verbose_name = 'Nombre de Región')
    km = models.IntegerField(null=True, blank=True, default=None, verbose_name='Kilometro')
    ### Datos de Log ###
    registroActivo = models.BooleanField( default = True, verbose_name = 'Registro Activo' )
    registroFechaCreacion = models.DateTimeField( null=False, blank=False, auto_now_add=True, verbose_name = 'Fecha de Creación')
    registroFechaModificacion = models.DateTimeField( null=False, blank=False, auto_now=True, verbose_name = 'Fecha de Modificación')
    class Meta:
        ordering = ['id']
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'

    def __str__(self):
        return self.nombre   

class Provincia( models.Model ):
    ### Atributos del Modelo ###
    nombre = models.CharField( max_length = 100, verbose_name='Nombre de Provincia' )
    region = models.ForeignKey( Region, on_delete=models.CASCADE, verbose_name='Región' )    
    ### Datos de Log ###
    registroActivo = models.BooleanField( default = True, verbose_name = 'Registro Activo' )
    registroFechaCreacion = models.DateTimeField( null=False, blank=False, auto_now_add=True, verbose_name = 'Fecha de Creación')
    registroFechaModificacion = models.DateTimeField( null=False, blank=False, auto_now=True, verbose_name = 'Fecha de Modificación')
    class Meta:
        ordering = ['id']
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return self.nombre    

class Comuna ( models.Model ):
    ### Atributos del Modelo ###
    nombre = models.CharField( max_length = 100, verbose_name = 'Nombre de Comuna' )
    cut = models.PositiveSmallIntegerField( unique=True, verbose_name = 'Código Único Territorial' )
    provincia = models.ForeignKey( Provincia, on_delete = models.CASCADE, verbose_name = 'Provincia' )
    area = models.DecimalField( verbose_name = 'Área (km2)', max_digits = 9, decimal_places = 2 )
    poblacion = models.PositiveIntegerField( verbose_name = 'Población (2017)' )
    latitud = models.FloatField(verbose_name = 'Latitud' )
    longitud = models.FloatField( verbose_name = 'Longitud' )
    ### Datos de Log ###
    registroActivo = models.BooleanField( default = True, verbose_name = 'Registro Activo' )
    registroFechaCreacion = models.DateTimeField( null=False, blank=False, auto_now_add=True, verbose_name = 'Fecha de Creación')
    registroFechaModificacion = models.DateTimeField( null=False, blank=False, auto_now=True, verbose_name = 'Fecha de Modificación')
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'

    def __str__(self):
        return self.nombre  
