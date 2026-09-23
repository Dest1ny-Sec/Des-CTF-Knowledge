---
title: CTF 之 Misc - zip 压缩包分析
contest: Misc CTF
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags:
- zip结构
- 文件头 50 4B 03 04
- 目录头 50 4B 01 02
- 结束符 50 4B 05 06
- 伪加密 1400XX0008
- fcrackzip暴力破解
- CRC32爆破
- 5字符
- 明文攻击
- ARCHPR
- 看雪 wx_酸菜鱼
attack_chain:
- 'zip 3 部分: 数据区 + 目录区 + 结束符'
- 文件头 50 4B 03 04, 目录 50 4B 01 02, 结束 50 4B 05 06
- '伪加密: 目录文件标记后 4 字节 1400XX0008, XX 改 9 → 伪加密, 改 0 还原'
- '暴力破解: fcrackzip -b -l 6-6 -c 1 -p 000000 passwd.zip'
- 'CRC32 爆破: 5 字符全字典 ascii_letters + _ + 0-9'
- '明文攻击: 已知文件 ZIP 加密后, 对比 hex 找 3 个 key'
- linux 0A vs windows 0D0A 换行符差异
key_payload: '''zip 文件头 50 4B 03 04 / 目录 50 4B 01 02 / 伪加密 1400XX0008 / fcrackzip -b -l 6-6 -c 1 / CRC32 5 字符爆破 / 明文攻击 hex 对比 / linux 0A vs windows 0D0A'''
one_liner: CTF Misc zip 压缩包分析 — 伪加密 (1400XX0008 改 9) + fcrackzip 暴力破解 + CRC32 5 字符爆破 + 明文攻击 (hex 对比) + linux/windows 换行符 0A vs 0D0A 差异。
lesson: zip 伪加密是改目录 14 00 XX 00 08 中 XX 第 1 位 (0/1 切换);CRC32 爆破只适合 ≤5 字符;明文攻击需已知明文 + 相同压缩算法。
quality: medium
full_path: CTF之Misc-zip压缩包分析.full.md
meta_path: CTF之Misc-zip压缩包分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'CTF 之 Misc - zip 压缩包分析。CTF Misc zip 压缩包分析 — 伪加密 (1400XX0008 改 9) + fcrackzip 暴力破解 + CRC32 5 字符爆破 + 明文攻击 (hex 对比) + linux/windows 换行符 0A vs 0D0A 差异。。关键路径：zip 3 部分: 数据区 + 目录区 + 结束符 → 文件头 50 4B 03 04,...'
category: misc
subcategory: misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/75389.html
reasoning_chain:
- 触发点：拿到加密 zip 文件但不知道密码 → 假设：先识别是否是伪加密再考虑爆破
- 动作：hexdump 看文件头 504B0304 + 目录 504B0102 + 结束符 504B0506 → 观察：结构清晰，无损坏
- 假设：目录头 504B0102 后 4 bytes 是 14 00 XX 00 08 flag → 动作：把 XX 改 9 = 伪加密标记；改 0 = 还原
- 观察：强网杯 2020 miscstudy level5 用此法直接解压 → 完成
- 下一步：case 暴力破解 → 动作：fcrackzip -b -l 6-6 -c 1 -p 000000 passwd.zip → 观察：6 位纯数字密码 10 分钟内出
- 假设：CRC32 爆破适用于 5 字符以下小文件 → 动作：level6 含 3 个 454 字节 txt，binascii.crc32(str(st)) & 0xffffffff 五层 for
- 下一步：明文攻击 → 动作：相同压缩算法 + 已知明文 → 加密 hex 对比找 3 个 key
- 假设：跨平台压缩要注意换行符 0A vs 0D0A 差异 → 动作：linux 压缩用 0A，windows 解压需 del 0D
failed_attempts:
- 试图 7z 兼容模式打开伪加密 → 失败：部分 7z 把伪加密当真加密
- 试图 CRC32 爆 6 字符 → 失败：5 字符已逼近 95^5=7.7 亿字典上限，6 字符几乎不可行
- 试图不解压直接 strings 看 flag → 失败：flag 在加密包里 strings 看不到
key_observations:
- zip 伪加密是改目录 14 00 XX 00 08 中 XX 第 1 位（0/1 切换）
- CRC32 爆破只适合 ≤5 字符（小文件 + 短内容）
- 明文攻击需已知明文 + 相同压缩算法 + 算法版本一致
- linux 0A vs windows 0D0A 换行符差异影响明文攻击 hex 字节数
- fcrackzip 字典攻击是 linux 下 zip 密码爆破标准工具
prerequisites:
- zip 文件结构（数据区/目录区/结束符 magic bytes）
- fcrackzip 命令行爆破（-b 暴力 -c 字符集 -l 长度）
- CRC32 算法理解（binascii.crc32 & 0xffffffff）
- 明文攻击原理（PKZIP 算法 + same compression method）
- ARCHPR Windows GUI 工具
---
# CTF之Misc-zip压缩包分析

