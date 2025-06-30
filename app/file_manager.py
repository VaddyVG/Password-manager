import os
from typing import Optional, List, Tuple


DEFAULT_FILENAME = "password_ecrypted.txt"

def save_password(name: str, encrypted_password: bytes,
                  filename: str = DEFAULT_FILENAME) -> None:
    """Сохраняет зашифрованный пароль в файл."""
    try:
        with open(filename, "a") as file:
            file.write(f"{name},{encrypted_password.decode()}\n")
        print(f"Пароль '{name}' успешно сохранен в {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении пароля: {e}")


def find_password_by_name(name: str,
                          filename: str = DEFAULT_FILENAME) -> Optional[str]:
    """Находит и возвращает зашифрованный пароль по названию."""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return None

    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    saved_name, encrypted_password = line.strip().split(",", 1)
                    if saved_name == name:
                        return encrypted_password
                except ValueError:
                    continue  # Пропуск некорректных строк
        return None
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def delete_password(name: str,
                    filename: str = DEFAULT_FILENAME) -> bool:
    """
    Удаляет пароль по названию. Возвращает True
    если удаление прошло успешно.
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return False

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        updated_lines = []
        found = False

        for line in lines:
            try:
                saved_name, _ = line.strip().split(",", 1)
                if saved_name != name:
                    updated_lines.append(line)
                else:
                    found = True
            except ValueError:
                continue  # Пропуск некорректных строк

        if found:
            with open(filename, "w") as file:
                file.writelines(updated_lines)
            print(f"Пароль '{name}' успешно удален")
        else:
            print(f"Пароль '{name}' не найден")

        return found
    except IOError as e:
        print(f"Ошибка при обработке файла: {e}")
        return False


def update_password(name: str,
                    new_encrypted_password: bytes,
                    filename: str = DEFAULT_FILENAME) -> bool:
    """
    Обновляет существующий пароль. 
    Возвращает True если обновление прошло успешно.
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return False

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    
        updated = False
        new_lines = []

        for line in lines:
            try:
                saved_name, _ = line.strip().split(",", 1)
                if saved_name == name:
                    new_lines.append(f"{name},{new_encrypted_password.decode()}\n")
                    updated = True
                else:
                    new_lines.append(line)
            except ValueError:
                continue  # Пропуск некорректных строк

        if updated:
            with open(filename, "w") as file:
                file.writelines(new_lines)
            print(f"Пароль '{name}' успешно обновлён")
        else:
            print(f"Пароль '{name}' не найден")
        return updated
    except IOError as e:
        print(f"Ошибка при обновлении пароля: {e}")
        return False


def list_all_passwords(filename: str = DEFAULT_FILENAME) -> List[Tuple[str]]:
    """
    Возвращает список всех 
    сохранённых паролей (имя, зашифрованный пароль).
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return []

    passwords = []
    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    if line.strip():  # Пропуск пустых строк
                        name, encrypted = line.strip().split(",", 1)
                        passwords.append((name, encrypted))
                except ValueError:
                    continue  # Пропуск некорректых строк
        if passwords:
            print("\nСписок сохраненных паролей:")
            for i, (name, _) in enumerate(passwords, 1):
                print(f"{i}. {name}")
        else:
            print("Нет сохранённых паролей.")
        input("\nНажмите Enter для продолжения...")
        return passwords
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return []
