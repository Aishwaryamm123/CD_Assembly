import re
import sys


value = {}
avail = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
regocc=[]

op1 = {'+': 'ADD', '*': 'MUL', '-': 'SUB', '/': 'DIV','==':'BNE', '!=': 'BE',
                          '<': 'BGE', '>': 'BLE', '<=': 'BGT', '>=': 'BLT'}

def regc(operand):
    for key in value.keys():
        if(operand == value[key]):
            r = key
            regocc.remove(r)
            regocc.append(r)
            return r
    r = get()
    if(operand.isnumeric()):
        print("\tMOV"+" "+r+" "+"#"+operand)
    else:
        print("\tLDR"+" "+r+" "+operand)
    value[r] = operand
    return r


def operation1(line, operation):
    r1 = regc(line[2])
    if(line[4].isnumeric()):
        r2 = "#"+str(line[4])
    else:
        r2 = regc(line[4])
    r3 = get()
    print("\t"+operation+" "+r3+" "+r1+" "+r2)
    regex_match = re.findall("^t[0-9]*$", line[0])
    if(len(regex_match)):
        pass
    else:

        print("\tSTR "+r3+" "+line[0])

    if(line[0] == line[2]):
        regocc.remove(r1)
        avail.append(r1)
        value.pop(r1)

    elif(line[0] == line[4] and not line[4].isnumeric()):
        regocc.remove(r2)
        avail.append(r2)
        value.pop(r2)

    else:
        r2 = regc(line[4])
    print("\tCMP "+r1+" "+r2)

    value[r3] = line[0]
condition = " "



def get():
    if(len(avail) != 0):
        r = avail.pop(0)
        regocc.append(r)
    else:
        r = regocc.pop(0)
        mem = value.pop(r)
        regocc.append(r)

    return r


def valuate(line):

    global condition
    for operator in op1:
        if operator in line and len(line) == 5:
            operation1(line, op1[operator])
            return

    for operator in op1:
        if operator in line and len(line) == 5:
            condition = op1[operator]
            operation1(line)
            return
    if(len(line) == 1):
        regex_match = re.findall("^[A-Za-z0-9]*:$", line[0])
        if(len(regex_match)):
            print(line[0])
            return

    if 'iffalse' in line and len(line) == 4:
        print("\t"+condition+" "+line[3])
        return

    if 'goto' in line and len(line) == 2:
        print("\tB "+line[1])
        return
    if 'true' in line and len(line) == 4:
        print("\tB "+line[3])
        return

    if '=' in line and len(line) == 3:
        r1 = regc(line[2])
        print("\tSTR "+r1+" "+line[0])
        regex_match = re.findall("^t[0-9]*$", line[2])
        if(line[2].isnumeric() or len(regex_match)):
            pass
        else:
            r2 = get()

        for r in value.keys():
            if(value[r] == line[0]):
                value.pop(r)
                regocc.remove(r)
                avail.append(r)
                break

        if(not line[2].isnumeric() and not len(regex_match)):
            value[r2] = line[0]

        if(value[r1].isnumeric() or len(regex_match)):
            regocc.remove(r1)
            regocc.append(r1)
            value[r1] = line[0]
        return


if __name__ == "__main__":
    if len(sys.argv) == 2:
        fp = str(sys.argv[1])

    c = open(fp, "r")
    line = c.readlines()

    for i in range(len(line)):
        line[i] = line[i].replace('\n', '')
        line[i] = line[i].split()

    for i in range(len(line)):
        valuate(line[i])
