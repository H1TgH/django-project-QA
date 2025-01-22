from django.db import models


class DemandPage(models.Model):
    year = models.IntegerField(verbose_name='Год')
    average_salary = models.IntegerField(verbose_name='Средння зарплата за год')
    vacancies_count = models.IntegerField(verbose_name='Количество вакансий')