> 原文: https://www.ctfiot.com/75389.html
> ID: 75389

本人打ctf总结的一点思路，如有错漏之处，敬请指正。

一个zip文件由三部分组成：压缩源文件数据区+压缩源文件目录区+压缩源文件目录结束标志。

在这个数据区中每一个压缩的源文件/目录都是一条记录，记录的格式如下：
[文件头+ 文件数据 + 数据描述符]

文件头结构、、、、、组成 　 长度文件头标记 4 bytes (0x04034b50)解压文件所需 pkware 版本 2 bytes全局方式位标记 2 bytes压缩方式 2 bytes最后修改文件时间 2 bytes最后修改文件日期 2 bytesCRC-32校验 4 bytes压缩后尺寸 4 bytes未压缩尺寸 4 bytes文件名长度 2 bytes扩展记录长度 2 bytes文件名 （不定长度）扩展字段 （不定长度）文件数据、、、、、数据描述符、、、、、CRC-32校验 4 bytes压缩后尺寸 4 bytes未压缩尺寸 4 bytes

这个数据描述符只在全局方式位标记的第３位设为１时才存在，紧接在压缩数据的最后一个字节后。这个数据描述符只用在不能对输出的 ZIP 文件进行检索时使用。例如：在一个不能检索的驱动器（如：磁带机上）上的 ZIP 文件中。如果是磁盘上的ZIP文件一般没有这个数据描述符。

50 4B 03 04：这是头文件标记（0x04034b50）
14 00：解压文件所需 pkware 版本
00 00：全局方式位标记（有无加密） 头文件标记后2bytes
08 00：压缩方式

在这个数据区中每一条纪录对应在压缩源文件数据区中的一条数据。

组成 　 长度目录中文件文件头标记 4 bytes (0x02014b50)压缩使用的　pkware 版本 2 bytes解压文件所需 pkware 版本 2 bytes全局方式位标记 2 bytes压缩方式 2 bytes最后修改文件时间 2 bytes最后修改文件日期 2 bytesＣＲＣ－３２校验 4 bytes压缩后尺寸 4 bytes未压缩尺寸 4 bytes文件名长度 2 bytes扩展字段长度 2 bytes文件注释长度 2 bytes磁盘开始号 2 bytes内部文件属性 2 bytes外部文件属性 4 bytes局部头部偏移量 4 bytes文件名 （不定长度）扩展字段 （不定长度）文件注释 （不定长度）

50 4B 01 02：目录中文件文件头标记(0x02014b50)
3F 00：压缩使用的 pkware 版本
14 00：解压文件所需 pkware 版本
00 00：全局方式位标记（有无加密，伪加密的关键） 目录文件标记后4bytes
08 00：压缩方式

组成 　 长度目录结束标记 4 bytes (0x02014b50)当前磁盘编号 2 bytes目录区开始磁盘编号 2 bytes本磁盘上纪录总数 2 bytes目录区中纪录总数 2 bytes目录区尺寸大小 4 bytes目录区对第一张磁盘的偏移量 4 bytesZIP 文件注释长度 2 bytesZIP 文件注释 （不定长度）

00 00：当前磁盘编号
00 00：目录区开始磁盘编号

暴力破解
暴力破解就是爆破压缩包的密码。

windows下可以使用ARCHPR这款工具。

linux下可以使用frackzip命令。

fcrackzip -b -l 6-6 -c 1 -p 000000 passwd.zip-b 暴力破解-c 1 限制密码是数字-l 6-6 限制密码长度为6-p 000000 初始化破解起点

伪加密

这里是504B01021400000008，将1400XX0008改成单数就形成了伪加密。将这里改成0009再来看一下再改回去就破解了伪加密。

例题 强网杯2020 miscstudy level5
伪加密，处理后解压出leve5

明文攻击
大致原理，一个需要解密的ZIP而且不知道密码，但幸运的是有ZIP包里一个已知文件，将已知文件进行ZIP加密后和待解密的ZIP里已知文件进行hex对比，两者的区别就是ZIP加密的三个key。
需要查看压缩算法是否一致，CRC校验值是否相同。

CRC爆破
CRC32碰撞用于非常小的文件（6字节以上基本就别试了），就是通过CRC来反推文件内容。
而且CRC32是很容易碰撞的，所以就6字节而言，同一个CRC32可能对应着十几个字符串（纯可视字符）。

例题 强网杯2020 miscstudy level6
level6的压缩包，发现内部有三个长度为454的txt文件，想到crc爆破。

