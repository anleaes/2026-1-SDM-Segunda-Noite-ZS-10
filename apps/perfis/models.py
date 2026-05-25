from django.db import models

class PerfilSaude(models.Model):
    paciente = models.OneToOneField(
        'pessoas.Paciente',
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    grupo_risco = models.BooleanField(default=False)
    gestante = models.BooleanField(default=False)
    alergias = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f'Perfil de {self.paciente}'