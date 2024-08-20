from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _

from utils.django_forms import add_placeholder


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], _('Type you username'))
        add_placeholder(self.fields['password'], _('Type you password'))

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def get_user(self):
        return authenticate(
            username=self.cleaned_data.get('username', ''),
            password=self.cleaned_data.get('password', '')
        )

    def login(self, request) -> bool:
        user = self.get_user()
        if user is None:
            return False
        login(request, user)
        return True
