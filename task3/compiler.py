from tokens import Token, KEYWORDS, OPERATORS, SEPARATORS

program = ""

with open("program.txt", "r") as file:
    program = file.read()

# print(program, end="\n\n")

program = program.replace(" ", "")
program = program.replace("\n", "")

tokens = []
current = ""

print(program, end="\n\n")

def add_token(value):
    """Функція для визначення типу токена"""
    if not value:
        return

    if value in KEYWORDS:
        tokens.append(Token("KEYWORD", value))
    elif value in OPERATORS:
        tokens.append(Token("OPERATOR", value))
    elif value in SEPARATORS:
        tokens.append(Token("SEPARATOR", value))
    elif value.isidentifier():
        tokens.append(Token("IDENTIFIER", value))
    elif value.isdigit():
        tokens.append(Token("NUMBER", int(value)))
    else:
        try:
            float_val = float(value)
            tokens.append(Token("NUMBER", float_val))
        except ValueError:
            raise ValueError(f"Uknown token: {value}")


i = 0
while i < len(program):
    ch = program[i]

    if ch in OPERATORS or ch in SEPARATORS:
        add_token(current)
        current = ""
        tokens.append(Token(
            "OPERATOR" if ch in OPERATORS else "SEPARATOR", ch
        ))
        i += 1
        continue

    if ch == " ":
        add_token(current)
        current = ""
        i += 1
        continue

    current += ch
    i += 1

add_token(current)

for token in tokens:
    print(token)