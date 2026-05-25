from django.shortcuts import render
from rest_framework import viewsets
from .models import RegistroVacinacao
from .serializers import RegistroVacinacaoSerializer
# Create your views here.
class RegistroVacinacaoViewSet(viewsets.ModelViewSet):
    queryset = RegistroVacinacao.objects.all()
    serializer_class = RegistroVacinacaoSerializer