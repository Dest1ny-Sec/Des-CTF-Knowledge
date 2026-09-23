---
title: DataCon2024解题报告WriteUp—网络基础设施安全赛道
contest: DataCon 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags:
- dns
- open-resolver
- isc-bind
- geoip2
- libjson
- features
- attack
attack_chain:
- '题目1: DNS开放解析器识别+攻击利用'
- 9.16/9.18 Bind版本
- 胶水缓存存在/弃用
- 陈旧缓存开启/弃用
- --disable-silent-rules（可选/不可选）
- --enable-backtrace（可选/不可选）
- --enable-shared
- --enable-native-pkcs11
- --with-geoip2 功能失效但可选
- --with-libjson 功能失效但可选
key_payload: '--with-geoip2 --with-libjson  # Bind 配置特征'
one_liner: DataCon2024 DNS开放解析器识别：Bind编译选项+功能版本
lesson: Bind编译参数+版本特征可用于识别DNS开放解析器
quality: medium
full_path: DataCon2024解题报告WriteUp—网络基础设施安全赛道.full.md
meta_path: DataCon2024解题报告WriteUp—网络基础设施安全赛道.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'DataCon2024解题报告WriteUp—网络基础设施安全赛道。DataCon2024 DNS开放解析器识别：Bind编译选项+功能版本。关键路径：题目1: DNS开放解析器识别+攻击利用 → 9.16/9.18 Bind版本 → 胶水缓存存在/弃用。经验：Bind编译参数+版本特征可用于识别DNS开放解析器'
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/224743.html
reasoning_chain:
- DNS 开放解析器识别 + 攻击利用 → 触发点：Bind 编译选项特征指纹
- 假设：Bind 9.16 与 9.18 编译选项差异 → 动作：扫描 --with-geoip2/--with-libjson/--enable-shared/--enable-native-pkcs11
- 观察：胶水缓存 9.16 存在/9.18 弃用；陈旧缓存 9.16 开启/9.18 弃用
- 假设：NS 递归链 a.qwe.com→.asd.com→.victim.com 触发 NS 解析记录 → 动作：查询触发循环
- 观察：长度 2444 的 NS 解析记录 = 放大链证据 → 下一步：设计攻击路径
- 蜜罐模拟 MQTT + MongoDB Wire → 假设：协议解析漏洞 → 动作：custom CONNECT packet payload 注入
- 观察：解析错误导致认证绕过 / Unknown packet type 3 → 下一步：写对抗脚本
failed_attempts:
- 试图只看 Bind 版本号 → 失败：版本相同但编译选项差异导致功能差异
- 试图用普通 DNS flood → 失败：题目需利用 NS 链递归触发放大
key_observations:
- Bind 编译选项（--with-geoip2/--with-libjson）可识别 DNS 开放解析器
- NS 递归链 a→b→c→…→victim 可被攻击者控制触发放大
- MQTT/MongoDB Wire 自定义字段解析错误可绕过认证
- Bind 9.16 与 9.18 胶水/陈旧缓存策略差异是稳定指纹
prerequisites:
- ISC Bind 编译选项与版本特性
- DNS NS 记录递归解析原理
- MQTT CONNECT packet 协议解析
- MongoDB Wire Protocol SCRAM-SHA-1 认证
---
# DataCon2024解题报告WriteUp—网络基础设施安全赛道

> 原文: https://www.ctfiot.com/224743.html
> ID: 224743

2024年11月28日，DataCon2024大数据安全分析竞赛落下帷幕。来自中国科学院信息工程研究所的“ddddns”战队荣获网络基础设施安全赛道冠军，本期一起来看看“ddddns”战队的解题报告。

1 DNS开放解析器识别与攻击利用

特征

9.16

9.18

胶水缓存

存在

弃用

陈旧缓存

开启

弃用

–disable-silent-rules

可选

不可选

–enable-backtrace

可选

不可选

–enable-shared

可选

不可选

–enable-native-pkcs11

可选

不可选

–with-geoip2

功能失效但可选

不可选

–with-libjson

功能失效但可选

不可选

功能失效但可选

