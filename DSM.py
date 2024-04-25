import sys

def hexstr(x):
    return "{:04x}".format(x)

def register(r):
    return " R" + str(r)

def disassemble(opcode, data):
    disCode = ""
    op = opcode >> 8 
    mode = opcode & 0xFF

    # MOV R1, R2
    if op == 0x00:
        if mode >= 0 and mode <= 7:
            R2 = data & 0xFF
            if R2 >= 0 and R2 <= R2:
                disCode = "MOV" + register(mode) + "," + register(data & 0xFF)
            else:
                print("Invalid Register: " + R2)
                sys.exit()
        else:
            print("Invalid Register: " + mode)
            sys.exit()

    # LD R, M
    elif op == 0x10:
        disCode = "LD" + register(mode) + ", $" + hexstr(data)

    # LD R, 16-bit value
    elif op == 0x11:
        if (mode >= 0 and mode <= 7):
            disCode = "LD" + register(mode) + ", 0x" + hexstr(data)
        else:
            print("Invalid Register: " + register(mode))
            sys.exit()

    # STL R1, R2
    elif op == 0x20:
        disCode = "STL" + register(mode) + "," + register(data & 0xFF)

    # STL R, M
    elif op == 0x21:
        disCode = "STL" + register(mode) + ", $" + hexstr(data)

    # ADD R1, R2
    elif op == 0x30:
        disCode = "ADD" + register(mode) + "," + register(data & 0xFF)

    # ADD R1, 16-bit value
    elif op == 0x31:
        disCode = "ADD" + register(mode) + ", " + hexstr(data)

    # SUB R1, R2
    elif op == 0x32:
        disCode = "SUB" + register(mode) + "," + register(data & 0xFF)

    # SUB R1, 16-bit value
    elif op == 0x33:
        disCode = "SUB" + register(mode) + ", " + hexstr(data)

    # CMP R, M
    elif op == 0x40:
        disCode = "CMP" + register(mode) + ", $" + hexstr(data)

    # CMP R, 16-bit value
    elif op == 0x41:
        disCode = "CMP" + register(mode) + ", 0x" + hexstr(data)
    
    # BLT label
    elif op == 0x50:
        disCode = "BLT" + " $" + hexstr(data)

    # BGT label
    elif op == 0x51:
        disCode = "BGT" + " $" + hexstr(data)    

    # BEQ label
    elif op == 0x52:
        disCode = "BEQ" + " $" + hexstr(data)

    # UCB label
    elif op == 0x53:
        disCode = "UCB" + " $" + hexstr(data)

    else:
        print("Invalid instruction: 0x" + op)

    return disCode
