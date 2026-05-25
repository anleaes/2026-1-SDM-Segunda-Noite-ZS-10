from django.db import models
# Create your models here.
STATUS_CHOICES = [
    ('agendado', 'Agendado'),
    ('realizado', 'Realizado'),
    ('cancelado', 'Cancelado'),
]

class Atendimento(models.Model):
    paciente = models.ForeignKey(
        'pessoas.Paciente', on_delete=models.CASCADE, related_name='atendimentos'
    )
    unidade_saude = models.ForeignKey('unidades.UnidadeSaude', on_delete=models.CASCADE)
    profissional = models.ForeignKey(
        'pessoas.ProfissionalSaude', on_delete=models.SET_NULL, null=True
    )
    data_atendimento = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'Atendimento {self.id} - {self.paciente}'


class DoseAtendimento(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, related_name='doses')
    vacina = models.ForeignKey('vacinas.Vacina', on_delete=models.CASCADE)
    lote = models.ForeignKey('vacinas.LoteVacina', on_delete=models.CASCADE)
    ordem_dose = models.CharField(max_length=20)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'Dose {self.ordem_dose} - {self.vacina}'