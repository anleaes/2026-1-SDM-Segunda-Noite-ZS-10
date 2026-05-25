from django.db import models

TIPO_CHOICES = [
    ('lembrete', 'Lembrete'),
    ('alerta', 'Alerta'),
    ('informativo', 'Informativo'),
]

class Notificacao(models.Model):
    paciente = models.ForeignKey(
        'pessoas.Paciente', on_delete=models.CASCADE, related_name='notificacoes'
    )
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.titulo} - {self.paciente}'
