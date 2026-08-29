---
title: ByteCTF WriteUp
contest: ByteCTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [clickhouse SSRF, /files..目录穿越, URL()函数, user_01提权, DNS bit 编码, 汉信码, RX-SSTV, bytezoom UAF, dog/cat 类型混淆, free_hook→system, libc-2.31]
attack_chain:
  - Web double sqli: clickhouse SQL, /files.. 目录穿越找 access .sql
  - user_01 权限 > user_2, 用 URL("http://0.0.0.0:8123/?user=user_01&password=...&query=select+flag+from+ctf.flag", CSV)
  - Misc frequently: DNS o.bytedanec.top 0, i.bytedanec.top 1, 8位一组转 ASCII
  - 前半 ByteCTF{^_^enJ0y&y0ur, 后半 UDP 追踪 sse1f_wIth_m1sc^^}
  - HearingNotBelieving: 汉信码 + RX-SSTV, ByteCTF{m4yB3_U_kn0W_S57V}
  - Pwn bytezoom: create cat+dog, select2 dog(0) cat(0) 触发 UAF, create dog(0) 复用 cat(0) 块
  - change_age 改 age 字段 (覆盖 cat.strings 指针) → leak libc
  - 改 tcache_entry → 改 free_hook → system → /bin/sh
key_payload: 'clickhouse URL() / 0.0.0.0:8123 / user_01 password / DNS 0/1 转 8 位 ASCII / 汉信码 + RX-SSTV / dog cat 类型混淆 UAF / change_age 改 cat.strings / free_hook→system'
one_liner: ByteCTF 2022 综合 — clickhouse URL() SSRF 提权 + DNS bit 0/1 转 ASCII + 汉信码/RX-SSTV + bytezoom pwn 狗/猫类型混淆 UAF + change_age 改 strings 指针 + free_hook→system。
lesson: clickhouse URL() 是 SSRF 提权经典;DNS o/i 域名后缀隐写 0/1 bit 是常见 misc trick;类型混淆 + UAF 改指针字段是堆题经典链。
quality: high
---

# ByteCTF WriteUp

## 速读
ByteCTF 综合 4 题 — Web/Misc/Pwn 多方向。

## Web — double sqli
- ClickHouse SQL 注入
- 目录穿越 `/files..` 找 `/var/lib/clickhouse/access/*.sql`
- user_01 密码
- `URL("http://0.0.0.0:8123/?user=user_01&password=...&query=select+flag+from+ctf.flag", CSV)`

## Misc — frequently
- DNS o.bytedanec.top = 0, i.bytedanec.top = 1
- 8 位一组转 ASCII
- 前段: `ByteCTF{^_^enJ0y&y0ur`
- 后段 UDP 追踪: `sse1f_wIth_m1sc^^}`
- flag: `ByteCTF{^_^enJ0y&y0urse1f_wIth_m1sc^_^}`

## Misc — HearingNotBelieving
- 汉信码 (手动还原)
- RX-SSTV (后半段)
- flag: `ByteCTF{m4yB3_U_kn0W_S57V}`

## Pwn — bytezoom
- create cat(0, 18) + dog(0, 18)
- select2 dog(0) + cat(0) → UAF
- create dog(0, 'bbbb') → cat(0) 块被 dog 复用 (类型混淆)
- change_age 改 dog age 覆盖 cat.strings 指针
- show cat(1) 泄 libc_base (高 4 字节 + 低 4 字节)
- 改 tcache_entry → 改 free_hook → system
- create dog(10, p64(system)*4) 写入
- create dog(9, "/bin/sh") 触发 system
