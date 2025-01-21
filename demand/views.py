from django.shortcuts import render
from .utils import save_graph
import os
from django.conf import settings


def index(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'demand', 'average_salary.json')
    save_graph(json_file_path)
    return render(request, 'demand/demand.html')
