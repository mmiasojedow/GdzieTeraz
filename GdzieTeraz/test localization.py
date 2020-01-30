from geopy.geocoders import Nominatim
from geopy import distance

geolocator = Nominatim(user_agent="specify_your_app_name_here", format_string="%s, Warsaw, Poland")
polna = geolocator.geocode("Polna 3")
print(polna.address)
print(polna.raw)
print(polna.latitude)
print(polna.longitude)

prosta = geolocator.geocode('Prosta 51')
print(prosta.address)
pol = (polna.latitude, polna.longitude)
pro = (prosta.latitude, prosta.longitude)

print(round(distance.distance(pol, pro).km, 2))
print(distance.distance(pol, pro).miles)