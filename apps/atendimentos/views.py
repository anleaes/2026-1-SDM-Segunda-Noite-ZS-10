from rest_framework import viewsets
from .models import Atendimento, DoseAtendimento
from .serializers import AtendimentoSerializer, DoseAtendimentoSerializer


class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer

class DoseAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = DoseAtendimento.objects.all()
    serializer_class = DoseAtendimentoSerializer