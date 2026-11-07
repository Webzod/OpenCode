"""Views for the catalogo app."""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import TipoZapato, Producto


def product_list(request):
    """Lista de productos con filtros por tipo, talla y color."""
    tipos = TipoZapato.objects.all()
    productos = Producto.objects.filter(activo=True).select_related('tipo')

    tipo_id = request.GET.get('tipo')
    talla = request.GET.get('talla')
    color = request.GET.get('color')
    q = request.GET.get('q')

    if tipo_id:
        productos = productos.filter(tipo_id=tipo_id)
    if talla:
        productos = productos.filter(talla__iexact=talla)
    if color:
        productos = productos.filter(color__icontains=color)
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

    # Tallas y colores disponibles para los filtros del sidebar
    tallas = Producto.objects.filter(activo=True).values_list('talla', flat=True).distinct()
    colores = Producto.objects.filter(activo=True).values_list('color', flat=True).distinct()

    context = {
        'tipos': tipos,
        'productos': productos,
        'tallas': tallas,
        'colores': colores,
        'filtro_tipo': tipo_id,
        'filtro_talla': talla,
        'filtro_color': color,
        'query': q,
    }
    return render(request, 'catalogo/product_list.html', context)


def product_detail(request, pk):
    """Detalle de un producto individual."""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    productos_relacionados = Producto.objects.filter(
        tipo=producto.tipo, activo=True
    ).exclude(pk=producto.pk)[:4]

    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'catalogo/product_detail.html', context)


def productos_json(request):
    """Endpoint JSON para filtrado dinamico via Fetch/JS sin recargar pagina."""
    productos = Producto.objects.filter(activo=True).select_related('tipo')

    tipo_id = request.GET.get('tipo')
    talla = request.GET.get('talla')
    color = request.GET.get('color')
    q = request.GET.get('q')

    if tipo_id:
        productos = productos.filter(tipo_id=tipo_id)
    if talla:
        productos = productos.filter(talla__iexact=talla)
    if color:
        productos = productos.filter(color__icontains=color)
    if q:
        from django.db.models import Q
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

    data = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio': str(p.precio),
            'tipo': p.tipo.nombre,
            'talla': p.talla,
            'color': p.color,
            'stock': p.stock,
            'disponible': p.disponible,
            'imagen': p.imagen.url if p.imagen else None,
        }
        for p in productos
    ]
    return JsonResponse({'productos': data})