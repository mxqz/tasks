import sys
from tokens import *
from tokenizer import tokens
from int_reference import IntReference

token_values = [token.value for token in tokens]
tokens.reverse()
sentence = []
commands = list[str]()
temp_count = IntReference(0)


def generateCommand():
    pass


def handleBlock():
    while tokens:
        current = tokens[-1]
        match current.type:
            case TokenType.KEYWORD:
                match current.value:
                    case "read" | "write":
                        handleCommand()
                    case "if" | "ifnot" | "while" | "whilenot":
                        handleOperatorBlock()
            case TokenType.OPERATOR | TokenType.SEPARATOR | TokenType.NUMBER:
                raise SyntaxError("Expected command, identifier or block statement")
            case TokenType.IDENTIFIER:
                handleCommand()
            case TokenType.UNKNOWN:
                tokens.pop()
                raise SyntaxError("Token unknown")


def handleCommand():
    command = ""
    
    if tokens[-1].type == TokenType.IDENTIFIER:
        res = tokens.pop().value
        
        if not tokens:
            raise SyntaxError("Expected '=' operator, found end of file instead")
        if tokens.pop() != Token(TokenType.OPERATOR, "="):
            raise SyntaxError("Expected '=' operator")

        handleExpression(res)

    try:
        current = tokens.pop()
        operator = tokens.pop()
    except:
        raise SyntaxError("Expected '>' operator, found end of file instead")
    else:
        if operator != Token(TokenType.OPERATOR, ">"):
            raise SyntaxError("Expected '>' operator")
    
    
        
    match current.value:
        case "read":
            try:
                current = tokens.pop()
            except:
                raise SyntaxError("Expected an identifier, found end of file instead")
            
            if current.type != TokenType.IDENTIFIER:
                raise SyntaxError("Expected an identifier")
            
            command = f"READ {current.value}"
        
        case "write":
            try:
                current = tokens.pop()
            except:
                raise SyntaxError("Expected an identifier, found end of file instead")
            
            if current.type != TokenType.IDENTIFIER:
                raise SyntaxError("Expected an identifier")
            
            command = f"WRITE {current.value}"
        
        case _:
            raise SyntaxError("Unexpected command")

    current = tokens.pop()

    if current != Token(TokenType.SEPARATOR, ";"):
        raise SyntaxError("Expected ';'")
    
    commands.append(command)


def handleExpression(res = ""):
    tokens.pop()
    raise SyntaxError("Expression")

    while tokens:
        token = tokens.pop()
        if token.type == TokenType.IDENTIFIER or token.type == TokenType.NUMBER:
            sentence.append(token.value)
        elif token.value in ARITHMETICS:
            sentence.append(token.value)
        else:
            break
    
    name = ""
    lhs = ""
    rhs = ""

    if not res:
        res = f"t{temp_count.value}"
        temp_count.value += 1
    
    while sentence:
        obj = sentence.pop()
        match obj:
            case "+":
                name = "ADD"
                lhs = handleExpression()
                rhs = handleExpression()
            case "-":
                name = "SUB"
                lhs = handleExpression()
                rhs = handleExpression()
                
            case "*":
                name = "MUL"
                lhs = handleExpression()
                rhs = handleExpression()
            case "/":
                name = "DIV"
                lhs = handleExpression()
                rhs = handleExpression()
            case "(":
                return handleExpression()
            case ")":
                commands.append(f"{name} {lhs} {rhs} {res}")
            case _:
                return obj
    
    return res


def handleOperatorBlock():
    current = tokens.pop()
    
    try:
        separator = tokens.pop()
    except:
        raise SyntaxError("Expected '[]' statement block, found end of file instead")
    
    if separator != Token(TokenType.SEPARATOR, "["):
        raise SyntaxError("Expected '[]' statement block")

    handleExpression()
    command = ""

    match current.value:
        case "if":
            pass
        case "ifnot":
            pass
        case "while":
            pass
        case "whilenot":
            pass
    
    commands.append(command)
        

if __name__ == "__main__":    
    try:
        handleBlock()
    except SyntaxError as e:
        num = len(token_values) - len(tokens)
        spaces = 0
        
        for token in token_values[:num - 1]:
            spaces += len(token) + 1

        print(*token_values, sep=" ")
        print(" " * spaces + "^")
        print(f"{str(e)} (pos {num}).")
        
        sys.exit(0)
    
    for command in commands:
        print(command)
