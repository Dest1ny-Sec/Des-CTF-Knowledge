cipher='Ygvdmq[lYate[elghqvakl}'

flag = ''

for i in range(len(cipher)):
    flag = ord(cipher[i]) ^ 0x7
    flag += 3
    print ( chr(flag),end='' )