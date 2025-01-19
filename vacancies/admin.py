from django.contrib import admin
from .models import VacanciesPage


class VacanciesPageAdmin(admin.ModelAdmin):
    list_display = ('vacancies_count', 'page_title')


admin.site.register(VacanciesPage, VacanciesPageAdmin)
