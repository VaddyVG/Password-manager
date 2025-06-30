from app.gen_password import generate_password
from app.encryptor import encrypt_password, decrypt_password
from app.key_manager import load_key
from typing import Optional, NoReturn
from app.file_manager import (
    save_password, find_password_by_name,
    delete_password, update_password, list_all_passwords
)
import sys


class PasswordManager:
    def __init__(self):
        """Инициализация менеджера паролей с загрузкой ключа шифрования."""
        self.key = self._load_encryption_key()
        self.menu_actions = {
            '1': self.generate_new_password,
            '2': self.find_password,
            '3': self.remove_password,
            '4': self.modify_password,
            '5': self.show_all_passwords,
            '6': self.exit_program
        }

    def _load_encryption_key(self):
        """Загружает ключ шифрования с обработкой возможных ошибок."""
        try:
            return load_key()
        except Exception as e:
            print(f"Ошибка загрузки ключа шифрования: {e}")
            sys.exit(1)

    def display_menu(self) -> None:
        """Отображает главное меню программы."""
        print("\n" + "="*30)
        print("Менеджер паролей".center(30))
        print("="*30)
        print("1. Сгенерировать новый пароль")
        print("2. Найти пароль по имени")
        print("3. Удалить пароль")
        print("4. Обновить пароль")
        print("5. Показать все пароли")
        print("6. Выйти")
        print("="*30)

    def get_password_parameters(self) -> tuple[int, bool, bool, bool]:
        """Запрашивает параметры генерации пароля у пользователя."""
        try:
            length = int(input("Длина пароля (8-64): "))
            if not 8 <= length <= 64:
                raise ValueError("Длина должна быть от 8 до 64 символов")
            use_uppercase = input("Буквы верхнего регистра (y/n): ").lower() == "y"
            use_digits = input("Цифры (y/n): ").lower() == "y"
            use_special = input("Спецсимволы (y/n): ").lower() == "y"
            
            return length, use_uppercase, use_digits, use_special
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
            return self.get_password_parameters() # Рекурсивный повтор при ошибке

    def generate_new_password(self) -> None:
        """Генерирует, шифрует и сохраняет пароль."""
        try:
            print("\nГенерация нового пароля:")
            params = self.get_password_parameters()
            password = generate_password(*params)
            print(f"\nВаш пароль: [ {password} ]")

            if input("Сохранить этот пароль? (y/n): ").lower() == 'y':
                encrypted = encrypt_password(password, self.key)
                name = input("Введите название для пароля: ").strip()
                if name:
                    save_password(name, encrypted)
                else:
                    print("Навзание пароля не может быть пустым!")
        except Exception as e:
            print(f"Ошибка генерации пароля: {e}")

    def find_password(self) -> Optional[str]:
        """Находит и расшифровывает пароль по имени."""
        print("\nПоиск пароля:")
        name = input("Введите имя пароля: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            return None

        try:
            encrypted = find_password_by_name(name)
            if encrypted:
                if isinstance(encrypted, str):
                    encrypted_bytes = encrypted.encode()
                else:
                    encrypted_bytes = encrypted
                password = decrypt_password(encrypted_bytes, self.key)
                print(f"\nПароль для '{name}': [ {password} ]")
                return password
            else:
                print("Пароль не найден")
                return None
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            return None

    def remove_password(self) -> None:
        """Удаляет пароль по имени."""
        print("\nУдаление пароля:")
        name = input("Введите название пароля для удаления: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            return
    
        try:
            delete_password(name)
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def modify_password(self) -> None:
        """Обновляет существующий пароль."""
        print("\nОбновление пароля:")
        name = input("Введите имя пароля для обновления: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            return
        try:
            if not find_password_by_name(name):
                print("Пароль не найден")
                return
            
            print("Введите новые параметры пароля:")
            params = self.get_password_parameters()
            new_password = generate_password(*params)
            print(f"\nНовый пароль: [ {new_password} ]")

            if input("Сохранить изменения? (y/n): ").lower() == "y":
                encrypted = encrypt_password(new_password, self.key)
                update_password(name, encrypted)
                print("Пароль обновлен!")
        except Exception as e:
            print(f"Ошибка обновления: {e}")

    def show_all_passwords(self) -> None:
        print("\nСписок сохраненных паролей:")
        return list_all_passwords()

    def exit_program(self) -> NoReturn:
        """Корректно завершает работу программы."""
        print("\nЗавершение работы менеджера паролей...")
        sys.exit(0)
    
    def run(self) -> None:
        """Основной цикл работы программы."""
        while True:
            try:
                self.display_menu()
                choice = input("\nВыберите действие (1-6): ").strip()
                action = self.menu_actions.get(choice)
                if action:
                    action()
                else:
                    print("Неверный выбор! Попробуйте снова.")
            except KeyboardInterrupt:
                if input("\nПрервать работу? (y/n): ").lower() == 'y':
                    self.exit_program()
            except Exception as e:
                print(f"Критическая ошибка: {e}")
                sys.exit(1)
    