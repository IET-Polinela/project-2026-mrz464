from django.urls import path, include
from .views import DashboardView, dashboard_data, report_search_api, report_detail_api

app_name = 'dashboard'

urlpatterns = [
    # 1. Halaman Statistik Dashboard (Ini yang dicari base.html)
    path('', DashboardView.as_view(), name='index'),
    
    # 2. API Statistik Lab Sebelumnya
    path('api/stats/', dashboard_data, name='api_stats'),
    path('api/search/', report_search_api, name='api_search'),
    path('api/detail/<int:pk>/', report_detail_api, name='api_detail'),
    
    # 3. Menghubungkan rute API Lab 9 (Fase 2)
    path('api/', include('dashboard_24782086.api_urls')), 
]