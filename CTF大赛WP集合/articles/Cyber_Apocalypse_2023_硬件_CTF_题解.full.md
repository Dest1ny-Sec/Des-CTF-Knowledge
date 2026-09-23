---
title: Cyber Apocalypse 2023 硬件 CTF 题解
contest: Cyber Apocalypse 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags:
- hardware
- 逻辑分析仪
- Gerber
- UART
- Verilog
- hamming74
- 数码管
attack_chain:
- 'Timed: 逻辑分析仪波形识别文字flag'
- 'Critical Flight: Gerber PCB viewer找隐藏字符串'
- 'Debug: UART波特率分析解码flag'
- 'HM74: Verilog 74汉明码纠错码统计分析'
- 'Secret-Code: 逻辑分析仪+Gerber通道映射还原数码管字符'
- 'hamming(7,4)码: p0,p1,p2校验+data_in3-0=4bit'
key_payload: 'ham_out={p0,p1,data_in3,p2,data_in2,data_in1,data_in0}  # 7位'
one_liner: 5道硬件题综合：波形图+Gerber+UART+Hamming+数码管逆向
lesson: 硬件CTF结合Verilog/逻辑分析仪/PCB viewer多工具
quality: high
full_path: Cyber_Apocalypse_2023_硬件_CTF_题解.full.md
meta_path: Cyber_Apocalypse_2023_硬件_CTF_题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'Cyber Apocalypse 2023 硬件 CTF 题解。5道硬件题综合：波形图+Gerber+UART+Hamming+数码管逆向。关键路径：Timed: 逻辑分析仪波形识别文字flag → Critical Flight: Gerber PCB viewer找隐藏字符串 → Debug: UART波特率分析解码flag。经验：硬件CTF结合Verilog/逻辑分析仪/PCB vie...'
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/222634.html
reasoning_chain:
- Timed Transmission 拿到逻辑分析仪波形图 → 触发点：波形高低电平组成字符
- 动作：人工识别波形脉冲时序 → 短长对应 ASCII 二进制位 → 假设：高低时序拼成 'flag{...}' 文本
- Critical Flight 拿到 Gerber PCB 文件 → 动作：digipcba viewer 或 pcbway OnlineGerberViewer → 观察：丝印层有隐藏字符串
- Debug 题目 → UART 通信 + 逻辑分析仪波形 → 假设：根据波特率（如 9600/115200）解码高低电平 → ASCII 字符串
- 动作：按 start bit(0) + 8 data bits + stop bit(1) 解 → 观察：拼出 flag
- HM74 题目给 Verilog module encoder(input[3:0] data_in, output[6:0] ham_out) → 触发点：Hamming(7,4) 纠错码
- Verilog 赋值 ham_out = {p0, p1, data_in3, p2, data_in2, data_in1, data_in0} → 假设：3 个校验位 p0/p1/p2 + 4 位数据
- 动作：写 bit_check 函数 → p0_error/p1_error/p2_error 标志 → 三个都错 → data_in0 反转；其他组合按规则修正 → 输出 4bit data
- Secret-Code 题目给逻辑分析仪 + Gerber → 动作：分析 Gerber 看通道连接 → 数码管段 a/b/c/d/e/f/g 映射 → 还原 7 段字符
failed_attempts:
- 试图直接读 Gerber 文件当图像 → 失败：Gerber 是 PCB 制造格式，需要 viewer 才能可视化
- 试图忽略 parity bits 直接拼 bit → 失败：含错误的数据必须经 Hamming 纠错
- 试图固定波特率解码 → 失败：不同 debug 串口用不同速率，必须从波形算 bit period
key_observations:
- 硬件 CTF 必装工具：digipcba viewer / pcbway OnlineGerberViewer（Gerber 查看）+ Sigrok/PulseView（逻辑分析）
- Hamming(7,4) 纠错规则：3 个 p 错 → data_in0 错；p0+p1 错 → data_in3 错；p0+p2 错 → data_in2 错；p1+p2 错 → data_in1 错
- UART 解码公式：1 start(0) + 8 data (LSB first) + 1 stop(1)，baud rate = 1/bit_period
- 7 段数码管标准映射：a=顶部/b=右上/c=右下/d=底部/e=左下/f=左上/g=中间
- 波形图/Gerber/Signals.txt 多源数据交叉验证是硬件 CTF 核心方法
prerequisites:
- Verilog 基础（assign / module / input/output）
- 数字电路（Hamming 码 / UART 时序 / 7 段数码管）
- Sigrok / PulseView 逻辑分析仪使用
- Gerber PCB 文件格式 + 在线 viewer 工具
- Python 字符串处理（hex/chr/int 转换）
---
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