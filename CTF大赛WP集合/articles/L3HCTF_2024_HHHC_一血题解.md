# L3HCTF 2024 HHHC 一血题解

> 原文: https://www.ctfiot.com/161467.html
> ID: 161467

周末看到学弟消息，有一道路由器相关的题。笔者是运维方向，在公司负责网络安全竞赛运维，对网络设备比较熟悉，于是花了点时间研究了下。

注意：题目是 Reverse 分类的，笔者做法属于非预期，预期解法可以从官方 Writeup 中学习（做题时并不知道这题是 Reverse 分类，以为是 Misc）。

题目描述

Remember the "hillst0ne" challenge in L3HCTF2021?L3HSec also has an MSR3610 router deployed since 2021. Now we have decided to upgrade to a newer model, but we couldn't find the PPPoE password. Could you locate it in the existing configuration?

解题流程

[L3HSEC-ROUTER-1]show current-configuration
# version 7.1.064, Release 0821P16
# sysname L3HSEC-ROUTER-1#wlan global-configuration
# security-zone intra-zone default permit
# dhcp enable dhcp server always-broadcast
# dns proxy enable
# system-working-mode standard password-recovery enable#vlan 1#dhcp server ip-pool lan1 gateway-list 192.168.0.1 network 192.168.0.0 mask 255.255.254.0 address range 192.168.1.2 192.168.1.254 dns-list 192.168.0.1#controller Cellular0/0#interface Dialer0 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg== ppp chap user hustpppoe114514 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ== dialer bundle enable dialer-group 2 dialer timer idle 0 dialer timer autodial 5 ip address ppp-negotiate nat outbound#interface NULL0#interface GigabitEthernet0/0 port link-mode route description LAN-interface ip address 192.168.0.1 255.255.254.0 tcp mss 1280#interface GigabitEthernet0/1 port link-mode route#interface GigabitEthernet0/1.3647 vlan-type dot1q vid 3647 pppoe-client dial-bundle-number 0#interface GigabitEthernet0/2 port link-mode route combo enable copper#interface GigabitEthernet0/3 port link-mode route combo enable copper#interface GigabitEthernet0/4 port link-mode route#interface GigabitEthernet0/5 port link-mode route
# scheduler logfile size 16#line class console user-role network-admin#line class tty user-role network-operator#line class vty user-role network-operator#line con 0 user-role network-admin#line vty 0 63 authentication-mode scheme user-role network-operator#performance-management
# password-control enable undo password-control aging enable undo password-control history enable password-control length 6 password-control login-attempt 3 exceed lock-time 10 password-control update-interval 0 password-control login idle-time 0#domain system
# domain default enable system#role name level-0 description Predefined level-0 role#role name level-1 description Predefined level-1 role#role name level-2 description Predefined level-2 role#role name level-3 description Predefined level-3 role#role name level-4 description Predefined level-4 role#role name level-5 description Predefined level-5 role#role name level-6 description Predefined level-6 role#role name level-7 description Predefined level-7 role#role name level-8 description Predefined level-8 role#role name level-9 description Predefined level-9 role#role name level-10 description Predefined level-10 role#role name level-11 description Predefined level-11 role#role name level-12 description Predefined level-12 role#role name level-13 description Predefined level-13 role#role name level-14 description Predefined level-14 role#user-group system#local-user admin class manage service-type telnet http authorization-attribute user-role network-admin
# ip http enable web new-style#wlan ap-group default-group vlan 1#return[L3HSEC-ROUTER-1]

interface Dialer0 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg== ppp chap user hustpppoe114514 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ==

可以看到这里大致是使用用户名为 hustpppoe114514，密码密文为

$c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg==。

后面还有一个 pap 的信息，用户名相同，密码密文为

$c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ==。

猜测是哈希存储，但是 cmd5 等解密站点不能识别。

后面搜到 GitHub 上有一个上古的工具 https://github.com/grutz/h3c-pt-tools/blob/master/hh3c_cipher.py#L285-L310。

其中有早期版本的解密，并且使用了固定的 DES 密钥。

也就是实际上存储的信息并不是哈希，应当是能够被解密的密文。

参考官方的操作手册 https://www.h3c.com/en/Support/Resource_Center/EN/Home/Routers/00-Public/Configure___Deploy/Configuration_Guides/MSR610[810][830][1000S][2600][3600]-R6728/05/202209/1696112_294551_0.htm，发现一句 For security purposes, the password specified in plaintext form and ciphertext form will be stored in encrypted form，证实了是以可逆的密文形式存储而非哈希。

