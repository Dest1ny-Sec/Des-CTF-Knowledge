---
title: 第二届数据安全大赛暨首届"数信杯"数据安全大赛数据安全积分争夺赛预赛南区- WriteUp By EDISEC
contest: 数信杯数据安全大赛
year: 2023
difficulty: medium
vuln_type: forensic_memory
tags: [应急响应,内存取证,Volatility,Win7SP1x64,SQL盲注,SSRF,RC4,TEA,Crypto,EDI招新]
attack_chain: 数据分析-不安全的U盘1: volatility_2.6_win64_standalone -f 1.raw --profile=Win7SP1x64 printkey→hashdump→lsadump→cmdline→netscan→filescan grep .toml→获取hahaha123/AcroRd32/192.168.31.238:4444/118.180.126.13:6770/attacker.toml|网站数据绝对安全1/2: livwdaw+EccpSOIlRPolP936707|Bitcoin: transferFrom|Web-justsoso: 双写绕SQL注入 aandnd/passwoorrd+binary like+md5+Download.php?img=http://127.0.0.1/flag.php%23 SSRF|Misc-Magic Audio: binwalk→菜就多练密码解zip→flag|Re-rrrrcccc: SMC+RC4+Whatareyourencryption&decryptionbasics+三段XOR|drink tea: TEA delta=555885348
key_payload: volatility...hashdump|hahaha123|flag{49059213-a7e2-4e39-b179-953ae9641063}|flag{61909dd6f4120aac7edb9193491fd83e}|flag{d3db69a34a51d7e1d23d621590827c01}|flag{acb8739759dc496ccc945703037e037f}
one_liner: 6道数据安全题涵盖内存取证(Win7SP1x64 volatility全流程)+SQL盲注双写绕(like binary逐位爆)+Download.php SSRF(#截断)+binwalk音频隐写+RC4+TEA(delta=555885348),末尾EDI招新招re/crypto/pwn方向
lesson: 1) Volatility内存取证全流程:printkey→hashdump→lsadump→cmdline→netscan→filescan grep; 2) SQL盲注双写绕:aandnd(aand and)/passwoorrd(or)/-- '1闭合; 3) like binary逐字符二分爆; 4) Download.php?img=http://127.0.0.1/flag.php%23用#截断本地路径; 5) RC4加密存在SMC自修改; 6) TEA delta可魔改为任意值(本题555885348=0x21212124),需从IDA反编译识别; 7) binwalk提取嵌入文件+已知密码解zip是音频隐写经典套路
quality: medium
---

## 备注

原文(https://www.ctfiot.com/173946.html)开头为EDI招新广告(收re/crypto/pwn方向师傅,邮箱root@edisec.net),后接6题WP+10张附图。

### 题目清单(6题)

**01 数据分析-不安全的U盘1**
- volatility 1.raw Win7SP1x64
- printkey -K "SAM\Domains\Account\Users\Names" → test
- hashdump → test:1000:aad3b435b51404eeaad3b435b51404ee:a06a10e99b2d8d53a7514fd0e73d42e1:::
- lsadump → hahaha123
- cmdline → C:\Program Files (x86)\Adobe\Reader 9.0\Reader\AcroRd32.exe
- netscan → 192.168.31.238:4444 + 118.180.126.13:6770
- filescan | grep .toml → frp配置文件(后缀.toml)→ 攻击者公网IP+端口

**网站的数据绝对安全1/2**
- livwdaw(直接答)
- EccpSOIlRPolP936707(直接答)

**Bitcoin: transferFrom**(直接答,Bitcoin合约函数)

**02 Web-justsoso**
- 双写绕:`aandnd`(aand and)/`passwoorrd`(password)
- `like binary '<prefix>%'` 逐字符爆
- md5(90440ad8ff884788ed99747acb0872c0) → yingyingying
- POST /login.php + X-Forwarded-For:127.0.0.1
- 提示 now you can try Download.php?img=static/image/bg
- Download.php?img=http://127.0.0.1/flag.php%23 → SSRF
- flag{49059213-a7e2-4e39-b179-953ae9641063}

**03 Misc-Magic Audio**
- binwalk找到flag.txt+zip嵌入
- 菜就多练作密码解zip
- flag{61909dd6f4120aac7edb9193491fd83e}

**04 Re-rrrrcccc**
- IDA打开,识别SMC自修改代码
- 反编译识别RC4加密
- 输入'c'*38 + 密文 + 明文"Whatareyourencryption&decryptionbasics"
- 三段XOR:a[i] = a[i] ^ d[i] ^ c[i] ^ f[i]
- flag{d3db69a34a51d7e1d23d621590827c01}

**05 Re-drink tea**
- 魔改TEA,delta = 555885348(=0x21212124)
- key=[1900550021, 2483099539, 2205172504, 1359557939]
- arr=4组2个uint32
- decipher(32, ...) 4次
- flag{acb8739759dc496ccc945703037e037f}

## 评级

- **quality: medium** — 6题payload完整但部分题目只给答案(livwdaw/transferFrom),volatility命令链齐全,SQL注入脚本完整,Re题反编译逻辑清晰
- **vuln_type: forensic_memory** — 主分类内存取证(Win7SP1x64);实际涉及forensic_memory(forensic)、sqli(双写绕+like爆)、ssrf(Download.php%23截断)、stego_audio(binwalk+zip密码)、reverse(SMC+RC4)、block_cipher(TEA魔改)
- 末尾EDI招新招re/crypto/pwn方向师傅,有兴趣可联系
