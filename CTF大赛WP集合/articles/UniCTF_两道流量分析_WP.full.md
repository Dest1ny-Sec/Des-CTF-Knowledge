---
title: UniCTF 两道流量分析 WP
contest: UniCTF (YunSee团队)
year: 2025
difficulty: medium
vuln_type: forensic_traffic
tags:
- modbus
- opc_ua
- dns
- http
- icmp
- snmp
- bkcrack
- xor_key_recover
- gzip_known_plaintext
- tcp_reassemble
- webshell_decrypt
- scada_forensic
attack_chain: 工厂应急响应 (7 任务):Modbus 0x05/ff00 → OPC UA ReadRequest → DNS 解析 → TCP 首连时间 → HTTP Host/URI → ICMP seq=0x0123 → SNMP OID → BlueBreath:TCP 8000 端口 bkcrack PNG 头明文攻击 → POST /uploads/shell.php → gzip 1f8b08 已知头推 XOR key → 解密 webshell 流量
key_payload: modbus.func_code==5 && modbus.data==ff:00 / bkcrack -C hint.zip -c hint.png -p png.header / KEY=b"dc3ef5ff0c670152" (16-byte XOR)
one_liner: YunSee 团队招新流量分析题，工厂应急响应 7 个 flag + BlueBreath XOR 加密 webshell 完整解密，HTTP+Modbus+OPC UA+SNMP 协议全接触。
lesson: Webshell 加密流量特征：gzip 头 1f 8b 08 是常见的"先压缩再异或"模板，可用已知明文反推 XOR key 头 9 字节再爆破。
quality: high
full_path: UniCTF_两道流量分析_WP.full.md
meta_path: UniCTF_两道流量分析_WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: UniCTF 两道流量分析 WP。YunSee 团队招新流量分析题，工厂应急响应 7 个 flag + BlueBreath XOR 加密 webshell 完整解密，HTTP+Modbus+OPC UA+SNMP 协议全接触。。经验：Webshell 加密流量特征：gzip 头 1f 8b 08 是常见的"先压缩再异或"模板，可用已知明文反推 XO...
category: forensic
subcategory: network_forensics
tools_used:
- C
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/296062.html
reasoning_chain:
- 触发点：题目'工厂应急响应挑战赛'7 个子任务 + BlueBreath webshell 加密流量 → 假设：工控 + HTTP 加密流量组合
- 任务 1：modbus.func_code == 5 && modbus.data == ff:00 → 假设：阀门打开是功能码 5 + FF00 → 观察：transaction_id=0x3c4d, Reference Number=0x0015 → flag{0x3c4d_0x05_0x0015}
- 任务 2：tcp contains 'ReadRequest' → OPC UA ReadRequest 过滤 → 假设：NodeId 是 ns=2;s=Valve/Status
- 任务 3：dns.qry.name == 'ctrlws.factory.local' → DNS 解析 → flag{192.168.1.10}
- 任务 4：ip.src==192.168.1.5 && ip.dst==192.168.1.10 → TCP 首连时间 → flag{2025-03-15T09:30:01Z}
- 任务 5：http && ip.src==192.168.1.5 && ip.dst==192.168.1.10 → Host/URI → flag{ctrlws.factory.local_/api/status}
- 任务 6：icmp && ip.src==192.168.1.100 → BE 大端序序列号 → flag{0x0123}
- 任务 7：udp.port == 161 → SNMP Get OID → flag{1.3.6.1.4.1.9999...}
- BlueBreath：TCP 8000 端口 webshell → bkcrack -C hint.zip -c hint.png -p png.header 已知明文攻击 → 假设：解压出 hint.png + flag.zip
- 动作：POST /uploads/shell.php 加密数据 → gzip 头 1f8b08 已知 → XOR 反推 key 前 9 字节 → AI 补全 16 字节 KEY=dc3ef5ff0c670152
- 动作：python dpkt + TCP seq 重组 + XOR 解密 → flag 解出
failed_attempts:
- 任务 1 试图按 IP 配对找阀门打开 → 失败：必须按 modbus.func_code + data 双条件过滤
- BlueBreath 试图不解密直接看 POST body 文本 → 失败：webshell 数据 XOR+gzip 加密
- 任务 6 试图读 LE 小端序 → 失败：协议是大端序 BE 才正确
key_observations:
- Webshell 加密流量特征：gzip 头 1f 8b 08 是常见的'先压缩再异或'模板，可用已知明文反推 XOR key
- Modbus 打开阀门 = func_code 5 + data FF00 是工控 SCADA 标准操作码
- OPC UA ReadRequest 第一个包通常就是读取的目标 NodeId
- ICMP 序列号字段按协议大端序 BE 解析，Wireshark 默认显示 LE 易踩坑
- SNMP 默认端口 161 是 UDP，OID 是 dot-decimal 数字层级标识
prerequisites:
- Wireshark/tshark 显示过滤器语法（modbus / opcua / dns / http / icmp / snmp）
- Modbus / OPC UA / MMS 工控协议基础
- bkcrack 已知明文攻击（PNG 头 16 字节固定）
- TCP 字节流重组（按 seq 排序 + 处理重传）
- XOR 加密原理（已知明文反推 key）
---
# UniCTF 两道流量分析 WP

