from GdzieTeraz.models import KITCHEN, CITY


def get_choices(request):
    return {'KITCHEN': KITCHEN,
            'CITY': CITY}
