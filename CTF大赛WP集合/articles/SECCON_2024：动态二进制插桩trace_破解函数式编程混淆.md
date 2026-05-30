# SECCON 2024：动态二进制插桩trace 破解函数式编程混淆

> 原文: https://www.ctfiot.com/220833.html
> ID: 220833

/f
FLAG: SECCON{fUnCt10n4l_pRoGr4mM1n6_1s_pR4c7iC4lLy_a_pUr3_0bfu5c4T1oN}
"Correct"

一

ida 逆向初探

v84 = 0;
 std::
variant>::
variant(
 (__int64)v106,
 (__int64)&v84);
 v83 = 0xB7E9A2A4;
 std::
variant>::
variant(
 (__int64)v105,
 (__int64)&v83);
 main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 (__int64)v107,
 (__int64)&v78,
 (__int64)v105,
 (__int64)v106,
 v3,
 v4);

std::
make_shared<Cons,std::
variant> &,std::
variant> &>(
 (__int64)v7,
 a3,
 a4);
 std::
variant>::
variant<std::
shared_ptr<Cons>,void,void,std::
shared_ptr<Cons>,void>(
 a1,
 (__int64)v7);
 std::
shared_ptr<Cons>::~shared_ptr(v7);

v5 = operator new(0x50uLL, a1);
 v6 = std::
forward<std::
variant> &>(a3);
 std::
variant>::
variant((__int64)v11, v6);
 v7 = std::
forward<std::
variant> &>(a2);
 std::
variant>::
variant((__int64)v10, v7);
 Cons::
Cons(v5, (__int64)v10, (__int64)v11);
 std::
variant>::~variant((__int64)v10);
 std::
variant>::~variant((__int64)v11);

std::
function<std::
variant> ()(void)>::
function<main::{lambda(void)#1},void>(
 (std::
_Function_base *)v127,
 (__int64)v95);

// level 1
*((_QWORD *)a1 + 3) = std::
_Function_handler<std::
variant> ()(void),main::{lambda(void)#1}>::
_M_invoke;

//level 2
std::
__invoke_r<std::
variant>,main::{lambda(void)#1} &>(a1, pointer);

//level 3
std::
__invoke_impl<std::
variant>,main::{lambda(void)#1} &>(a1, v2);

//level 4
main::{lambda(void)#1}::
operator()(a1, v2);

//level5
v8 = __readfsqword(0x28u);
 v2 = *(_QWORD **)a2;
 v3 = *(_QWORD *)(a2 + 32);
 v4 = *(_QWORD *)(a2 + 8);
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_E_EclIJRS7_EEEDcDpOT_(
 v6,
 *(_QWORD *)(a2 + 16),
 *(_QWORD *)(a2 + 24));
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_E0_EclIJSB_EEEDcDpOT_(
 v7,
 v4,
 v6);
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E3_EclIJSB_RSB_EEEDcDpOT_(
 a1,
 v2,
 (__int64)v7,
 v3);
 std::
variant>::~variant((__int64)v7);
 std::
variant>::~variant((__int64)v6);
 return a1

二

pyda trace

FROM ubuntu:24.04 as target

FROM ghcr.io/ndrewh/pyda

COPY --from=target /usr/lib/x86_64-linux-gnu/ /target_libs/

RUN apt update && apt install -y patchelf

COPY F /F
RUN patchelf --set-interpreter /target_libs/ld-linux-x86-64.so.2 --set-rpath /target_libs/ /F
RUN apt install -y binutils

from pyda import *
from pwnlib.elf.elf import ELF
from pwnlib.util.packing import u64, u32
import string
import sys
import subprocess
from collections import defaultdict

p = process()

e = ELF(p.exe_path)
e.address = p.maps[p.exe_path].base

plt_map = { e.plt[x]: x for x in e.plt }

def get_cmp(proc):
 p = subprocess.run(f"objdump -M intel -d {proc.exe_path} | grep cmp", shell=True, capture_output=True)

 output = p.stdout.decode()
 cmp_locs = {}
 for l in output.split("n"):
 if len(l) <= 1:
 continue

 # TODO: memory cmp
 if "QWORD PTR" in l:
 continue

 if ":t" not in l:
 continue

 cmp_locs[int(l.split(":")[0].strip(), 16)] = l.split()[-1]

 return cmp_locs

cmp_locs_unfiltered = get_cmp(p)
cmp_locs = {}
for (a, v) in cmp_locs_unfiltered.items():
 info = v.split(",")
 if len(info) != 2:
 continue
 if "[" in info[0] or "[" in info[1]:
 continue

 if "0x" in info[0] or "0x" in info[1]:
 continue

 cmp_locs[a] = info

print(f"cmp_locs: {len(cmp_locs)}")

eq_count = 0
neq_count = 0
reg_map = {
 "eax": "rax",
 "ebx": "rbx",
 "ecx": "rcx",
 "edx": "rdx",
 "esi": "rsi",
 "edi": "rdi",
 "ebp": "rbp",
 "esp": "rsp",
 "r8d": "r8",
}

counts_by_pc = defaultdict(int)
good_cmps = defaultdict(int)
def cmp_hook(p):
 global eq_count, neq_count
 info = cmp_locs[p.regs.pc - e.address]

 counts_by_pc[p.regs.pc - e.address] += 1

 reg1 = reg_map.get(info[0], info[0])
 reg2 = reg_map.get(info[1], info[1])
 r1 = p.regs[reg1]
 r2 = p.regs[reg2]
 eq = r1 == r2

 if eq:
 eq_count += 1
 else:
 neq_count += 1

 print(f"cmp @ {hex(p.regs.rip - e.address)} {reg1}={hex(r1)} {reg2}={hex(r2)} {eq}")

for x in cmp_locs:
 p.hook(e.address + x, cmp_hook)

p.run()

pyda cmplog.py -- /F
cmp_locs: 46
FLAG: AAAAAAAAAAAAAAAA
//.. TOO LONG NOT TO SHOW
cmp @ 0x182a7 rcx=0x10 rdx=0x40 False
"Wrong"

pyda cmplog.py -- /F
cmp_locs: 46
FLAG: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
//.. TOO LONG NOT TO SHOW
cmp @ 0x1891b rcx=0xc3df45f3 rdx=0x11793013 False
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000002 rax=0x100000001 False
"Wrong"

cmp @ 0x1891b rcx=0xc3df45f3 rdx=0x11793013 False

pyda cmplog.py -- /F
cmp_locs: 46
FLAG:
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
//.. TOO LONG NOT TO SHOW
cmp @ 0x1891b rcx=0x5b0608cd rdx=0x11793013 False
//.. TOO LONG NOT TO SHOW
"Wrong"

from pwn import *
from pyda import *
from pwnlib.elf.elf import ELF
from pwnlib.util.packing import *

p = process(io=True)

e = ELF(p.exe_path)

e.address = p.maps[p.exe_path].base

base_address = e.address
print(hex(base_address))

def cons(p):
 print(f"cons {hex(p.regs.rip-base_address),hex(u32(p.read(p.regs.rdi, 4))), hex(u32(p.read(p.regs.rsi, 4))), hex(u32(p.read(p.regs.rdx, 4)))}")

p.hook(e.address + 0x15a06, cons)

p.recvuntil("FLAG: ")
p.sendline(("ABCDEFGH").ljust(0x40,"A"))
p.run()

//enc
cons ('0x15a06', '0x0', '0xb7e9a2a4', '0x0')
cons ('0x15a06', '0x0', '0x1904c652', '0xdbbfdbf0')
cons ('0x15a06', '0x0', '0xbe8afe4d', '0xdbbfdc60')
cons ('0x15a06', '0x0', '0xbd18775a', '0xdbbfdcd0')
cons ('0x15a06', '0x0', '0x82841cf4', '0xdbbfdd40')
cons ('0x15a06', '0x0', '0xd2c1d5af', '0xdbbfddb0')
cons ('0x15a06', '0x0', '0xf389c4a', '0xdbbfde20')
cons ('0x15a06', '0x0', '0x451f151a', '0xdbbfde90')
cons ('0x15a06', '0x0', '0xd5689a8c', '0xdbbfdf00')
cons ('0x15a06', '0x0', '0x927b5bd9', '0xdbbfdf70')
cons ('0x15a06', '0x0', '0xf86c82d7', '0xdbbfdfe0')
cons ('0x15a06', '0x0', '0x34bc7c60', '0xdbbfe050')
cons ('0x15a06', '0x0', '0x97aef869', '0xdbbfe0c0')
cons ('0x15a06', '0x0', '0x2c0cccdd', '0xdbbfe130')
cons ('0x15a06', '0x0', '0x88d2ec9b', '0xdbbfe1a0')
cons ('0x15a06', '0x0', '0x11793013', '0xdbbfe210')

//sbox
cons ('0x15a06', '0x0', '0x7', '0x0')
cons ('0x15a06', '0x0', '0x0', '0xdbbfe2f0')
cons ('0x15a06', '0x0', '0xc', '0xdbbfe360')
cons ('0x15a06', '0x0', '0xd', '0xdbbfe3d0')
cons ('0x15a06', '0x0', '0x2', '0xdbbfe440')
cons ('0x15a06', '0x0', '0xf', '0xdbbfe4b0')
cons ('0x15a06', '0x0', '0xb', '0xdbbfe520')
cons ('0x15a06', '0x0', '0x8', '0xdbbfe590')
cons ('0x15a06', '0x0', '0x6', '0xdbbfe600')
cons ('0x15a06', '0x0', '0x5', '0xdbbfe670')
cons ('0x15a06', '0x0', '0x9', '0xdbbfe6e0')
cons ('0x15a06', '0x0', '0x4', '0xdbbfe750')
cons ('0x15a06', '0x0', '0xa', '0xdbbfe7c0')
cons ('0x15a06', '0x0', '0x1', '0xdbbfe830')
cons ('0x15a06', '0x0', '0xe', '0xdbbfe8a0')
cons ('0x15a06', '0x0', '0x3', '0xdbbfe910')

//input
cons ('0x15a06', '0x0', '0x41414141', '0x0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbffe30')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbffea0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbfff10')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbfff80')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbffff0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00060')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc000d0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00140')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc001b0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00220')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00290')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00300')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00370')
cons ('0x15a06', '0x0', '0x48474645', '0xdbc003e0')
cons ('0x15a06', '0x0', '0x44434241', '0xdbc00450')

