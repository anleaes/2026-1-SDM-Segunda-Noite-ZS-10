from rest_framework import serializers
from .models import Vacina, LoteVacina

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = '__all__'

class LoteVacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteVacina
        fields = '__all__'
