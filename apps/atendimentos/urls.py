from rest_framework.routers import DefaultRouter
from .views import AtendimentoViewSet, DoseAtendimentoViewSet

router = DefaultRouter()
router.register(r'atendimentos', AtendimentoViewSet)
router.register(r'doses', DoseAtendimentoViewSet)

urlpatterns = router.urls