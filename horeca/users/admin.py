from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_superuser', 'is_staff', 'groups'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
        'is_active',
    )
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(models.Admin)
class AdministratorAdmin(admin.ModelAdmin):
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(models.Manager)
class ManagerAdmin(admin.ModelAdmin):
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(models.Candidate)
class CandidateAdmin(admin.ModelAdmin):
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(models.CandidateCreator)
class CandidateCreatorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    pass
