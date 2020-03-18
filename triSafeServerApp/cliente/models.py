import json
import sys
import traceback
from django.db import models
from rest_framework import status
from clienteIter.models import ClienteIter
from comum.retorno import Retorno

class Cliente(models.Model):
    id_cliente_iter = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=70, null=False)
    nomeUsuario = models.CharField(max_length=20, blank=False, null=True)
    cpf = models.CharField(max_length=11, blank=False, null=True)
    rg = models.CharField(max_length=10, blank=False, null=True)
    rua = models.CharField(max_length=200, blank=False, null=True)
    numero = models.IntegerField()
    cep = models.CharField(max_length=11, blank=False, null=True)
    bairro = models.CharField(max_length=200, blank=False, null=True) 
    cidade = models.CharField(max_length=200, blank=False, null=True) 
    uf = models.CharField(max_length=11, blank=False, null=True)
    telefone = models.CharField(max_length=11, blank=False, null=True)
    email = models.EmailField()
    senha = models.CharField(max_length=20, blank=False, null=True)
    senhaConfirmacao = models.CharField(max_length=20, blank=False, null=True)
    dt_hr_inclusao = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    
    def obter(self):
        try:
            retorno = Cliente.validarDadosObrigatoriosChaves(self)
                
            if not retorno.estado.ok:
                return retorno

            retorno = Retorno(False, 'Cliente não cadastrado', 'NaoCadastrado', 406)
            
            # Valida se o cliente já está cadastrado.
            listaClientes = Cliente.objects.filter(cpf=self.cpf)
            if listaClientes:
                oCliente = listaClientes[0]
                if oCliente:
                    # Obtem o cadastro na Iter.
                    oRetornoClienteIter = ClienteIter.obter(self, oCliente.id_cliente_iter)
                    
                    if not oRetornoClienteIter.estado.ok:
                        return oRetornoClienteIter
                    
                    self.converterDeClienteIter(oRetornoClienteIter.dados)
                    retorno = Retorno(True)
                    retorno.dados = self.json()
            
            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno

    def obterUltimo(self):
        try:
            # Valida se o cliente já está cadastrado.
            listaClientes = Cliente.objects.filter()
            if listaClientes:
                oCliente = listaClientes[listaClientes.count()-1]
                if oCliente:
                    # Obtem o cadastro na Iter.
                    oRetornoClienteIter = ClienteIter.obter(self, oCliente.id_cliente_iter)
                    
                    if not oRetornoClienteIter.estado.ok:
                        return oRetornoClienteIter
                    
                    self.converterDeClienteIter(oRetornoClienteIter.dados)
                    retorno = Retorno(True)
                    retorno.dados = self.json()
            
            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
                
    def incluir(self):
        try:
            retorno = Cliente.validarDadosObrigatorios(self)
            
            if not retorno.estado.ok:
                return retorno

            # Valida se o cliente já está cadastrado.
            retorno = Cliente.obter(self)

            if retorno.estado.codMensagem != 'NaoCadastrado':
                return retorno
            
            # Inclusao na Iter.
            cIter = ClienteIter()
            retorno = cIter.incluir(self)
            
            if not retorno.estado.ok:
                return retorno

            oClienteIter = retorno.dados
            self.id_cliente_iter = oClienteIter['id']
        
            f = open("demofile2.txt", "a")
            f.write(str(oClienteIter))
            f.close()
            
            if not retorno.estado.ok:
                return retorno

            self.save()
            
            retorno = Retorno(True, 'Cadastro realizado com sucesso.', 200)
            retorno.dados = self.json()

            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.')
            return retorno
    
    def converterDeClienteIter(self, oClienteIter):
        if oClienteIter:
            self.id_cliente_iter = oClienteIter['id']
            self.nome = oClienteIter['name']
            # self.nomeUsuario = oClienteIter['username']
            self.cpf = oClienteIter['document']
            # self.rg = oClienteIter['']
            self.rua = oClienteIter['street']
            self.numero = oClienteIter['number']
            self.cep = oClienteIter['zipcode']
            self.bairro = oClienteIter['district']
            self.cidade = oClienteIter['city']
            self.uf = oClienteIter['state']
            self.telefone = oClienteIter['phone']
            self.email = oClienteIter['email']

    def validarDadosObrigatoriosChaves(self):
        if len(str(self.cpf).strip()) <= 0 and len(str(self.email).strip()) <= 0:
            return Retorno(False, "Informe o CPF e/ou E-Mail.", 406)

        return Retorno(True)
    
    def validarDadosObrigatorios(self):
        
        retorno = Cliente.validarDadosObrigatoriosChaves(self)
            
        if not retorno.estado.ok:
            return retorno

        if len(str(self.nome).strip()) <= 0:
            return Retorno(False, "Informe o nome.", 406)
        return Retorno(True)
    
    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
            "id_cliente_iter": self.id_cliente_iter,
            "nome": self.nome,
            "nomeUsuario": self.nomeUsuario,
            "cpf": self.cpf,
            "rg": self.rg,
            "rua": self.rua,
            "numero": self.numero,
            "cep": self.cep,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "telefone": self.telefone,
            "email": self.email,
            }
        return ret

    def __str__(self):
        return self.nome