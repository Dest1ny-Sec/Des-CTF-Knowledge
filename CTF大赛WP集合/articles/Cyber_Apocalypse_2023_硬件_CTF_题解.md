# Cyber Apocalypse 2023 硬件 CTF 题解

> 原文: https://www.ctfiot.com/222634.html
> ID: 222634

AI 速读

1、Timed Transmission

通过分析逻辑分析仪的波形图，识别出波形组成的文字，得到 flag

2、Critical Flight

解析 Gerber 文件，找到隐藏的字符串，拼接成 flag

3、Debug

通过分析 UART 通信的波特率，解码得到 flag

4、HM74

分析 Verilog 代码，对干扰的数据进行汉明码解码，通过统计分析得到 flag

5、Secret-Code

结合逻辑分析仪记录和 Gerber 文件，分析数码管的显示内容，通过通道与数码管的连接关系，还原出数码管显示的字符，最终得到 flag

Timed Transmission

Critical Flight

https://viewer.digipcba.com/viewer/
https://www.pcbway.com/project/OnlineGerberViewer.html

debug

HM74

module encoder(
    input [3:0] data_in,
    output [6:0] ham_out
    );

    wire p0, p1, p2;

    assign p0 = data_in[3] ^ data_in[2] ^ data_in[0];
    assign p1 = data_in[3] ^ data_in[1] ^ data_in[0];
    assign p2 = data_in[2] ^ data_in[1] ^ data_in[0];
    
    assign ham_out = {p0, p1, data_in[3], p2, data_in[2], data_in[1], data_in[0]};
endmodule

module main;
    wire[3:0] data_in = 5;
    wire[6:0] ham_out;

    encoder en(data_in, ham_out);

    initialbegin
        #10;
        $display("%b", ham_out);
    end
endmodule

As you venture further into the depths of the tomb, your communication with your team becomes increasingly disrupted by noise. Despite their attempts to encode the data packets, the errors persist and prove to be a formidable obstacle. Fortunately, you have the exact Verilog module used in both ends of the communication. Will you be able to discover a solution to overcome the communication disruptions and proceed with your mission?当你进一步冒险进入坟墓深处时，你与团队的沟通会越来越受到噪音的干扰。尽管他们尝试对数据包进行编码，但错误仍然存在，并被证明是一个巨大的障碍。幸运的是，您在通信两端都使用了完全相同的 Verilog 模块。您能否找到解决方案来克服通信中断并继续执行您的任务？

def bit_check(data):
    p0 = int(data[0])
    p1 = int(data[1])
    data_in3 = int(data[2])
    p2 = int(data[3])
    data_in2 = int(data[4])
    data_in1 = int(data[5])
    data_in0 = int(data[6])
    p0_error = False
    p1_error = False
    p2_error = False
    if (p0 != data_in3 ^ data_in2 ^ data_in0):
        p0_error = True
    if (p1 != data_in3 ^ data_in1 ^ data_in0):
        p1_error = True
    if (p2 != data_in2 ^ data_in1 ^ data_in0):
        p2_error = True
    if (p0_error == True) and (p1_error == True) and (p2_error == True):  # 如果三个都错了，说明data_in0错了
        data_in0 = int(not data_in0)
    if (p0_error == True) and (p1_error == True) and (p2_error == False): # 如果p2是对的，说明data_in3错了
        data_in3 = int(not data_in3)
    if (p0_error == True) and (p1_error == False) and (p2_error == True): # 如果p1是对的，说明data_in2错了
        data_in2 = int(not data_in2)
    if (p0_error == False) and (p1_error == True) and (p2_error == True): # 如果p0是对的，说明data_in1错了
        data_in1 = int(not data_in1)
    return str(data_in3)+str(data_in2)+str(data_in1)+str(data_in0)

file = open("signals.txt",'r').readlines()

