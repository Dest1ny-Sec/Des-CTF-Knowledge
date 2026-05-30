# 北美大厂后端开发CTF面试题解题记录

> 原文: https://www.ctfiot.com/230796.html
> ID: 230796

前言

过年的时候，美国留学的朋友联系我说在美国求职，在笔试之前投递简历的过程中要在完成一个线上的题目，发给我链接之后我发现竟然是一个CTF题目(Fetch Backend CTF)，但是我朋友面试的是后端开发岗位。于是简单的记录了一下解题过程。

题目地址:

https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/pages/landing_page.html

题目描述：

There are currently 5 tokens hidden in this challenge. Your goal is to find as many as you can. You do not need to find all of them, and you should only spend the amount of time you think is reasonable for a CTF. We do not track how long you spend attempting the challenge, and there is no time limit.
Good Luck!

Token1

访问跟目录可以看到存在列目录漏洞。

在https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/pages/token.md中获得第一个Token。

Token2

https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/pages/secretbox.md

存在加密数据

# Secretbox

To correctly decrypt the tokens, you will need to use an NaCl secret box implementation.

Base64 Encoded Secret Key:  dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g=
Base64 Encoded Nonce:  usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq
Base64 Encoded Value:  usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq4OxKbmluN/Ec7gS9EVVeh82JsqgcCUfxmAXXAx3xqmDz+dA8+JTtRknQwgjekROmuAbLiiYCQgddczHcu9xRGf1g0/KKeqnrcfbdIj1PUlK0W5iL22v98ZK+5gTFpPoHdqOHCJ2wesES6a18/t1C0CI7F40AnTrL2kengA0FCh4s4MY4

Base64 Encoded Secret Key:  dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g=
Base64 Encoded Nonce:  /KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1i
Base64 Encoded Value:  /KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1iMQBE3XbIMi0G/BowKduAtkW9uvBwoRDicvmeFfDvaez3xw==

谷歌搜了一下这个算法没有找到现成的脚本，于是结合chatgpt进行了实现。

首先安装对应的库

pip install pynacl

解密脚本1

import nacl.secret
import base64
import binascii

base64_key = "dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g="
base64_nonce = "usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq"
base64_encrypted_value = "usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq4OxKbmluN/Ec7gS9EVVeh82JsqgcCUfxmAXXAx3xqmDz+dA8+JTtRknQwgjekROmuAbLiiYCQgddczHcu9xRGf1g0/KKeqnrcfbdIj1PUlK0W5iL22v98ZK+5gTFpPoHdqOHCJ2wesES6a18/t1C0CI7F40AnTrL2kengA0FCh4s4MY4"

key = base64.b64decode(base64_key)
nonce = base64.b64decode(base64_nonce)
encrypted_value = base64.b64decode(base64_encrypted_value)

print(key)
print(nonce)
print(encrypted_value)

box = nacl.secret.SecretBox(key)

decrypted_value = box.decrypt(encrypted_value)
print(f"Decrypted value: {decrypted_value}")

解密之后得到一个token

Decrypted value: b'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IkpXVF9UT0tFTiJ9.ghpSD18-j76IdRH3xqaKk1-PrnyzOq3E5kiqUGLXzBI'

解密脚本2

第二个密码解密之后得到一个token

import nacl.secret
import base64
import binascii

base64_key = "dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g="
base64_nonce = "/KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1i"
base64_encrypted_value = "/KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1iMQBE3XbIMi0G/BowKduAtkW9uvBwoRDicvmeFfDvaez3xw=="
key = base64.b64decode(base64_key)
nonce = base64.b64decode(base64_nonce)
encrypted_value = base64.b64decode(base64_encrypted_value)

print(key)
print(nonce)
print(encrypted_value)

box = nacl.secret.SecretBox(key)

decrypted_value = box.decrypt(encrypted_value)
print(f"Decrypted value: {decrypted_value}")

解密结果

