---
title: 破解 iTunes 备份密码 by EDI
contest: 美亚杯
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags: [iTunes-backup, hashcat, MySQL-300, sha512-1800, NT-1000, LM-3000, MSSQL-132, WordPress-400, RAR-13000, ZIP-13600, Office-9600, WiFi-2500]
attack_chain:
  - Mac 备份路径: ~/Library/Application Support/MobileSync/Backup/
  - iTunes 备份 hash 格式: $itunes_backup$*9*<WPKY>**<SALT>**
  - hashcat -m 14700 (iTunes Backup < 10.0) -a 3 字典攻击
  - hashcat -m 300 MySQL (?d?d?d?d?d?d)
  - hashcat -m 1800 sha512 ($6$mxuA5cdy$... ?l?l?l?l)
  - hashcat -m 1000 NT-Hash (209C6174DA490CAEB422F3FA5A7AE634 ?l?l?l?l?l)
  - hashcat -m 3000 LM-Hash (F0D412BD764FFE81AAD3B435B51404EE ?l?l?l?l?l)
  - hashcat -m 132 MSSQL (0x01008c80... ?l?l?l?l?l?d?d?d)
  - hashcat -m 400 WordPress ($P$BYEYcHEj3vDhV1lwGBv6rpxurKOEWY/ ?d?d?d?d?d?d)
  - hashcat -m 2611 Discuz (14e1b600b1fd579f47433b88e8d85291: ?d?d?d?d?d?d)
  - rar2john + hashcat -m 13000 RAR
  - zip2john + hashcat -m 13600 ZIP
  - office2john + hashcat -m 9600 Office
  - cap2hccapx + hashcat -m 2500 WiFi
key_payload: 'hashcat -m 14700 $itunes_backup$*9*<WPKY>**<SALT>** ?d?d?d?d...'
one_liner: EDI 招新广告 + 2022 美亚杯经验：iTunes 备份 + MySQL + sha512 + NT/LM + WordPress + RAR/ZIP/Office 全部 hashcat 一把梭。
lesson: hashcat mode 编号是密码学必背知识点；john the ripper 工具链（rar2john/zip2john/office2john）+ cap2hccapx 是 CTF 取证标配。
quality: medium
---

# 破解 iTunes 备份密码

**来源**: ctfiot.com ID 74033
**战队**: EDI 安全（招新广告）
**出处**: 2022 美亚杯经验

## iTunes 备份 hash 格式
```
$itunes_backup$*<ver>*<WPKY>**<SALT>*
```

例如：
```
$itunes_backup$*9*c1212e8754a1db6dfddc4fc6a386795eda88c18b865742e6fbd961b13e3229efda50dc0b69bdfc2e*10000*2b06ba3c6281ce101a0bd0249c1203cc9c8da1a8**
```

## hashcat 各种模式

### iTunes Backup < 10.0
```bash
hashcat64 -m 14700 -a 3 "$itunes_backup$*9*<WPKY>**<SALT>**" ?d?d?d?d ?d?d?d?d
```

### MySQL
```bash
hashcat64.exe -a 3 -m 300 --force 6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9 ?d?d?d?d?d?
```

### sha512
```bash
hashcat64.exe -a 3 -m 1800 --force $6$mxuA5cdy$XZRk0CvnPFqOgVopqiPEFAFK72SogKVwwwp7gWaUOb7b6tVwfCpcSUsCEk64ktLLYmzyew/xd0O0hPG/yrm2X. ?l?l?l?l
```

### NT-Hash
```bash
hashcat64.exe -a 3 -m 1000 209C6174DA490CAEB422F3FA5A7AE634 ?l?l?l?l?l
```

### LM-Hash
```bash
hashcat64.exe -a 3 -m 3000 F0D412BD764FFE81AAD3B435B51404EE ?l?l?l?l?l
```

### MSSQL
```bash
hashcat64.exe -a 3 -m 132 --force 0x01008c8006c224f71f6bf0036f78d863c3c4ff53f8c3c48edafb ?l?l?l?l?l?d?d?d
```

### WordPress
```bash
hashcat64.exe -a 3 -m 400 --force $P$BYEYcHEj3vDhV1lwGBv6rpxurKOEWY/ ?d?d?d?d?d?d
```

### Discuz
```bash
hashcat64.exe -a 3 -m 2611 --force 14e1b600b1fd579f47433b88e8d85291: ?d?d?d?d?d?d
```

### RAR
```bash
rar2john.exe 1.rar
hashcat64.exe -a 3 -m 13000 --force $rar5$16$639e9ce8344c680da12e8bdd4346a6a3$15$a2b056a21a9836d8d48c2844d171b73d$8$04a52d2224ad082e ?d?d?d?d?d?d
```

### ZIP
```bash
zip2john.exe 1.zip
hashcat64.exe -a 3 -m 13600 $zip2$*0*3*0*554bb43ff71cb0cac76326f292119dfd*ff23*5*24b28885ee*d4fe362bb1e91319ab53*$/zip2$ --force ?d?d?d?d?d?d
```

### Office
```bash
python office2john.py 11.docx
hashcat64.exe -a 3 -m 9600 $office$*2013*100000*256*16*e4a3eb62e8d3576f861f9eded75e0525*9eeb35f0849a7800d48113440b4bbb9c*577f8d8b2e1c5f60fed76e62327b38d28f25230f6c7dfd66588d9ca8097aabb9 --force ?d?d?d?d?d?d
```

### WiFi
```bash
# https://hashcat.net/cap2hccapx/
hashcat64.exe -a 3 -m 2500 1.hccapx 1391040?d?d?d?d
```

## 参考
- iPhone 数据保护深入: http://esec-lab.sogeti.com/static/publications/11-hitbamsterdam-iphonedataprotection.pdf
- iphone-dataprotection code: https://code.google.com/archive/p/iphone-dataprotection/

## 评价
EDI 招新广告 + 2022 美亚杯密码学 hashcat 工具应用集合。hashcat 模式编号是 CTF 取证必背技能。
