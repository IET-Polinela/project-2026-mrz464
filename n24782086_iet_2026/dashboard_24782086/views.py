from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count, Q
from main_app.models import Report  # Tetap pertahankan model utama

# --- IMPORT DRF UNTUK KEBUTUHAN LAB 10 & 12 ---
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from .serializers import ReportSerializer

# ====================================================================
# KODE LAB 7 & 8 - UNTUK MENYUPLAI DATA KE WEB HTML & PLOT CHART.JS
# ====================================================================

# 1. Menampilkan halaman HTML utama
class DashboardView(TemplateView):
    template_name = 'dashboard_24782086/index.html'

# 2. API untuk menyuplai data ke Chart.js dan Tabel Dashboard
def dashboard_data(request):
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
        return JsonResponse({'error': 'Not found'}, status=404)

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
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Menyinkronkan urutan agar SPA Portal Warga juga menampilkan data terbaru di atas
        return Report.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()