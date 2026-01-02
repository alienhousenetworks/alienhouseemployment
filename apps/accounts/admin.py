from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active')
    list_filter = ('role',)
    search_fields = ('email', 'full_name')

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('role',)
        return ()
