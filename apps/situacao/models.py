from django.db import models

STATUS_VACINAL = [
    ('em_dia', 'Em Dia'),
    ('pendente', 'Pendente'),
    ('atrasado', 'Atrasado'),
]

class SituacaoVacinal(models.Model):

    paciente = models.ForeignKey(
        'pessoas.Paciente',
        on_delete=models.CASCADE
    )

    vacina = models.ForeignKey(
        'vacinas.Vacina',
        on_delete=models.CASCADE
    )

    calendario_vacinal = models.ForeignKey(
        'calendario.CalendarioVacinal',
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_VACINAL
    )

    data_verificacao = models.DateTimeField(
        auto_now=True
    )

    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.paciente} - {self.vacina} - {self.status}'