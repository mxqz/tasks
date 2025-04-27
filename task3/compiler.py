program = ""

with open("program.txt", "r") as file:
    program = file.read()

# print(program, end="\n\n")

program = program.replace(" ", "")
program = program.replace("\n", "")

print(program, end="\n\n")

tokens = []
temp = ""

for i in program:
    match i:
        case ";" | "(" | ")" | "[" | "]" | "{" | "}" | "=" | "+" | "-" | "*" | "/":
            if temp:
                tokens.append(temp)
            tokens.append(i)
            temp = ""
        case ">":
            temp += i
            tokens.append(temp)
            temp = ""
        case _:
            temp += i

print(*tokens, end="\n\n")