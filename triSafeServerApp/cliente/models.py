import json
from django.db import models
from rest_framework import status
from clienteIter.models import ClienteIter
from comum.retorno import Retorno

class Cliente(models.Model):
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

    def obter(self, idCliente):
        
        return ClienteIter.obter(self, idCliente)
    
    def incluir(self):
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

        self.save()
        retorno = Retorno(True, '', '')
        return retorno

    def __str__(self):
        return self.nome

    def validarDadosObrigatorios(self):
        if len(str(self.cpf)) <= 0:
            return Retorno(False, "Informe o CPF.", 406)

        if len(str(self.nome)) <= 0:
            return Retorno(False, "Informe o nome.", 406)
        
        return Retorno(True, '', '')