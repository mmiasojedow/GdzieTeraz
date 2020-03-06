from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from geopy.exc import GeocoderTimedOut

from main_app.views import geolocator
from my_user_auth.models import Token
from restaurant_app.forms import RestaurantAddForm, AddTableForm
from restaurant_app.models import Restaurant, Tables


class RestaurantAddView(View):
    def get(self, request, token):
        t = Token.objects.get(token=token)
        if not t:
            return redirect('main')
        else:
            form = RestaurantAddForm()
            bar = 'Dołącz do naszej bazy restuaracji!'
            return render(request, 'main_app/form.html', {'form': form, 'bar': bar})

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
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']

            new_user = User.objects.create_user(username, mail, password)
            Restaurant.objects.create(name=name, kitchen=kitchen, address=address, phone=phone, user=new_user)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
            return redirect("main")
        else:
            return render(request, 'main_app/form.html', {'form': form, 'bar': bar})


class RestaurantProfileView(LoginRequiredMixin, View):
    def get(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        return render(request, 'restaurant_app/restaurant_profile.html', {'restaurant': restaurant})

    def post(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        try:
            localization = geolocator.geocode(restaurant.address)
        except GeocoderTimedOut as e:
            ups = 'Ups! Coś poszło nie tak...'
            return render(request, 'restaurant_app/restaurant_profile.html', {'error': ups, 'restaurant': restaurant})
        latitude = localization.latitude
        longitude = localization.longitude
        restaurant.latitude = latitude
        restaurant.longitude = longitude
        restaurant.save()
        return render(request, 'restaurant_app/restaurant_profile.html', {'restaurant': restaurant})


# STOLIKI

class AddTableView(LoginRequiredMixin, View):
    def get(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        form = AddTableForm()
        bar = restaurant.name
        return render(request, 'main_app/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})

    def post(self, request):
        restaurant = Restaurant.objects.get(user=request.user)
        form = AddTableForm(request.POST)
        bar = restaurant.name
        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            new_table = Tables.objects.create(restaurant=restaurant, name=name, size=size)
            bar = f"Dodano stolik o nazwie {new_table.name} dla {new_table.size} os."
            return render(request, 'main_app/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})
        else:
            return render(request, 'main_app/form.html', {'restaurant': restaurant, 'form': form, 'bar': bar})


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
        return render(request, 'restaurant_app/tables.html',
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
