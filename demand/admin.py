from django.contrib import admin
from .models import DemandPage


class DemandPageAdmin(admin.ModelAdmin):
    list_display = ('year', 'average_salary', 'vacancies_count')
    list_filter = ('year'), 

admin.site.register(DemandPage, DemandPageAdmin)