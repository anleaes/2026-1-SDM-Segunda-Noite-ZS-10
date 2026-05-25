from rest_framework.routers import DefaultRouter
from .views import NotificacaoViewSet

router = DefaultRouter()
router.register(r'notificacoes', NotificacaoViewSet)

urlpatterns = router.urls
