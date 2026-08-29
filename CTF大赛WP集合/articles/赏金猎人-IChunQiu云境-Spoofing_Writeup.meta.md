---
title: 赏金猎人:IChunQiu云境-Spoofing Writeup
contest: IChunQiu云境-Spoofing
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [GhostCat, CNVD-2020-10487, Tomcat-AJP, MS17-010, WebClient-Coerce, PetitPotam, NTLM-relay, RBCD, noPac, AD-pentest, BloodHound]
attack_chain:
- Nmap发现8009 AJP端口,Tomcat 9.0.30,使用GhostCat (CNVD-2020-10487) 读/web-inf/web.xml
- 字典爆破servlet路径找到uploadservlet,上传temp.txt
- ajpShooter替换./upload为/upload,读上传文件
- 上传JSP shell,执行ssh-rsa公钥注入/root/.ssh/authorized_keys
- chomod 600 + SSH flag01
- 入口Ubuntu 172.22.11.76,挂代理扫445发现3台主机
- XR-Desktop 172.22.11.45 (Windows7) MS17-010利用+提权
- 本地凭据:Administrator/John,域凭据:yangmei
- 不能直接拿域控(xiaorang-dc 172.22.11.6):MAQ=0无法addcomputer,无LDAPS
- 域内有nopac但对XR-Desktop无WriteDacl无法改SamAccountName
- 无CVE-2019-1040,改用PetitPotam + WebClient NTLM中继
- 目标:XR-LCM3AE8B 172.22.11.26 (开启WebClient)
- socat+SSH反向端口转发让80监听0.0.0.0
- ntlmrelayx -t ldap://DC --escalate-user 'xr-desktop$' --delegate-access
- PetitPotam触发XR-LCM3AE8B认证→RBCD攻击
- 申请XR-LCM3AE8B CIFS银票+psexec拿flag03
- mimikatz获取zhanghui 1232126b24cdf8c9bd2f788a9d7c7ed1 (MA_Admin组)
- zhanghui + nopac create-child申请CIFS票据登录DC
- flag04+域管administrator 0fadb57f5ec71437d1b03eea2cda70b9
key_payload: CNVD-2020-10487 + PetitPotam + RBCD + nopac
one_liner: IChunQiu云境Spoofing赏金猎人WP,Tomcat GhostCat读web.xml+MS17-010内网打域+PetitPotam+WebClient NTLM中继+RBCD攻击+nopac域提权,完整内网渗透链。
lesson: Tomcat AJP GhostCat (CNVD-2020-10487) 是稳定的web入口;PetitPotam+WebClient+NTLM中继是AD域渗透的稳定攻击链;RBCD + nopac是2022-2024 AD提权标配;BloodHound采集需注意CreateChild等ACL。
quality: high
---

## 题目列表

IChunQiu云境Spoofing 1000元一血,完整内网渗透链

## 关键考点

### 1. 信息收集 + GhostCat
- Nmap发现8009 AJP端口(对应Tomcat tag)
- 目录扫描发现Tomcat 9.0.30
- GhostCat (CNVD-2020-10487) 读/web-inf/web.xml
- 字典爆破servlet路径找到uploadservlet
- 上传temp.txt + ajpShooter替换./upload为/read

### 2. JSP Webshell
- 上传shell.txt:JSP执行Runtime.getRuntime().exec(base64 bash反弹)
- SSH公钥注入:/root/.ssh/authorized_keys
- chmod 600 + SSH flag01

### 3. 内网渗透 - Ubuntu 172.22.11.76
- SSH连入开代理
- 扫445发现3台主机:
  - 172.22.11.45 XR-Desktop.xiaorang.lab (Windows7)
  - 172.22.11.6 xiaorang-dc.xiaorang.lab (DC)
  - 172.22.11.26 XR-LCM3AE8B.xiaorang.lab

### 4. MS17-010 + 凭据
- XR-Desktop 172.22.11.45 MS17-010一气呵成
- 凭据:
  - Administrator 4430c690b4c1ab3f4fe4f8ac0410de4a
  - John 03cae082068e8d55ea307b75581a8859
  - XR-DESKTOP$ 3aa5c26b39a226ab2517d9c57ef07e3e
  - yangmei 25e42ef4cc0ab6a8ff9e3edbbda91841 - xrihGHgoNZQ

### 5. 域控分析(不能直接拿下)
- MAQ=0,无法addcomputer (samr+ldaps都受MAQ限制)
- 域内有nopac但对XR-Desktop无WriteDacl,无法改SamAccountName
- 无CVE-2019-1040,改用PetitPotam
- WebClient扫描确定可拿XR-LCM3AE8B 172.22.11.26

### 6. PetitPotam + WebClient + NTLM中继
- socat + SSH反向端口转发让80监听0.0.0.0
- `ntlmrelayx.py -t ldap://172.22.11.6 --no-dump --no-da --no-acl --escalate-user 'xr-desktop$' --delegate-access`
- PetitPotam触发XR-LCM3AE8B认证到ubuntu
- 完成RBCD攻击
- 申请XR-LCM3AE8B CIFS银票

### 7. psexec + nopac create-child
- psexec登录XR-LCM3AE8B拿flag03
- mimikatz获取zhanghui 1232126b24cdf8c9bd2f788a9d7c7ed1 (MA_Admin组)
- BloodHound看不到CreateChild(未采集)
- AdFind.exe -b "CN=Computers,DC=xiaorang,DC=lab" nTSecurityDescriptor -sddl+++
- nopac + create-child参数申请CIFS票据登录DC
- flag04 + 域管administrator 0fadb57f5ec71437d1b03eea2cda70b9

## 实战价值
- Tomcat AJP GhostCat (CNVD-2020-10487) 是稳定的web入口
- PetitPotam + WebClient + NTLM中继是AD域渗透的稳定攻击链
- RBCD(Resource-Based Constrained Delegation) + nopac是2022-2024 AD提权标配
- BloodHound采集需注意CreateChild等ACL
- socat+SSH反向端口转发是跨网络监听的常用技巧
