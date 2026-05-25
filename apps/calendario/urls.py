from rest_framework.routers import DefaultRouter
from .views import CalendarioVacinaViewSet

router = DefaultRouter()
router.register(r'calendarios', CalendarioVacinaViewSet)

urlpatterns = router.urls