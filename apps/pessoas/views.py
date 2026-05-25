from rest_framework import viewsets
from .models import Paciente, ProfissionalSaude
from .serializers import PacienteSerializer, ProfissionalSaudeSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class ProfissionalSaudeViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalSaude.objects.all()
    serializer_class = ProfissionalSaudeSerializer