b'thisisakeywith32lettersinitfetch'
b'xfcxa4x88xbf0xfex11xf0xf6xa2x14xc3Kxc62]gxe9xccxxd5xaex9db'
b'xfcxa4x88xbf0xfex11xf0xf6xa2x14xc3Kxc62]gxe9xccxxd5xaex9db1x00Dxddvxc82-x06xfcx1a0)xdbx80xb6Exbdxbaxf0pxa1x10xe2rxf9x9ex15xf0xefixecxf7xc7'
Decrypted value: b'NA_CL_SECRET_TOKEN'

于是拿到了第二个token。

Token3

在https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/pages/openapi.yaml发现存在两个接口。

# Generated with protoc-gen-openapi
# https://github.com/google/gnostic/tree/master/cmd/protoc-gen-openapi

openapi: 3.0.3
info:
    title: Fetch Backend CTF
    version: 0.0.1
paths:
    /token.v1.TokenService/GetToken:
        post:
            tags:
                - TokenService
            operationId: TokenService_GetToken
            requestBody:
                content:
                    application/json: {}
                required: true
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/GetTokenResponse'
    /token.v1.TokenService/StreamToken:
        post:
            tags:
                - TokenService
            operationId: TokenService_StreamToken
            requestBody:
                content:
                    application/json: {}
                required: true
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/StreamTokenResponse'
components:
    schemas:
        GetTokenResponse:
            type: object
            properties:
                token:
                    type: string
        StreamTokenResponse:
            type: object
            properties:
                message:
                    type: string
tags:
    - name: TokenService

分别是

/token.v1.TokenService/GetToken
/token.v1.TokenService/StreamToken

猜测剩余两个token要在两个接口中获取。首先尝试第一个接口，直接请求

curl  https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/token.v1.TokenService/GetToken

提示405，使用POST继续请求。

curl -v -X POST https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/token.v1.TokenService/GetToken

提示请求的content-type不正确，通过接口文档，我们可以指导content-type为josn格式。

最终提示我们没有正确的token，结合token2中获取的token发起请求。

最终我们获取到了第三个token。

Token4

第四个token应该是第二个接口获取。尝试发起请求

首先提示的是HTTP/2 415 Unsupported Media Type，第二个接口不在接受application/json，我们观察一下返回包的Accept-Post，发现接受以下请求:

Accept-Post: application/connect+json, application/connect+json; charset=utf-8, application/connect+proto, application/grpc, application/grpc+json, application/grpc+json; charset=utf-8, application/grpc+proto, application/grpc-web, application/grpc-web+json, application/grpc-web+json; charset=utf-8, application/grpc-web+proto

于是使用application/connect+json进行请求

从返回包的响应看应该是我们的请求体构造的有问题，带着疑问喂给deepseek。

问题

回答

最后尝试了各种方式，还是没有拿到最终的Token，猜测可能跟接口文档以及application/connect+json有关吧。最后如果有师傅拿到最后一个token可以私聊交流一下。

最后

由于实在找不到最后一个token，朋友也是直接放弃只交了三个Token+1个Authorization。最后我也顺便问了问美国程序员的薪资，大概就是大厂好一点年薪9w美刀吧。