//1 sub_byte
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0x0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00650')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc007a0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc008f0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00960')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc009d0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00a40')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ab0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b20')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b90')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c00')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c70')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ce0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00d50')
cons ('0x15a06', '0x862acd7e', '0x48464549', '0xdbc00dc0')
cons ('0x15a06', '0x862acd7e', '0x444a414e', '0xdbc00e30')

//2 mul 0xe14de95e
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0x0')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc006c0')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00730')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00f10')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00810')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00880')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00f80')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00570')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc005e0')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc00ff0')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc01060')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc010d0')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc01140')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc011b0')
cons ('0x15a06', '0x0', '0xd36975c1', '0xdbc01220')
cons ('0x15a06', '0x0', '0xe14de95e', '0xdbc01290')

//3 rotl(0x93af4e5e, 29) ^ rotl(0x93af4e5e, 17) ^ rotl(0xd36975c1, 7) ^ 0xe14de95e
0xd 0xc
cons ('0x15a06', '0x862acd8c', '0x93af4e5e', '0x0')
cons ('0x15a06', '0x862acd8c', '0x93af4e5e', '0xdbc01370')
cons ('0x15a06', '0x862acd8c', '0x93af4e5e', '0xdbc00b20')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00e30')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00dc0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00d50')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00ce0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00c70')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00c00')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00b90')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00ea0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00650')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc007a0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc008f0')
cons ('0x15a06', '0x862acd8c', '0x4a06941d', '0xdbc00960')
cons ('0x15a06', '0x862acd8c', '0x1b3fc722', '0xdbc009d0')

//1 sub_byte
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0x0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00650')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc007a0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc008f0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00960')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc009d0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00a40')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ab0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b20')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b90')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c00')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c70')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ce0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00d50')
cons ('0x15a06', '0x862acd7e', '0x48464549', '0xdbc00dc0')
cons ('0x15a06', '0x862acd7e', '0x444a414e', '0xdbc00e30')

三

gdb + ida + pyda backtrace 破解加密逻辑

from pwn import *
from pyda import *
from pwnlib.elf.elf import ELF
from pwnlib.util.packing import *

p = process(io=True)

e = ELF(p.exe_path)

e.address = p.maps[p.exe_path].base

base_address = e.address
print(hex(base_address))

def get_symbol_name(addr):
 for name, sym in e.symbols.items():
 print(name,hex(sym-base_address))
 #if sym == addr:
 # return name
 return "unknown"


