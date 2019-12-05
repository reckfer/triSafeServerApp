import json
import sys
import traceback
from django.db import models
from rest_framework import status
from clienteIter.models import ClienteIter
from comum.retorno import Retorno

class Cliente(models.Model):
    id_cliente_iter = models.IntegerField()
    nome = models.CharField(max_length=70, null=False)
    nomeUsuario = models.CharField(max_length=20, blank=False, null=True)
    cpf = models.CharField(max_length=11, blank=False, null=True)
    rg = models.CharField(max_length=10, blank=False, null=True)
    endereco = models.CharField(max_length=200, blank=False, null=True)
    cep = models.CharField(max_length=11, blank=False, null=True)
    bairro = models.CharField(max_length=200, blank=False, null=True) 
    cidade = models.CharField(max_length=200, blank=False, null=True) 
    estado = models.CharField(max_length=11, blank=False, null=True)
    dt_hr_inclusao = models.DateTimeField(blank=False, null=True)
    telefone = models.CharField(max_length=11, blank=False, null=True)
    email = models.EmailField()

    def obter(self):
        
        retorno = Cliente.validarDadosObrigatorios(self)
            
        if not retorno.ok:
            return retorno

        # Valida se o cliente já está cadastrado.
        listaClientes = Cliente.objects.filter(cpf=self.cpf)
        if listaClientes:
            cliente = listaClientes[0]
            if cliente:
                return ClienteIter.obter(self, cliente.id_cliente_iter)
            else:
                return Retorno(False, 'Cliente não cadastrado.', 406)        
    
    def incluir(self):
        try:
            retorno = Cliente.validarDadosObrigatorios(self)
            
            if not retorno.ok:
                return retorno

            # Valida se o cliente já está cadastrado.
            listaClientes = Cliente.objects.filter(cpf=self.cpf)
            if listaClientes:
                cliente = listaClientes[0]
                if cliente:
                    return Retorno(False, 'Cliente já cadastrado.', 406)

            # Inclusao na Iter.
            cIter = ClienteIter()
            retorno = cIter.incluir(self)
            
            print(str(retorno))
            
            self.id_cliente_iter = retorno.dadosJson['user']['id']
            dadosCliente = retorno.dadosJson

            f = open("demofile2.txt", "a")
            f.write(str(dadosCliente))
            f.close()
            
            if not retorno.ok:
                return retorno

            self.save()
            retorno = Retorno(True, 'Cadastro realizado com sucesso.', '')
            retorno.dadosJson = dadosCliente

            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return retorno

    def __str__(self):
        return self.nome

    def validarDadosObrigatorios(self):
        if len(str(self.cpf)) <= 0:
            return Retorno(False, "Informe o CPF.", 406)

        # if len(str(self.nome)) <= 0:
        #     return Retorno(False, "Informe o nome.", 406)
        
        return Retorno(True, '', '')