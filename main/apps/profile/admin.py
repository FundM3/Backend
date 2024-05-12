from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('address', 'email', 'name', 'visible', 'created_at')
    search_fields = ('user__wallet_address', 'user__email', 'name')
    list_filter = ('visible', 'created_at')
    readonly_fields = ('email', 'address', 'created_at', 'user')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'visible', 'profile_img', 'created_at')
        }),
        ('Social Links', {
            'classes': ('collapse',),
            'fields': ('x_url', 'github_url', 'telegram_url'),
        }),
    )

admin.site.register(Profile, ProfileAdmin)
