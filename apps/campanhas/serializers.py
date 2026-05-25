from rest_framework import serializers
from .models import CampanhaVacinacao


class CampanhaVacinacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampanhaVacinacao
        fields = '__all__'