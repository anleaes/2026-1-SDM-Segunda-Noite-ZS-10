from rest_framework.routers import DefaultRouter
from .views import AtendimentoViewSet, DoseAtendimentoViewSet

router = DefaultRouter()
router.register(r'doses', DoseAtendimentoViewSet, basename='doseatendimento')
router.register(r'', AtendimentoViewSet, basename='atendimento')

urlpatterns = router.urls