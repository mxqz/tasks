class StackVM:
    def __init__(self):
        self.stack = []
        self.vars = {}

    def get_value(self, operand: str):
        if operand.isnumeric():
            return int(operand)
        if operand in self.vars:
            return self.stack[self.vars[operand]]
        else:
            raise ValueError(f"No variable {operand} declared")

    def execute(self, instruction):
        parts = instruction.split()
        op = parts[0]
        target = parts[len(parts) - 1]

        operands = parts[1:-1]

        if op == "COPY":
            result = self.get_value(operands[0])
        elif op == "ADD":
            result = self.get_value(operands[0]) + self.get_value(operands[1])
        elif op == "SUB":
            result = self.get_value(operands[0]) - self.get_value(operands[1])
        elif op == "MUL":
            result = self.get_value(operands[0]) * self.get_value(operands[1])
        elif op == "DIV":
            result = self.get_value(operands[0]) / self.get_value(operands[1])
        else:
            raise ValueError(f"Unknown operation: {op}")

        if not target in self.vars and str(target).isalpha():
            self.vars[target] = len(self.stack)
            self.stack.append(result)
        else:
            self.stack[self.vars[target]] = result

    def run(self, program):
        for instr in program:
            self.execute(instr)
            # self.dump_vars()
            self.dump_stack()

    def dump_vars(self):
        for var, val in self.vars.items():
            print(f"{var} = {val}")

    def dump_stack(self):
        print("Stack:", self.stack)


program = open("raw.txt", "r").readlines()


vm = StackVM()
vm.run(program)
