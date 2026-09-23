s = ['f',0xA,'k',0xC,'w','&','O','.','@',0x11,'x',0xD,'Z',';','U',0x11,'p',0x19,'F',0x1F,'v','"','M','#','D',0xE,'g',6,'h',0xF,'G','2','O']

flag = 'f'#第一个字符不用进行异或运算
for i in range(1,len(s)):
    if(isinstance(s[i],int)):#将数字转化为字符
        s[i] = chr(s[i])
for i in range(1,len(s)):
    flag += chr(ord(s[i]) ^ ord(s[i-1]))#a^b=c 等于 a^c=b

print(flag)

