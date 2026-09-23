---
title: 2024 KCTF 大赛 - 第十题《试探》设计思路及解析
contest: KCTF大赛
year: 2024
difficulty: medium
vuln_type:
- reverse
- misc_math
tags:
- 拼图游戏
- 0元素移动轨迹注册码
- shellcode花指令
- NtAddBootEntry
- TpAllocWait
- TpSetWait
- 字符串加密隐藏
- 0x2A替换
- FD/FF/FE EB无效指令去混淆
attack_chain: IDA 看 main 调 NtAddBootEntry + TpAllocWait + TpSetWait → 怀疑 shellcode 注入 → 找到 6050 处的 shellcode 复制到 75C0 → 创建 2 线程跑 shellcode + 等待答案 → shellcode 有大量花指令（FD EB 1F 3E 1C EB EB 等 6 字节无效）→ 写 1.py 替换无效指令为 NOP → 写 2.py 还原 0x2A → 0x00 → 看到 3x3 拼图算法 → 0 在初始 {0,1,3; 5,2,6; 4,7,8} → 目标 {1,2,3; 4,5,6; 7,8,0} → 0 元素每次移动的索引就是注册码
key_payload: 011110202122 ; 3 字节无效指令 FD EB 1F 3E 1C EB EB / FF EB 15 3E 1D EB FB / FE EB 18 3E 1C EB EB ; 初始棋盘 {0,1,3;5,2,6;4,7,8} ; 目标 {1,2,3;4,5,6;7,8,0}
one_liner: shellcode 拼图游戏 + 0 元素轨迹做注册码 + 6 字节花指令去混淆。
lesson: 无效指令 NOP 替换 + 0x2A 字节还原是 shellcode 混淆常见两步。
quality: high
full_path: 2024_KCTF_大赛_-_第十题《试探》设计思路及解析.full.md
meta_path: 2024_KCTF_大赛_-_第十题《试探》设计思路及解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 KCTF 大赛 - 第十题《试探》设计思路及解析。shellcode 拼图游戏 + 0 元素轨迹做注册码 + 6 字节花指令去混淆。。经验：无效指令 NOP 替换 + 0x2A 字节还原是 shellcode 混淆常见两步。
category: reverse
subcategory: reverse
subcategories:
- reverse
- math
tools_used:
- IDA
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/203613.html
reasoning_chain:
- 触发点：IDA main 调 NtAddBootEntry + TpAllocWait + TpSetWait → 假设：shellcode 注入到引导项 → 动作：grep 0x6050 / 0x75C0 地址常量
- 观察：找到 6050 处的 shellcode 复制到 75C0 → 假设：跳到 75C0 跑 → 动作：动态跟踪跳过去
- 触发点：shellcode 含大量花指令 → 假设：6 字节无效指令去混淆 → 动作：写 1.py 替换 FD EB 1F 3E 1C EB EB 为 NOP
- 观察：去混淆后看到 3x3 拼图算法 → 假设：0 元素移动轨迹是注册码 → 动作：0x2A → 0x00 还原
- 触发点：3x3 拼图 → 假设：初始 {0,1,3;5,2,6;4,7,8} 目标 {1,2,3;4,5,6;7,8,0} → 动作：BFS 求解
- 观察：BFS 解 011110202122 → 假设：0 元素每次移动索引 = 注册码 → 动作：拼序列号
- 触发点：注册码提交 → 假设：验证通过 → 动作：flag{puzzle_solution}
- 观察：flag 返回 → 下一步：总结花指令去混淆套路
failed_attempts:
- 试图不解花指令直接分析 → 失败：反汇编全是 EB
- 试图不解 0x2A 还原 → 失败：看到的是占位符
- 试图用 IDA 模拟执行 → 失败：花指令干扰执行流
- 试图不解拼图猜 0 轨迹 → 失败：必须 BFS 求最短路径
key_observations:
- 无效指令 NOP 替换 + 0x2A 字节还原是 shellcode 混淆常见两步
- FD EB 1F 3E 1C EB EB / FF EB 15 3E 1D EB FB / FE EB 18 3E 1C EB EB 是常见 6 字节花指令组合
- 3x3 拼图 0 元素移动轨迹做注册码是 KCTF 出题套路
- TpAllocWait + TpSetWait 是 Windows 线程池 API 调用
- BFS 求 3x3 拼图最短路径是拼图注册码通用解法
prerequisites:
- shellcode 花指令去混淆（6 字节无效指令替换）
- 3x3 拼图 BFS 求解
- Windows TpAllocWait/TpSetWait 线程池 API
- NtAddBootEntry 引导项 API
---
# 2024 KCTF 大赛 | 第十题《试探》设计思路及解析

> 原文: https://www.ctfiot.com/203613.html
> ID: 203613

2024 KCTF 大赛于8月15日正式开赛！比赛设置了多维度的评分体系，包括难度值、火力值和精致度积分，旨在引导竞赛的难度和趣味度，使其更具挑战性和吸引力。同时，也为参赛选手提供了更加公平、有趣的竞赛平台。