不可选

–with-libtool

功能失效但可选

不可选

edns中的最大udp长度

4096

1232

图1.3.1 NS记录查询结果

图1.3.2 攻击方法概览

图1.3.3 查询域名触发a.qwe.com触发的NS解析记录

a.qwe.com.-> ans.victim.com. -> b.qwe.com. -> b.asd.com. -> bns.victim.com. -> c.qwe.com. -> c.asd.com. -> cns.victim.com. -> d.qwe.com. -> d.asd.com. -> dns.victim.com. -> e.qwe.com. -> e.asd.com. -> ens.victim.com. -> f.qwe.com. -> f.asd.com. -> fns.victim.com. -> g.qwe.com. -> g.asd.com. -> gns.victim.com. -> h.qwe.com. -> h.asd.com. -> hns.victim.com. -> i.qwe.com. -> i.asd.com. -> ins.victim.com. -> i1.qwe.com. -> i1.asd.com. -> i1ns.victim.com. -> i2.qwe.com. -> ...i10.asd.com. -> i10.qwe.com. -> i9ns.victim.com. -> i9.asd.com. -> i9.qwe.com. -> i8ns.victim.com. -> i8.asd.com. -> i8.qwe.com. -> i7ns.victim.com. -> i7.asd.com. -> i7.qwe.com. -> i6ns.victim.com. -> i6.asd.com. -> i6.qwe.com. -> i5ns.victim.com. -> i5.asd.com. -> i5.qwe.com. -> i4ns.victim.com. -> i4.asd.com. -> i4.qwe.com. -> i3ns.victim.com. -> i3.asd.com. -> i3.qwe.com. -> i2ns.victim.com. -> i2.asd.com. -> i2.qwe.com. -> i1ns.victim.com. -> i1.asd.com. -> i1.qwe.com. -> ins.victim.com. -> i.asd.com. -> i.qwe.com. -> hns.victim.com. -> h.asd.com. -> h.qwe.com. -> gns.victim.com. -> g.asd.com. -> g.qwe.com. -> fns.victim.com. -> f.asd.com. -> f.qwe.com. -> ens.victim.com. -> e.asd.com. -> e.qwe.com. -> dns.victim.com. -> d.asd.com. -> d.qwe.com. -> cns.victim.com. -> c.asd.com. -> c.qwe.com. -> bns.victim.com. -> b.asd.com. -> b.qwe.com. -> ans.victim.com.

图1.3.4 长度为2444的NS解析记录

a.ieka.com. -> a.yumlly.com. -> a.losers.com. -> a.victim.com. -> b.yumlly.com. -> b.losers.com. -> b.victim.com. -> c.yumlly.com. -> c.losers.com. -> c.victim.com. -> d.yumlly.com. -> d.losers.com. -> d.victim.com. -> d1.yumlly.com. -> d1.losers.com. -> d1.victim.com. -> d2.yumlly.com. -> d2.losers.com. -> d2.victim.com. -> d3.yumlly.com. -> d3.yumlly.com. -> d2.victim.com. -> d2.losers.com. -> d2.yumlly.com. -> d1.victim.com. -> d1.losers.com. -> d1.yumlly.com. -> d.victim.com. -> d.losers.com. -> d.yumlly.com. -> c.victim.com. -> c.losers.com. -> c.yumlly.com. -> b.victim.com. -> b.losers.com. -> b.yumlly.com. -> a.victim.com. -> a.victim.com. -> a.losers.com. -> a.yumlly.com.

图1.3.7 按照数据包长度进行排序

2 蜜罐模拟与对抗

图2.3.1 监听脚本输出

2024-11-17 16:25:40,417 - INFO - Parsed CONNECT packet from ('10.0.33.52', 43903): {'protocol_name': 'MQTT', 'protocol_level': 4, 'connect_flags': 194, 'keep_alive': 60, 'username': '', 'password': 'datacon'} 2024-11-17 16:25:40,417 - WARNING - Authentication failed for ('10.0.33.52', 43903): username=, password=datacon // username解析错误导致认证失败 2024-11-17 16:25:40,417 - INFO - Connection with ('10.0.33.52', 43903) closed

