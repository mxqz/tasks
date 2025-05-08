import sys
import re

memory = {}
labels = {}
lines = []

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
            print(f"Error: variable '{s}' is not initialized.")
            sys.exit(1)
    else:
        print(f"Syntax error: invalid operand '{s}'")
        sys.exit(1)

def preprocess():
    """Build label map before execution."""
    for i, line in enumerate(lines):
        line = line.strip()
        if line.endswith(':'):
            label = line[:-1]
            if not is_variable(label):
                print(f"Syntax error: invalid label name '{label}'")
                sys.exit(1)
            labels[label] = i

def execute_line(index: int):
    line = lines[index].strip()
    if not line or line.endswith(':'):
        return index + 1

    tokens = line.split()
    command = tokens[0].upper()

    match command:
        case "READ":
            if len(tokens) != 2 or not is_variable(tokens[1]):
                print(f"Syntax error in command '{command}'")
                sys.exit(1)
            var = tokens[1]
            print(f"{var} = ", end="")
            val = str(input())
            if not is_number(val):
                print("Error: expected a number.")
                sys.exit(1)
            memory[var] = float(val)

        case "WRITE":
            if len(tokens) != 2 or not is_variable(tokens[1]):
                print(f"Syntax error in command '{command}'")
                sys.exit(1)
            var = tokens[1]
            if var not in memory:
                print(f"Error: variable '{var}' is not found.")
                sys.exit(1)
            print(f"{var} = {memory[var]}")

        case "COPY":
            if len(tokens) != 3:
                print(f"Syntax error in command '{command}'")
                sys.exit(1)
            src, dst = tokens[1], tokens[2]
            if not is_variable(dst):
                print("Error: invalid variable name.")
                sys.exit(1)
            memory[dst] = get_value(src)

        case "ADD" | "SUB" | "MUL" | "DIV":
            if len(tokens) != 4:
                print(f"Syntax error in arithmetic operation '{command}'")
                sys.exit(1)
            _, left, right, dst = tokens
            if not is_variable(dst):
                print("Error: result must be stored in a variable.")
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
                    print("Error: division by zero.")
                    sys.exit(1)
                memory[dst] = lval / rval

        case "GOTO":
            if len(tokens) != 2:
                print("Syntax error: GOTO requires one label.")
                sys.exit(1)
            label = tokens[1]
            if label not in labels:
                print(f"Error: label '{label}' not found.")
                sys.exit(1)
            return labels[label]

        case "GOTOIF":
            if len(tokens) != 3:
                print("Syntax error: GOTOIF requires a condition and label.")
                sys.exit(1)
            cond, label = tokens[1], tokens[2]
            if get_value(cond):
                if label not in labels:
                    print(f"Error: label '{label}' not found.")
                    sys.exit(1)
                return labels[label]

        case "GOTOIFNOT":
            if len(tokens) != 3:
                print("Syntax error: GOTOIFNOT requires a condition and label.")
                sys.exit(1)
            cond, label = tokens[1], tokens[2]
            if not get_value(cond):
                if label not in labels:
                    print(f"Error: label '{label}' not found.")
                    sys.exit(1)
                return labels[label]

        case _:
            print(f"Syntax error: unknown command '{tokens[0]}'")
            sys.exit(1)

    return index + 1

def run(filename: str):
    global lines
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    preprocess()
    i = 0
    while i < len(lines):
        try:
            i = execute_line(i)
        except SystemExit:
            print(f"(line {i + 1})")
            sys.exit(1)

if __name__ == "__main__":
    run("Vr/cd.txt")
