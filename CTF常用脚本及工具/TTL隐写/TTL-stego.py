import binascii

f = open('attachment.txt','r')
s = ''
a = ''
data = ''
# print(f.readlines())
for i in f.readlines():
    if i == "63\n":
        a='00'
    if i == "127\n":
        a='01'
    if i == "191\n":
        a='10'
    if i == "255\n":
        a='11'
    s += a
# print(s)

for i in range(0,len(s),8): # 每8位一组
    data += chr(int(s[i:i+8],2)) # 转为二进制再转为ASCII字符
data = binascii.unhexlify(data)
print(data)

with open('flag.zip','wb') as f:
    f.write(data)