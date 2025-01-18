from django.shortcuts import render


def index(request):
    return render(request, 'geography/geography.html')
