from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active')
    list_filter = ('role',)
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Role', {'fields': ('role',)}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('role',)
        return self.readonly_fields



# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ('email', 'full_name', 'role', 'is_active')
#     list_filter = ('role',)
#     search_fields = ('email', 'full_name')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('full_name', 'phone')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('date_joined',)}),
#         ('Role', {'fields': ('role',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
#         }),
#     )
#     ordering = ('email',)

#     def get_readonly_fields(self, request, obj=None):
#         if not request.user.is_superuser:
#             return ('role',)
#         return ()
