test = "2 + 2 * 2"
tokens = test.split()
arg = []
op = []
temp = 0

for token in tokens:
    match token:
        case "=" | "+" | "-" | "*" | "/":
            op.append(token)
        case _:
            if token.isnumeric():
                arg.append(float(token))

print(f"{tokens}\n\n{arg}\n{op}\n")

def handle_expression(arg, op):
    while op:
        right = arg.pop()
        operation = op.pop()
        match operation:
            case "+":
                arg.append(handle_expression(arg, op) + right)
            case "-":
                arg.append(handle_expression(arg, op) - right) 
            case "*":
                left = arg.pop()
                arg.append(left * right)
            case "/":
                left = arg.pop()
                arg.append(left / right)
    
    return arg[-1]

def handle_expression_problem(arg, op):
    while op:
        right = arg.pop()
        left = arg.pop()
        operation = op.pop()
        match operation:
            case "+":
                arg.append(left + right)
            case "-":
                arg.append(left - right) 
            case "*":
                arg.append(left * right)
            case "/":
                arg.append(left / right)
    
    return arg[-1]

vars = handle_expression(arg, op)

print(vars)
