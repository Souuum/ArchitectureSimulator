import re
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import copy


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

    def copy(self):
        new_memory = Memory(len(self.mem))
        new_memory.mem = copy.deepcopy(self.mem)
        return new_memory


class Stack:
    def __init__(self, size):
        self.stack = [None] * size
        self.sp = 0

    def push(self, value):
        self.stack[self.sp] = value
        self.sp += 1

    def pop(self):
        self.sp -= 1
        self.stack.pop(self.sp)
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
        self.operations = {'LDA': self.lda,
                           'STR': self.str,
                           'PUSH': self.push,
                           'POP': self.pop,
                           'AND': self.and_,
                           'OR': self.or_,
                           'NOT': self.not_,
                           'ADD': self.add,
                           'SUB': self.sub,
                           'DIV': self.div,
                           'MUL': self.mul,
                           'MOD': self.mod,
                           'INC': self.inc,
                           'DEC': self.dec,
                           'BEQ': self.beq,
                           'BNE': self.bne,
                           'BBG': self.bbg,
                           'BSM': self.bsm,
                           'JMP': self.jmp,
                           'HLT': self.hlt,
                           'SRR': self.srr,
                           'SRL': self.srl,
                           }

    # Part 1

    # 1. LDA <reg1> <reg2>/<var>/<const>
    # Load register reg1 with the contents of either the contents of reg2, or the memory var or a constant const.
    #  Memory regions loads (load into a variable, for instance) are NOT ALLOWED.

    def lda(self, reg1, reg2):

        # check if reg1 and reg2 are registers (T0ˆ9)
        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', str(reg2)):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg2].value

        # if reg2 is a variable => number as string
        elif re.match(r'\d+', str(reg2)):
            self.registers[reg1].value = self.memory.read(int(reg2))
        # if reg2 is a constant
        else:
            self.registers[reg1].value = int(reg2)

    # 2. 2. STR <var> <reg>/<const>
    # Store in the memory position referred by var the value of register reg or a constant const.
    # Register stores (store into register t0, for instance) are NOT ALLOWED.

    def str(self, var, reg):

        var = int(var)
        # if reg is a register
        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
            self.memory.write(var, self.registers[reg].value)
        # if reg is a constant
        else:
            self.memory.write(var, int(reg))

    # 3. PUSH <reg>/<var>/<const>
    # Push to the top of the stack the contents of reg or var or a constant const

    def push(self, reg):

        # if reg is a register
        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
            self.stack.push(self.registers[reg].value)
        # if reg is a variable
        elif re.match(r'\d+', reg):
            self.stack.push(self.memory.read(int(reg)))
        # if reg is a constant
        else:
            self.stack.push(reg)

    # 4. POP <reg>
    # Pop from the top of the stack and store the value on reg. Storing in a memory region is NOT ALLOWED.
    def pop(self, reg):
        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
            self.registers[reg].value = self.stack.pop()

    # 5. AND <reg1> <reg2>/<var>/<const>
    # Performs a logical AND operation between reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def and_(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg1].value & self.registers[reg2].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.registers[reg1].value & self.memory.read(
                int(reg2))

        # if reg2 is a constant
        else:
            self.registers[reg1].value = self.registers[reg1].value & self.memory.read(
                reg2)

    # 6. OR <reg1> <reg2>/<var>/<const>
    # Performs a logical OR operation between reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def or_(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg1].value | self.registers[reg2].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.registers[reg1].value | self.memory.read(
                reg2)

        # if reg2 is a constant
        else:
            self.registers[reg1].value = self.registers[reg1].value | int(reg2)

    # 7. NOT <reg>
    # Performs a logical NOT operation on register reg and store the result on register reg.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def not_(self, reg):

        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
            self.registers[reg].value = ~self.registers[reg].value

    # 8. ADD <reg1> <reg2>/<var>/<const>
    # Performs the addition operation of reg1 and a register reg2, a variable var or a constant const,
    # and store the result on register reg1. Memory regions stores (store result into a variable, for
    # instance) are NOT ALLOWED.

    def add(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg1].value + \
                self.registers[reg2].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.registers[reg1].value + \
                self.memory.read(reg2)
        # if reg2 is a constant
        else:
            self.registers[reg1].value = self.registers[reg1].value + int(reg2)

    # 9. SUB <reg1> <reg2>/<var>/<const>
    # Performs the subtraction operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # The operation is given by second argument minus the first argument (i.e., reg2 – reg1).
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def sub(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg2].value - \
                self.registers[reg1].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.memory.read(reg2) - \
                self.registers[reg1].value

        # if reg2 is a constant
        else:
            self.registers[reg1].value = int(reg2) - \
                self.registers[reg1].value

    # 10. DIV <reg1> <reg2>/<var>/<const>
    # Performs the integer division operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # The operation is given by second argument divided by the first argument (i.e., reg2 / reg1).
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def div(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg2].value / \
                self.registers[reg1].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.memory.read(reg2) / \
                self.registers[reg1].value

        # if reg2 is a constant
        else:
            self.registers[reg1].value = int(reg2) / \
                self.registers[reg1].value

    # 11. MUL <reg1> <reg2>/<var>/<const>
    # Performs the multiplication operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def mul(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg2].value * \
                self.registers[reg1].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.memory.read(reg2) * \
                self.registers[reg1].value

        # if reg2 is a constant
        else:
            self.registers[reg1].value = int(reg2) * \
                self.registers[reg1].value

    # 12. MOD <reg1> <reg2>/<var>/<const>
    # Performs the integer modulo operation of reg1 and a register reg2,
    # a variable var or a constant const, and store the result on register reg1.
    # The operation is given by second argument modulo the first argument (i.e., reg2 mod reg1).
    # Memory regions stores (store result into a variable, for instance) are NOT ALLOWED.

    def mod(self, reg1, reg2):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])

        # if reg2 is a register
        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            self.registers[reg1].value = self.registers[reg2].value % \
                self.registers[reg1].value

        # if reg2 is a variable
        elif re.match(r'\d+', reg2):
            self.registers[reg1].value = self.memory.read(reg2) % \
                self.registers[reg1].value

        # if reg2 is a constant
        else:
            self.registers[reg1].value = int(reg2) % \
                self.registers[reg1].value

    # 13. INC <reg>
    # Increments the value of register reg.
    # Memory increments (incrementing a variable, for instance) are NOT ALLOWED.

    def inc(self, reg):

        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
        self.registers[reg].value += 1

    # 14. DEC <reg>
    # Decrements the value of register reg.
    # Memory increments (decrementing a variable, for instance) are NOT ALLOWED.

    def dec(self, reg):

        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
        self.registers[reg].value -= 1

    # 15. BEQ <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If they are equal, jump to the address defined by the label LABEL

    def beq(self, reg1, reg2, label):
        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])
            val1 = self.registers[reg1].value

        elif re.match(r'\d+', reg1):
            val1 = self.memory.read(reg1)

        else:
            val1 = int(reg1)

        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            val2 = self.registers[reg2].value

        elif re.match(r'\d+', reg2):
            val2 = self.memory.read(reg2)

        else:
            val2 = int(reg2)

        if val1 == val2:
            self.program_counter.value = label

    # 16. BNE <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If they are different, jump to the address defined by the label LABEL

    def bne(self, reg1, reg2, label):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])
            val1 = self.registers[reg1].value

        elif re.match(r'\d+', reg1):
            val1 = self.memory.read(reg1)

        else:
            val1 = int(reg1)

        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            val2 = self.registers[reg2].value

        elif re.match(r'\d+', reg2):
            val2 = self.memory.read(reg2)

        else:
            val2 = int(reg2)

        if val1 != val2:
            self.program_counter.value = label

    # 17. BBG <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If the first parameter is bigger than the second parameter,
    # jump to the address defined by the label LABEL

    def bbg(self, reg1, reg2, label):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])
            val1 = self.registers[reg1].value

        elif re.match(r'\d+', reg1):
            val1 = self.memory.read(reg1)

        else:
            val1 = int(reg1)

        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            val2 = self.registers[reg2].value

        elif re.match(r'\d+', reg2):
            val2 = self.memory.read(reg2)

        else:
            val2 = int(reg2)

        if val1 > val2:
            self.program_counter.value = label

    # 18. BSM <reg1>/<var1>/<const1> <reg2>/<var2>/<const2> <LABEL>
    # Performs a comparison between two values, given by registers, variables or constants.
    # Any combination is permitted. If the first parameter is smaller than the second parameter,
    #  jump to the address defined by the label LABEL

    def bsm(self, reg1, reg2, label):

        if re.match(r'T\d+', reg1):
            reg1 = int(reg1[1:])
            val1 = self.registers[reg1].value

        elif re.match(r'\d+', reg1):
            val1 = self.memory.read(reg1)

        else:
            val1 = int(reg1)

        if re.match(r'T\d+', reg2):
            reg2 = int(reg2[1:])
            val2 = self.registers[reg2].value

        elif re.match(r'\d+', reg2):
            val2 = self.memory.read(reg2)

        else:
            val2 = int(reg2)

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

        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
            self.registers[reg].value = self.registers[reg].value << int(const)

    # b. SRR <reg> <const>
    # This operation takes the value in reg and performs a logical shift right of the number of bits defined
    # by the constant const. For instance, the value 1000 right shifted 1 time becomes 0100.

    def srr(self, reg, const):

        if re.match(r'T\d+', reg):
            reg = int(reg[1:])
            self.registers[reg].value = self.registers[reg].value >> int(const)


