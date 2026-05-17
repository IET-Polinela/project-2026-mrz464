from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

router = DefaultRouter()
router.register(r'report', ReportViewSet, basename='report') # Registrasi ke router [cite: 98]

urlpatterns = router.urls