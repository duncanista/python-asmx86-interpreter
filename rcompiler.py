#encoding: utf-8
import sys

stack = {"AX": 0, "BX": 0, "CX": 0, "DX": 0, "CMP": None}
variables = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
instructions = ["MOV", "CMP", "PUSH", "DIV", "MUL", "SUB", "ADD", "INC", "DEC"]
jumps = ["JNE", "JE", "JMP"]
end = ["INT", "21h", "RET"]
ignore = ["org", "100h"]
movcount = 0
functions = {}

def read():
    global instructions, jumps
    it = iter(sys.stdin.read().splitlines())
    file = []
    next(it)
    while True:
        try:
            line = next(it).split()
            if line:
                line = " ".join(line).replace(',', ' ')
                line = line.split()
                if ";" in line:
                    index = line.index(";")
                    line = line[:index]
                    if line:
                        file.append(line)
                else:
                    line =  " ".join(line)
                    if ";" in line:
                        line.split()
                        index = 0
                        for i in range(len(line)):
                            if ";" in line[i]:
                                index = i
                        line = line[:index]
                        if line:
                            file.append(line)
                    else:
                        file.append(line.split())
        except:
            break
    file = [item for line in file for item in line]

    return file

def precompile(file):
    global functions, instructions, jumps, end, ignore
    items = file
    new_items = []
    i = 0
    functionKey = ""
    compilingFunction = False

    while (i < len(items)):
        element = items[i]

        if element in instructions:
            register = items[i+1]
            nextElement = items[i+2]

            if "h" in nextElement:
                nextElement = nextElement.replace('h','')

            if not compilingFunction:

                # i += executeInstruction(element, register, nextElement)
                #print("INSTR  ['{}']".format(element))
                #print("INSTR >['{}']".format(register))

                new_items.append(element)
                new_items.append(register)
                i += 1
                if nextElement not in instructions:
                    variable = nextElement
                    new_items.append(variable)
                    #print("INSTR <['{}']".format(variable))
                    i += 1

            else:
                #print("INSTR  ['{}']".format(element))
                #print("INSTR >['{}']".format(register))
                functions[functionKey].append(element)
                functions[functionKey].append(register)
                i += 1
                if nextElement not in instructions:
                    variable = nextElement
                    functions[functionKey].append(variable)
                    # print("INSTR <['{}']".format(variable))
                    i += 1

        elif element in jumps:
            jumpTo = items[i+1]
            if not compilingFunction:
                #print("")
                #print("JUMP  ['{}']".format(element))
                #print("JUMP >['{}']".format(jumpTo))
                new_items.append(element)
                new_items.append(jumpTo)
            else:
                #print("JUMP  ['{}']".format(element))
                #print("JUMP >['{}']".format(jumpTo))
                functions[functionKey].append(element)
                functions[functionKey].append(jumpTo)
            i += 1
        elif ':' in element:
            #print("FUNCT  ['{}']".format(element))
            #print("---- FUNCTION")
            new_items.append(element)
            functions[element] = []
            functionKey = element
            compilingFunction = True
        elif element in end:
            if not compilingFunction:
                new_items.append(element)
            else:
                functions[functionKey].append(element)
        else:
            if element in ignore:
                pass
            else:
                if not compilingFunction:
                    print("No sé que es esto  ['{}']".format(element))
                else:
                    functions[functionKey].append(element)
                    print("No sé que es esto ['{}']".format(element))
        i += 1

    return new_items

def compile(file):
    items = file
    i = 0
    while i < len(items):
        element = items[i]
        register = ""
        nextElement = ""
        if i + 1 < len(items):
            register = items[i + 1]
        if i + 2 < len(items):
            nextElement = items[i+2]
        index, activeFunction = executeInstruction(element, register, nextElement)

        if activeFunction and activeFunction in items:
            i = items.index(activeFunction)
        else:
            i += index

        i += 1

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
    activeFunction = None
    if instruction == "MOV":
        mov(register, nextElement)
        index += 1
    elif instruction == "CMP":
        cmp(register, nextElement)
        index += 1
    elif instruction == "PUSH":
        push(register)

    elif instruction in ["INC", "DEC", "ADD", "SUB", "MUL", "DIV"]:
        index = operator(instruction, register, nextElement)
    elif instruction in jumps:
        activeFunction = jump(instruction, register)
    else:
        activeFunction = instruction
        index -= 1
    if instruction in end:
        fin()
    if activeFunction:
        if ":" not in activeFunction:
            activeFunction += ":"
        compile(functions[activeFunction])


    return index, activeFunction

def jump(instruction, where):
    global stack
    comparison = stack["CMP"]
    activateFunction = None

    if(instruction in jumps[:2]):
        if(instruction == "JE"):
            if comparison:
                activateFunction = where
        elif(instruction == "JNE"):
            if not comparison:
                activateFunction = where
    else:
        activateFunction = where
    return activateFunction

def mov(where, value):
    global variables, movcount
    if isRegister(value):
        variables[where] = variables[value]
    else:
        variables[where] = int(value)
    movcount+=1

def cmp(where, value):
    global variables
    if isRegister(value):
        comparison = (variables[where] == variables[value])
    else:
        comparison = (variables[where] == int(value))

    stack["CMP"] = comparison

def push(where):
    global stack
    print("{} : {}".format(where, variables[where]))
    stack[where] = variables[where]

def operator(instruction, where, value):
    global variables
    index = 1
    if instruction in ["ADD", "SUB", "MUL", "DIV"]:
        index = operatorAux(instruction, where, value)
    elif instruction == "INC":
        variables[where] += 1

    elif instruction == "DEC":
        variables[where] -= 1
    else:
        pass
    return index

def operatorAux(instruction, where, value):
    global variables, instructions
    index = 1
    add = sub = mul = div = False
    if instruction == "ADD":
        add = True
    elif instruction == "SUB":
        sub = True
    elif instruction == "MUL":
        mul = True
    elif instruction == "DIV":
        div = True
    if value not in instructions:
        if isRegister(value):
            if add:
                variables[where] += variables[value]
            elif sub:
                variables[where] -= variables[value]
            elif mul:
                variables[where] *= variables[value]
            elif div:
                variables["DX"] = variables[where] % variables[value]
        else:
            temporal = int(value)
            if add:
                variables[where] += temporal
            elif sub:
                variables[where] -= temporal
            elif mul:
                variables[where] *= temporal
            elif div:
                variables["DX"] = variables[where] % variables[value]
        index = 2
    else:
        previousVariable = getPreviousVariable(where)
        if add:
            variables[where] += variables[previousVariable]
        elif sub:
            variables[where] -= variables[previousVariable]
        elif mul:
            variables[where] *= variables[previousVariable]
        elif div:
            variables["DX"] = variables[where] % variables[previousVariable]
    return index

def fin():
    print("Finalizando programa...")
    print("movcount: {}".format(movcount))
    print("Stack: {}".format(stack))
    print("Variables: {}".format(variables))
    exit()

def main():
    file = read()
    file = precompile(file)
    compile(file)

main()