---
title: 关于音频隐写的一些总结
contest: 音频隐写综合
year: 2023
difficulty: easy
vuln_type: stego_audio
tags:
- 音频隐写
- Audacity频谱图
- SSTV
- DeepSound
- MP3stego
- DTMF拨号
- MIDI通道
- HackRF原始数据
- 摩尔斯
attack_chain:
- '工具集: Audacity/Adobe Audition(au)/SilentEye/DeepSound/SSTV/mp3stego'
- 'WAV 文件头: 57415645'
- 'Audacity 频谱图: 上下峰二进制 + 倒序反相慢速降噪'
- 'SSTV (慢扫描电视): Robot36 (Android) / MMSSTV (PC) 把图片藏到音频'
- 'DeepSound: 密码音频隐写, john 爆破密码'
- 'MP3stego: cmd Decode.exe -X <mp3> -P <pass>'
- '拨号隐写 (DTMF): https://gitcode.net/mirrors/ribt/dtmf-decoder'
- 'MIDI 隐写: 4D546864 头, 改音乐通道 2→3 找隐藏 QR'
- '信号分析: HackRF / GPS / PT2242 (4bit 同步+20bit 地址+4bit 功能+1bit 停止)'
- '原始数据: 后缀 .s8 等奇怪后缀用 Import Raw 选采样率/尾端/编码'
key_payload: '''sstv+robot36 + mp3stego + john deepsound + dtmf-decoder'''
one_liner: 音频隐写 6 大工具 + 7 种题型总结：WAV 频谱/SSTV/DeepSound/MP3stego/DTMF/MIDI/原始数据。
lesson: 音频题先听一遍无信息 → Audacity 频谱图 → 上下峰二进制/倒序反相/慢速降噪；MIDI 4D546864 头可改通道数；HackRF/原始数据后缀 .s8 需 Import Raw。
quality: medium
full_path: 关于音频隐写的一些总结.full.md
meta_path: 关于音频隐写的一些总结.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '关于音频隐写的一些总结。音频隐写 6 大工具 + 7 种题型总结：WAV 频谱/SSTV/DeepSound/MP3stego/DTMF/MIDI/原始数据。。关键路径：工具集: Audacity/Adobe Audition(au)/SilentEye/DeepSound/SSTV/mp3stego → WAV 文件头: 57415645 → Audacity 频谱图: 上下峰二进制 + ...'
category: misc
subcategory: stego
time_required: quick
difficulty_score: 2
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/95105.html
reasoning_chain:
- 音频隐写题 → 触发点：人耳听不到的信息藏在波形里
- '工具集: Audacity/Adobe Audition(au)/SilentEye/DeepSound/SSTV/mp3stego'
- 'WAV 文件头: 57415645 → 动作：Audacity 频谱图 → 上下峰二进制'
- 假设：倒序反相慢速降噪可恢复隐藏文本 → 观察：频域图分块
- 'SSTV (慢扫描电视): Robot36 (Android) / MMSSTV (PC) 把图片藏到音频 → 假设：图声是常见音频'
- 'DeepSound: 密码音频隐写 → john 爆破密码'
- 'MP3stego: cmd Decode.exe -X <mp3> -P <pass>'
- 假设：拨号隐写 DTMF → 动作：dtmf-decoder
- 'MIDI 隐写: 4D546864 头 → 改音乐通道 2→3 找隐藏 QR'
- '信号分析: HackRF / GPS / PT2242 (4bit 同步+20bit 地址+4bit 功能+1bit 停止)'
- '原始数据: 后缀 .s8 等奇怪后缀用 Import Raw 选采样率/尾端/编码'
failed_attempts:
- 试图不解频谱直接读 flag → 失败：人耳不可听
- 试图用 DeepSound 解 MP3 → 失败：MP3 用 mp3stego
- 试图不识别文件后缀 → 失败：.s8 需 Import Raw
key_observations:
- 音频题先听一遍无信息 → Audacity 频谱图 → 上下峰二进制/倒序反相/慢速降噪
- MIDI 4D546864 头可改通道数
- HackRF/原始数据后缀 .s8 需 Import Raw
- PT2242 编码 4bit 同步+20bit 地址+4bit 功能+1bit 停止
prerequisites:
- Audacity 频谱图分析
- SSTV 解码（Robot36/MMSSTV）
- MP3stego 命令行使用
- DTMF 拨号识别
---
# 关于音频隐写的一些总结