> 原文: https://www.ctfiot.com/296062.html
> ID: 296062

YunSee团队招新

为了进一步壮大团队实力，我们现面向全网招募密码学、AI 安全、逆向方向的师傅 加入交流。只要你愿意分享、热爱探索、喜欢和同好一起“碰撞火花”，我们都热烈欢迎！

招新要求：

具有 CTF 比赛经验者优先，且在相关赛事中取得优异成绩者将予以重点考虑；

优先考虑能定制和训练 CTF 解题 Agent 的选手

当然，我们也十分欢迎愿意一起交流、组队打 CTF 的师傅加入我们的“魔丸”交流群，在这里共同探讨技术、相互学习进步。

联系方式：

简历发邮箱：achenc1013@gmali.com

魔丸交流群：1034296865

工厂应急响应挑战赛

任务 1：谁把阀门打开了？

找到 Modbus 打开阀门指令的相关信息。

打开阀门操作应该对应功能码是0x05，而打开操作的data通常为0xFF00

modbus.func_code == 5 && modbus.data == ff:00

fig:

transaction_id = 0x3c4d
fig:

function_code = 0x05
fig:

coil_address找Reference Number即可

Reference Number = 0x0015
fig:

flag{0x3c4d_0x05_0x0015}

任务 2：被读取的 NodeId

找到通过 OPC UA 协议读取的 NodeId。

读取请求我们直接针对ReadRequest进行模糊筛选

tcp contains "ReadRequest"

fig:

第一个包就是
fig:

flag{ns=2;s=Valve/Status}

任务 3：控制站域名解析结果

找出控制站域名 ctrlws.factory.local 的解析 IP。

dns.qry.name == "ctrlws.factory.local"

fig:

可以看到A地址域名解析的IP
fig:

flag{192.168.1.10}

任务 4：连接建立时间

确定SCADA（源：192.168.1.5）到控制站（目的：192.168.1.10）上首个成功发起的时间点(UTC)。

ip.src == 192.168.1.5 && ip.dst == 192.168.1.10 && tcp

fig:
fig:

flag{2025-03-15T09:30:
01Z}

任务 5：HTTP 请求痕迹

提取 SCADA 对控制站发起的 HTTP 请求的 Host 与 URI。

已知SCADA 系统（192.168.1.5）控制站（192.168.1.10）

http && ip.src == 192.168.1.5 && ip.dst == 192.168.1.10

fig:
fig:
fig:

flag{ctrlws.factory.local_/api/status}

任务 6：ICMP Echo Request 序列号

攻击者（192.168.1.100）对控制站发起了 ICMP Echo Request（ping）。找出该 ICMP 请求的序列号（Sequence Number）。

直接针对icmp报文进行过滤

icmp && ip.src == 192.168.1.100 && ip.dst == 192.168.1.10

fig:

BE表示大端序，LE表示小端序。而协议是按照大端序发的，所以BE才是正确的序列号
fig:
fig:

flag{0x0123}

任务 7：SNMP Get 请求的 OID

SCADA 对控制站发起了 SNMP Get 请求。找出该请求查询的 OID（Object Identifier）。

SNMP的默认端口是161

udp.port == 161 && ip.src == 192.168.1.5 && ip.dst == 192.168.1.10 && udp

fig:

追踪UDP流
fig:
fig:

BlueBreath

在统计会话中TCP协议频次最高的端口就是：8000

Server：172.30.96.1:
8000

Client：192.168.80.129
fig:

NetA自动下载了一个压缩包，但是解压需要密码
fig:

已知是一个png文件，尝试使用bkcrack明文破解

89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52  
# PNG的固定开头16字节

写一个明文文件

open("png.header","wb").write(bytes.fromhex("89504E470D0A1A0A0000000D49484452"))

fig:

bkcrack -C hint.zip -c hint.png -p png.header

fig:
fig:

这图片我也不清楚有啥用，没啥可用的信息

先来到wireshark 筛选http POST请求

http.request.method == "POST"

fig:

发现上传了shell.php可疑文件
fig:

像二进制被加密数据

筛选所有包含shell.php 的流

