from rest_framework.routers import DefaultRouter
from .views import CampanhaVacinacaoViewSet

router = DefaultRouter()
router.register(r'campanhas', CampanhaVacinacaoViewSet)

urlpatterns = router.urls
