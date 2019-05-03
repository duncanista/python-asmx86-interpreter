#encoding: utf-8
import sys

stack = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
variables = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
instructions = ["MOV", "CMP", "PUSH", "PULL", "DIV", "MUL", "SUB", "ADD", "INC", "DEC"]
jumps = ["JNE", "JE", "JMP"]

def read():
    it = iter(sys.stdin.read().splitlines())
    line = next(it)
    file = []
    while (True):
        try:
            line = next(it).split()
            if (line):
                if (";" in line):
                    index = line.index(";")
                    line = line[:index]
                    if (line):
                        file.append(line)
                else:
                    line = " ".join(line)
                    if (";" in line):
                        line.split()
                        index = 0
                        for i in range(len(line)):
                            if (";" in line[i]):
                                index = i
                        line = line[:index]
                        if (line):
                            file.append(line)
                    else:
                        file.append(line.split())
        except:
            break

    instructions = [item for line in file for item in line]
    #print(instructions)
    #print("")



    return file

def isRegister(value):
    return bool(variables.get(value))

def mov(where, value):
    global variables
    if isRegister(value):
        variables[where] = variables[value]
    else:
        variables[where] = int(value)

def cmp(where, value):
    global variables
    if isRegister(value):
        comparison = (variables[where] == variables[value])
    else:
        comparison = (variables[where] == int(value))
    return comparison

def push(where, value):
    if isRegister(value):
        stack[where] = variables[value]
    else:
        stack[where] = int(value)

def pull(where):
    return stack[where]

def operator(instruction, where, value):
    if isRegister(value):
        temporal = variables[value]
    else:
        temporal = int(value)
    if instruction == "ADD":
        variables[where] += temporal
    elif instruction == "SUB":
        variables[where] -= temporal
    elif instruction == "MUL":
        variables[where] *= temporal
    elif instruction == "DIV":
        variables[where] //= temporal
    elif instruction == "INC":
        variables[where] += 1
    elif instruction == "DEC":
        variables[where] -= 1

def fin():
    exit()

file = read()

for i in range(len(file)):
    print(file[i])


variables["CX"] = 2
mov("AX", "CX")
mov("BX", "2")

