from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Report

# Menampilkan semua daftar laporan (List)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

# Menampilkan detail satu laporan
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

# Membuat laporan baru
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

# Mengedit laporan
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

# Menghapus laporan
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_report_confirm.html'
    success_url = reverse_lazy('report_list')

# View khusus untuk Workflow perubahan status
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('report_list')