def bt_hook(p):
 print(f"Stack trace at {hex(p.regs.rip)}:")

 current_rbp = p.regs.rbp
 current_rsp = p.regs.rsp

 try:
 frame_count = 0
 while current_rbp:
 ret_addr = u64(p.read(current_rbp + 8, 8))
 #fun_name = get_symbol_name(ret_addr)
 #print(fun_name)
 offset = ret_addr - base_address
 print(f"Frame #{frame_count}: ret = {hex(offset)}")

 current_rbp = u64(p.read(current_rbp, 8))
 frame_count += 1

 if frame_count > 20:
 break

 
except Exception as e:
 print(f"Error while unwinding stack: {e}")

 print("nRegisters:")
 print(f"RIP: {hex(p.regs.rip)}")
 print(f"RSP: {hex(p.regs.rsp)}")
 print(f"RBP: {hex(p.regs.rbp)}")
 print(f"[RSI]: {hex(u32(p.read(p.regs.rsi, 4)))}")
 #if u32(p.read(p.regs.rsi, 4)) == 0x444a414e | u32(p.read(p.regs.rsi, 4)) == 0x93af4e5e:
 input("continue")

#p.hook(e.address + 0x1891b, bt_hook)

def cons(p):
 print(f"cons {hex(p.regs.rip-base_address),hex(u32(p.read(p.regs.rdi, 4))), hex(u32(p.read(p.regs.rsi, 4))), hex(u32(p.read(p.regs.rdx, 4)))}")

#if u32(p.read(p.regs.rsi, 4)) == 0x4e4e4e4e:
p.hook(e.address + 0x15a06,bt_hook)

#p.hook(e.address + 0x15a06, cons)

p.recvuntil("FLAG: ")
p.sendline(("ABCDEFGH").ljust(0x40,"A"))
#get_symbol_name(1)
p.run()

Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x8741
Frame #7: ret = 0x13a61
Frame #8: ret = 0x117c2
Frame #9: ret = 0xf18e
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x8a06
Frame #13: ret = 0x4cec
Frame #14: ret = 0xc124
Frame #15: ret = 0x1430f
Frame #16: ret = 0x12afe
Frame #17: ret = 0x1007c
Frame #18: ret = 0x167d4
Frame #19: ret = 0x3ba6
Frame #20: ret = 0xc427

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0cb268
RBP: 0x7ffcab0cb310
[RSI]: 0x444a414e
continue
Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x8e67
Frame #7: ret = 0x13c1b
Frame #8: ret = 0x11bae
Frame #9: ret = 0xf4bc
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x914a
Frame #13: ret = 0x8c54
Frame #14: ret = 0x1192b
Frame #15: ret = 0xf2e2
Frame #16: ret = 0xd73f
Frame #17: ret = 0x8dcc
Frame #18: ret = 0x13c1b
Frame #19: ret = 0x11bae
Frame #20: ret = 0xf4bc

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0c5388
RBP: 0x7ffcab0c5430
[RSI]: 0x93af4e5e
continue

Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x8741 // first_transform
Frame #7: ret = 0x13a61
Frame #8: ret = 0x117c2
Frame #9: ret = 0xf18e
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x8a06
Frame #13: ret = 0x8558
Frame #14: ret = 0x1153f
Frame #15: ret = 0xefb4
Frame #16: ret = 0xd539
Frame #17: ret = 0x86d0
Frame #18: ret = 0x13a61
Frame #19: ret = 0x117c2
Frame #20: ret = 0xf18e

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0c5688
RBP: 0x7ffcab0c5730
[RSI]: 0x4e4e4e4e

0x41414141 -> 0x4e4e4e4e

v2 = *a2;
 v3 = a2[5];
 v4 = a2[7];
 v5 = a2[6];
 v10 = 1;
 std::
variant>::
variant(
 (__int64)v14,
 (__int64)&v10);
 std::
variant>::
variant((__int64)v13, a2[4]);
 ADD((__int64)v15, v5, (__int64)v13, (__int64)v14);
 ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E1_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 (__int64)v16,
 v3,
 a2[3],
 (__int64)v15,
 v4);
 v6 = (__int64 *)a2[1];
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E_EclIJRSB_SF_EEEDcDpOT_(
 (__int64)v11,
 (__int64 *)a2[2],
 a2[3],
 a2[4]);
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E0_EclIJSB_EEEDcDpOT_(
 (__int64)v12,
 v6,
 (__int64)v11);
 main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v12,
 (__int64)v16,
 v7,
 v8);
 std::
variant>::~variant((__int64)v12);// 0X8741

ADD
// 增加索引
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E1_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_
//递归调用
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E0_EclIJSB_EEEDcDpOT_(
 (__int64)v12,
 v6,
 (__int64)v11);
 // do first_transform
 main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v12,
 (__int64)v16,
 v7,
 v8);
 // 存储第一组密文

ADD((__int64)v15, v5, (__int64)v13, (__int64)v14);
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E1_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 (__int64)v16,
 v3,
 a2[3],
 (__int64)v15,
 v4);
v6 = (__int64 *)a2[1];
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E_EclIJRSB_SF_EEEDcDpOT_(
 (__int64)v11,
 (__int64 *)a2[2],
 a2[3],
 a2[4]);
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E0_EclIJSB_EEEDcDpOT_(
 (__int64)v12,
 v6,
 (__int64)v11);
main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v12,
 (__int64)v16,
 v7,
 v8);

In [56]: sbox = [0x7,
 ...: 0x0,
 ...: 0xc,
 ...: 0xd,
 ...: 0x2,
 ...: 0xf,
 ...: 0xb,
 ...: 0x8,
 ...: 0x6,
 ...: 0x5,
 ...: 0x9,
 ...: 0x4,
 ...: 0xa,
 ...: 0x1,
 ...: 0xe,
 ...: 0x3][::-1]

In [57]: hex(sbox[0x4])
Out[57]: '0x4'

In [58]: hex(sbox[0x1])
Out[58]: '0xe'

ADD((__int64)v17, v5, (__int64)v15, (__int64)v16);
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E2_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 v18,
 v3,
 a2[3],
 v17,
 v4);
v6 = a2[1];
v10 = 0x4E6A44B9;
std::
variant>::
variant(
 (__int64)v13,
 (__int64)&v10);
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E_EclIJRSB_SF_EEEDcDpOT_(
 (__int64)v12,
 (__int64 *)a2[2],
 a2[3],
 a2[4]);
main::{lambda(std::
variant>,std::
variant>)#3}::
operator()(
 (__int64)v14,
 v6,
 (__int64)v12,
 (__int64)v13);//32bits mul
main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v14,
 (__int64)v18,
 v7,
 v8);

