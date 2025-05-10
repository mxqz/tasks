from tokens import *

tokens = list[Token]()

def add_token(value: str) -> None:
    """Token type evaluation function"""
    if not value:
        return

    token_type = ""

    if value in KEYWORDS:
        token_type = TokenType.KEYWORD
    elif value in OPERATORS:
        token_type = TokenType.OPERATOR
    elif value in SEPARATORS:
        token_type = TokenType.SEPARATOR
    elif value.isalpha():
        token_type = TokenType.IDENTIFIER
    else:
        try:
            _ = float(value)
        except ValueError:
            raise ValueError(f"Uknown token: {value}")
        else:
            token_type = TokenType.NUMBER
    
    tokens.append(Token(token_type, value))

program = ""

with open("program.txt", "r") as file:
    program = file.read()

program = program.replace(" ", "")
program = program.replace("\n", "")

current = ""

for ch in program:
    if ch in OPERATORS or ch in SEPARATORS:
        if current:
            add_token(current)
            current = ""
        add_token(ch)
    else:
        current += ch
add_token(current)

if __name__ == "__main__":
    print(program, end="\n\n")
    
    for token in tokens:
        print(token)
