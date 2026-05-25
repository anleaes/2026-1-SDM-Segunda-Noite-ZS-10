from rest_framework import viewsets
from .models import PerfilSaude
from .serializers import PerfilSaudeSerializer

class PerfilSaudeViewSet(viewsets.ModelViewSet):
    queryset = PerfilSaude.objects.all()
    serializer_class = PerfilSaudeSerializer
