import json
import sys
import traceback
from django.db import models
from rest_framework import status
from comum.retorno import Retorno

class Produto(models.Model):
    # Tipos de produtos
    FISICO = 'F'
    SERVICO = 'S'
    TIPOS_PRODUTO = [
        (FISICO, 'Produto Físico'),
        (SERVICO, 'Serviço'),
    ]

    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=70, null=False, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=1, null=False, choices=TIPOS_PRODUTO, default=FISICO)
    dt_hr_inclusao = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    
    def obter(self):
        try:
            retorno = Produto.validarDadosObrigatoriosChaves(self)
                
            if not retorno.estado.ok:
                return retorno

            retorno = Retorno(False, 'Produto não cadastrado', 'NaoCadastrado', 406)
            
            # Valida se o cliente já está cadastrado.
            listaProdutos = Produto.objects.filter(nome=self.nome)
            if listaProdutos:
                oProduto = listaProdutos[0]
                if oProduto:
                    retorno = Retorno(True)
                    retorno.dados = oProduto.json()
            
            return retorno

        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
    
    def listar(self):
        try:
            retorno = Retorno(False, 'Nenhum Produto TriSafe está cadastrado.', 'NaoCadastrado', 406)

            # Lista os produtos cadastrados.
            listaProdutos = Produto.objects.all()
            if listaProdutos:
                listaProdutosJson = []
                for oProduto in listaProdutos:
                    listaProdutosJson.append(oProduto)

                retorno = Retorno(True)
                retorno.dados = listaProdutos
                
            return retorno
            
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno

    def incluir(self):
        try:
            retorno = Produto.validarDadosObrigatorios(self)
            
            if not retorno.estado.ok:
                return retorno

            # Valida se o produto já está cadastrado.
            retorno = Produto.obter(self)

            if retorno.estado.codMensagem != 'NaoCadastrado':
                return retorno

            self.save()
            
            retorno = Retorno(True, 'Cadastro realizado com sucesso.', 200)
            retorno.dados = self.json()

            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
    
    def validarDadosObrigatoriosChaves(self):
        if self.codigo <= 0 or len(str(self.nome).strip()) <= 0 :
            return Retorno(False, "Informe o código ou o nome completo do produto.", 406)

        return Retorno(True)
    
    def validarDadosObrigatorios(self):
        
        retorno = Produto.validarDadosObrigatoriosChaves(self)
        
        if not retorno.estado.ok:
            return retorno

        if self.valor <= 0:
            return Retorno(False, "Informe o valor do produto.", 406)

        return Retorno(True)
    
    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
                "codigo": self.codigo,
                "nome": self.nome,
                "valor": self.valor,
                "tipo": self.tipo,
                "dt_hr_inclusao": self.dt_hr_inclusao,
            }
        return ret

    def __str__(self):
        return self.nome