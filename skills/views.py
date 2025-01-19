from django.shortcuts import render
from .utils import data_analysis


def index(request):
    data_analysis('vacancies_2024.csv', 'QA', True)
    return render(request, 'skills/skills.html')
