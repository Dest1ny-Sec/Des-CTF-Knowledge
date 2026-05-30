# pem类文件解析及2022蓝帽杯crypto详解

> 原文: https://www.ctfiot.com/49973.html
> ID: 49973

pem文件

pem格式的文件通常用于数字证书认证机构(Certificate Authorities，CA)，其文件形式主要为base64编码的文件，头尾有类似于-----BEGIN PUBLIC KEY-----和-----END PUBLIC KEY-----的头尾标记。

生成公私钥

在python中，可以通过安装包from Crypto.PublicKey import RSA生成想要的公私钥文件

public key

from Crypto.PublicKey import RSA
from Crypto.Util.number import *
p,q = getPrime(512),getPrime(512)
n = p * q
e = 0x10001
pub = RSA.construct((n,e))
with open('out.pem','wb') as f:
    f.write(pub.exportKey('PEM'))
with open('out.pem','rb') as f:
    print(f.read().decode())
'''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuRPouMRTcLWPBEUlhjCrZ6MNQ
rSy29BrHjH4+lGMykB23azPtT9fk7IsEFXoodm6tsPL8kheJ6cP+0WPldlQOw/K3
c9LUGzeCCAhNJuBjUoeW32ruE2HS7RoIF6vkP36zLs167ZZMK7Fg0cqW6VNXoJHT
zaKdqysBe+3W1VHl6QIDAQAB
-----END PUBLIC KEY-----
'''

private key

from Crypto.PublicKey import RSA
from Crypto.Util.number import *
p,q = getPrime(512),getPrime(512)
n = p * q
e = 0x10001
d = inverse(e,(p - 1) * (q - 1))
pub = RSA.construct((n,e,d,p,q))
with open('out.pem','wb') as f:
    f.write(pub.exportKey('PEM'))
with open('out.pem','rb') as f:
    print(f.read().decode())
'''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCnHIvLP0IERPVRaED+71dlCRBcm3be4jlHgqVqIIXyIvrzc8ZC
IIbIDqlBybNgq32i6PVlzBCsWiiTfBYS6J24qCjYVTywKk+yieNshieNNohmvQRF
bZOZITJiP99URkhtGWo3trQfoAZEQ7NfMoS1N3PDvPet1lMfFK81AyWt1wIDAQAB
AoGAIq74DK0KZJxzVfwPUVoXh27EKJRTrZrCTKc+8bHiWwkLkK+8vEjH8Imqc28L
fcrZ/o/fLsuVwk/MECA27KG+6hiRPJDWZmFgCInCABuhd+xitSBciMSGrO5ITjoq
YdgMsR5xJTI8vhXIJ1iCkkCz6fD6Di7s+3n/+Ti3iuK87jECQQDOY/pLyH0ppOk0
49pieQRshckQMXqsKhahEDZmWMu70JqDLF0U3aIfup1R87uogB8hJj8+K5RQavG4
4l0W5ghTAkEAz0eTNEWTe2iJ/Dq+8JKTN/MA/a8MiG7wvAkXqjx+B+Eow77IdoN8
D5ehD0x6ou73yaorTddidDAplNmvyq0D7QJAJbcPXhndBWclVozss2H59Prdqx/f
kuZ+DCCyUDGZyVBta9sHh3CY18N6TCeF+1yuU5hxpiLAj5F7apWy/SQ8EQJBAMtv
AxGda6cGLc8o1PeF1AlobUONxy4sPAdAoUJKRqNzH7AmEdcHKv6eoctDE2XQRc9e
PUwTpSRFlLnrgLXZYu0CQBKKT+oY4ssnwKDQqGPsh9MtPyilySL9sWJilk1cSXmQ
Xm7gjDq5S/x4k1gJyQFXbUnxTfsbLWs6BljHHlKSRes=
-----END RSA PRIVATE KEY-----
'''

如果是生成一组随机的公私钥文件，可以直接直接使用RSA.generate(bits)，其中的bits参数为生成的公钥文件中n的二进制位数，且bits>=1024，默认为1024。

from Crypto.PublicKey import RSA
from Crypto.Util.number import *
key = RSA.generate(1024)
print(key.publickey)
with open('out.pem','wb') as f:
    f.write(key.exportKey('PEM'))
with open('out.pem','rb') as f:
    print(f.read().decode())
'''
<bound method RsaKey.public_key of RsaKey(n=99929675131146107818047790971049703803161677332600984800831117021637597471437271599719384035180982326470249457001083005224626356572009901255841391966616564984242588913592789383087326511196585443834216472384770224810255153922375944881215835774119177009570247468911673932973239275741131654695253944455708641727, e=65537, d=27501740780061900509028777360107084282858928440567277451824014559115713670042546183199393779857817534085793587304881725189343016621314014739780326627796196251470626677550096120689732366473717193895036548926100990548453802714993577259273117223098888966957225092204230317866243049867167880710514827901086931493, p=9959145719455053414348729655771312861460726396890001110536788452571591154277537325754067618769136991544158484849077735057792084414015625760536769751415507, q=10033960536990122517580769502852456118641921945920255759007869111269242067226468943041901092934902353013133963062909073461567977701122665256982872188799461, u=2111771661302217183343493746406805348965531581492223651147849337466575464897027597797323383307376291792334461891498947953036261381547003770335520720819326)>
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCOTfkFWAc5UsCT07Y4bU9jKfpT5pt+ScHFIk/39jsE8yDHSFAo
pcQMlJ6GKRYfU7F/3xbY2udbvXBj9jJVLBmh3ORbZT06xwYDeqhvE2kJB+QfGk+J
POqzjCkFiDorxMUzWEq4us8nXmkv6WsrJMGSQZ0SQ7c29N9M0/8K622JvwIDAQAB
AoGAJyntaVuXLV8JcgW3piLrUNLKOpICZEi/Q9ZUJN2G069n64CK0wz//ihe0nR3
SqrZdGQ84PSp7LUfu9sTch5fdSQLH/OAQtVf/rwWuwulm8wS0njrU9xxQQWrwZoe
L9W7DlBWf5+PbmYdgyoLIwL3+wskvxiWswlvVcSR7RkXGiUCQQC+J0pN+1W2U3qe
a8rhAwX7XMSXoblFuqfBfH/duLZvseEEjtuTcj0ISlJgts2aZT1J8yHnllUoiqAu
WQPUK/rTAkEAv5T6OwPHj+4J/4WzQgJTN89Xj9ihR45wpr8Rr6WPXUCgXTe82UFz
ny68nIzALvKrLTf58yu8/E5wy2+SejBJ5QJASNUnwsK3y8QhvTgwVwsfaW3Y5vNM
0YZy5stW9offaNzLAUHunIUvF1PQRbb+/Vo1pXN40wljyMmAHQB/VO8bfQJBAIGQ
nVKAEdyzHavjngHMVL9vyEYOObSNDn6Wxb1GeJiWdl3UrjE35JwJHaG6Rtb5Yu7n
5nCgaeUwn3PV9vgP5EkCQQCWIiD5b8Qb5Mma8/iDNhchmRkosUug/iCBeqNh3nJc
txZnUy1fjc0toXxJY3ZBzTl3TNsk8p8x4H9y/NXoDtvu
-----END RSA PRIVATE KEY-----
'''

