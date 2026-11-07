"""Admin for the usuarios app."""

from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'telefono', 'fecha_registro']
    list_filter = ['rol', 'fecha_registro']
    search_fields = ['user__username', 'user__email']