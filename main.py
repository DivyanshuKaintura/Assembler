import time
from DSM import disassemble
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

dumpDisplay = True
debug = False
interactive = False

# since we are working on 8 bit machine we can have 256 registers
registers = [0, 1, 2, 3, 4, 5, 6, 7]
program_counter = 0

# Total memory: 64K
# Programmable memory: 63K
# Storage memory: 1K from the end (from 0xFA00)
main_memory = bytearray(0x10000) 

# flags
zero_flag = 0
greater_flag = 0
less_flag = 0

# Display Starting Address
display_address = 0xFA00

def hexstr(x):
    return "{:04x}".format(x)

def debugRegisters(opcode, data):
    print("PC: " + str(program_counter - 4) + "\t OP: 0x" + hexstr(opcode) + "\t Data: 0x" + hexstr(data))
    print("Code: " + disassemble(opcode, data))
    print("R0:" + hexstr(registers[0]) + "   R1:" + hexstr(registers[1]) + "   R2:" + hexstr(registers[2]) + "   R3:" + hexstr(registers[3]) + "   R4:" + hexstr(registers[4]) + "   R5:" + hexstr(registers[5]) + "   R6:" + hexstr(registers[6]) +   "   R7:" + hexstr(registers[7]))
    print("Z: " + str(zero_flag) + "   GT: " + str(greater_flag) + "   LT: " + str(less_flag) + "\n")

# Pin 25 on Pico is the built-in LED
led = Pin(25, Pin.OUT)

# Init OLED display for PICO
# This demo uses a 128x32 OLED I2C display
# Driven by the SSD1306.
oled_width = 128 # Pixels
oled_height = 32 # Pixels
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# OLED DISPLAY STUFF ON PICO
# Text display. Three lines, 16 characters each.
# 48 Bytes in total.
# Lots of potential for bigger displays.
# Graphic modes and text modes possible, etc.
# This demo uses a 128x32 OLED I2C display
# Driven by the SSD1306.
def dumpdisplaytooled():
    oled.fill(0)
    x = 0
    y = 0
    i = display_address
    j = display_address + 48
    while i < j:
        line = ""
        while x < 16:
            c = main_memory[i] & 0xFF
            if c < 32: # non-printable characters
                line = line + " "
            else:
                line = line + str(chr(c))
            x = x + 1
            i = i + 1
        oled.text(line, 0, y)
        x = 0
        y = y + 12
    oled.show()

def display():
    count = 0
    i = display_address
    j = display_address + 58

    print("--------------------")
    while i < j:
        temp = ""
        while count < 58:
            x = main_memory[i] & 0xFF
            if x < 32:
                temp = temp + " "
            else:
                temp = temp + str(chr(x))
            i = i + 1
            count = count + 1
        print(temp)
        count = 0
    print("--------------------")
    time.sleep(0.01)


def decode(pc, opcode, data):
    global zero_flag, less_flag, greater_flag
    global main_memory
    global registers

    op = opcode >> 8
    mode = opcode &0xFF

    # Move: MOV R1, R2
    if op == 0x00:
        registers[mode] = registers[data & 0xFF]

    # Load: LD R, M
    elif op == 0x10: 
        registers[mode] = main_memory[data]

    # Load: LD R, 0xFFFF
    elif op == 0x11:
        registers[mode] = data

    # Store: STL R1, R2
    elif op == 0x20:
        main_memory[registers[data]] = registers[mode]

    # Store: STL R, M
    elif op == 0x21:
        main_memory[data] = registers[mode] >> 8

    # Add R1, R2
    elif op == 0x30:
        registers[mode] = (registers[mode] + registers[data & 0xFF]) & 0xFFFF

    # ADD R1, value
    elif op == 0x31:
        registers[mode] = (registers[mode] + data) & 0xFFFF

    # SUB R1, R2
    elif op == 0x32:
        registers[mode] = (registers[mode] - registers[data & 0xFF]) & 0xFFFF

    # SUB R1, value
    elif op == 0x33:
        registers[mode] = (registers[mode] - data) & 0xFFFF
    
    # Compare: CMP R, M
    elif op == 0x40:
        if registers[mode] == main_memory[data]:
            zero_flag = 1
            greater_flag = 0
            less_flag = 0

        elif registers[mode] < main_memory[data]:
            zero_flag = 0
            less_flag = 1
            greater_flag = 0

        else:
            zero_flag = 0
            greater_flag = 1
            less_flag = 0

    # CMP R, value
    elif op == 0x41:
        if registers[mode] == data:
            zero_flag = 1
            greater_flag = 0
            less_flag = 0

        elif registers[mode] < data:
            zero_flag = 0
            less_flag = 1
            greater_flag = 0

        else:
            zero_flag = 0
            greater_flag = 1
            less_flag = 0

    # Branch if less_than_flag = 1: BLT label
    elif op == 0x50:
        if less_flag == 1:
            pc = data

    # Branch if greater_than_flag = 1: BGT label
    elif op == 0x51:
        if greater_flag == 1:
            pc = data

    # Branch if zero_flag = 1: BEQ label
    elif op == 0x52:
        if zero_flag == 1:
            pc = data

    # Unconditional Branch: UCB label
    elif op == 0x53:
        pc = data

    else:
        print("Unknown instruction!")
        exit(0)      

    return pc

# Main 
        
with open("code.bin", mode = 'rb') as file:
    code = bytearray(file.read())

last_index = len(code)

# Copy code into main memory
i = 0
while i < last_index:
    main_memory[i] = code[i]
    i = i + 1

cmd = 's' # when in interactive mode
refreshdisplay=0

while program_counter < last_index:
    # read 4 bytes
    opcode = main_memory[program_counter] << 8 | main_memory[program_counter + 1]
    program_counter = program_counter + 2

    data = main_memory[program_counter] << 8 | main_memory[program_counter + 1]
    program_counter = program_counter + 2

    program_counter = decode(program_counter, opcode, data)

    if debug == True:
        debugRegisters(opcode, data)

    if dumpDisplay == True:
        display()

    # Update OLED display, regardless of DEBUG etc flags
    # But not every cycle, otherwise too much time is taken
    # just to update the display
    refreshdisplay = (refreshdisplay + 1) % 3
    if refreshdisplay == 0:
        led.toggle()
        dumpdisplaytooled()

    # If in interactive mode then allow for single stepping etc
    # More interactive commands could be added here
    if interactive == True:
        if cmd == 's':
            cmd = input("[S]tep")
            if cmd == '':
                cmd = 's'

display()