有n,e,d,p,q,u个6个参数，其中

。

使用公私钥加密或解密文件

在python中，利用公私钥文件，通过PKCS1_OAEP算法填充可以实现加解密，例如

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import *
flag = b'This_is_a_message_qwer'

key = RSA.generate(1024)
pub = key.publickey().exportKey()
public_key = RSA.importKey(pub)
pk = PKCS1_OAEP.new(public_key)
enc = pk.encrypt(flag)
print(enc)

priv = key.exportKey()
priv_key = RSA.importKey(priv)
sk = PKCS1_OAEP.new(priv_key)
msg = sk.decrypt(enc)
print(msg)
b'xd1/Ouxaexba]zxc0txc6xd7xc4fx13x96x9axeb5xdb8x92xc7x19x12yx9cx18xf7Ax9dxe9n&=<x16x07xefzxad2-x983xecx932xcbxf0x87~xdfxc1xd2x9fxd7@\Hx1fx87#xf3x84xa0xfcxd9xcfV$>xd7Ofxe6Gx06xcbx91xa1xccx0cxadxc2x9axadxe46x91xxadxa51xbbxfbxc1Ex93~e%xd1~xf8lx19nx88xffxac^xcax8fs*}xb9c0xc0Nxf2xfaxa4xd8x18g'
b'This_is_a_message_qwer'

解析公私钥

openssl

openssl是linux系统里一个开源的的软件包，应用程序通过openssl加密通信避免窃听，主要库为C语言写成。openssl还支持许多加密算法，例如RSA、DSA、ECDSA、ECDHE、Diffie–Hellman key exchange等。本文主要介绍openssl用于RSA中pem文件的加解密。

读取公钥pem

openssl rsa -pubin -text -modulus -in 1.pem
┌──(root㉿kali)-[/tmp]
└─# openssl rsa -pubin -text -modulus -in 1.pem 
RSA Public-Key: (1024 bit)
Modulus:
    00:8f:36:54:4b:9c:ac:89:f9:76:b1:3c:16:8c:10:
    db:99:4c:e9:95:92:ab:03:e9:31:d3:41:6f:a3:52:
    da:fe:66:fc:9a:4e:22:37:98:73:b3:c2:97:e6:42:
    ee:9b:04:ae:2d:5d:d0:3d:6f:09:9f:e7:44:35:b0:
    2f:3b:b2:41:8a:b1:3c:2b:d5:97:c1:8e:77:df:8b:
    d1:06:02:c3:35:42:d3:f0:fb:ec:a7:af:13:5c:1b:
    96:97:92:15:7b:35:a9:b3:58:d7:ba:f0:d1:45:9f:
    c8:d5:05:59:e7:ff:4d:8a:97:93:29:a0:7e:50:ab:
    6d:2e:e6:45:7e:74:b0:4b:3d
Exponent: 65537 (0x10001)
Modulus=8F36544B9CAC89F976B13C168C10DB994CE99592AB03E931D3416FA352DAFE66FC9A4E22379873B3C297E642EE9B04AE2D5DD03D6F099FE74435B02F3BB2418AB13C2BD597C18E77DF8BD10602C33542D3F0FBECA7AF135C1B969792157B35A9B358D7BAF0D1459FC8D50559E7FF4D8A979329A07E50AB6D2EE6457E74B04B3D
writing RSA key
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCPNlRLnKyJ+XaxPBaMENuZTOmV
kqsD6THTQW+jUtr+ZvyaTiI3mHOzwpfmQu6bBK4tXdA9bwmf50Q1sC87skGKsTwr
1ZfBjnffi9EGAsM1QtPw++ynrxNcG5aXkhV7NamzWNe68NFFn8jVBVnn/02Kl5Mp
oH5Qq20u5kV+dLBLPQIDAQAB
-----END PUBLIC KEY-----

其中Modulus为模数n的16进制下的值，Exponent为加密指数e。

读取私钥pem

openssl rsa -in 1.pem -text
┌──(root㉿kali)-[/tmp]
└─# openssl rsa -in 1.pem -text                
RSA Private-Key: (1024 bit, 2 primes)
modulus:
    00:8f:36:54:4b:9c:ac:89:f9:76:b1:3c:16:8c:10:
    db:99:4c:e9:95:92:ab:03:e9:31:d3:41:6f:a3:52:
    da:fe:66:fc:9a:4e:22:37:98:73:b3:c2:97:e6:42:
    ee:9b:04:ae:2d:5d:d0:3d:6f:09:9f:e7:44:35:b0:
    2f:3b:b2:41:8a:b1:3c:2b:d5:97:c1:8e:77:df:8b:
    d1:06:02:c3:35:42:d3:f0:fb:ec:a7:af:13:5c:1b:
    96:97:92:15:7b:35:a9:b3:58:d7:ba:f0:d1:45:9f:
    c8:d5:05:59:e7:ff:4d:8a:97:93:29:a0:7e:50:ab:
    6d:2e:e6:45:7e:74:b0:4b:3d
