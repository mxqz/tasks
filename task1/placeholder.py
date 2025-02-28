import re
import sys
import msvcrt
import os
from colorama import Fore, Style

def evaluate_password(password):
    hints = []

    score = 0
    
    if not password:
        #hints.append("ВВЕДІТЬ ПАРОЛЬ!!")
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

def read_password():
    password = ""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') 

        score, hints = evaluate_password(password)
        
        print(f"Пароль: {password}")  # print(f"Пароль: {'*' * len(password)}") # print(f"Пароль: {password}") - щоб пароль показувався не зірочками, а введеними символами
        print(f"Оцінка: {'*' * score}")
        
        if hints:
            if "Помилка" in hints[0]:
                print(Fore.RED + hints[0] + Style.RESET_ALL)
            else:
                print(f"Підказка: {hints[0]}")  

        char = msvcrt.getch()
        
        if char in {b"\r", b"\n"}:  # Enter
            if any("Помилка" in hint for hint in hints):  # Якщо є помилка
                print(Fore.RED + hints[0] + Style.RESET_ALL)
                password = ""
                msvcrt.getch()  # Очікуємо натискання клавіші перед очищенням екрану
                continue  # Повертаємося на початок введення

            if score < 3:
                print("Пароль занадто слабкий, спробуйте ще раз!")
                password = ""
                msvcrt.getch()  # Очікуємо натискання клавіші перед очищенням екрану
                continue  # Повертаємося на початок циклу для нового введення
            else:
                print("\nПароль прийнято.")
                msvcrt.getch()  # Очікуємо натискання клавіші перед очищенням екрану
                break

        elif char == b"\x08": 
            if password:
                password = password[:-1]

        elif char == b"\xe0":
            msvcrt.getch()
            continue

        elif 32 <= ord(char) <= 126:
            password += char.decode()  
    
    return password

if __name__ == "__main__":
    while True:
        read_password()