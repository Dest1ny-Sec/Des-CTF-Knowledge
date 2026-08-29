---
title: SHCTF-2024-Week2 官方WP
contest: SHCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [shctf2024-week2, jwt-cracker, python-pickle, mersenne-twister, hash-length-extension, flask-session-forge]
attack_chain:
- 从两端向中间搜索 pxorq 重建 p/q 二进制
- QRazyBox 修复受损二维码 + Reed-Solomon 解码
- 自定义 base64 字母表 (ABCDjp0yIJKL...2345678Y+/) 解密
- jwt-cracker 6 位弱口令爆破 HS256 密钥 222333
- 改 jwt payload role: user → admin
- pickle find_class() 黑名单绕过 posix.system
- random.seed(1000000-9999999) 爆破 seed 预测 next
- 自实现 MD5 长度扩展攻击 + SECRET_KEY=Th1s_is_5ecr3t_k3y 伪造 session
- flask-session-cookie-manager 伪造 is_admin: 1
- union select secretdata from ctf.flag SQL 注入
- seccomp 59 号 + open/read/write 链式 sys_open
- 0xBB / 0x97 字节溢出一字节改 ret_addr
- picoGadget 工具链泄露 libc → ret2libc
- 0x100 字节异或 shellcode
key_payload: -1") union select 1,scretdata from ctf.flag
one_liner: 看雪 ctfiot 招新 Week2 完整 WP，涵盖 Crypto/JWT/Pickle/Flask/Pwn/Reverse 多类基础题。
lesson: 当 pickle 显式 import 黑名单时，要想到 posix.system 这类「带前缀的等价模块」常被遗忘在黑名单。
quality: medium
---
# SHCTF-2024-Week2 官方 WP（ctfiot 210419）

## Crypto
- **worde 很大**：dp 泄露 e 较大，从两端向中间搜索 pxorq 重建 p/q 二进制（满足「低 k 位乘积等于 n 低 k 位」+ 端位扩展）
- **受损二维码**：QRazyBox 修复 + Reed-Solomon 解码得 `F1agf4K3rF1agf4K3r` → 自定义 base64 字母表 → THis_F14GTHis_F14G

## Web
- **登录验证**：jwt-cracker 6 位弱口令 → 密钥 222333 → 改 role: admin → SHCTF{y0u_v3r1F1ed_Y0U_aRe_yOU_...}
- **dickle**：黑名单有 `os.system`，但 pickle `find_class` 会查 `posix.system`（未在黑名单）→ 反弹 shell
- **guess_the_number**：伪随机数爆破 seed 1e6-9e6，预测 second_num
- **MD5 GOD!**：自实现 MD5 长度扩展攻击 64 用户签到，SECRET_KEY=Th1s_is_5ecr3t_k3y 伪造 flask session
- **入侵者禁入**：flask-session-cookie-manager encode `is_admin: 1` + role.flag 字段 → lipsum SSTI
- **自助查询**：`")` 闭合 SQL 注入 `-1") union select 1,scretdata from ctf.flag`

## Pwn
- **ezorw**：No canary + PIE；fd=0 close + open("/flag") + puts 输出
- **week1 复刻**：shellcraft.sh() 末尾去 0x0f05 → 写入栈 → 跳到栈执行
- **easy_canary**：格式化字符串写低 1 字节爆破 canary
- **largebox**：house of spirit + setcontext 控制 rsp/rip
- **no_canary_one_shot**：pop rdi + ret2libc
- **mellon**：tcache stash unlink
- **old_fashion**：off-by-null 改 chunk size
- **shellcode_x64**：手写 0x60 字节 push/pop shellcode
- **shellcode_x86**：32 位同款
- **shellcode_arm64**：AArch64 Linux shellcode
- **shellcode_riscv64**：RISC-V shellcode
- **lockbox2**：seccomp 59 + open/read/write + stack pivot
- **mimic_stack**：栈帧混淆 re-imitate 真实 ret
- **fmt_64**：非栈 fmt-string + 写 GOT
