# 暗魂CTF平台-工控-协议分析-writeup

> 原文: https://www.ctfiot.com/198479.html
> ID: 198479

点击蓝字

关注我们

微信搜一搜

暗魂攻防实验室

协议分析

modbus

描述：

黑客通过modbus协议向他的同伙发送了一条秘密信息，通过流量设备我们抓取到了相关的流量包，你能根据流量包找到这条信息么?

exp:

过滤一下 modbus ，追踪第一条数据的 http 流，就能发现 flag

flag为：flag{We1c0meToZXB2023}

异常的流量

描述：

请对提供的流量进行分析，发现可能存在的异常，找出flag，提交格式：flag{xxx}。

exp：

在过滤器中过滤一下 tcp ，追踪一下第一个 tcp 流，选择一下会话往下翻就能发现一串 16 进制，一共有 3 处拼接起来就行，然后我看了一下，我基本每个 tcp 流都会泄露这个串 16 进制，然后进行解码，用 flag{} 包裹就行

flag： flag{EnergyRevolution}

S7Error

描述：

某工厂的工程师发现有一台西门子设备存在资源异常，请分析并找出异常流量的数据包编号。

exp：

过滤器过滤 s7comm，大概了解一下 s7comm 协议，分析 Header 部分，可以看到 Ack_Data 的 Header 中大部分 Error code 是 0x00，说明这种流应该是没有异常的，那我过滤一下不等于 0x00 就行了

Ack_Data：带有返回数据，例如指令是查询内容，返回的就有要查询的东西

s7comm.header.errcod !== 0x00

[工控CTF之协议分析7——OMRON_omron协议-CSDN博客](https://blog.csdn.net/song123sh/article/details/128388409)

omron.command == 0x0102

9fS4Fcr/0vUj2Sf+0sM4+HCxkhBzyMd47I7RuBEc1MkCczJy1UuAX3Hnahevf nu):

def swap_bytes(hex_str): result = []for i inrange(0, len(hex_str), 4): byte1 = hex_str[i:i+2] byte2 = hex_str[i+2:i+4] result.append(byte2 + byte1)return''.join(result)
input_hex ="396653344663722f3076556a3253662b30734d342b4843786b68427a794d64343749375275424563314d6b43637a4a79315575415833486e"output_hex = swap_bytes(input_hex)print(output_hex)
f94ScF/rv0jUS2+fs04MH+xChkzBMy4dI7R7BucEM1CkzcyJU1Au3XnHhave fun:)

5ae1746f6473a56b35616531373436663634373361353662
跟上面一样每两个字节交换一次位置
a51e47f646375ab6

联系微信客服

扫码联系

暗魂攻防实验室

微信搜一搜

暗魂攻防实验室


```
s7comm.header.errcod !== 0x00
```



```
[工控CTF之协议分析7——OMRON_omron协议-CSDN博客](https://blog.csdn.net/song123sh/article/details/128388409)
```



```
omron.command == 0x0102
```



```
9fS4Fcr/0vUj2Sf+0sM4+HCxkhBzyMd47I7RuBEc1MkCczJy1UuAX3Hnahevf nu):
```



```
def swap_bytes(hex_str): result = []for i inrange(0, len(hex_str), 4): byte1 = hex_str[i:i+2] byte2 = hex_str[i+2:i+4] result.append(byte2 + byte1)return''.join(result)
input_hex ="396653344663722f3076556a3253662b30734d342b4843786b68427a794d64343749375275424563314d6b43637a4a79315575415833486e"output_hex = swap_bytes(input_hex)print(output_hex)
f94ScF/rv0jUS2+fs04MH+xChkzBMy4dI7R7BucEM1CkzcyJU1Au3XnHhave fun:)
```



```
5ae1746f6473a56b35616531373436663634373361353662
跟上面一样每两个字节交换一次位置
a51e47f646375ab6
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1723424511.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1723424511.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1723424512.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1723424512.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1723424513.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1723424513.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1723424514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1723424514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1723424515.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1723424515.png)