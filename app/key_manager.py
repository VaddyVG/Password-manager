import os
from cryptography.fernet import Fernet


def generate_key(filename="secret.key"):
    """Функция для генерации и сохранения ключа шифрования."""
    key = Fernet.generate_key()
    with open(filename, "wb") as key_file:
        key_file.write(key)
    return key


def load_key(filename="secret.key"):
    """Функция для загрузки ключа."""
    if not os.path.exists(filename):
        return generate_key()
    with open(filename, "rb") as key_file:
        return key_file.read()
