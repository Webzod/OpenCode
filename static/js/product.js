/* Zapatos Store - JavaScript para filtrado dinámico de productos */

document.addEventListener('DOMContentLoaded', function() {
    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroTalla = document.getElementById('filtro-talla');
    const filtroColor = document.getElementById('filtro-color');
    const filtroQ = document.getElementById('filtro-q');
    const btnAplicar = document.getElementById('btn-aplicar-filtros');
    const contenedor = document.getElementById('productos-container');
    const jsonUrl = document.getElementById('productos-json').dataset.url;

    if (!contenedor || !jsonUrl) return;

    function renderizarProductos(productos) {
        contenedor.innerHTML = '';

        if (productos.length === 0) {
            contenedor.innerHTML = `
                <div class="col-12">
                    <div class="text-center py-5">
                        <i class="bi bi-search display-4 text-muted"></i>
                        <h3>No se encontraron productos</h3>
                        <p class="text-muted">Intenta ajustar tus filtros de búsqueda.</p>
                    </div>
                </div>
            `;
            return;
        }

        productos.forEach(p => {
            const disponible = p.stock > 0;
            const html = `
                <div class="col">
                    <div class="card h-100 shadow-sm">
                        ${p.imagen ? `<img src="${p.imagen}" alt="${p.nombre}" class="card-img-top" style="height: 200px; object-fit: cover;">` : `<div class="bg-light border-bottom h-100 d-flex align-items-center justify-content-center text-muted" style="height: 200px;"><i class="bi bi-image"></i></div>`}
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${p.nombre}</h5>
                            <p class="card-text small text-muted">${p.tipo} · ${p.talla} · ${p.color}</p>
                            <div class="mt-auto">
                                <span class="fw-bold">$${parseFloat(p.precio).toFixed(2)}</span>
                                ${disponible ? `<span class="badge bg-success ms-2">${p.stock} en stock</span>` : `<span class="badge bg-danger ms-2">Agotado</span>`}
                            </div>
                        </div>
                        <div class="card-footer border-0 bg-transparent d-flex justify-content-between align-items-center">
                            <form class="d-inline" data-product-id="${p.id}">
                                <input type="hidden" name="product_id" value="${p.id}">
                                <input type="hidden" name="quantity" value="1">
                                ${disponible ? `
                                    <button type="submit" class="btn btn-sm btn-outline-primary">Agregar</button>
                                ` : `<button type="button" class="btn btn-sm btn-outline-secondary" disabled>Agotado</button>`}
                            </form>
                            <a href="/producto/${p.id}/" class="btn btn-sm btn-primary">Ver</a>
                        </div>
                    </div>
                </div>
            `;
            contenedor.innerHTML += html;
        });

        // Re-vincular eventos de formularios dinámicos
        document.body.addEventListener('submit', function(e) {
            const form = e.target;
            if (form.tagName === 'FORM' && form.dataset.productId) {
                e.preventDefault();
                agregarProductoDinamico(form.dataset.productId);
            }
        });
    }

    function aplicarFiltros() {
        const params = new URLSearchParams();
        if (filtroTipo.value) params.append('tipo', filtroTipo.value);
        if (filtroTalla.value) params.append('talla', filtroTalla.value);
        if (filtroColor.value) params.append('color', filtroColor.value);
        if (filtroQ.value) params.append('q', filtroQ.value);

        fetch(`${jsonUrl}?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            renderizarProductos(data.productos || []);
        })
        .catch(error => {
            console.error('Error filtrando:', error);
        });
    }

    btnAplicar.addEventListener('click', aplicarFiltros);

    // También aplicar al presionar Enter en el buscador
    filtroQ.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            aplicarFiltros();
        }
    });
});

function agregarProductoDinamico(productId) {
    const btn = document.querySelector(`form[data-product-id="${productId}"] button`);
    const textoOriginal = btn.textContent;

    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-spinner"></i>';

    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', '1');

    fetch('/pedidos/carrito/agregar/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            btn.innerHTML = '<i class="bi bi-check2"></i>';
            actualizarContadorCarrito();
            setTimeout(() => {
                btn.disabled = false;
                btn.innerHTML = textoOriginal;
            }, 1000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        btn.disabled = false;
        btn.innerHTML = textoOriginal;
    });
}

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
    });
}