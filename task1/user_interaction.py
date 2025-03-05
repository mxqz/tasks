import re
import msvcrt
import os
from colorama import Fore, Style

class Esc(Exception):
    """Custom exception used to exit when Escape key is pressed."""
    def __init__(self):
        super().__init__("Escape Pressed")


def clear() -> None:
    """Simply clears the screen to remove extra text in the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def getch() -> bytes:
    """Reads a single character from the keyboard without requiring Enter."""
    return msvcrt.getch()


def evaluate_password(password: str) -> tuple[int, list[str]]:
    """Checks the password and evaluates its strength.
    
    Args:
        password (str): The password entered by the user.
    
    Returns:
        tuple[int, list[str]]: Password score (from 0 to 5) and a list of suggestions for improvement.
        
    Raises:
        Esc: If the Escape key is pressed.
    """
    hints: list[str] = []
    score: int = 0
    
    if not password:
        return score, hints

    if re.search(r'[^a-zA-Z0-9]', password): 
        hints.append("Помилка: у паролі присутні неприпустимі символи!")
        return score, hints
    else:
        score += 1

    if len(password) >= 8: 
        score += 1
    else:
        hints.append("довжина паролю менше 8 символів")

    if any(c.isupper() for c in password): 
        score += 1
    else:
        hints.append("у паролі відсутні букви верхнього регістру")

    if any(c.islower() for c in password): 
        score += 1
    else:
        hints.append("у паролі відустні букви нижнього регістру")

    if len(re.findall(r'\d', password)) >= 2: 
        score += 1
    else:
        hints.append("у паролі менше двох цифр")
    
    return score, hints


def read_username(starting_username: str = "") -> str:
    """Reads the username from the keyboard.
    
    Args:
        starting_username (str, optional): Initial value if needed. Defaults to an empty string.
    
    Returns:
        str: The entered username.
        
    Raises:
        Esc: If the Escape key is pressed.
    """
    username: str = starting_username

    while True:
        clear()

        print(f"Ім'я користувача: {username}")

        char: bytes = getch()

        if char == b"\r" or char == b"\n": 
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
            if re.search(r'[^a-zA-Z0-9]', str(char.decode())):
                continue
            username += char.decode()
    
    return username
    

def read_password(show_password: bool = False, show_hints: bool = True) -> str:
    """Prompts the user to enter a password and checks its strength.
    
    
    Args:
        show_password (bool, optional): Whether to display the entered password. Defaults to False.
        show_hints (bool, optional): Whether to show password hints. Defaults to True.
    
    Returns:
        str: The entered password.
    """
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

        char: bytes = getch()
        
        if char == b"\r" or char == b"\n":  # Enter
            if any("Помилка" in hint for hint in hints) and show_hints:  
                password = ""
                continue 

            if score < 3 and show_hints:
                print("Пароль занадто слабкий, спробуйте ще раз!")
                password = ""
                getch()  
                continue 
            else:
                if show_hints:
                    print("\nПароль прийнято.")
                    getch() 
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