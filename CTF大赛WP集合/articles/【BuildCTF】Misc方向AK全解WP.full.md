---
title: 【BuildCTF】Misc 方向 AK 全解 WP
contest: BuildCTF
year: 2024
difficulty: easy
vuln_type: stego
tags:
- morse-code
- LSB-stego
- base64
- yangguaiqi
- fojue
- tianji
- base58
- zero-width-stego
- hanxin-code
- snow-stego
- ez-zip
- qrcode
- base45
attack_chain: what is this 二进制转字符串 + 摩斯密码 / 老色批 LSB 信息 base64 解 / 一念 阴阳怪气 + 佛曰 + 天书 + Base58 / 如果再来一次 图片两字节反转 + 8!67adz6 压缩包密码 + 条形码识别 / 别真给我开盒了 铁路线路 s3901 查霸州西/南站 / 四妹 图片高度调整获后半截密文 / 白白的真好看 零宽字符隐写 + Word 调色得 Flag1 + 汉信码识别 + snow 解密 Flag3 / EZ_ZIP 图片末尾压缩包 + 修改压缩大小 + 加密标志 00 / Guesscoin 全猜 0 爆破 / Black&White 黑白色块拼二维码 + Base45
key_payload: '三段拼接 BuildCTF{Th3_wh1t3_y0u_s33_1s_n0t_wh1t3}  铁路 flag: BuildCTF{津保铁路}'
one_liner: BuildCTF 2024 Misc 方向 AK 全解 WP，10 道题横跨编码/隐写/图像/条形码/铁路 OSINT/二维码。
lesson: LSB 隐写 + 零宽字符 + Snow 隐写 + 佛曰/天书/阴阳怪气是国内 Misc 隐写库三件套；图片两字节反转是常见处理；铁路 OSINT 看线路编号；汉信码是中国自主二维码标准；Base45 是欧洲常用编码。
quality: high
full_path: 【BuildCTF】Misc方向AK全解WP.full.md
meta_path: 【BuildCTF】Misc方向AK全解WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【BuildCTF】Misc 方向 AK 全解 WP。BuildCTF 2024 Misc 方向 AK 全解 WP，10 道题横跨编码/隐写/图像/条形码/铁路 OSINT/二维码。。经验：LSB 隐写 + 零宽字符 + Snow 隐写 + 佛曰/天书/阴阳怪气是国内 Misc 隐写库三件套；图片两字节反转是...
category: misc
subcategory: misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/212905.html
reasoning_chain:
- what is this → 二进制字节转 ASCII → 'HELLO...' → 触发点：二进制摩斯密码
- 动作：按空格/分隔符切分 → 观察：.和-组合 → 摩斯解码 → BuildCTF{}
- 老色批 → LSB 信息 base64 解 → 触发点：图片隐写
- 假设：LSB 隐写 → 动作：stegsolve → base64 解码 → flag
- 一念 → 阴阳怪气 + 佛曰 + 天书 + Base58 → 假设：国内隐写库三件套 → 动作：逐个解码 → flag
- 如果再来一次 → 图片两字节反转 → 8!67adz6 压缩包密码 → 条形码识别 → 加密标志 00 → 解压
- 别真给我开盒了 → 图中 s3901 → 假设：铁路线路 OSINT → 动作：搜霸州西/南站 → 津保铁路
- 四妹 → 图片高度调整获后半截密文 → 拼接 → 解密
- 白白的真好看 → 零宽字符隐写 → Flag2 + Word 调色 → Flag1 + 汉信码 → snow 解密 → Flag3
- EZ_ZIP → 图片末尾压缩包 + 修改压缩大小 + 加密标志 00 → 解压
- Guesscoin → 全猜 0 爆破
- Black&White → 黑白色块拼二维码 + Base45
failed_attempts:
- 试图 stegsolve 默认设置 → 失败：必须选 LSB plane
- 试图不解密标志位直接解压 → 失败：必须改 00
key_observations:
- LSB 隐写 + 零宽字符 + Snow 隐写 + 佛曰/天书/阴阳怪气是国内 Misc 三件套
- 图片两字节反转是常见处理
- 铁路 OSINT 看线路编号
- 汉信码是中国自主二维码标准
- Base45 是欧洲常用编码
prerequisites:
- 摩斯密码表
- LSB 隐写工具（stegsolve / zsteg）
- 零宽字符 / Snow / 佛曰/天书 在线解码
- 汉信码识别 + Base45 解码
---
# 【BuildCTF】Misc方向AK全解WP