http.request.method == "POST" && http.request.uri contains "shell.php"

fig:

前三个流一大片乱码，怀疑是后门的加密源码

从第四个流开始，这里的传输的加密数据好似哥斯拉那种加密shell后门，请求的命令以及执行结果回显
fig:

数据的开头都是：7b e8 3b 65 66 35 66 66 30 …
fig:

webshell 常见做法是“先压缩再混淆”，于是尝试以 gzip 固定头 1f 8b 08 00 00 00 00 00 00 作为已知明文，利用 C XOR P 反推出前 9 字节密钥
fig:

得到的是可显示的字符串，说明这是密钥的一部分

这里我也不清楚key的长度以及爆破出完整的key，就求助AI了
fig:

拿到完整的key之后，写个解密脚本将加密webshell解密

import re, gzip, socket  
import dpkt  

PCAP = "BlueBreath.pcapng"
KEY = b"dc3ef5ff0c670152"# 16-byte XOR key  

def reassemble(segs):
"""按 TCP seq 重组（处理重传/重叠）"""
ifnot segs:  
returnb""
segs = sorted(segs, key=lambda x: x[0])  
base = segs[0][0]  
out = bytearray()  
cur = base  
for seq, data in segs:  
if seq < cur:  
overlap = cur - seq  
if overlap >= len(data):  
continue
data = data[overlap:]  
seq = cur  
if seq > cur:  
out.extend(b"x00" * (seq - cur))  
cur = seq  
out.extend(data)  
cur += len(data)  
return bytes(out)  

def parse_http_bodies(stream_bytes, is_request=True):
"""从 TCP 字节流里按 Content-Length 拆 HTTP 消息 body"""
res = []  
i = 0
whileTrue:  
if is_request:  
j = stream_bytes.find(b"POST ", i)  
else:  
j = stream_bytes.find(b"HTTP/1.", i)  
if j == -1:  
break
k = stream_bytes.find(b"rnrn", j)  
if k == -1:  
break
header = stream_bytes[j:k].decode("iso-8859-1", errors="ignore")  
m = re.search(r"Content-Length:s*(d+)", header, re.I)  
clen = int(m.group(1)) if m else0
body_start = k + 4
body = stream_bytes[body_start:
body_start + clen]  
res.append((header.split("rn", 1)[0], header, body))  
i = body_start + clen  
return res  

def xor_dec(data, key):
return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))  

def main():
# 收集所有 8000 端口 TCP 分段：按 (client_ip, client_port, server_ip, 8000) 归一化成一个连接  
streams = {} # key -> {'c2s':[(seq,data)], 's2c':[(seq,data)]}  

with open(PCAP, "rb") as f:  
pcap = dpkt.pcapng.Reader(f)  
for ts, buf in pcap:  
try:  
eth = dpkt.ethernet.Ethernet(buf)  
ip = eth.data  
ifnot isinstance(ip, dpkt.ip.IP):  
continue
tcp = ip.data  
ifnot isinstance(tcp, dpkt.tcp.TCP) ornot tcp.data:  
continue

src = socket.inet_ntoa(ip.src)  
dst = socket.inet_ntoa(ip.dst)  

if tcp.dport == 8000:  
key = (src, tcp.sport, dst, 8000)  
streams.setdefault(key, {"c2s": [], "s2c": []})  
streams[key]["c2s"].append((tcp.seq, tcp.data))  
elif tcp.sport == 8000:  
key = (dst, tcp.dport, src, 8000)  
streams.setdefault(key, {"c2s": [], "s2c": []})  
streams[key]["s2c"].append((tcp.seq, tcp.data))  
except:  
pass

# 找出包含 /uploads/shell.php 的连接并解密  
for key, d in streams.items():  
c2s = reassemble(d["c2s"])  
ifb"POST /uploads/shell.php"notin c2s:  
continue
s2c = reassemble(d["s2c"])  

reqs = parse_http_bodies(c2s, is_request=True)  
resps = parse_http_bodies(s2c, is_request=False)  

print("n=== shell conn:", key, "===")  
for first, header, body in reqs:  
if"/uploads/shell.php"notin first:  
continue
ifnot body:  
continue
p = xor_dec(body, KEY)  
try:  
out = gzip.decompress(p)  
print("[REQ]", out.decode(errors="ignore"))  
except Exception as e:  
print("[REQ] decrypt fail:", e)  

for first, header, body in resps:  
ifnot body:  
continue
p = xor_dec(body, KEY)  
try:  
out = gzip.decompress(p)  
print("[RESP]", out.decode(errors="ignore"))  
except Exception as e:  
print("[RESP] decrypt fail:", e)  

if __name__ == "__main__":  
main()

fig:

加入我们