class Simulator:
    def __init__(self):
        self.registers = [Register() for _ in range(4)]
        self.memory = Memory(4096)
        self.stack = Stack(4096)
        self.program_counter = ProgramCounter()
        self.alu = ALU(self.registers, self.memory,
                       self.stack, self.program_counter)

    def load_program(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        state = "start"
        program = []
        memory = {}

        i = 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith("!"):
                continue

            if line.startswith("#DATA"):
                state = "data"
                continue

            if line.startswith("#CODE"):
                state = "code"
                continue

            if state == "data":
                variable, value = re.split(r'\s+', line)
                memory[variable] = {'value': int(value), 'indice': i}
                i += 1
            elif state == "code":
                program.append(line)

        # Initialize memory with the loaded variable values
        for var, value in memory.items():
            self.memory.write(value['indice'], value['value'])

        print("program loaded")

        return program, memory

    def execute_program(self, program, memory):
        self.program_counter.pc = self.program_counter.pc

        instruction = program[self.program_counter.pc]
        tokens = re.split(r'\s+', instruction)

        operation = tokens[0]

        for i in range(1, len(tokens)):
            print("token: ", tokens[i])
            # check if a token is a register

            if re.match(r'T\d+', tokens[i]):
                print("found register")
            # else if a token is a variable (start with a letter)
            elif re.match(r'[a-zA-Z]+', tokens[i]):
                print("found variable")
                # check if it is A+n or A-n
                if re.match(r'[a-zA-Z]+\+\d+', tokens[i]):
                    print("found indirect addressing")
                    var, value = re.split(r'\+', tokens[i])
                    tokens[i] = str(memory[var]['indice'] + int(value))
                elif re.match(r'[a-zA-Z]+\-\d+', tokens[i]):
                    print("found indirect addressing")
                    var, value = re.split(r'\-', tokens[i])
                    tokens[i] = str(memory[var]['indice'] - int(value))

                else:
                    tokens[i] = str(memory[tokens[i]]['indice'])
            # else if a token is a constant (start with a number)
            else:
                print("found constant")
                tokens[i] = int(tokens[i])

        print(tokens[1:])

        # look if operations are in the list of operations in ALU and execute the corresponding function
        if operation in self.alu.operations.keys():
            self.alu.operations[operation](
                *tokens[1:])
        else:
            print("Error: Operation not found")

        print('register')
        for r in self.registers:
            print(r.value)

        print('memory')
        for i in range(0, 3):
            print(self.memory.read(i))

        # Handle instructions ...
        self.program_counter.next()

        # update memory variable
        for var, value in memory.items():
            memory[var]['value'] = self.memory.read(value['indice'])

        return memory


def main():

    simulator = Simulator()
    root = tk.Tk()
    root.title("Assembly Simulator")

    # Add this button to the interface

    program, memory, previous_states = [], [], []

    instructions_frame = ttk.LabelFrame(root, text="Instructions")
    instructions_frame.grid(row=0, column=0, padx=10, pady=10)

    memory_frame = ttk.LabelFrame(root, text="Memory")
    memory_frame.grid(row=1, column=0, padx=10, pady=10)

    registers_frame = ttk.LabelFrame(root, text="Registers")
    registers_frame.grid(row=0, column=1, padx=10, pady=10)

    stack_frame = ttk.LabelFrame(root, text="Stack")
    stack_frame.grid(row=1, column=1, padx=10, pady=10)

    instructions_text = tk.Text(
        instructions_frame, wrap=tk.WORD, height=10, width=30)
    instructions_text.pack(padx=10, pady=10)
    for i in program:
        instructions_text.insert(tk.END, i + "\n")

    memory_text = tk.Text(memory_frame, wrap=tk.WORD, height=10, width=30)
    memory_text.pack(padx=10, pady=10)

    registers_text = tk.Text(
        registers_frame, wrap=tk.WORD, height=10, width=30)
    registers_text.pack(padx=10, pady=10)
    registers_text.insert(tk.END, [s.value for s in simulator.alu.registers])

    stack_text = tk.Text(
        stack_frame, wrap=tk.WORD, height=10, width=30)
    stack_text.pack(padx=10, pady=10)
    stack_text.insert(
        tk.END, [s for s in simulator.alu.stack.stack if s != None])

    def on_step_click():

        if simulator.program_counter.pc == len(program):
            print("Program terminated")
            return

        nonlocal memory, previous_states

        # saving current states
        current_state = {
            'program': list(program),
            'mem': copy.deepcopy(memory),
            'sim_mem': copy.deepcopy(simulator.memory),
            'registers': [r.value for r in simulator.registers],
        }

        previous_states.append(current_state)

        # Handle instructions ...

        memory = simulator.execute_program(program, memory)

        # Clear the existing content of the Text widgets
        instructions_text.delete('1.0', tk.END)
        memory_text.delete('1.0', tk.END)
        registers_text.delete('1.0', tk.END)

        # Update the Text widgets with the new content
        keys = list(memory.keys())
        # update instructions
        for i in program:
            instructions_text.insert(tk.END, i + "\n")

        # update registers
        for i in range(0, len(simulator.registers)):
            registers_text.insert(tk.END, "T" + str(i) + " " + str(
                simulator.registers[i].value) + "\n")

        # update memory
        for i in range(0, len(keys)):
            memory_text.insert(tk.END, keys[i] + " " + str(
                memory[keys[i]]['value']) + "\n")

        # update stack
        stack_text.delete('1.0', tk.END)
        stack_text.insert(
            tk.END, [s for s in simulator.alu.stack.stack if s != None])

        # update program counter label
        count.config(text="step " + str(simulator.program_counter.pc))

        pass

    def on_reverse_step_click():
        nonlocal memory, previous_states, simulator, program

        if simulator.program_counter.pc == 0:
            return
        if not previous_states:
            return

        last_state = previous_states.pop()
        program[:] = last_state['program']
        simulator.memory = last_state['sim_mem']
        for i, register_value in enumerate(last_state['registers']):
            simulator.registers[i].value = register_value

        # Clear the existing content of the Text widgets
        instructions_text.delete('1.0', tk.END)
        memory_text.delete('1.0', tk.END)
        registers_text.delete('1.0', tk.END)

        simulator.program_counter.pc = simulator.program_counter.pc - 1

        # Update the Text widgets with the new content
        # update instructions
        for i in program:
            instructions_text.insert(tk.END, i + "\n")

        # update registers
        for i in range(0, len(simulator.registers)):
            registers_text.insert(tk.END, "T" + str(i) + " " + str(
                simulator.registers[i].value) + "\n")

        keys = list(memory.keys())

        # update memory
        for i in range(0, len(keys)):
            memory_text.insert(tk.END, keys[i] + " " + str(
                last_state['mem'][keys[i]]['value']) + "\n")

        # update stack
        stack_text.delete('1.0', tk.END)
        stack_text.insert(
            tk.END, [s for s in simulator.alu.stack.stack if s != None])

        # update program counter label
        count.config(text="step " + str(simulator.program_counter.pc))

    def load_file_button_click():
        nonlocal program, memory, simulator
        file_path = filedialog.askopenfilename(
            filetypes=[("Assembly files", "*.asm"), ("All files", "*.*")])

        if file_path:
            simulator = Simulator()
            program, memory = simulator.load_program(file_path)

            # Clear the existing content of the Text widgets
            instructions_text.delete('1.0', tk.END)
            memory_text.delete('1.0', tk.END)
            registers_text.delete('1.0', tk.END)
            stack_text.delete('1.0', tk.END)
            count.config(text="step " + str(simulator.program_counter.pc))

            # Update the Text widgets with the new content
            keys = list(memory.keys())
            # update instructions
            for i in program:
                instructions_text.insert(tk.END, i + "\n")

            # update registers
            for i in range(0, len(simulator.registers)):
                registers_text.insert(tk.END, "T" + str(i) + " " + str(
                    simulator.registers[i].value) + "\n")

            # update memory
            for i in range(0, len(memory)):
                memory_text.insert(tk.END, keys[i] + " " + str(
                    simulator.memory.read(i)) + "\n")

    # run every instruction

    def on_run_click():

        if simulator.program_counter.pc == len(program):
            print("Program terminated")
            return

        nonlocal memory, previous_states

        # saving current states
        current_state = {
            'program': list(program),
            'mem': copy.deepcopy(memory),
            'sim_mem': copy.deepcopy(simulator.memory),
            'registers': [r.value for r in simulator.registers],
        }

        previous_states.append(current_state)

        # Handle instructions ...

        while simulator.program_counter.pc != len(program):
            memory = simulator.execute_program(program, memory)

        # Clear the existing content of the Text widgets
        instructions_text.delete('1.0', tk.END)
        memory_text.delete('1.0', tk.END)
        registers_text.delete('1.0', tk.END)

        # Update the Text widgets with the new content
        keys = list(memory.keys())
        # update instructions
        for i in program:
            instructions_text.insert(tk.END, i + "\n")

        # update registers
        for i in range(0, len(simulator.registers)):
            registers_text.insert(tk.END, "T" + str(i) + " " + str(
                simulator.registers[i].value) + "\n")

        # update memory
        for i in range(0, len(keys)):
            memory_text.insert(tk.END, keys[i] + " " + str(
                memory[keys[i]]['value']) + "\n")

        # update stack
        stack_text.delete('1.0', tk.END)
        stack_text.insert(
            tk.END, [s for s in simulator.alu.stack.stack if s != None])

        # update program counter label
        count.config(text="step " + str(simulator.program_counter.pc))

        pass

    step_button = ttk.Button(root, text="Step", command=on_step_click)
    step_button.grid(row=2, column=0, pady=10)

    load_button = tk.Button(root, text="Load File",
                            command=load_file_button_click)
    load_button.grid(row=3, column=0, padx=10, pady=10)
    # reverse_step_button = ttk.Button(
    #     root, text="Reverse Step", command=on_reverse_step_click)
    # reverse_step_button.grid(row=2, column=1, pady=10)

    run_button = ttk.Button(root, text="Run", command=on_run_click)
    run_button.grid(row=2, column=1, pady=10)

    count = ttk.Label(root, text="step 0")
    count.grid(row=3, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":

    main()
