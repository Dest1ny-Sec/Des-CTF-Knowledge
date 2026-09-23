---
title: CTF学习交流群 第六期writeup大放送
contest: 群赛出题
year: 2017
difficulty: medium
vuln_type: forensic_traffic
tags:
- misc
- etl
- smb
- NTLM
- hashcat
- reverse
- life_or_flag
- 群活动
attack_chain:
- etl2pcapng转换netsh trace为pcap
- wireshark看SMB抓flag.zip多次重传
- 提取Net-NTLM hash format username::domain:challenge:HMAC-MD5:blob
- hashcat -m 5600爆破administrator密码为flag
- 'life_or_flag: 20字符flag读入后deal()分支运算+4字节线性方程组'
key_payload: hashcat64 -m 5600 administrator:::8b1ca28f...:1c4d7b10...:010100... flag.txt
one_liner: 群第6期三题，etl+SMB Net-NTLM爆破+逆向flag约束方程
lesson: Net-NTLM从SMB包中提取后hashcat秒破
quality: high
full_path: CTF学习交流群_第六期writeup大放送.full.md
meta_path: CTF学习交流群_第六期writeup大放送.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: CTF学习交流群 第六期writeup大放送。群第6期三题，etl+SMB Net-NTLM爆破+逆向flag约束方程。关键路径：etl2pcapng转换netsh trace为pcap → wireshark看SMB抓flag.zip多次重传 → 提取Net-NTLM hash format username::domain:challenge:HMAC-MD5:blob。经验：Net-N...
category: web
subcategory: web_other
tools_used:
- hashcat
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/92889.html
reasoning_chain:
- 触发点：拿到 netsh trace ETL 文件 → 假设：要把 ETL 转成 pcap 才能用 wireshark 分析
- 动作：用 etl2pcapng 转换 → 观察：networksh 原始 trace 转为 wireshark 可读
- 下一步：wireshark 看 SMB 协议 → 观察：flag.zip 多次重传，每次包体相同
- 假设：Net-NTLM 凭据隐藏在 SMB 认证过程 → 动作：提取 username::domain:challenge:HMAC-MD5:blob 格式 hash
- 下一步：hashcat -m 5600 爆破 → 动作：rockyou.txt + administrator:::8b1ca28f...:1c4d7b10...:010100... → 观察：破解 administrator 密码为 flag
- 下一步：life_or_flag 题 20 字符 flag → 动作：deal() 分支运算 + 4 字节线性方程组求解
- 观察：等式逆推每个 char → 完成
failed_attempts:
- 试图直接 strings etl 文件找 flag → 失败：etl 是 windows binary trace 格式，非明文
- 试图 netsh trace converter wireshark 内置 → 失败：wireshark 不能直接解析 etl
- 试图 hashcat -m 1000 不用 NTLM 模式 → 失败：Net-NTLM 必须用 -m 5600
key_observations:
- Net-NTLM 从 SMB 包中提取后 hashcat -m 5600 秒破是 CTF Web/Misc 标配
- etl2pcapng 是 Windows netsh trace 转 wireshark 标准工具
- SMB 多次重传包体相同是 Net-NTLM 提取的有利信号
- username::domain:challenge:HMAC-MD5:blob 是 Net-NTLMv2 完整格式
- life_or_flag 等式约束 reverse 转化为矩阵求解
prerequisites:
- netsh trace + etl2pcapng 转换
- wireshark SMB 协议过滤器
- Net-NTLMv2 哈希格式识别
- hashcat 命令行使用（-m 5600 + rockyou）
- 线性方程组 reverse 求解
---
# CTF学习交流群 第六期writeup大放送

> 原文: https://www.ctfiot.com/92889.html
> ID: 92889

前言

CTF学习交流群(群号 473831530)日前已关闭入群，现公布第6期题目的writeup，感谢札克利师傅、七友师傅、Processor师傅提供的题目。第7期题目将在6月份的某一天开放，届时将开放入群。

札克利的BrainOverFlow

wp作者：札克利
https://www.bilibili.com/video/BV1Hv411z75h
（也可点击最底部的“原文链接”。）

七友的etl

wp作者：七友
拿到题目，发现是一个etl文件，对windows有经验的同学很快就可以发现这是windows netsh中的trace功能捕获的数据包，要分析的话我们先要把它转化为pcap格式，然后再用wireshark分析，我们可以使用微软的windows message analyzer，不过还有更快的，用微软这个项目：https://github.com/microsoft/etl2pcapng

转换

etl2pcapng.exe ctf.etl ctf.pcap

转换之后用wireshark打开，数据包不多，发现有多个SMB协议的数据包，其中发现了一个通过SMB复制了flag.zip。

