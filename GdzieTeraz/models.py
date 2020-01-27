from django.db import models

# Create your models here.
KITCHEN = (
    (1, 'Amerykańska'),
    (2, 'Azjatycka'),
    (3, 'Europejska'),
    (4, 'Indyjska'),
    (5, 'Pizza'),
    (6, 'Polska'),
    (7, 'Śródziemnomorska'),
    (8, 'Wegetariańska'),
)

CITY = (
    (1, 'Warszawa'),
    (2, 'Trójmiasto'),
    (3, 'Wrocław'),
)

SIZES = (
    (2, 2),
    (4, 4),
    (6, 6),
    (8, 8),
)


class Restaurant(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa')
    kitchen = models.IntegerField(choices=KITCHEN, verbose_name='Kuchania')
    city = models.IntegerField(choices=CITY, verbose_name='Miasto')
    address = models.CharField(max_length=128, verbose_name='Adres')
    phone = models.IntegerField(verbose_name='Telefon')
    www = models.URLField(verbose_name='Strona')


class Tables(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    size = models.IntegerField(choices=SIZES, verbose_name='Wielkość')
    taken = models.BooleanField(default=False, verbose_name='Zajęty')
