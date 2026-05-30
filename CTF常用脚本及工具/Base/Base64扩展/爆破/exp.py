str="JASGBWcQPRXEFLbCDIlmnHUVKTYZdMovwipatNOefghq56rs****kxyz012789+/"
ciper="MyLkTaP3FaA7KOWjTmKkVjWjVzKjdeNvTnAjoH9iZOIvTeHbVD"#(==没有用)
import string
import binascii
# for i in string.ascii_letters+string.digits:
#     if i not in str:
#         print(i)
import itertools
s=['j','u','3','4']
for i in itertools.permutations(s,4):
    ss="JASGBWcQPRXEFLbCDIlmnHUVKTYZdMovwipatNOefghq56rs"+"".join(i)+"kxyz012789+/"
    bins = ""
    for j in ciper:
        bins+=bin(ss.index(j))[2:].zfill(6)
    # print(hex(eval("0b"+bins))[2:-1])
    print(binascii.unhexlify(hex(eval("0b"+bins))[2:-1]))