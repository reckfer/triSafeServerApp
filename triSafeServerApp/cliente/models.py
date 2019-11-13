from django.db import models
from clienteIter.models import ClienteIter

class Cliente(models.Model):
    nome = models.CharField(max_length=70, null=False)
    #cpf = models.OneToOneField(CPF, on_delete=models.CASCADE, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=False, null=False)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    idade = models.IntegerField()
    email = models.EmailField()

    def obter(self, idCliente):
        
        return ClienteIter.obter(self, idCliente)
    
    def incluir(self, nomeCliente, email, nomeUsuario):
        
        return ClienteIter.incluir(self, nomeCliente, email, nomeUsuario)

    def __str__(self):
        return self.nome