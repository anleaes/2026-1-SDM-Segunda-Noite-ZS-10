from rest_framework import serializers
from .models import CalendarioVacinal

class CalendarioVacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarioVacinal
        fields = '__all__'