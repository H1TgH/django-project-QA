from django.db import models


class SkillStatistic(models.Model):
    year = models.IntegerField(verbose_name='Год')
    skill = models.CharField(max_length=255, verbose_name='Навык')
    count = models.IntegerField(verbose_name='Количество упоминаний')
    
    class Meta:
        unique_together = ('year', 'skill')