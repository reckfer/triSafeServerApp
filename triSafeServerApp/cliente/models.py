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
        
        retorno = Cliente.validarDadosObrigatoriosChaves(self)
            
        if not retorno.ok:
            return retorno

        # Valida se o cliente já está cadastrado.
        listaClientes = Cliente.objects.filter(cpf=self.cpf)
        if listaClientes:
            cliente = listaClientes[0]
            if cliente:
                return ClienteIter.obter(self, cliente.id_cliente_iter)
            
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
            
            if not retorno.ok:
                return retorno

            oClienteIter = retorno.dados
            self.id_cliente_iter = oClienteIter['id']
        
            f = open("demofile2.txt", "a")
            f.write(str(oClienteIter))
            f.close()
            
            if not retorno.ok:
                return retorno

            self.save()
            
            retorno = Retorno(True, 'Cadastro realizado com sucesso.', 200)
            retorno.dados = oClienteIter

            return retorno
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
                    
            retorno = Retorno(False, 'Falha de comunicação. Em breve será normalizado.', '')
            return retorno

    def __str__(self):
        return self.nome

    def validarDadosObrigatoriosChaves(self):
        if len(str(self.cpf).strip()) <= 0:
            return Retorno(False, "Informe o CPF.", 406)

        if len(str(self.email).strip()) <= 0:
            return Retorno(False, "Informe o e-mail.", 406)
        
        return Retorno(True, '', '')
    
    def validarDadosObrigatorios(self):
        
        retorno = Cliente.validarDadosObrigatoriosChaves(self)
            
        if not retorno.ok:
            return retorno

        if len(str(self.nome).strip()) <= 0:
            return Retorno(False, "Informe o nome.", 406)

        if len(str(self.rg).strip()) <= 0:
            return Retorno(False, "Informe o RG.", 406)
        
        return Retorno(True, '', '')