publicExponent: 65537 (0x10001)
privateExponent:
    1b:5b:06:de:0c:96:de:a2:22:bc:77:1c:5d:73:e8:
    e6:8f:0c:fd:4f:af:50:07:6e:c7:8a:33:cf:70:47:
    b9:99:a5:7d:ba:18:0a:23:9a:52:47:84:e9:6c:76:
    94:70:df:ee:75:81:8e:02:94:45:91:90:f3:6a:6c:
    93:4c:18:fd:a2:75:d5:18:9a:81:1d:38:ec:85:c3:
    33:f6:1e:69:0a:27:d5:ba:12:5d:1d:86:ac:4e:14:
    dc:e1:ad:f7:0b:64:ac:6a:3c:58:f7:c1:1c:5c:4f:
    d9:91:9a:05:c3:de:a0:2f:4c:43:28:da:33:9b:fe:
    60:a5:31:83:2f:ce:d8:51
prime1:
    00:bc:a4:41:8f:de:bc:c4:cc:c3:4b:ac:7e:65:da:
    f9:53:0b:53:d7:e9:f2:11:8b:fd:03:96:27:ca:f6:
    cb:02:ba:fd:60:51:56:78:64:7d:37:b5:b8:ee:92:
    12:57:ce:5f:be:96:32:40:48:47:fb:ea:8f:75:bb:
    60:c1:90:c1:e9
prime2:
    00:c2:59:5e:53:6e:a6:17:33:ea:00:72:87:da:0b:
    55:36:0f:cd:40:25:c6:e3:2c:b8:a3:4f:e5:13:9d:
    80:b2:76:78:66:04:88:51:13:fa:3e:7e:fc:08:f7:
    06:6b:3b:ce:09:bd:cc:46:91:e7:b7:74:8a:52:e4:
    f7:66:a9:36:35
exponent1:
    4e:a6:3d:1f:7a:c2:41:5b:0d:e1:b3:1d:4f:e2:28:
    29:53:83:b5:75:b8:93:50:46:41:04:8d:ba:b5:82:
    96:b4:d7:87:1c:e2:6c:77:99:2d:6c:fa:99:9d:15:
    40:be:ae:74:8b:b2:8f:d2:93:10:99:0f:0f:0a:fc:
    a0:37:76:61
exponent2:
    22:2f:a6:2f:f6:de:b0:66:29:5b:3a:ca:3a:c8:93:
    8c:96:ea:fb:c5:a9:5e:7c:97:5d:e2:c7:e0:d3:6b:
    b7:f8:ae:e5:03:17:17:6b:f4:30:da:15:6b:5e:48:
    7a:c4:62:51:c4:59:12:70:c7:d9:b5:5e:3f:86:97:
    1e:2f:d5:a1
coefficient:
    00:83:55:17:ad:1a:fe:bb:ac:04:d5:f7:92:ee:1a:
    b4:37:a9:28:e2:e9:73:3f:14:b3:d0:2d:8f:56:28:
    d5:55:22:9d:56:27:de:18:67:e5:b4:96:42:ca:8f:
    b0:b9:60:fb:23:9f:ab:62:3b:19:92:2c:0c:6a:31:
    b9:ad:09:0b:3c
writing RSA key
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCPNlRLnKyJ+XaxPBaMENuZTOmVkqsD6THTQW+jUtr+ZvyaTiI3
mHOzwpfmQu6bBK4tXdA9bwmf50Q1sC87skGKsTwr1ZfBjnffi9EGAsM1QtPw++yn
rxNcG5aXkhV7NamzWNe68NFFn8jVBVnn/02Kl5MpoH5Qq20u5kV+dLBLPQIDAQAB
AoGAG1sG3gyW3qIivHccXXPo5o8M/U+vUAdux4ozz3BHuZmlfboYCiOaUkeE6Wx2
lHDf7nWBjgKURZGQ82psk0wY/aJ11RiagR047IXDM/YeaQon1boSXR2GrE4U3OGt
9wtkrGo8WPfBHFxP2ZGaBcPeoC9MQyjaM5v+YKUxgy/O2FECQQC8pEGP3rzEzMNL
rH5l2vlTC1PX6fIRi/0DlifK9ssCuv1gUVZ4ZH03tbjukhJXzl++ljJASEf76o91
u2DBkMHpAkEAwlleU26mFzPqAHKH2gtVNg/NQCXG4yy4o0/lE52AsnZ4ZgSIURP6
Pn78CPcGazvOCb3MRpHnt3SKUuT3Zqk2NQJATqY9H3rCQVsN4bMdT+IoKVODtXW4
k1BGQQSNurWClrTXhxzibHeZLWz6mZ0VQL6udIuyj9KTEJkPDwr8oDd2YQJAIi+m
L/besGYpWzrKOsiTjJbq+8WpXnyXXeLH4NNrt/iu5QMXF2v0MNoVa15IesRiUcRZ
EnDH2bVeP4aXHi/VoQJBAINVF60a/rusBNX3ku4atDepKOLpcz8Us9Atj1Yo1VUi
nVYn3hhn5bSWQsqPsLlg+yOfq2I7GZIsDGoxua0JCzw=
-----END RSA PRIVATE KEY-----

其中一共有8个参数，分别为：

modulus:模数n

publicExponent:加密指数e

privateExponent:解密指数d

prime1&2:模数n的两个大因子p和q

exponent1&2:dp和dq，d mod (p – 1)和d mod (q – 1)

coefficient:

原始数据读取

读取公钥pem

例如一个pem公钥文件

-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXrGq02sFKE5Znv2GljNLThSWB
P6N2NfV41vaADS/ZEZB6JPo0RLTg4UYZOGg5SLYQkr5IvO6thXQJ+xFduuOYl8oe
p4BeLZLIwFnxZQIjSDe5GD/Id6wPLTDTGFB4y7aVK/D0v+y12uW44HrYAUeTCNU8
renYB8YQwZIwuO2qZwIDAQAB
-----END PUBLIC KEY-----

读取其中的base64编码并转hex得到

