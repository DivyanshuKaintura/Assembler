.start
LD R1, 65
LD R2, 0xFA00
.loop
STL R1, R2
CMP R1, 122
ADD R1, 1
ADD R2, 1
BLT loop
LD R1, 32
LD R2, 0xFA00
.loop2
STL R1, R2
CMP R2, 0xFA3A
ADD R2, 1
BLT loop2
UCB start