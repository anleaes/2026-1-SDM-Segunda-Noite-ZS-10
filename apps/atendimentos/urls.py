from rest_framework.routers import DefaultRouter
from .views import AtendimentoViewSet, DoseAtendimentoViewSet

router = DefaultRouter()
router.register(r'', AtendimentoViewSet, basename='atendimento')
router.register(r'doses', DoseAtendimentoViewSet, basename='doseatendimento')

urlpatterns = router.urls