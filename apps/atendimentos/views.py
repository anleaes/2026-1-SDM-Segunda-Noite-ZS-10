from django.shortcuts import render
from rest_framework import viewsets
from .models import Atendimento, DoseAtendimento
from .serializers import AtendimentoSerializer, DoseAtendimentoSerializer
# Create your views here.
class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer

class DoseAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = DoseAtendimento.objects.all()
    serializer_class = DoseAtendimentoSerializer