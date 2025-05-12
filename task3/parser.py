import sys
import json
from tokens import *
from tokenizer import tokens
from int_reference import IntReference

paths: dict = json.load(open("config.json", "r"))
token_values: list[str] = [token.value for token in tokens]
commands: list[str] = list[str]()
temp_count: IntReference = IntReference(0)
op: list[str] = list[str]()
arg: list[str] = list[str]()
tokens.reverse()

def priority(operator: str) -> int:
    power: int
    match operator:
        case "+":
            power = 1
        case "-":
            power = 1
        case "*":
            power = 2
        case "/":
            power = 2
        case _:
            raise ValueError(f"Invalid operator {operator}")
    return power


def generateCommand(res = ""):
    try:
        opr = op.pop()
        rhs = arg.pop()
        lhs = arg.pop()
    except:
        raise SyntaxError("Invalid expression")

    name = ""

    match opr:
        case "+":
            name = "ADD"
        case "-":
            name = "SUB"
        case "*":
            name = "MUL"
        case "/":
            name = "DIV"
        case _:
            raise ValueError(f"Invalid operator {opr}")
    
    if not res:
        res = f"t{temp_count.value}"
        temp_count.value += 1
    
    arg.append(res)
    command = f"{name} {lhs} {rhs} {res}"
    commands.append(command)


def handleBlock():
    internal = len(commands)
    while tokens:
        current = tokens[-1]
        match current.type:
            case TokenType.KEYWORD:
                match current.value:
                    case "read" | "write":
                        handleCommand()
                    case "if" | "ifnot" | "while" | "whilenot":
                        handleOperatorBlock()
            case TokenType.SEPARATOR:
                if current.value == "}" and internal:
                    return
                raise SyntaxError("Expected command, identifier or block statement")
            case TokenType.OPERATOR | TokenType.NUMBER:
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

        pre_count = len(commands)
        var = tokens[-1].value

        handleExpression(res)

        if pre_count == len(commands):
            command = f"COPY {var} {res}"
    else:
        current = tokens.pop()
        
        if not tokens or tokens.pop() != Token(TokenType.OPERATOR, ">"):
            raise SyntaxError("Expected '>' operator")

        match current.value:
            case "read":
                if not tokens or tokens.pop().type != TokenType.IDENTIFIER:
                    raise SyntaxError("Expected an identifier")
                
                command = f"READ {current.value}"
                
            case "write":
                if not tokens:
                    raise SyntaxError("Expected an expression")

                current = tokens[-1]
                dst = ""
                if current == Token(TokenType.SEPARATOR, "("):
                    dst = handleExpression()
                elif current.type in {TokenType.IDENTIFIER, TokenType.NUMBER}:
                    tokens.pop()
                    dst = current.value
                else:
                    raise SyntaxError("Expected an expression")
                
                command = f"WRITE {dst}"
            
            case _:
                raise SyntaxError("Unexpected command")

    if not tokens or tokens.pop() != Token(TokenType.SEPARATOR, ";"):
        raise SyntaxError("Expected ';'")
    
    if command:
        commands.append(command)


def handleExpression(res = ""):
    arg.clear()
    op.clear()
    
    while tokens:
        token = tokens[-1]
        if token.type in {TokenType.IDENTIFIER, TokenType.NUMBER}:
            arg.append(token.value)
        elif token.type == TokenType.OPERATOR and token.value in ARITHMETICS:
            while op:
                if not op[-1] in {"+", "-", "*", "/"}:
                    break
                if priority(op[-1]) < priority(token.value):
                    break
                generateCommand(res)
            op.append(token.value)
        elif token.value == "(":
            op.append(token.value)
        elif token.value == ")":
            while op[-1] != "(":
                generateCommand(res)
            if not op:
                raise SyntaxError("Invalid expression")
            if op[-1] != "(":
                raise SyntaxError("Invalid expression")
            op.pop()
        else:
            break
        
        tokens.pop()
    
    if len(arg) == 1 and len(op) == 0:
        return arg[0]

    while op:
        if op[-1] in {"(", ")"}:
            raise SyntaxError("Invalid expression")
        generateCommand(res)
    
    if res:
        return res

    if temp_count.value < 1:
        raise SyntaxError("Invalid expression")

    return f"t{temp_count.value - 1}"


def handleOperatorBlock():
    current = tokens.pop()
    
    if not tokens or tokens.pop() != Token(TokenType.SEPARATOR, "["):
        raise SyntaxError("Expected '[' to start a statement block")

    begin = len(commands)

    var = handleExpression()

    position = len(commands)
    
    command = ""

    match current.value:
        case "if":
            command = "GOTOIFNOT"
        case "ifnot":
            command = "GOTOIF"
        case "while":
            command = "GOTOIFNOT"
        case "whilenot":
            command = "GOTOIF"
        case _:
            raise SyntaxError("Unknown operator block")

    if not tokens or tokens.pop() != Token(TokenType.SEPARATOR, "]"):
        raise SyntaxError("Expected ']' to end a statement block")
     
    if not tokens or tokens.pop() != Token(TokenType.SEPARATOR, "{"):
        raise SyntaxError("Expected '{' to start a block body")
    
    commands.append("")

    handleBlock()

    if not tokens or tokens.pop() != Token(TokenType.SEPARATOR, "}"):
        raise SyntaxError("Expected '}' to end a block body")
    
    if current.value in ["while", "whilenot"]:
        commands.append(f"GOTO {begin}")

    end = len(commands)

    commands[position] = f"{command} {var} {end}"
        

if __name__ == "__main__":    
    open(paths.get("path_raw"), "w").close()
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
    
    with open(paths.get("path_raw"), "w") as file:
        for command in commands:
            file.write(command + "\n")
