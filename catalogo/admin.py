"""Admin for the catalogo app."""

from django.contrib import admin
from .models import TipoZapato, Producto


@admin.register(TipoZapato)
class TipoZapatoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'talla', 'color', 'precio', 'stock', 'disponible', 'activo']
    list_filter = ['tipo', 'talla', 'color', 'activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['stock', 'activo']
    prepopulated_fields = {}