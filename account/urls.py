from django.urls import path
from .views import show_account_page_w_o_login, login_view, register


urlpatterns = [
    path('', show_account_page_w_o_login, name='account'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
]
