from rest_framework import serializers
from .models import CampanhaVacinacao

class CampanhaVacinacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampanhaVacinacao
        fields = [
            'id', 'nome', 'descricao',
            'data_inicio', 'data_fim',
            'publico_alvo', 'ativa', 'vacinas'
        ]