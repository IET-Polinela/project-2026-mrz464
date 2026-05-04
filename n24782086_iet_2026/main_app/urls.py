from django.urls import path
from .views import (
    home_view, # Pastikan home_view ikut di-import
    ReportListView, ReportDetailView, ReportCreateView, 
    ReportUpdateView, ReportDeleteView, ReportUpdateStatusView
)

urlpatterns = [
    # 1. Halaman utama (Landing Page)
    path('', home_view, name='home'),
    
    # 2. Halaman menampilkan daftar laporan (ListView)
    path('laporan/', ReportListView.as_view(), name='report_list'),
    
    # Halaman detail laporan (DetailView)
    path('report/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    
    # Halaman tambah laporan (CreateView)
    path('report/add/', ReportCreateView.as_view(), name='report_add'),
    
    # Halaman edit laporan (UpdateView)
    path('report/<int:pk>/edit/', ReportUpdateView.as_view(), name='report_edit'),
    
    # Halaman konfirmasi hapus (DeleteView)
    path('report/<int:pk>/delete/', ReportDeleteView.as_view(), name='report_delete'),
    
    # URL khusus untuk perubahan status workflow
    path('report/<int:pk>/status/', ReportUpdateStatusView.as_view(), name='report_status'),
]