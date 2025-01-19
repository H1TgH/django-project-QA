from django.shortcuts import render


def show_account_page_w_o_login(request):
    return render(request, 'account/account-without-login.html')

def show_account_login_page(request):
    return render(request, 'account/login.html')
