import binascii

# 读取文件内容
f = open('3.txt','r')
content = f.read()
# print(content)

content1 = ''
content2 = ''
content3 = ''
for i in range(0,len(content)):
    content1 = content[i:i+2] + '111111'
    content2 = hex(int(content1,2))
    content3 += str(int(content2,16))+ '\n'

with open('5.txt','a+') as f:
    f.write(content3)