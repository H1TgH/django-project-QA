from django.contrib import admin
from .models import GeographyPageSalary, GeographyPagePercentage


class GeographyPageSalaryAdmin(admin.ModelAdmin):
    list_display = ('city', 'average_salary')

class GeographyPagePercentageAdmin(admin.ModelAdmin):
    list_display = ('city', 'percentage')

admin.site.register(GeographyPageSalary, GeographyPageSalaryAdmin)
admin.site.register(GeographyPagePercentage, GeographyPagePercentageAdmin)