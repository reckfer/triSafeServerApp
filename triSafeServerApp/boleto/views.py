from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from .models import BoletoGerenciaNet
from rest_framework.renderers import JSONRenderer
from comum.retorno import Retorno
import json
import traceback
import sys

class BoletoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BoletoGerenciaNet
        fields = ('charge_id')

# ViewSets define the view behavior.
class BoletoViewSet(viewsets.ModelViewSet, permissions.BasePermission):
    queryset = BoletoGerenciaNet.objects.all()
    serializer_class = BoletoSerializer
    
    @action(detail=False, methods=['post'])
    def gerarBoleto(self, request):
        try:
            b = BoletoGerenciaNet()
            
            retornoBoleto = b.gerar()
            return Response(retornoBoleto.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @classmethod
    def apropriarDadosHTTPChave(cls, request):
        c = BoletoGerenciaNet()
        c.cpf = request.data['cpf']
        c.email = request.data['email']

        return c

    @classmethod
    def apropriarDadosHTTP(cls, request):
        c = BoletoViewSet.apropriarDadosHTTPChave(request)
        
        c.rg = request.data['cpf']
        c.nome = request.data['nome']
        c.nomeUsuario = request.data['nomeUsuario']
        
        return c