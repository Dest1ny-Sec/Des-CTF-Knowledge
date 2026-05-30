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

flag{2025-03-15T09:30:01Z}

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

Server：172.30.96.1:8000

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
body = stream_bytes[body_start:body_start + clen]  
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
```



```
tcp contains "ReadRequest"
```



```
dns.qry.name == "ctrlws.factory.local"
```



```
ip.src == 192.168.1.5 && ip.dst == 192.168.1.10 && tcp
```



```
http && ip.src == 192.168.1.5 && ip.dst == 192.168.1.10
```



```
icmp && ip.src == 192.168.1.100 && ip.dst == 192.168.1.10
```



```
udp.port == 161 && ip.src == 192.168.1.5 && ip.dst == 192.168.1.10 && udp
```



```
89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52  
# PNG的固定开头16字节
```



```
open("png.header","wb").write(bytes.fromhex("89504E470D0A1A0A0000000D49484452"))
```



```
bkcrack -C hint.zip -c hint.png -p png.header
```



```
http.request.method == "POST"
```



```
http.request.method == "POST" && http.request.uri contains "shell.php"
```



```
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
body = stream_bytes[body_start:body_start + clen]  
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198030-wxsync-2026-02-8cfa401f64cbbdd0d9e0fd9342e9336e.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198034-wxsync-2026-02-2de1a590a65e7ccca7723a544fbead6c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198036-wxsync-2026-02-a3b2a631b4fad5cd4bac3117074b59e2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198037-wxsync-2026-02-09e63d063664c601b50c8a559d97be76.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198039-wxsync-2026-02-ab2decfb392899836003aadd0fe983c2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198041-wxsync-2026-02-0c91534938c72d730d31b95e158dbb2c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198043-wxsync-2026-02-84ff2bfd4ae62500ffb6384f215da030.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198045-wxsync-2026-02-8f81769e008e3c38289685fff568def0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198046-wxsync-2026-02-aa844a6dc1a94a4d76d34db76d532bad.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770198048-wxsync-2026-02-065edcea57b6853d42f909224c1dfef3.png)