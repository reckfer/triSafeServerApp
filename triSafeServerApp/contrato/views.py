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
# from boleto.models import TransacaoGerenciaNet
from boleto.models import BoletoGerenciaNet
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
    def incluir(self, request):
        try:
            m_contrato = ContratoViewSet.apropriar_dados_http(request)
            
            lista_produtos = ContratoViewSet.extrair_produtos_dados_http(request)
            retorno = m_contrato.incluir(lista_produtos)

            if not retorno.estado.ok:
                return retorno

            # m_boleto = BoletoGerenciaNet()
            # retorno = m_boleto.gerar(m_contrato)
            
            return Response(retorno.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @action(detail=False, methods=['post'])
    def aceitar(self, request):
        try:
            m_contrato = ContratoViewSet.apropriar_dados_http(request)
            
            retorno = m_contrato.aceitar()

            if not retorno.estado.ok:
                return retorno

            # m_boleto = BoletoGerenciaNet()
            # retorno = m_boleto.gerar(m_contrato)
            
            return Response(retorno.json())
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return Response(retorno.json())
    
    @classmethod
    def apropriar_dados_http(cls, request):
        m_contrato = Contrato()
        m_contrato.cliente = ContratoViewSet.extrair_cliente_dados_http(request)
        
        d_dados_app = request.data['dados_app']
        m_contrato.id_contrato = d_dados_app['id_contrato']

        return m_contrato

    @classmethod
    def extrair_cliente_dados_http(cls, request):
        m_cliente = Cliente()

        d_dados_app = request.data['dados_app']

        d_cliente = d_dados_app['cliente']        
        m_cliente.cpf = d_cliente['cpf']

        return m_cliente

    @classmethod
    def extrair_produtos_dados_http(cls, request):
   
        d_dados_app = request.data['dados_app']
        d_contrato = d_dados_app['contrato']
        d_produtos_contratados = d_contrato['produtos_contratados']
                    
        return d_produtos_contratados