```
modbus.func_code == 5 && modbus.data == ff:00
tcp contains "ReadRequest"
dns.qry.name == "ctrlws.factory.local"
ip.src == 192.168.1.5 && ip.dst == 192.168.1.10 && tcp
http && ip.src == 192.168.1.5 && ip.dst == 192.168.1.10
icmp && ip.src == 192.168.1.100 && ip.dst == 192.168.1.10
udp.port == 161 && ip.src == 192.168.1.5 && ip.dst == 192.168.1.10 && udp
89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52  
# PNG的固定开头16字节
open("png.header","wb").write(bytes.fromhex("89504E470D0A1A0A0000000D49484452"))
bkcrack -C hint.zip -c hint.png -p png.header
http.request.method == "POST"
http.request.method == "POST" && http.request.uri contains "shell.php"
import re, gzip, socket  
import dpkt  

PCAP = "BlueBreath.pcapng"
KEY = b"dc3ef5ff0c670152"# 16-byte XOR key  

def reassemble(segs):
"""按 TCP seq 重组（处理重传/重叠）"""
ifnot segs:  
returnb""
segs = sorted(segs, key=lambda x: x[0])  
base = segs[0][0]  
out = bytearray()  
cur = base  
for seq, data in segs:  
if seq < cur:  
overlap = cur - seq  
if overlap >= len(data):  
continue
data = data[overlap:]  
seq = cur  
if seq > cur:  
out.extend(b"x00" * (seq - cur))  
cur = seq  
out.extend(data)  
cur += len(data)  
return bytes(out)  

def parse_http_bodies(stream_bytes, is_request=True):
"""从 TCP 字节流里按 Content-Length 拆 HTTP 消息 body"""
res = []  
i = 0
whileTrue:  
if is_request:  
j = stream_bytes.find(b"POST ", i)  
else:  
j = stream_bytes.find(b"HTTP/1.", i)  
if j == -1:  
break
k = stream_bytes.find(b"rnrn", j)  
if k == -1:  
break
header = stream_bytes[j:k].decode("iso-8859-1", errors="ignore")  
m = re.search(r"Content-Length:s*(d+)", header, re.I)  
clen = int(m.group(1)) if m else0
body_start = k + 4
body = stream_bytes[body_start:
body_start + clen]  
res.append((header.split("rn", 1)[0], header, body))  
i = body_start + clen  
return res  

def xor_dec(data, key):
return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))  

def main():
# 收集所有 8000 端口 TCP 分段：按 (client_ip, client_port, server_ip, 8000) 归一化成一个连接  
streams = {} # key -> {'c2s':[(seq,data)], 's2c':[(seq,data)]}  

with open(PCAP, "rb") as f:  
pcap = dpkt.pcapng.Reader(f)  
for ts, buf in pcap:  
try:  
eth = dpkt.ethernet.Ethernet(buf)  
ip = eth.data  
ifnot isinstance(ip, dpkt.ip.IP):  
continue
tcp = ip.data  
ifnot isinstance(tcp, dpkt.tcp.TCP) ornot tcp.data:  
continue

src = socket.inet_ntoa(ip.src)  
dst = socket.inet_ntoa(ip.dst)  

if tcp.dport == 8000:  
key = (src, tcp.sport, dst, 8000)  
streams.setdefault(key, {"c2s": [], "s2c": []})  
streams[key]["c2s"].append((tcp.seq, tcp.data))  
elif tcp.sport == 8000:  
key = (dst, tcp.dport, src, 8000)  
streams.setdefault(key, {"c2s": [], "s2c": []})  
streams[key]["s2c"].append((tcp.seq, tcp.data))  
except:  
pass

# 找出包含 /uploads/shell.php 的连接并解密  
for key, d in streams.items():  
c2s = reassemble(d["c2s"])  
ifb"POST /uploads/shell.php"notin c2s:  
continue
s2c = reassemble(d["s2c"])  

reqs = parse_http_bodies(c2s, is_request=True)  
resps = parse_http_bodies(s2c, is_request=False)  

print("n=== shell conn:", key, "===")  
for first, header, body in reqs:  
if"/uploads/shell.php"notin first:  
continue
ifnot body:  
continue
p = xor_dec(body, KEY)  
try:  
out = gzip.decompress(p)  
print("[REQ]", out.decode(errors="ignore"))  
except Exception as e:  
print("[REQ] decrypt fail:", e)  

for first, header, body in resps:  
ifnot body:  
continue
p = xor_dec(body, KEY)  
try:  
out = gzip.decompress(p)  
print("[RESP]", out.decode(errors="ignore"))  
except Exception as e:  
print("[RESP] decrypt fail:", e)  

if __name__ == "__main__":  
main()
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