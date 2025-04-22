from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'verified', 'access_level', 'is_staff']


    list_filter = ['verified', 'access_level', 'is_staff']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('access_level', 'verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'access_level', 'verified', 'password1', 'password2'),
        }),
    )

    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['id']

admin.site.register(CustomUser, CustomUserAdmin)
