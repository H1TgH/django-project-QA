from django.urls import path
from .views import show_account_page, login_view, register
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', show_account_page, name='account'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
