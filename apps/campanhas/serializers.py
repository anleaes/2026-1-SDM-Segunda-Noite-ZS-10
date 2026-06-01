from rest_framework import serializers
from .models import CampanhaVacinacao

class CampanhaVacinacaoSerializer(serializers.ModelSerializer):
    # Descrição e público-alvo são opcionais (alinhado ao formulário do app).
    descricao = serializers.CharField(required=False, allow_blank=True)
    publico_alvo = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CampanhaVacinacao
        fields = [
            'id', 'nome', 'descricao',
            'data_inicio', 'data_fim',
            'publico_alvo', 'ativa', 'vacinas'
        ]

    def validate(self, attrs):
        inst = self.instance
        inicio = attrs.get('data_inicio') or getattr(inst, 'data_inicio', None)
        fim = attrs.get('data_fim') or getattr(inst, 'data_fim', None)
        if inicio and fim and fim < inicio:
            raise serializers.ValidationError(
                {'data_fim': 'A data de fim deve ser posterior à data de início.'}
            )
        return attrs
