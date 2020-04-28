from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model


def signup(request):
    if request.method == 'POST':
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
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def profile(request, username):
    User = get_user_model()
    profile_user = User.objects.get(username=username)

    context = {
        'profile_user': profile_user,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, username):
    User = get_user_model()

    me = request.user
    you = User.objects.get(username=username)

    if me == you:
        return redirect('accounts:profile', username)

    # if you.followers.filter(pk=me.pk).exists(): 쿼리 처리, 더 빠름
    # if me.followings.filter(pk=you.pk).exists(): 위와 동일, 기준점이 다를 뿐
    if me in you.followers.all():
        you.followers.remove(me)
    else:
        you.followers.add(me)

    return redirect('accounts:profile', username)