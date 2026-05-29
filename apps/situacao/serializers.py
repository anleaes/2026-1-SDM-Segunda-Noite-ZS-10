from rest_framework import serializers
from .models import SituacaoVacinal

class SituacaoVacinaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)

    class Meta:
        model = SituacaoVacinal
        fields = [
            'id', 'paciente', 'paciente_nome',
            'vacina', 'vacina_nome',
            'calendario_vacinal',
            'status', 'data_verificacao', 'observacao'
        ]