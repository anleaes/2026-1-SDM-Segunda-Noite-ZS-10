from rest_framework import viewsets
from .models import SituacaoVacinal
from .serializers import SituacaoVacinaSerializer

class SituacaoVacinaViewSet(viewsets.ModelViewSet):
    queryset = SituacaoVacinal.objects.all()
    serializer_class = SituacaoVacinaSerializer
