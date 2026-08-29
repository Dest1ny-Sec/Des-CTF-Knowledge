---
title: 第二届"长城杯"信息安全铁人三项赛(防护赛)总决赛-Pwn方向部分题解
contest: 长城杯信息安全铁人三项赛
year: 2024
difficulty: medium
vuln_type: heap_exploit
tags: [Pwn-Heap,libc2.31,Protobuf,菜单题,free_hook覆盖]
attack_chain: 分析sub_12FD展示函数(循环16个qword)+sub_1141指令解析(空格/冒号分隔index字符串)→识别add/delete/show菜单→大量add堆块+rm触发free→off-by-null/0x91溢出→show Data#8泄libc_base(libc-0x3ebca0)→覆盖__free_hook→system('/bin/sh')→rm(2)触发
key_payload: pay = b':\ntitle:\nAAAAAAAAA:\nsubtitle:A' + p32(0x601)|add(b'Y'*0x120 + p64(free_hook))|add(b'/bin/sh')|add(p64(system))|rm(2)
one_liner: Protobuf格式字符串解析的菜单add/delete/show题,libc2.31通过0x91 chunk size边界溢出让show泄libc,然后多次add+rm控制chunk到__free_hook写入system,rm(2)触发
lesson: 1) ProtobufCFieldDescriptor结构体{name,id,label,type,quantifier_offset,offset,descriptor,default_value,flags}识别二进制协议格式; 2) 0x91 size chunk边界+off-by-null可破坏下一个chunk metadata; 3) libc_base = leak - 0x3ebca0(unsorted bin fd偏移); 4) __free_hook覆盖链:多次add(0x120)→rm→add(0x120-1)→rm→add(0x120-2)→rm→add(0x120-8)+p64(free_hook)逐步缩小对齐; 5) brva 0x0144F定位关键断点
quality: medium
---

## 备注

原文(https://www.ctfiot.com/259435.html)含二进制NUL字符,需用iconv清洗。文件前半部分给出sub_12FD/sub_1141伪代码与ProtobufCFieldDescriptor结构,后半部分给出完整Pwntools攻击脚本。

### 关键函数逆向

**sub_12FD** — 展示函数,循环16次(i=0..15)遍历qword_2020A8[2*i]指针数组,打印Data #i: 内容
- 数组在BSS段,16个槽位(0-15),每个槽8字节指针+8字节metadata

**sub_1141** — 指令解析
- 接收字符串a1,空格/冒号分隔参数
- 第一段a1(直到空格/冒号)为指令名(strcmp "index")
- 第二段atoi为索引(<=0xF)
- 检查v7[1](数据指针)非空则free(v7[1])+v7[1]=0+(dword)v7=0
- "No such data!" / "Invalid index!" / "Invalid argument" 错误处理

### ProtobufCFieldDescriptor结构

```
struct ProtobufCFieldDescriptor {
    char *name;              // "giaoid" / "giaosize" / "giaocontent"
    int id;                  // 1/2/3
    int label;               // 3 (required)
    int type;                // 3 (int32/string)
    int quantifier_offset;   // 0
    int offset;              // 0x18/0x20
    __int64 descriptor;      // 0
    __int64 default_value;   // 0
    int flags;               // 0
    int reserved_flags;      // 0
    int reserved_pad[1];
    __int64 reserved2;
    __int64 reserved3;
};
```

### 攻击流程

1. **初始堆块布置**(add 0x27/0xF7×7次)
2. **触发溢出**:pay = `b':\ntitle:\nAAAAAAAAA:\nsubtitle:A' + p32(0x601)` 制造0x601大小chunk触发off-by
3. **rm(0)/rm(2)/rm(3)** — 释放制造tcache
4. **show** — ru('Data #8:')→ru(': ')→r(6)泄libc_base = uu64(leak) - 0x3ebca0
5. **多次add+rm对齐** — add(b'Y'*0x127)→rm(1)→add(0x126)→rm→add(0x125)→rm
6. **写free_hook** — add(b'Y'*0x120 + p64(free_hook))
7. **触发** — add(b'/bin/sh') + add(p64(system)) + rm(2)→system('/bin/sh')

### GDB脚本

```
brva 0x0144F
```

(0x144F为关键断点,可能是add指令解析跳转位置)

## 评级

- **quality: medium** — exp脚本完整可复现,但漏洞成因(off-by-null/0x91溢出)未明确解释,brva断点位置未明确定位
- **vuln_type: heap_exploit** — glibc 2.31 + 堆溢出 + free_hook覆盖
- 攻击面:Protobuf结构识别→菜单函数逆向→堆风水→__free_hook
