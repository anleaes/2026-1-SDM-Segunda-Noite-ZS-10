from django.db import models

class Vacina(models.Model):
    nome = models.CharField(max_length=200)
    fabricante = models.CharField(max_length=200)
    doenca_prevenida = models.CharField(max_length=200)
    quantidade_doses = models.IntegerField()
    intervalo_dias = models.IntegerField(default=0)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class LoteVacina(models.Model):
    vacina = models.ForeignKey(
        Vacina,
        on_delete=models.CASCADE,
        related_name='lotes'
    )
    unidade_saude = models.ForeignKey(
        'unidades.UnidadeSaude',
        on_delete=models.CASCADE,
        related_name='lotes'
    )
    numero_lote = models.CharField(max_length=50)
    data_validade = models.DateField()
    quantidade_disponivel = models.IntegerField()

    def __str__(self):
        return f'{self.numero_lote} - {self.vacina}'