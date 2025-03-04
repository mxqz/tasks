import re
import msvcrt
import os
from colorama import Fore, Style

class Esc(Exception):
    def __init__(self):
        super().__init__("Escape Pressed")


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def getch() -> bytes:
    return msvcrt.getch()


def evaluate_password(password: str) -> tuple[int, list[str]]:
    hints: list[str] = []
    score: int = 0
    
    if not password:
        # hints.append("ВВЕДІТЬ ПАРОЛЬ!!")
        return score, hints

    if re.search(r'[^a-zA-Z0-9]', password): #якщо присутні спец символи, то пароль недійсний, поки їх нема +1 бал який є з самого початку
        hints.append("Помилка: у паролі присутні неприпустимі символи!")
        return score, hints
    else:
        score += 1

    if len(password) >= 8: #довжина довше 8 символів
        score += 1
    else:
        hints.append("довжина паролю менше 8 символів")

    if any(c.isupper() for c in password): # присутня хоча б одна велика літера
        score += 1
    else:
        hints.append("у паролі відсутні букви верхнього регістру")

    if any(c.islower() for c in password): #присутня хоча б одна маленька літера
        score += 1
    else:
        hints.append("у паролі відустні букви нижнього регістру")

    if len(re.findall(r'\d', password)) >= 2: #цифр у паролі хоча б дві
        score += 1
    else:
        hints.append("у паролі менше двох цифр")
    
    return score, hints


def read_username(starting_username: str = "") -> str:
    username: str = starting_username

    while True:
        clear()

        print(f"Ім'я користувача: {username}")

        char: bytes = getch()

        if char == b"\r" or char == b"\n":  # Enter
            if not username:
                continue
            break
        
        elif char == b'\x1b':
            raise Esc

        elif char == b"\x08": 
            if username:
                username = username[:-1]

        elif char == b"\xe0":
            getch()
            continue

        elif char == b"\x17":
            username = ""
            continue

        elif 32 <= ord(char) <= 126:
            username += char.decode()
    
    return username
    

def read_password(show_password: bool = False, show_hints: bool = True) -> str:
    password: str = ""
    
    while True:
        clear()
        
        score: int
        hints: list[str]
        score, hints = evaluate_password(password)
        
        if show_password:
            print(f"Пароль: {password}")
        else:
            print(f"Пароль: {'*' * len(password)}")
        
        if show_hints:    
            print(f"Оцінка: {'*' * score}")
        
        if hints and show_hints:
            if "Помилка" in hints[0]:
                print(Fore.RED + hints[0] + Style.RESET_ALL)
            else:
                print(f"Підказка: {hints[0]}")  
                # for hint in hints:
                #     print(f"Підказка: {hint}")  

        char: bytes = getch()
        
        if char == b"\r" or char == b"\n":  # Enter
            if any("Помилка" in hint for hint in hints) and show_hints:  # Якщо є помилка
                password = ""
                continue  # Повертаємося на початок введення

            if score < 3 and show_hints:
                print("Пароль занадто слабкий, спробуйте ще раз!")
                password = ""
                getch()  # Очікуємо натискання клавіші перед очищенням екрану
                continue  # Повертаємося на початок циклу для нового введення
            else:
                if show_hints:
                    print("\nПароль прийнято.")
                    getch()  # Очікуємо натискання клавіші перед очищенням екрану
                break
        
        elif char == b'\x1b':
            raise Esc

        elif char == b"\x08": 
            if password:
                password = password[:-1]

        elif char == b"\xe0":
            getch()
            continue

        elif char == b"\x17":
            password = ""
            continue

        elif 32 <= ord(char) <= 126:
            password += char.decode()  
    
    return password

if __name__ == "__main__":
    read_password()