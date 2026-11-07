"""Views for the usuarios app."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction

from .models import PerfilUsuario


def registro_view(request):
    """Vista de registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        rol = request.POST.get('rol', PerfilUsuario.ROLE_CLIENTE)

        # Validaciones básicas
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'usuarios/registro.html')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuarios/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuarios/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'usuarios/registro.html')

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            PerfilUsuario.objects.create(user=user, rol=rol)

        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect('usuarios:login')

    context = {'roles': PerfilUsuario.ROLES}
    return render(request, 'usuarios/registro.html', context)


def login_view(request):
    """Vista de inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            next_url = request.GET.get('next', 'usuarios:perfil')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')


def logout_view(request):
    """Vista de cierre de sesión."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required
def perfil_view(request):
    """Vista del perfil del usuario con sus pedidos."""
    from pedidos.models import Pedido

    perfil = request.user.perfil
    pedidos = Pedido.objects.filter(cliente_email=request.user.email).order_by('-fecha')

    context = {
        'perfil': perfil,
        'pedidos': pedidos,
    }
    return render(request, 'usuarios/perfil.html', context)


@login_required
def editar_perfil_view(request):
    """Vista para editar el perfil del usuario."""
    perfil = request.user.perfil

    if request.method == 'POST':
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')

        perfil.telefono = telefono
        perfil.direccion = direccion
        perfil.save()

        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('usuarios:perfil')

    context = {'perfil': perfil}
    return render(request, 'usuarios/editar_perfil.html', context)