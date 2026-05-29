from rest_framework.routers import DefaultRouter
from .views import CampanhaVacinacaoViewSet

router = DefaultRouter()

router.register(
    r'',
    CampanhaVacinacaoViewSet,
    basename='campanhavacinacao'
)

urlpatterns = router.urls