那么接下来有两个方向可以尝试：

1，获取固件去分析解密过程（预期）

2，在运行时解密后抓到明文（非预期）

笔者选择了后者。

一开始想直接使用单台设备导入配置然后发送 PPPoE 认证请求，但是手头恰好没有 H3C 设备。

想起来不管是华为还是思科都有模拟器，H3C 应当也有，在官网找到了模拟器的下载页面。

https://www.h3c.com/cn/Service/Document_Software/Software_Download/Other_Product/H3C_Cloud_Lab/Catalog/HCL/

得到了一个看起来挺现代化 UI 的 H3C 模拟器。

我们不用关心其他配置，直接导入需要的 Dialer0，也就是直接复制下面这段导入。

interface Dialer0 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg== ppp chap user hustpppoe114514 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ== dialer bundle enable dialer-group 2 dialer timer idle 0 dialer timer autodial 5 ip address ppp-negotiate nat outbound

通过查询命令 show current-configuration interface Dialer0，可以看到已经导入了与题目相同的配置了。

通过官方操作手册可以看到需要在接口里绑定这个 PPPoE 拨号才算启用，但是前面没有接线导致没有接口启用。

我们重新画一下拓扑。

可以看到新的拓扑中接口 GE0/0 是启用的状态。

我们在二号路由器上重复前面的操作导入 Dialer0 的配置，并绑定 GE0/0 作为拨号接口。

给 GE0/0 启用 pppoe-server 并绑定 VT1。

可以看到抓包内容已经出现了下一步的包。

但是我们想要的认证账户信息仍然没有获取到。

是哪里出了问题？

通过查阅资料发现，Dialer0 中的认证有 CHAP 和 PAP 两种方式

The main difference between PAP and CHAP is that PAP uses a Two-Way Handshake and sends the password in clear-text form, whereas CHAP uses a Three-Way Handshake and never sends the password between the parties. As a result, CHAP is much more secure than PAP.PAP, or password authentication protocol, is a point-to-point protocol (PPP) authentication method that uses passwords to validate users. It is an internet standard (RFC 1334), password-based authentication protocol. Using PAP, data is not encrypted. It is sent to the authentication server as plain text

总结

如出题人的 Flag 所说，PPPoE 是需要保存明文密码认证用。

而 CHAP 和 PAP 中，PAP 是明文传输认证信息，CHAP 相对安全一些不会使用明文传输。

后记

公司荣誉

2021年 CVVD首届车联网漏洞挖掘赛二等奖

2021年 第二届“祥云杯”网络安全大赛总决赛三等奖

2021年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖

2021年 浙江省信息通信行业网络安全技能竞赛团体竞赛一等奖

2021年 智能网联汽车安全测评技能大赛智能网联汽车破解悬赏赛三等奖

2022年 首届中国智能网联汽车数据与隐私安全技能大赛最佳数据安全漏洞挖掘奖

2022年 第六届河北师范大学信息安全挑战赛暨HECTF2022优秀技术支持单位

2022年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖

2022年 浙江省信息通信行业网络安全技能竞赛团体竞赛一等奖

2022年 中国工业互联网安全大赛（浙江省选拔赛）团体竞赛三等奖

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛冠军（特等奖）

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛广义功能安全奖

2023年 “凌武杯”杭州未来科技城网络与信息安全管理员职业技能竞赛优秀承办单位

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）个人赛冠军

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）团队赛二等奖

2023年 浙江省工业互联网安全竞赛三等奖

2023年 “梦想·中移杯”杭州未来科技城软件系统测试职业技能大赛二等奖

2023年 软件供应链安全竞赛优秀支撑单位

2023年 第七届河北师范大学信息安全挑战赛暨HECTF2023优秀技术支持单位

2023年 第四届电信和互联网行业职业技能竞赛个人赛二等奖

2023年 全国网络与信息安全管理员职工职业技能竞赛一等奖

2023年 “补天杯”破解大赛亚军

2023年 首届“强基杯”数据安全技能竞赛数据安全实战赛道全国二等奖

2023年 首届“强基杯”数据安全技能竞赛复赛华东赛区数据安全实战赛道团队三等奖

