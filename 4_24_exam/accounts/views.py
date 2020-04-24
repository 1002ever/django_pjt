# 각 문제를 해결하기 위하여 필요한 import문은 이곳에 작성합니다.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'accounts/index.html')

# POST방식과 GET방식 분기 처리하여, form을 각자 다르게 처리 후 페이지 표현
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

# signup과 동일한 논리, form.html을 공유, AuthenticationForm을 사용한다는 점만 다름
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

# login이 필요하다는 점을 적용
@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')