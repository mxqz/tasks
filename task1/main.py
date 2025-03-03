import os
import msvcrt
import database
import user_interaction
import hashlib

# Функція для додавання пароля
def add_user(db: database.Database):
    username = ""
    while True:
        try:
            username = user_interaction.read_username()
        except user_interaction.Esc:
            return
        unique = db.find("username", username) == -1
        if unique:
            break
        print("Ім'я користувача зайнято, спробуйте інше")
        msvcrt.getch()

    try:    
        password = user_interaction.read_password()
    except user_interaction.Esc:
        return
    password = hashlib.sha256(password.encode()).hexdigest()
    db.add([username, password])
    db.save_csv()

# Функція для зміни пароля
def change_password(db: database.Database):
    username = ""
    while True:
        try:
            username = user_interaction.read_username()
        except user_interaction.Esc:
            return
        unique = db.find("username", username) == -1
        if not unique:
            break
        print("Ім'я користувача відсутнє у списку.")
        msvcrt.getch()

    try:    
        password = user_interaction.read_password()
    except user_interaction.Esc:
        return
    
    password = hashlib.sha256(password.encode()).hexdigest()
    index = db.find("username", username)
    
    if password != db[index].get("password"):
        print("Невірний пароль.")
        msvcrt.getch()
        return

    db.change(index, [username, password])
    db.save_csv()

# Функція для перегляду користувачів
def view_users(db: database.Database):
    user_interaction.clear()
    print("Список користувачів:")
    for user in db.get_column("username"):
        print(user)
    msvcrt.getch()

# Функція для видалення користувача
def delete_user(db: database.Database):
    username = ""
    while True:
        try:
            username = user_interaction.read_username()
        except user_interaction.Esc:
            return
        unique = db.find("username", username) == -1
        if not unique:
            break
        print("Ім'я користувача відсутнє у списку.")
        msvcrt.getch()

    try:    
        password = user_interaction.read_password()
    except user_interaction.Esc:
        return
    
    password = hashlib.sha256(password.encode()).hexdigest()
    index = db.find("username", username)
    
    if password != db[index].get("password"):
        print("Невірний пароль.")
        msvcrt.getch()
        return
    
    print("Ви дійсно хочете видалити даного користувача?\n(Esc - відмінити, Any Key - продовжити)")
    if msvcrt.getch() == b'\x1b':
        return
    db.remove(index)
    db.save_csv()

# Основне меню
def main_menu(db: database.Database):
    while True:
        user_interaction.clear()
        print("Менеджер паролів")
        print("1. Створити нового користувача")
        print("2. Змінити пароль користувача")
        print("3. Переглянути користувачів")
        print("4. Видалити користувача")
        print("5. Вийти")

        char = msvcrt.getch()

        match char:
            case b'1':
                add_user(db)
            case b'2':
                change_password(db)
            case b'3':
                view_users(db)
            case b'4':
                delete_user(db)
            case b'5' | b'\x1b':
                print("Вихід з програми.")
                break


if __name__ == "__main__":
    db = database.Database("passwords.csv")
    main_menu(db)
