# -*-coding: utf-8 -*-
from PIL import Image

binstr = ""
flag = ""

def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

for i in range(1168):
    image=Image.open(r'./202011/'+str(i)+'.png')
    # print (image.getpixel((115,55)))#输出颜色值
    # print (image.getpixel((115,145)))
    tmp1 = image.getpixel((115,55))
    tmp2 = image.getpixel((115,150))
    # print (type(tmp1))
    if(tmp1[0] > 250):
        binstr += '1'
    elif(tmp2[1] > 250):
        binstr += '0'
    else:
        binstr += ''
print (binstr)

for i in range(len(binstr)):
    if i%8==0:
        flag +=decode(binstr[i:i+8])
print(flag)
