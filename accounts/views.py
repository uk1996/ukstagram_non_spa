from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'ukstagram에 오신걸 환영합니다!')
            return redirect('root')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form':form,
    })