30819f300d06092a864886f70d010101050003818d0030818902818100d7ac6ab4dac14a139667bf61a58cd2d38525813fa37635f578d6f6800d2fd911907a24fa3444b4e0e1461938683948b61092be48bceead857409fb115dbae39897ca1ea7805e2d92c8c059f16502234837b9183fc877ac0f2d30d3185078cbb6952bf0f4bfecb5dae5b8e07ad801479308d53cade9d807c610c19230b8edaa670203010001

其中

内容
解析

3081
标签头，81表示后面接1bytes，82表示后接2bytes表示长度

9f
后接上0xdf(159)bytes的内容

300d06092a864886f70d010101050003
固定序列(具体包含的内容未知)

81
后面接1bytes，为82则表示后接2bytes表示长度

8d
后接上0x8d(141)bytes的内容

0030
固定序列

81
后面接1bytes，为82则表示后接2bytes表示长度

89
后接上0x89(137)bytes的内容

0281
81表示后面接1bytes，82表示后接2bytes表示长度

81
后面的模数n长度为0x81bytes，但是其中1bytes为00，故生成的模数二进制位数为1024

00d7-67
模数n的16进制形式

0203010001
02后接加密指数e的长度03即内容010001

内容
解析

3082
标签头，81表示后面接1bytes，82表示后接2bytes表示长度。

025e
后接0x25e(606)bytes的内容。

02010002
固定序列

81
81表示后面接1bytes，82表示后接2bytes表示长度。

81
后面的模数n长度为0x81bytes，但是其中1bytes为00，故生成的模数二进制位数为1024

b0fd-9017
模数n的16进制

0203010001
02后接加密指数e的长度03即内容010001

028180
81表示后面接1bytes的长度信息，80表示后接0x80(128)bytes长度的信息

13ea-580d
私钥指数d的16进制

024100
起始序列

c96c-e8e3
p的16进制

024100
起始序列

e0f2-463d
q的16进制

0240
起始序列

37af-d3af
dp的16进制

0240
起始序列

3537-91c1
dq的16进制

0240
起始序列

2167-b272
q inv p

推荐阅读：

关于微信数据库的解密以及取证

Shiro 历史漏洞分析

浅谈pyd文件逆向

CVE-2022-23222漏洞及利用分析

Mimikatz详细使用总结

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
p,q = getPrime(512),getPrime(512)
n = p * q
e = 0x10001
pub = RSA.construct((n,e))
with open('out.pem','wb') as f:
    f.write(pub.exportKey('PEM'))
with open('out.pem','rb') as f:
    print(f.read().decode())
'''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuRPouMRTcLWPBEUlhjCrZ6MNQ
rSy29BrHjH4+lGMykB23azPtT9fk7IsEFXoodm6tsPL8kheJ6cP+0WPldlQOw/K3
c9LUGzeCCAhNJuBjUoeW32ruE2HS7RoIF6vkP36zLs167ZZMK7Fg0cqW6VNXoJHT
zaKdqysBe+3W1VHl6QIDAQAB
-----END PUBLIC KEY-----
'''
```



```
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
p,q = getPrime(512),getPrime(512)
n = p * q
e = 0x10001
d = inverse(e,(p - 1) * (q - 1))
pub = RSA.construct((n,e,d,p,q))
with open('out.pem','wb') as f:
    f.write(pub.exportKey('PEM'))
with open('out.pem','rb') as f:
    print(f.read().decode())
'''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCnHIvLP0IERPVRaED+71dlCRBcm3be4jlHgqVqIIXyIvrzc8ZC
IIbIDqlBybNgq32i6PVlzBCsWiiTfBYS6J24qCjYVTywKk+yieNshieNNohmvQRF
bZOZITJiP99URkhtGWo3trQfoAZEQ7NfMoS1N3PDvPet1lMfFK81AyWt1wIDAQAB
AoGAIq74DK0KZJxzVfwPUVoXh27EKJRTrZrCTKc+8bHiWwkLkK+8vEjH8Imqc28L
fcrZ/o/fLsuVwk/MECA27KG+6hiRPJDWZmFgCInCABuhd+xitSBciMSGrO5ITjoq
YdgMsR5xJTI8vhXIJ1iCkkCz6fD6Di7s+3n/+Ti3iuK87jECQQDOY/pLyH0ppOk0
49pieQRshckQMXqsKhahEDZmWMu70JqDLF0U3aIfup1R87uogB8hJj8+K5RQavG4
4l0W5ghTAkEAz0eTNEWTe2iJ/Dq+8JKTN/MA/a8MiG7wvAkXqjx+B+Eow77IdoN8
D5ehD0x6ou73yaorTddidDAplNmvyq0D7QJAJbcPXhndBWclVozss2H59Prdqx/f
kuZ+DCCyUDGZyVBta9sHh3CY18N6TCeF+1yuU5hxpiLAj5F7apWy/SQ8EQJBAMtv
AxGda6cGLc8o1PeF1AlobUONxy4sPAdAoUJKRqNzH7AmEdcHKv6eoctDE2XQRc9e
PUwTpSRFlLnrgLXZYu0CQBKKT+oY4ssnwKDQqGPsh9MtPyilySL9sWJilk1cSXmQ
Xm7gjDq5S/x4k1gJyQFXbUnxTfsbLWs6BljHHlKSRes=
-----END RSA PRIVATE KEY-----
'''
```



```
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
key = RSA.generate(1024)
print(key.publickey)
with open('out.pem','wb') as f:
    f.write(key.exportKey('PEM'))
with open('out.pem','rb') as f:
    print(f.read().decode())
