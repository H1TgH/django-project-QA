from django.db import models


class MainPage(models.Model):
    description = models.TextField(verbose_name="Описание профессии")
    image_path = image_path = models.CharField(max_length=255, verbose_name="Путь к изображению", help_text="Путь к графику, сохранённому в папке static.")
    
    def __str__(self):
        return self.description
