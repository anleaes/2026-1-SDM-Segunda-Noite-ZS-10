from rest_framework.routers import DefaultRouter
from .views import CalendarioVacinaViewSet

router = DefaultRouter()
router.register(r'', CalendarioVacinaViewSet, basename='calendariovacinal')

urlpatterns = router.urls