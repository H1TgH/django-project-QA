from django.db import models


class VacanciesPage(models.Model):
    vacancies_count = models.PositiveSmallIntegerField(verbose_name='Количество вакансий', help_text='Количество вакансий, которое необходимо выводить на странице (не рекомендуется ставить больше 10)')
    page_title = models.TextField(verbose_name='Заголовок страницы')
