
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)  # автоматически авторизуем
        return redirect('home')  # или куда хочешь
    return render(request, 'users/register.html', {'form': form})

class MyLogin(LoginView):
    form_class=AuthenticationForm
    template_name='users/login.html'

