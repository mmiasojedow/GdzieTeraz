import secrets

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.views import View

from my_user_auth.forms import LoginForm
from my_user_auth.models import Token


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        bar = 'Logowanie'
        return render(request, 'main_app/form.html', {'form': form, 'bar': bar})

    def post(self, request):
        form = LoginForm(request.POST)
        bar = 'Logowanie'
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('main')
                else:
                    url = request.GET.get('next') if request.GET.get('next') is not None else 'profile'
                    return redirect(url)
            else:
                return render(request, 'main_app/form.html',
                              {'form': form, 'message': 'Błędny login lub hasło', 'bar': bar})
        else:
            return render(request, 'main_app/form.html', {'form': form, 'bar': bar})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


class TokenGeneratorView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            bar = 'Link do rejestracji'
            return render(request, 'my_user_auth/token.html', {'bar': bar})
        else:
            return redirect("main")

    def post(self, request):
        token = secrets.token_hex(16)
        Token.objects.create(token=token)
        return render(request, 'my_user_auth/token.html', {'token': f"http://localhost:8000/add_restaurant/{token}"})
