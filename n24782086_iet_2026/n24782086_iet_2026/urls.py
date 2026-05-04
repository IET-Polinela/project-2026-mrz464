from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782086 import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rute aplikasi utama
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # --- Rute Dashboard (Lab Session 7) ---
    path('dashboard/', include('dashboard_24782086.urls')),
    
    # --- Rute Autentikasi (Lab Session 6) ---
    
    # 1. Login: Menggunakan view bawaan Django
    path("login/", auth_views.LoginView.as_view(template_name="usermanagement_24782086/login.html"), name="login"),
    
    # 2. Logout: Menggunakan view bawaan Django
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    # 3. Register: Menggunakan fungsi view kustom yang kita buat di views.py
    path("register/", user_views.register_view, name="register"),
]