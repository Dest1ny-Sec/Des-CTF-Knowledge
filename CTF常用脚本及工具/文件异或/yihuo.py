original = open("亦真亦假",'r').read()
flag = open("flag",'w')
for i in original:
    tmp = int(i,16)^5
    flag.write(hex(tmp)[2:])

