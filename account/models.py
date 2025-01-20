from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=30, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='Email')
    is_admin = models.BooleanField(default=False)
    admin_granted_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='admin_granted_users')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')

    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions_set', blank=True
    )

    def __str__(self):
        return self.username
    