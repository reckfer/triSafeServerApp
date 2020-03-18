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
    # Tipos de produtos
    FISICO = 'F'
    SERVICO = 'S'
    TIPOS_PRODUTO = [
        (FISICO, 'Contrato Físico'),
        (SERVICO, 'Serviço'),
    ]

    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    produto = models.ManyToManyField(Produto)
    chavesProdutos = None
    
    def efetivar(self):
        try:
            retornoCliente = self.cliente.obter()

            if not retornoCliente.estado.ok:
                return retornoCliente

            # clienteTmp = Cliente()
            # clienteTmp.nome = "Fernando teste"
            # clienteTmp.cpf = "82951128053"
            # clienteTmp.email = "nandorex@gmail.com"
            # clienteTmp.telefone = "51999454554"

            oContrato = Contrato()
            oContrato.cliente = retornoCliente

            oContrato.produto = self
            oContrato.valorTotal = 243.00

            oBoleto = BoletoGerenciaNet()
            retornoBoleto = oBoleto.gerar(oContrato)
            
            if not retornoBoleto.estado.ok:
                return retornoBoleto

            return retornoBoleto

            retorno = Retorno(True)
            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
    
    @classmethod
    def associarProdutos(cls):
        for produto in Contrato.chavesProdutos:
            oProduto = Produto()
            oProduto.codigo = produto['codigo']
            oProduto.nome = produto['nome']
            oContrato.produto.add(oProduto)
    
    def gerarContratoPDF(self):
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Welcome to Py", ln=1, align="C")
        pdf.output("simple_demo.pdf")
    
    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
            "nome": self.cliente.nome
            }
        return ret

    def __str__(self):
        return self.cliente.nome