---
title: bi0sCTF 2024 Virtio-note (译)
contest: bi0sCTF
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [qemu, virtio, custom-device, oob, kernel, vm-escape]
attack_chain:
  - 解析 QEMU 自定义 virtio 设备源码
  - 识别 virtio_note_handle_req
  - 触发 cpu_physical_memory_read OOB
  - 越界读写宿主机内存
  - 构造 vm escape 链
key_payload: 越界读 / 写 cpu_physical_memory 触发 QEMU 进程 RCE
one_liner: bi0sCTF 2024 高质量 Pwn 题，QEMU 自定义 virtio-note 设备 + 越界读写实现 VM Escape。
lesson: 客制化 QEMU 设备的攻击面在 virtio backend (handle_req / handle_output) + cpu_physical_memory_* 不带范围检查。
quality: high
---

bi0sCTF 2024 QEMU 客制化设备 + 虚拟机逃逸题。题面给一份带 virtio-note 设备的
QEMU 源码 + 客户机 client 程序。virtio-note 是一个简化版 virtio 块设备，
读写两个 handle 函数直接调 cpu_physical_memory_read / cpu_physical_memory_write
做 DMA 拷贝。

漏洞：virtio_note_handle_req 接收请求时未校验 req->offset + req->len 是否
超出 DMA 区域，且 offset 字段类型为 uint32_t，size 由请求方控制。客户机
可以构造 offset=0xffffffff - small_value 的越界 offset，再加一个巨大 len，
让 QEMU 进程自身堆/栈上被读写。

攻击链：
1. 逆向 QEMU 源码，定位 virtio_note_handle_req
2. 写 client 程序触发 OOB read 泄 QEMU 进程基址
3. 写 client 程序触发 OOB write 写 got 表 / 函数指针
4. 跳到 system("/bin/sh") 弹宿主机 shell

作者是 bi0s 战队原班人马(印度顶尖战队)，WP 译后质量极高，QEMU 内部
virtio-pci / virtio-mmio 注册流程 + DMA 翻译 + 中断注入机制都讲到位。
