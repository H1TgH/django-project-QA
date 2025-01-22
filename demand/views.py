from django.shortcuts import render
from .utils import save_salary_graph, vacancies_count_by_year, save_vacancies_count_graph, import_average_salary, import_vacancies_count
import os
from django.conf import settings
from .models import DemandPageSalary, DemandPageVacanciesCount


def index(request):
    # vacancies_count_by_year('vacancies_2024.csv', 'demand/vacancies_count_by_year.json')
     
    # path_to_average_salary = os.path.join(settings.BASE_DIR, 'demand', 'average_salary.json')
    # import_average_salary(path_to_average_salary)

    # path_to_vacancies_count = os.path.join(settings.BASE_DIR, 'demand', 'vacancies_count_by_year.json')
    # import_vacancies_count(path_to_vacancies_count)

    # save_vacancies_count_graph('demand/vacancies_count_by_year.json')
    # save_salary_graph('demand/average_salary.json')
    
    average_salary_data = DemandPageSalary.objects.all().order_by('year')
    vacancies_count_data = DemandPageVacanciesCount.objects.all().order_by('year')

    average_salary = {}
    for stat in average_salary_data:
        average_salary[stat.year] = stat.average_salary

    vacancies_count = {}
    for stat in vacancies_count_data:
        vacancies_count[stat.year] = stat.vacancies_count

    return render(request, 'demand/demand.html', {
        'average_salary': average_salary,
        'vacancies_count': vacancies_count,
    })
