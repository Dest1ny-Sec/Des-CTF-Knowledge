---
title: 软件系统安全赛-traffic_hunt
contest: 软件系统安全赛
year: 2026
difficulty: hard
vuln_type: forensic_disk
tags: [Behinder-webshell, AES-ECB-MD5, pcap-analysis, traffic-encryption, tshark, AES-GCM, python-pack, C2-implant, base64-extract, ELF-reassemble]
attack_chain:
- HTTP协议前半部分:目录扫描(404状态)
- 第404205包开始:植入Java class文件(冰蝎马第一阶段)
- 反编译class:使用p参数值的MD5前16字节作为AES ECB密钥
- p=HWmc2TLDoihdlr0N,key=1f2c8075acd3d118
- 后续流量:AES ECB加密的冰蝎载荷,tshark提取frame.number 404652-412212的POST data
- 攻击者用冰蝎文件上传模块,文件分片(blockIndex乱序)
- 前10文件顺序:404339(2)→404376(5)→404433(4)→404440(9)→404461(0)→404488(7)→404513(3)→404575(8)→404578(1)→404615(6)
- 11-349文件按blockIndex顺序,最后3个:412223(351)→412240(349)→412271(350)
- 拼接得ELF文件,运行发现是python打包
- pycdc反编译pyc:C2植入物,AES-GCM加密,key=IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs=
- 报文:4 bytes长度|12 bytes nonce|n bytes密文|16 bytes GCM tag
- 解密冰蝎后流量得flag: dart{d9850b27-85cb-4777-85e0-df0b78fdb722}
key_payload: dart{d9850b27-85cb-4777-85e0-df0b78fdb722}
one_liner: 软件系统安全赛traffic_hunt流量分析,冰蝎马AES-ECB+MD5(p)密钥推导+分片文件上传(blockIndex乱序重组)+Python pyc C2植入物+AES-GCM后渗透通信解密。
lesson: 冰蝎马用MD5(p)前16字节作AES-ECB密钥是标准实现;分片文件上传blockIndex乱序是流量侧的检测规避;Python打包的ELF+pyc反编译是C2分析常见路径;AES-GCM(4B长度+12B nonce+n字节密文+16B tag)是自定义协议稳定格式。
quality: high
---

## 题目列表

1道流量分析:traffic_hunt

## 关键考点

### 冰蝎马分析
- 第一阶段:Java class文件,反编译
- 关键:`p`参数值的MD5前16字节作为AES ECB密钥
- 流程:每个阶段用第一阶段载荷请求头中的`p`值 → md5(p)[:16] → AES ECB密钥

### 关键密钥
- p = HWmc2TLDoihdlr0N
- md5(p)[:16] = 1f2c8075acd3d118
- AES-ECB解密后续冰蝎载荷

### 文件分片重组
- 冰蝎分片上传(规避流量侧检测)
- blockIndex乱序
- 前10文件顺序:
  - 404339→2
  - 404376→5
  - 404433→4
  - 404440→9
  - 404461→0
  - 404488→7
  - 404513→3
  - 404575→8
  - 404578→1
  - 404615→6
- 11-349按blockIndex顺序
- 350-352:412223→351, 412240→349, 412271→350

### AES-ECB分片解密
- tshark提取frame.number 404652-412212的POST data
- AES.new(KEY, AES.MODE_ECB).decrypt(ciphertext)
- 正则匹配`[A-Za-z0-9+/]{100,}={0,2}` 提取base64
- 拼接后10 + 中间 + 后3 → 完整ELF

### Python打包分析
- ELF运行发现是PyInstaller打包
- pyinstxtractor + pycdc反编译
- C2植入物pyc:
  - SERVER_LISTEN_IP:10.1.243.155
  - SERVER_LISTEN_PORT:7788
  - AES-GCM加密通信
  - set_aes_key, encrypt_data, decrypt_data

### AES-GCM后渗透通信
- 攻击者传入aes-key=IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs=
- 报文格式:4B长度|12B nonce|n字节密文|16B GCM tag
- 解密后通信得flag

### flag
- `dart{d9850b27-85cb-4777-85e0-df0b78fdb722}`

## 实战价值
- 冰蝎马MD5(p)[:16]密钥推导是WebShell分析标准方法
- 分片文件上传blockIndex乱序重组是流量侧检测规避研究热点
- PyInstaller打包+pyc反编译是恶意软件分析常见路径
- AES-GCM(长度+nonce+密文+tag)格式是C2协议稳定结构
- tshark + 正则 + base64是流量分析三件套
