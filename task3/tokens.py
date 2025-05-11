class TokenType:
    KEYWORD = "KEYWORD"
    OPERATOR = "OPERATOR"
    SEPARATOR = "SEPARATOR"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    UNKNOWN = "UNKNOWN"

class Token:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
    
    def __ne__(self, other):
        return not self.__eq__(other)
    

KEYWORDS = {"read", "write", "if", "ifnot", "while", "whilenot"}
OPERATORS = {"+", "-", "*", "/", "=", ">"}
SEPARATORS = {";", "(", ")", "{", "}", "[", "]"}
ARITHMETICS = {"+", "-", "*", "/", "(", ")"}
