from django.urls import path
from .views import DashboardView, dashboard_data, report_search_api, report_detail_api

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('api/stats/', dashboard_data, name='api_stats'),
    path('api/search/', report_search_api, name='api_search'),
    path('api/detail/<int:pk>/', report_detail_api, name='api_detail'),
]