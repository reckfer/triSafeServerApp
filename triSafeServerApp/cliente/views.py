from django.shortcuts import render
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
        fields = ('nome', 'endereco')

# ViewSets define the view behavior.
class ClienteViewSet(viewsets.ModelViewSet, permissions.BasePermission):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    @action(detail=False, methods=['post'])
    def obter(self, request):
        try:
            c = Cliente()
            c.cpf = request.data['cpf']
            c.email = request.data['email']
            c.nomeUsuario = request.data['nomeUsuario']
            
            #c = Cliente.obter(self, request.query_params['idCliente'])
            cIter = c.obter()
            print (cIter)
            return Response(cIter.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
            # retorno = Retorno(False, str(e), 500)
            # return Response(retorno.json(), retorno.http_status)

    @action(detail=False, methods=['post'])
    def incluir(self, request):
        try:
            c = Cliente()
            #c.id_cliente_iter = 1
            c.cpf = request.data['cpf']
            c.rg = request.data['rg']
            c.nome = request.data['nomeCliente']
            c.email = request.data['email']
            c.nomeUsuario = request.data['nomeUsuario']
            
            retorno = c.incluir()
            
            if not retorno.ok:
                return Response(retorno.json())

            return Response(retorno.json(), retorno.http_status)

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
            # retorno = Retorno(False, str(e), 500)
            # return Response(retorno.json(), retorno.http_status)

    @action(detail=False)
    def recent_users(self, request):
        
        #json = JSONRenderer().render()
        return Response({"a": "abc"})
        #return Response(json.dumps({"a": "b"}))