from django.shortcuts import render
from .utils import calculate_vacancy_percentage_by_city, save_salary_by_city_graph, save_vacancies_percentage_by_city_graph, sort_json_salaries, sort_json_percentage, import_salary_by_city, import_percent_by_city
import os
from django.conf import settings
from .models import GeographyPageSalary, GeographyPagePercentage


def index(request):
    # calculate_vacancy_percentage_by_city('vacancies_2024.csv', 'percentage_vacancies_by_city.json')

    # sort_json_salaries('geography/salary_by_city.json')
    # sort_json_percentage('geography/percentage_vacancies_by_city.json')

    # save_salary_by_city_graph('geography/top_20_salaries.json')
    # save_vacancies_percentage_by_city_graph('geography/top_20_percentage.json')
    
    # path_to_salary_by_city = os.path.join(settings.BASE_DIR, 'geography', 'sorted-salaries.json')
    # import_salary_by_city(path_to_salary_by_city)
    # path_to_salary_by_city = os.path.join(settings.BASE_DIR, 'geography', 'sorted-percentage.json')
    # import_percent_by_city(path_to_salary_by_city)

    average_salary_by_city_data = GeographyPageSalary.objects.order_by('-average_salary')[:20]

    average_salary_by_city = {}
    for stat in average_salary_by_city_data:
        average_salary_by_city[stat.city] = stat.average_salary

    percentage_data = GeographyPagePercentage.objects.order_by('-percentage')[:20]
    
    percentage_by_city = {}
    for stat in percentage_data:
        percentage_by_city[stat.city] = stat.percentage

    return render(request, 'geography/geography.html', {
        'average_salary_by_city': average_salary_by_city,
        'percentage_by_city': percentage_by_city,
    })