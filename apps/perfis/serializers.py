from rest_framework import serializers
from .models import PerfilSaude

class PerfilSaudeSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)

    class Meta:
        model = PerfilSaude
        fields = ['id', 'paciente', 'paciente_nome', 'grupo_risco', 'gestante', 'alergias', 'observacoes']
