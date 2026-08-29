---
title: 2023 年春秋杯春季赛 - WriteUp By EDISEC
contest: 春秋杯春季赛 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [phpstudy漏洞, numpy_pickle, qqcms_SSTI, ezrust, php_again_opcache, sudo提权, Pell方程, EC_ElGamal, 数独md5, VMP_UPX, z3求解, EDISEC]
attack_chain:
  - Web phpstudy: 修改 admin 密码 + 勾选系统权限 + 查看文件下载 flag
  - Web easypy: numpy.loads(pickle) opcode 手搓 + base64 编码过滤 R
  - Web qqcms: SSTI 模板注入 {{loop sql=...}} 改密码 + 文件包含读 flag
  - Web ezrust: 当前目录即 work，./flag 路径穿越
  - Web php_again: opcache file_cache + bind_id + 修改 bin 文件时间戳上传
  - Misc sudo: nano -- /flag 提权读 flag
  - Misc piphack: socket AF_UNIX + pickle 反序列化 + SCM_RIGHTS
  - Misc wordle: 猜单词
  - Misc 58与64: 14268 个 base58 编码 + base64 套娃
  - Crypto checkin: Pell 方程 N=1117 + 二项式展开
  - Crypto cr2: EC-ElGamal + SHA256 k2 + MD5 key + AES-ECB
  - RE sum: 数独 + 9 个 1-9 之和=405 + md5(405)
  - RE Poisoned_tea: VMP 字符串改 UPX + upx 4.0.2 脱壳 + TEA 36 轮
  - RE Pytrans: pyinstxtractor 解包 + uncopyle6 反编译 + z3 约束求解
key_payload: 'pell N=1117, key[]={0x05,0x02,9,7,0}, 数独和 405, md5(405)=bbcbff5c...'
one_liner: 春秋杯 EDISEC 11 题：phpstudy+pickle+SSTI+Pell+EC_ElGamal+数独 md5+TEA 36 轮+pyinstxtractor。
lesson: 数独答案 9 个 1-9 之和恒为 405，md5 即可；VMP 字符串改 UPX 是经典脱壳绕过；pyinstxtractor+uncopyle6 解 PyInstaller。
quality: high
---

# 2023 年春秋杯春季赛 - WriteUp By EDISEC

## 来源
- 原文：ctfiot.com/116586.html
- 团队：EDI 安全（EDISEC）

## 11 道题详解

### WEB
1. **phpstudy**（修改 admin 密码 + 文件下载）
2. **easypy**（pickle + numpy.loads + 字符过滤）
3. **qqcms**（SSTI 模板注入改密 + 文件包含读 flag）
4. **ezrust**（路径穿越 `./flag`）
5. **php_again**（opcache file_cache + 时间戳绕过）

### MISC
6. **sudo**（`EDITOR='nano -- /flag' sudoedit /etc/GAMELAB` 提权）
7. **piphack**（socket AF_UNIX + SCM_RIGHTS + pickle）
8. **wordle**（猜单词）
9. **盲人隐藏了起来**（补文件头 + zsteg）
10. **happy2forensics**（BitLocker 取证）
11. **58 与 64**（base58 + base64 套娃）

### CRYPTO
12. **checkin**（Pell 方程 N=1117）
13. **cr2**（EC-ElGamal + SHA256 k2 + MD5 key + AES-ECB）

### RE
14. **sum**（数独 + md5(405)）
15. **Poisoned_tea**（VMP 改 UPX + TEA 36 轮）
16. **Pytrans**（pyinstxtractor + z3 约束求解）

## 关键技巧
- **数独之和恒为 405**：9 行 1-9 之和 = 1+2+...+9 = 45，每行 45，共 9 行 = 405
- **md5(405) = bbcbff5c1f1ded46c25d28119a85c6c2**
- **VMP 改 UPX**：HxD 替换字符串
- **opcache 绕过**：修改 bin 文件时间戳与服务器一致
- **pyinstxtractor**：PyInstaller 解包工具
- **z3 约束求解**：BitVec 线性方程组

## 适用场景
- phpstudy 后渗透
- pickle 反序列化
- SSTI 模板注入
- Pell 方程
- EC-ElGamal 加密
- 经典 RE 加固
