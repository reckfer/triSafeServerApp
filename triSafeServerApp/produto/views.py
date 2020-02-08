from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from .models import Produto
from cliente.models import Cliente
from rest_framework.renderers import JSONRenderer
from comum.retorno import Retorno
import json
import traceback
import sys

class ProdutoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Produto
        fields = ('codigo', 'nome')

# ViewSets define the view behavior.
class ProdutoViewSet(viewsets.ModelViewSet, permissions.BasePermission):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    @action(detail=False, methods=['post'])
    def listar(self, request):
        try:
            p = Produto()
            
            retornoProdutos = p.listar()
            return Response(retornoProdutos.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @classmethod
    def apropriarDadosHTTPChave(cls, request):
        oProduto = Produto()
        oProduto.cpf = request.data['codigo']

        return oProduto

    @classmethod
    def apropriarDadosHTTP(cls, request):
        oProduto = ProdutoViewSet.apropriarDadosHTTPChave(request)
        
        oProduto.nome = request.data['nome']
        oProduto.tipo = request.data['tipo']
        oProduto.valor = request.data['valor']
        # listaProdutos = request.data['produtos']

        oCliente = Cliente()
        oCliente.cpf = request.data['cpf']
        oProduto.cliente = oCliente
                
        return oProduto