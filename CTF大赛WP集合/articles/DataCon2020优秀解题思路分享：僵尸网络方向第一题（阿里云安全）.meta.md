---
title: DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）
contest: DataCon 2020
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags: [botnet, honeypot, http-log, sql, ld_preload, xgoahead, cgi, malware]
attack_chain:
  - 黑名单正则过滤honeypot_http_log
  - 长度>=32的URL
  - 发现LD_PRELOAD=/proc/self/fd/0 + ELF头post data
  - xgoahead web服务器+admin/login.cgi
  - filename=2.elf+Content-Disposition
  - sub_5C4解密: chr(ord(c)-98)
  - MD5 4个ELF文件
  - passive_dns查exec.kfckiller.cc等C2域名
key_payload: sub_5C4(c) = chr(ord(c) - 98)  # 字符减98
one_liner: DataCon2020僵尸网络分析：蜜罐HTTP日志+LD_PRELOAD ELF+xgoahead
lesson: 蜜罐日志过滤用长URL+LD_PRELOAD+ELF头识别攻击payload
quality: high
---

# DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）

## 题目信息
- 比赛：DataCon 2020（阿里云安全）
- 方向：僵尸网络分析
- 工具：SQL 查询 + 蜜罐日志分析

## 关键攻击链
### 1. 蜜罐 HTTP 日志过滤
```sql
-- 黑名单正则
"echo >NiGGeR|Account\\.User1\\.Password>\\$\\(|shell_exec\\(|busybox.*?wget.*?\\./|invokefunction&function=call_user_func_array|content=|/language/Swedish\\${IFS\\}|/model/__show_info\\.php\\?REQUIRE_FILE=|wget( |\\+)|/shellinvoker/shellinvoker\\.jsp|/invoker/JMXInvokerServlet|/jbossass/jbossass\\.jsp|certutil\\.exe|\\\\think\\\\template\\\\driver\\\\file/write&cacheFile|<\\?php|FxCodeShell\\.jsp|<%@|shell\\.jsp|java\\.lang\\.System|"
-- 白名单
"CHANGELOG\\.txt|snapshot\\.cgi"
-- 长度>=32
and LENGTH(url) >= 32
group by url order by cn desc
```

### 2. 关键攻击载荷
- `cgi-bin/cgitest?LD_PRELOAD=/proc/self/fd/0` + POST data `\x7fELF\x02\x01\x01...`
- xgoahead web 服务器，`admin/login.cgi` 接受文件上传
- `filename=2.elf` + `name="%4cD%5f%50%52E%4c%4f%41D"`（unicode 编码字段名）

### 3. ELF 解密
```python
g_enc_table_1 = "\xC5\xC6\x82..."
g_enc_table_2 = "\xAE\xA6..."
def sub_5C4(input_str):
    return ''.join(chr(ord(c) - 98) for c in input_str)
```

### 4. 关联分析
- ELF 文件 MD5 4 个
- `passive_dns_data` 表查 `exec.kfckiller.cc` / `exec.dtdtdt.info` / `control.dtdtdt.info`
- C2 服务器：`http://exec.dtdtdt.info/d.sh`

## 评分
- quality: high（蜜罐日志 SQL 过滤 + 字符减 98 解密 + 关联 DNS 查询）
