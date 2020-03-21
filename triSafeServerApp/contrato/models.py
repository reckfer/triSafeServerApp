import json
import sys
import traceback
from django.db import models
from rest_framework import status
from comum.retorno import Retorno
from cliente.models import Cliente
from produto.models import Produto
from boleto.models import BoletoGerenciaNet
from fpdf import FPDF

class Contrato(models.Model):
    id_contrato = models.CharField(primary_key=True, max_length=16)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    produtos_contratados = models.ManyToManyField(Produto)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Tipos de produtos
    FISICO = 'F'
    SERVICO = 'S'
    TIPOS_PRODUTO = [
        (FISICO, 'Contrato Físico'),
        (SERVICO, 'Serviço'),
    ]
    
    def incluir(self):
        try:

            retorno_cliente = self.cliente.obter()

            if not retorno_cliente.estado.ok:
                return retorno_cliente

            id_contrato = str(self.cliente.id_cliente_iter).rjust(6, '0') + '456' #str(retornoTransacao.dadosJson['id']).rjust(10, '0')
            
            self.id_contrato = id_contrato
            self.cliente = retorno_cliente.dados
            self.save()

            # self.associarProdutos()
            
            # oBoleto = BoletoGerenciaNet()
            # retorno_boleto = oBoleto.gerar(m_contrato)
            
            # if not retorno_boleto.estado.ok:
            #     return retorno_boleto

            # return retorno_boleto

            retorno = Retorno(True, 'Seu contrato foi gerado e será efetivado após o pagamento do boleto.')
            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno

    def atualizarProdutos(self, chaves_produtos):
        produtos = list()

        for chave_produto in chaves_produtos:
            
            lista_produtos = Produto.objects.filter(codigo = chave_produto['codigo'])
            if lista_produtos:
                m_produto = lista_produtos[0]
                if m_produto:
                    produtos.append(m_produto)

        self.produtos_contratados.add(*produtos)        

    def gerarContratoPDF(self):
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Welcome to Py", ln=1, align="C")
        pdf.output("simple_demo.pdf")
    
    def json(self):
        return self.__criar_json__()

    def __criar_json__(self):
        ret = {
            "nome": self.cliente.nome
            }
        return ret

    def __str__(self):
        return self.cliente.nome