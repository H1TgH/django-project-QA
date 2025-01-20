from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('granted_by_admin', 'created_at', 'updated_at')}),
    )

    list_display = ['username', 'email', 'is_staff', 'granted_by_admin', 'created_at', 'updated_at']

    list_editable = ['is_staff', 'granted_by_admin']

    readonly_fields = ['created_at', 'updated_at']

    list_filter = ['is_staff', 'granted_by_admin']

admin.site.register(CustomUser, CustomUserAdmin)
