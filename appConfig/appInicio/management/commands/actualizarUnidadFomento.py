from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from datetime import datetime
from decimal import Decimal
from pprint import pprint
import requests
import xmltodict, json

from appFinanzas.models import UnidadFomento
from appGeneral.library import obtenerPrimerDiaMes, obtenerUltimoDiaMes


class Command(BaseCommand):
    help = 'Creación de datos iniciales para el levantamiento del sistema'

    def handle(self, *args, **options):
        URL = 'https://api.cmfchile.cl/api-sbifv3/recursos_api/'
        API_KEY = '1b126ceb04faf2c13554da972f18d6f56dfb68c4'
        _anno = 2015
        while _anno <= datetime.now().year:
            _url = URL + 'uf/'+ str(_anno) +'?formato=xml&apikey=' + API_KEY
            _response = requests.get(_url)
            _data = xmltodict.parse(_response.content)
            _data = json.loads(json.dumps(_data))

            for _item in _data['IndicadoresFinancieros']['UFs']['UF']:        
                try: 
                    _fecha = datetime.strptime(_item['Fecha'], '%Y-%m-%d').date() 
                    _valor = Decimal(str(_item['Valor']).replace('.','').replace(',','.'))
                    try:
                        _uf = UnidadFomento.objects.get(periodo = _fecha, valor = _valor)
                    except UnidadFomento.DoesNotExist:
                        _uf = UnidadFomento.objects.create(periodo = _fecha, valor = _valor)
                except Exception as e:
                    print(e)
            _anno += 1
        print('Actualización de UF finalizado...')