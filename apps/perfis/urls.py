from rest_framework.routers import DefaultRouter
from .views import PerfilSaudeViewSet

router = DefaultRouter()
router.register(r'', PerfilSaudeViewSet, basename='perfilsaude')

urlpatterns = router.urls
