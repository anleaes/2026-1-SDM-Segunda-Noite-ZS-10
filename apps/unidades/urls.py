from rest_framework.routers import DefaultRouter
from .views import UnidadeSaudeViewSet

router = DefaultRouter()
router.register(r'unidades', UnidadeSaudeViewSet)

urlpatterns = router.urls
