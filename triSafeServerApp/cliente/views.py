from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from cliente.models import Cliente
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

            retornoCliente = c.obter()
            return Response(retornoCliente.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @action(detail=False, methods=['post'])
    def obterUltimo(self, request):
        try:
            c = Cliente()
            retornoCliente = c.obterUltimo()
            
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

            return Response(retorno.json())

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())

    @classmethod
    def apropriarDadosHTTPChave(cls, request):
        c = Cliente()
        
        cliente = request.data['cliente']
        c.cpf = cliente['cpf']
        c.email = cliente['email']

        return c

    @classmethod
    def apropriarDadosHTTP(cls, request):
        c = ClienteViewSet.apropriarDadosHTTPChave(request)
        
        cliente = request.data['cliente']
        c.rg = cliente['rg']
        c.nome = cliente['nome']
        c.nomeUsuario = cliente['nomeUsuario']
        c.rua = cliente['rua']
        c.telefone = cliente['telefone']
        c.numero = cliente['numero']
        c.bairro = cliente['bairro']
        c.cidade = cliente['cidade']
        c.cep = cliente['cep']
        c.uf = cliente['uf']

        return c