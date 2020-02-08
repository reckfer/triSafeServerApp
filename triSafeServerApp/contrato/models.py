import json
import sys
import traceback
from django.db import models
from rest_framework import status
from comum.retorno import Retorno
from cliente.models import Cliente
from produto.models import Produto
from boleto.models import BoletoGerenciaNet

class Contrato(models.Model):
    # Tipos de produtos
    FISICO = 'F'
    SERVICO = 'S'
    TIPOS_PRODUTO = [
        (FISICO, 'Contrato Físico'),
        (SERVICO, 'Serviço'),
    ]

    id_cliente_iter = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = None
    contrato = None

    def efetivar(self):
        try:
            # retornoCliente = self.cliente.obter()

            # if not retornoCliente.estado.ok:
            #     return retornoCliente
            clienteTmp = Cliente()
            clienteTmp.nome = "Fernando teste"
            clienteTmp.cpf = "82951128053"
            clienteTmp.email = "nandorex@gmail.com"
            clienteTmp.telefone = "51999454554"

            oContrato = Contrato()
            oContrato.cliente = clienteTmp

            # oContrato.produto = self
            oContrato.valorTotal = 243.00

            oBoleto = BoletoGerenciaNet()
            retornoBoleto = oBoleto.gerar(oContrato)
            
            if not retornoBoleto.estado.ok:
                return retornoBoleto

            # retorno = Retorno(True, 'Cadastro realizado com sucesso.', 200)
            # retorno.dados = retornoBoleto.json()

            return retornoBoleto
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
    
    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
            "nome": self.cliente.nome,
            }
        return ret

    def __str__(self):
        return self.cliente.nome