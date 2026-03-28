from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    list_display = ('username', 'phone', 'role')

    # 👇 form fields clean kar diya
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('phone', 'role', 'wallet_balance')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone', 'role'),
        }),
    )

    # 👇 ye sab hata diya
    exclude = ('groups', 'user_permissions', 'last_login', 'is_superuser', 'is_staff')