__int64 __fastcall main::{lambda(std::
variant>,std::
variant>)#3}::
operator()(
 __int64 a1,
 __int64 a2,
 __int64 a3,
 __int64 a4)
{
 int v4; // ebx
 int v7; // [rsp+24h] [rbp-1Ch] BYREF
 unsigned __int64 v8; // [rsp+28h] [rbp-18h]

 v8 = __readfsqword(0x28u);
 v4 = *(_DWORD *)std::
get>(a3);
 v7 = v4 * *(_DWORD *)std::
get>(a4);
 std::
variant>::
variant(
 a1,
 (__int64)&v7);
 return a1;
}

In [59]: hex( 0x4E6A44B9 * 0x4e4e4e4e & 2 ** 32 -1)
Out[59]: '0x93af4e5e'

Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x983e
Frame #7: ret = 0x13ddb
Frame #8: ret = 0x11fde
Frame #9: ret = 0xf804
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x9f2e
Frame #13: ret = 0x13f95
Frame #14: ret = 0x12340
Frame #15: ret = 0xfa54
Frame #16: ret = 0x167d4
Frame #17: ret = 0x3ba6
Frame #18: ret = 0xa5a6
Frame #19: ret = 0x93cf
Frame #20: ret = 0x11d2f

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0c00e8
RBP: 0x7ffcab0c0190
[RSI]: 0xac0af82
continue

ADD((__int64)v16, v5, (__int64)v14, (__int64)v15);
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_SC_E_EEclIJRSC_SI_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 (__int64)v17,
 v3,
 a2[2],
 a2[5],
 (__int64)v16,
 v4);
v6 = (__int64 *)a2[1];
std::
variant>::
variant((__int64)v12, a2[3]);
std::
variant>::
variant((__int64)v11, a2[2]);
main::{lambda(std::
variant>,std::
variant>)#21}::
operator()(
 (__int64)v13,
 v6,
 (__int64)v11,
 (__int64)v12);// DO THIRD TRANSFORM
main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v13,
 (__int64)v17,
 v7,
 v8);

rotl(p[i+3], 29) ^ rotl(p[i+2], 17) ^ rotl(p[i+1], 7) ^ p[i]

In [62]: hex(rotl(0x93af4e5e, 29) ^ rotl(0x93af4e5e, 17) ^ rotl(0x93af4e5e, 7) ^ 0x93af4e5e)
Out[62]: '0xac0af82'

四

破解

from pwn import *
import copy
sbox = [0x7,
 0x0,
 0xc,
 0xd,
 0x2,
 0xf,
 0xb,
 0x8,
 0x6,
 0x5,
 0x9,
 0x4,
 0xa,
 0x1,
 0xe,
 0x3][::-1]

sbox_rev = {}
for index,num in enumerate(sbox):
 sbox_rev[num] = index

def rotl(num,offset):
 return (num << offset | num >> (32 - offset)) & 2 ** 32 - 1

def enc(plainlist):
 enclist = []
 oldlist = plainlist
 start = 0xc
 for i in range(8):
 newlist = []
 #sub_byte
 for num in oldlist:
 newnum = 0
 for j in range(8):
 index = num >> (4*j) & 0xf
 newnum |= sbox[index] << (4*j)
 newlist.append(newnum)
 #mul
 for index,num in enumerate(newlist):
 newlist[index] = ((num * 0x4E6A44B9) & 2 ** 32 - 1)
 #rotl ^ rotl ^ rotl ^ num
 cur = start + i
 roxlist = copy.deepcopy(newlist)
 for k in range(13):
 val = rotl(roxlist[(cur+1)%16],7) ^ rotl(roxlist[(cur+2)%16],17) ^ rotl(roxlist[(cur+3)%16],29) ^ roxlist[cur%16]
 newlist[cur%16] = val
 cur -= 1
 oldlist = newlist
 enclist = newlist
 for i in newlist:
 print(hex(i),end=',')
 print()
 return enclist

def dec(enc_list):
 print("dec-------------------------------------------------------------------------------------------")
 plain_list =[]
 oldlist = enc_list
 start = 3
 for i in range(8):
 newlist = []
 #rotl ^ rotl ^ rotl ^ num
 cur = start - i
 roxlist = oldlist
 for k in range(13):
 val = rotl(roxlist[(cur+1)%16],7) ^ rotl(roxlist[(cur+2)%16],17) ^ rotl(roxlist[(cur+3)%16],29) ^ roxlist[(cur)%16]
 oldlist[(cur)%16] = val
 cur -= 1
 # for i in oldlist:
 # print(hex(i),end=',')
 # print()
 #mul
 for index,num in enumerate(oldlist):
 oldlist[index] = ((num * 0x20808189) & 2 ** 32 - 1)
 #sub_byte
 for num in oldlist:
 newnum = 0
 for j in range(8):
 index = num >> (4*j) & 0xf
 newnum |= sbox_rev[index] << (4*j)
 newlist.append(newnum)
 oldlist = newlist
 plain_list = newlist
 return plain_list

# plaintext = ("ABCDEFGH").ljust(0x40,"A")
# plainlist = []

# for i in range(0,len(plaintext),4):
# plainlist.append(u32(plaintext[i:i+4]))
# enc_list = enc(plainlist)

enc_list = [ 0xb7e9a2a4,
 0x1904c652,
 0xbe8afe4d,
 0xbd18775a,
 0x82841cf4,
 0xd2c1d5af,
 0xf389c4a,
 0x451f151a,
 0xd5689a8c,
 0x927b5bd9,
 0xf86c82d7,
 0x34bc7c60,
 0x97aef869,
 0x2c0cccdd,
 0x88d2ec9b,
 0x11793013][::-1]

plain_list = dec(enc_list)

flag = b''
for num in plain_list:
 flag += int.to_bytes(num,4,'little')

print(flag)
#b'SECCON{fUnCt10n4l_pRoGr4mM1n6_1s_pR4c7iC4lLy_a_pUr3_0bfu5c4T1oN}'

看雪ID：SleepAlone

https://bbs.kanxue.com/user-home-950548.htm

*本文为看雪论坛精华文章，由 SleepAlone 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
/f
FLAG: SECCON{fUnCt10n4l_pRoGr4mM1n6_1s_pR4c7iC4lLy_a_pUr3_0bfu5c4T1oN}
"Correct"
一
ida 逆向初探
v84 = 0;
 std::
variant>::
variant(
 (__int64)v106,
 (__int64)&v84);
 v83 = 0xB7E9A2A4;
 std::
variant>::
variant(
 (__int64)v105,
 (__int64)&v83);
 main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 (__int64)v107,
 (__int64)&v78,
 (__int64)v105,
 (__int64)v106,
 v3,
 v4);
