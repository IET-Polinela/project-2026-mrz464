from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782086 import views as user_views

# IMPORT UNTUK LAB 10 (JWT & REGISTRASI API)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usermanagement_24782086.api_views import RegisterView

urlpatterns = [
    # --- 1. RUTE HALAMAN UTAMA & DASHBOARD ---
    # main_app akan menangani Landing Page / Info Aplikasi asli saat mengakses IP polosan
    path('', include('main_app.urls')), 
    path('dashboard/', include('dashboard_24782086.urls')), 
    
    # --- 2. RUTE REST API LAB 9 & 10 ---
    path('api/', include('dashboard_24782086.api_urls')),
    
    # --- 3. ENDPOINT REGISTRASI API CITIZEN ---
    path('api/register/', RegisterView.as_view(), name='api_register'),
    
    # --- 4. ENDPOINT AUTENTIKASI API JWT ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- 5. RUTE ADMIN & AUTENTIKASI WEB HTML ---
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path("login/", auth_views.LoginView.as_view(template_name="usermanagement_24782086/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", user_views.register_view, name="register"),
]