'''
<bound method RsaKey.public_key of RsaKey(n=99929675131146107818047790971049703803161677332600984800831117021637597471437271599719384035180982326470249457001083005224626356572009901255841391966616564984242588913592789383087326511196585443834216472384770224810255153922375944881215835774119177009570247468911673932973239275741131654695253944455708641727, e=65537, d=27501740780061900509028777360107084282858928440567277451824014559115713670042546183199393779857817534085793587304881725189343016621314014739780326627796196251470626677550096120689732366473717193895036548926100990548453802714993577259273117223098888966957225092204230317866243049867167880710514827901086931493, p=9959145719455053414348729655771312861460726396890001110536788452571591154277537325754067618769136991544158484849077735057792084414015625760536769751415507, q=10033960536990122517580769502852456118641921945920255759007869111269242067226468943041901092934902353013133963062909073461567977701122665256982872188799461, u=2111771661302217183343493746406805348965531581492223651147849337466575464897027597797323383307376291792334461891498947953036261381547003770335520720819326)>
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCOTfkFWAc5UsCT07Y4bU9jKfpT5pt+ScHFIk/39jsE8yDHSFAo
pcQMlJ6GKRYfU7F/3xbY2udbvXBj9jJVLBmh3ORbZT06xwYDeqhvE2kJB+QfGk+J
POqzjCkFiDorxMUzWEq4us8nXmkv6WsrJMGSQZ0SQ7c29N9M0/8K622JvwIDAQAB
AoGAJyntaVuXLV8JcgW3piLrUNLKOpICZEi/Q9ZUJN2G069n64CK0wz//ihe0nR3
SqrZdGQ84PSp7LUfu9sTch5fdSQLH/OAQtVf/rwWuwulm8wS0njrU9xxQQWrwZoe
L9W7DlBWf5+PbmYdgyoLIwL3+wskvxiWswlvVcSR7RkXGiUCQQC+J0pN+1W2U3qe
a8rhAwX7XMSXoblFuqfBfH/duLZvseEEjtuTcj0ISlJgts2aZT1J8yHnllUoiqAu
WQPUK/rTAkEAv5T6OwPHj+4J/4WzQgJTN89Xj9ihR45wpr8Rr6WPXUCgXTe82UFz
ny68nIzALvKrLTf58yu8/E5wy2+SejBJ5QJASNUnwsK3y8QhvTgwVwsfaW3Y5vNM
0YZy5stW9offaNzLAUHunIUvF1PQRbb+/Vo1pXN40wljyMmAHQB/VO8bfQJBAIGQ
nVKAEdyzHavjngHMVL9vyEYOObSNDn6Wxb1GeJiWdl3UrjE35JwJHaG6Rtb5Yu7n
5nCgaeUwn3PV9vgP5EkCQQCWIiD5b8Qb5Mma8/iDNhchmRkosUug/iCBeqNh3nJc
txZnUy1fjc0toXxJY3ZBzTl3TNsk8p8x4H9y/NXoDtvu
-----END RSA PRIVATE KEY-----
'''
```



```
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import *
flag = b'This_is_a_message_qwer'

key = RSA.generate(1024)
pub = key.publickey().exportKey()
public_key = RSA.importKey(pub)
pk = PKCS1_OAEP.new(public_key)
enc = pk.encrypt(flag)
print(enc)

priv = key.exportKey()
priv_key = RSA.importKey(priv)
sk = PKCS1_OAEP.new(priv_key)
msg = sk.decrypt(enc)
print(msg)
b'xd1/Ouxaexba]zxc0txc6xd7xc4fx13x96x9axeb5xdb8x92xc7x19x12yx9cx18xf7Ax9dxe9n&=<x16x07xefzxad2-x983xecx932xcbxf0x87~xdfxc1xd2x9fxd7@\Hx1fx87#xf3x84xa0xfcxd9xcfV$>xd7Ofxe6Gx06xcbx91xa1xccx0cxadxc2x9axadxe46x91xxadxa51xbbxfbxc1Ex93~e%xd1~xf8lx19nx88xffxac^xcax8fs*}xb9c0xc0Nxf2xfaxa4xd8x18g'
b'This_is_a_message_qwer'
```



```
openssl rsa -pubin -text -modulus -in 1.pem
┌──(root㉿kali)-[/tmp]
└─# openssl rsa -pubin -text -modulus -in 1.pem 
RSA Public-Key: (1024 bit)
Modulus:
    00:8f:36:54:4b:9c:ac:89:f9:76:b1:3c:16:8c:10:
    db:99:4c:e9:95:92:ab:03:e9:31:d3:41:6f:a3:52:
    da:fe:66:fc:9a:4e:22:37:98:73:b3:c2:97:e6:42:
    ee:9b:04:ae:2d:5d:d0:3d:6f:09:9f:e7:44:35:b0:
    2f:3b:b2:41:8a:b1:3c:2b:d5:97:c1:8e:77:df:8b:
    d1:06:02:c3:35:42:d3:f0:fb:ec:a7:af:13:5c:1b:
    96:97:92:15:7b:35:a9:b3:58:d7:ba:f0:d1:45:9f:
    c8:d5:05:59:e7:ff:4d:8a:97:93:29:a0:7e:50:ab:
    6d:2e:e6:45:7e:74:b0:4b:3d
Exponent: 65537 (0x10001)
Modulus=8F36544B9CAC89F976B13C168C10DB994CE99592AB03E931D3416FA352DAFE66FC9A4E22379873B3C297E642EE9B04AE2D5DD03D6F099FE74435B02F3BB2418AB13C2BD597C18E77DF8BD10602C33542D3F0FBECA7AF135C1B969792157B35A9B358D7BAF0D1459FC8D50559E7FF4D8A979329A07E50AB6D2EE6457E74B04B3D
writing RSA key
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCPNlRLnKyJ+XaxPBaMENuZTOmV
kqsD6THTQW+jUtr+ZvyaTiI3mHOzwpfmQu6bBK4tXdA9bwmf50Q1sC87skGKsTwr
1ZfBjnffi9EGAsM1QtPw++ynrxNcG5aXkhV7NamzWNe68NFFn8jVBVnn/02Kl5Mp
oH5Qq20u5kV+dLBLPQIDAQAB
-----END PUBLIC KEY-----
```



```
openssl rsa -in 1.pem -text
┌──(root㉿kali)-[/tmp]
└─# openssl rsa -in 1.pem -text                
RSA Private-Key: (1024 bit, 2 primes)
modulus:
    00:8f:36:54:4b:9c:ac:89:f9:76:b1:3c:16:8c:10:
    db:99:4c:e9:95:92:ab:03:e9:31:d3:41:6f:a3:52:
    da:fe:66:fc:9a:4e:22:37:98:73:b3:c2:97:e6:42:
    ee:9b:04:ae:2d:5d:d0:3d:6f:09:9f:e7:44:35:b0:
    2f:3b:b2:41:8a:b1:3c:2b:d5:97:c1:8e:77:df:8b:
    d1:06:02:c3:35:42:d3:f0:fb:ec:a7:af:13:5c:1b:
    96:97:92:15:7b:35:a9:b3:58:d7:ba:f0:d1:45:9f:
    c8:d5:05:59:e7:ff:4d:8a:97:93:29:a0:7e:50:ab:
    6d:2e:e6:45:7e:74:b0:4b:3d
