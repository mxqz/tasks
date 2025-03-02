import os
import msvcrt

# Перевірка натискання клавіші "Esc"
def check_escape_key():
    print("Натисніть 'Esc' для повернення до головного меню.")
    if msvcrt.kbhit():  # Якщо натиснута клавіша
        char = msvcrt.getch()
        if char == b'\x1b':  # Якщо натиснуто 'Esc' (код клавіші Escape)
            print("Повернення до головного меню...")
            return True
    return False



# Функція для додавання пароля
def evaluate_password():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("Додати пароль")
      

        #username = input("Введіть ім'я користувача: ")
        #password = input("Введіть пароль: ")

        
        
        if check_escape_key():
            return
           
      

# Функція для зміни пароля
def change_password():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очищаємо екран
        print("змінити пароль")
        
        
        #username = input("Введіть ім'я користувача для зміни паролю: ")
        #new_password = input("Введіть новий пароль: ")

      
       
        check_escape_key()
       

    

# Функція для перегляду користувачів
def view_passwords():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("Перегляд користувачів")
       



       
        check_escape_key()
          
          



# Функція для видалення користувача
def delete_user():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') 
        print(" Видалити користувача")
        

        #username = input("Введіть ім'я користувача для видалення: ")


       
    
        check_escape_key()
       
      

# Основне меню
def main_menu():
 while True:
     
    os.system('cls' if os.name == 'nt' else 'clear')  
    print("Менеджер паролів")
    print("1. Додати пароль")
    print("2. Змінити пароль")
    print("3. Переглянути користувачів")
    print("4. Видалити користувача")
    print("5. Вийти")

    char = msvcrt.getch()

    match char:
        case b'1':
            evaluate_password()
        case b'2':
            change_password()
        case b'3':
            view_passwords()
        case b'4':
            delete_user()
        case b'5' | b'\x1b':  
            print("Вихід з програми.")
            break


if __name__ == "__main__":
    main_menu()  
