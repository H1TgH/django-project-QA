from django.db import models


class GeographyPageSalary(models.Model):
    city = models.CharField(max_length=255, unique=True, verbose_name='Город')
    average_salary = models.PositiveIntegerField(verbose_name='Средняя зарплата')

class GeographyPagePercentage(models.Model):
    city = models.CharField(max_length=255, unique=True, verbose_name='Город')
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
