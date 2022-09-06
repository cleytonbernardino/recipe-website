from pprint import pprint
from random import randint

from faker import Faker

fake = Faker('pt-BR')


def radom_size():
    return randint(840, 900), randint(473, 573)


def make_recipe():
    return {
        'id': fake.random_number(digits=2, fix_len=True),
        'title': fake.sentence(nb_words=6),
        'description': fake.sentence(nb_words=12),
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        'preparation_time_unit': 'Minutos',
        'servings': fake.random_number(digits=1, fix_len=True),
        'servings_unit': 'Porcões',
        'praparation_steps': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'firt_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': fake.word(),
        'cover': 'https://loremflickr.com/%s/%s/food,cook' % radom_size(),
    }


if __name__ == '__main__':
    pprint(make_recipe())
