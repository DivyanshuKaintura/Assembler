.start
LD R1, 65
LD R2, 0xFBFF
.loop
STL R1, R2
CMP R1, 112
ADD R1, R2
ADD R2, 1
BLT loop
LD R1, 32
LD R2, 0xFBFF
.loop2
STL R1, R2
CMP R2, 0xFC2E
ADD R2, 1
BLT loop2
UCB start