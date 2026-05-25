from django.db import models
# Create your models here.
class RegistroVacinacao(models.Model):
    paciente = models.ForeignKey('pessoas.Paciente', on_delete=models.CASCADE)
    vacina = models.ForeignKey('vacinas.Vacina', on_delete=models.CASCADE)
    lote = models.ForeignKey('vacinas.LoteVacina', on_delete=models.CASCADE)
    profissional = models.ForeignKey(
        'pessoas.ProfissionalSaude', on_delete=models.SET_NULL, null=True
    )
    unidade_saude = models.ForeignKey('unidades.UnidadeSaude', on_delete=models.CASCADE)
    atendimento = models.ForeignKey('atendimentos.Atendimento', on_delete=models.CASCADE)
    
    data_aplicacao = models.DateField()
    dose = models.CharField(max_length=20)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.paciente} - {self.vacina} - {self.dose}'