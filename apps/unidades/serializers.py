from rest_framework import serializers
from .models import UnidadeSaude

class UnidadeSaudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeSaude
        fields = ['id', 'nome', 'endereco', 'bairro', 'telefone', 'horario_funcionamento', 'ativa']
