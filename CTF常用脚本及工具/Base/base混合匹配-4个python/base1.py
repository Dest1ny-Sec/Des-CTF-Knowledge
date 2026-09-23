import re
import base64
with open('base_python.txt','r') as f:
    decode = f.read()
    try:
        for i in range(30):
         s = re.compile(r'[a-z]|[=]').findall(decode)
         s1 = re.compile(r'[0189]').findall(decode)
         s2 = re.compile(r'[,%;>|){:”’*?@<.(]').findall(decode)
         if 'flag' in decode:
             print(decode)
             print(i)
             break
         elif (bool(s1) == False) and  (bool(s2) ==False) :
             decode = base64.b32decode(decode)
         elif bool(s) == True and bool(s2) == False :
             decode = base64.b64decode(decode)
         elif bool(s2) == True:
             decode = base64.b85decode(decode)
         else :
             decode = base64.b16decode(decode)
         decode = str(decode, encoding='utf-8')
    except:
        print(decode)
f.close()
print(decode)
