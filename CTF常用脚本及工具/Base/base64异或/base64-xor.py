import base64
import string

flag = ''
a = base64.b64decode('AAoHAR1TIiIkUFUjUFQgVyInVSVQJVFRUSNRX1YgXiJSVyJQVRs=')

for i in string.printable:
    for j in a:
        flag += chr( ord(i) ^ j)
    print(flag + '\n')
