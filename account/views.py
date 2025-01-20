from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth import login


def show_account_page_w_o_login(request):
    return render(request, 'account/account-without-login.html')

def show_account_login_page(request):
    return render(request, 'account/login.html')

def show_account_register_page(request):
    if request.method == 'POST':
        return redirect('verify-code')
    return render(request, 'account/register.html')

def show_verify_code_page(request):
    return render(request, 'account/verify-code.html')

def create_user(request):
    pass
