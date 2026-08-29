---
title: 2025 高校网络安全管理运维赛-电子取证分析师赛道-决赛 WriteUp
contest: 2025 高校网络安全管理运维赛
year: 2025
difficulty: medium
vuln_type: [forensic_disk, forensic_memory, misc_unknown]
tags: [高校网络安全管理运维赛 2025 决赛, 电子取证分析师, 签到题 gif 分帧组合扫码, log 日志 awk 过滤, MD5 11cd6a875898416+6c37ac826a2a04bc, 3c6e0b8a9c15224a 解密密钥, pcap redis/1234567qwerc Caddy /usr/share/caddy/testinfo.php, VeraCrypt 加密卷 SM3 校验, Keepass ironbox.safe PqR$34%sTuVwX, 用户名 maaiyu, U 盘 jetflash, RAID lvscan 挂载对比]
attack_chain:
  - 签到: gif 分帧-组合-画图-拼接-扫码
  - 谁真正执行命令: log awk 过滤
  - 网络流量 MD5 解密: 11cd6a875898416+6c37ac826a2a04bc → 3c6e0b8a9c15224a
  - PACPdfir-pcap: flag{redis}, flag{1234567qwerc}, flag{/usr/share/caddy/testinfo.php}
  - DFIR-archer: 账户创建时间 2022-02-05 00:25:26
  - Keepass ironbox.safe 密码 PqR$34%sTuVwX
  - VeraCrypt SM3 校验: ce4a2f20ebc2bcdce729885ae12fb3de0a7231e6c0a8dc1cc050605f9f8f1663
  - DFIR-rensom: 用户 maaiyu, U 盘 jetflash
  - DFIR-RAID: lvscan + mount + diff -r back new
key_payload: "Keepass ironbox.safe → PqR$34%sTuVwX"
one_liner: 2025 高校网络安全管理运维赛电子取证分析师决赛：签到 GIF + log awk + PACP pcap + Keepass + VeraCrypt + 勒索恢复 + RAID 对比。
lesson: 高校运维赛取证赛道覆盖签到/log/pcap/账户/Keepass/VeraCrypt/勒索/RAID 全栈；Keepass 主密码 PqR$34%sTuVwX 需 keepass2john + john 爆破；VeraCrypt SM3 是国密场景。
quality: medium
---

# 2025 高校网络安全管理运维赛-电子取证分析师赛道-决赛 WriteUp

## 题目列表与答案

### 签到题
gif 文件 → 分帧-组合-画图-拼接-扫码。

### 谁真正执行了命令？
log 日志文件 → Kali `awk` 过滤 或肉眼看。
**flag{b1bdef37df1a7acec711e97568c8e3b8}**

### 网络流量中的巨兽踪迹 god
```
11cd6a875898416+6c37ac826a2a04bc
```
MD5 解密密钥 = `3c6e0b8a9c15224a`

### MISC-PACPdfir-pcap
- **flag{redis}** （Redis 数据）
- **flag{1234567qwerc}** （Caddy 密码）
- **flag{/usr/share/caddy/testinfo.php}** （路径）

### DFIR-archer
- RSA 公钥: `flag{42DDE4A368FD17641E8B56017081A5B00CAB11B89FD88495E3FE2D684A9F3DC9}`
- archer 用户创建时间: `flag{2022-02-05 00:25:26}`
- Keepass ironbox.safe 密码: `flag{PqR$34%sTuVwX}`
- VeraCrypt Excel 热成像图片 SM3 校验值: `flag{ce4a2f20ebc2bcdce729885ae12fb3de0a7231e6c0a8dc1cc050605f9f8f1663}`
- 热成像图片内容: `flag{hereyouare}`

### DFIR-rensom（勒索病毒恢复）
- 主机用户姓名全拼: `flag{maaiyu}`
- 最近一次插过的 U 盘厂商: `flag{jetflash}`
- 电脑 OEM 厂商品牌: `flag{???}`

### DFIR-RAID
```bash
blkid  # 列出所有分区的 UUID、文件系统类型
lsblk -f
systemctl list-unit-files | grep dlna
find / -name *dlna*
cd /usr/trim/bin/minidlnad -V
lvscan  # 查看挂载的盘，发现有两个
mkdir new back
mount /dev/newnew/vol1 new
mount /dev/newnew/back back
diff -r back new  # 对比两个文件 -r 递归
```

## 战队
- 鱼影安全社区（CSDN: Aluxian_）
