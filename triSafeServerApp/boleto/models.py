import json
import sys
import traceback
from datetime import date
from django.db import models
from rest_framework import status
from comum.retorno import Retorno
from gerencianet import Gerencianet

credentials = {
    'client_id': 'Client_Id_add8181cd3a52a8343ca8912c17bebf2acc579ae',
    'client_secret': 'Client_Secret_8c2e0c711440ccb2ca969115cb9322d697cf02da',
    'sandbox': True
}

class BoletoGerenciaNet(models.Model):
    
    def gerar(self, oContrato):
        try:
            t = TransacaoGerenciaNet()
            
            retorno = t.incluir()
            if not retorno.estado.ok:
                return retorno

            today = date.today()

            dataVencimento = today.strftime("%Y-%m-%d")
            
            gn = Gerencianet(credentials)
 
            params = {
                'id': retorno.dados['id']
            }
            
            body = {
                'payment': {
                    'banking_billet': {
                        'expire_at': dataVencimento,
                        'customer': {
                            'name': oContrato.cliente.nome,
                            'email': oContrato.cliente.email,
                            'cpf': oContrato.cliente.cpf,
                            # 'birth': oContrato.cliente.,
                            'phone_number': oContrato.cliente.telefone
                        }
                    }
                }
            }
            
            oBillet = gn.pay_charge(params=params, body=body)

            retorno = self.tratarRetornoGerenciaNet(oBillet)

            return retorno

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno

    def tratarRetornoGerenciaNet(self, oBillet):
        retorno = Retorno(True)
        oDados = None

        if oBillet:
            if 'error_description' in oBillet:
                oError = oBillet['error_description']
                msgErro = oError

                if 'message' in oError:
                    msgErro = oError['message']

                if(oError):
                    retorno = Retorno(False, msgErro, oBillet['error'])
                    return retorno
            elif 'data' in oBillet:
                oDadosBoleto = oBillet['data']
                if oDadosBoleto:
                    self.converterDeGerenciaNet(oDadosBoleto)
                    oDados = self.json()    
                else:
                    retorno = Retorno(False, 'Os dados de geração do boleto foram retornados vazios.')

        else:
            retorno = Retorno(False, 'O objeto retornado na geração do boleto está vazio.')
        
        retorno.dados = oDados

        return retorno

    def converterDeGerenciaNet(self, oDadosBoleto):
        if oDadosBoleto:
            if 'pdf' in oDadosBoleto:
                oPDF = oDadosBoleto['pdf']
                if oPDF:
                    self.url_pdf = oPDF['charge']
            if 'link' in oDadosBoleto:
                self.url_html = oDadosBoleto['link']
    
    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
            "url_boleto_pdf": self.url_pdf,
            "url_boleto_html": self.url_html,
            }
        return ret

    def __str__(self):
        return self.url_pdf

class TransacaoGerenciaNet(models.Model):
    
    def incluir(self):
        try:
            gn = Gerencianet(credentials)

            body = {
                'items': [{
                    'name': "Cliente 1",
                    'value': 1000,
                    'amount': 2
                }],
                'shippings': [{
                    'name': "Contrato de adesao",
                    'value': 100
                }]
            }
            
            oCharge = gn.create_charge(body=body)
            self.converterDeGerenciaNet(oCharge)

            retorno = Retorno(True)
            retorno.dados = self.json()

            return retorno

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
    
    def converterDeGerenciaNet(self, oCharge):
        if oCharge:
            oData = oCharge['data']
            self.id = oData['charge_id']
            self.dataCriacao = oData['created_at']
            self.estado = oData['status']
            self.total = oData['total']

    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
            "id": self.id,
            "data_criacao": self.dataCriacao,
            "estado": self.estado,
            "total": self.total
            }
        return ret

    def __str__(self):
        return self.id