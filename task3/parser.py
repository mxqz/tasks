import sys
from tokens import *
from tokenizer import tokens, program, program_unformatted

tokens_original = [token.value for token in tokens]
tokens.reverse()
commands = list[str]()

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

def handleCommand():
    command = ""
    
    current = tokens.pop()
    
    try:
        operator = tokens.pop()
    except:
        if current.type == TokenType.KEYWORD:
            raise SyntaxError("Expected '>' operator, found end of file instead")
        else:
            raise SyntaxError("Expected '=' operator, found end of file instead")
    else:
        if current.type == TokenType.KEYWORD and operator != Token(TokenType.OPERATOR, ">"):
            raise SyntaxError("Expected '>' operator")
        elif current.type == TokenType.IDENTIFIER and operator != Token(TokenType.OPERATOR, "="):
            raise SyntaxError("Expected '=' operator")
        
        
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
                print("Expected an identifier")
            
            command = f"WRITE {current.value}"
        
        case _:
            handleExpression()
            command = f"COPY {1} {2}"
        
    current = tokens.pop()

    if current != Token(TokenType.SEPARATOR, ";"):
        raise SyntaxError("Expected ';'")
    
    commands.append(command)
            

def handleExpression():
    pass

def handleOperatorBlock():
    current = tokens.pop()
    
    try:
        separator = tokens.pop()
    except:
        raise SyntaxError("Expected '[]' statement block, found end of file instead")
    
    if separator != Token(TokenType.SEPARATOR, "["):
        raise SyntaxError("Expected '[]' statement block")

    handleExpression()

    match current.value:
        case "if":
            pass
        case "ifnot":
            pass
        case "while":
            pass
        case "whilenot":
            pass
        

if __name__ == "__main__":    
    try:
        handleBlock()
    except SyntaxError as e:
        num = len(tokens_original) - len(tokens)
        spaces = 0
        
        for i in range(num):
            spaces += len(tokens_original[i]) + 1
        
        print(*tokens_original, sep=" ")
        print(" " * spaces + "^")
        print(f"{str(e)} (pos {num}).")
        
        sys.exit(0)
    
    for command in commands:
        print(command)
