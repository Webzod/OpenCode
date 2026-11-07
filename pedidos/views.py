"""Views for the pedidos app."""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from catalogo.models import Producto
from .models import Pedido, DetallePedido, Envio, MetodoEnvio


def _get_cart(request):
    """Obtiene el carrito desde la sesion de Django."""
    return request.session.get('cart', {})


def _save_cart(request, cart):
    """Guarda el carrito en la sesion."""
    request.session['cart'] = cart
    request.session.modified = True


def cart_view(request):
    """Vista del carrito de compras."""
    cart = _get_cart(request)
    items = []
    subtotal = 0

    for product_id, quantity in cart.items():
        try:
            producto = Producto.objects.get(pk=product_id, activo=True)
            item_subtotal = producto.precio * quantity
            subtotal += item_subtotal
            items.append({
                'producto': producto,
                'cantidad': quantity,
                'subtotal': item_subtotal,
            })
        except Producto.DoesNotExist:
            continue

    metodos_envio = MetodoEnvio.objects.filter(activo=True)

    context = {
        'items': items,
        'subtotal': subtotal,
        'metodos_envio': metodos_envio,
    }
    return render(request, 'pedidos/cart.html', context)


@require_POST
def cart_add(request):
    """Agrega un producto al carrito via POST (AJAX o formulario)."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    cart = _get_cart(request)
    cart[product_id] = cart.get(product_id, 0) + quantity
    _save_cart(request, cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': sum(cart.values()),
            'message': 'Producto agregado al carrito',
        })

    messages.success(request, 'Producto agregado al carrito.')
    return redirect('catalogo:product_list')


@require_POST
def cart_remove(request):
    """Elimina un producto del carrito."""
    product_id = request.POST.get('product_id')
    cart = _get_cart(request)
    if product_id in cart:
        del cart[product_id]
        _save_cart(request, cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('pedidos:cart')


@require_POST
def cart_update(request):
    """Actualiza la cantidad de un producto en el carrito."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 0))

    cart = _get_cart(request)
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity
    _save_cart(request, cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('pedidos:cart')


def cart_count(request):
    """Devuelve la cantidad total de items en el carrito (para el navbar)."""
    cart = _get_cart(request)
    count = sum(cart.values())
    return JsonResponse({'cart_count': count})


def checkout(request):
    """Vista de checkout: resumen, envío y creación del pedido."""
    cart = _get_cart(request)

    if not cart:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('catalogo:product_list')

    items = []
    subtotal = 0

    for product_id, quantity in cart.items():
        try:
            producto = Producto.objects.get(pk=product_id, activo=True)
            item_subtotal = producto.precio * quantity
            subtotal += item_subtotal
            items.append({
                'producto': producto,
                'cantidad': quantity,
                'subtotal': item_subtotal,
            })
        except Producto.DoesNotExist:
            continue

    metodos_envio = MetodoEnvio.objects.filter(activo=True)

    if request.method == 'POST':
        metodo_envio_id = request.POST.get('metodo_envio')
        cliente_nombre = request.POST.get('cliente_nombre')
        cliente_email = request.POST.get('cliente_email')
        direccion_envio = request.POST.get('direccion_envio')

        try:
            metodo_envio = MetodoEnvio.objects.get(pk=metodo_envio_id, activo=True)
        except MetodoEnvio.DoesNotExist:
            messages.error(request, 'Método de envío inválido.')
            return redirect('pedidos:checkout')

        costo_envio = metodo_envio.costo
        total = subtotal + costo_envio

        with transaction.atomic():
            # Validar stock antes de crear el pedido
            for product_id, quantity in cart.items():
                producto = Producto.objects.select_for_update().get(pk=product_id)
                if producto.stock < quantity:
                    messages.error(
                        request,
                        f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}'
                    )
                    return redirect('pedidos:checkout')

            # Crear pedido
            pedido = Pedido.objects.create(
                cliente_nombre=cliente_nombre,
                cliente_email=cliente_email,
                direccion_envio=direccion_envio,
                subtotal=subtotal,
                costo_envio=costo_envio,
                total=total,
                estado=Pedido.ESTADO_PENDIENTE,
            )

            # Crear detalles y descontar stock
            for product_id, quantity in cart.items():
                producto = Producto.objects.get(pk=product_id)
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=quantity,
                    precio_unitario=producto.precio,
                )
                producto.stock -= quantity
                producto.save()

            # Crear envío
            Envio.objects.create(
                pedido=pedido,
                metodo=metodo_envio,
                costo=costo_envio,
                tiempo_entrega=metodo_envio.tiempo_entrega,
            )

        # Limpiar carrito
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, f'Pedido #{pedido.pk} creado con éxito.')
        return redirect('pedidos:order_confirmation', pk=pedido.pk)

    context = {
        'items': items,
        'subtotal': subtotal,
        'metodos_envio': metodos_envio,
    }
    return render(request, 'pedidos/checkout.html', context)


def order_confirmation(request, pk):
    """Pagina de confirmacion de pedido."""
    pedido = get_object_or_404(Pedido, pk=pk)
    context = {'pedido': pedido}
    return render(request, 'pedidos/order_confirmation.html', context)