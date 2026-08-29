---
title: SUSTF WriteUp - ChaMd5 Venom
contest: SUSTF
year: 2022
team: ChaMd5 Venom
difficulty: medium
vuln_type: misc_unknown
tags: [lfsr-recover, gaussian-elimination, browser-pwn, js-prototype-pollution, uaf]
attack_chain:
- lfsr(seed2, mask2, n2) 枚举 (2^12, 2^12) 找与 plain "Date" XOR 匹配
- 已知 plain 头 16 字节构造方程组
- gauss 消元解 mask1
- browser 0day: DataView.setUint32/getUint32 注入 ArrayBuffer 调
- leak libc1/libc2 = dataView.gu32(8/12)
- 改 a4.setUint32(0x98, libc1+0x2f28) 触发任意读
- 改 a5.setUint32(0, libc1-0x1967f0+0x91871) 触发任意写
- suid find /tmp → /bin/umount 替换反弹 shell
- web fxxkcors: report 页面 admin 访问提交 URL
- changeapi.php 提权改用户 → admin 改自己
- LFSR magic_box 解 2 个文件
- TEA 解密 standard 加密字符串
- 数据流追踪分析代码
key_payload: lfsr(seed2, mask2, n2) gauss mask1
one_liner: SUSCTF 招新题库，ChaMd5 Venom IOT/工控组，涵盖 LFSR/Browser/Web 三类。
lesson: LFSR 已知明文 + 短长度即可用高斯消元解掩码；浏览器 OOB 读写比传统 UAF 更具威力。
quality: medium
---
# SUSCTF WriteUp - ChaMd5 Venom

## 1. Crypto - magic_box LFSR
两个文件，文件名是 base64 时间戳。第一个文件密文头 4 字节 + 已知明文 "Date"，枚举 lfsr (seed2, mask2) 找出 n2=12 配置；第二个文件已知明文 8 字节用同样方法推断 seed3 范围；最后用 gauss 消元 64x64 矩阵解 mask1；还原生成器 XOR 解密得 SUSCTF flag。

## 2. Browser/JS - 0day 链
`a = RegExp` 注入 `su32/gu32` prototype 方法；`DataView(0x18)` 三个实例构造重叠 ArrayBuffer；`delete a3; delete a2; delete b` 触发 OOB；`a5.setUint8(0x20, 0xb8)` 改 size；最后 `a4.setUint32(0x98, libc+...)` 触发任意写改 vtable。

## 3. Web - fxxkcors
report 页面是 admin 访问你提交的 URL；changeapi.php 修改权限需要 admin。HTML 页面 form 表单提交 → admin 自动访问 → 修改 cookie 改自己为 admin。

## 4. Misc - 维吉尼亚
直接打开是乱码编码问题；vim 打开正常；最后几个字符像维吉尼亚密文，找无密钥揭秘工具解。

## 5. Pwn - heap menu
经典 add/delete/show。`add(-0xa0, 'a')` 整数溢出 malloc size 触发 negative size 绕过；`add(0x68, 'a')` 触发 unsortedbin 残余；之后 `__free_hook = system; delete(0x51) where 0x51 内容为 '/bin/sh'`。

## 招新
ChaMd5 Venom 新成立 IOT+工控+样本分析组，长期招新，admin@chamd5.org。
