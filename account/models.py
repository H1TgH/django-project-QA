from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    granted_by_admin = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='granted_users',
        verbose_name='Администратор, выдавший права'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    # Изменяем related_name для groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # новое имя обратной связи
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # новое имя обратной связи
        blank=True,
    )
