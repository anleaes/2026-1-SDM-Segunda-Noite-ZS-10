from rest_framework.routers import DefaultRouter
from .views import PerfilSaudeViewSet

router = DefaultRouter()
router.register(r'perfis', PerfilSaudeViewSet)

urlpatterns = router.urls
