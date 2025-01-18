from django.shortcuts import render
import requests
from datetime import datetime, timedelta
import re


def get_recent_vacancies(profession):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": profession,
        "date_from": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
        "per_page": 10,
        "order_by": "publication_time",
        "only_with_salary": True,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies_data = response.json()
        vacancies = []

        for vacancyIndex in range(min(10, len(vacancies_data["items"]))):
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

            vacancies.append({
                'title': title,
                'description': description,
                'skills': skills,
                'employer': employer,
                'salary': salary,
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

def index(request):
    vacancies = get_recent_vacancies('QA Engineer')
    reqq = vacancies[0]
    return render(request, 'vacancies/vacancies.html', reqq)
