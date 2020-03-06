from django.http import JsonResponse
from django.views import View

from restaurant_app.models import Restaurant


class APIRestaurantView(View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        tables = restaurant.tables_set.all()
        free_tables = restaurant.tables_set.filter(taken=False)
        tables_count = len(tables)
        free_tables_count = len(free_tables)
        seats = 0
        free_seats = 0
        distance = 0
        if request.session.get('distance') is not None:
            distance = request.session.get('distance').get(str(pk))

        for table in free_tables:
            free_seats += table.size
        for table in tables:
            seats += table.size

        return JsonResponse({'kitchen': restaurant.get_kitchen_display(), 'address': restaurant.address,
                             'phone': restaurant.phone, 'free_tables': free_tables_count, 'tables': tables_count,
                             'free_seats': free_seats, 'seats': seats, 'distance': distance})