> 原文: https://www.ctfiot.com/212905.html
> ID: 212905

【what is this?】

二进制转字符串

解摩斯密码

套上BuildCTF{}即可

【老色批】

查看lsb信息

解base64得到flag

【一念愚即般若绝，一念智即般若生】

阴阳怪气解码

解压，继续佛曰解密

天书解密https://github.com/BlackCat184/Sealed-Book

Base58解密即可

【如果再来一次，还会选择我吗？】

图片的每两字节两两反转

压缩包密码8!67adz6

简单扣一下条形码，在线识别

解压文件后加一堆base64解码即可

【别真给我开盒了哥】

图中看到s3901，搜一下该线路找哪里离铁路近

找一下霸州西站和霸州南站这条线路

得到flag：BuildCTF{津保铁路}

【四妹，你听我解释】

结尾hex转中文

调整图片高度，获得后半截密文

拼接到一起解密即可

【白白的真好看】

零宽字符隐写得到Flag2:
_wh1t3_y0u_s33

Word显示可显文字调色得到Flag1:
BuildCTF{Th3_wh1t3

汉信码识别得到公众号

http://weixin.qq.com/r/ekReRh7Eh0P4rVol9xFo

转二维码扫描得到异步社区公众号，得到提示snowsnow

Snow解密（不需要添加-C -Q -S）

得到_1s_n0t_wh1t3}

三段拼接到一起去掉重合部分即BuildCTF{Th3_wh1t3_y0u_s33_1s_n0t_wh1t3}

【EZ_ZIP】

图片末尾提取出压缩包

压缩包套娃，直接上脚本

得到flaggggggg.zip

修改压缩大小使其frData部分下一节是504b0102

修改中间的加密标志位为00

解密即可得到flag

【Guesscoin】

写脚本全猜0直接爆破

【Black&White】

根据黑白块的顺序拼接二维码

扫码得到3I8XEDHUCJTARQFOEDX7D+08AC80T8N08Y6948DF2C43C9B6Z2

Base45解码即可

【有黑客！！！】

查看118262数据包，将hacker参数urldecode，字符串反转，base64解码得到

解密hhhhacker部分的参数

得到脚本

看到代码在eval执行命令之后使用gzencode编码了一下

把每个包的回显丢进去解一下就可以找到flag了

【我太喜欢亢金星君了！】

Gif分帧

转摩斯code

去掉中间的特殊符号加上BuildCTF即可

Flag：BuildCTF{BUILDCTFW41COM4N4WF1SH}

【HEX的秘密】

直接赛博厨子magic

【食不食油饼】

零宽文本盲隐写得到a2V5Ojdna2pUIW9wbw==

Base64解码得到密码key:
7gkjT!opo

解压缩包得到一张图片

单图FFT转化得到第二个密码8GMdP3

解压缩后将文本base32解码即可

【四妹？还是萍萍呢？】

拼图之后是一个公众号

第二张图片最后一个IDAT块缺少压缩包504b文件头

并且把504b0506后面的IDAT块内容删掉

预览文件看到提示公众号回复password有惊喜

使用此密码解压该压缩包

最后就是一个文本的base64转图片就好了

需要使用随波逐流修复一下宽高

【什么？来玩玩心算吧】

输入单引号报错看到是python的eval命令执行，但是过滤了字母和部分符号

使用工具parselmouth设定过滤规则生成payload

【FindYourWindows】

Vc挂在加密磁盘并选择key文件做为密钥文件

打开M盘发现桌面上的flag是假的，真正的在回收站里，但是没法资源管理器直接打开查看

用Winhex以打开查看驱动器的方式查看回收站中的文件即可

【E2_?_21P】

解压需要密码

先去掉伪加密，再解压提示CRC校验错误

然后把Compression参数改成8就可以正常解压缩了

然后bf解码即可

原文始发于微信公众号（智佳网络安全）：【BuildCTF】Misc方向AK全解WP

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