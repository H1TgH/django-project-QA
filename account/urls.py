from django.urls import path
from .views import show_account_page_w_o_login, login, register, verify_code


urlpatterns = [
    path('', show_account_page_w_o_login, name='account'),
    path('login/', login, name='login'),
    path('verify-code', verify_code, name='verify-code'),
    path('register/', register, name='register'),
]
