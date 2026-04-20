from django.urls import path
from .views import (
    ReportListView, ReportDetailView, ReportCreateView, 
    ReportUpdateView, ReportDeleteView, ReportUpdateStatusView
)

urlpatterns = [
    # Halaman utama menampilkan daftar laporan (ListView)
    path('', ReportListView.as_view(), name='report_list'),
    
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