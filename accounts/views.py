from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.views import (LoginView as AuthLoginView,
                                         LogoutView, logout_then_login,
                                       PasswordChangeView as AuthPasswordChangeView)
from django.urls import reverse_lazy

from .forms import SignupForm, ProfileForm, PasswordChangeForm

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

class LoginView(AuthLoginView):
    template_name = 'accounts/login_form.html'
    next_page = 'root'

    def form_valid(self, form):
        messages.success(self.request, '로그인 하였습니다.')
        return super().form_valid(form)

login = LoginView.as_view()

def logout(request):
    messages.success(request, '로그아웃 하였습니다.')
    return logout_then_login(request)


@login_required
def profile_edit(request):
    if request.method =='POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 수정하였습니다.')
            return redirect('accounts:profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit_form.html', {
    'form':form
    })


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('root')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, '비밀번호를 변경하였습니다.')
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()

@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    
    # 팔로우 기능 구현
    request.user.following_set.add(follow_user)

    messages.success(request, f"{follow_user}님을 팔로우했습니다.")
    redirect_url = request.META.get('HTTP_REFERR', 'root')
    return redirect(redirect_url)

@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(get_user_model(), username=username, is_active=True)

    # 언팔로우 기능 구현
    request.user.following_set.remove(unfollow_user)

    messages.success(request, f"{unfollow_user}님을 언팔로우했습니다.")
    redirect_url = request.META.get('HTTP_REFERR', 'root')
    return redirect(redirect_url)