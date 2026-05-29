from rest_framework.routers import DefaultRouter
from .views import UnidadeSaudeViewSet

router = DefaultRouter()
router.register(r'', UnidadeSaudeViewSet, basename='unidadesaude')

urlpatterns = router.urls