2023年 全国行业职业技能竞赛–第二届全国数据安全职业技能竞赛总决赛一等奖

杭州凌武科技有限公司是一家专注于网络安全的新兴企业，自主研发了竞赛平台、实训平台、文件追踪平台、攻防演练平台、钓鱼演练平台等多款安全产品，提供专业的渗透测试、漏洞挖掘、安全培训、竞赛支撑等服务，对车联网安全、物联网安全、工控安全等新方向有深入的研究，致力于成为客户信赖的安全伙伴。如果您有以上相关业务的需求，欢迎随时联系我们。

关注我们

联系我们


```
Remember the "hillst0ne" challenge in L3HCTF2021?L3HSec also has an MSR3610 router deployed since 2021. Now we have decided to upgrade to a newer model, but we couldn't find the PPPoE password. Could you locate it in the existing configuration?
[L3HSEC-ROUTER-1]show current-configuration
# version 7.1.064, Release 0821P16
# sysname L3HSEC-ROUTER-1#wlan global-configuration
# security-zone intra-zone default permit
# dhcp enable dhcp server always-broadcast
# dns proxy enable
# system-working-mode standard password-recovery enable#vlan 1#dhcp server ip-pool lan1 gateway-list 192.168.0.1 network 192.168.0.0 mask 255.255.254.0 address range 192.168.1.2 192.168.1.254 dns-list 192.168.0.1#controller Cellular0/0#interface Dialer0 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg== ppp chap user hustpppoe114514 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ== dialer bundle enable dialer-group 2 dialer timer idle 0 dialer timer autodial 5 ip address ppp-negotiate nat outbound#interface NULL0#interface GigabitEthernet0/0 port link-mode route description LAN-interface ip address 192.168.0.1 255.255.254.0 tcp mss 1280#interface GigabitEthernet0/1 port link-mode route#interface GigabitEthernet0/1.3647 vlan-type dot1q vid 3647 pppoe-client dial-bundle-number 0#interface GigabitEthernet0/2 port link-mode route combo enable copper#interface GigabitEthernet0/3 port link-mode route combo enable copper#interface GigabitEthernet0/4 port link-mode route#interface GigabitEthernet0/5 port link-mode route
# scheduler logfile size 16#line class console user-role network-admin#line class tty user-role network-operator#line class vty user-role network-operator#line con 0 user-role network-admin#line vty 0 63 authentication-mode scheme user-role network-operator#performance-management
# password-control enable undo password-control aging enable undo password-control history enable password-control length 6 password-control login-attempt 3 exceed lock-time 10 password-control update-interval 0 password-control login idle-time 0#domain system
# domain default enable system#role name level-0 description Predefined level-0 role#role name level-1 description Predefined level-1 role#role name level-2 description Predefined level-2 role#role name level-3 description Predefined level-3 role#role name level-4 description Predefined level-4 role#role name level-5 description Predefined level-5 role#role name level-6 description Predefined level-6 role#role name level-7 description Predefined level-7 role#role name level-8 description Predefined level-8 role#role name level-9 description Predefined level-9 role#role name level-10 description Predefined level-10 role#role name level-11 description Predefined level-11 role#role name level-12 description Predefined level-12 role#role name level-13 description Predefined level-13 role#role name level-14 description Predefined level-14 role#user-group system#local-user admin class manage service-type telnet http authorization-attribute user-role network-admin
# ip http enable web new-style#wlan ap-group default-group vlan 1#return[L3HSEC-ROUTER-1]
interface Dialer0 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg== ppp chap user hustpppoe114514 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ==
interface Dialer0 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg== ppp chap user hustpppoe114514 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ== dialer bundle enable dialer-group 2 dialer timer idle 0 dialer timer autodial 5 ip address ppp-negotiate nat outbound
The main difference between PAP and CHAP is that PAP uses a Two-Way Handshake and sends the password in clear-text form, whereas CHAP uses a Three-Way Handshake and never sends the password between the parties. As a result, CHAP is much more secure than PAP.PAP, or password authentication protocol, is a point-to-point protocol (PPP) authentication method that uses passwords to validate users. It is an internet standard (RFC 1334), password-based authentication protocol. Using PAP, data is not encrypted. It is sent to the authentication server as plain text
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/5-1707194488.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/9-1707194488.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1707194489.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1707194490.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1707194490.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1707194491.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/6-1707194492.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/10-1707194492.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1707194493.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1707194495.png)