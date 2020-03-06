from django.shortcuts import render
from django.views import View

from main_app.forms import SearchForm

from geopy.geocoders import Nominatim
from geopy import distance
from geopy.exc import GeocoderTimedOut

from restaurant_app.models import Restaurant

geolocator = Nominatim(user_agent="gdzie_teraz", format_string="%s, Warsaw, Poland")


class MainView(View):
    def get(self, request):
        form = SearchForm()
        return render(request, 'main_app/base.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            kitchen = form.cleaned_data['kitchen']
            name = form.cleaned_data['name']
            chosen_distance = form.cleaned_data['distance']
            address = form.cleaned_data['address']
            empty = 'Żadna restauracja nie spełnia wymagań'

            # getting user location
            try:
                user_localization = geolocator.geocode(address)
            except GeocoderTimedOut:
                ups = 'Ups! Coś poszło nie tak...'
                return render(request, 'main_app/base.html',
                              {'form': form, 'empty': ups})
            user_latitude = user_localization.latitude
            user_longitude = user_localization.longitude
            user = (user_latitude, user_longitude)

            # selection based on kitchen and name
            if kitchen == '0':
                restaurants = Restaurant.objects.filter(name__icontains=name)
            else:
                restaurants = Restaurant.objects.filter(kitchen=kitchen, name__icontains=name)

            # selection based on free tables
            free_restaurants = []
            for restaurant in restaurants:
                if len(restaurant.tables_set.filter(taken=False)) > 0:
                    free_restaurants.append(restaurant)

            # selection based on distance
            request.session['distance'] = {}
            near_restaurants = []
            for restaurant in free_restaurants:
                rest_loc = (restaurant.latitude, restaurant.longitude)
                dist = (round(distance.distance(user, rest_loc).km, 2))
                if dist <= int(chosen_distance):
                    request.session['distance'][str(restaurant.pk)] = dist
                    near_restaurants.append([restaurant.pk, restaurant.name, dist])

            near_restaurants.sort(key=lambda x: x[2])  # sorting based on distance
            return render(request, 'main_app/base.html',
                          {'form': form, 'restaurants': near_restaurants, 'empty': empty})
        else:
            return render(request, 'main_app/base.html', {'form': form})
