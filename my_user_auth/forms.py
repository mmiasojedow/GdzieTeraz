from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit

from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=120)
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                'login',
                'password',
                css_class='form_width'
            ),
            Submit('submit', 'Zaloguj się', css_class='btn btn-info')
        )