把flag.zip提取出来，发现有多个flag，一个一个试显然不太现实。

回到数据包中发现也有SMB登陆时候的数据

猜测应该是从数据包中提取Net-NTLM hash，然后用提取出来的flag.zip爆破。Net-NTLM hash的格式为：username::
domain:
challenge:
HMAC-MD5:
blob，然后我们可以从数据包中逐个提取出来。

username为：administrator，domain为空

challenge为：8b1ca28f73d4de6b

HMAC-MD5也就是数据包中的NTProofStr：1c4d7b101dabb5d9efccce3d6f9d9075

blob就是数据包中Response去掉NTProofStr的后半部分：

0101000000000000c6a7b132cde7d5012a4bfb2ba66158e90000000002000a00510049005900
4f00550001001e00570049004e002d0051004600500048004a0053004d0031004c0037004700
040012007100690079006f0075002e0063006f006d0003003200570049004e002d0051004600
500048004a0053004d0031004c00370047002e007100690079006f0075002e0063006f006d00
050012007100690079006f0075002e0063006f006d0007000800c6a7b132cde7d50106000400
02000000080030003000000000000000010000000020000060c22a597a1da37d0ad6f1c6e64f
9cdf757a4377b789ff764b727dfb87e971080a00100000000000000000000000000000000000
0900280063006900660073002f003100390032002e003100360038002e003100340031002e00
3100340035000000000000000000

然后可以构造出完整的Net-NTLM hash，用在数据包中发现字典爆破即可

Net-NTLM hash：

administrator:::
8b1ca28f73d4de6b:
1c4d7b101dabb5d9efccce3d6f9d9075:
0101000000000000c6a7b132cde7d5012a4bfb2ba66158e90000000002000a005100490059004f00550001001e00570049004e002d0051004600500048004a0053004d0031004c0037004700040012007100690079006f0075002e0063006f006d0003003200570049004e002d0051004600500048004a0053004d0031004c00370047002e007100690079006f0075002e0063006f006d00050012007100690079006f0075002e0063006f006d0007000800c6a7b132cde7d5010600040002000000080030003000000000000000010000000020000060c22a597a1da37d0ad6f1c6e64f9cdf757a4377b789ff764b727dfb87e971080a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100340031002e003100340035000000000000000000

Net-NTLM hash我们可以用hashcat爆破，flag不到1秒出来了：

hashcat64.exe -m 5600 administrator:::
8b1ca28f73d4de6b:
1c4d7b101dabb5d9efccce3d6f9d9075:
0101000000000000c6a7b132cde7d5012a4bfb2ba66158e90000000002000a005100490059004f00550001001e00570049004e002d0051004600500048004a0053004d0031004c0037004700040012007100690079006f0075002e0063006f006d0003003200570049004e002d0051004600500048004a0053004d0031004c00370047002e007100690079006f0075002e0063006f006d00050012007100690079006f0075002e0063006f006d0007000800c6a7b132cde7d5010600040002000000080030003000000000000000010000000020000060c22a597a1da37d0ad6f1c6e64f9cdf757a4377b789ff764b727dfb87e971080a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100340031002e003100340035000000000000000000 ./flag.txt --force

Processor的life_or_flag

wp作者：天河
整个文件通过逆向还原流程，首先从flag文件中读取二十个字符，而后在400AAC算MD5放在V6中

在402358 4024dd上进行两次check，当返回值为1时退出。402358这个函数是类似于一个约束条件。

对flag中的四个字节做出了约束，4024DD函数中对输入进行简单处理，最终比较在堆栈上定义的数据。

最后在以下部分对md5进行校验。

flag_encode=[204,110,95,51,61,47,118,57,87,50,115,228,86,47,49,37,25,118,31,123]
print len(flag_encode)
def deal(a):
    s=a&3
    if s==1:
        a=a-2
    if s==2:
        a=(a*2)&0xff
    if s==3:
        a=a/2
    if s==0:
        a=a+2
    return a
s=[]
for i in range(20):
    z=[]
    for j in range(128):
        k=deal(j)
        if k==flag_encode[i]:
            z.append(j)
    s.append(z)
print s
dd=s[5]
ddd=s[9]
dddd=s[13]
ddddd=s[16]
for v2 in dd:
    for v3 in ddd:
        for v4 in dddd:
            for v5 in ddddd:
                if 9 * v3 + 6 * v2 + 3 * v4 + 8 * v5 == 1281 and 2 * v2 + 11 * v3 + 22 * v4 + 3 * v5 == 1857 and 3 * v3 + 7 * v2 + 9 * v4 + 4 * v5 == 1132 and 19 * v3 + 11 * v2 + 20 * v4 + v5 == 2482:
                    print v2,v3,v4,v5
                    a=[]
                    a.append(v2)
                    s[5]=a
                    a=[]
                    a.append(v3)
                    s[9]=a
                    a=[]
                    a.append(v4)
                    s[13]=a
                    a=[]
                    a.append(v5)
                    s[16]=a
