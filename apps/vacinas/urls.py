from rest_framework.routers import DefaultRouter
from .views import VacinaViewSet, LoteVacinaViewSet

router = DefaultRouter()
router.register(r'', VacinaViewSet, basename='vacina')
router.register(r'lotes', LoteVacinaViewSet, basename='lotevacina')

urlpatterns = router.urls
