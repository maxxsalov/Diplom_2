import random as r
import string

from faker import Faker


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(r.choice(letters) for i in range(length))
    return random_string


fake = Faker(locale="ru_RU")

