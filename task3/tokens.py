class TokenType:
    KEYWORD = "KEYWORD"
    OPERATOR = "OPERATOR"
    SEPARATOR = "SEPARATOR"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"

class Token:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

KEYWORDS = {"read", "write", "if", "ifnot", "while", "whilenot"}
OPERATORS = {"+", "-", "*", "/", "=", ">"}
SEPARATORS = {";", "(", ")", "{", "}", "[", "]"}
