from rest_framework import serializers
from .models import Notificacao

class NotificacaoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)

    class Meta:
        model = Notificacao
        fields = [
            'id', 'paciente', 'paciente_nome',
            'titulo', 'mensagem', 'data_envio', 'tipo', 'lida'
        ]