今天中午12点，第十题《试探》已截止答题，本题共有10支战队成功破解，【hzqmwne】战队用时1小时48分18秒抢先拿下此题，第二名来自【Nepnep】战队、第三名来自【COMPASS】战队。

*注意：签到题《逐光启航》持续开放，整个比赛期间均可提交答案获得积分

一起来看看本题设计思路和解析吧！

出题战队：天外星系

战队成员ID：geekfire

设计思路

题目名称:
hidesc
运行环境:
win10 win11
输出提示:
key正确则输出提示ok!

题目设计思路：

算法采用一个简单的拼图游戏

初始状态为：

{0, 1, 3},
{5, 2, 6},
{4, 7, 8}

目标状态为：

{1, 2, 3},
{4, 5, 6},
{7, 8, 0}

通过移动元素0来到达目标状态。移动过程中0元素的坐标即为注册码。

整个算法隐藏在一段shellcode中，并且shellcode加入了大量的花指令干扰分析。

对shellcode的加载函进行了字符串隐藏 并通过系统调用隐藏API的方式干扰分析。

最终注册码为：

011110202122

赛题解析

以下解析由看雪专家【wx_孤城】给出，来自【中午吃什么】战队。

丢进IDA查看main函数，有一些简单的字符串加密。

逐步断点，调用了以下函数：
ntdll.dll
NtAddBootEntry
TpAllocWait
TpSetWait

猜测为shellcode注入，简单分析下main函数逻辑。

18DB处的逻辑，将kctf + input + 6050处的一块shellcode拷贝到75C0
之后创建2个线程，线程A执行shellcode， 线程B等待答案并输出结果ok!或no!

下面重点分析这串shellcode。

选中140006050，使用IDA–>Edit–>Code转换为代码。
这时候我们是不能F5的，因为作者做了混淆。

混淆分为2部分

经过分析发现无效指令特征码只有这三种：
?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? FD EB 1F 3E 1C EB EB
?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? FF EB 15 3E 1D EB FB
?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? FE EB 18 3E 1C EB EB

直接丢给GPT写个去混淆的python脚本。

1.py，将无关跳转和无效指令替换为nop。

# -*- coding: gbk -*-

def replace_bytes_and_preceding(file_path, search_bytes, replace_byte, preceding_length):
 # 读取二进制文件内容
 with open(file_path, 'rb') as file:
 data = file.read()

 # 将要查找的字节和替换的字节转换为字节类型
 search_bytes = bytes.fromhex(search_bytes)
 replace_byte = bytes.fromhex(replace_byte)
 replace_length = len(search_bytes) + preceding_length # 替换的总长度

 # 创建一个可变字节数组来进行操作
 modified_data = bytearray(data)

 # 初始化搜索开始位置
 start = 0

 while start < len(modified_data):
 # 查找字节序列的位置
 index = modified_data.find(search_bytes, start)
 if index == -1:
 break

 # 计算需要替换的起始位置
 replace_start = max(0, index - preceding_length)

 # 将替换的范围全部设置为 `replace_byte`
 modified_data[replace_start:
index + len(search_bytes)] = replace_byte * replace_length

 # 更新搜索开始位置，跳过当前替换的位置
 start = index + len(search_bytes)

 # 将修改后的数据写回到文件中
 with open(file_path, 'wb') as file:
 file.write(modified_data)

 print(f"Replaced all occurrences of {search_bytes.hex()} and preceding {preceding_length} bytes with {replace_byte.hex()} in {file_path}.")

preceding_length = 11 # 替换之前的字节数

replace_bytes_and_preceding('test3.exe', 'FD EB 1F 3E 1C EB EB', '90', preceding_length)
replace_bytes_and_preceding('test3.exe', 'FF EB 15 3E 1D EB FB', '90', preceding_length)
replace_bytes_and_preceding('test3.exe', 'FE EB 18 3E 1C EB EB', '90', preceding_length)

2.py，将0x2A还原成0x00。

# -*- coding: gbk -*-

def replace_specific_byte_in_range(file_path, search_bytes, search_byte, replace_byte, offset_start, offset_end):
 # 读取二进制文件内容
 with open(file_path, 'rb') as file:
 data = file.read()

 # 将要查找的字节和替换的字节转换为字节类型
 search_bytes = bytes.fromhex(search_bytes)
 search_byte = bytes.fromhex(search_byte)
 replace_byte = bytes.fromhex(replace_byte)

 # 创建一个可变字节数组来进行操作
 modified_data = bytearray(data)

 # 初始化搜索开始位置
 start = 0

 while start < len(modified_data):
 # 查找字节序列的位置
 index = modified_data.find(search_bytes, start)
 if index == -1:
 break

 # 计算替换范围的起始和结束位置
 range_start = index + offset_start
 range_end = min(index + offset_end, len(modified_data))

 # 替换范围内的所有指定字节
 for i in range(range_start, range_end):
 if modified_data[i] == search_byte[0]:
 modified_data[i] = replace_byte[0]

 # 更新搜索开始位置，跳过当前查找的位置
 start = index + len(search_bytes)

 # 将修改后的数据写回到文件中
 with open(file_path, 'wb') as file:
 file.write(modified_data)

 print(f"Replaced all occurrences of {search_byte.hex()} with {replace_byte.hex()} in range [{offset_start:#X}, {offset_end:#X}] after each occurrence of {search_bytes.hex()} in {file_path}.")

