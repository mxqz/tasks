from tokens import Token
from compiler import tokens

commands = []

def handleExpression(expr_tokens):
    expr_str = " ".join(str(token.value) for token in expr_tokens)  #<-- приймає список токенів
    commands.append(f"EVAL {expr_str}")                     #<-- EVAL означає обчилити вираз

def handleCommand(tokens, i):   #<-- обробляє команду, визначає її тип, переторює на команду для віртуалки
    token = tokens[i]   
                                                #тут по факту все компіпаст, тому шо кожен блок повинен пропустити дужки перші, другі, пробіли і тд. самої логіки мінімум
    if token.value == 'read':
        var = tokens[i+2]                       #<-- пропускаємо 2 токени перед командою READ
        commands.append(f"READ {var.value}")
        return i + 4                            #<-- пропускаємо 4 токени після команди READ

    elif token.value == 'write':
        var = tokens[i+2]
        commands.append(f"WRITE {var.value}")
        return i + 4                            #<-- пропускаємо 4 токени після команди WRITE

    elif token.value == 'if':
        i += 2                          #<-- пропуск перших дужок 
        condition_tokens = []
        while tokens[i].value != ']':
            condition_tokens.append(tokens[i])
            i += 1                          #<-- пропуск перших дужок
        handleExpression(condition_tokens)
        i += 1                          #<-- пропуск перших дужок
        i += 1                          #<-- пропуск других дужок
        label_end = f"ENDIF_{i}"
        commands.append(f"JZ {label_end}")
        i = handleBlock(tokens[i:]) + i
        commands.append(f"{label_end}:")
        return i + 1                            #<-- пропуск других дужок

    elif token.value == 'while':
        i += 2                          #<-- пропуск перших дужок
        condition_tokens = []
        start_label = f"WHILE_{i}"
        end_label = f"ENDWHILE_{i}"
        commands.append(f"{start_label}:")
        while tokens[i].value != ']':
            condition_tokens.append(tokens[i])
            i += 1                          #<-- пропуск перших дужок
        handleExpression(condition_tokens)
        i += 1                          #<-- пропуск перших дужок 
        i += 1                          #<-- пропуск перших дужок
        commands.append(f"JZ {end_label}")
        i = handleBlock(tokens[i:]) + i
        commands.append(f"JMP {start_label}")
        commands.append(f"{end_label}:")
        return i + 1                            #<-- пропуск других дужок
    
    elif token.type == 'IDENTIFIER' and tokens[i+1].value == '=':
        var_name = token.value
        expr_tokens = []
        i += 2
        while tokens[i].value != ';':
            expr_tokens.append(tokens[i])
            i += 1
        handleExpression(expr_tokens)
        commands.append(f"STORE {var_name}")
        return i + 1

    else:
        raise ValueError(f"Unknown command at token {i}: {token}")

def handleBlock(tokens): #<-- обробляє блоки if та while
    i = 0
    while i < len(tokens):
        if tokens[i].value == '}':
            return i 
        i = handleCommand(tokens, i)
    return i

if __name__ == "__main__":
    handleBlock(tokens)
    print("йоу~~~VM Commands~~~йоу")
    for cmd in commands:
        print(cmd)
