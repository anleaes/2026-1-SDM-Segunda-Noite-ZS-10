from rest_framework import serializers
from .models import RegistroVacinacao

class RegistroVacinacaoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)
    lote_numero = serializers.CharField(source='lote.numero_lote', read_only=True)
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True, allow_null=True)
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)

    class Meta:
        model = RegistroVacinacao
        fields = [
            'id', 'paciente', 'paciente_nome',
            'vacina', 'vacina_nome',
            'lote', 'lote_numero',
            'profissional', 'profissional_nome',
            'unidade_saude', 'unidade_saude_nome',
            'atendimento',
            'data_aplicacao', 'dose', 'observacao'
        ]