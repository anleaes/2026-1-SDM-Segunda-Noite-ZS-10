from rest_framework import viewsets
from .models import UnidadeSaude
from .serializers import UnidadeSaudeSerializer

class UnidadeSaudeViewSet(viewsets.ModelViewSet):
    queryset = UnidadeSaude.objects.all()
    serializer_class = UnidadeSaudeSerializer
