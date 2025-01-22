from django.shortcuts import render
from .utils import save_salary_graph, vacancies_count_by_year
import os
from django.conf import settings


def index(request):
    # vacancies_count_by_year('vacancies_2024.csv', 'demand/vacancies_count_by_year')
    
    return render(request, 'demand/demand.html')