2024-11-17 17:35:51,426 - INFO - Parsed CONNECT packet from ('10.0.33.52', 43453): {'protocol_name': 'MQTT', 'protocol_level': 4, 'connect_flags': 194, 'keep_alive': 60, 'username': 'datacon', 'password': 'datacon'}2024-11-17 17:35:51,426 - INFO - Authentication successful for ('10.0.33.52', 43453)2024-11-17 17:35:52,427 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:35:53,428 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:35:54,430 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:35:55,431 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:36:05,440 - INFO - Connection closed by ('10.0.33.52', 42555)

2024-11-17 20:14:40,416 - INFO - Received SUBSCRIBE packet from ('10.0.33.52', 46603): 820a000100056f7a62706a002024-11-17 20:14:40,416 - INFO - Parsed SUBSCRIBE packet: {'message_id': 1, 'topics': ['ozbpj'], 'qos_values': [0]}2024-11-17 20:14:41,416 - INFO - New connection from ('10.0.33.52', 55815)2024-11-17 20:14:41,416 - INFO - Received CONNECT packet from ('10.0.33.52', 55815): 101e00044d51545404c2003c0000000764617461636f6e000764617461636f6e321400056f7a62706a000148454c4c4f20574f524c442024-11-17 20:14:41,416 - INFO - Authentication successful for ('10.0.33.52', 55815)2024-11-17 20:14:42,418 - INFO - Received PUBLISH packet from ('10.0.33.52', 55815): 321300056f7a62706a00027572676f7369666e63622024-11-17 20:14:42,418 - INFO - Parsed PUBLISH packet: {'topic_name': 'ozbpj', 'qos': 1, 'retain': 0, 'packet_id': 2, 'payload': 'urgosifncb'}2024-11-17 20:14:42,418 - INFO - Sent PUBACK for Packet ID: 2

图2.3.3 MQTT的通信过程

2024-11-18 09:26:01,415 - INFO - Received PUBLISH packet from ('10.0.33.52', 33573): 321400056c716b627a000148454c4c4f20574f524c442024-11-18 09:26:01,415 - INFO - Parsed PUBLISH packet: {'topic_name': 'lqkbz', 'qos': 1, 'retain': 0, 'packet_id': 1, 'payload': 'HELLO WORLD'}2024-11-18 09:26:01,415 - INFO - Sent PUBLISH message to ('10.0.33.52', 41111): 3000056c716b627a48454c4c4f20574f524c442024-11-18 09:26:01,415 - INFO - Sent PUBACK for Packet ID: 1……2024-11-18 09:26:05,419 - INFO - Sent PUBACK for Packet ID: 52024-11-18 09:26:06,421 - WARNING - Unknown packet type 14 from ('10.0.33.52', 33573)2024-11-18 09:26:06,421 - INFO - Connection closed by ('10.0.33.52', 33573)

图2.3.4 PUBLISH报文未能正常解析

图2.3.5 DISCONNECT报文

图2.4.1 MongoDB Wire Protocol中的Query数据包

{ "saslStart": 1, "mechanism": "SCRAM-SHA-1", "payload": binary("n,," + clientFirstMsg), "autoAuthorize": 1}

{ "conversationId": 1, "payload": binary("r=fyko+d2lbbFgONRv9qkxdawLHo+Vgk7qvUOKUwuWLIWg4l/9SraGMHEE,s=rQ9ZY3MntBeuP3E1TDVC4w==,i=10000"), "done": false, "ok": 1}

clientFinalNoPf := "c=biws,r=${serverNonce}"authMessage:="${clientFirstMsg},${serverFirstMsg},${clientFinalNoPf}"clientKey:= Buf().print("Client Key").hmac("SHA-1", saltedPassword)storedKey:= clientKey.toDigest("SHA-1")clientSignature := Buf().print(authMessage).hmac("SHA-1", storedKey)clientProof:= xor(clientKey, clientSignature)clientFinal:= "${clientFinalNoPf},p=${clientProof.toBase64}"

