---
title: 2023 年江苏省信息通信行业网络与信息安全职业技能竞赛决赛 – WriteUp
contest: 江苏信息通信行业网安竞赛 2023
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [php_trick_md5_substr, control%0a绕preg_match, str_replace_data://绕, USB键盘流量, SlientEye隐写, AES秘钥爆破, LCG+费马小定理RSA, 花指令RE]
attack_chain:
  - Web php_trick: substr(path, 32) === md5(path) + path[] 数组绕过
  - con=control%0a 绕 /^control$/ 正则但 !==
  - flag=dadata://ta://text/plain 绕 str_replace + base64 Y3RmZXI=
  - USB 键盘流量解析 vim flag.txt + 9f0adccb...ff0c2f091e49a5dd96
  - SlientEye 隐写：flag{8a497aff3184d4b33000c44150760559}
  - AES 秘钥爆破：key 前 15 位 1016Aes128L12l2 + 末位爆破
  - LCG 6 组输出还原 a,b,m + 费马小定理分解 N
  - RE 花指令 605：patch jmp + 密文两位对调后 -32
key_payload: 'flag=dadata://ta://text/plain;base64,Y3RmZXI='
one_liner: 江苏信息通信综合 7 题：php_trick 多重绕+USB 流量+SlientEye+AES 爆破+LCG+RSA+花指令。
lesson: substr 数组绕过 + con %0a 绕正则 + dadata 协议绕 str_replace；LCG 6 组输出即可还原 a,b,m。
quality: high
---

# 2023 年江苏省信息通信行业网络与信息安全职业技能竞赛决赛 – WriteUp

## 来源
- 原文：ctfiot.com/147695.html
- 团队：EDI 安全（EDISEC）

## 7 道题详解

### Web
1. **php_trick**（多重绕过）
   ```php
   if(!(substr($_GET['path'], 32) === md5($_GET['path']))) {...}
   if(preg_match('/^control$/', $_GET['con']) && $_GET['con'] !== 'control') {...}
   $b = str_replace("data://", "", $a);
   $getflag = file_get_contents($b);
   if($getflag === 'ctfer') { include 'flag.php'; }
   ```
   - `path[]=1` 数组绕过 substr 报错
   - `con=control%0a` 绕正则但 !==
   - `flag=dadata://ta://text/plain;base64,Y3RmZXI=` 绕 str_replace
   - flag: `flag{HUgOMjhlVufsUQKP7f4tsYUeWfi9d09I}`

### Misc
2. **careUSB**（USB 键盘流量）
   ```
   vim<SPACE>flag.txt<RET>i<DOWN1><RET>flag[]<LEFT1>9f0adccbffb79191<DEL>ff0c2f091e49a5dd96...
   ```
   - flag: `flag{9f0adccbffb7919ff0c2f091e49a5d96}`

3. **PE**（SlientEye 隐写）
   - flag: `flag{8a497aff3184d4b33000c44150760559}`

4. **数据安全 1**（base64 隐写 + styles.xml）
   - base64stego 工具梭
   - flag: `flag{db84ecac8eb2375777dcce20c4ba939e}`

5. **数据安全 2**（盲水印）
   - flag: `flag{3cef299383cd6c5d5cc90720d7fbcb61}`

### Crypto
6. **AES 秘钥爆破**
   - key 前 15 位 `1016Aes128L12l2` 已知
   - 末位爆破
   - key = `1016Aes128L12l2y`
   - flag: `flag{373d7743fa45531b786b70e044ab768d}`

7. **LCG + RSA**
   - LCG 6 组输出还原 a, b, m
   - RSA: hint = pow(2023*q+231103, p, n) → 费马小定理分解
   - flag: `flag{1a1cba1971ba474fccbc7d9f7ca7c473}`

### RE
8. **RE605**（花指令 + 字节对调 + -32）
   - 现场 patch jmp 不恢复代码
   - 赛后动调：51→15, 52→25 两位对调，减 32
   - key = 'green_mountains' XOR
   - flag: `flag{a5206bad02483af48c25963266c621e0}`

## 关键技巧
- **substr 数组绕过**：`path[]=1` 触发 substr 警告返回 null
- **%0a 绕正则**：`control\n` 仍匹配 /^control$/ 但 !== 'control'
- **dadata 协议绕 str_replace**：`str_replace("data://", "", $a)` 后留 "data://"
- **LCG 攻击**：6 组输出 → gcd 算 m
- **花指令 patch**：jmp 改 nop 还原逻辑

## 适用场景
- PHP 多重绕过组合
- USB 流量分析
- AES 爆破末位
- LCG 密码学攻击
- RE 花指令
