from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from .models import Cliente
from rest_framework.renderers import JSONRenderer
from comum.retorno import Retorno
import json
import traceback
import sys

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ('cpf', 'email', 'nome', 'endereco')

# ViewSets define the view behavior.
class ClienteViewSet(viewsets.ModelViewSet, permissions.BasePermission):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    @action(detail=False, methods=['post'])
    def obter(self, request):
        try:
            c = ClienteViewSet.apropriarDadosHTTPChave(request)
            
            #c = Cliente.obter(self, request.query_params['idCliente'])

            retornoCliente = c.obter()
            return Response(retornoCliente.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())

    @action(detail=False, methods=['post'])
    def incluir(self, request):
        try:
            c = ClienteViewSet.apropriarDadosHTTP(request)
            
            retorno = c.incluir()
            
            if not retorno.ok:
                return Response(retorno.json())

            return Response(retorno.json())

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())

    @classmethod
    def apropriarDadosHTTPChave(cls, request):
        c = Cliente()
        c.cpf = request.data['cpf']
        c.email = request.data['email']

        return c

    @classmethod
    def apropriarDadosHTTP(cls, request):
        c = ClienteViewSet.apropriarDadosHTTPChave(request)
        
        c.rg = request.data['rg']
        c.nome = request.data['nomeCliente']
        c.nomeUsuario = request.data['nomeUsuario']
        c.rua = request.data['rua']
        c.telefone = request.data['telefone']
        c.numero = request.data['numero']
        c.bairro = request.data['bairro']
        c.cidade = request.data['cidade']
        c.cep = request.data['cep']
        c.uf = request.data['uf']

        return c