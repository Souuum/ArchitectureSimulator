class Register:
    def __init__(self):
        self.value = 0


class Memory:
    def __init__(self, size):
        self.mem = [0] * size

    def read(self, address):
        return self.mem[address]

    def write(self, address, value):
        self.mem[address] = value


class Stack:
    def __init__(self, size):
        self.stack = [0] * size
        self.sp = 0

    def push(self, value):
        self.stack[self.sp] = value
        self.sp += 1

    def pop(self):
        self.sp -= 1
        return self.stack[self.sp]


class ProgramCounter:
    def __init__(self):
        self.pc = 0

    def next(self):
        self.pc += 1

    def jump(self, address):
        self.pc = address


class ALU:
    def __init__(self, registers, memory, stack, program_counter):
        self.registers = registers
        self.memory = memory
        self.stack = stack
        self.program_counter = program_counter

    # Part 1

    # 1. LDA <reg1> <reg2>/<var>/<const>
    # Load register reg1 with the contents of either the contents of reg2, or the memory var or a constant const.
    #  Memory regions loads (load into a variable, for instance) are NOT ALLOWED.

    def lda(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.memory.read(var)
            else:
                self.registers[reg1].value = const
        else:
            self.registers[reg1].value = self.registers[reg2].value

    # 2. 2. STR <var> <reg>/<const>
    # Store in the memory position referred by var the value of register reg or a constant const.
    # Register stores (store into register t0, for instance) are NOT ALLOWED.

    def str(self, var, reg, const):
        if reg == None:
            self.memory.write(var, const)
        else:
            self.memory.write(var, self.registers[reg].value)

    # 3. PUSH <reg>/<var>/<const>
    # Push to the top of the stack the contents of reg or var or a constant const

    def push(self, reg, var, const):
        if reg == None:
            if var != None:
                self.stack.push(self.memory.read(var))
            else:
                self.stack.push(const)
        else:
            self.stack.push(self.registers[reg].value)

    # 4. POP <reg>
    # Pop from the top of the stack and store the value on reg. Storing in a memory region is NOT ALLOWED.
    def pop(self, reg):
        self.registers[reg].value = self.stack.pop()

    # 5. AND <reg1> <reg2>/<var>/<const>
    # Performs a logical AND operation between reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def and_(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.registers[reg1].value & self.memory.read(
                    var)
            else:
                self.registers[reg1].value = self.registers[reg1].value & const
        else:
            self.registers[reg1].value = self.registers[reg1].value & self.registers[reg2].value

    # 6. OR <reg1> <reg2>/<var>/<const>
    # Performs a logical OR operation between reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def or_(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.registers[reg1].value | self.memory.read(
                    var)
            else:
                self.registers[reg1].value = self.registers[reg1].value | const
        else:
            self.registers[reg1].value = self.registers[reg1].value | self.registers[reg2].value

    # 7. NOT <reg>
    # Performs a logical NOT operation on register reg and store the result on register reg.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def not_(self, reg):
        self.registers[reg].value = ~self.registers[reg].value

    # 8. ADD <reg1> <reg2>/<var>/<const>
    # Performs the addition operation of reg1 and a register reg2, a variable var or a constant const,
    # and store the result on register reg1. Memory regions stores (store result into a variable, for
    # instance) are NOT ALLOWED.

    def add(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.registers[reg1].value + self.memory.read(
                    var)
            else:
                self.registers[reg1].value = self.registers[reg1].value + const
        else:
            self.registers[reg1].value = self.registers[reg1].value + \
                self.registers[reg2].value

    # 9. SUB <reg1> <reg2>/<var>/<const>
    # Performs the subtraction operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # The operation is given by second argument minus the first argument (i.e., reg2 – reg1).
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def sub(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.memory.read(
                    var) - self.registers[reg1].value
            else:
                self.registers[reg1].value = const - self.registers[reg1].value
        else:
            self.registers[reg1].value = self.registers[reg2].value - \
                self.registers[reg1].value

    # 10. DIV <reg1> <reg2>/<var>/<const>
    # Performs the integer division operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # The operation is given by second argument divided by the first argument (i.e., reg2 / reg1).
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def div(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.memory.read(
                    var) // self.registers[reg1].value
            else:
                self.registers[reg1].value = const // self.registers[reg1].value
        else:
            self.registers[reg1].value = self.registers[reg2].value // self.registers[reg1].value

    # 11. MUL <reg1> <reg2>/<var>/<const>
    # Performs the multiplication operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def mul(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.registers[reg1].value * self.memory.read(
                    var)
            else:
                self.registers[reg1].value = self.registers[reg1].value * const
        else:
            self.registers[reg1].value = self.registers[reg1].value * \
                self.registers[reg2].value

    # 12. MOD <reg1> <reg2>/<var>/<const>
    # Performs the integer modulo operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # The operation is given by second argument modulo the first argument (i.e., reg2 mod reg1).
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def mod(self, reg1, reg2, var, const):
        if reg2 == None:
            if var != None:
                self.registers[reg1].value = self.memory.read(
                    var) % self.registers[reg1].value
            else:
                self.registers[reg1].value = const % self.registers[reg1].value
        else:
            self.registers[reg1].value = self.registers[reg2].value % self.registers[reg1].value

    # 13. INC <reg>
    # Increments the value of register reg.
    # Memory increments (incrementing a variable, for instance) are NOT ALLOWED.

    def inc(self, reg):
        self.registers[reg].value += 1

    # 14. DEC <reg>
    # Decrements the value of register reg.
    # Memory increments (decrementing a variable, for instance) are NOT ALLOWED.

    def dec(self, reg):
        self.registers[reg].value -= 1

    # 15. BEQ <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If they are equal, jump to the address defined by the label LABEL

    def beq(self, reg1, var1, const1, reg2, var2, const2, label):
        if reg1 == None:
            if var1 != None:
                val1 = self.memory.read(var1)
            else:
                val1 = const1
        else:
            val1 = self.registers[reg1].value

        if reg2 == None:
            if var2 != None:
                val2 = self.memory.read(var2)
            else:
                val2 = const2
        else:
            val2 = self.registers[reg2].value

        if val1 == val2:
            self.program_counter.value = label

    # 16. BNE <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If they are different, jump to the address defined by the label LABEL

    def bne(self, reg1, var1, const1, reg2, var2, const2, label):
        if reg1 == None:
            if var1 != None:
                val1 = self.memory.read(var1)
            else:
                val1 = const1
        else:
            val1 = self.registers[reg1].value

        if reg2 == None:
            if var2 != None:
                val2 = self.memory.read(var2)
            else:
                val2 = const2
        else:
            val2 = self.registers[reg2].value

        if val1 != val2:
            self.program_counter.value = label

    # 17. BBG <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If the first parameter is bigger than the second parameter,
    # jump to the address defined by the label LABEL

    def bbg(self, reg1, var1, const1, reg2, var2, const2, label):
        if reg1 == None:
            if var1 != None:
                val1 = self.memory.read(var1)
            else:
                val1 = const1
        else:
            val1 = self.registers[reg1].value

        if reg2 == None:
            if var2 != None:
                val2 = self.memory.read(var2)
            else:
                val2 = const2
        else:
            val2 = self.registers[reg2].value

        if val1 > val2:
            self.program_counter.value = label

    # 18. BSM <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If the first parameter is smaller than the second parameter,
    #  jump to the address defined by the label LABEL

    def bsm(self, reg1, var1, const1, reg2, var2, const2, label):
        if reg1 == None:
            if var1 != None:
                val1 = self.memory.read(var1)
            else:
                val1 = const1
        else:
            val1 = self.registers[reg1].value

        if reg2 == None:
            if var2 != None:
                val2 = self.memory.read(var2)
            else:
                val2 = const2
        else:
            val2 = self.registers[reg2].value

        if val1 < val2:
            self.program_counter.value = label

    # 19. JMP <LABEL>
    # Jump to the address defined by the label LABEL

    def jmp(self, label):
        self.program_counter.value = label

    # 20. HLT
    # End the program execution.

    def hlt(self):
        self.program_counter.value = -1

    # Part 2

    # a. SRL <reg> <const>
    # This operation takes the value in reg and performs a logical shift left of the number of bits defined
    #  by the constant const. For instance, the value 0001 left shifted 1 time becomes 0010.

    def srl(self, reg, const):
        self.registers[reg].value = self.registers[reg].value >> const

    # b. SRR <reg> <const>
    # This operation takes the value in reg and performs a logical shift right of the number of bits defined
    # by the constant const. For instance, the value 1000 right shifted 1 time becomes 0100.

    def srr(self, reg, const):
        self.registers[reg].value = self.registers[reg].value << const


class Simulator:
    def __init__(self):
        self.registers = [Register() for _ in range(4)]
        self.memory = Memory(4096)
        self.stack = Stack(4096)
        self.program_counter = ProgramCounter()
        self.alu = ALU(self.registers, self.memory,
                       self.stack, self.program_counter)

    def load_program(self, filename):
        # Load the assembly program from the file
        return

    def execute_program(self):
        # Execute the loaded program step by step
        return


def main():
    simulator = Simulator()
    simulator.load_program("assembly_program.txt")
    simulator.execute_program()


if __name__ == "__main__":
    main()
