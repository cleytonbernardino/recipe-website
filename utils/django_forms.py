from re import compile

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
            'Password must have at least one Uppercase letter, '
            'one lowercase letter, and one number. The lenght should be '
            'at last 8 characters.'
        ),
            code='invalid'
        )
