from django import forms
from restaurant_app.models import KITCHEN

DISTANCE = (
    (1, '1 km'),
    (3, '3 km'),
    (5, '5 km'),
    (10, '10 km'),
)


class SearchForm(forms.Form):
    kitchen = forms.ChoiceField(choices=KITCHEN, required=False,
                                widget=forms.Select(attrs={'class': "custom-select mr-sm-2"}))
    name = forms.CharField(max_length=128, label='Nazwa', required=False,
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Nazwa restauracji', 'class': "form-control mr-sm-2"}))
    address = forms.CharField(max_length=128, label='Adres', required=True,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Twój adres', 'class': "form-control mr-sm-2"}))
    distance = forms.ChoiceField(choices=DISTANCE, label='Promień', required=True,
                                 widget=forms.Select(attrs={'class': "custom-select mr-sm-2"}))
