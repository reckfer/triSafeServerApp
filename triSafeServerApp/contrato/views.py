from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from .models import Contrato
from rest_framework.renderers import JSONRenderer
from comum.retorno import Retorno
import json
import traceback
import sys

class ContratoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contrato
        fields = ()

# ViewSets define the view behavior.
class ContratoViewSet(viewsets.ModelViewSet, permissions.BasePermission):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    
    @action(detail=False, methods=['post'])
    def efetivar(self, request):
        try:
            oContrato = ContratoViewSet.apropriarDadosHTTP(request)
            retorno = oContrato.efetivar()
            
            return Response(retorno.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @classmethod
    def apropriarDadosHTTPChave(cls, request):
        oContrato = Contrato()
        # oContrato.cpf = request.data['codigo']

        return oContrato

    @classmethod
    def apropriarDadosHTTP(cls, request):
        oContrato = ContratoViewSet.apropriarDadosHTTPChave(request)
        
        dadosContrato = request.data['contrato']

        oContrato.valorTotal = dadosContrato['valorTotal']
                
        return oContrato