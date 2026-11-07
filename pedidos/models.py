"""Models for the pedidos app."""

from django.db import models
from django.conf import settings
from catalogo.models import Producto


class Pedido(models.Model):
    """Orden de compra realizada por un cliente."""
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_PAGADO = 'pagado'
    ESTADO_ENVIADO = 'enviado'
    ESTADO_ENTREGADO = 'entregado'
    ESTADO_CANCELADO = 'cancelado'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_ENVIADO, 'Enviado'),
        (ESTADO_ENTREGADO, 'Entregado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    direccion_envio = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    metodo_pago = models.CharField(max_length=50, blank=True)
    transaccion_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.cliente_nombre}'


class DetallePedido(models.Model):
    """Linea de un pedido: producto, cantidad y precio unitario."""
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles',
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalles de pedido'

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    @property
    def subtotal_linea(self):
        return self.cantidad * self.precio_unitario


class MetodoEnvio(models.Model):
    """Opciones de envio disponibles con costo y tiempo estimado."""
    nombre = models.CharField(max_length=100)  # Estándar, Exprés, etc.
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega = models.CharField(max_length=100)  # ej. "3-5 días hábiles"
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Método de envío'
        verbose_name_plural = 'Métodos de envío'
        ordering = ['costo']

    def __str__(self):
        return f'{self.nombre} - ${self.costo} ({self.tiempo_entrega})'


class Envio(models.Model):
    """Registro de envio vinculado a un pedido."""
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='envio',
    )
    metodo = models.ForeignKey(MetodoEnvio, on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega = models.CharField(max_length=100)
    numero_guia = models.CharField(max_length=100, blank=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Envío'
        verbose_name_plural = 'Envíos'

    def __str__(self):
        return f'Envío para Pedido #{self.pedido.pk}'