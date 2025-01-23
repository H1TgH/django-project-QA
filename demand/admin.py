from django.contrib import admin
from .models import DemandPageSalary, DemandPageVacanciesCount


class DemandPageSalaryAdmin(admin.ModelAdmin):
    list_display = ('year', 'average_salary')

class DemandPageVacanciesCountAdmin(admin.ModelAdmin):
    list_display = ('year', 'vacancies_count')

admin.site.register(DemandPageSalary, DemandPageSalaryAdmin)
admin.site.register(DemandPageVacanciesCount, DemandPageVacanciesCountAdmin)