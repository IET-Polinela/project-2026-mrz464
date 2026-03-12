from django.urls import path
from . import views # Titik (.) artinya mengambil dari folder yang sama

urlpatterns = [
    path('', views.home, name='home'), # Halaman utama (kosong)
]