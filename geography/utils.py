import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import json
from django.conf import settings
from demand.utils import get_currency_rate
from .models import GeographyPageSalary


CURRENCY_RATE = {'RUR': 1}

def calculate_average_salary_by_city(file_path, output_json_path):
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

    df['from'] = df['from'].fillna(df['to'])
    df['to'] = df['to'].fillna(df['from'])

    df = df[
        ((df['to'].isna()) | (df['to'] < 10_000_000)) &
        ((df['from'].isna()) | (df['from'] < 10_000_000))
        ]

    salary_by_city = df.groupby('area_name').agg({
        'from': 'mean',
        'to': 'mean'
    }).assign(avg_salary=lambda x: (x['from'] + x['to']) / 2)['avg_salary'].to_dict()

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(salary_by_city, f, ensure_ascii=False, indent=4)

    return salary_by_city

def sort_json(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    sorted_data = {city: int(salary) for city, salary in sorted_data}

    with open("sorted.json", "w", encoding="utf-8") as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)

    top_20_data = dict(list(sorted_data.items())[:20])
    with open("top_20_salaries.json", "w", encoding="utf-8") as file:
        json.dump(top_20_data, file, ensure_ascii=False, indent=4)

def save_salary_by_city_graph(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        salary_data = json.load(f)

    cities = list(map(str, salary_data.keys()))
    salaries = [round(salary) for salary in salary_data.values()]

    plt.figure(figsize=(10, len(salaries) * 0.5))
    plt.bar(cities, salaries, color='skyblue')

    plt.title('Топ-20 зарплат по городам', fontsize=14)
    plt.xlabel('Город', fontsize=10)
    plt.ylabel('Средняя зарплата (руб.)', fontsize=10)

    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.xticks(cities, rotation=45, ha='right', fontsize=6)
    plt.yticks(fontsize=8)

    plt.tight_layout()

    img_dir = os.path.join(settings.BASE_DIR, 'static', 'geography', 'img')
    file_path = os.path.join(img_dir, f'salary_by_city.png')
    plt.savefig(file_path, dpi=300)
    plt.close()

def import_salary_by_city(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for city, average_salary in data.items():
        GeographyPageSalary.objects.update_or_create(
            city=city,
            defaults={'average_salary': round(average_salary)}
        )
