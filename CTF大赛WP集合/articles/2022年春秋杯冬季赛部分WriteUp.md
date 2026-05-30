# 2022年春秋杯冬季赛部分WriteUp

> 原文: https://www.ctfiot.com/88076.html
> ID: 88076

2022年春秋杯冬季赛部分WriteUp

天权信安网络安全团队（简称“天权信安”），成立于2022年，是一支研究红蓝对抗、内网渗透、红队武器库、CTF竞赛、CTF竞赛靶场及其网安相关活动的安全团队。这里聚集着一群有技术有担当有理想、热爱信安奉献信安的多方面专业人才。天权信安的“天权”来源于北斗七星，又称为文曲星，它代表着天资聪颖，能力超群，也象征着天权信安的高标准、高水平与高质量，体现着我们的宗旨–打造一支实力强劲、团结协作的精英团队，用技术与毅力共同守护网络安全。目前成员 40 余人，队员分布于科大、航空大、北航、地大、武大、华科、西工大、西电、警大、江苏海洋大学、成信、西邮、国际关系学院、广大、河北师范大学、吉林师范大学、重庆科技学院、中原工学院、珠海科技学院、山东建筑大学、南邮、河大、郑州轻工业大学等国内各大高校，也分布于绿盟科技、四叶草安全、长亭科技、安恒信息、联通、腾讯、华为、启明星辰等国内安全大厂。

以下，为本次比赛赛题的解题思路分享：

目录

○ WEB

    ◇ ezphp

○ MISC

    ◇ nan’s analysis

    ◇ reindeer game

○ REVERSE

    ◇ easy_python

01

WEB

01

ezphp

构造payload?num=1_11

02

MISC

01

nan’s analysis

看到ftp数据，直接导出所有ftp对象

图片末尾发现图片与题目无关

shell.zip是加密的压缩包

零宽隐写，但是解出来很奇怪

02

reindeer game

小游戏难度设得简单了，完全可以通过游戏达到通关要求

结果为

flag{82a2acb6-9803-4936-92db-f1431d90c6d1}

03

REVERSE

01

easy_python

python字节码逆向分析

3 0 LOAD_CONST 1 (204) 3 LOAD_CONST 2 (141) 6 LOAD_CONST 3 (44) 9 LOAD_CONST 4 (236) 12 LOAD_CONST 5 (111) 15 LOAD_CONST 6 (140) 18 LOAD_CONST 6 (140) 21 LOAD_CONST 7 (76) 24 LOAD_CONST 3 (44) 27 LOAD_CONST 8 (172) 30 LOAD_CONST 9 (7) 33 LOAD_CONST 9 (7) 36 LOAD_CONST 10 (39) 39 LOAD_CONST 11 (165) 42 LOAD_CONST 12 (70) 45 LOAD_CONST 9 (7) 48 LOAD_CONST 10 (39) 51 LOAD_CONST 13 (166) 54 LOAD_CONST 11 (165) 57 LOAD_CONST 14 (134) 60 LOAD_CONST 14 (134) 63 LOAD_CONST 6 (140) 66 LOAD_CONST 1 (204) 69 LOAD_CONST 11 (165) 72 LOAD_CONST 9 (7) 75 LOAD_CONST 10 (39) 78 LOAD_CONST 15 (230) 81 LOAD_CONST 6 (140) 84 LOAD_CONST 11 (165) 87 LOAD_CONST 12 (70) 90 LOAD_CONST 3 (44) 93 LOAD_CONST 8 (172) 96 LOAD_CONST 16 (102) 99 LOAD_CONST 17 (6) 102 LOAD_CONST 6 (140) 105 LOAD_CONST 1 (204) 108 LOAD_CONST 15 (230) 111 LOAD_CONST 15 (230) 114 LOAD_CONST 7 (76) 117 LOAD_CONST 18 (198) 120 LOAD_CONST 19 (38) 123 LOAD_CONST 20 (175) 126 BUILD_LIST 42 129 STORE_FAST 0 (flag)
 4 132 SETUP_LOOP 54 (to 189) 135 LOAD_GLOBAL 0 (range) 138 LOAD_CONST 21 (42) 141 CALL_FUNCTION 1 144 GET_ITER >> 145 FOR_ITER 40 (to 188) 148 STORE_FAST 1 (i)
 5 151 LOAD_FAST 0 (flag) 154 LOAD_FAST 1 (i) 157 BINARY_SUBSCR 158 LOAD_CONST 22 (5) 161 BINARY_RSHIFT 162 LOAD_FAST 0 (flag) 165 LOAD_FAST 1 (i) 168 BINARY_SUBSCR 169 LOAD_CONST 23 (3) 172 BINARY_LSHIFT 173 BINARY_OR 174 LOAD_CONST 24 (255) 177 BINARY_AND 178 LOAD_FAST 0 (flag) 181 LOAD_FAST 1 (i) 184 STORE_SUBSCR 185 JUMP_ABSOLUTE 145 >> 188 POP_BLOCK >> 189 LOAD_CONST 0 (None) 192 RETURN_VALUE