def bit_check(data):
    p0 = int(data[0])
    p1 = int(data[1])
    data_in3 = int(data[2])
    p2 = int(data[3])
    data_in2 = int(data[4])
    data_in1 = int(data[5])
    data_in0 = int(data[6])
    p0_error = False
    p1_error = False
    p2_error = False
    if (p0 != data_in3 ^ data_in2 ^ data_in0):
        p0_error = True
    if (p1 != data_in3 ^ data_in1 ^ data_in0):
        p1_error = True
    if (p2 != data_in2 ^ data_in1 ^ data_in0):
        p2_error = True
    if (p0_error == True) and (p1_error == True) and (p2_error == True): # 如果三个都错了，说明data_in0错了
        data_in0 = int(not data_in0)
    if (p0_error == True) and (p1_error == True) and (p2_error == False): # 如果p2是对的，说明data_in3错了
        data_in3 = int(not data_in3)
    if (p0_error == True) and (p1_error == False) and (p2_error == True): # 如果p1是对的，说明data_in2错了
        data_in2 = int(not data_in2)
    if (p0_error == False) and (p1_error == True) and (p2_error == True): # 如果p0是对的，说明data_in1错了
        data_in1 = int(not data_in1)
    data = str(data_in3)+str(data_in2)+str(data_in1)+str(data_in0)
    return data

outputs = [] # 包含所有输出的列表

for line in file:
    line = line[10:].strip()
    s = ''
    for i in range(0,len(line),7):
        data = line[i:i+7]
        data_checked = bit_check(data)
        my_data = hex(int(data_checked,2))[2:]
        s += my_data
    try:
        outputs.append(bytes.fromhex(s))
        print(bytes.fromhex(s))
    except:
        pass

char_counts = {} # 初始化一个字典，用于存储每个位置上的字符出现次数

for output in outputs:  # 遍历每个输出
    s = output.decode('latin1')  # 将字节串转换为字符串

    for i, char in enumerate(s):   # 遍历字符串中的每个字符和它们的位置
        if i notin char_counts:
            char_counts[i] = {}    # 如果位置不在字典中，添加进去

        if char in char_counts[i]:  # 如果字符已经在字典中，增加它的计数，否则设置为1
            char_counts[i][char] += 1
        else:
            char_counts[i][char] = 1

most_common_chars = ''
for i in range(len(char_counts)):  # 找出每个位置上出现次数最多的字符
    most_common_chars += max(char_counts[i], key=char_counts[i].get)

print(most_common_chars)  # 打印结果

Secret-Code

e <-> channel 6
d <-> channel 0
c <-> channel 4
dp <-> channel 1
b <-> channel 5
a <-> channel 2
f <-> channel 7
g <-> channel 3

4854427b70307733325F63306d33355F6632306d5F77313768316E4021237d


```
https://viewer.digipcba.com/viewer/
https://www.pcbway.com/project/OnlineGerberViewer.html
```



```
module encoder(
    input [3:0] data_in,
    output [6:0] ham_out
    );

    wire p0, p1, p2;

    assign p0 = data_in[3] ^ data_in[2] ^ data_in[0];
    assign p1 = data_in[3] ^ data_in[1] ^ data_in[0];
    assign p2 = data_in[2] ^ data_in[1] ^ data_in[0];
    
    assign ham_out = {p0, p1, data_in[3], p2, data_in[2], data_in[1], data_in[0]};
endmodule

module main;
    wire[3:0] data_in = 5;
    wire[6:0] ham_out;

    encoder en(data_in, ham_out);

    initialbegin
        #10;
        $display("%b", ham_out);
    end
endmodule
```



