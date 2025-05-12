import sys
import re
import json
from int_reference import IntReference

paths: dict = json.load(open("config.json", "r"))

class ErrorMessage:
    VAR_NOT_INIT = "variable '{}' is not initialized"
    VAR_NOT_FOUND = "variable '{}' is not found"
    VAR_NOT_STORED = "result must be stored in a variable"
    COMMAND_UNKNOWN = "unknown command '{}'"
    OPERAND_INVALID = "invalid operand '{}'"
    SYNTAX_FAILURE = "syntax failure in '{}'"
    ARITHMETIC_SYNTAX_FAILURE = "syntax failure in arithmetic operation '{}'"
    NUMBER_EXPECTED = "expected a number"
    ZERO_DIVISION = "division by zero"
    FILE_NOT_FOUND = "file '{}' not found"
    WRONG_LINE = "wrong line goto"
    RUNTIME_ERROR = "runtime error, infinite loop"

    @classmethod
    def print(cls, message: str, target: str = ""):
        print(f"Error: {message.format(target)}", end=" ")

memory: dict = {}

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
        if not s in memory:
            ErrorMessage.print(ErrorMessage.VAR_NOT_INIT, s)
            sys.exit(1)
        return memory[s]
    else:
        ErrorMessage.print(ErrorMessage.OPERAND_INVALID, s)
        sys.exit(1)

def validate_tokens(command: str, tokens: list[str], expected_len: int, message: str = ErrorMessage.SYNTAX_FAILURE):
    if len(tokens) != expected_len:
        ErrorMessage.print(message, command)
        sys.exit(1)

def go_to_line(line: int, current_index: IntReference):
    if line == current_index.value:
        ErrorMessage.print(ErrorMessage.RUNTIME_ERROR)
        sys.exit(1)
    current_index.value = line
        

def validate_variable(var: str):
    if not is_variable(var):
        ErrorMessage.print(ErrorMessage.VAR_NOT_FOUND, var)
        sys.exit(1)

def execute(lines: list[str], index: IntReference):
    if index.value < 0 or index.value > len(lines):
        ErrorMessage.print(ErrorMessage.WRONG_LINE)
        sys.exit(1)
    
    line = lines[index.value]
    
    if not line:
        index.value += 1
        return

    tokens = line.split()
    command = tokens[0].upper()

    match command:
        case "READ":
            if len(tokens) != 2 or not is_variable(tokens[1]):
                ErrorMessage.print(ErrorMessage.SYNTAX_FAILURE, command)
                sys.exit(1)
            var = tokens[1]
            print(f"{var} = ", end="")
            val = str(input())
            if not is_number(val):
                ErrorMessage.print(ErrorMessage.NUMBER_EXPECTED)
                sys.exit(1)
            memory[var] = float(val)

        case "WRITE":
            validate_tokens(command, tokens, 2)
            var = tokens[1]
            if is_variable(var):
                if var not in memory:
                    ErrorMessage.print(ErrorMessage.VAR_NOT_FOUND, var)
                    sys.exit(1)
                print(f"{var} = {memory[var]}")
            elif is_number(var):
                print(var)
            else:
                ErrorMessage.print(ErrorMessage.SYNTAX_FAILURE, command)
                sys.exit(1)

        case "COPY":
            validate_tokens(command, tokens, 3)
            src, dst = tokens[1], tokens[2]
            validate_variable(dst)
            memory[dst] = get_value(src)

        case  "ADD" | "SUB" | "MUL" | "DIV":
            validate_tokens(command, tokens, 4, ErrorMessage.ARITHMETIC_SYNTAX_FAILURE)
            _, left, right, dst = tokens
            validate_variable(dst)

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
                    ErrorMessage.print(ErrorMessage.ZERO_DIVISION)
                    sys.exit(1)
                memory[dst] = lval / rval

        case "GOTO":
            validate_tokens(command, tokens, 2)
            line = int(get_value(tokens[1]))
            go_to_line(line, index)
            return

        case "GOTOIF":
            validate_tokens(command, tokens, 3)
            
            val = get_value(tokens[1])
            line = int(get_value(tokens[2]))

            if val > 0:
                go_to_line(line, index)
                return 

        case "GOTOIFNOT":
            validate_tokens(command, tokens, 3)
            
            val = get_value(tokens[1])
            line = int(get_value(tokens[2]))

            if not val > 0:
                go_to_line(line, index)
                return

        case _:
            ErrorMessage.print(ErrorMessage.COMMAND_UNKNOWN, tokens[0])
            sys.exit(1)
        
    index.value += 1

def run(filename: str):
    lines = list[str]()
    i = IntReference(0)
    try:
        with open(filename, "r") as file:
            lines = file.read().split(sep="\n")
            while i.value < len(lines):
                try:
                    execute(lines, i)
                except SystemExit:
                    print(f"(line {i.value + 1}).")
                    sys.exit(1)
                    
    except FileNotFoundError:
        ErrorMessage.print(ErrorMessage.FILE_NOT_FOUND, filename)
        sys.exit(1)

if __name__ == "__main__":
    run(paths.get("path_raw"))