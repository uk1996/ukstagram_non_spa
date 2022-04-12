from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, 'ukstagram에 오신걸 환영합니다!')
            return redirect('root')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form':form,
    })

login = LoginView.as_view(template_name='accounts/login_form.html')

def logout(request):
    messages.success(request, '로그아웃 되었습니다.')
    return logout_then_login(request)
