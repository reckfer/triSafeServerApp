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
    contrato_id = models.CharField(primary_key=True, max_length=16)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    produto = models.ManyToManyField(Produto)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Tipos de produtos
    FISICO = 'F'
    SERVICO = 'S'
    TIPOS_PRODUTO = [
        (FISICO, 'Contrato Físico'),
        (SERVICO, 'Serviço'),
    ]
    
    def efetivar(self):
        try:
            retornoCliente = self.cliente.obter()

            if not retornoCliente.estado.ok:
                return retornoCliente

            # oContrato = Contrato()
            self.cliente = retornoCliente.dados
            self.save()

            # self.associarProdutos()
            
            # oBoleto = BoletoGerenciaNet()
            # retornoBoleto = oBoleto.gerar(oContrato)
            
            # if not retornoBoleto.estado.ok:
            #     return retornoBoleto

            # return retornoBoleto

            retorno = Retorno(True)
            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno

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