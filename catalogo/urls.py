"""URLs for the catalogo app."""

from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('producto/<int:pk>/', views.product_detail, name='product_detail'),
    path('api/productos/', views.productos_json, name='productos_json'),
]