from rest_framework import serializers
from .models import RegistroVacinacao

class RegistroVacinacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVacinacao
        fields = '__all__'