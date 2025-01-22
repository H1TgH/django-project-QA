from django.db import models


class DemandPageSalary(models.Model):
    year = models.IntegerField(verbose_name="Год")
    average_salary = models.IntegerField(verbose_name="Средняя зарплата")

class DemandPageVacanciesCount(models.Model):
    year = models.IntegerField(verbose_name="Год")
    vacancies_count = models.IntegerField(verbose_name="Количество вакансий")
