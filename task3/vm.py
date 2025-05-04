import sys
import re

memory = {}

VAR_PATTERN = re.compile(r'^(?:[a-zA-Z]+|t\d+)$')
FLOAT_PATTERN = re.compile(r'^-?(\d+\.?\d*|\.\d+)$')

def is_variable(s: str):
    return bool(VAR_PATTERN.fullmatch(s))

def is_number(s: str):
    return bool(FLOAT_PATTERN.fullmatch(s))

def get_value(s: str):
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

def execute(line: str):
    line = line.strip()
    if not line:
        return

    tokens = line.split()
    command = tokens[0].upper()

    match command:
        case "READ":
            if len(tokens) != 2 or not is_variable(tokens[1]):
                print(f"Синтаксична помилка в команді '{command}'")
                sys.exit(1)
            var = tokens[1]
            print(f"{var} = ", end="")
            val = str(input())
            if not is_number(val):
                print("Помилка: очікувалось число")
                sys.exit(1)
            memory[var] = float(val)

        case "WRITE":
            if len(tokens) != 2 or not is_variable(tokens[1]):
                print(f"Синтаксична помилка в команді '{command}'")
                sys.exit(1)
            var = tokens[1]
            if var not in memory:
                print(f"Помилка: змінна '{var}' не знайдена")
                sys.exit(1)
            print(f"{var} = {memory[var]}")
            # print(memory[var])

        case "COPY":
            if len(tokens) != 3:
                print(f"Синтаксична помилка в команді '{command}'")
                sys.exit(1)
            src, dst = tokens[1], tokens[2]
            if not is_variable(dst):
                print("Помилка: недопустиме імʼя змінної")
                sys.exit(1)
            memory[dst] = get_value(src)

        case  "ADD" | "SUB" | "MUL" | "DIV":
            if len(tokens) != 4:
                print(f"Синтаксична помилка в арифметичній операції '{command}'")
                sys.exit(1)
            _, left, right, dst = tokens
            if not is_variable(dst):
                print("Помилка: результат має бути збережений у змінну")
                sys.exit(1) 

            lval = get_value(left)
            rval = get_value(right)

            if command == 'ADD':
                memory[dst] = lval + rval
            elif command == 'SUB':
                memory[dst] = lval - rval
            elif command == 'MUL':
                memory[dst] = lval * rval
            elif command == 'DIV':
                if rval == 0:
                    print("Помилка: ділення на нуль")
                    sys.exit(1)
                memory[dst] = lval / rval

        case _:
            print(f"Синтаксична помилка: невідома команда '{tokens[0]}'")
            sys.exit(1)

def run(filename: str):
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
    run("Vr/cd.txt")
