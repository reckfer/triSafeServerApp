from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from contrato.models import Contrato
from produto.models import Produto
from cliente.models import Cliente
from rest_framework.renderers import JSONRenderer
from comum.retorno import Retorno
from boleto.models import TransacaoGerenciaNet
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
           
            transacaoGerenciaNet = TransacaoGerenciaNet()
                
            retornoTransacao = transacaoGerenciaNet.incluir()
            if not retornoTransacao.estado.ok:
                return retornoTransacao

            idContrato = str(oContrato.cliente.id_cliente_iter).rjust(6, '0') + str(retornoTransacao.dados['id']).rjust(10, '0')
            
            oContrato.contrato_id = idContrato
            oContrato.save()

            produtos = ContratoViewSet.extrairProdutosDadosHTTP(request)
            oContrato.produto.add(produtos)
            
            return Response(Retorno(True))
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @classmethod
    def apropriarDadosHTTP(cls, request):
        oContrato = Contrato()
        oContrato.cliente = ContratoViewSet.extrairClienteDadosHTTP(request)
                        
        return oContrato

    @classmethod
    def extrairClienteDadosHTTP(cls, request):
        oCliente = None
        cliente = request.data['cliente']
        listaClientes = Cliente.objects.filter(cpf=cliente['cpf'])
        
        if listaClientes:
            oCliente = listaClientes[0]

        return oCliente

    @classmethod
    def extrairProdutosDadosHTTP(cls, request):
        dadosContrato = request.data['contrato']
        chavesProdutos = dadosContrato['listaProdutos']
        produtos = []

        for produto in chavesProdutos:
            listaProdutos = Produto.objects.filter(codigo = produto['codigo'])
            # produtoLista = Produto.objects.filter(codigo=produto['codigo'])
            if listaProdutos:
                oProduto = listaProdutos[0]
                if oProduto:
                    produtos.append(oProduto)
                    
        return produtos