publicExponent: 65537 (0x10001)
privateExponent:
    1b:5b:06:de:0c:96:de:a2:22:bc:77:1c:5d:73:e8:
    e6:8f:0c:fd:4f:af:50:07:6e:c7:8a:33:cf:70:47:
    b9:99:a5:7d:ba:18:0a:23:9a:52:47:84:e9:6c:76:
    94:70:df:ee:75:81:8e:02:94:45:91:90:f3:6a:6c:
    93:4c:18:fd:a2:75:d5:18:9a:81:1d:38:ec:85:c3:
    33:f6:1e:69:0a:27:d5:ba:12:5d:1d:86:ac:4e:14:
    dc:e1:ad:f7:0b:64:ac:6a:3c:58:f7:c1:1c:5c:4f:
    d9:91:9a:05:c3:de:a0:2f:4c:43:28:da:33:9b:fe:
    60:a5:31:83:2f:ce:d8:51
prime1:
    00:bc:a4:41:8f:de:bc:c4:cc:c3:4b:ac:7e:65:da:
    f9:53:0b:53:d7:e9:f2:11:8b:fd:03:96:27:ca:f6:
    cb:02:ba:fd:60:51:56:78:64:7d:37:b5:b8:ee:92:
    12:57:ce:5f:be:96:32:40:48:47:fb:ea:8f:75:bb:
    60:c1:90:c1:e9
prime2:
    00:c2:59:5e:53:6e:a6:17:33:ea:00:72:87:da:0b:
    55:36:0f:cd:40:25:c6:e3:2c:b8:a3:4f:e5:13:9d:
    80:b2:76:78:66:04:88:51:13:fa:3e:7e:fc:08:f7:
    06:6b:3b:ce:09:bd:cc:46:91:e7:b7:74:8a:52:e4:
    f7:66:a9:36:35
exponent1:
    4e:a6:3d:1f:7a:c2:41:5b:0d:e1:b3:1d:4f:e2:28:
    29:53:83:b5:75:b8:93:50:46:41:04:8d:ba:b5:82:
    96:b4:d7:87:1c:e2:6c:77:99:2d:6c:fa:99:9d:15:
    40:be:ae:74:8b:b2:8f:d2:93:10:99:0f:0f:0a:fc:
    a0:37:76:61
exponent2:
    22:2f:a6:2f:f6:de:b0:66:29:5b:3a:ca:3a:c8:93:
    8c:96:ea:fb:c5:a9:5e:7c:97:5d:e2:c7:e0:d3:6b:
    b7:f8:ae:e5:03:17:17:6b:f4:30:da:15:6b:5e:48:
    7a:c4:62:51:c4:59:12:70:c7:d9:b5:5e:3f:86:97:
    1e:2f:d5:a1
coefficient:
    00:83:55:17:ad:1a:fe:bb:ac:04:d5:f7:92:ee:1a:
    b4:37:a9:28:e2:e9:73:3f:14:b3:d0:2d:8f:56:28:
    d5:55:22:9d:56:27:de:18:67:e5:b4:96:42:ca:8f:
    b0:b9:60:fb:23:9f:ab:62:3b:19:92:2c:0c:6a:31:
    b9:ad:09:0b:3c
writing RSA key
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCPNlRLnKyJ+XaxPBaMENuZTOmVkqsD6THTQW+jUtr+ZvyaTiI3
mHOzwpfmQu6bBK4tXdA9bwmf50Q1sC87skGKsTwr1ZfBjnffi9EGAsM1QtPw++yn
rxNcG5aXkhV7NamzWNe68NFFn8jVBVnn/02Kl5MpoH5Qq20u5kV+dLBLPQIDAQAB
AoGAG1sG3gyW3qIivHccXXPo5o8M/U+vUAdux4ozz3BHuZmlfboYCiOaUkeE6Wx2
lHDf7nWBjgKURZGQ82psk0wY/aJ11RiagR047IXDM/YeaQon1boSXR2GrE4U3OGt
9wtkrGo8WPfBHFxP2ZGaBcPeoC9MQyjaM5v+YKUxgy/O2FECQQC8pEGP3rzEzMNL
rH5l2vlTC1PX6fIRi/0DlifK9ssCuv1gUVZ4ZH03tbjukhJXzl++ljJASEf76o91
u2DBkMHpAkEAwlleU26mFzPqAHKH2gtVNg/NQCXG4yy4o0/lE52AsnZ4ZgSIURP6
Pn78CPcGazvOCb3MRpHnt3SKUuT3Zqk2NQJATqY9H3rCQVsN4bMdT+IoKVODtXW4
k1BGQQSNurWClrTXhxzibHeZLWz6mZ0VQL6udIuyj9KTEJkPDwr8oDd2YQJAIi+m
L/besGYpWzrKOsiTjJbq+8WpXnyXXeLH4NNrt/iu5QMXF2v0MNoVa15IesRiUcRZ
EnDH2bVeP4aXHi/VoQJBAINVF60a/rusBNX3ku4atDepKOLpcz8Us9Atj1Yo1VUi
nVYn3hhn5bSWQsqPsLlg+yOfq2I7GZIsDGoxua0JCzw=
-----END RSA PRIVATE KEY-----
```



```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXrGq02sFKE5Znv2GljNLThSWB
P6N2NfV41vaADS/ZEZB6JPo0RLTg4UYZOGg5SLYQkr5IvO6thXQJ+xFduuOYl8oe
p4BeLZLIwFnxZQIjSDe5GD/Id6wPLTDTGFB4y7aVK/D0v+y12uW44HrYAUeTCNU8
renYB8YQwZIwuO2qZwIDAQAB
-----END PUBLIC KEY-----
```



```
30819f300d06092a864886f70d010101050003818d0030818902818100d7ac6ab4dac14a139667bf61a58cd2d38525813fa37635f578d6f6800d2fd911907a24fa3444b4e0e1461938683948b61092be48bceead857409fb115dbae39897ca1ea7805e2d92c8c059f16502234837b9183fc877ac0f2d30d3185078cbb6952bf0f4bfecb5dae5b8e07ad801479308d53cade9d807c610c19230b8edaa670203010001
```



```
from Crypto.PublicKey import RSA
key = RSA.generate(1024)
with open('1.pem','wb') as f:
    f.write(b'n = ' + str(hex(key.n)[2:]).encode() + b'n')
    f.write(b'e = ' + str(hex(key.e)[2:]).encode() + b'n')
    f.write(b'p = ' + str(hex(key.p)[2:]).encode() + b'n')
    f.write(b'q = ' + str(hex(key.q)[2:]).encode() + b'n')
    f.write(b'd = ' + str(hex(key.d)[2:]).encode() + b'n')
    f.write(b'dp = '+ str(hex((key.d) % ((key.p) - 1))[2:]).encode() + b'n')
    f.write(b'dq = ' + str(hex((key.d) % ((key.q) - 1))[2:]).encode() + b'n')
    f.write(b'p_q = ' + str(hex(pow(key.p,-1,key.q))[2:]).encode() + b'n')
    f.write(b'q_p = ' + str(hex(pow(key.q, -1, key.p))[2:]).encode() + b'n')
    f.write(key.exportKey('PEM'))

