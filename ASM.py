import sys
import re

labelList = {}

def createFile(fn):
    with open("code.bin", "wb") as byte_code_file:
        byte_code_file.close()

def writeFile(fn, b):
    with open("code.bin", "ab") as byte_code_file:
        byte_code_file.write(bytearray(b))

# initialize the labels dictionary
def createLabels(fn):
    line_number = 0
    with open(sys.argv[1]) as code:
        for line in code:
            line = line.replace('\n', '').replace('\r', '')

            #ignore comments
            if line[0] == '#':
                 continue
            
            if line[0] == '.':
                label = line[1:]
                labelList[label] = line_number * 4
                print("Label: " + label + " $ " + format(line_number * 4, '#04x'))

            else:
                line_number = line_number + 1
# labelList now consist of every label mapped to their corresponding address

# main

# if no .asm file is passed as command line argument 
if len(sys.argv) != 2:
    print ("Please pass an .asm file")
    sys.exit()

# create file for the binary code 
createFile("code.bin")

# parsing through the entire code to search for labels
createLabels(sys.argv[1])

with open(sys.argv[1]) as code:
    for instruction in code:

        # ignore labels
        if instruction[0] == '.':
            continue

        #ignore comments
        if instruction[0] == '#':
            continue

        instruction = instruction.replace('\n', '').replace('\r', '')
        
        # get every token from the instruction
        tok = re.split(r'[, ]', instruction)

        # remove black spaces if they exist
        if '' in tok:
            tok.remove('')

        print(str(tok))

        if tok[0].upper() == "MOV":
            register = int(tok[1].upper()[1]) # Register 1
            if register >= 1 and register <= 7:
                operand = tok[2] # Reegister 2
                if operand[0] == 'R':
                    r2 = int(operand[1:], 0) # extracting the no. of register
                    b = [0x00, register, 0, r2]
                    writeFile("code.bin", b)

                else:
                    print("Invalid Register: " + tok[2])
                    sys.exit()
                    
            else:
                print("Invalid Register: " + tok[2])
                sys.exit()
                

        elif tok[0].upper() == "LD":
            register = int(tok[1].upper()[1])
            if register >= 1 and register <= 7:
                operand = tok[2]
                if operand[0] == '$':
                    # Address
                    address = int(operand[1:], 16)
                    b = [0x10, register, address >> 8, address & 0xFF] # b = [0x10, register, 0, address >> 8, address & 0xFF]
                    writeFile("code.bin", b)

                else:
                    # Value
                    value = int(operand, 0)
                    b = [0x11, register, value >> 8, value & 0xFF]
                    writeFile("code.bin", b)
                
            else:
                print("Invalid Register: " + tok[1])
                sys.exit()


        elif tok[0].upper() == "STL":
            register = int(tok[1].upper()[1])
            if register >= 1 and register <= 7:
                operand = tok[2]

                if operand[0] == 'R':
                    # Register
                    r2 = int(tok[2].upper()[1])
                    if r2 >= 1 and r2 <= 7:
                        b = [0x20, register, 0, r2]
                        writeFile("code.bin", b)

                    else:
                        print("Invalid Register: " + tok[2])
                        sys.exit()

                else:
                    # Memory Address
                    address = int(operand[1:], 16)
                    b = [0x21, register, address >> 8, address & 0xFF] # b = [0x21, register, 0, address >> 8, address & 0xFF]
                    writeFile("code.bin", b)

            else:
                print("Invalid Register: " + tok[1])
                sys.exit()


        elif tok[0].upper() == "ADD":
            register = int(tok[1].upper()[1])
            if (register >= 1 and register <= 7):
                operand = tok[2]
                if (operand[0] == 'R'):
                    # Register
                    r2 = int(operand[1])
                    b = [0x30, register, 0, r2]
                    writeFile("code.bin", b)

                else:
                    # Value
                    value = int(operand, 0)
                    b = [0x31, register, value >> 8, value & 0xFF]
                    writeFile("code.bin", b)


            else:
                print("Invalid Register: " + tok[1])
                sys.exit()


        elif tok[0].upper() == "SUB":
            register = int(tok[1].upper()[1])
            if register >= 0 and register <= 7:
                operand = tok[2]
                if operand[0] == 'R':
                    # Register
                    r2 = int(operand[1])
                    b = [0x32, register, 0, r2]
                    writeFile("code.bin", b)
                
                else:
                    # value
                    value = int(operand, 0)
                    b = [0x33, register, value >> 8, value & 0xFF]
                    writeFile("code.bin", b)
                    

            else:
                print("Invalid Register: " + tok[1])
                sys.exit()

        elif tok[0].upper() == "CMP":
            register = int(tok[1].upper()[1])
            if register >= 0 and register <= 7:
                operand = tok[2]
                if operand[0] == 'R':
                    # Register
                    r2 = int(operand[1])
                    b = [0x40, register, 0, r2]
                    writeFile("code.bin", b)

                else:
                    # Value
                    value = int(operand, 0)
                    b = [0x41, register, value >> 8, value & 0xFF]
                    writeFile("code.bin", b)
                

            else:
                print("Invalid Register: " + tok[1])
                sys.exit()

            
        elif tok[0].upper() == "BLT":
            if tok[1] in labelList:
                address = labelList[tok[1]]
                b = [0x50, 0, address >> 8, address & 0xFF]
                writeFile("code.bin", b)
            
            else:
                print("Unknown Label: " + tok[1])
                sys.exit()

        elif tok[0].upper() == "BGT":
            if tok[1] in labelList:
                address = labelList[tok[1]]
                b = [0x51, 0, address >> 8, address & 0xFF]
                writeFile("code.bin", b)

            else:
                print("Unknown Label: " + tok[1])
                sys.exit()   

        elif tok[0].upper() == "BEQ":
            if tok[1] in labelList:
                address = labelList[tok[1]]
                b = [0x52, 0, address >> 8, address & 0xFF]
                writeFile("code.bin", b)

            else:
                print("Unknown Label: " + tok[1])
                sys.exit() 

        elif tok[0].upper() == "UCB":
            if tok[1] in labelList:
                address = labelList[tok[1]]
                b = [0x53, 0, address >> 8, address & 0xFF]
                writeFile("code.bin", b)

            else:
                print("Unknown Label: " + tok[1])
                sys.exit() 

        else:
            print("Unknown Instruction: " + tok[0])
            sys.exit()
