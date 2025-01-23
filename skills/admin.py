from django.contrib import admin
from .models import SkillStatistic


class SkillStatisticAdmin(admin.ModelAdmin):
    list_display = ('year', 'skill', 'count')

admin.site.register(SkillStatistic, SkillStatisticAdmin)