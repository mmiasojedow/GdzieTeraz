from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from restaurant_app.models import KITCHEN, SIZES


def login_validator(value):
    taken_logins = User.objects.filter(username=value)
    if taken_logins:
        raise ValidationError('Login jest zajęty')


def kitchen_validator(value):
    if value == '0':
        raise ValidationError('Wybierz rodzaj kuchni')


class RestaurantAddForm(forms.Form):
    login = forms.CharField(label='Login', validators=[login_validator])
    mail = forms.EmailField(label='Email', error_messages={'invalid': "Nieprawidłowy adres Email"})
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)
    name = forms.CharField(label='Nazwa restauracji')
    kitchen = forms.ChoiceField(choices=KITCHEN, label='Kuchania', validators=[kitchen_validator])
    address = forms.CharField(max_length=128, label='Adres')
    phone = forms.IntegerField(label='Telefon')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Hasła nie są identyczne')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('login', css_class='form-group col-md-6 mb-0'),
                Column('mail', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('kitchen', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Dołącz', css_class='btn btn-info')
        )


class AddTableForm(forms.Form):
    name = forms.CharField(max_length=64, label='Nazwa')
    size = forms.ChoiceField(choices=SIZES, label='Wielkość')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                'name',
                'size',
                css_class='form_width'
            ),
            Submit('submit', 'Dodaj stolik', css_class='btn btn-info'),
        )
