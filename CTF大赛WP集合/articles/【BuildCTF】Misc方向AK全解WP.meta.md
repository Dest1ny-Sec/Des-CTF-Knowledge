---
title: 【BuildCTF】Misc 方向 AK 全解 WP
contest: BuildCTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [morse-code, LSB-stego, base64, yangguaiqi, fojue, tianji, base58, zero-width-stego, hanxin-code, snow-stego, ez-zip, qrcode, base45]
attack_chain: what is this 二进制转字符串 + 摩斯密码 / 老色批 LSB 信息 base64 解 / 一念 阴阳怪气 + 佛曰 + 天书 + Base58 / 如果再来一次 图片两字节反转 + 8!67adz6 压缩包密码 + 条形码识别 / 别真给我开盒了 铁路线路 s3901 查霸州西/南站 / 四妹 图片高度调整获后半截密文 / 白白的真好看 零宽字符隐写 + Word 调色得 Flag1 + 汉信码识别 + snow 解密 Flag3 / EZ_ZIP 图片末尾压缩包 + 修改压缩大小 + 加密标志 00 / Guesscoin 全猜 0 爆破 / Black&White 黑白色块拼二维码 + Base45
key_payload: 三段拼接 BuildCTF{Th3_wh1t3_y0u_s33_1s_n0t_wh1t3}  铁路 flag: BuildCTF{津保铁路}
one_liner: BuildCTF 2024 Misc 方向 AK 全解 WP，10 道题横跨编码/隐写/图像/条形码/铁路 OSINT/二维码。
lesson: LSB 隐写 + 零宽字符 + Snow 隐写 + 佛曰/天书/阴阳怪气是国内 Misc 隐写库三件套；图片两字节反转是常见处理；铁路 OSINT 看线路编号；汉信码是中国自主二维码标准；Base45 是欧洲常用编码。
quality: high
---

# 【BuildCTF】Misc 方向 AK 全解 WP

## 概览
BuildCTF 2024 Misc 方向 AK（All Kill）10 道题全解，涵盖编码、隐写、图像、铁路 OSINT、二维码。

## 题目1: what is this
- 二进制转字符串 + 摩斯密码
- 套 `BuildCTF{}` 即可

## 题目2: 老色批
- 查看 LSB 隐写信息
- Base64 解密得 flag

## 题目3: 一念愚即般若绝，一念智即般若生
- 阴阳怪气编码解码
- 解压 + 佛曰解密（`https://github.com/BlackCat184/Sealed-Book`）
- 天书解密
- Base58 解密

## 题目4: 如果再来一次，还会选择我吗
- 图片每两字节两两反转
- 压缩包密码 `8!67adz6`
- 条形码识别
- 解压后 Base64 多层解码

## 题目5: 别真给我开盒了哥
- 图中看到 s3901，搜该线路找离铁路近的位置
- 霸州西站和霸州南站
- flag: `BuildCTF{津保铁路}`

## 题目6: 四妹，你听我解释
- 结尾 hex 转中文
- 调整图片高度获后半截密文
- 拼接解密

## 题目7: 白白的真好看
- **Flag1**: 零宽字符隐写 `_wh1t3_y0u_s33`
- **Flag2**: Word 显示可显文字调色 `BuildCTF{Th3_wh1t3`
- **Flag3**: 汉信码识别得公众号 → 异步社区公众号 → 提示 `snownow` → Snow 解密 `_1s_n0t_wh1t3}`
- 拼接：`BuildCTF{Th3_wh1t3_y0u_s33_1s_n0t_wh1t3}`

## 题目8: EZ_ZIP
- 图片末尾提取压缩包
- 压缩包套娃，写脚本递归
- 得到 flaggggggg.zip
- 修改压缩大小使其 frData 下一节是 50 4B 01 02
- 加密标志位 00
- 解密

## 题目9: Guesscoin
- 写脚本全猜 0 直接爆破

## 题目10: Black&White
- 根据黑白块顺序拼接二维码
- 扫码得 `3I8XEDHUCJTARQFOEDX7D+08AC80T8N08Y6948DF2C43C9B6Z2`
- Base45 解码

## 经验提炼
- LSB 隐写 + 零宽字符 + Snow 隐写 + 佛曰/天书/阴阳怪气是国内 Misc 隐写库三件套
- 图片两字节反转是常见处理
- 铁路 OSINT 看线路编号（如 s3901 = 津保铁路）
- 汉信码是中国自主二维码标准
- Base45 是欧洲常用编码（`0-9A-Z $%*+\-. /:` 字符集）
- 修改 ZIP 压缩大小 + 加密标志 00 是 ZIP 修复经典手法
- 拼接多段 flag 时要去除重合部分
