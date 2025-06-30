import string
import random


def generate_password(length, use_uppercase=True,
                      use_digits=True, use_special=True):
    """Функция для генерации пароля"""
    characters = string.ascii_lowercase

    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = "".join(random.choice(characters) for _ in range(length))
    return password