std::
make_shared<Cons,std::
variant> &,std::
variant> &>(
 (__int64)v7,
 a3,
 a4);
 std::
variant>::
variant<std::
shared_ptr<Cons>,void,void,std::
shared_ptr<Cons>,void>(
 a1,
 (__int64)v7);
 std::
shared_ptr<Cons>::~shared_ptr(v7);
v5 = operator new(0x50uLL, a1);
 v6 = std::
forward<std::
variant> &>(a3);
 std::
variant>::
variant((__int64)v11, v6);
 v7 = std::
forward<std::
variant> &>(a2);
 std::
variant>::
variant((__int64)v10, v7);
 Cons::
Cons(v5, (__int64)v10, (__int64)v11);
 std::
variant>::~variant((__int64)v10);
 std::
variant>::~variant((__int64)v11);
std::
function<std::
variant> ()(void)>::
function<main::{lambda(void)#1},void>(
 (std::
_Function_base *)v127,
 (__int64)v95);
// level 1
*((_QWORD *)a1 + 3) = std::
_Function_handler<std::
variant> ()(void),main::{lambda(void)#1}>::
_M_invoke;

//level 2
std::
__invoke_r<std::
variant>,main::{lambda(void)#1} &>(a1, pointer);

//level 3
std::
__invoke_impl<std::
variant>,main::{lambda(void)#1} &>(a1, v2);

//level 4
main::{lambda(void)#1}::
operator()(a1, v2);

//level5
v8 = __readfsqword(0x28u);
 v2 = *(_QWORD **)a2;
 v3 = *(_QWORD *)(a2 + 32);
 v4 = *(_QWORD *)(a2 + 8);
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_E_EclIJRS7_EEEDcDpOT_(
 v6,
 *(_QWORD *)(a2 + 16),
 *(_QWORD *)(a2 + 24));
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_E0_EclIJSB_EEEDcDpOT_(
 v7,
 v4,
 v6);
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E3_EclIJSB_RSB_EEEDcDpOT_(
 a1,
 v2,
 (__int64)v7,
 v3);
 std::
variant>::~variant((__int64)v7);
 std::
variant>::~variant((__int64)v6);
 return a1
二
pyda trace
FROM ubuntu:24.04 as target

FROM ghcr.io/ndrewh/pyda

COPY --from=target /usr/lib/x86_64-linux-gnu/ /target_libs/

RUN apt update && apt install -y patchelf

COPY F /F
RUN patchelf --set-interpreter /target_libs/ld-linux-x86-64.so.2 --set-rpath /target_libs/ /F
RUN apt install -y binutils
from pyda import *
from pwnlib.elf.elf import ELF
from pwnlib.util.packing import u64, u32
import string
import sys
import subprocess
from collections import defaultdict

p = process()

e = ELF(p.exe_path)
e.address = p.maps[p.exe_path].base

plt_map = { e.plt[x]: x for x in e.plt }

def get_cmp(proc):
 p = subprocess.run(f"objdump -M intel -d {proc.exe_path} | grep cmp", shell=True, capture_output=True)

 output = p.stdout.decode()
 cmp_locs = {}
 for l in output.split("n"):
 if len(l) <= 1:
 continue

 # TODO: memory cmp
 if "QWORD PTR" in l:
 continue

 if ":t" not in l:
 continue

 cmp_locs[int(l.split(":")[0].strip(), 16)] = l.split()[-1]

 return cmp_locs

cmp_locs_unfiltered = get_cmp(p)
cmp_locs = {}
for (a, v) in cmp_locs_unfiltered.items():
 info = v.split(",")
 if len(info) != 2:
 continue
 if "[" in info[0] or "[" in info[1]:
 continue

 if "0x" in info[0] or "0x" in info[1]:
 continue

 cmp_locs[a] = info

print(f"cmp_locs: {len(cmp_locs)}")

eq_count = 0
neq_count = 0
reg_map = {
 "eax": "rax",
 "ebx": "rbx",
 "ecx": "rcx",
 "edx": "rdx",
 "esi": "rsi",
 "edi": "rdi",
 "ebp": "rbp",
 "esp": "rsp",
 "r8d": "r8",
}

counts_by_pc = defaultdict(int)
good_cmps = defaultdict(int)
def cmp_hook(p):
 global eq_count, neq_count
 info = cmp_locs[p.regs.pc - e.address]

 counts_by_pc[p.regs.pc - e.address] += 1

 reg1 = reg_map.get(info[0], info[0])
 reg2 = reg_map.get(info[1], info[1])
 r1 = p.regs[reg1]
 r2 = p.regs[reg2]
 eq = r1 == r2

 if eq:
 eq_count += 1
 else:
 neq_count += 1

 print(f"cmp @ {hex(p.regs.rip - e.address)} {reg1}={hex(r1)} {reg2}={hex(r2)} {eq}")

for x in cmp_locs:
 p.hook(e.address + x, cmp_hook)

p.run()
pyda cmplog.py -- /F
cmp_locs: 46
FLAG: AAAAAAAAAAAAAAAA
//.. TOO LONG NOT TO SHOW
cmp @ 0x182a7 rcx=0x10 rdx=0x40 False
"Wrong"
pyda cmplog.py -- /F
cmp_locs: 46
FLAG: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
//.. TOO LONG NOT TO SHOW
cmp @ 0x1891b rcx=0xc3df45f3 rdx=0x11793013 False
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True
cmp @ 0x15787 rdx=0x100000002 rax=0x100000001 False
"Wrong"
cmp @ 0x1891b rcx=0xc3df45f3 rdx=0x11793013 False
pyda cmplog.py -- /F
cmp_locs: 46
FLAG:
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
//.. TOO LONG NOT TO SHOW
cmp @ 0x1891b rcx=0x5b0608cd rdx=0x11793013 False
//.. TOO LONG NOT TO SHOW
"Wrong"
from pwn import *
from pyda import *
from pwnlib.elf.elf import ELF
from pwnlib.util.packing import *

p = process(io=True)

e = ELF(p.exe_path)

e.address = p.maps[p.exe_path].base

base_address = e.address
print(hex(base_address))

def cons(p):
 print(f"cons {hex(p.regs.rip-base_address),hex(u32(p.read(p.regs.rdi, 4))), hex(u32(p.read(p.regs.rsi, 4))), hex(u32(p.read(p.regs.rdx, 4)))}")

p.hook(e.address + 0x15a06, cons)

p.recvuntil("FLAG: ")
p.sendline(("ABCDEFGH").ljust(0x40,"A"))
p.run()
//enc
cons ('0x15a06', '0x0', '0xb7e9a2a4', '0x0')
cons ('0x15a06', '0x0', '0x1904c652', '0xdbbfdbf0')
cons ('0x15a06', '0x0', '0xbe8afe4d', '0xdbbfdc60')
cons ('0x15a06', '0x0', '0xbd18775a', '0xdbbfdcd0')
cons ('0x15a06', '0x0', '0x82841cf4', '0xdbbfdd40')
cons ('0x15a06', '0x0', '0xd2c1d5af', '0xdbbfddb0')
cons ('0x15a06', '0x0', '0xf389c4a', '0xdbbfde20')
cons ('0x15a06', '0x0', '0x451f151a', '0xdbbfde90')
cons ('0x15a06', '0x0', '0xd5689a8c', '0xdbbfdf00')
cons ('0x15a06', '0x0', '0x927b5bd9', '0xdbbfdf70')
cons ('0x15a06', '0x0', '0xf86c82d7', '0xdbbfdfe0')
cons ('0x15a06', '0x0', '0x34bc7c60', '0xdbbfe050')
cons ('0x15a06', '0x0', '0x97aef869', '0xdbbfe0c0')
cons ('0x15a06', '0x0', '0x2c0cccdd', '0xdbbfe130')
cons ('0x15a06', '0x0', '0x88d2ec9b', '0xdbbfe1a0')
cons ('0x15a06', '0x0', '0x11793013', '0xdbbfe210')

//sbox
cons ('0x15a06', '0x0', '0x7', '0x0')
cons ('0x15a06', '0x0', '0x0', '0xdbbfe2f0')
cons ('0x15a06', '0x0', '0xc', '0xdbbfe360')
cons ('0x15a06', '0x0', '0xd', '0xdbbfe3d0')
cons ('0x15a06', '0x0', '0x2', '0xdbbfe440')
cons ('0x15a06', '0x0', '0xf', '0xdbbfe4b0')
cons ('0x15a06', '0x0', '0xb', '0xdbbfe520')
cons ('0x15a06', '0x0', '0x8', '0xdbbfe590')
cons ('0x15a06', '0x0', '0x6', '0xdbbfe600')
cons ('0x15a06', '0x0', '0x5', '0xdbbfe670')
cons ('0x15a06', '0x0', '0x9', '0xdbbfe6e0')
cons ('0x15a06', '0x0', '0x4', '0xdbbfe750')
cons ('0x15a06', '0x0', '0xa', '0xdbbfe7c0')
cons ('0x15a06', '0x0', '0x1', '0xdbbfe830')
cons ('0x15a06', '0x0', '0xe', '0xdbbfe8a0')
cons ('0x15a06', '0x0', '0x3', '0xdbbfe910')

//input
cons ('0x15a06', '0x0', '0x41414141', '0x0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbffe30')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbffea0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbfff10')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbfff80')
cons ('0x15a06', '0x0', '0x41414141', '0xdbbffff0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00060')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc000d0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00140')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc001b0')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00220')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00290')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00300')
cons ('0x15a06', '0x0', '0x41414141', '0xdbc00370')
cons ('0x15a06', '0x0', '0x48474645', '0xdbc003e0')
cons ('0x15a06', '0x0', '0x44434241', '0xdbc00450')

//1 sub_byte
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0x0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00650')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc007a0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc008f0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00960')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc009d0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00a40')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ab0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b20')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b90')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c00')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c70')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ce0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00d50')
cons ('0x15a06', '0x862acd7e', '0x48464549', '0xdbc00dc0')
cons ('0x15a06', '0x862acd7e', '0x444a414e', '0xdbc00e30')

