from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils import django_forms as ult


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ult.add_placeholder(
            self.fields['first_name'], 'Type your First Name here')
        ult.add_placeholder(self.fields['last_name'], 'You Last Name')
        ult.add_placeholder(self.fields['username'], 'You Username')
        ult.add_placeholder(self.fields['email'], 'Ex: email@example.com')

    first_name = forms.CharField(
        label='First Name',
        error_messages={
            'required': 'Write your first name',
        }
    )

    last_name = forms.CharField(
        label='Last Name',
        error_messages={
            'required': 'Write your last name'
        }
    )

    username = forms.CharField(
        min_length=4,
        max_length=50,
        label='Username',
        help_text='Create you username',
        error_messages={
            'required': 'This field must be not empty',
            'min_length': 'Username must have at last 4 characters',
            'max_length': 'User character limit is 50',
        },
    )

    email = forms.EmailField(
        label='E-mail',
        help_text='The E-mail must be valid.',
        error_messages={
            'required': 'Email is required'
        },
    )

    password = forms.CharField(
        label='Create a new password.',
        validators=[ult.strong_password],
        help_text=(
            'Password must have at least one Uppercase letter, '
            'one lowercase letter, and one number. The leght should be '
            'at last 8 caracters.'
        ),
        error_messages={
            'required': 'This field must be not empty',
        },
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your Password here'
        }),
    )

    password2 = forms.CharField(
        label='Confirm the Password',
        help_text='The password to confirm',
        error_messages={
            'required': 'Please repeat you password',
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        try:
            User.objects.get(email=email)
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )
        except User.DoesNotExist:
            return email

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
