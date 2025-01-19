from django.shortcuts import render


def show_account_page_w_o_login(request):
    return render(request, 'account/account-without-login.html')
