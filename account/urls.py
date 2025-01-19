from django.urls import path
from .views import show_account_page_w_o_login, show_account_login_page


urlpatterns = [
    path('', show_account_page_w_o_login, name='account'),
    path('login/', show_account_login_page, name='login'),
    path('register/', show_account_page_w_o_login, name='register'),
]
