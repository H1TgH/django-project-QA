from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages

User = get_user_model()

def show_account_page_w_o_login(request):
    return render(request, 'account/account-without-login.html')

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

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизованы!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный email или пароль.')

    return render(request, 'account/login.html')

