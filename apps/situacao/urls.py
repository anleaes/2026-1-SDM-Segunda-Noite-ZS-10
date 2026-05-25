from rest_framework.routers import DefaultRouter
from .views import SituacaoVacinaViewSet

router = DefaultRouter()
router.register(r'situacao', SituacaoVacinaViewSet)

urlpatterns = router.urls
