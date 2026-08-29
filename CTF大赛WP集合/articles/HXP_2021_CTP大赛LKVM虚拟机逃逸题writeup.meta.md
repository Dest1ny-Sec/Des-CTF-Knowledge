---
title: HXP 2021 CTP大赛LKVM虚拟机逃逸题writeup
contest: HXP 2021 CTP
year: 2021
difficulty: hard
vuln_type: web_unknown
tags: [pwn, lkvm, kvmtool, virtio, oob-read-write, rop, jop, hypervisor-escape, cve-2021-45464]
attack_chain:
  - 攻击面: virtio-console/net/balloon 0xD2000000-0xD20000FF MMIO
  - 越界读/写：config结构体后0x100字节
  - 信息泄露：bln_dev指针+lkvm基址
  - 控制RIP: exit_lists数组指针覆盖
  - virtio_pci__data_out VIRTIO_PCI_QUEUE_PFN调用init_vq
  - vq=0x16 让bdev->vqs[0x16]指向exit_lists
  - echo c > /proc/sysrq-trigger 触发内核崩溃调用退出处理
  - t->init(kvm) 跳到ROP/JOP链
  - 伪init_item: 0x41填充
  - ret gadget: virtio_net_exec_script
  - 跳到 mov rax,[rbx+0x28]; mov rdi,rbx; ...
  - 最终execl("/bin/sh", "", null) 宿主机shell
key_payload: bdev->vqs[0x16] = exit_lists指针 + echo c > /proc/sysrq-trigger
one_liner: HXP 2021 LKVM虚拟化逃逸：virtio OOB读写+JOP+execl宿主shell
lesson: lkvm exit_lists可被OOB覆盖+内核崩溃触发宿主RCE
quality: high
---

# HXP 2021 CTP大赛LKVM虚拟机逃逸题writeup

## 题目信息
- 比赛：HXP 2021 CTP
- 题目：LKVM 虚拟机逃逸
- 关联：CVE-2021-45464
- 参考：https://www.kalmarunionen.dk/writeups/2021/hxp-2021/lkvm/

## 关键攻击链
### 1. 攻击面
- 宿主机与 VM 内存显式隔离
- 通过 PCI 与宿主机通信
- 模拟 3 个设备：virtio-console、virtio-net、virtio-balloon
- 写 0xD2000000-0xD20000FF 触发 VM 中断
- 控制流 → KVM 驱动 → lkvm 进程

### 2. 信息泄露
- `virtio_pci__data_in` 函数：偏移量映射为 BAR
- 写 0xD2000000+VIRTIO_PCI_QUEUE_NUM 进入 else if 分支
- `config_offset = offset - 20` 无边界检查
- 越界 0x100 字节访问 config 结构体后内存
- 泄露：`bln_dev` 结构体地址 + lkvm 基址
- `/dev/mem` 访问 mmap 区域

### 3. 控制 RIP
- `virtio_pci__specific_data_in` 中 OOB 写
- `init.c` 第 51 行：退出 lkvm 时遍历 `init_item[]`
- 最后一个元素 `t->init(kvm)` 函数指针偏移 0x18
- 写覆盖 `exit_lists` 数组指针

### 4. 触发调用链
- `virtio_pci__data_out` VIRTIO_PCI_QUEUE_PFN case
- `vring_init` `vr->desc = p` 完全控制 VM 物理页面
- `init_vq(bdev, vq)` `bdev->vqs[vq]` 无边界检查
- 设置 vq=0x16 让 `bdev->vqs[0x16]` 指向 exit_lists

### 5. 触发方式
- `echo c > /proc/sysrq-trigger` 触发内核崩溃
- 调用退出处理 → 跳到伪造 init_item
- t->init(kvm) → JOP gadget
- `mov rax, [rbx+0x28]; mov rdi, rbx; mov rsi, [rax+8]; call [rax]`
- 跳到 `virtio_net_exec_script` 中的 ret gadget
- `execl("/bin/sh", "", null)` → 宿主机 shell

## 评分
- quality: high（lkvm 0day 漏洞 + virtio OOB + JOP + CVE-2021-45464）
