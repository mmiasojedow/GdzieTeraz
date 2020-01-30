from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import *
from GdzieTeraz.forms import *
from GdzieTeraz.models import *
import secrets


# Create your views here.

# MAIN I LOGOWANIE

class MainView(View):
    def get(self, request):
        form = SearchForm()
        return render(request, 'GdzieTeraz/base.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            kitchen = form.cleaned_data['kitchen']
            name = form.cleaned_data['name']
            empty = 'Żadna restauracja nie spełnia wymagań'
            if kitchen == '0':
                restaurants = Restaurant.objects.filter(city=city, name__icontains=name)
            else:
                restaurants = Restaurant.objects.filter(city=city, kitchen=kitchen, name__icontains=name)
            free_restaurants = []
            for restaurant in restaurants:
                if len(restaurant.tables_set.filter(taken=False)) > 0:
                    free_restaurants.append(restaurant)
            return render(request, 'GdzieTeraz/base.html',
                          {'form': form, 'restaurants': free_restaurants, 'empty': empty})
        else:
            return render(request, 'GdzieTeraz/base.html', {'form': form})


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
                if user.is_superuser:
                    return redirect('main')
                else:
                    url = request.GET.get('next') if request.GET.get('next') is not None else 'profile'
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


class TokenGeneratorView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            bar = 'Link do rejestracji'
            return render(request, 'GdzieTeraz/token.html', {'bar': bar})
        else:
            return redirect("main")

    def post(self, request):
        token = secrets.token_hex(16)
        Token.objects.create(token=token)
        return render(request, 'GdzieTeraz/token.html', {'token': f"http://localhost:8000/add_restaurant/{token}"})


# RESTAURACJE

class RestaurantAddView(View):
    def get(self, request, token):
        t = Token.objects.get(token=token)
        if not t:
            return redirect('main')
        else:
            form = RestaurantAddForm()
            bar = 'Dołącz do naszej bazy restuaracji!'
            return render(request, 'GdzieTeraz/form.html', {'form': form, 'bar': bar})

    def post(self, request, token):
        t = Token.objects.get(token=token)
        if not t:
            return redirect('main')
        else:
            t.delete()
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
            Restaurant.objects.create(name=name, kitchen=kitchen, city=city, address=address,
                                      phone=phone, user=new_user)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
            return redirect("main")
        else:
            return render(request, 'GdzieTeraz/form.html', {'form': form, 'bar': bar})


class RestaurantProfileView(LoginRequiredMixin, View):
    def get(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        return render(request, 'GdzieTeraz/restaurant_profile.html', {'restaurant': restaurant})


class APIRestaurantView(LoginRequiredMixin, View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        tables = restaurant.tables_set.all()
        free_tables = restaurant.tables_set.filter(taken=False)
        tables_count = len(tables)
        free_tables_count = len(free_tables)
        seats = 0
        free_seats = 0

        for table in free_tables:
            free_seats += table.size
        for table in tables:
            seats += table.size

        if not request.user.is_superuser:
            return redirect("main")
        else:
            return JsonResponse({'kitchen': restaurant.get_kitchen_display(), 'address': restaurant.address,
                                 'city': restaurant.get_city_display(), 'phone': restaurant.phone,
                                 'free_tables': free_tables_count, 'tables': tables_count, 'free_seats': free_seats,
                                 'seats': seats})


# STOLIKI

class AddTableView(LoginRequiredMixin, View):
    def get(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        form = AddTableForm()
        bar = restaurant.name
        return render(request, 'GdzieTeraz/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})

    def post(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        form = AddTableForm(request.POST)
        bar = restaurant.name
        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            new_table = Tables.objects.create(restaurant=restaurant, name=name, size=size)
            bar = f"Dodano stolik o nazwie {new_table.name} dla {new_table.size} os."
            return render(request, 'GdzieTeraz/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})
        else:
            return render(request, 'GdzieTeraz/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})


class TablesView(LoginRequiredMixin, View):
    def get(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
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

    def post(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        tables = restaurant.tables_set.all()
        taken_tables = request.POST.getlist('tables')
        for table in tables:
            if str(table.pk) in taken_tables:
                table.taken = True
                table.save()
            else:
                table.taken = False
                table.save()
        return redirect("tables")
