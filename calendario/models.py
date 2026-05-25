from django.db import models

class CalendarioVacinal(models.Model):
    # Relacionamento com a classe Vacina (do app vacinas)
    vacina = models.ForeignKey(
        'vacinas.Vacina', on_delete=models.CASCADE, related_name='calendarios'
    )
    idade_minima_meses = models.IntegerField()
    idade_maxima_meses = models.IntegerField(null=True, blank=True)
    publico_alvo = models.CharField(max_length=200)
    dose_recomendada = models.CharField(max_length=50)
    obrigatoria = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.vacina} - {self.dose_recomendada}'
# Create your models here.
