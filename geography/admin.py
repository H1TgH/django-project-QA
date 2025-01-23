from django.contrib import admin
from .models import GeographyPageSalary


class GeographyPageSalaryAdmin(admin.ModelAdmin):
    list_display = ('city', 'average_salary')

admin.site.register(GeographyPageSalary, GeographyPageSalaryAdmin)