from django.db import models


class SkillStatistic(models.Model):
    year = models.IntegerField(verbose_name='Год')
    skill = models.CharField(max_length=255, verbose_name='Навык')
    count = models.IntegerField(verbose_name='Количество упоминаний')
    image_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='Путь к файлу с графиком', help_text='Путь указывать, как: static/skill/img/your_year.png')

    class Meta:
        unique_together = ('year', 'skill')