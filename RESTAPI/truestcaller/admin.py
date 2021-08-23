from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from truestcaller import models as truestcaller_models


class CustomUserAdmin(UserAdmin):
    """
    Define admin model for custom User model with no username field.
    """

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('email', 'name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'name', 'email'),
        }),
    )
    list_display = ('phone_number', 'name', 'email', 'is_staff')
    search_fields = ('phone_number', 'name', 'email')
    ordering = ('phone_number',)


# Register your models here.
admin.site.register(truestcaller_models.User, CustomUserAdmin)
admin.site.register(truestcaller_models.Directory)
