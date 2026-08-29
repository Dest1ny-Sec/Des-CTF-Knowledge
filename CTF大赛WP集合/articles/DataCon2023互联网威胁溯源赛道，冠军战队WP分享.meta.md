---
title: DataCon2023互联网威胁溯源赛道，冠军战队WP分享
contest: DataCon 2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [threat-hunting, ddos, ntp-flood, slow-http, botnet, p2p, c2, aes-ecb, ptrace]
attack_chain:
  - DDoS 5种：NTP(100源)+UDP(100)+SYN(200)+慢速header(50)+慢速payload(50)
  - 慢速http双向握手→僵尸机真实IP
  - 102.33.5.89跳板机+83.250.118.40被控主机+koko运行
  - 106.167.202.117+104.54.45.183 P2P僵尸节点+SSH爆破
  - AES-ECB窃密流量：16字节分组+全0段+相同明文密文相同
  - 配置文件：root/tsgoingon admin/admin123
  - 加密配置解密→C2 NODE_IP
key_payload: MON_GETLIST字段是NTP反射放大攻击标志
one_liner: DataCon2023威胁溯源：DDoS分类+僵尸机IP+窃密AES-ECB流量
lesson: 慢速http双向握手IP是真实僵尸机；P2P节点IP=僵尸IP
quality: high
---

# DataCon2023互联网威胁溯源赛道，冠军战队WP分享

## 题目信息
- 比赛：DataCon 2023
- 方向：互联网威胁溯源
- 冠军：中科院信工所 Hematopoiesisbshjdkvhbj

## 关键攻击链
### 题目 1：形形色色的 DDoS
- 0-20s：流量包集中发送
- >20s：每 20s 固定数量包
- 502 会话、503 节点
- **MON_GETLIST** 字段 = NTP 反射放大
- 100 个 6-IP 分割响应包 = NTP 反射
- 攻击分类：
  - NTP Flood: 100 源 IP
  - UDP Flood: 100 源 IP
  - SYN Flood: 200 源 IP
  - 慢速 http header 泛洪: 50 源 IP
  - 慢速 http payload 泛洪: 50 源 IP

### 题目 3：藏于幕后的僵网 C2
- 加密配置：
  - `JXNT-C2:1.2.3.4 NODE_IP:104.54.45.183 NODE_PORT:13241`
  - `106.167.202.117:33333`
  - `109.11.12.249:33333`

### 题目 4：消失的窃密流量
- 16 字节分组 + 全 0 段 + ECB 模式相同明文相同密文
- IP 分析：
  - ntp 反射源 IP = ntp server（无关）
  - udp/syn flood 源 IP = 任意伪造
  - 慢速 http 源 IP = 真实僵尸机（100 个）
  - 93.33.5.89 = 跳板机（被控）
  - 83.250.118.40 = koko 运行被控主机
  - 106.167.202.117 / 104.54.45.183 = P2P 僵尸节点 + SSH 爆破

### SSH 凭据
- `root:tsgoingon` / `admin:admin123`
- ptrace(PTRACE_TRACEME, 0, 0, 0) 反调试

## 评分
- quality: high（DDoS 5 类分类 + 真实僵尸机 IP 判定 + AES-ECB 窃密分析）