flag = [204,141,44,236,111,140,140,76,44,172,7,7,39,165,70,7,39,166,165,134,134,140,204,165,7,39,230,140,165,70,44,172,102,6,140,204,230,230,76,198,38,175]for i in range(0,42): flag[i] = (flag[i] >> 5 | flag[i] << 3)&255for v in flag: print(chr(v),end="")#flag=flag{ddbae889-2895-44df-897d-2ae30df77b61}

–天权信安网络安全团队–

网络无边 安全有界

天权信安欢迎技术大咖、CTF选手等资深专业人士前来分享网络安全前沿技术、攻防实战经验、内网渗透、IOT安全、CTF、工控安全等内容，一起来帮助大家了解最新网络安全动态，提升新的安全技术，拓宽知识领域，打造一个开放共享的网络安全生态圈，吸引各大爱好CTFer和实战大咖加入我们。这里聚集了一群热爱网络安全的有志之士的加入，为“网络安全爱好者”提供一个更好的学习交流生态圈。


```
构造payload?num=1_11
flag{82a2acb6-9803-4936-92db-f1431d90c6d1}
3 0 LOAD_CONST 1 (204) 3 LOAD_CONST 2 (141) 6 LOAD_CONST 3 (44) 9 LOAD_CONST 4 (236) 12 LOAD_CONST 5 (111) 15 LOAD_CONST 6 (140) 18 LOAD_CONST 6 (140) 21 LOAD_CONST 7 (76) 24 LOAD_CONST 3 (44) 27 LOAD_CONST 8 (172) 30 LOAD_CONST 9 (7) 33 LOAD_CONST 9 (7) 36 LOAD_CONST 10 (39) 39 LOAD_CONST 11 (165) 42 LOAD_CONST 12 (70) 45 LOAD_CONST 9 (7) 48 LOAD_CONST 10 (39) 51 LOAD_CONST 13 (166) 54 LOAD_CONST 11 (165) 57 LOAD_CONST 14 (134) 60 LOAD_CONST 14 (134) 63 LOAD_CONST 6 (140) 66 LOAD_CONST 1 (204) 69 LOAD_CONST 11 (165) 72 LOAD_CONST 9 (7) 75 LOAD_CONST 10 (39) 78 LOAD_CONST 15 (230) 81 LOAD_CONST 6 (140) 84 LOAD_CONST 11 (165) 87 LOAD_CONST 12 (70) 90 LOAD_CONST 3 (44) 93 LOAD_CONST 8 (172) 96 LOAD_CONST 16 (102) 99 LOAD_CONST 17 (6) 102 LOAD_CONST 6 (140) 105 LOAD_CONST 1 (204) 108 LOAD_CONST 15 (230) 111 LOAD_CONST 15 (230) 114 LOAD_CONST 7 (76) 117 LOAD_CONST 18 (198) 120 LOAD_CONST 19 (38) 123 LOAD_CONST 20 (175) 126 BUILD_LIST 42 129 STORE_FAST 0 (flag)
 4 132 SETUP_LOOP 54 (to 189) 135 LOAD_GLOBAL 0 (range) 138 LOAD_CONST 21 (42) 141 CALL_FUNCTION 1 144 GET_ITER >> 145 FOR_ITER 40 (to 188) 148 STORE_FAST 1 (i)
 5 151 LOAD_FAST 0 (flag) 154 LOAD_FAST 1 (i) 157 BINARY_SUBSCR 158 LOAD_CONST 22 (5) 161 BINARY_RSHIFT 162 LOAD_FAST 0 (flag) 165 LOAD_FAST 1 (i) 168 BINARY_SUBSCR 169 LOAD_CONST 23 (3) 172 BINARY_LSHIFT 173 BINARY_OR 174 LOAD_CONST 24 (255) 177 BINARY_AND 178 LOAD_FAST 0 (flag) 181 LOAD_FAST 1 (i) 184 STORE_SUBSCR 185 JUMP_ABSOLUTE 145 >> 188 POP_BLOCK >> 189 LOAD_CONST 0 (None) 192 RETURN_VALUE
flag = [204,141,44,236,111,140,140,76,44,172,7,7,39,165,70,7,39,166,165,134,134,140,204,165,7,39,230,140,165,70,44,172,102,6,140,204,230,230,76,198,38,175]for i in range(0,42): flag[i] = (flag[i] >> 5 | flag[i] << 3)&255for v in flag: print(chr(v),end="")#flag=flag{ddbae889-2895-44df-897d-2ae30df77b61}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/5-1672031548.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672031549.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1672031549.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/9-1672031550.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672031550.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1672031551.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/5-1672031551.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672031552.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1672031553.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672031553.png)