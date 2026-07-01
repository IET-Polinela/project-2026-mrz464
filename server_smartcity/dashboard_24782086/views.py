from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count, Q
from main_app.models import Report  # Tetap pertahankan model utama

# --- IMPORT DRF UNTUK KEBUTUHAN LAB 10 & 12 ---
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated  # Ubah agar mengenali Token JWT
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly

# ====================================================================
# KODE LAB 7 & 8 - UNTUK MENYUPLAI DATA KE WEB HTML & PLOT CHART.JS
# ====================================================================

# 1. Menampilkan halaman HTML utama
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard_24782086/index.html'

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_admin)

    def handle_no_permission(self):
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.error(self.request, "Akses Ditolak! Halaman ini hanya untuk Admin/Petugas.")
        return redirect('login')

# 2. API untuk menyuplai data ke Chart.js dan Tabel Dashboard
def dashboard_data(request):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Akses Ditolak!")
    status_counts = list(Report.objects.values('status').annotate(total=Count('status')))
    category_counts = list(Report.objects.values('category').annotate(total=Count('category')))
    
    latest_reported = list(Report.objects.filter(status='REPORTED').order_by('-id').values('title', 'category', 'location')[:5])
    latest_resolved = list(Report.objects.filter(status='RESOLVED').order_by('-id').values('title', 'category', 'location')[:5])
    
    return JsonResponse({
        'status_data': status_counts,
        'category_data': category_counts,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
    })

# 3. API untuk fitur Live Search (SUDAH DIPERBAIKI AGAR TERBARU DI ATAS)
def report_search_api(request):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Akses Ditolak!")
    query = request.GET.get('q', '')
    
    # Tambahkan .order_by('-id') agar laporan baru otomatis berada di baris paling atas tabel
    reports = Report.objects.filter(
        Q(title__icontains=query) | Q(location__icontains=query)
    ).order_by('-id')[:10]
    
    results = []
    for r in reports:
        results.append({
            'id': r.id,
            'title': r.title,
            'category': r.category,
            'status': r.status,
            'location': r.location
        })
    return JsonResponse({'results': results})

# 4. API untuk mengambil detail laporan (Pop-up Modal)
def report_detail_api(request, pk):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Akses Ditolak!")
    try:
        r = Report.objects.get(pk=pk)
        return JsonResponse({
            'title': r.title,
            'category': r.category,
            'description': r.description,
            'location': r.location,
            'status': r.get_status_display(),
        })
    except Report.DoesNotExist:
        from django.http import Http404
        raise Http404("Laporan tidak ditemukan")

# ====================================================================
# KODE LAB 10 & 12 - DRF API UNTUK SPA CITIZEN PORTAL
# ====================================================================

class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_permissions(self):
        """
        Mengatur hak akses dinamis secara ketat (Aturan Lab 10):
        - Edit (update, partial_update) dan Hapus (destroy) wajib pemilik & status DRAFT.
        - Akses lainnya (List, Detail, Create) hanya butuh login umum (IsAuthenticated).
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        tab = self.request.query_params.get('tab')
        if tab == 'my_reports':
            return Report.objects.filter(reporter=user).order_by('-created_at')
        elif tab == 'feed':
            # Feed kota only shows reported, verified, in_progress, resolved reports
            return Report.objects.exclude(status='DRAFT').order_by('-created_at')
        else:
            # Default or detail view: hide drafts of other users
            return Report.objects.filter(
                Q(reporter=user) | ~Q(status='DRAFT')
            ).order_by('-created_at')

    def perform_create(self, serializer):
        # KUNCI UTAMA: Otomatis mencatat akun user token yang aktif ke database
        serializer.save(reporter=self.request.user)