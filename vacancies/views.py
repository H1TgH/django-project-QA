from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from .models import VacanciesPage


def get_recent_vacancies(profession):
    vacancies_count = VacanciesPage.objects.first().vacancies_count
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": profession,
        "date_from": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
        "per_page": vacancies_count,
        "order_by": "publication_time",
        "only_with_salary": True,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies_data = response.json()
        vacancies = []

        for vacancyIndex in range(min(vacancies_count, len(vacancies_data["items"]))):
            vacancy = vacancies_data["items"][vacancyIndex]
            id = vacancy.get('id')
            title = vacancy.get('name', 'Нет данных')
            employer = vacancy.get('employer', {}).get('name', 'Нет данных')
            salary = vacancy.get('salary')
            area = vacancy.get('area', {}).get('name', 'Нет данных')
            published_at = vacancy.get('published_at', 'Нет данных')
            details = get_vacancy_details(id)
            description = details.get('description', 'Нет данных') if details else 'Нет данных'
            skills = details.get('key_skills', 'Нет данных') if details else 'Нет данных'

            skills_string = ''
            for skillIndex in range(len(skills)):
                if skillIndex != len(skills) - 1:
                    skills_string = skills_string + skills[skillIndex].get('name') + ', '
                else:
                    skills_string += skills[skillIndex].get('name')

            salary_string = ''
            salary_currency = salary.get('currency')

            currency_rate = get_currency_rate(salary_currency)

            if salary.get('from') is not None:
                if currency_rate:
                    salary_string += f'Зарплата от: {salary.get("from") * currency_rate:.2f} руб.'
                else:
                    salary_string += f'Зарплата от: {salary.get("from")} {salary_currency}'

            if salary.get('to') is not None:
                if salary_string:
                    salary_string += ' '
                else: 
                    salary_string += 'Зарплата до: '

                if currency_rate:
                    salary_string += f'{salary.get("to") * currency_rate:.2f} руб.'
                else:
                    salary_string += f'{salary.get("to")} {salary_currency}'

            if salary.get('gross', False):
                salary_string += ' после вычета налогов'
            else:
                salary_string += ' до вычета налогов'

                time_in_new_format = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z')
                published_at = time_in_new_format.strftime('%Y-%m-%d %H:%M:%S')
            
            vacancies.append({
                'title': title,
                'description': description,
                'skills': skills_string,
                'employer': employer,
                'salary': salary_string,
                'area': area,
                'published_at': published_at
            })

        return vacancies

    return []

def get_vacancy_details(vacancy_id):
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_currency_rate(currency_code):
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()

    if currency_code in data['Valute']:
        rate = data['Valute'][currency_code]['Value']
        return rate
    return None

def index(request):
    vacancies = get_recent_vacancies('QA Engineer')
    dictionary = {
        'vacancies': vacancies
    }
    return render(request, 'vacancies/vacancies.html', dictionary)
