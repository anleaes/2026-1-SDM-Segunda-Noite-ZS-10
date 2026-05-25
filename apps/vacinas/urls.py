from rest_framework.routers import DefaultRouter
from .views import VacinaViewSet, LoteVacinaViewSet

router = DefaultRouter()
router.register(r'vacinas', VacinaViewSet)
router.register(r'lotes', LoteVacinaViewSet)

urlpatterns = router.urls
