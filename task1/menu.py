import tkinter as tk
from tkinter import messagebox, ttk
import csv
from placeholder import evaluate_password  # Ви не використовуєте 'hints' в імпорті, тому треба прибрати

# Ну коротше я зробив візуал попросив джбт все прокоментував щоб вам було простіше розібратися 
# import tkinter as tk from tkinter import messagebox, ttk --  це візуал і на якій бібліотеці воно паше
# Воно зразу підтримує файл Вови тобто повністю з ним взаємодіє
# да тут є шото типу додавання до бази даних бо мені потрібно було бачити чи воно коректно працює
# надіюсь ви мене сильно не будете хуєсосити
# а ще там не їбу чоно создається файл  кожного разу при запуску програми но його можна удаляти 

CSV_FILE = "passwords.csv"  # Шлях до файлу, в якому зберігаються паролі

# Збереження пароля
def save_password(username, password):
    if not username or not password:  # Перевіряємо, чи введені обидва поля
        messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля")  # Якщо не введено, виводимо помилку
        return
    
    score, hints = evaluate_password(password)  # Оцінка паролю і підказки для нього
    if score < 5:  # Якщо оцінка паролю менша за 5, показуємо підказки
        messagebox.showerror("Помилка", "\n".join(hints))  # Виводимо підказки
        return

    with open(CSV_FILE, mode='a', newline='') as file:  # Відкриваємо файл для запису
        writer = csv.writer(file)  # Створюємо об'єкт для запису в CSV
        writer.writerow([username, password])  # Записуємо ім'я користувача та пароль
    messagebox.showinfo("Успіх", "Пароль збережено")  # Повідомлення про успіх

# Зміна пароля
def change_password(username, new_password):
    if not username or not new_password:  # Перевірка, чи введено ім'я користувача і новий пароль
        messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля")
        return
    
    score, hints = evaluate_password(new_password)  # Оцінка нового паролю
    if score < 5:  # Якщо пароль слабкий, показуємо підказки
        messagebox.showerror("Помилка", "\n".join(hints))
        return

    rows = []  # Список для зберігання всіх рядків з файлу
    found = False  # Змінна для позначення, чи знайдений користувач
    with open(CSV_FILE, mode='r', newline='') as file:  # Читаємо з файлу
        reader = csv.reader(file)  # Створюємо об'єкт для читання CSV
        for row in reader:
            if row and row[0] == username:  # Якщо знайдений користувач
                row[1] = new_password  # Оновлюємо пароль
                found = True  # Позначаємо, що користувач знайдений
            rows.append(row)  # Додаємо рядок до списку
    
    if found:
        with open(CSV_FILE, mode='w', newline='') as file:  # Перезаписуємо файл з новим паролем
            writer = csv.writer(file)
            writer.writerows(rows)  # Записуємо всі рядки з оновленим паролем
        messagebox.showinfo("Успіх", "Пароль змінено")  # Повідомлення про успіх
    else:
        messagebox.showerror("Помилка", "Користувач не знайдений")  # Повідомлення, якщо користувач не знайдений

# Перегляд списку користувачів
def view_passwords():
    try:
        with open(CSV_FILE, mode='r', newline='') as file:  # Відкриваємо файл для читання
            reader = csv.reader(file)
            users = [row[0] for row in reader if row]  # Отримуємо список користувачів

        if not users:
            messagebox.showinfo("Користувачі", "Список порожній")  # Якщо користувачів немає
            return

        # Створюємо нове вікно для відображення користувачів
        top = tk.Toplevel()
        top.title("Список користувачів")
        top.geometry("300x400")
        top.configure(bg="#1E1E1E")

        ttk.Label(top, text="Список користувачів", font=("Arial", 14, "bold"), background="#1E1E1E", foreground="white").pack(pady=10)

        # Додаємо Treeview (таблиця для відображення користувачів)
        frame = tk.Frame(top, bg="#1E1E1E")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        tree = ttk.Treeview(frame, columns=("№", "Ім'я"), show="headings", height=15)
        tree.heading("№", text="№", anchor="center")  # Номер користувача
        tree.heading("Ім'я", text="Ім'я користувача", anchor="center")  # Ім'я користувача
        tree.column("№", width=30, anchor="center")
        tree.column("Ім'я", anchor="w")

        # Додаємо користувачів у таблицю
        for i, user in enumerate(users, start=1):
            tree.insert("", "end", values=(i, user))

        tree.pack(side="left", fill="both", expand=True)

        # Додаємо прокрутку для таблиці
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    except FileNotFoundError:
        messagebox.showerror("Помилка", "Файл з паролями не знайдено")  # Якщо файл не знайдено, вивести помилку