```
def bit_check(data):
    p0 = int(data[0])
    p1 = int(data[1])
    data_in3 = int(data[2])
    p2 = int(data[3])
    data_in2 = int(data[4])
    data_in1 = int(data[5])
    data_in0 = int(data[6])
    p0_error = False
    p1_error = False
    p2_error = False
    if (p0 != data_in3 ^ data_in2 ^ data_in0):
        p0_error = True
    if (p1 != data_in3 ^ data_in1 ^ data_in0):
        p1_error = True
    if (p2 != data_in2 ^ data_in1 ^ data_in0):
        p2_error = True
    if (p0_error == True) and (p1_error == True) and (p2_error == True):  # 如果三个都错了，说明data_in0错了
        data_in0 = int(not data_in0)
    if (p0_error == True) and (p1_error == True) and (p2_error == False): # 如果p2是对的，说明data_in3错了
        data_in3 = int(not data_in3)
    if (p0_error == True) and (p1_error == False) and (p2_error == True): # 如果p1是对的，说明data_in2错了
        data_in2 = int(not data_in2)
    if (p0_error == False) and (p1_error == True) and (p2_error == True): # 如果p0是对的，说明data_in1错了
        data_in1 = int(not data_in1)
    return str(data_in3)+str(data_in2)+str(data_in1)+str(data_in0)
```



```
file = open("signals.txt",'r').readlines()

def bit_check(data):
    p0 = int(data[0])
    p1 = int(data[1])
    data_in3 = int(data[2])
    p2 = int(data[3])
    data_in2 = int(data[4])
    data_in1 = int(data[5])
    data_in0 = int(data[6])
    p0_error = False
    p1_error = False
    p2_error = False
    if (p0 != data_in3 ^ data_in2 ^ data_in0):
        p0_error = True
    if (p1 != data_in3 ^ data_in1 ^ data_in0):
        p1_error = True
    if (p2 != data_in2 ^ data_in1 ^ data_in0):
        p2_error = True
    if (p0_error == True) and (p1_error == True) and (p2_error == True): # 如果三个都错了，说明data_in0错了
        data_in0 = int(not data_in0)
    if (p0_error == True) and (p1_error == True) and (p2_error == False): # 如果p2是对的，说明data_in3错了
        data_in3 = int(not data_in3)
    if (p0_error == True) and (p1_error == False) and (p2_error == True): # 如果p1是对的，说明data_in2错了
        data_in2 = int(not data_in2)
    if (p0_error == False) and (p1_error == True) and (p2_error == True): # 如果p0是对的，说明data_in1错了
        data_in1 = int(not data_in1)
    data = str(data_in3)+str(data_in2)+str(data_in1)+str(data_in0)
    return data

outputs = [] # 包含所有输出的列表

for line in file:
    line = line[10:].strip()
    s = ''
    for i in range(0,len(line),7):
        data = line[i:i+7]
        data_checked = bit_check(data)
        my_data = hex(int(data_checked,2))[2:]
        s += my_data
    try:
        outputs.append(bytes.fromhex(s))
        print(bytes.fromhex(s))
    except:
        pass

char_counts = {} # 初始化一个字典，用于存储每个位置上的字符出现次数

for output in outputs:  # 遍历每个输出
    s = output.decode('latin1')  # 将字节串转换为字符串

    for i, char in enumerate(s):   # 遍历字符串中的每个字符和它们的位置
        if i notin char_counts:
            char_counts[i] = {}    # 如果位置不在字典中，添加进去

        if char in char_counts[i]:  # 如果字符已经在字典中，增加它的计数，否则设置为1
            char_counts[i][char] += 1
        else:
            char_counts[i][char] = 1

most_common_chars = ''
for i in range(len(char_counts)):  # 找出每个位置上出现次数最多的字符
    most_common_chars += max(char_counts[i], key=char_counts[i].get)

print(most_common_chars)  # 打印结果
```



```
e <-> channel 6
d <-> channel 0
c <-> channel 4
dp <-> channel 1
b <-> channel 5
a <-> channel 2
f <-> channel 7
g <-> channel 3
```



```
4854427b70307733325F63306d33355F6632306d5F77313768316E4021237d
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/4-1736081324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736081324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736081325.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736081325.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736081326.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/3-1736081327.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736081328.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736081328.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736081329.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736081330.png)