{ "saslContinue": 1, "conversationId": conversationId, "payload": binary(clientFinal)}

{ "conversationId": 1, "payload": binary("v=UMWeI25JD1yNYZRMpZ4VHvhZ9e0="), "done": false, "ok": 1}

图2.4.1 insert操作数据包

图2.4.2 find操作数据包

END


```
a.qwe.com.-> ans.victim.com. -> b.qwe.com. -> b.asd.com. -> bns.victim.com. -> c.qwe.com. -> c.asd.com. -> cns.victim.com. -> d.qwe.com. -> d.asd.com. -> dns.victim.com. -> e.qwe.com. -> e.asd.com. -> ens.victim.com. -> f.qwe.com. -> f.asd.com. -> fns.victim.com. -> g.qwe.com. -> g.asd.com. -> gns.victim.com. -> h.qwe.com. -> h.asd.com. -> hns.victim.com. -> i.qwe.com. -> i.asd.com. -> ins.victim.com. -> i1.qwe.com. -> i1.asd.com. -> i1ns.victim.com. -> i2.qwe.com. -> ...i10.asd.com. -> i10.qwe.com. -> i9ns.victim.com. -> i9.asd.com. -> i9.qwe.com. -> i8ns.victim.com. -> i8.asd.com. -> i8.qwe.com. -> i7ns.victim.com. -> i7.asd.com. -> i7.qwe.com. -> i6ns.victim.com. -> i6.asd.com. -> i6.qwe.com. -> i5ns.victim.com. -> i5.asd.com. -> i5.qwe.com. -> i4ns.victim.com. -> i4.asd.com. -> i4.qwe.com. -> i3ns.victim.com. -> i3.asd.com. -> i3.qwe.com. -> i2ns.victim.com. -> i2.asd.com. -> i2.qwe.com. -> i1ns.victim.com. -> i1.asd.com. -> i1.qwe.com. -> ins.victim.com. -> i.asd.com. -> i.qwe.com. -> hns.victim.com. -> h.asd.com. -> h.qwe.com. -> gns.victim.com. -> g.asd.com. -> g.qwe.com. -> fns.victim.com. -> f.asd.com. -> f.qwe.com. -> ens.victim.com. -> e.asd.com. -> e.qwe.com. -> dns.victim.com. -> d.asd.com. -> d.qwe.com. -> cns.victim.com. -> c.asd.com. -> c.qwe.com. -> bns.victim.com. -> b.asd.com. -> b.qwe.com. -> ans.victim.com.
a.ieka.com. -> a.yumlly.com. -> a.losers.com. -> a.victim.com. -> b.yumlly.com. -> b.losers.com. -> b.victim.com. -> c.yumlly.com. -> c.losers.com. -> c.victim.com. -> d.yumlly.com. -> d.losers.com. -> d.victim.com. -> d1.yumlly.com. -> d1.losers.com. -> d1.victim.com. -> d2.yumlly.com. -> d2.losers.com. -> d2.victim.com. -> d3.yumlly.com. -> d3.yumlly.com. -> d2.victim.com. -> d2.losers.com. -> d2.yumlly.com. -> d1.victim.com. -> d1.losers.com. -> d1.yumlly.com. -> d.victim.com. -> d.losers.com. -> d.yumlly.com. -> c.victim.com. -> c.losers.com. -> c.yumlly.com. -> b.victim.com. -> b.losers.com. -> b.yumlly.com. -> a.victim.com. -> a.victim.com. -> a.losers.com. -> a.yumlly.com.
2024-11-17 16:25:40,417 - INFO - Parsed CONNECT packet from ('10.0.33.52', 43903): {'protocol_name': 'MQTT', 'protocol_level': 4, 'connect_flags': 194, 'keep_alive': 60, 'username': '', 'password': 'datacon'} 2024-11-17 16:25:40,417 - WARNING - Authentication failed for ('10.0.33.52', 43903): username=, password=datacon // username解析错误导致认证失败 2024-11-17 16:25:40,417 - INFO - Connection with ('10.0.33.52', 43903) closed
2024-11-17 17:35:51,426 - INFO - Parsed CONNECT packet from ('10.0.33.52', 43453): {'protocol_name': 'MQTT', 'protocol_level': 4, 'connect_flags': 194, 'keep_alive': 60, 'username': 'datacon', 'password': 'datacon'}2024-11-17 17:35:51,426 - INFO - Authentication successful for ('10.0.33.52', 43453)2024-11-17 17:35:52,427 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:35:53,428 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:35:54,430 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:35:55,431 - WARNING - Unknown packet type 3 from ('10.0.33.52', 43453)2024-11-17 17:36:05,440 - INFO - Connection closed by ('10.0.33.52', 42555)
2024-11-17 20:14:40,416 - INFO - Received SUBSCRIBE packet from ('10.0.33.52', 46603): 820a000100056f7a62706a002024-11-17 20:14:40,416 - INFO - Parsed SUBSCRIBE packet: {'message_id': 1, 'topics': ['ozbpj'], 'qos_values': [0]}2024-11-17 20:14:41,416 - INFO - New connection from ('10.0.33.52', 55815)2024-11-17 20:14:41,416 - INFO - Received CONNECT packet from ('10.0.33.52', 55815): 101e00044d51545404c2003c0000000764617461636f6e000764617461636f6e321400056f7a62706a000148454c4c4f20574f524c442024-11-17 20:14:41,416 - INFO - Authentication successful for ('10.0.33.52', 55815)2024-11-17 20:14:42,418 - INFO - Received PUBLISH packet from ('10.0.33.52', 55815): 321300056f7a62706a00027572676f7369666e63622024-11-17 20:14:42,418 - INFO - Parsed PUBLISH packet: {'topic_name': 'ozbpj', 'qos': 1, 'retain': 0, 'packet_id': 2, 'payload': 'urgosifncb'}2024-11-17 20:14:42,418 - INFO - Sent PUBACK for Packet ID: 2
2024-11-18 09:26:01,415 - INFO - Received PUBLISH packet from ('10.0.33.52', 33573): 321400056c716b627a000148454c4c4f20574f524c442024-11-18 09:26:01,415 - INFO - Parsed PUBLISH packet: {'topic_name': 'lqkbz', 'qos': 1, 'retain': 0, 'packet_id': 1, 'payload': 'HELLO WORLD'}2024-11-18 09:26:01,415 - INFO - Sent PUBLISH message to ('10.0.33.52', 41111): 3000056c716b627a48454c4c4f20574f524c442024-11-18 09:26:01,415 - INFO - Sent PUBACK for Packet ID: 1……2024-11-18 09:26:05,419 - INFO - Sent PUBACK for Packet ID: 52024-11-18 09:26:06,421 - WARNING - Unknown packet type 14 from ('10.0.33.52', 33573)2024-11-18 09:26:06,421 - INFO - Connection closed by ('10.0.33.52', 33573)
{ "saslStart": 1, "mechanism": "SCRAM-SHA-1", "payload": binary("n,," + clientFirstMsg), "autoAuthorize": 1}
{ "conversationId": 1, "payload": binary("r=fyko+d2lbbFgONRv9qkxdawLHo+Vgk7qvUOKUwuWLIWg4l/9SraGMHEE,s=rQ9ZY3MntBeuP3E1TDVC4w==,i=10000"), "done": false, "ok": 1}
clientFinalNoPf := "c=biws,r=${serverNonce}"authMessage:="${clientFirstMsg},${serverFirstMsg},${clientFinalNoPf}"clientKey:= Buf().print("Client Key").hmac("SHA-1", saltedPassword)storedKey:= clientKey.toDigest("SHA-1")clientSignature := Buf().print(authMessage).hmac("SHA-1", storedKey)clientProof:= xor(clientKey, clientSignature)clientFinal:= "${clientFinalNoPf},p=${clientProof.toBase64}"
{ "saslContinue": 1, "conversationId": conversationId, "payload": binary(clientFinal)}
{ "conversationId": 1, "payload": binary("v=UMWeI25JD1yNYZRMpZ4VHvhZ9e0="), "done": false, "ok": 1}
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