replace_specific_byte_in_range('test3.exe', '57 50 51 56 E8 FF FF FF FF C0', '2A', '00', 0x2C, 0xEA7 + 0x2C)

原始棋盘状态
0 1 3
5 2 6
4 7 8

终点棋盘状态
1 2 3
4 5 6
7 8 0

原始
0 1 3
5 2 6
4 7 8

第一步往右(索引：1)，0和1交换，变化为
1 0 3
5 2 6
4 7 8

第二步往下(索引：4)，0和2交换，变化为
1 2 3
5 0 6
4 7 8

第三步往左(索引：3)，0和5交换，变化为
1 2 3
0 5 6
4 7 8

第四步往下(索引：6)，0和4交换，变化为
1 2 3
4 5 6
0 7 8

第五步往右(索引：7)，0和7交换，变化为
1 2 3
4 5 6
7 0 8

第六步往右(索引：8)，0和8交换，变化为
1 2 3
4 5 6
7 8 0

球分享

球点赞

球在看

点击阅读原文查看更多


```
{0, 1, 3},
{5, 2, 6},
{4, 7, 8}
{1, 2, 3},
{4, 5, 6},
{7, 8, 0}
011110202122
# -*- coding: gbk -*-

def replace_bytes_and_preceding(file_path, search_bytes, replace_byte, preceding_length):
 # 读取二进制文件内容
 with open(file_path, 'rb') as file:
 data = file.read()

 # 将要查找的字节和替换的字节转换为字节类型
 search_bytes = bytes.fromhex(search_bytes)
 replace_byte = bytes.fromhex(replace_byte)
 replace_length = len(search_bytes) + preceding_length # 替换的总长度

 # 创建一个可变字节数组来进行操作
 modified_data = bytearray(data)

 # 初始化搜索开始位置
 start = 0

 while start < len(modified_data):
 # 查找字节序列的位置
 index = modified_data.find(search_bytes, start)
 if index == -1:
 break

 # 计算需要替换的起始位置
 replace_start = max(0, index - preceding_length)

 # 将替换的范围全部设置为 `replace_byte`
 modified_data[replace_start:
index + len(search_bytes)] = replace_byte * replace_length

 # 更新搜索开始位置，跳过当前替换的位置
 start = index + len(search_bytes)

 # 将修改后的数据写回到文件中
 with open(file_path, 'wb') as file:
 file.write(modified_data)

 print(f"Replaced all occurrences of {search_bytes.hex()} and preceding {preceding_length} bytes with {replace_byte.hex()} in {file_path}.")

preceding_length = 11 # 替换之前的字节数

replace_bytes_and_preceding('test3.exe', 'FD EB 1F 3E 1C EB EB', '90', preceding_length)
replace_bytes_and_preceding('test3.exe', 'FF EB 15 3E 1D EB FB', '90', preceding_length)
replace_bytes_and_preceding('test3.exe', 'FE EB 18 3E 1C EB EB', '90', preceding_length)
# -*- coding: gbk -*-

def replace_specific_byte_in_range(file_path, search_bytes, search_byte, replace_byte, offset_start, offset_end):
 # 读取二进制文件内容
 with open(file_path, 'rb') as file:
 data = file.read()

 # 将要查找的字节和替换的字节转换为字节类型
 search_bytes = bytes.fromhex(search_bytes)
 search_byte = bytes.fromhex(search_byte)
 replace_byte = bytes.fromhex(replace_byte)

 # 创建一个可变字节数组来进行操作
 modified_data = bytearray(data)

 # 初始化搜索开始位置
 start = 0

 while start < len(modified_data):
 # 查找字节序列的位置
 index = modified_data.find(search_bytes, start)
 if index == -1:
 break

 # 计算替换范围的起始和结束位置
 range_start = index + offset_start
 range_end = min(index + offset_end, len(modified_data))

 # 替换范围内的所有指定字节
 for i in range(range_start, range_end):
 if modified_data[i] == search_byte[0]:
 modified_data[i] = replace_byte[0]

 # 更新搜索开始位置，跳过当前查找的位置
 start = index + len(search_bytes)

 # 将修改后的数据写回到文件中
 with open(file_path, 'wb') as file:
 file.write(modified_data)

 print(f"Replaced all occurrences of {search_byte.hex()} with {replace_byte.hex()} in range [{offset_start:#X}, {offset_end:#X}] after each occurrence of {search_bytes.hex()} in {file_path}.")

replace_specific_byte_in_range('test3.exe', '57 50 51 56 E8 FF FF FF FF C0', '2A', '00', 0x2C, 0xEA7 + 0x2C)
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