//2 mul 0xe14de95e
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0x0')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc006c0')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00730')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00f10')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00810')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00880')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00f80')
cons ('0x15a06', '0x862acd7e', '0x93af4e5e', '0xdbc00570')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc005e0')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc00ff0')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc01060')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc010d0')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc01140')
cons ('0x15a06', '0x0', '0x93af4e5e', '0xdbc011b0')
cons ('0x15a06', '0x0', '0xd36975c1', '0xdbc01220')
cons ('0x15a06', '0x0', '0xe14de95e', '0xdbc01290')

//3 rotl(0x93af4e5e, 29) ^ rotl(0x93af4e5e, 17) ^ rotl(0xd36975c1, 7) ^ 0xe14de95e
0xd 0xc
cons ('0x15a06', '0x862acd8c', '0x93af4e5e', '0x0')
cons ('0x15a06', '0x862acd8c', '0x93af4e5e', '0xdbc01370')
cons ('0x15a06', '0x862acd8c', '0x93af4e5e', '0xdbc00b20')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00e30')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00dc0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00d50')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00ce0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00c70')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00c00')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00b90')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00ea0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc00650')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc007a0')
cons ('0x15a06', '0x862acd8c', '0xac0af82', '0xdbc008f0')
cons ('0x15a06', '0x862acd8c', '0x4a06941d', '0xdbc00960')
cons ('0x15a06', '0x862acd8c', '0x1b3fc722', '0xdbc009d0')
//1 sub_byte
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0x0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00650')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc007a0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc008f0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00960')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc009d0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00a40')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ab0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b20')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00b90')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c00')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00c70')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00ce0')
cons ('0x15a06', '0x862acd7e', '0x4e4e4e4e', '0xdbc00d50')
cons ('0x15a06', '0x862acd7e', '0x48464549', '0xdbc00dc0')
cons ('0x15a06', '0x862acd7e', '0x444a414e', '0xdbc00e30')
三
gdb + ida + pyda backtrace 破解加密逻辑
from pwn import *
from pyda import *
from pwnlib.elf.elf import ELF
from pwnlib.util.packing import *

p = process(io=True)

e = ELF(p.exe_path)

e.address = p.maps[p.exe_path].base

base_address = e.address
print(hex(base_address))

def get_symbol_name(addr):
 for name, sym in e.symbols.items():
 print(name,hex(sym-base_address))
 #if sym == addr:
 # return name
 return "unknown"


def bt_hook(p):
 print(f"Stack trace at {hex(p.regs.rip)}:")

 current_rbp = p.regs.rbp
 current_rsp = p.regs.rsp

 try:
 frame_count = 0
 while current_rbp:
 ret_addr = u64(p.read(current_rbp + 8, 8))
 #fun_name = get_symbol_name(ret_addr)
 #print(fun_name)
 offset = ret_addr - base_address
 print(f"Frame #{frame_count}: ret = {hex(offset)}")

 current_rbp = u64(p.read(current_rbp, 8))
 frame_count += 1

 if frame_count > 20:
 break

 
