"""URLs for the pedidos app."""

from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrito/', views.cart_view, name='cart'),
    path('carrito/agregar/', views.cart_add, name='cart_add'),
    path('carrito/eliminar/', views.cart_remove, name='cart_remove'),
    path('carrito/actualizar/', views.cart_update, name='cart_update'),
    path('carrito/contador/', views.cart_count, name='cart_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<int:pk>/', views.order_confirmation, name='order_confirmation'),
]