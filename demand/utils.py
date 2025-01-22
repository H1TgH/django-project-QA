import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
import json
from django.conf import settings
from demand.models import DemandPageSalary
from demand.models import DemandPageVacanciesCount


CURRENCY_RATE = {'RUR': 1}

def get_currency_rate(currency_code):
    if currency_code not in CURRENCY_RATE:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = response.json()
        if currency_code == 'BYR':
            CURRENCY_RATE['BYN'] = data['Valute']['BYN']['Value']
            return data['Valute']['BYN']['Value']
        CURRENCY_RATE[currency_code] = data['Valute'][currency_code]['Value']
        return data['Valute'][currency_code]['Value']
    else:
        return CURRENCY_RATE[currency_code]


def calculate_average_salary(file_path):
    try:
        df = pd.read_csv(file_path,
                         parse_dates=['published_at'],
                         dtype={'key_skills': str},
                         quotechar='"',
                         skipinitialspace=True,
                         utc=True)
    except Exception:
        df = pd.read_csv(file_path,
                         dtype={'key_skills': str, 'published_at': str},
                         quotechar='"',
                         skipinitialspace=True)

        try:
            df['published_at'] = df['published_at'].apply(
                lambda x: pd.to_datetime(x, utc=True) if pd.notna(x) else pd.NaT
            )
        except Exception:
            return {}

    df = df.dropna(subset=['published_at'])

    df = df.dropna(subset=['salary_currency'])
    df = df.drop(columns=['key_skills'])
    df = df[df['name'].str.contains('тестировщик', case=False, na=False)]

    df['currency_rate'] = df['salary_currency'].apply(get_currency_rate)
    df['from'] = df['salary_from'] * df['currency_rate']
    df['to'] = df['salary_to'] * df['currency_rate']

    df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

    df = df[
        ((df['to'].isna()) | (df['to'] < 10_000_000)) &
        ((df['from'].isna()) | (df['from'] < 10_000_000))
        ]

    try:
        df['year'] = df['published_at'].dt.year
    except Exception:
        return {}

    salary_by_year = df.groupby('year').agg({
        'from': 'mean',
        'to': 'mean'
    }).assign(avg_salary=lambda x: (x['from'] + x['to']) / 2)['avg_salary'].to_dict()

    return salary_by_year

def vacancies_count_by_year(file_path, output_json_path):
    df = pd.read_csv(file_path, quotechar='"', skipinitialspace=True, dtype={'key_skills': str})

    df = df.dropna(subset=['published_at'])

    df = df[df['name'].str.contains('тестировщик', case=False, na=False)]

    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)

    df = df.dropna(subset=['published_at'])

    df['year'] = pd.to_datetime(df['published_at']).dt.year

    vacancies_by_year = df.groupby('year').size().to_dict()

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(vacancies_by_year, f, ensure_ascii=False, indent=4)

    return vacancies_by_year

def save_salary_graph(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        salary_data = json.load(f)

    years = list(map(int, salary_data.keys()))
    salaries = [round(salary) for salary in salary_data.values()]

    plt.figure(figsize=(10, len(salaries) * 0.5))
    plt.bar(years, salaries, color='skyblue')

    plt.title('Динамика уровня зарплат тестировщика по годам', fontsize=14)
    plt.xlabel('Год', fontsize=10)
    plt.ylabel('Средняя зарплата (руб.)', fontsize=10)

    plt.xticks(years, fontsize=8)
    plt.yticks(fontsize=8)

    plt.tight_layout()

    img_dir = os.path.join(settings.BASE_DIR, 'static', 'demand', 'img')
    file_path = os.path.join(img_dir, f'avg-salaries.png')
    plt.savefig(file_path, dpi=300)
    plt.close()

def save_vacancies_count_graph(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        vacancies_count_data = json.load(f)

    years = list(map(int, vacancies_count_data.keys()))
    vacancies_count = [salary for salary in vacancies_count_data.values()]

    plt.figure(figsize=(10, len(vacancies_count) * 0.5))
    plt.bar(years, vacancies_count, color='skyblue')

    plt.title('Количество вакансий по годам', fontsize=14)
    plt.xlabel('Год', fontsize=10)
    plt.ylabel('Количество вакансий', fontsize=10)

    plt.xticks(years, fontsize=8)
    plt.yticks(fontsize=8)

    plt.tight_layout()

    img_dir = os.path.join(settings.BASE_DIR, 'static', 'demand', 'img')
    file_path = os.path.join(img_dir, f'vacancies-count.png')
    plt.savefig(file_path, dpi=300)
    plt.close()

def import_average_salary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for year, average_salary in data.items():
        rounded_salary = int(round(average_salary))
        
        DemandPageSalary.objects.update_or_create(
            year=year, 
            defaults={'average_salary': rounded_salary}
        )

def import_vacancies_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for year, vacancies_count in data.items():
        DemandPageVacanciesCount.objects.update_or_create(
            year=year, 
            defaults={'vacancies_count': vacancies_count}
        )