with open('1.pem','rb') as f:
    print(f.read().decode())
```



```
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCw/aHmn+xs4OCJbVu1U0JhR/M4h42TYeVyR02wdtV+Dwt+CrE7
JlZyKBCM+jOXx+tgoxZ6e/U+voP9iU4Fpdmyi/HE8U5ZZ6YH8Bzx8Qh8vM3QM8XU
W4NGfg6N9VG7uVdwioOBbZ9AoOBYHjMdxoZ8O5AxO3Lp0rzkfQTUe9CQFwIDAQAB
AoGAE+puYeOj+HpzebNXCvfT89tjSHykVy3AYlQYr18n1df+jI/KcqP1PUI53os2
7ADggQ7I9D5nkchhVNGy+Fq5vLgdTRYZ859iT1h9i+bTwt7Uq2OfJR/NRkVcvaSv
7UKHmF3AyzNOpSf2NunvYUSJ5n92jUuXdXkvqmeS3/FOWA0CQQDJbCjac+mVzCzZ
U84s+7JXviTHPoN9GXZY3vr1tIBogwyftCa1+pVIYu7WTwwHzcKe9KU4GPbLCTYU
45FJ0ejjAkEA4PK+h3cB65Oahwmxza1w7tugGNTXcLhMpJ8PCO65pG0wRIpp3doC
TRLKdUUAcVromiiU8m/Mt8jwyhVxFMpGPQJAN6/uj47yapbbY253FxqzUOzh8DAJ
XGHYxXNIgPvZcIuixtigxzkzYqLvk1KhadrqTtYmg57rRHEUgav09CrTrwJANTc3
+7QbsC9rDycr+Qxe+yLZ7QXtMa1n9EnstKBFKrDqCkz0XpeEk9cuLi/0utxWyqFv
Gyt3ssLGtAf+iHyRwQJAIWcJAM/jTFTMXNUrYK0fa0MMpNMrwnlDb6uyMn/4Q41g
f3RB/34+gFrCRZEhMtasgaOkoHYP3VZQvqkXzyaycg==
-----END RSA PRIVATE KEY-----
```



```
3082025b02010002818100
b0fda1e69fec6ce0e0896d5bb553426147f338878d9361e572474db076d57e0f0b7e0ab13b26567228108cfa3397c7eb60a3167a7bf53ebe83fd894e05a5d9b28bf1c4f14e5967a607f01cf1f1087cbccdd033c5d45b83467e0e8df551bbb957708a83816d9f40a0e0581e331dc6867c3b90313b72e9d2bce47d04d47bd09017
0203010001
028180 13ea6e61e3a3f87a7379b3570af7d3f3db63487ca4572dc0625418af5f27d5d7fe8c8fca72a3f53d4239de8b36ec00e0810ec8f43e6791c86154d1b2f85ab9bcb81d4d1619f39f624f587d8be6d3c2ded4ab639f251fcd46455cbda4afed4287985dc0cb334ea527f636e9ef614489e67f768d4b9775792faa6792dff14e580d
024100 c96c28da73e995cc2cd953ce2cfbb257be24c73e837d197658defaf5b48068830c9fb426b5fa954862eed64f0c07cdc29ef4a53818f6cb093614e39149d1e8e3
024100 e0f2be877701eb939a8709b1cdad70eedba018d4d770b84ca49f0f08eeb9a46d30448a69ddda024d12ca754500715ae89a2894f26fccb7c8f0ca157114ca463d
0240   37afee8f8ef26a96db636e77171ab350ece1f030095c61d8c5734880fbd9708ba2c6d8a0c7393362a2ef9352a169daea4ed626839eeb44711481abf4f42ad3af
0240   353737fbb41bb02f6b0f272bf90c5efb22d9ed05ed31ad67f449ecb4a0452ab0ea0a4cf45e978493d72e2e2ff4badc56caa16f1b2b77b2c2c6b407fe887c91c1
0240   21670900cfe34c54cc5cd52b60ad1f6b430ca4d32bc279436fabb2327ff8438d607f7441ff7e3e805ac245912132d6ac81a3a4a0760fdd5650bea917cf26b272
```



```
from Crypto.Util.number import *
from Crypto.PublicKey import RSA

e = 65537
flag = b'ACTF{...}'

while True:
    p = getPrime(1024)
    q = inverse(e, p)
    if not isPrime(q):
        continue
    n = p * q
    public = RSA.construct((n, e))
    with open("public.pem", "wb") as file:
        file.write(public.exportKey('PEM'))
    with open("flag", "wb") as file:
        file.write(long_to_bytes(pow(bytes_to_long(flag), e, n)))
    break
