import re
import sys

aval_reg=('r0','r1','r2','r3','r4','r5','r6','r7')	#list of registers
value={}
regocc=()
available=aval_reg


operations={'+': 'ADD', '*': 'MUL', '-': 'SUB', '/': 'DIV','==': 'BNE', '!=': 'BE','<': 'BGE', '>': 'BLE', '<=': 'BGT', '>=': 'BLT'}

def operation(line,operations):
    r1 = register(line[2])
    if(line[4].isnumeric()):
        r2 = "#"+str(line[4])
    else:
        r2 = register(line[4])
    r3 = get()
    print("\t"+operations+" "+r3+" "+r1+" "+r2)
    regex_match = re.findall("^t[0-9]*$", line[0])
    if(len(regex_match)):
        pass
    else:

        print("\tSTR "+r3+" "+line[0])

    if(line[0] == line[2]):
        regocc.remove(r1)
        available.append(r1)
        values.pop(r1)

    elif(line[0] == line[4] and not line[4].isnumeric()):
        regocc.remove(r2)
        available.append(r2)
        values.pop(r2)
    values[r3] = line[0]


def evaluate(line):

    global condition_used
    for operator in operations:
        if operator in line and len(line) == 5:
            operations(line, operations[operator])
            return

    if(len(line) == 1):
        regex_match = re.findall("^[A-Za-z0-9]*:$", line[0])
        if(len(regex_match)):
            print(line[0])
            return
    
    if 'if' in line and len(line) == 11:
        print("\t"+condition_used+" "+line[10])
        return

    if 'goto' in line and len(line) == 2:
        print("\tB "+line[1])
        return

    if 'true' in line and len(line) == 4:
        print("\tB "+line[3])
        return

    if '=' in line and len(line) == 3:
        r1 = register(line[2])
        print("\tSTR "+r1+" "+line[0])
        regex_match = re.findall("^t[0-9]*$", line[2])
        if(line[2].isnumeric() or len(regex_match)):
            pass
        else:
            r2 = get()

        for register in value.keys():
            if(value[register] == line[0]):
                value.pop(register)
                regocc.remove(register)
                available.append(register)
                break

        if(not line[2].isnumeric() and not len(regex_match)):
            value[r2] = line[0]

        if(value[r1].isnumeric() or len(regex_match)):
            regocc.remove(r1)
            regocc.append(r1)
            value[r1] = line[0]
        return
    



#checking registers
def register(x):
    for i in val.keys(): #taking values of register
        if (x==val[i]):
            r=i
            regocc.remove(r)
            regocc.append(r)
        return r
    #need to get the register
    r=get() #calling get fun
    if x.isnumeric():
        print("mov"+" "+register+" "+"#"+operand)
    else:
        print("ldr"+" "+register+" "+operand)
    value[r]=x
    return r




def get():
    if(available !=0 ):
        r = available.pop(0)
        regocc.append(r)
       # print(regocc)

    else:
        r=regocc.pop(0)
        free=val.pop(r)
        regocc.append(r)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        fp = str(sys.argv[1])

    code = open(fp, "r")
    lines = code.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
        lines[i] = lines[i].split()

    for i in range(len(lines)):
        evaluate(lines[i])


    
	

