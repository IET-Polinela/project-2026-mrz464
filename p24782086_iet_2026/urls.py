from django.contrib import admin
from django.urls import path
from django.http import HttpResponse # Import wajib untuk Lab 1

# Ini fungsi untuk menampilkan tulisan
def welcome_view(request):
    return HttpResponse("Selamat Datang")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', welcome_view), # Ini rute untuk memanggil tulisan tersebut
]