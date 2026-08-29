---
title: 强网杯 S8 Rust Pwn chat-with-me 出题思路分享
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [Rust, lifetime-extension, Vec, dangling-reference, UAF, ChatBox, get_ptr, static-mut, libc-2.39, GeekCmore]
attack_chain:
  - Rust 聊天框: 1=add, 2=show, 3=edit, 4=delete, 5=exit
  - 结构: struct ChatBox { msg_list: Vec<&'static mut Msg> }
  - 漏洞: get_ptr() 通过 fn ident<'a,'b>(val_b: &'b mut T) -> &'a mut T 把栈上 msg 借用成 'static lifetime
  - push 进 Vec 后, msg 出作用域被释放, Vec 仍持有 'static 引用 → 悬垂指针
  - 利用: add → add → delete index 0 → edit index 0 (触发 UAF 写已释放栈)
  - 由于栈帧被覆盖, edit 写入可被后续 read 读到
  - libc-2.39-0ubuntu8.3, 用 pwntools + ret2libc/one_gadget
  - 难点: Rust 符号名 mangling + inline(never) 函数边界
key_payload: "Vec<&'static mut Msg> + 栈 msg 悬垂 + edit 写 UAF + 后续调用覆盖栈"
one_liner: 强网杯 S8 Rust Pwn：Vec<&'static mut Msg> 借用扩展为 'static lifetime 导致悬垂指针，edit 触发 UAF。
lesson: Rust 借用检查器不能防止所有生命周期误用，unsafe fn ident() 提升 lifetime 是经典反模式。
quality: high
---

# 强网杯 S8 Rust Pwn chat-with-me 出题思路分享

**来源**: ctfiot.com ID 219681
**作者**: GeekCmore

## 出题源码

```rust
use std::fmt;
use std::io::{self, Read, Write};

const MAX_MSG_LEN: usize = 0x50;

struct Msg {
    data: [u8; MAX_MSG_LEN],
}

impl Msg {
    #[inline(never)]
    fn new() -> Self {
        Msg { data: [0; MAX_MSG_LEN] }
    }
}

impl fmt::Display for Msg {
    #[inline(never)]
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self.data)
    }
}

#[inline(never)]
fn prompt(msg: String) {
    print!("{} > ", msg);
    io::stdout().flush().unwrap();
}

struct ChatBox {
    msg_list: Vec<&'static mut Msg>,
}

impl ChatBox {
    #[inline(never)]
    fn new() -> Self {
        ChatBox { msg_list: Vec::new() }
    }

    #[inline(never)]
    fn add_msg(&mut self) {
        println!("Adding a new message");
        self.msg_list.push(self.get_ptr());
    }

    #[inline(never)]
    fn show_msg(&mut self) {
        prompt("Index".to_string());
        let mut index = String::new();
        io::stdin().read_line(&mut index).expect("Failed to read");
        let index: usize = index.trim().parse().expect("Invalid!");
        println!("Content: {}", self.msg_list[index]);
    }

    #[inline(never)]
    fn edit_msg(&mut self) {
        prompt("Index".to_string());
        let mut index = String::new();
        io::stdin().read_line(&mut index).expect("Failed to read");
        let index: usize = index.trim().parse().expect("Invalid!");
        prompt("Content".to_string());
        let mut handle = io::stdin().lock();
        handle.read(&mut self.msg_list[index].data).expect("Failed to read");
        println!("Content: {}", self.msg_list[index]);
    }

    #[inline(never)]
    fn delete_msg(&mut self) {
        prompt("Index".to_string());
        let mut index = String::new();
        io::stdin().read_line(&mut index).expect("Failed to read");
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
        let mut msg = Msg::new();
        get_ptr(&mut msg)
    }
}
```

## 漏洞分析

### 关键: get_ptr 的 lifetime 提升
```rust
fn ident<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b mut T) -> &'a mut T {
    val_b
}
```

- `_val_a: &'a &'b ()` 把 'b 套在 'a 里 → 编译器推断 val_b 的 lifetime 为 'a
- 通过 `f: fn(_, &'a mut T) -> &'b mut T = ident` 强制 val_b 同时满足 'a 和 'b
- 实际效果：栈上 `let mut msg` 的引用被提升为 'static lifetime
- 推入 Vec 后，msg 出作用域，Vec 仍持有 'static 引用 → **悬垂指针**

## 利用思路

1. **add → add**: msg_list.push(dangling_ptr_1) + msg_list.push(dangling_ptr_2)
2. **delete index 0**: 移除 msg_list[0] 引用
3. **edit index 0**: 写入已释放栈（UAF 写）
4. 由于 Rust 释放 msg 后栈帧可被后续函数调用覆盖，edit 写入实际是写栈
5. 用 pwntools + ret2libc/one_gadget 控 rip

## 调试
```python
gs = """
b *$rebase(0x1A979)
b /home/geekcmore/RustroverProjects/chat-with-me/src/main.rs:145
set debug-file-directory /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6-dbg_2.39-0ubuntu8.3_amd64/usr/lib/debug
set directories /home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/glibc-source_2.39-0ubuntu8.3_all/usr/src/glibc/glibc-2.39
"""
```

## libc
- `libc-2.39-0ubuntu8.3_amd64`
- 路径：`/home/geekcmore/.config/cpwn/pkgs/2.39-0ubuntu8.3/amd64/libc6_2.39-0ubuntu8.3_amd64/usr/lib/x86_64-linux-gnu/libc.so.6`

## 评价
强网杯 S8 Rust Pwn 高质量出题。考察：
- **Rust 生命周期反模式**：`fn ident()` 提升 lifetime 是 unsafe 边界
- **Vec 持有悬垂引用**：编译器无法检测 'static 实际指向栈
- **Rust 符号 mangling + inline(never)**：IDA 调试技巧

是 Rust 安全研究的经典反例。
