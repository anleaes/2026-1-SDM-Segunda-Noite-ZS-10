from rest_framework.routers import DefaultRouter
from .views import SituacaoVacinaViewSet

router = DefaultRouter()

router.register(
    r'',
    SituacaoVacinaViewSet,
    basename='situacaovacinal'
)

urlpatterns = router.urls