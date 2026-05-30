def conv(s):
    return hex(int(s, 2))[2:]

def IEEE802(bs):
    pass
    dict = {
        "0101": "11",
        "1001": "01",
        "0110": "10",
        "1010": "00"
    }
    bs=str(bs)
    # print(bs)
    r = ""
    for j in range(0, len(bs), 4):
        i=bs[j:j+4]
        if i in dict.keys():
            r += dict[i]
    return r

n = 0x5555555595555A65556AA696AA6666666955 # 密文
flag = ''
bs = '0' + bin(n)[2:]
r = ''
# print(bs)
r = IEEE802(bs)
print(r)
#
for i in range(0, len(r), 8): # 每8位反转
    tmp = r[i:i + 8][::-1]
    flag += conv(tmp[:4])
    flag += conv(tmp[4:])
print(flag.upper()) # 翻转