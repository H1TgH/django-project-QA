import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
import json
from django.conf import settings


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


def csv_reader(file_path):
    try:
        data = pd.read_csv(file_path,
                           parse_dates=['published_at'],
                           dtype={'key_skills': str},
                           quotechar='"',
                           skipinitialspace=True,
                           utc=True)
    except Exception:
        data = pd.read_csv(file_path,
                           dtype={'key_skills': str, 'published_at': str},
                           quotechar='"',
                           skipinitialspace=True)

        try:
            data['published_at'] = data['published_at'].apply(
                lambda x: pd.to_datetime(x, utc=True) if pd.notna(x) else pd.NaT
            )
        except Exception:
            return {}

    data = data.dropna(subset=['published_at'])

    data = data.dropna(subset=['salary_currency'])
    data = data.drop(columns=['key_skills'])
    data = data[data['name'].str.contains('тестировщик', case=False, na=False)]

    data['currency_rate'] = data['salary_currency'].apply(get_currency_rate)
    data['from'] = data['salary_from'] * data['currency_rate']
    data['to'] = data['salary_to'] * data['currency_rate']

    data = data.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

    data = data[
        ((data['to'].isna()) | (data['to'] < 10_000_000)) &
        ((data['from'].isna()) | (data['from'] < 10_000_000))
        ]

    try:
        data['year'] = data['published_at'].dt.year
    except Exception:
        return {}

    salary_by_year = data.groupby('year').agg({
        'from': 'mean',
        'to': 'mean'
    }).assign(avg_salary=lambda x: (x['from'] + x['to']) / 2)['avg_salary'].to_dict()

    return salary_by_year

def save_graph(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        salary_data = json.load(f)

    years = list(map(int, salary_data.keys()))
    salaries = [round(salary) for salary in salary_data.values()]

    plt.figure(figsize=(10, len(salaries) * 0.5))
    plt.bar(years, salaries, color='skyblue')
    
    plt.title('Динамика уровня зарплат тестировщика по годам', fontsize=14)
    plt.xlabel('Год', fontsize=10)
    plt.ylabel('Средняя зарплата (руб.)', fontsize=10)
    
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    plt.tight_layout()

    img_dir = os.path.join(settings.BASE_DIR, 'static', 'demand', 'img')
    os.makedirs(img_dir, exist_ok=True)
    file_path = os.path.join(img_dir, f'avg-salaries.png')
    plt.savefig(file_path, dpi=300)
    plt.close()

