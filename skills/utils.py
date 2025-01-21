import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter
from django.conf import settings
import json
from .models import SkillStatistic


def data_analysis(file_path, profession, output_json_path, is_need_plot):
    df = pd.read_csv(file_path, quotechar='"', skipinitialspace=True, dtype={'key_skills': str})

    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)

    df = df.dropna(subset=['published_at'])

    df['key_skills'] = df['key_skills'].str.replace(r'\n', ',', regex=True)

    df = df[df['name'].str.contains(profession, case=False, na=False)]

    df = df.dropna(subset=['key_skills'])

    df['year'] = df['published_at'].dt.year

    results = {}

    for year, group in df.groupby('year'):
        all_skills = group['key_skills'].str.cat(sep=',')

        skills = [skill.strip() for skill in all_skills.split(',')]

        skill_counts = Counter(skills)

        top_skills = skill_counts.most_common(20)
        results[year] = top_skills

        if top_skills and is_need_plot:
            save_graph(year, top_skills)
        
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

    return results

def save_graph(year, top_skills):
    skills, counts = zip(*top_skills)

    unique_skills = [f"{i} ({skill})" if counts.count(skill) > 1 else skill for i, skill in enumerate(skills)]

    plt.figure(figsize=(10, len(skills) * 0.5))
    plt.barh(unique_skills, counts, color='skyblue')
    plt.xlabel('Частота использования', fontsize=10)
    plt.ylabel('Навыки', fontsize=10)
    plt.title(f'ТОП-20 навыков за {year}', fontsize=12)

    plt.gca().invert_yaxis()
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.tight_layout()

    img_dir = os.path.join(settings.BASE_DIR, 'static', 'skills', 'img')
    os.makedirs(img_dir, exist_ok=True)
    file_path = os.path.join(img_dir, f'skills-plot-{year}.png')
    plt.savefig(file_path, dpi=300)
    plt.close()

def import_skills_from_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for year, skills in data.items():
            if isinstance(skills, list):
                for skill_data in skills:
                    if isinstance(skill_data, list) and len(skill_data) == 2:
                        skill = skill_data[0]
                        count = skill_data[1]
                        if skill and count is not None:
                            SkillStatistic.objects.update_or_create(
                                year=year,
                                skill=skill,
                                defaults={'count': count}
                            )
    except Exception as e:
        print(f"Ошибка при обработке JSON: {e}")