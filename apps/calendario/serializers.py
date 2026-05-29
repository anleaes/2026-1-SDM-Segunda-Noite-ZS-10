from rest_framework import serializers
from .models import CalendarioVacinal

class CalendarioVacinaSerializer(serializers.ModelSerializer):
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)

    class Meta:
        model = CalendarioVacinal
        fields = [
            'id', 'vacina', 'vacina_nome',
            'idade_minima_meses', 'idade_maxima_meses',
            'publico_alvo', 'dose_recomendada', 'obrigatoria'
        ]