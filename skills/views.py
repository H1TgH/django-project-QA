from django.shortcuts import render
from .utils import import_skills_from_json
import os
from django.conf import settings
from .models import SkillStatistic


def index(request):
    # json_file_path = os.path.join(settings.BASE_DIR, 'skills', 'skills_results.json')
    # import_skills_from_json(json_file_path)

    skills_data = SkillStatistic.objects.all().order_by('year')

    statistic = {}
    for stat in skills_data:
        if stat.year not in statistic:
            statistic[stat.year] = []
        statistic[stat.year].append(stat)

    graph_paths = {}
    for year in statistic.keys():
        graph_paths[year] = f"skills/img/skills-plot-{year}.png"

    return render(request, 'skills/skills.html', {
        'statistic': statistic,
        'graph_paths': graph_paths
    })
