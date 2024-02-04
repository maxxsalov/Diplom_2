import requests

from constants import BASE_URL, REGISTER_USER
from helpers import generate_random_string, fake


def register_new_user_and_return_login_password():
    login_pass = []

    email = fake.email()
    password = generate_random_string(10)
    name = fake.name()

    body = {
        "email": email,
        "password": password,
        "name": name
    }

    response = \
        requests.post(
            f'{BASE_URL}{REGISTER_USER}',
            data=body)

    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(name)

    return login_pass, response
