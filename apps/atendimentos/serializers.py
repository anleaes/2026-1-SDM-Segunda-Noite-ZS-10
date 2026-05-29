from rest_framework import serializers
from .models import Atendimento, DoseAtendimento

class AtendimentoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True, allow_null=True)

    class Meta:
        model = Atendimento
        fields = [
            'id', 'paciente', 'paciente_nome',
            'unidade_saude', 'unidade_saude_nome',
            'profissional', 'profissional_nome',
            'data_atendimento', 'status', 'observacao'
        ]

class DoseAtendimentoSerializer(serializers.ModelSerializer):
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)
    lote_numero = serializers.CharField(source='lote.numero_lote', read_only=True)

    class Meta:
        model = DoseAtendimento
        fields = [
            'id', 'atendimento',
            'vacina', 'vacina_nome',
            'lote', 'lote_numero',
            'ordem_dose', 'observacao'
        ]