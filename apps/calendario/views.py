from django.shortcuts import render
from rest_framework import viewsets
from .models import CalendarioVacinal
from .serializers import CalendarioVacinaSerializer
# Create your views here.
class CalendarioVacinaViewSet(viewsets.ModelViewSet):
    queryset = CalendarioVacinal.objects.all()
    serializer_class = CalendarioVacinaSerializer