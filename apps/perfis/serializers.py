from rest_framework import serializers
from .models import PerfilSaude

class PerfilSaudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilSaude
        fields = '__all__'
