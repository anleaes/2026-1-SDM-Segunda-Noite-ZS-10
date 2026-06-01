from rest_framework import serializers
from .models import Vacina, LoteVacina

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = ['id', 'nome', 'fabricante', 'doenca_prevenida', 'quantidade_doses', 'intervalo_dias', 'ativa']

    def validate_quantidade_doses(self, value):
        if value < 1:
            raise serializers.ValidationError('A vacina deve ter pelo menos 1 dose.')
        if value > 10:
            raise serializers.ValidationError('Quantidade de doses inválida (máximo 10).')
        return value

    def validate_intervalo_dias(self, value):
        if value < 0:
            raise serializers.ValidationError('O intervalo entre doses não pode ser negativo.')
        return value


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

    def validate_quantidade_disponivel(self, value):
        if value < 0:
            raise serializers.ValidationError('A quantidade disponível não pode ser negativa.')
        return value

    def validate_data_validade(self, value):
        from django.utils import timezone
        # Só impede validade no passado ao criar um lote novo.
        if self.instance is None and value < timezone.now().date():
            raise serializers.ValidationError('A data de validade não pode estar no passado.')
        return value
