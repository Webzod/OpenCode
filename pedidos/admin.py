"""Admin for the pedidos app."""

from django.contrib import admin
from .models import Pedido, DetallePedido, MetodoEnvio, Envio


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['subtotal_linea']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente_nombre', 'cliente_email', 'fecha', 'total', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['cliente_nombre', 'cliente_email', 'id']
    inlines = [DetallePedidoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal_linea']
    list_filter = ['pedido__estado']


@admin.register(MetodoEnvio)
class MetodoEnvioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'costo', 'tiempo_entrega', 'activo']
    list_editable = ['activo']


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'metodo', 'costo', 'tiempo_entrega', 'numero_guia']