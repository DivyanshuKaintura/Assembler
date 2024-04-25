.start
LD R1, 65
LD R2, 0xfa00
.loop
STL R1, R2
CMP R1, 70
ADD R1, 1
ADD R2, 1
BLT loop