from rest_framework import viewsets
from .models import Vacina, LoteVacina
from .serializers import VacinaSerializer, LoteVacinaSerializer

class VacinaViewSet(viewsets.ModelViewSet):
    queryset = Vacina.objects.all()
    serializer_class = VacinaSerializer

class LoteVacinaViewSet(viewsets.ModelViewSet):
    queryset = LoteVacina.objects.all()
    serializer_class = LoteVacinaSerializer
