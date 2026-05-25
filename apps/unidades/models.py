from django.db import models

class UnidadeSaude(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300)
    bairro = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    horario_funcionamento = models.CharField(max_length=100)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome