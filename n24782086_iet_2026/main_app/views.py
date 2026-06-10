from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
# Tambahkan 'render' di sini untuk memanggil halaman home biasa
from django.shortcuts import get_object_or_404, redirect, render 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Report

# ==========================================
# VIEW BERANDA / LANDING PAGE (Baru ditambahkan)
# ==========================================
def home_view(request):
    return render(request, 'main_app/home.html')


# ==========================================
# VIEW PUBLIK (Bisa diakses Citizen & Admin)
# ==========================================

# Menampilkan semua daftar laporan (List) - SUDAH DIPERBAIKI AGAR TERBARU DI ATAS
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html' 
    context_object_name = 'reports'
    ordering = ['-id']  # <-- INI DIA TRIKNYA! Menambahkan minus (-) sebelum id artinya mengurutkan dari yang terbaru


# Menampilkan detail satu laporan
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# ==========================================
# VIEW TERPROTEKSI (Hanya bisa diakses Admin)
# ==========================================

# Membuat laporan baru
class ReportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    # Fungsi pengecekan: Apakah user sudah login DAN apakah dia Admin? 
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    # Jika bukan Admin, arahkan kembali dengan pesan error 
    def handle_no_permission(self):
        messages.error(self.request, "Akses Ditolak! Fitur Tambah Data hanya untuk Admin.")
        return redirect('report_list')


# Mengedit laporan
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


# Menghapus laporan
class ReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report_confirm.html'
    success_url = reverse_lazy('report_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Akses Ditolak! Fitur Hapus Data hanya untuk Admin.")
        return redirect('report_list')

    # Feedback sukses menghapus (dari Lab 5)
    def post(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus secara permanen!")
        return super().post(request, *args, **kwargs)


# View khusus untuk Workflow perubahan status
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