"""Models for the accounts app."""

from django.contrib.auth.models import User
from django.db import models


class PerfilUsuario(models.Model):
    """Perfil extendido del usuario con rol y datos adicionales."""

    ROLE_CLIENTE = 'cliente'
    ROLE_ADMIN = 'admin'

    ROLES = [
        (ROLE_CLIENTE, 'Cliente'),
        (ROLE_ADMIN, 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default=ROLE_CLIENTE)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'{self.user.username} - {self.get_rol_display()}'

    def es_cliente(self):
        return self.rol == self.ROLE_CLIENTE

    def es_admin(self):
        return self.rol == self.ROLE_ADMIN