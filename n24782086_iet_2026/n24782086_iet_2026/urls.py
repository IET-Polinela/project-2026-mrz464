from django.contrib import admin
from django.urls import path, include # Import include sangat penting di sini [cite: 23]

urlpatterns = [
    path('admin/', admin.site.urls),
    # Menghubungkan URL project dengan URL masing-masing app [cite: 8, 25]
    path('', include('main_app.urls')),      # Halaman utama [cite: 25]
    path('about/', include('about.urls')),   # Halaman about [cite: 38]
    path('contacts/', include('contacts.urls')), # Halaman contacts [cite: 38]
]