from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', lambda request: redirect('home/')),
    path('home/', include('main.urls')),
    path('account/', include('account.urls')),
    path('statistic/', include('statistic.urls')),
    path('demand/', include('demand.urls')),
    path('geography/', include('geography.urls')),
    path('skills/', include('skills.urls')),
    path('vacancies/', include('vacancies.urls')),
]
