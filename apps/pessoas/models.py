from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Paciente(Pessoa):
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome} - {self.cpf}'


class ProfissionalSaude(Pessoa):
    unidade_saude = models.ForeignKey(
        'unidades.UnidadeSaude',
        on_delete=models.SET_NULL,
        null=True,
        related_name='profissionais'
    )
    registro_profissional = models.CharField(max_length=50)
    cargo = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome} - {self.cargo}'