```



```
from Crypto.PublicKey import RSA
with open(r'public.pem', "r") as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    n = rsakey.n
    e = rsakey.e
```



```
from Crypto.Util.number import *
import gmpy2
from Crypto.PublicKey import RSA
from tqdm import tqdm
with open(r'public.pem', "r") as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    n = rsakey.n
    e = rsakey.e
with open('flag','rb') as f:
    c = f.read()
    c = bytes_to_long(c)
print(c)

for k in tqdm(range(1,1 << 16)):
    root = gmpy2.iroot(1 + 4 * k * n * e,2)
    if root[1] == True:
        p = (1 + root[0]) // (2 * k)
        assert n % p == 0
        q = n // p
        phi = (p - 1) * (q - 1)
        d = gmpy2.invert(e,phi)
        m = pow(c,d,n)
        print(long_to_bytes(m))
        break
```



```
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from secret import flag

key = RSA.generate(1024)
open("flag.enc",'wb').write(PKCS1_OAEP.new(key.publickey()).encrypt(flag))
open('priv.pem','wb').write(key.exportKey('PEM'))
```



```
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDXFSUGqpzsBeUzXWtG9UkUB8MZn9UQkfH2Aw03YrngP0nJ3NwH
UFTgzBSLl0tBhUvZO07haiqHbuYgBegO+Aa3qjtksb+bH6dz41PQzbn/l4Pd1fXm
dJmtEPNh6TjQC4KmpMQqBTXF52cheY6GtFzUuNA7DX51wr6HZqHoQ73GQQIDAQAB

yQvOzxy6szWFheigQdGxAkEA4wFss2CcHWQ8FnQ5w7k4uIH0I38khg07HLhaYm1c
zUcmlk4PgnDWxN+ev+vMU45O5eGntzaO3lHsaukX9461mA==
-----END RSA PRIVATE KEY-----
```



```
第一段：
3082025e02010002818100d7152506aa9cec05e5335d6b46f5491407c3199fd51091f1f6030d3762b9e03f49c9dcdc075054e0cc148b974b41854bd93b4ee16a2a876ee62005e80ef806b7aa3b64b1bf9b1fa773e353d0cdb9ff9783ddd5f5e67499ad10f361e938d00b82a6a4c42a0535c5e76721798e86b45cd4b8d03b0d7e75c2be8766a1e843bdc6410203010001
第二段：
c90bcecf1cbab3358585e8a041d1b1024100e3016cb3609c1d643c167439c3b938b881f4237f24860d3b1cb85a626d5ccd4726964e0f8270d6c4df9ebfebcc538e4ee5e1a7b7368ede51ec6ae917f78eb598
```



```
n = 0xd7152506aa9cec05e5335d6b46f5491407c3199fd51091f1f6030d3762b9e03f49c9dcdc075054e0cc148b974b41854bd93b4ee16a2a876ee62005e80ef806b7aa3b64b1bf9b1fa773e353d0cdb9ff9783ddd5f5e67499ad10f361e938d00b82a6a4c42a0535c5e76721798e86b45cd4b8d03b0d7e75c2be8766a1e843bdc641
e = 0x10001
```



```
_dq = 0xc90bcecf1cbab3358585e8a041d1b1
qinvp = 0xe3016cb3609c1d643c167439c3b938b881f4237f24860d3b1cb85a626d5ccd4726964e0f8270d6c4df9ebfebcc538e4ee5e1a7b7368ede51ec6ae917f78eb598
```



```
from Crypto.Util.number import *
import gmpy2
from tqdm import tqdm
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
n = 0xd7152506aa9cec05e5335d6b46f5491407c3199fd51091f1f6030d3762b9e03f49c9dcdc075054e0cc148b974b41854bd93b4ee16a2a876ee62005e80ef806b7aa3b64b1bf9b1fa773e353d0cdb9ff9783ddd5f5e67499ad10f361e938d00b82a6a4c42a0535c5e76721798e86b45cd4b8d03b0d7e75c2be8766a1e843bdc641
e = 0x10001
_dq = 0xc90bcecf1cbab3358585e8a041d1b1
t = 0xe3016cb3609c1d643c167439c3b938b881f4237f24860d3b1cb85a626d5ccd4726964e0f8270d6c4df9ebfebcc538e4ee5e1a7b7368ede51ec6ae917f78eb598
with open('flag.enc','rb') as f:
    c = f.read()
PR.<x> = PolynomialRing(Zmod(n))
dq = (2 ** 120 * x) + _dq
for k in tqdm(range(65537,55000,-1)):
    f = t * (e * dq - 1) ** 2 + k * (2 * t - 1) * (e * dq - 1) + t * k * k - k * k
    f = f.monic()
    root = f.small_roots(X=2^392,beta=0.4)
    if len(root) > 0:
        print(int(root[0]) * 2 ** 120 + _dq)
        break
#dq = 11263269100321843418340309033584057768246046953115325020896491943793759194249558697334095131684279304657225064156696057310019203890620314290203835007881649
#k = 59199
```



```
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import gmpy2
with open("flag.enc","rb")as f:
    c = f.read()
dq = 11263269100321843418340309033584057768246046953115325020896491943793759194249558697334095131684279304657225064156696057310019203890620314290203835007881649
k = 59199
n = 0xd7152506aa9cec05e5335d6b46f5491407c3199fd51091f1f6030d3762b9e03f49c9dcdc075054e0cc148b974b41854bd93b4ee16a2a876ee62005e80ef806b7aa3b64b1bf9b1fa773e353d0cdb9ff9783ddd5f5e67499ad10f361e938d00b82a6a4c42a0535c5e76721798e86b45cd4b8d03b0d7e75c2be8766a1e843bdc641
e = 0x10001
q = int((e * dq - 1) // k + 1)
assert n % q == 0
p = int(n // q)
phi = (p - 1) * (q - 1)
d = int(gmpy2.invert(e,phi))
key = RSA.construct((n,e,d,p,q))
flag = PKCS1_OAEP.new(key)
flag = flag.decrypt(c)
print(flag)
```
