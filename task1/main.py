import database
import user_interaction
import hashlib

message = {
    "WRONG_PASSWORD": "Невірний пароль.",
    "USER_DELETION_CONFIRM": "Ви дійсно хочете видалити даного користувача?\n(Esc - відмінити, Any Key - продовжити)",
    "USER_IS_TAKEN": "Ім'я користувача зайнято, спробуйте інше.",
    "USER_LIST": "Список користувачів:",
    "SCORE_LIST": "Оцінка захищеності паролю:",
    "USER_NOT_FOUND": "Ім'я користувача відсутнє у списку.",
    "EXIT": ""
}


# Функція для додавання пароля
def add_user(db: database.Database):
    username = ""
    while True:
        try:
            username = user_interaction.read_username(starting_username = username)
        except user_interaction.Esc:
            return
        
        unique = db.find("username", username) == -1

        if unique:
            break

        print(message["USER_IS_TAKEN"])
        user_interaction.getch()

    try:    
        password = user_interaction.read_password()
    except user_interaction.Esc:
        return
    
    score = user_interaction.evaluate_password(password)[0]

    password = hashlib.sha256(password.encode()).hexdigest()
    
    db.add([username, password, score])
    db.save_csv()


# Функція для зміни пароля
def change_password(db: database.Database):
    username = ""
    while True:
        try:
            username = user_interaction.read_username(starting_username = username)
        except user_interaction.Esc:
            return
        
        unique = db.find("username", username) == -1
        
        if not unique:
            break
        
        print(message["USER_NOT_FOUND"])
        user_interaction.getch()

    try:    
        password = user_interaction.read_password(show_hints = False)
    except user_interaction.Esc:
        return
    
    password = hashlib.sha256(password.encode()).hexdigest()
    index = db.find("username", username)
    
    if password != db[index].get("password"):
        print(message["WRONG_PASSWORD"])
        user_interaction.getch()
        return

    try:
        password = user_interaction.read_password()
    except user_interaction.Esc:
        return

    score = user_interaction.evaluate_password(password)[0]

    db.change(index, [username, password, score])
    db.save_csv()


# Функція для перегляду користувачів
def view_users(db: database.Database):
    user_interaction.clear()
    print(f"{message["USER_LIST"]:31}{message["SCORE_LIST"]}")
    for i in range(len(db)):
        print(f"{db[i]["username"]:16}{db[i]["score"]:16}")
    user_interaction.getch()


# Функція для видалення користувача
def delete_user(db: database.Database):
    username = ""
    while True:
        try:
            username = user_interaction.read_username(starting_username = username)
        except user_interaction.Esc:
            return
        
        unique = db.find("username", username) == -1

        if not unique:
            break

        print(message["USER_NOT_FOUND"])
        user_interaction.getch()

    while True:
        try:    
            password = user_interaction.read_password(show_hints = False)
        except user_interaction.Esc:
            return
        
        password = hashlib.sha256(password.encode()).hexdigest()
        index = db.find("username", username)
        
        if password == db[index].get("password"):
            break
        
        print(message["WRONG_PASSWORD"])
        user_interaction.getch()
    
    user_interaction.clear()
    print(message["USER_DELETION_CONFIRM"])
    if user_interaction.getch() == b'\x1b':
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

        char = user_interaction.getch()

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
                print(message["EXIT"])
                break


if __name__ == "__main__":
    db = database.Database("passwords.csv")
    main_menu(db)
