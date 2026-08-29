---
title: Realworld CTF - Black Box Writeup (CVE-2020-14364 QEMU USB 逃逸)
contest: Realworld CTF
year: 2021
difficulty: high
vuln_type: pwn_unknown
tags: [qemu-escape, usb-uhci, cve-2020-14364, vm-escape, setup_len-overflow, do_token_setup, s-setup_buf, data_buf-overflow]
attack_chain:
  - QEMU 5.15.0 + x86_64 + softmmu + usb-tablet + uhci 驱动
  - CVE-2020-14364: usb_process_one → do_token_setup → s->setup_len 校验不足
  - do_token_setup: s->setup_len = (s->setup_buf[7]<<8)|s->setup_buf[6] 用户可控
  - do_token_in: len = s->setup_len - s->setup_index, 多次 IN 累加 setup_index
  - 越界读写: data_buf[0x1000] + setup_index 可控 越界 USBDevice 结构
  - s->setup_index 设为 -8 越界改 s->setup_buf[0] USB_DIR_IN
  - 越界写 setup_index 控制 USBDevice.setup_state
  - UHCI 协议: Frame List + QH + TD (Token Descriptor)
  - UHCI_TD link/ctrl/token/buffer 32 字节
  - Vf=depth first / Q=TD or QH / T=last
  - max_len = ((td->token >> 21) + 1) & 0x7ff
  - uhci_handle_td 设置 p->iov.size = max_len
  - step1: 正常 token_setup 设置 setup_state
  - step2: token_setup size=0x5000 扩大 setup_len 操作范围
  - step3: token_out 越界写 setup_index=-8
  - 改 setup_buf[0] USB_DIR_IN 标记 → do_token_in 越界读
  - 利用 pi (physical address) + virt (virtual address) 双重映射
  - data_buf 0x7fffxxxx 虚拟机地址 / device 0x5ff55xxx 物理机虚拟地址
  - g_malloc0 分配 QH/TD buffer + UHCI port 写入 s->fl_base_addr
  - uhci_port_write 0x10/0x12 端口自定义 frame_list_base
  - timer_mod_ns 触发 uhci_frame_timer → uhci_process_frame
  - 完整利用: 覆盖 timer_list + 时钟伪造 → 任意地址写 + system
key_payload: do_token_setup(size=0x5000) + do_token_out(offset=-8) 改 setup_index + do_token_in(OOB read) 泄物理地址
one_liner: Realworld CTF 之 Black Box：CVE-2020-14364 QEMU 5.15 USB UHCI 驱动 do_token_setup setup_len 用户可控 → data_buf 越界读写 → 改 UHCI frame_list 任意地址写 → 时钟劫持 → QEMU host RCE。
lesson: USB UHCI 协议复杂但 do_token_setup 中的 setup_len 赋值后检测是经典漏洞；data_buf 越界读写 + setup_index 整数下溢是 USB 设备逃逸经典攻击面；QEMU VM 逃逸需结合 virt+phys 双地址空间分析。
quality: high
---
