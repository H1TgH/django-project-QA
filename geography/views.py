from django.shortcuts import render
from .utils import save_salary_by_city_graph, sort_json, import_salary_by_city
import os
from django.conf import settings
from .models import GeographyPageSalary


def index(request):
    # sort_json('geography/salary_by_city.json')

    # save_salary_by_city_graph('geography/top_20_salaries.json')
    
    # path_to_salary_by_city = os.path.join(settings.BASE_DIR, 'geography', 'sorted.json')
    # import_salary_by_city(path_to_salary_by_city)

    average_salary_data = GeographyPageSalary.objects.order_by('-average_salary')[:20]

    average_salary_by_city = {}
    for stat in average_salary_data:
        average_salary_by_city[stat.city] = stat.average_salary

    return render(request, 'geography/geography.html', {
        'average_salary_by_city': average_salary_by_city,
    })