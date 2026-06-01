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

    def validate(self, attrs):
        inst = self.instance
        minima = attrs.get('idade_minima_meses', getattr(inst, 'idade_minima_meses', None))
        maxima = attrs.get('idade_maxima_meses', getattr(inst, 'idade_maxima_meses', None))
        if minima is not None and minima < 0:
            raise serializers.ValidationError(
                {'idade_minima_meses': 'A idade mínima não pode ser negativa.'}
            )
        if maxima is not None and minima is not None and maxima < minima:
            raise serializers.ValidationError(
                {'idade_maxima_meses': 'A idade máxima deve ser maior ou igual à mínima.'}
            )
        return attrs