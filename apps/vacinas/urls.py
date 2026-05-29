from rest_framework.routers import DefaultRouter
from .views import VacinaViewSet, LoteVacinaViewSet

router = DefaultRouter()
router.register(r'lotes', LoteVacinaViewSet, basename='lotevacina')
router.register(r'', VacinaViewSet, basename='vacina')

urlpatterns = router.urls
