from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet

# Inisialisasi Router DRF
router = DefaultRouter()

# Mendaftarkan ReportViewSet dengan rute 'reports'
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    # Memasukkan semua rute otomatis dari router ke dalam urlpatterns
    path('', include(router.urls)),
]