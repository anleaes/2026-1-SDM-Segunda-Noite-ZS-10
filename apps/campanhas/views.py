from rest_framework import viewsets
from .models import CampanhaVacinacao
from .serializers import CampanhaVacinacaoSerializer

class CampanhaVacinacaoViewSet(viewsets.ModelViewSet):
    queryset = CampanhaVacinacao.objects.all()
    serializer_class = CampanhaVacinacaoSerializer