```
https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/pages/landing_page.html
There are currently 5 tokens hidden in this challenge. Your goal is to find as many as you can. You do not need to find all of them, and you should only spend the amount of time you think is reasonable for a CTF. We do not track how long you spend attempting the challenge, and there is no time limit.
Good Luck!
# Secretbox

To correctly decrypt the tokens, you will need to use an NaCl secret box implementation.

Base64 Encoded Secret Key:  dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g=
Base64 Encoded Nonce:  usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq
Base64 Encoded Value:  usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq4OxKbmluN/Ec7gS9EVVeh82JsqgcCUfxmAXXAx3xqmDz+dA8+JTtRknQwgjekROmuAbLiiYCQgddczHcu9xRGf1g0/KKeqnrcfbdIj1PUlK0W5iL22v98ZK+5gTFpPoHdqOHCJ2wesES6a18/t1C0CI7F40AnTrL2kengA0FCh4s4MY4

Base64 Encoded Secret Key:  dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g=
Base64 Encoded Nonce:  /KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1i
Base64 Encoded Value:  /KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1iMQBE3XbIMi0G/BowKduAtkW9uvBwoRDicvmeFfDvaez3xw==
pip install pynacl
import nacl.secret
import base64
import binascii

base64_key = "dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g="
base64_nonce = "usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq"
base64_encrypted_value = "usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq4OxKbmluN/Ec7gS9EVVeh82JsqgcCUfxmAXXAx3xqmDz+dA8+JTtRknQwgjekROmuAbLiiYCQgddczHcu9xRGf1g0/KKeqnrcfbdIj1PUlK0W5iL22v98ZK+5gTFpPoHdqOHCJ2wesES6a18/t1C0CI7F40AnTrL2kengA0FCh4s4MY4"

key = base64.b64decode(base64_key)
nonce = base64.b64decode(base64_nonce)
encrypted_value = base64.b64decode(base64_encrypted_value)

print(key)
print(nonce)
print(encrypted_value)

box = nacl.secret.SecretBox(key)

decrypted_value = box.decrypt(encrypted_value)
print(f"Decrypted value: {decrypted_value}")
Decrypted value: b'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IkpXVF9UT0tFTiJ9.ghpSD18-j76IdRH3xqaKk1-PrnyzOq3E5kiqUGLXzBI'
import nacl.secret
import base64
import binascii

base64_key = "dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g="
base64_nonce = "/KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1i"
base64_encrypted_value = "/KSIvzD+EfD2ohTDS8YyXWfpzHjVrp1iMQBE3XbIMi0G/BowKduAtkW9uvBwoRDicvmeFfDvaez3xw=="
key = base64.b64decode(base64_key)
nonce = base64.b64decode(base64_nonce)
encrypted_value = base64.b64decode(base64_encrypted_value)

print(key)
print(nonce)
print(encrypted_value)

box = nacl.secret.SecretBox(key)

decrypted_value = box.decrypt(encrypted_value)
print(f"Decrypted value: {decrypted_value}")
b'thisisakeywith32lettersinitfetch'
b'xfcxa4x88xbf0xfex11xf0xf6xa2x14xc3Kxc62]gxe9xccxxd5xaex9db'
b'xfcxa4x88xbf0xfex11xf0xf6xa2x14xc3Kxc62]gxe9xccxxd5xaex9db1x00Dxddvxc82-x06xfcx1a0)xdbx80xb6Exbdxbaxf0pxa1x10xe2rxf9x9ex15xf0xefixecxf7xc7'
Decrypted value: b'NA_CL_SECRET_TOKEN'
# Generated with protoc-gen-openapi
# https://github.com/google/gnostic/tree/master/cmd/protoc-gen-openapi

openapi: 3.0.3
info:
    title: Fetch Backend CTF
    version: 0.0.1
paths:
    /token.v1.TokenService/GetToken:
        post:
            tags:
                - TokenService
            operationId: TokenService_GetToken
            requestBody:
                content:
                    application/json: {}
                required: true
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/GetTokenResponse'
    /token.v1.TokenService/StreamToken:
        post:
            tags:
                - TokenService
            operationId: TokenService_StreamToken
            requestBody:
                content:
                    application/json: {}
                required: true
            responses:
                "200":
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/StreamTokenResponse'
components:
    schemas:
        GetTokenResponse:
            type: object
            properties:
                token:
                    type: string
        StreamTokenResponse:
            type: object
            properties:
                message:
                    type: string
tags:
    - name: TokenService
/token.v1.TokenService/GetToken
/token.v1.TokenService/StreamToken
curl  https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/token.v1.TokenService/GetToken
curl -v -X POST https://prod-backend-ctf.us-east-1.prod-services.fetchrewards.com/token.v1.TokenService/GetToken
Accept-Post: application/connect+json, application/connect+json; charset=utf-8, application/connect+proto, application/grpc, application/grpc+json, application/grpc+json; charset=utf-8, application/grpc+proto, application/grpc-web, application/grpc-web+json, application/grpc-web+json; charset=utf-8, application/grpc-web+proto
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/8-1741771656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/0-1741771658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1741771659.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/0-1741771660.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/6-1741771661.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/0-1741771663.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/10-1741771665.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/8-1741771666.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/10-1741771668.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/10-1741771670.png)