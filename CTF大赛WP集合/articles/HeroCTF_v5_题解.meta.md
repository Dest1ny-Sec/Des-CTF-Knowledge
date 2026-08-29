---
title: HeroCTF v5 题解
contest: HeroCTF
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [Solidity, GraphQL, JWT, SSTI, pwn, 招新]
attack_chain: |
  1. Solidity decompile 出 5 个函数 0x3c5269d8/0x459a2790/0x75ec067a/0xe9a37061/win
  2. GraphQL mutation increaseClickSchool 批量请求绕过
  3. nginx referer 校验 + JWT HS256 弱密钥爆破 hashcat -a 0 -m 16500
  4. Flask SSTI {{config.update(a=config.update).__globals__...os.popen}}
  5. Pwn 负索引 -13 越界写 GOT 触发 l33t() Hero{Unch3ck3d_n3g4t1v3_1nd3x_1nt0_G0T_0v3wr1t3_g03s_brrrrrr}
key_payload: |
  Hero{Unch3ck3d_n3g4t1v3_1nd3x_1nt0_G0T_0v3wr1t3_g03s_brrrrrr}
one_liner: 狼组安全社区把 v5 多道题 payload 拼成一篇水文 + 公众号引流。
lesson: 单题笔记凑成的"题解合集"价值有限；Solidity 0.8.17 decompile + Flask SSTI 属性链 + GOT 负索引是高频考点。
quality: low
---

# HeroCTF v5 题解

> 来源: ctfiot.com 115399 - 狼组安全社区公众号文章

## 题型拆解

文章是几道 v5 题目的代码片段合集，每题只有 payload 没有完整过程：

- **Solidity 合约 decompile**：`hero2303` UNDVTOK/UDK token 有 buy/sell/transfer + Attack 合约用 `selfdestruct(target)` 强送 ETH
- **GraphQL 批量查询**：`mutation { increaseClickSchool(schoolName: "Flag CyberSecurity School"){schoolId, nbClick} }` 数组提交
- **Referer 白名单绕过**：nginx `if ($http_referer !~* "^https://admin.internal.com") return 403`；Node 后端 `req.header("referer") === "YOU_SHOUD_NOT_PASS!"` 双 Referer 头
- **JWT HS256 弱密钥**：`hashcat -a 0 -m 16500 jwt.secrets.list` 爆破出 `role: guest` 的 key
- **Flask SSTI**：`{{config.update(a=config.update)}}` → `{{config.a(b=lipsum.__globals__)}}` → `__builtins__.__import__('os').popen('cat f*t').read()`
- **Pwn 负索引**：`sla("Enter the index of this appointment (0-7):",-13)` 写入 GOT
- **VBS 木马 / Office 宏 / cv2 拼图** / **AES XOR key 还原** flag：`Hero{hyp3r_l00p!1}`

## 评价

典型狼组公众号水文：堆 payload、堆代码块、堆公众号二维码，正文是几段碎片的拼贴。没有完整复现链路、没有调试过程，只有"答案+核心代码"。

适合作为速查 cheat sheet 看，但当作学习材料价值不高。