except Exception as e:
 print(f"Error while unwinding stack: {e}")

 print("nRegisters:")
 print(f"RIP: {hex(p.regs.rip)}")
 print(f"RSP: {hex(p.regs.rsp)}")
 print(f"RBP: {hex(p.regs.rbp)}")
 print(f"[RSI]: {hex(u32(p.read(p.regs.rsi, 4)))}")
 #if u32(p.read(p.regs.rsi, 4)) == 0x444a414e | u32(p.read(p.regs.rsi, 4)) == 0x93af4e5e:
 input("continue")

    #p.hook(e.address + 0x1891b, bt_hook)

def cons(p):
 print(f"cons {hex(p.regs.rip-base_address),hex(u32(p.read(p.regs.rdi, 4))), hex(u32(p.read(p.regs.rsi, 4))), hex(u32(p.read(p.regs.rdx, 4)))}")

    #if u32(p.read(p.regs.rsi, 4)) == 0x4e4e4e4e:
p.hook(e.address + 0x15a06,bt_hook)

    #p.hook(e.address + 0x15a06, cons)

p.recvuntil("FLAG: ")
p.sendline(("ABCDEFGH").ljust(0x40,"A"))
    #get_symbol_name(1)
p.run()
Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x8741
Frame #7: ret = 0x13a61
Frame #8: ret = 0x117c2
Frame #9: ret = 0xf18e
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x8a06
Frame #13: ret = 0x4cec
Frame #14: ret = 0xc124
Frame #15: ret = 0x1430f
Frame #16: ret = 0x12afe
Frame #17: ret = 0x1007c
Frame #18: ret = 0x167d4
Frame #19: ret = 0x3ba6
Frame #20: ret = 0xc427

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0cb268
RBP: 0x7ffcab0cb310
[RSI]: 0x444a414e
continue
Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x8e67
Frame #7: ret = 0x13c1b
Frame #8: ret = 0x11bae
Frame #9: ret = 0xf4bc
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x914a
Frame #13: ret = 0x8c54
Frame #14: ret = 0x1192b
Frame #15: ret = 0xf2e2
Frame #16: ret = 0xd73f
Frame #17: ret = 0x8dcc
Frame #18: ret = 0x13c1b
Frame #19: ret = 0x11bae
Frame #20: ret = 0xf4bc

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0c5388
RBP: 0x7ffcab0c5430
[RSI]: 0x93af4e5e
continue
Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x8741 // first_transform
Frame #7: ret = 0x13a61
Frame #8: ret = 0x117c2
Frame #9: ret = 0xf18e
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x8a06
Frame #13: ret = 0x8558
Frame #14: ret = 0x1153f
Frame #15: ret = 0xefb4
Frame #16: ret = 0xd539
Frame #17: ret = 0x86d0
Frame #18: ret = 0x13a61
Frame #19: ret = 0x117c2
Frame #20: ret = 0xf18e

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0c5688
RBP: 0x7ffcab0c5730
[RSI]: 0x4e4e4e4e
0x41414141 -> 0x4e4e4e4e
v2 = *a2;
 v3 = a2[5];
 v4 = a2[7];
 v5 = a2[6];
 v10 = 1;
 std::
variant>::
variant(
 (__int64)v14,
 (__int64)&v10);
 std::
variant>::
variant((__int64)v13, a2[4]);
 ADD((__int64)v15, v5, (__int64)v13, (__int64)v14);
 ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E1_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 (__int64)v16,
 v3,
 a2[3],
 (__int64)v15,
 v4);
 v6 = (__int64 *)a2[1];
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E_EclIJRSB_SF_EEEDcDpOT_(
 (__int64)v11,
 (__int64 *)a2[2],
 a2[3],
 a2[4]);
 ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E0_EclIJSB_EEEDcDpOT_(
 (__int64)v12,
 v6,
 (__int64)v11);
 main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v12,
 (__int64)v16,
 v7,
 v8);
 std::
variant>::~variant((__int64)v12);// 0X8741
ADD
// 增加索引
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E1_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_
//递归调用
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E0_EclIJSB_EEEDcDpOT_(
 (__int64)v12,
 v6,
 (__int64)v11);
 // do first_transform
 main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v12,
 (__int64)v16,
 v7,
 v8);
 // 存储第一组密文
ADD((__int64)v15, v5, (__int64)v13, (__int64)v14);
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E1_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 (__int64)v16,
 v3,
 a2[3],
 (__int64)v15,
 v4);
v6 = (__int64 *)a2[1];
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E_EclIJRSB_SF_EEEDcDpOT_(
 (__int64)v11,
 (__int64 *)a2[2],
 a2[3],
 a2[4]);
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E0_EclIJSB_EEEDcDpOT_(
 (__int64)v12,
 v6,
 (__int64)v11);
main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v12,
 (__int64)v16,
 v7,
 v8);
In [56]: sbox = [0x7,
 ...: 0x0,
 ...: 0xc,
 ...: 0xd,
 ...: 0x2,
 ...: 0xf,
 ...: 0xb,
 ...: 0x8,
 ...: 0x6,
 ...: 0x5,
 ...: 0x9,
 ...: 0x4,
 ...: 0xa,
 ...: 0x1,
 ...: 0xe,
 ...: 0x3][::-1]

In [57]: hex(sbox[0x4])
Out[57]: '0x4'

In [58]: hex(sbox[0x1])
Out[58]: '0xe'
ADD((__int64)v17, v5, (__int64)v15, (__int64)v16);
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_E2_EEclIJRSC_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 v18,
 v3,
 a2[3],
 v17,
 v4);
v6 = a2[1];
v10 = 0x4E6A44B9;
std::
variant>::
variant(
 (__int64)v13,
 (__int64)&v10);
ZNKR3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESB_SB_E_EclIJRSB_SF_EEEDcDpOT_(
 (__int64)v12,
 (__int64 *)a2[2],
 a2[3],
 a2[4]);
main::{lambda(std::
variant>,std::
variant>)#3}::
operator()(
 (__int64)v14,
 v6,
 (__int64)v12,
 (__int64)v13);//32bits mul
main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v14,
 (__int64)v18,
 v7,
 v8);
