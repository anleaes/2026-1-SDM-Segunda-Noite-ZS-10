from rest_framework import serializers
from .models import Paciente, ProfissionalSaude

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nome', 'email', 'telefone', 'cpf', 'data_nascimento', 'ativo']

class ProfissionalSaudeSerializer(serializers.ModelSerializer):
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)

    class Meta:
        model = ProfissionalSaude
        fields = [
            'id', 'nome', 'email', 'telefone',
            'unidade_saude', 'unidade_saude_nome',
            'registro_profissional', 'cargo', 'ativo'
        ]
