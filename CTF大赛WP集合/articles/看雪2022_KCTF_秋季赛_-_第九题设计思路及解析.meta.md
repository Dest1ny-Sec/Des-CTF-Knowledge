---
title: 看雪2022 KCTF 秋季赛 | 第九题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [ZIP伪加密, 504b0102第5字节改08, 云影密码, base32, JJEncode, 艾特巴什码, Unicode, pydumpck, 逆运算]
attack_chain: same.zip伪加密504b0102第5字节09→08→c1云影密码→base32→JJEncode→艾特巴什→base32→Unicode→c1大数→liyou.xls用pydumpck解出exe密码2333→n文件真加密爆破前缀498+数字→NewFile base85→base91→base36→base16
key_payload: "504b0102第5字节09改08伪加密;云影密码;base32;JJEncode;艾特巴什码;pydumpck;base85→base91→base36→base16"
one_liner: KCTF2022秋Q9《乡绅压迫》全misc：伪加密+云影+base32+JJEncode+艾特巴什+Unicode+pydumpck+多层base
lesson: ZIP伪加密=504b0102第5字节改08；多层编码识别顺序是CTF misc基本功
quality: medium
---

# 看雪2022 KCTF 秋季赛 | 第九题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q9《乡绅压迫》

**难度**：4天，无人提交flag（设计题）

**完整破解链**：

**1. ZIP伪加密**
- 010edit打开same.zip
- 504b0102第5字节：09 → 08（伪加密位）
- 正常解压

**2. c1文件（多层编码）**
- 0-9数字 → **云影密码**（8位=1位）
- 全大写+数字 → **base32**
- JJEncode特征 → **JJEncode解码**
- 全大写+ascii范围内 → **艾特巴什码**（A↔Z）
- 再base32 → **Unicode**
- 最终 c1 = 大整数

**3. liyou.xls（伪xls实为exe）**
- file命令识别为exe
- 改后缀liyou.exe
- 三种解法：
  - (1) 逆向移位算法
  - (2) 直接爆破纯数字
  - (3) **pydumpck**（github工具）汇编python源码
- 逆运算得密码：**e1 = 2333**

**4. n文件（真加密）**
- 010edit发现真加密
- 文件名前缀498 + 数字爆破
- 12毫秒出结果

**5. NewFile.txt.zip（再次伪加密）**
- 504b0102第5字节改08
- base85 → base91 → base36 → base16

**6. 整体结果**：
- c1 + e1 = 最终flag

**技术总结**：
- ZIP伪加密：504b0102第5字节09→08
- 编码识别链：云影密码 → base32 → JJEncode → 艾特巴什 → base32 → Unicode
- pydumpck：python exe反编译神器
- 多层base：85/91/36/16顺序

**质量评估**：中（编码链清晰，但缺完整flag）