__int64 __fastcall main::{lambda(std::
variant>,std::
variant>)#3}::
operator()(
 __int64 a1,
 __int64 a2,
 __int64 a3,
 __int64 a4)
{
 int v4; // ebx
 int v7; // [rsp+24h] [rbp-1Ch] BYREF
 unsigned __int64 v8; // [rsp+28h] [rbp-18h]

 v8 = __readfsqword(0x28u);
 v4 = *(_DWORD *)std::
get>(a3);
 v7 = v4 * *(_DWORD *)std::
get>(a4);
 std::
variant>::
variant(
 a1,
 (__int64)&v7);
 return a1;
}
In [59]: hex( 0x4E6A44B9 * 0x4e4e4e4e & 2 ** 32 -1)
Out[59]: '0x93af4e5e'
Stack trace at 0x7f8abea24a06:
Frame #0: ret = 0x1c40b
Frame #1: ret = 0x1bb86
Frame #2: ret = 0x1a834
Frame #3: ret = 0x18efd
Frame #4: ret = 0x1684a
Frame #5: ret = 0x3bfe
Frame #6: ret = 0x983e
Frame #7: ret = 0x13ddb
Frame #8: ret = 0x11fde
Frame #9: ret = 0xf804
Frame #10: ret = 0x167d4
Frame #11: ret = 0x3ba6
Frame #12: ret = 0x9f2e
Frame #13: ret = 0x13f95
Frame #14: ret = 0x12340
Frame #15: ret = 0xfa54
Frame #16: ret = 0x167d4
Frame #17: ret = 0x3ba6
Frame #18: ret = 0xa5a6
Frame #19: ret = 0x93cf
Frame #20: ret = 0x11d2f

Registers:
RIP: 0x7f8abea24a06
RSP: 0x7ffcab0c00e8
RBP: 0x7ffcab0c0190
[RSI]: 0xac0af82
continue
ADD((__int64)v16, v5, (__int64)v14, (__int64)v15);
ZNKSt17reference_wrapperIK3fixIZ4mainEUlT_St7variantIJjNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESt10shared_ptrI4ConsEEESC_SC_SC_E_EEclIJRSC_SI_SC_SI_EEENSt15__invoke_resultIRSF_JDpT_EE4typeEDpOSL_(
 (__int64)v17,
 v3,
 a2[2],
 a2[5],
 (__int64)v16,
 v4);
v6 = (__int64 *)a2[1];
std::
variant>::
variant((__int64)v12, a2[3]);
std::
variant>::
variant((__int64)v11, a2[2]);
main::{lambda(std::
variant>,std::
variant>)#21}::
operator()(
 (__int64)v13,
 v6,
 (__int64)v11,
 (__int64)v12);// DO THIRD TRANSFORM
main::{lambda(std::
variant>,std::
variant>)#19}::
operator()(
 a1,
 v2,
 (__int64)v13,
 (__int64)v17,
 v7,
 v8);
rotl(p[i+3], 29) ^ rotl(p[i+2], 17) ^ rotl(p[i+1], 7) ^ p[i]
In [62]: hex(rotl(0x93af4e5e, 29) ^ rotl(0x93af4e5e, 17) ^ rotl(0x93af4e5e, 7) ^ 0x93af4e5e)
Out[62]: '0xac0af82'
四
破解
from pwn import *
import copy
sbox = [0x7,
 0x0,
 0xc,
 0xd,
 0x2,
 0xf,
 0xb,
 0x8,
 0x6,
 0x5,
 0x9,
 0x4,
 0xa,
 0x1,
 0xe,
 0x3][::-1]

sbox_rev = {}
for index,num in enumerate(sbox):
 sbox_rev[num] = index

def rotl(num,offset):
 return (num << offset | num >> (32 - offset)) & 2 ** 32 - 1

def enc(plainlist):
 enclist = []
 oldlist = plainlist
 start = 0xc
 for i in range(8):
 newlist = []
 #sub_byte
 for num in oldlist:
 newnum = 0
 for j in range(8):
 index = num >> (4*j) & 0xf
 newnum |= sbox[index] << (4*j)
 newlist.append(newnum)
 #mul
 for index,num in enumerate(newlist):
 newlist[index] = ((num * 0x4E6A44B9) & 2 ** 32 - 1)
 #rotl ^ rotl ^ rotl ^ num
 cur = start + i
 roxlist = copy.deepcopy(newlist)
 for k in range(13):
 val = rotl(roxlist[(cur+1)%16],7) ^ rotl(roxlist[(cur+2)%16],17) ^ rotl(roxlist[(cur+3)%16],29) ^ roxlist[cur%16]
 newlist[cur%16] = val
 cur -= 1
 oldlist = newlist
 enclist = newlist
 for i in newlist:
 print(hex(i),end=',')
 print()
 return enclist

def dec(enc_list):
 print("dec-------------------------------------------------------------------------------------------")
 plain_list =[]
 oldlist = enc_list
 start = 3
 for i in range(8):
 newlist = []
 #rotl ^ rotl ^ rotl ^ num
 cur = start - i
 roxlist = oldlist
 for k in range(13):
 val = rotl(roxlist[(cur+1)%16],7) ^ rotl(roxlist[(cur+2)%16],17) ^ rotl(roxlist[(cur+3)%16],29) ^ roxlist[(cur)%16]
 oldlist[(cur)%16] = val
 cur -= 1
 # for i in oldlist:
 # print(hex(i),end=',')
 # print()
 #mul
 for index,num in enumerate(oldlist):
 oldlist[index] = ((num * 0x20808189) & 2 ** 32 - 1)
 #sub_byte
 for num in oldlist:
 newnum = 0
 for j in range(8):
 index = num >> (4*j) & 0xf
 newnum |= sbox_rev[index] << (4*j)
 newlist.append(newnum)
 oldlist = newlist
 plain_list = newlist
 return plain_list

# plaintext = ("ABCDEFGH").ljust(0x40,"A")
# plainlist = []

# for i in range(0,len(plaintext),4):
# plainlist.append(u32(plaintext[i:i+4]))
# enc_list = enc(plainlist)

enc_list = [ 0xb7e9a2a4,
 0x1904c652,
 0xbe8afe4d,
 0xbd18775a,
 0x82841cf4,
 0xd2c1d5af,
 0xf389c4a,
 0x451f151a,
 0xd5689a8c,
 0x927b5bd9,
 0xf86c82d7,
 0x34bc7c60,
 0x97aef869,
 0x2c0cccdd,
 0x88d2ec9b,
 0x11793013][::-1]

plain_list = dec(enc_list)

flag = b''
for num in plain_list:
 flag += int.to_bytes(num,4,'little')

print(flag)
    #b'SECCON{fUnCt10n4l_pRoGr4mM1n6_1s_pR4c7iC4lLy_a_pUr3_0bfu5c4T1oN}'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1734697505.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1734697506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1734697506.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1734697506.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/8-1734697507.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1734697507.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1734697508.gif)