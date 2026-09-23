import zlib
import struct
file = '1.png'
fr = open(file,'rb').read()
data = bytearray(fr[12:29])
#crc32key = eval(str(fr[29:33]).replace('\\x','').replace("b'",'0x').replace("'",'')) 
crc32key = 0xC4ED3 
#data = bytearray(b'\x49\x48\x44\x52\x00\x00\x01\xF4\x00\x00\x01\xF1\x08\x06\x00\x00\x00') 
n = 4095 
for w in range(n): 
    width = bytearray(struct.pack('>i', w))
    for h in range(n): 
        height = bytearray(struct.pack('>i', h)) 
        for x in range(4): 
            data[x+4] = width[x] 
            data[x+8] = height[x] 
            #print(data) 
        crc32result = zlib.crc32(data) 
        if crc32result == crc32key: 
            print(width,height) 
            print(data) 
            newpic = bytearray(fr) 
            for x in range(4): 
                newpic[x+16] = width[x]
                newpic[x+20] = height[x] 
            fw = open(file+'.png','wb') 
            fw.write(newpic)
            fw.close