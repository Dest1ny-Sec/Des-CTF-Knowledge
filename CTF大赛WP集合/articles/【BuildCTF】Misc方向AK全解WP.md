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

零宽字符隐写得到Flag2:_wh1t3_y0u_s33

Word显示可显文字调色得到Flag1:BuildCTF{Th3_wh1t3

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

Base64解码得到密码key:7gkjT!opo

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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1730380320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1730380320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1730380321.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1730380321.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1730380322.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1730380322.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1730380323.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1730380324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1730380324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1730380325.png)