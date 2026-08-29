---
title: 逆向心法修炼之道 FLARE ON 9TH WRITEUP
contest: FLARE ON 9th Challenge
year: 2022
difficulty: hard
vuln_type: reverse
tags: [FlareOn, Mandiant, mixed-mode-PE, .NET-native, capa, floss, PE32, RC4, moonphase-calc, wchar-keystream, xor-decrypt]
attack_chain:
- 第1题Flaredle:word.js内置硬编码值对比
- 第2题Pixel Poker:像素坐标x==0x52414C46%0x2E5=95,y==0x6E4F2D45%0x281=313
- 第3题Magic 8 Ball:输入gimme flag pls?+L L U R U L D U L方向键序列
- 第4题darn_mice:str[i]+v5[i]=单字节ret(0xC3)+反推输入see three, C3 C3 C3 C3 C3 C3 C3! XD
- 第5题T8:sleep到满月+srand(本小时毫秒数)+rc4(FO9+randnum)+POST flare-on.com
- T8攻击:枚举srand seed(14:14:36前后)+遍历65535个md5+找出rc4 key
- T8解密:14组_SYSTEMTIME+月相值索引alphabet表=flag前缀i_**
- 第6题àla mode:capa v4.0识别mixed mode+floss-floss找xor解密后的\\.\pipe\FlareOn
- DllEntryPoint定位0x1000181A+native code xor动态解密函数符号+\\.\pipe\FlareOn RPC通信
- 预置密码:MyV0ic3!+0x10001187解密flag
key_payload: see three, C3 C3 C3 C3 C3 C3 C3! XD + MyV0ic3!
one_liner: FlareOn 9th (2022)全11题WP,涵盖Flaredle硬编码/Pixel Poker坐标/Magic 8 Ball方向键/darn_mice单字节ret反推/T8满月+srand+RC4+月相计算+àla mode mixed-mode PE+pipe RPC+password MyV0ic3!。
lesson: FlareOn是Windows逆向顶级比赛,Mandiant出题质量高;mixed-mode PE(.NET+native)是复杂逆向场景;capa+floss+IDA联合分析是Windows逆向标配;满月+日期穿越是T8的特色。
quality: high
---

## 题目列表

FlareOn 9th Challenge(2022)11题:
1. Flaredle (word.js硬编码)
2. Pixel Poker (坐标95,313)
3. Magic 8 Ball (gimme flag pls?+方向键)
4. darn_mice (单字节ret反推)
5. T8 (满月+srand+RC4+月相)
6. àla mode (mixed mode PE+pipe)
7-11. 其他(详细在原文)

## 关键考点

### 第1题Flaredle
- 通过与word.js中内置的一组硬编码值进行比对
- 若相符即验证通过

### 第2题Pixel Poker
- X == 0x52414C46 % 0x2E5
- Y == 0x6E4F2D45 % 0x281
- 选取坐标(95, 313)点击

### 第3题Magic 8 Ball
- 输入gimme flag pls?
- 方向键序列:L L U R U L D U L
- 函数0x4024E0校验逻辑
- 满足后进入flag解密分支

### 第4题darn_mice
- v2(v2)操作,地址填充str[i]+v5[i](1字节)
- 该1字节必须是ret指令(0xC3)
- 反推输入:see three, C3 C3 C3 C3 C3 C3 C3! XD

### 第5题T8
- 月相计算函数判断日期(满月才不sleep)
- 修改系统日期绕过sleep
- t8.exe作为网络请求客户端,向flare-on.com发起2次POS请求
- srand(milliseconds since current hour)
- key = wchar(md5sum.hexdigest(wchar("FO9"+randnumOfDecimal)))
- POST1: wchar(b64_encode(rc4(key, wchar("ahoy"))))
- RESP1: rc4(key, b64_decode(resp))
- 攻击:枚举srand seed(14:14:36前后1000-65535ms)+遍历65535个md5
- 当password=FO911950时,rc4(key, "ahoy")=ydN8BXq16RE=
- key:61003500630036003900390033003200390039003400320039006100610037006200390030003000320031003100640034006100320037003900380034003800
- RESP1解密:wchar(",")分割生成14组_SYSTEMTIME结构
- 计算月相值+索引alphabet表=flag前缀i_**

### 第6题àla mode
- capa v4.0识别mixed mode特征
- floss v1.7.0找xor解密后的\\.\pipe\FlareOn
- IDA Load config:Portable executable for 80386
- DllEntryPoint定位0x1000181A
- native code xor动态解密函数符号
- \\.\pipe\FlareOn RPC通信(native code读,managed code写)
- 预置密码:MyV0ic3!
- 0x10001187函数解密flag

## 实战价值
- FlareOn是Windows逆向顶级比赛,Mandiant出题质量高
- mixed-mode PE(.NET+native)是复杂逆向场景
- capa+floss+IDA联合分析是Windows逆向标配
- 满月+日期穿越是T8的特色
- 单字节ret反推是darn_mice的trick
- FlareOn 9th是2022年Windows逆向的标杆
