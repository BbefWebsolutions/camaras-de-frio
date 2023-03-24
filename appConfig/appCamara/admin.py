from django.contrib import admin
from appCamara.models import Camara, Cotizacion, TipoCamara, TipoPago, ValorTransporte
# Register your models here.

admin.site.register(TipoCamara)
admin.site.register(TipoPago)
admin.site.register(Camara)
admin.site.register(Cotizacion)
admin.site.register(ValorTransporte)
