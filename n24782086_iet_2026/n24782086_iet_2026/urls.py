from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782086 import views as user_views

urlpatterns = [
    # 1. Halaman Utama (Root)
    path('', include('main_app.urls')), 
    
    # 2. Dashboard dengan Namespace 'dashboard' (PENTING untuk base.html)
    path('dashboard/', include('dashboard_24782086.urls')), 

    # 3. REST API untuk Lab 9
    path('api/', include('dashboard_24782086.api_urls')),

    # 4. Fitur Lainnya
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # 5. Login & Register
    path("login/", auth_views.LoginView.as_view(template_name="usermanagement_24782086/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", user_views.register_view, name="register"),
]