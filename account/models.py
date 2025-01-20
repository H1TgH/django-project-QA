from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.admin.models import LogEntry as AdminLogEntry


class CustomUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
    )

    def delete(self, *args, **kwargs):
        AdminLogEntry.objects.filter(user=self).delete()

        super().delete(*args, **kwargs)
