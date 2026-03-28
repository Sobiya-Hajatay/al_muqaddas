from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'phone', 'role', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": ("phone", "role", "wallet_balance"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {
            "fields": ("phone", "role", "wallet_balance"),
        }),
    )