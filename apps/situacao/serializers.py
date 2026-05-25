from rest_framework import serializers
from .models import SituacaoVacinal

class SituacaoVacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SituacaoVacinal
        fields = '__all__'
