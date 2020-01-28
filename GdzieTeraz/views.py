from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import *

from GdzieTeraz.forms import *
from GdzieTeraz.models import *


# Create your views here.

# MAIN I LOGOWANIE

class MainView(View):
    def get(self, request):
        return render(request, 'GdzieTeraz/base.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        bar = 'Logowanie'
        return render(request, 'GdzieTeraz/form.html', {'form': form, 'bar': bar})

    def post(self, request):
        form = LoginForm(request.POST)
        bar = 'Logowanie'
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.GET.get('next') if request.GET.get('next') is not None else 'main'
                return redirect(url)
            else:
                return render(request, 'GdzieTeraz/form.html',
                              {'form': form, 'message': 'Błędny login lub hasło', 'bar': bar})
        else:
            return render(request, 'GdzieTeraz/form.html', {'form': form, 'bar': bar})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


# RESTAURACJE

class RestaurantAddView(View):
    def get(self, request):
        form = RestaurantAddForm()
        bar = 'Dołącz do naszej bazy restuaracji!'
        return render(request, 'GdzieTeraz/form.html', {'form': form, 'bar': bar})

    def post(self, request):
        form = RestaurantAddForm(request.POST)
        bar = 'Dołącz do naszej bazy restuaracji!'
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            mail = form.cleaned_data['mail']
            name = form.cleaned_data['name']
            kitchen = form.cleaned_data['kitchen']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            new_user = User.objects.create_user(username, mail, password)
            new_restaurant = Restaurant.objects.create(name=name, kitchen=kitchen, city=city, address=address,
                                                       phone=phone, user=new_user)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile", pk=new_restaurant.pk)
            return redirect("main")
        else:
            return render(request, 'GdzieTeraz/form.html', {'form': form, 'bar': bar})


class RestaurantProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        return render(request, 'GdzieTeraz/restaurant_profile.html', {'restaurant': restaurant})


class RestaurantDetailsView(DetailView):
    model = Restaurant
    template_name = 'GdzieTeraz/restaurant_details.html'


# STOLIKI

class AddTableView(View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        form = AddTableForm()
        bar = restaurant.name
        return render(request, 'GdzieTeraz/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        form = AddTableForm(request.POST)
        bar = restaurant.name
        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            new_table = Tables.objects.create(restaurant_id=pk, name=name, size=size)
            bar = f"Dodano stolik o nazwie {new_table.name} dla {new_table.size} os."
            return render(request, 'GdzieTeraz/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})
        else:
            return render(request, 'GdzieTeraz/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})


class TablesView(View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        tables = restaurant.tables_set.all()
        seats = 0
        free_seats = 0
        free_tables = restaurant.tables_set.filter(taken=False)
        for table in free_tables:
            free_seats += table.size
        for table in tables:
            seats += table.size
        return render(request, 'GdzieTeraz/tables.html',
                      {'restaurant': restaurant, 'tables': tables, 'seats': seats, 'free_seats': free_seats,
                       'free_tables': free_tables})

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        tables = restaurant.tables_set.all()
        taken_tables = request.POST.getlist('tables')
        for table in tables:
            if str(table.pk) in taken_tables:
                table.taken = True
                table.save()
            else:
                table.taken = False
                table.save()

        return redirect("tables", pk=restaurant.pk)
