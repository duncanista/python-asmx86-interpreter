#encoding: utf-8
import sys

stack = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
variables = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
instructions = ["MOV", "CMP", "PUSH", "DIV", "MUL", "SUB", "ADD", "INC", "DEC"]
jumps = ["JNE", "JE", "JMP"]
end = ["INT", "21h", "RET"]
ignore = ["org", "100h"]
functions = {}


def read():
    global instructions, jumps
    it = iter(sys.stdin.read().splitlines())
    file = []
    next(it)
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

    file = [item for line in file for item in line]

    return file

def precompile(file):
    items = file
    i = 0
    f = ""
    functionActive = False
    while (i < len(items)):
        element = items[i]
        if (element in instructions):
            register = items[i+1]
            if (not functionActive):
                nextElement = items[i + 2]
                #i += executeInstruction(element, register, nextElement)
                print("INSTR  ['{}']".format(element))
                print("INSTR >['{}']".format(register))
            else:

                print("INSTR  ['{}']".format(element))
                print("INSTR >['{}']".format(register))
                functions[f].append(element)
                functions[f].append(register)
                nextElement = items[i + 2]
                if (nextElement in instructions):
                    i += 1
                else:
                    variable = nextElement
                    print("INSTR <['{}']".format(variable))
                    functions[f].append(variable)
                    i += 2

        elif (element in jumps):
            jumpTo = items[i+1]
            if (not functionActive):
                print("")
                print("JUMP  ['{}']".format(element))
                print("JUMP >['{}']".format(jumpTo))
            else:
                if (not isFunction(f)):
                    functions[f] = []
                print("JUMP  ['{}']".format(element))
                print("JUMP >['{}']".format(jumpTo))
                functions[f].append(element)
                functions[f].append(jumpTo)

            i += 1
        elif (':' in element):
            print("FUNCT  ['{}']".format(element))
            print("---- FUNCTION")
            functions[element] = []
            f = element
            functionActive = True
        else:
            if (not functionActive):
                print("!!!!   ['{}']".format(element))
            else:
                functions[f].append(items[i])
                print("!!!!  ['{}']".format(element))
        i += 1

    return 0

def isRegister(value):
    return bool(variables.get(value))

def isFunction(value):
    return bool(functions.get(value))

def getPreviousVariable(toFind):
    temporal = [key for key in variables]
    temporal.sort()
    index = temporal.index(toFind)
    return temporal[index-1]

def executeInstruction(instruction, register, nextElement):
    global instructions
    index = 1
    if(instruction == "MOV"):
        mov(register, nextElement)
        index = 2
    elif(instruction == "CMP"):
        cmp(register, nextElement)
        index = 2
    elif(instruction == "PUSH"):
        push(register, nextElement)
    else:
        pass



    if(nextElement in instructions):
        index += 1
    else:
        variable = nextElement
        print("INSTR <['{}']".format(variable))
        index += 2
    return 0

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

def operator(instruction, where, value):
    if isRegister(value):
        temporal = variables[value]
    else:
        if(value not in instructions):
            temporal = int(value)
        else:
            pass
    if instruction == "ADD":
        variables[where] += temporal
    elif instruction == "SUB":
        variables[where] -= temporal
    elif instruction == "MUL":
        variables[where] *= temporal
    elif instruction == "DIV":
        if(value not in instructions):
            if(isRegister(value)):
                variables[where] //= variables[value]
            else:
                variables[where] //= temporal
        else:
            previousVariable = getPreviousVariable(where)
            variables[where] //= variables[previousVariable]
    elif instruction == "INC":
        variables[where] += 1
    elif instruction == "DEC":
        variables[where] -= 1

def fin():
    exit()

file = read()
#file = precompile(file)


for index in functions:
    print("{} \t".format(index))
    s = ""
    list = functions[index]
    for i in range(len(list)):
        s += "\t" +list[i] + " "
        if(i+1 < len(list)):
            if(functions[index][i+1] in instructions or functions[index][i+1] in jumps):
                s += "\n"
    print(s)

variables["CX"] = 2
mov("AX", "CX")
mov("BX", "8")
print(variables)
operator("DIV", "BX", "CX")
print(variables)
print(getPreviousVariable("BX"))

