from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')

def detail(request, user_pk):
    duser = User.objects.get(pk=user_pk)
    context = {
        'duser': duser,
    }
    return render(request, 'accounts/detail.html', context)

@login_required
def follow(request, user_pk):
    User = get_user_model()

    me = request.user
    you = User.objects.get(pk=user_pk)

    if me == you:
        return redirect('accounts:detail', user_pk)

    if you.followers.filter(pk=me.pk).exists():
        you.followers.remove(me)
    else:
        you.followers.add(me)

    return redirect('accounts:detail', user_pk)