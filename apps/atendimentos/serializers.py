from rest_framework import serializers
from .models import Atendimento, DoseAtendimento

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = '__all__'

class DoseAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoseAtendimento
        fields = '__all__'