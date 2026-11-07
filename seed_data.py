"""Script para poblar datos iniciales de la tienda de zapatos."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_zapatos.settings')
django.setup()

from catalogo.models import TipoZapato, Producto
from pedidos.models import MetodoEnvio

# Tipos de zapato
tipos_data = [
    ('Deportivo', 'deportivo', 'Zapatos para hacer ejercicio y deporte'),
    ('Formal', 'formal', 'Zapatos elegantes para oficina y eventos'),
    ('Infantil', 'infantil', 'Zapatos para niños y niñas'),
    ('Casual', 'casual', 'Zapatos cómodos para el día a día'),
    ('Botas', 'botas', 'Botas y botines'),
]

for nombre, slug, desc in tipos_data:
    TipoZapato.objects.get_or_create(slug=slug, defaults={'nombre': nombre, 'descripcion': desc})

# Métodos de envío
metodos_data = [
    ('Estándar', 5.00, '5-7 días hábiles'),
    ('Exprés', 12.00, '2-3 días hábiles'),
    ('Recogida en tienda', 0.00, '1-2 días hábiles'),
]

for nombre, costo, tiempo in metodos_data:
    MetodoEnvio.objects.get_or_create(nombre=nombre, defaults={'costo': costo, 'tiempo_entrega': tiempo})

# Productos de muestra
productos_data = [
    ('Zapato Deportivo AirRun', 'Zapato deportivo con amortiguación para running diario.', 'Deportivo', '42', 'Negro', 89.99, 15),
    ('Zapato Deportivo AirRun', 'Zapato deportivo con amortiguación para running diario.', 'Deportivo', '40', 'Blanco', 89.99, 10),
    ('Zapato Formal Oxford', 'Zapato formal de cuero para ocasiones especiales.', 'Formal', '41', 'Marrón', 120.00, 8),
    ('Zapato Formal Oxford', 'Zapato formal de cuero para ocasiones especiales.', 'Formal', '43', 'Negro', 120.00, 5),
    ('Zapatilla Infantil Play', 'Zapatilla cómoda y resistente para niños.', 'Infantil', '28', 'Azul', 45.00, 20),
    ('Zapatilla Infantil Play', 'Zapatilla cómoda y resistente para niños.', 'Infantil', '30', 'Rosa', 45.00, 12),
    ('Bota de Montaña Trek', 'Bota impermeable para senderismo y montaña.', 'Botas', '42', 'Verde olivo', 150.00, 7),
    ('Zapato Casual Lona', 'Zapato casual de lona para uso diario.', 'Casual', '39', 'Blanco', 55.00, 18),
    ('Zapato Casual Lona', 'Zapato casual de lona para uso diario.', 'Casual', '41', 'Negro', 55.00, 9),
]

for nombre, desc, tipo_nom, talla, color, precio, stock in productos_data:
    tipo = TipoZapato.objects.get(nombre=tipo_nom)
    Producto.objects.get_or_create(
        nombre=nombre,
        talla=talla,
        color=color,
        tipo=tipo,
        defaults={
            'descripcion': desc,
            'precio': precio,
            'stock': stock,
        },
    )

print('Datos iniciales creados correctamente')
print(f'- {TipoZapato.objects.count()} tipos de zapato')
print(f'- {MetodoEnvio.objects.count()} métodos de envío')
print(f'- {Producto.objects.count()} productos')