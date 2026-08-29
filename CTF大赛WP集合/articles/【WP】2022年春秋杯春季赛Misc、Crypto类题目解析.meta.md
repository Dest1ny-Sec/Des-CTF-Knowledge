---
title: 【WP】2022年春秋杯春季赛 Misc、Crypto 类题目解析
contest: 春秋杯
year: 2022
difficulty: mixed
vuln_type: misc_unknown
tags: [CRC-stego, IDAT-10000-blocks, vera-crypt, winhex-recover, ICMP-data-len, IP-38-39-binary, PDF-reorder, capture-radiate]
attack_chain: 签到 关注公众号 + 音谱点击/Capture Radiate Chart alien.png 10000+ IDAT 块 CRC 最后一字节藏 RAR/RecoverMe VeraCrypt 密码本爆破 aaaAAA111 + winhex 恢复挂载盘 + secret.pcapng ICMP data.len 拼 zip 头 50 4B 03 04 + tshark 提取 IP 38/39 编码二进制 = 压缩包密码
key_payload: 春秋伽玛公众号"上课铃声"  VeraCrypt 密码 aaaAAA111  IP 末位 38/39 → 0/1
one_liner: 2022 春秋杯春季赛 Misc/Crypto 4 题 WP，CRC 隐写 + VeraCrypt 爆破 + ICMP 流量恢复 zip + IP 末位编码。
lesson: PNG IDAT 10000+ 块且 CRC 不正常是 CRC 隐写标志；VeraCrypt 密码本爆破可让 passware kit 跑 10 分钟；ICMP data.len 字段可编码文件内容；IP 末位 38/39 二值编码是隐蔽通道。
quality: high
---

# 【WP】2022年春秋杯春季赛 Misc、Crypto 类题目解析

## 概览
2022 春秋杯春季赛 4 道题 WP（签到/Capture Radiate Chart/RecoverMe + 1 道未详述）。

## 签到
- 关注"春秋伽玛"公众号
- 回复"上课铃声"拿提示
- 根据图片音谱点击相应键值

## Capture Radiate Chart
- 附件 alien.png，010 Editor 打开发现 10000+ IDAT 块
- 观察题目名 + CRC 发现是 CRC 隐写
- 用 tweakpng 查看
- 第一个 IDAT 块开始，CRC 最后一个字节隐藏数据
- 提取脚本：
  ```python
  data = open('alien.png', 'rb').read()
  flag = ''
  pos = data.index(b'IDAT')
  data = data[pos+5:]
  while 1:
      try:
          pos = data.index(b'IDAT')
          flag += str(hex(data[pos-5])[2:].zfill(2))
          data = data[pos+5:]
      except:
          open('out.rar', 'w').write(flag)
          exit(1)
  ```
- 得到的 rar 用 cyberchef hex 转
- 解压得到看起来空白的 PDF
- 重排为 `0 1 3 8 9 6 7 2 4 5` 得 flag

## RecoverMe
- VeraCrypt 加密磁盘 + 密码本
- 推荐 passware kit 爆破（每密码 10+ 秒）
- 密码: `aaaAAA111`
- 进去发现是 fake flag
- 头像图片无用
- winhex 工具→打开磁盘→选择挂载盘
- 恢复出 `secret.pcapng`

### ICMP 流量分析
- 全是 ICMP 协议
- data 大小变化
- 前 4 个 data: 80 75 3 4 → 50 4B 03 04 (ZIP 头)
- tshark 提取：
  ```bash
  tshark -r secret.pcapng -T fields -e data.len -Y "icmp.type == 8" > out.txt
  ```
- 16 进制转 → zip 文件
- 需要密码，提示 IP

### IP 末位编码
- 提取目的 IP：
  ```bash
  tshark -r secret.pcapng -T fields -e ip.dst -Y "icmp.type == 8" > ip.txt
  ```
- 末位 38 = 0, 39 = 1（猜测二进制）
- 拼成 zip 密码

## 经验提炼
- PNG IDAT 10000+ 块且 CRC 不正常是 CRC 隐写标志
- VeraCrypt 密码本爆破可让 passware kit 跑 10 分钟
- ICMP data.len 字段可编码文件内容
- IP 末位 38/39 二值编码是隐蔽通道
- winhex 工具→打开磁盘→选择挂载盘可恢复已挂载的 VeraCrypt 内容
- CRC 隐写取 IDAT 块前 5 字节（CRC 末字节）
- tshark `-T fields -e data.len` 提取 ICMP 字段
- 公众号签到题关注"春秋伽玛"回复特定关键字
