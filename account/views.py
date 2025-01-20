from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def show_account_page_w_o_login(request):
    return render(request, 'account/account-without-login.html')

def login_view(request):
    return render(request, 'account/login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('register')

        user = User.objects.create_user(email=email, username=username, password=password)
        user.is_active = True
        user.save()

        login(request, user)
        messages.success(request, 'Вы успешно зарегистрированы и авторизованы!')
        return redirect('home')

    return render(request, 'account/register.html')

def verify_code(request):
    return render(request, 'account/verify-code.html')
