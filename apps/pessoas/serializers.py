from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Paciente, ProfissionalSaude

class PacienteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=Paciente.objects.all(),
            message='Este e-mail já foi registrado.',
        )]
    )
    cpf = serializers.CharField(
        max_length=14,
        validators=[UniqueValidator(
            queryset=Paciente.objects.all(),
            message='Este CPF já foi registrado.',
        )]
    )

    class Meta:
        model = Paciente
        fields = ['id', 'nome', 'email', 'telefone', 'cpf', 'data_nascimento', 'ativo']

    def validate_data_nascimento(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError('A data de nascimento não pode ser no futuro.')
        return value

class ProfissionalSaudeSerializer(serializers.ModelSerializer):
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=ProfissionalSaude.objects.all(),
            message='Este e-mail já foi registrado.',
        )]
    )

    class Meta:
        model = ProfissionalSaude
        fields = [
            'id', 'nome', 'email', 'telefone',
            'unidade_saude', 'unidade_saude_nome',
            'registro_profissional', 'cargo', 'ativo'
        ]
