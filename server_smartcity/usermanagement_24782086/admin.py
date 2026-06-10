from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Daftarkan model User kustom kamu ke admin panel
admin.site.register(User, UserAdmin)