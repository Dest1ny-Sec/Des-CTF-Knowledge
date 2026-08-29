---
title: 第二届陇剑杯决赛Misc-Win
contest: 陇剑杯决赛
year: 2023
difficulty: medium
vuln_type: forensic_disk
tags: [陇剑杯,Vmware加密,VMX加密,rockyou爆破,Xshell密码,Reg注册表,启动脚本]
attack_chain: 1. VMX加密: 识别encryption.keySafe=vmware:key/list/(pair/...)→pyvmx-cracker.py+rockyou.txt爆破→密码somewhere|2. Xshell会话: NetSarang Computer\7\Xshell\Sessions找.xsh文件→XShellCryptoHelper.py -d -user testtt -sid SID→密码123456a|3. 启动脚本: 注册表HKEY_CURRENT_USER\Environment + Startup目录C:\Users\testtt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup|4. 访问次数: 内存或日志检索www.baidu.com共10次
key_payload: pyvmx-cracker.py -v VMX.vmx -d rockyou.txt|encryption.keySafe = vmware:key/list/(pair/(phrase/...))|XShellCryptoHelper.py -d -user testtt -sid S-1-5-21-1844938145-4200775270-4174914976-1000 p5orZNxx2PcH/dp8h0/0nr+yyIooYMX/TOPZSiHvt2VmrQ+Sya1X|somewhere|123456a|C:\Users\testtt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup|10
one_liner: 陇剑杯决赛win场景4问:VMX加密pyvmx-cracker+rockyou爆破somewhere+Xshell 7 NetSarang Computer\7\Xshell\Sessions反序列化AES密码123456a+启动脚本注册表Environment+Startup目录+访问www.baidu.com 10次
lesson: 1) VMware加密VMX文件结构:encryption.keySafe=vmware:key/list/(pair/(phrase/PBKDF2-HMAC-SHA-1/AES-256/rounds=10000/salt=...)); 2) pyvmx-cracker.py是标准VMX密码爆破工具,搭配rockyou.txt字典; 3) Xshell 7会话存储路径C:\Users\<user>\Documents\NetSarang Computer\7\Xshell\Sessions\,XShellCryptoHelper.py解密SID+cipher; 4) 启动脚本两处:注册表HKCU\Environment(用户环境变量)和Startup目录(开始菜单启动项); 5) 日志/内存检索URL计数可用grep
quality: high
---

## 备注

原文(https://www.ctfiot.com/136503.html)2023年9月16日第二届陇剑杯决赛,4个flag题。

### 题目详情

**@Name: win @Game: 2023 第二届陇剑杯决赛 @Time: 2023/9/16 @Type: Misc**

**@Description:**
1. 小明在一台电脑中获取了一个虚拟机文件以及桌面上存有 rockyou.txt,打开虚拟机的密码是多少?
2. xshell 连接的密码是多少?
3. 登陆脚本启动的程序路径是什么?
4. 共访问了几次 www.baidu.com?

**@Flag:**
1. somewhere
2. 123456a
3. C:\Users\testtt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
4. 10

### 详解

**1) VMX密码爆破**
- Windows 7 x64.vmdk / .vmsd / .vmx / .vmxf
- 正常.vmsd是空白的,加密后增加密钥到encryption.keySafe
- 加密VMX结构:
  ```
  encryption.keySafe = "vmware:key/list/(pair/(phrase/tAEghLS8980%3d/pass2key%3dPBKDF2-HMAC-SHA-1%3acipher%3dAES-256%3arounds%3d10000%3asalt%3dy2uTjk2sa7ri9phabetHQA%253d%253d,HMAC-SHA-1,qipjap5UguTA5Evy1dipkNaW4xEtjoc9dkjcLKCXxOY1AK8GBi25tkYmApN98B6LuusWn%2b3hSLgJacDobycflOpwa%2bmw3xt%2fvnVT47asYLDXExOtjEiB6%2bGhU32CXMiD8bwkSp5f4IiKC62i2pn1BYgRRws%3d))"
  encryption.data = "Oo3FlZJquP2Km+9s..."
  ```
- URL解码后:phrase=tAEghLS8980=,pass2key=PBKDF2-HMAC-SHA-1,cipher=AES-256,rounds=10000,salt=y2uTjk2sa7ri9phabetHQA==
- 工具:`python3 pyvmx-cracker.py -v VMX.vmx -d rockyou.txt`
- 答案:`somewhere`

**2) Xshell密码**
- 7版本路径:`C:\Users\%username%\Documents\NetSarang Computer\7\Xshell\Sessions\`
- 6版本路径:`C:\Users\%username%\Documents\NetSarang Computer\6\Xshell\Sessions\`
- 当前用户testtt:SID=S-1-5-21-1844938145-4200775270-4174914976-1000
- 工具:`python XShellCryptoHelper.py -d -user testtt -sid SID cipher_base64`
- 答案:`123456a`

**3) 启动脚本路径**
- 启动目录:`C:\Users\testtt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
- 注册表:`HKEY_CURRENT_USER\Environment`(用户环境变量,登录时执行)

**4) 访问www.baidu.com次数**
- 答案:10

## 评级

- **quality: high** — 4题全部答出+详细路径+pyvmx-cracker/XShellCryptoHelper工具链,考VMware加密VMX+Xshell密码+启动脚本+日志统计,完整应急响应取证流程
- **vuln_type: forensic_disk** — 主机取证(VMDK/VMX+注册表+会话文件)
- 实战价值:Vmware Workstation/Player加密VM的密码恢复是CTF与实战高频考点
