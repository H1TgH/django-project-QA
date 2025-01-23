from django.shortcuts import render
from demand.models import DemandPageSalary, DemandPageVacanciesCount
from geography.models import GeographyPagePercentage, GeographyPageSalary
from skills.models import SkillStatistic


def index(request):
    average_salary_data = DemandPageSalary.objects.all().order_by('year')
    vacancies_count_data = DemandPageVacanciesCount.objects.all().order_by('year')

    average_salary = {}
    for stat in average_salary_data:
        average_salary[stat.year] = stat.average_salary

    vacancies_count = {}
    for stat in vacancies_count_data:
        vacancies_count[stat.year] = stat.vacancies_count

    average_salary_by_city_data = GeographyPageSalary.objects.order_by('-average_salary')[:20]

    average_salary_by_city = {}
    for stat in average_salary_by_city_data:
        average_salary_by_city[stat.city] = stat.average_salary

    percentage_data = GeographyPagePercentage.objects.order_by('-percentage')[:20]
    
    percentage_by_city = {}
    for stat in percentage_data:
        percentage_by_city[stat.city] = stat.percentage

    skills_data = SkillStatistic.objects.all().order_by('year')

    statistic = {}
    for stat in skills_data:
        if stat.year not in statistic:
            statistic[stat.year] = []
        statistic[stat.year].append(stat)

    graph_paths = {}
    for year in statistic.keys():
        graph_paths[year] = f"skills/img/skills-plot-{year}.png"

    return render(request, 'statistic/statistic.html', {
        'average_salary': average_salary,
        'vacancies_count': vacancies_count,
        'average_salary_by_city': average_salary_by_city,
        'percentage_by_city': percentage_by_city,
        'statistic': statistic,
        'graph_paths': graph_paths
    })
