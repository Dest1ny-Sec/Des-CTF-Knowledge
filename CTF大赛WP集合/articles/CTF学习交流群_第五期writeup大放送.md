# CTF学习交流群 第五期writeup大放送

> 原文: https://www.ctfiot.com/92908.html
> ID: 92908

前言

CTF学习交流群(群号 473831530)日前已关闭入群，现公布第5期题目的writeup，感谢kkkkkkkkx师傅、大土豆师傅、Adolph师傅提供的题目。第6期题目将在新年期间开放，届时将开放入群。

kkkkkkkkx的misc题

wp作者：天河

大土豆的apk题

wp作者：天河

flag_en=[0x65,0x31,0x60,0x32,0x75,0x60,0x7a,0x31,0x76,0x73,0x34,0x66,0x6d,0x67]
print (len(flag_en))
s=""
for i in flag_en:
    s+=chr(i-1)
print s

Adolph的web题

这里直接附上Adolph师傅的出题文档：

http://pcat.cc/tmp/adolph.pdf

ps. 该web环境这个春节期间内仍有效。

第6期预告

札克利的BrainOverFlow：

欢迎！现在就下载BrainOverFlow，在超大（并不）的RPG世界中扮演天河，开始您的冒险！

在BrainOverFlow的世界中扮演勇者天河，担负人类最后的希望，加入“命运”小队，在诺德大陆的最后一块净土上与“恶魔”们战斗，守护“封印”的最后一座哨站，击碎“恶魔”们的阴谋，拯救这个“世界”。

您就有机会：

· 和榕榕，glzjin，郁离歌，pcat等人并肩战斗

· 在风格各异的地图中探寻宝藏，呀呼，谁不喜欢宝藏猎人呢？

· 强大的魔法和技能，帮助您撕碎可怕的“恶魔”

· 丰富的剧情和人物塑造，身临其境的紧张氛围

· 多种多样的装备和武器，武装自己！

还等什么？现在就下载BrainOverFlow，成为“救世主”，开始属于您的冒险吧！

DLC——《BrainOverFlow 冬季仙境》

哇哦！现在购买就送游戏本体！惊爆的价格！

诺德大陆的冬天来了！“命运”小队的各位也都换上了冬装，包括“恶魔”！

新增游戏内容：

· 新角色——十月正式加入”命运“小队，让我们看看一个擅长弓术的女孩如何为战斗带来改变！

· 新衣服——包括榕榕，glzjin，郁离歌，pcat等人的全新形象！

· 新……

root@Charon_01:/mnt/ControlPanel
# Notice: Intrusion Detected.

root@Charon_01:/mnt/ControlPanel
# Notice: Firewall Building......

root@Charon_01:/mnt/ControlPanel
# 10%...20%...30%...40%...

root@Charon_01:/mnt/ControlPanel
# Fatal Error: Insufficient Computing Resources.

root@Charon_01:/mnt/ControlPanel
# Warning: Notifying Administrator......

root@Charon_01:/mnt/ControlPanel
# Warning: Process Termination!

root@Charon_01:/mnt/ControlPanel
# Notice: Remote Session Connecting......

root@Charon_01:/mnt/ControlPanel
# Notice: Remote Session Connected Successfully!

user@Virink:/#

##########################################

#########VV#################VV############

##########VV###############VV#############

###########VV#############VV##############

############VV###########VV###############

#############VV#########VV################

##############VV#######VV#################

###############VV#####VV##################

################VV###VV###################

#################VV#VV####################

##################VVV#####################

###################V######################

##########################################

user@Virink:/# Drilling......

10%...20%...30%...40%...50%...60%...70%...80%...90%...100%...

DONE!

root@Virink:/# -/...././.--/---/.-./.-../-../../.../..-./.-/-.-/.

root@Charon_01:/mnt/ControlPanel
# Notice: Remote Session Disconnected!

root@Charon_01:/mnt/ControlPanel
#  Service SecurityCheck Restart

root@Charon_01:/mnt/ControlPanel
# python traceback.py

root@Charon_01:/mnt/ControlPanel
# WARNING: Traceability System Started...

root@Charon_01:/mnt/ControlPanel
# hid

· 新装备！大家翘首盼望已久的冬季大剑终于来了，现在还在商店特价！

· 新剧情，榕榕在雪地中的祈愿，pcat和郁离歌之间不得不说的往事，等您来探索！

快来吧！穿上冬装，和大家一起快乐玩耍！

Processor的逆向题life_or_flag：

招新小广告

ChaMd5 ctf组 长期招新

尤其是crypto+reverse+pwn+合约的大佬

欢迎联系admin@chamd5.org


```
flag_en=[0x65,0x31,0x60,0x32,0x75,0x60,0x7a,0x31,0x76,0x73,0x34,0x66,0x6d,0x67]
print (len(flag_en))
s=""
for i in flag_en:
    s+=chr(i-1)
print s
root@Charon_01:/mnt/ControlPanel
# Notice: Intrusion Detected.

root@Charon_01:/mnt/ControlPanel
# Notice: Firewall Building......

root@Charon_01:/mnt/ControlPanel
# 10%...20%...30%...40%...

root@Charon_01:/mnt/ControlPanel
# Fatal Error: Insufficient Computing Resources.

root@Charon_01:/mnt/ControlPanel
# Warning: Notifying Administrator......

root@Charon_01:/mnt/ControlPanel
# Warning: Process Termination!

root@Charon_01:/mnt/ControlPanel
# Notice: Remote Session Connecting......

root@Charon_01:/mnt/ControlPanel
# Notice: Remote Session Connected Successfully!

user@Virink:/#

##########################################

#########VV#################VV############

##########VV###############VV#############

###########VV#############VV##############

############VV###########VV###############

#############VV#########VV################

##############VV#######VV#################

###############VV#####VV##################

################VV###VV###################

#################VV#VV####################

##################VVV#####################

###################V######################

##########################################

user@Virink:/# Drilling......

10%...20%...30%...40%...50%...60%...70%...80%...90%...100%...

DONE!

root@Virink:/# -/...././.--/---/.-./.-../-../../.../..-./.-/-.-/.

root@Charon_01:/mnt/ControlPanel
# Notice: Remote Session Disconnected!

root@Charon_01:/mnt/ControlPanel
#  Service SecurityCheck Restart

root@Charon_01:/mnt/ControlPanel
# python traceback.py

root@Charon_01:/mnt/ControlPanel
# WARNING: Traceability System Started...

root@Charon_01:/mnt/ControlPanel
# hid
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673937473.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673937474.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673937474.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673937475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1673937475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673937476.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673937476.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1673937478.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673937479.jpg)