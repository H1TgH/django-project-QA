from django.contrib import admin
from .models import MainPage


class MainPageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image_path')


admin.site.register(MainPage, MainPageAdmin)