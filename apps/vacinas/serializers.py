from rest_framework import serializers
from .models import Vacina, LoteVacina

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = ['id', 'nome', 'fabricante', 'doenca_prevenida', 'quantidade_doses', 'intervalo_dias', 'ativa']

class LoteVacinaSerializer(serializers.ModelSerializer):
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)

    class Meta:
        model = LoteVacina
        fields = [
            'id', 'vacina', 'vacina_nome',
            'unidade_saude', 'unidade_saude_nome',
            'numero_lote', 'data_validade', 'quantidade_disponivel'
        ]
