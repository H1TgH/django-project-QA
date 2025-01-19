from django.shortcuts import render
from .models import MainPage

def index(request):
    profession_info = MainPage.objects.first()
    return render(request, 'main/index.html', {'profession_info': profession_info})