import stringimport binascii dic = string.ascii_letters+"_"+'0123456789'crc2=0xEED7E184crc1=0x9AEACC13crc3=0x289585AF def aa(crc): for i in dic: for j in dic: for k in dic: for p in dic: for q in dic: st = i+j+k+p+q if crc == (binascii.crc32(str(st)) & 0xffffffff): print st return def bb(crc): for i in dic: for j in dic: for k in dic: for p in dic: st = i+j+k+p if crc == (binascii.crc32(str(st)) & 0xffffffff): print st return aa(crc1)bb(crc2)aa(crc3)

例题PT Site bytectf2020
在注册页面看到三张图

最后的一张图有用 根据这个，自己输入员工编号，申请编号是日期加后四位随机，去爆破CRC。

import binasciiimport stringimport zipfileimport base64import syscrc = int(0xcb0d2242)i = 0aaa="0123456789"for a in aaa: for b in aaa: for c in aaa: for d in aaa: strings = "亲爱的员工888888，您自助申请的PT邀请服务已受理完成，邀请链接在附件压缩包中，欢迎下次使用。nn"+"申请编号：20201025"+a + b + c+ d +"n"+"ByteCTF Secret PT Server" strings = strings.encode('utf-8') print(binascii.crc32(strings)) if crc == ((binascii.crc32(strings))&0xFFFFFFFF): print(strings) sys.exit(1) else: print(i) i = i+1

然后去明文攻击，其中有一点是，把数据写到.txt中，会看到数据比压缩包里的密文多三个字节,那是因为linux下的换行符位0A，windows下为0D0A，将0D删去即可。

得到http://182.92.4.49:
30080/signup.php?type=invite&invitenumber=8128e1f98353335c9b935fec58f0be46

看雪ID：wx_酸菜鱼

https://bbs.pediy.com/user-home-865065.htm

*本文由看雪论坛 wx_酸菜鱼 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
文件头结构、、、、、组成 　 长度文件头标记 4 bytes (0x04034b50)解压文件所需 pkware 版本 2 bytes全局方式位标记 2 bytes压缩方式 2 bytes最后修改文件时间 2 bytes最后修改文件日期 2 bytesCRC-32校验 4 bytes压缩后尺寸 4 bytes未压缩尺寸 4 bytes文件名长度 2 bytes扩展记录长度 2 bytes文件名 （不定长度）扩展字段 （不定长度）文件数据、、、、、数据描述符、、、、、CRC-32校验 4 bytes压缩后尺寸 4 bytes未压缩尺寸 4 bytes
组成 　 长度目录中文件文件头标记 4 bytes (0x02014b50)压缩使用的　pkware 版本 2 bytes解压文件所需 pkware 版本 2 bytes全局方式位标记 2 bytes压缩方式 2 bytes最后修改文件时间 2 bytes最后修改文件日期 2 bytesＣＲＣ－３２校验 4 bytes压缩后尺寸 4 bytes未压缩尺寸 4 bytes文件名长度 2 bytes扩展字段长度 2 bytes文件注释长度 2 bytes磁盘开始号 2 bytes内部文件属性 2 bytes外部文件属性 4 bytes局部头部偏移量 4 bytes文件名 （不定长度）扩展字段 （不定长度）文件注释 （不定长度）
组成 　 长度目录结束标记 4 bytes (0x02014b50)当前磁盘编号 2 bytes目录区开始磁盘编号 2 bytes本磁盘上纪录总数 2 bytes目录区中纪录总数 2 bytes目录区尺寸大小 4 bytes目录区对第一张磁盘的偏移量 4 bytesZIP 文件注释长度 2 bytesZIP 文件注释 （不定长度）
fcrackzip -b -l 6-6 -c 1 -p 000000 passwd.zip-b 暴力破解-c 1 限制密码是数字-l 6-6 限制密码长度为6-p 000000 初始化破解起点
import stringimport binascii dic = string.ascii_letters+"_"+'0123456789'crc2=0xEED7E184crc1=0x9AEACC13crc3=0x289585AF def aa(crc): for i in dic: for j in dic: for k in dic: for p in dic: for q in dic: st = i+j+k+p+q if crc == (binascii.crc32(str(st)) & 0xffffffff): print st return def bb(crc): for i in dic: for j in dic: for k in dic: for p in dic: st = i+j+k+p if crc == (binascii.crc32(str(st)) & 0xffffffff): print st return aa(crc1)bb(crc2)aa(crc3)
import binasciiimport stringimport zipfileimport base64import syscrc = int(0xcb0d2242)i = 0aaa="0123456789"for a in aaa: for b in aaa: for c in aaa: for d in aaa: strings = "亲爱的员工888888，您自助申请的PT邀请服务已受理完成，邀请链接在附件压缩包中，欢迎下次使用。nn"+"申请编号：20201025"+a + b + c+ d +"n"+"ByteCTF Secret PT Server" strings = strings.encode('utf-8') print(binascii.crc32(strings)) if crc == ((binascii.crc32(strings))&0xFFFFFFFF): print(strings) sys.exit(1) else: print(i) i = i+1
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