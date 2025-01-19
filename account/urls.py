from django.urls import path
from .views import show_account_page_w_o_login


urlpatterns = [
    path('', show_account_page_w_o_login, name='account'),
    path('register/', show_account_page_w_o_login, name='register'),
    path('login/', show_account_page_w_o_login, name='login'),
]
