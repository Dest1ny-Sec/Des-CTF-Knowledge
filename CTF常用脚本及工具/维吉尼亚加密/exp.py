c='SRLU{LZPL_S_UASHKXUPD_NXYTFTJT}'
m='ACTF{'
a=[]
for i in range(4):
    a.append(str(ord(c[i])-ord(m[i])))
print(m,end='')
for i in range(5,len(c)):
    if 'A'<= c[i]<= 'Z':
        print(chr((ord(c[i])-int(a[i%4])-ord('A'))%26+ord('A')),end='')
    else:
        print(c[i],end='')