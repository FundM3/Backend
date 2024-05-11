from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'wallet_address', 'is_active', 'is_staff', 'is_superuser')
    list_editable = ('is_active', 'is_staff')
    search_fields = ('email', 'wallet_address')
    ordering = ('email',)
    list_filter = ('is_active', 'is_staff', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'wallet_address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'wallet_address'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
