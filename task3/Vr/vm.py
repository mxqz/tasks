import sys
import re

memory = {}  # Реєстр памʼяті

# Патерни для перевірки
VAR_PATTERN = re.compile(r'^[a-zA-Z]+$')
FLOAT_PATTERN = re.compile(r'^-?\d+(\.\d+)?$')

def is_variable(s):
    return bool(VAR_PATTERN.fullmatch(s))

def is_number(s):
    return bool(FLOAT_PATTERN.fullmatch(s))

def get_value(s):
    if is_number(s):
        return float(s)
    elif is_variable(s):
        if s in memory:
            return memory[s]
        else:
            print(f"Помилка: змінна '{s}' не ініціалізована.")
            sys.exit(1)
    else:
        print(f"Синтаксична помилка: некоректний операнд '{s}'")
        sys.exit(1)


def execute(line):
    line = line.strip()
    if not line:
        return  # Порожній рядок

    tokens = line.split()

    if line.startswith("read>"):
        if len(tokens) != 2 or not is_variable(tokens[1]):
            print("Синтаксична помилка в команді 'read>'")
            sys.exit(1)
        var = tokens[1]
        val = input(f"{var} = ")
        if not is_number(val):
            print("Помилка: очікувалось число")
            sys.exit(1)
        memory[var] = float(val)

    elif line.startswith("write>"):
        if len(tokens) != 2 or not is_variable(tokens[1]):
            print("Синтаксична помилка в команді 'write>'")
            sys.exit(1)
        var = tokens[1]
        if var not in memory:
            print(f"Помилка: змінна '{var}' не знайдена")
            sys.exit(1)
        print(memory[var])

    elif tokens[0] == '=':
        if len(tokens) != 3:
            print("Синтаксична помилка в команді присвоєння '='")
            sys.exit(1)
        src, dst = tokens[1], tokens[2]
        if not is_variable(dst):
            print("Помилка: недопустиме імʼя змінної")
            sys.exit(1)
        memory[dst] = get_value(src)

    elif tokens[0] in ['+', '-', '*', '/']:
        if len(tokens) != 4:
            print(f"Синтаксична помилка в арифметичній операції '{tokens[0]}'")
            sys.exit(1)
        op, left, right, dst = tokens
        if not is_variable(dst):
            print("Помилка: результат має бути збережений у змінну")
            sys.exit(1)

        lval = get_value(left)
        rval = get_value(right)

        if op == '+':
            memory[dst] = lval + rval
        elif op == '-':
            memory[dst] = lval - rval
        elif op == '*':
            memory[dst] = lval * rval
        elif op == '/':
            if rval == 0:
                print("Помилка: ділення на нуль")
                sys.exit(1)
            memory[dst] = lval / rval

    else:
        print(f"Синтаксична помилка: невідома команда '{tokens[0]}'")
        sys.exit(1)

def run(filename):
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                try:
                    execute(line)
                except SystemExit:
                    print(f"(рядок {line_num})")
                    sys.exit(1)
    except FileNotFoundError:
        print(f"Помилка: файл '{filename}' не знайдено.")
        sys.exit(1)

if __name__ == "__main__":
    run("cd.txt")

