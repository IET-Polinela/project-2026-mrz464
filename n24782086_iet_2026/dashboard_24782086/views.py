from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count, Q

# 1. Menampilkan halaman HTML utama
class DashboardView(TemplateView):
    template_name = 'dashboard_24782086/index.html'

# 2. API untuk menyuplai data ke Chart.js dan Tabel Dashboard
def dashboard_data(request):
    # Data agregasi untuk grafik
    status_counts = list(Report.objects.values('status').annotate(total=Count('status')))
    category_counts = list(Report.objects.values('category').annotate(total=Count('category')))
    
    # 5 Laporan Terbaru (REPORTED) diurutkan dari ID terbesar (paling baru)
    latest_reported = list(Report.objects.filter(status='REPORTED').order_by('-id').values('title', 'category', 'location')[:5])
    
    # 5 Laporan Selesai (RESOLVED) diurutkan dari ID terbesar (paling baru)
    latest_resolved = list(Report.objects.filter(status='RESOLVED').order_by('-id').values('title', 'category', 'location')[:5])
    
    return JsonResponse({
        'status_data': status_counts,
        'category_data': category_counts,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
    })

# 3. API untuk fitur Live Search
def report_search_api(request):
    query = request.GET.get('q', '')
    reports = Report.objects.filter(
        Q(title__icontains=query) | Q(location__icontains=query)
    )[:10]  # Dibatasi 10 agar respon server cepat
    
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