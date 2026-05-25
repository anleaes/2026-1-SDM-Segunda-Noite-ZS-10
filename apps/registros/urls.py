from rest_framework.routers import DefaultRouter
from .views import RegistroVacinacaoViewSet

router = DefaultRouter()
router.register(r'registros', RegistroVacinacaoViewSet)

urlpatterns = router.urls