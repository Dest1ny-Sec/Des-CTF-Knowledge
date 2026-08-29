---
title: 强网拟态 2024 writeup - Arr3stY0u
contest: 强网拟态 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [srand(0)爆破, libc_read_leak, mprotect, ORW_shellcode, /proc/self/maps泄露, one_gadget, kernel键, packet_socket, modprobe_path, shellcode拼图, 0x18a6断点, XTEA魔改, claripy符号执行, libServ1ce.so, CapooObj__wakeup, Phar反序列化, pickle__reduce__]
attack_chain: Pwn1:cdll.srand(0)+cdll.rand()%100+1爆破 → 栈溢出+libc read leak+pop_rdi+read+libc mprotect RWX+open/read/write /flag shellcode → Pwn2:5次0+i输入+管理员0x6b8b4567登录+读/proc/self/maps+one_gadget+system+bin_sh → Kernel:unshare(CLONE_NEWUSER|NEWNS|NEWNET)+AF_PACKET socket+TPACKET_V3 PACKET_RX_RING+add_key/keyctl_read喷+add 0x21d8000写modprobe_path → Pwn4:6字节shellcode写+pop fs:[rsi]栈+open/read/write /flag → Pwn6:House of Apple 2 _IO_wfile_jumps 0x48+stderr+system → Web:pickle __reduce__反弹shell → PHP CapooObj __wakeup正则banlist过滤(l$1s$IFS/绕)+Phar反序列化 → Android:libServ1ce.so JNI check+inp[i]^keyarray[i])*num+enc_flag + claripy符号执行 → Re:XTEA 0x66轮魔改+add 40+xor 0x7F
key_payload: srand(0)+cdll.rand()%100+1 + AF_PACKET TPACKET_V3 modprobe_path + 6字节shellcode pop fs:[rsi] + l$1s$IFS/ 绕空banlist
one_liner: 强网拟态2024 Arr3stY0u全方向7题:栈溢出ROP+House of Apple 2/内核AF_PACKET modprobe_path/6字节shellcode/Pickle反序列化/CapooObj Phar/Android JNI XTEA。
lesson: srand(0)+rand()%100+1=1..100可爆破验证;AF_PACKET socket+TPACKET_V3 PACKET_RX_RING堆喷+add_key keyring+改modprobe_path经典内核提权;6字节shellcode可用pop fs:[rsi]+syscall;CapooObj正则banlist含" "可用$IFS绕;libServ1ce.so JNI check函数做inp[i]^keyarray[i]*num+enc_flag验证,claripy符号执行求解;XTEA魔改OP=0x66轮+add 40+xor 0x7F。
quality: high
---