# Видалення користувача
def delete_user(username):
    if not username:
        messagebox.showerror("Помилка", "Будь ласка, введіть ім'я користувача")  # Якщо не введено ім'я
        return
    rows = []  # Список для зберігання рядків після видалення користувача
    found = False  # Змінна для позначення, чи знайдений користувач
    with open(CSV_FILE, mode='r', newline='') as file:  # Читаємо з файлу
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] != username:  # Якщо користувача не знайдено, додаємо його до списку
                rows.append(row)
            else:
                found = True  # Користувач знайдений
    
    if found:
        with open(CSV_FILE, mode='w', newline='') as file:  # Перезаписуємо файл без видаленого користувача
            writer = csv.writer(file)
            writer.writerows(rows)
        messagebox.showinfo("Успіх", "Користувача видалено")
    else:
        messagebox.showerror("Помилка", "Користувач не знайдений")  # Якщо користувача не знайдено

# Додавання підказок для паролю
def update_password_hints(*args):
    password = password_var.get()  # Отримуємо значення з поля паролю
    score, hints = evaluate_password(password)  # Оцінюємо пароль
    if score < 5:  # Якщо пароль слабкий, показуємо підказки
        hint_label.config(text="\n".join(hints), foreground="red")  # Підказки виводяться червоним
    else:
        hint_label.config(text="Пароль є достатньо сильним", foreground="green")  # Якщо пароль сильний, повідомлення зеленим

# Графічний інтерфейс
def create_gui():
    global password_var, hint_label  # Оголошуємо змінні глобальними, щоб використовувати в іншій частині коду
    
    root = tk.Tk()
    root.title("Менеджер паролів")
    root.geometry("400x520")
    root.configure(bg='#1E1E1E')  # Темний фон

    # Налаштування стилю для елементів інтерфейсу
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10, background="#444", foreground="black")
    style.configure("TLabel", font=("Arial", 12, "bold"), background="#1E1E1E", foreground="white")
    style.configure("TEntry", font=("Arial", 12), padding=5, fieldbackground="#333", foreground="black")
    style.map("TButton", background=[("active", "#666")])

    frame = tk.Frame(root, bg="#1E1E1E")  # Основний контейнер
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    ttk.Label(frame, text="Менеджер паролів", font=("Arial", 16, "bold")).pack(pady=10)
    
    ttk.Label(frame, text="Ім'я користувача:").pack(anchor="w")
    username_entry = ttk.Entry(frame)  # Поле для введення імені користувача
    username_entry.pack(pady=5, fill="x")
    
    ttk.Label(frame, text="Пароль:").pack(anchor="w")
    
    password_var = tk.StringVar()  # Змінна для зберігання паролю
    password_entry = ttk.Entry(frame, show="*", textvariable=password_var)  # Поле для введення паролю
    password_entry.pack(pady=4, fill="x")

    # Додаємо Label для підказок
    hint_label = ttk.Label(frame, text="", font=("Arial", 10), foreground="red", background="#1E1E1E")
    hint_label.pack(pady=5)

    # Додаємо trace для оновлення підказок при введенні паролю
    password_var.trace("w", update_password_hints)

    button_frame = tk.Frame(frame, bg="#1E1E1E")
    button_frame.pack(pady=10, fill="x")
    
    # Кнопки для додавання, зміни паролю, перегляду та видалення користувачів
    ttk.Button(button_frame, text="Додати пароль", command=lambda: save_password(username_entry.get(), password_entry.get())).pack(fill='x', pady=3)
    ttk.Button(button_frame, text="Змінити пароль", command=lambda: change_password(username_entry.get(), password_entry.get())).pack(fill='x', pady=3)
    ttk.Button(button_frame, text="Переглянути користувачів", command=view_passwords).pack(fill='x', pady=3)
    ttk.Button(button_frame, text="Видалити користувача", command=lambda: delete_user(username_entry.get())).pack(fill='x', pady=3)
    ttk.Button(button_frame, text="Вийти", command=root.quit).pack(fill='x', pady=3)
    
    root.mainloop()  # Запуск графічного інтерфейсу

if __name__ == "__main__":
    create_gui()  # Викликаємо функцію для запуску інтерфейсу
