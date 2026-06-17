from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_member', 'is_staff')
    
    # Memasukkan field custom ke halaman edit user
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('is_admin', 'is_member')}),
    )

admin.site.register(User, CustomUserAdmin)