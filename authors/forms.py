from re import compile

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_new_attr(field, attr_name, attr_new_value, overwrite=False):
    existing_attr = "" if overwrite else field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_value}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = str(placeholder_val)


def strong_password(password):
    regex = compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number. Ther length should be '
            'at least 8 characters'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['last_name'], 'You Last Name')
        add_placeholder(self.fields['username'], 'You Username')
        add_placeholder(self.fields['email'], 'Ex: email@example.com')

    password = forms.CharField(
        required=True,
        label='Create a new password.',
        validators=[strong_password],
        error_messages={
            'required': 'This field must be not empty',
        },
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your Password here'
        }),
    )

    password2 = forms.CharField(
        required=True,
        label='Confirm the Password',
        help_text='The password to confirm',
        error_messages={
            'required': 'This field must be not empty',
        },
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm the Password'
        }),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The E-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must be not empty',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your First Name here',
                'class': 'text-name'
            }),
        }

    # Era para funcionar mas por algum motivo não está
    def clean_username(self):
        data = self.cleaned_data.get("username")

        if data.lower() == 'admin':
            raise ValidationError(
                'Esse nome de usuario não é permitido',
                code='invalid',
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Confirm the password, it must be the same as the password',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
