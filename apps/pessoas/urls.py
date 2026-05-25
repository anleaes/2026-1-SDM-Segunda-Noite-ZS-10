from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, ProfissionalSaudeViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'profissionais', ProfissionalSaudeViewSet)

urlpatterns = router.urls
