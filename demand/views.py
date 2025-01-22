from django.shortcuts import render
from .utils import save_graph
import os
from django.conf import settings


def index(request):
    return render(request, 'demand/demand.html')
