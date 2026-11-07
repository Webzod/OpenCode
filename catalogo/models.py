"""Models for the catalogo app."""

from django.db import models


class TipoZapato(models.Model):
    """Categoria de zapato: Deportivo, Formal, Infantil, etc."""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Tipo de zapato'
        verbose_name_plural = 'Tipos de zapato'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto individual: un zapato con talla, color, precio y stock."""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(
        TipoZapato,
        on_delete=models.CASCADE,
        related_name='productos',
    )
    talla = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.nombre} - Talla {self.talla} - {self.color}'

    @property
    def disponible(self):
        return self.activo and self.stock > 0