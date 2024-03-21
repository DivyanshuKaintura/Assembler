with open("code.bin", 'rb') as in_file:
        hexFile = open("ByteCode.txt", "w")
        k = 0
        while True:
            hexdata = in_file.read(1).hex()
            if len(hexdata) == 0:
                hexFile.close()                
                break
   
            if k == 4:
                k = 0
                hexFile.write("\n")

            k = k + 1
            hexFile.write(hexdata + " ")  
