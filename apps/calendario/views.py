from rest_framework import viewsets
from .models import CalendarioVacinal
from .serializers import CalendarioVacinaSerializer


class CalendarioVacinaViewSet(viewsets.ModelViewSet):
    queryset = CalendarioVacinal.objects.all()
    serializer_class = CalendarioVacinaSerializer