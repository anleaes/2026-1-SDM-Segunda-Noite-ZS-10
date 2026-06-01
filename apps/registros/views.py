from django.db import transaction
from rest_framework import viewsets

from .models import RegistroVacinacao
from .serializers import RegistroVacinacaoSerializer


class RegistroVacinacaoViewSet(viewsets.ModelViewSet):
    queryset = RegistroVacinacao.objects.all()
    serializer_class = RegistroVacinacaoSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        # Devolve a dose ao estoque do lote ao excluir o registro.
        lote = instance.lote
        super().perform_destroy(instance)
        lote.quantidade_disponivel += 1
        lote.save(update_fields=['quantidade_disponivel'])
