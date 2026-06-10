from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Report

# Import komponen tambahan untuk kebutuhan REST Framework API SPA
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from usermanagement_24782086.serializers import ReportSerializer # Mengambil serializer dari folder usermanagement kamu

# ====================================================================
# VIEW BERANDA / LANDING PAGE
# ====================================================================
def home_view(request):
    return render(request, 'main_app/home.html')


# ====================================================================
# VIEW PUBLIK (Biasa diakses via Web Multi-Page Biasa)
# ====================================================================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html' 
    context_object_name = 'reports'
    ordering = ['-id']  # Mengurutkan dari yang terbaru


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# ====================================================================
# VIEW TERPROTEKSI ADMIN (Web Multi-Page Biasa)
# ====================================================================
class ReportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Akses Ditolak! Fitur Tambah Data hanya untuk Admin.")
        return redirect('report_list')


class ReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Akses Ditolak! Fitur Edit Data hanya untuk Admin.")
        return redirect('report_list')


class ReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report_confirm.html'
    success_url = reverse_lazy('report_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Akses Ditolak! Fitur Hapus Data hanya untuk Admin.")
        return redirect('report_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus secara permanen!")
        return super().post(request, *args, **kwargs)


class ReportUpdateStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Akses Ditolak! Fitur Ubah Status hanya untuk Admin.")
        return redirect('report_list')

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        messages.success(request, "Status laporan berhasil diubah!")
        return redirect('report_list')


# ====================================================================
# VIEWSET API REST FRAMEWORK (BARU: KHUSUS MELAYANI ENDPOINT /api/reports/ SPA)
# ====================================================================
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-id')
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Mengunci akun pelapor secara otomatis berdasarkan pemilik Token JWT aktif saat submit form
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)