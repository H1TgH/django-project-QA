from django.contrib import admin
from .models import SkillStatistic


class SkillStatisticAdmin(admin.ModelAdmin):
    list_display = ('year', 'skill', 'count')
    search_fields = ('skill',)
    list_filter = ('year',)

admin.site.register(SkillStatistic, SkillStatisticAdmin)