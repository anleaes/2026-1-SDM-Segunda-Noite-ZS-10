from django.db import models

class CampanhaVacinacao(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    publico_alvo = models.CharField(max_length=200)
    ativa = models.BooleanField(default=True)

    vacinas = models.ManyToManyField(
        'vacinas.Vacina',
        related_name='campanhas',
        blank=True
    )

    def __str__(self):
        return self.nome