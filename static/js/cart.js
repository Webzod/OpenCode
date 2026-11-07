/* Zapatos Store - JavaScript del carrito */

document.addEventListener('DOMContentLoaded', function() {
    actualizarContadorCarrito();

    // Escuchar clicks en botones "Agregar al carrito" (formas dinámicas)
    document.body.addEventListener('submit', function(e) {
        if (e.target.action && e.target.action.includes('/carrito/agregar/')) {
            e.preventDefault();

            const form = e.target;
            const formData = new FormData(form);
            const btn = form.querySelector('button[type="submit"]');
            const textoOriginal = btn.textContent;

            // Estado de carga
            btn.disabled = true;
            btn.innerHTML = '<i class="bi bi-spinner"></i> Agregando...';

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    actualizarContadorCarrito();

                    // Animación visual
                    btn.classList.add('agregado-animado');
                    btn.innerHTML = '<i class="bi bi-check2"></i> ¡Agregado!';

                    setTimeout(() => {
                        btn.classList.remove('agregado-animado');
                        btn.disabled = false;
                        btn.innerHTML = textoOriginal;
                    }, 1500);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                btn.disabled = false;
                btn.innerHTML = textoOriginal;
                alert('Error al agregar al carrito. Intenta de nuevo.');
            });
        }
    });
});

function actualizarContadorCarrito() {
    fetch('/pedidos/carrito/contador/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        const badge = document.getElementById('cart-count-badge');
        if (badge) {
            badge.textContent = data.cart_count;
        }
    })
    .catch(error => {
        console.error('Error obteniendo contador:', error);
    });
}