> 原文: https://www.ctfiot.com/95105.html
> ID: 95105

长

行

好

运

丁

财

旺

兔年大吉

年后第一送

先送MISC

富

贵

平

安

福

满

堂

一、常见工具

工具：Audacity、Adobe Audition(简称au)、SilentEye、DeepSound、SSTV、mp3stego。

       其实和图片一样，数字音频也可以用于信息隐写，音视频隐写会存在比较明显的特征：

   

     · 音频载体信号存在冗余，为隐蔽信息提供支持；

     · 人类听觉系统频谱范围是20Hz18kHz，但对2kHz4kH信息最为敏感；

     · 人类听觉系统只对相对相位敏感，而无法感知绝对相位。

    

       这里参考一位师傅写的文章

    C语言解析WAV音频文件

https://www.cnblogs.com/guojun-junguo/p/10129548.html

所以对于音频题，拿到题目当然首先是听一下，然后再根据是否获得信息来进行下一步操作

二、常见题型

Wave (wav)， 文件头：57415645

Audacity

作为最常用的音频查看软件，当试听题目音频没有明显杂音或者信息时，一般会选择用Audacity打开

并可以选择查看波形、频谱图

可能会获得morse电码或者二进制的信息,当然部分题目信息量过大，会用到脚本来进行提取

此外，波形图的上下峰也可能会暗含信息

出题方式是千变万化，分离左右声道来获得信息，diff反相音频获得信息，通过倒序，反相，慢速，降噪等步骤也视情况尝试（例如：经典的单词模糊听写，需要倒序后慢速听；充斥杂音的音频需要一定程度的降噪才能获得信息；ASCII编码的数字需要注意是否越过127）

SSTV

（慢扫描电视）

把图片隐藏到音频信息中的隐写，手机上可以装Robot36（app），PC可以用MMSSTV。

Deepsound

作为带有密码的音频隐写

Deepsound的密码可通过john爆破

Deepsound

作为带有密码的音频隐写

Deepsound的密码可通过john爆破

MP3stego

MP3格式文件：

    cmd打开，将 Decode.exe 拖到命令行里，将要解密的文件放在文件夹中

    # 隐藏信息

    # —E 读取隐藏信息文件的内容，-P 设置密码

encode.exe -E hidden.txt -P pass CTF.wav svega_stego.mp3

decode.exe -X svega_stego.mp3 -P pass

拨号隐写（DTMF）

推荐一个GitHub上的脚本工具

https://gitcode.net/mirrors/ribt/dtmf-decoder?utm_source=csdn_github_accelerator

MIDI隐写

MIDI (mid)， 文件头：4D546864

乍看没有发现任何信息，但稍微研究一下midi的文件结构，将音乐通道由2改为3

再重新打开文件，即可发现隐藏通道下的二维码

信号分析

包括无线电信号分析，GPS信号分析，一般用Adobe Audition或者Audacity分析；PT2242信号：前面4bit表示同步码，中间的20bit表示地址码，后面的4bit表示功能码，最后一位是停止码。

HackRF区别

原始数据

当见到音频的后缀为一些奇怪的组合时，比如扩展名为s8，要考虑是否为原始数据，所以在导入时选择导入原始数据

默认采样率、尾端和编码获取不到信息时，也要根据需要调试（频谱图可以容易的识别出信号的中心频率）

完

兔

年

大

吉

辞

旧

迎

新

–天权信安网络安全团队–

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！

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