print s

z=""
for i in s:
    if len(i)>1:
        z+="*"
    else:
        for j in i:
            z+=chr(j)

print z

第7期预告

札克利的BrainOverFlow Vol2：

ps. CTF学习交流群跟ChaMd5安全团队无关，本文乃投稿。

end

ChaMd5 ctf组 长期招新

尤其是crypto+reverse+pwn+合约的大佬

欢迎联系admin@chamd5.org


```
etl2pcapng.exe ctf.etl ctf.pcap
0101000000000000c6a7b132cde7d5012a4bfb2ba66158e90000000002000a00510049005900
4f00550001001e00570049004e002d0051004600500048004a0053004d0031004c0037004700
040012007100690079006f0075002e0063006f006d0003003200570049004e002d0051004600
500048004a0053004d0031004c00370047002e007100690079006f0075002e0063006f006d00
050012007100690079006f0075002e0063006f006d0007000800c6a7b132cde7d50106000400
02000000080030003000000000000000010000000020000060c22a597a1da37d0ad6f1c6e64f
9cdf757a4377b789ff764b727dfb87e971080a00100000000000000000000000000000000000
0900280063006900660073002f003100390032002e003100360038002e003100340031002e00
3100340035000000000000000000
administrator:::
8b1ca28f73d4de6b:
1c4d7b101dabb5d9efccce3d6f9d9075:
0101000000000000c6a7b132cde7d5012a4bfb2ba66158e90000000002000a005100490059004f00550001001e00570049004e002d0051004600500048004a0053004d0031004c0037004700040012007100690079006f0075002e0063006f006d0003003200570049004e002d0051004600500048004a0053004d0031004c00370047002e007100690079006f0075002e0063006f006d00050012007100690079006f0075002e0063006f006d0007000800c6a7b132cde7d5010600040002000000080030003000000000000000010000000020000060c22a597a1da37d0ad6f1c6e64f9cdf757a4377b789ff764b727dfb87e971080a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100340031002e003100340035000000000000000000
hashcat64.exe -m 5600 administrator:::
8b1ca28f73d4de6b:
1c4d7b101dabb5d9efccce3d6f9d9075:
0101000000000000c6a7b132cde7d5012a4bfb2ba66158e90000000002000a005100490059004f00550001001e00570049004e002d0051004600500048004a0053004d0031004c0037004700040012007100690079006f0075002e0063006f006d0003003200570049004e002d0051004600500048004a0053004d0031004c00370047002e007100690079006f0075002e0063006f006d00050012007100690079006f0075002e0063006f006d0007000800c6a7b132cde7d5010600040002000000080030003000000000000000010000000020000060c22a597a1da37d0ad6f1c6e64f9cdf757a4377b789ff764b727dfb87e971080a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100340031002e003100340035000000000000000000 ./flag.txt --force
flag_encode=[204,110,95,51,61,47,118,57,87,50,115,228,86,47,49,37,25,118,31,123]
print len(flag_encode)
def deal(a):
    s=a&3
    if s==1:
        a=a-2
    if s==2:
        a=(a*2)&0xff
    if s==3:
        a=a/2
    if s==0:
        a=a+2
    return a
s=[]
for i in range(20):
    z=[]
    for j in range(128):
        k=deal(j)
        if k==flag_encode[i]:
            z.append(j)
    s.append(z)
print s
dd=s[5]
ddd=s[9]
dddd=s[13]
ddddd=s[16]
for v2 in dd:
    for v3 in ddd:
        for v4 in dddd:
            for v5 in ddddd:
                if 9 * v3 + 6 * v2 + 3 * v4 + 8 * v5 == 1281 and 2 * v2 + 11 * v3 + 22 * v4 + 3 * v5 == 1857 and 3 * v3 + 7 * v2 + 9 * v4 + 4 * v5 == 1132 and 19 * v3 + 11 * v2 + 20 * v4 + v5 == 2482:
                    print v2,v3,v4,v5
                    a=[]
                    a.append(v2)
                    s[5]=a
                    a=[]
                    a.append(v3)
                    s[9]=a
                    a=[]
                    a.append(v4)
                    s[13]=a
                    a=[]
                    a.append(v5)
                    s[16]=a
print s

z=""
for i in s:
    if len(i)>1:
        z+="*"
    else:
        for j in i:
            z+=chr(j)

print z
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