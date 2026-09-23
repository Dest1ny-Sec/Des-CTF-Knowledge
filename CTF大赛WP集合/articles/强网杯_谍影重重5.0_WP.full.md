---
title: 强网杯 谍影重重5.0
contest: 强网杯 (Qiangwang)
year: 2024
difficulty: hard
vuln_type:
- forensic_disk
- stego_traffic
- misc_unknown
tags:
- NTLMv2
- tshark
- pcapng
- NTLMSSP
- hashcat
- rockyou
- ARC4
- MD4-MD5-HMAC
- SMB-Session-Key
- RDP
- scancode
- fastpath
- keycode
attack_chain:
- tshark 提取 NTLMSSP NTLMv2 认证字段
- hashcat -m 5600/rockyou 爆破 tom 密码 babygirl233
- MD4+HMAC-MD5 推 responseKey/keyExchangeKey
- ARC4 解密 SMB session key 解密后续 SMB 流量
- tshark 提 rdp.fastpath.scancode.keycode 还原键盘记录
key_payload: tom::.:c1dec53240124487:ca32f9b5b48c04ccfa96f35213d63d75:0101...2900
one_liner: NTLMSSP 离线爆破 + SMB 会话密钥解密 + RDP 键盘还原
lesson: pcapng 含 NTLMv2 时可直接 hashcat 爆破密码；session key 解密后才有 SMB 流量；RDP fastpath scancode 是键码记录可还原键盘输入
quality: medium
full_path: 强网杯_谍影重重5.0_WP.full.md
meta_path: 强网杯_谍影重重5.0_WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 强网杯 谍影重重5.0。NTLMSSP 离线爆破 + SMB 会话密钥解密 + RDP 键盘还原。关键路径：tshark 提取 NTLMSSP NTLMv2 认证字段 → hashcat -m 5600/rockyou 爆破 tom 密码 babygirl233 → MD4+HMAC-MD5 推 responseKey/keyExchangeKey。经验：pcapng 含 NTLMv2 时可...
category: forensic
subcategory: disk_forensics
subcategories:
- disk_forensics
- stego
- misc_other
tools_used:
- hashcat
- tshark
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/213700.html
reasoning_chain:
- 题目给 dy.pcapng + traffic.pcapng → 触发点：tshark 看到 NTLMSSP messagetype 0x00000003 类型认证
- 假设：能直接爆破 NTLMv2 密码 → 动作：tshark -Y 'ntlmssp.messagetype==0x00000003' -T fields 提取 username/domain/ntproofstr/ntresponse
- 观察：用户 tom 域 . → 动作：hashcat -m 5600 -a 0 rockyou.txt 爆破 → 观察：密码 babygirl233
- 假设：必须解 SMB session key 才能看后续 SMB 流量 → 动作：MD4+HMAC-MD5 推 responseKey/keyExchangeKey
- 动作：ARC4(keyExchangeKey).decrypt(sessionKey) → 观察：得到 decryptedSessionKey
- 触发点：后续 pcapng 是 RDP fastpath scancode.keycode → 假设：键码还原键盘输入
- 动作：tshark -Y 'rdp.fastpath' -T fields -e scancode.keycode + 自建 scancode_map → 观察：还原键盘记录
failed_attempts:
- 试图不解 SMB session key 直接看 SMB 内容 → 失败：加密
- 试图用 john 替代 hashcat → 失败：john 对 NTLMv2 支持较弱
- 试图不解 RDP 还原键盘输入 → 失败：fastpath 没解看不出来
key_observations:
- pcapng 含 NTLMv2 时可直接 hashcat -m 5600/rockyou 爆破密码
- NTLMSSP messagetype 0x03 是 challenge-response 阶段
- MD4+HMAC-MD5 推 responseKey/keyExchangeKey 是 NTLM 标准算法
- session key 解密后才有 SMB 流量可见性
- RDP fastpath scancode.keycode 是键码记录，可逐字节还原键盘输入
prerequisites:
- tshark 命令行（-Y 过滤 / -T fields 提取）
- NTLMv2 认证协议（NTLMSSP messagetype）
- hashcat 模式 5600 (NTLMv2) + 字典攻击
- MD4/HMAC-MD5/ARC4 加密原语
---
# 强网杯 谍影重重5.0 WP

> 原文: https://www.ctfiot.com/213700.html
> ID: 213700

# username domain ntproofstr ntresponsetshark -n -r dy.pcapng -Y 'ntlmssp.messagetype == 0x00000003' -T fields -e ntlmssp.auth.username -e ntlmssp.auth.domain -e ntlmssp.ntlmv2_response.ntproofstr -e ntlmssp.auth.ntresponse
# ntlmserverchallenge$ tshark -n -r traffic.pcapng -Y 'ntlmssp.messagetype == 0x00000002' -T fields -e ntlmssp.ntlmserverchallenge

tom::.:
c1dec53240124487:
ca32f9b5b48c04ccfa96f35213d63d75:
010100000000000040d0731fb92adb01221434d6e24970170000000002001e004400450053004b0054004f0050002d004a0030004500450039004d00520001001e004400450053004b0054004f0050002d004a0030004500450039004d00520004001e004400450053004b0054004f0050002d004a0030004500450039004d00520003001e004400450053004b0054004f0050002d004a0030004500450039004d0052000700080040d0731fb92adb0106000400020000000800300030000000000000000100000000200000bd69d88e01f6425e6c1d7f796d55f11bd4bdcb27c845c6ebfac35b8a3acc42c20a001000000000000000000000000000000000000900260063006900660073002f003100370032002e00310036002e003100300035002e003100320039000000000000000000

from Crypto.Cipher import ARC4from Crypto.Hash import MD4, MD5, HMAC
password = 'babygirl233'passwordHash = MD4.new(password.encode('utf-16-le')).hexdigest()username = 'tom'domain = '.'ntProofStr = 'ca32f9b5b48c04ccfa96f35213d63d75'serverChallenge = 'c1dec53240124487'sessionKey = '5643a37f253b00b2f52df1afd48c1514'
responseKey = HMAC.new(bytes.fromhex(passwordHash), (username.upper()+domain.upper()).encode('utf-16-le'), MD5).digest()keyExchangeKey = HMAC.new(responseKey, bytes.fromhex(ntProofStr), MD5).digest()decryptedSessionKey = ARC4.new(keyExchangeKey).decrypt(bytes.fromhex(sessionKey))print('Decrypted SMB Session Key is: {}'.format(decryptedSessionKey.hex()))

import json
from jsonpath import jsonpath
scancode_map = { 0x01: 'Esc', 0x02: '1', 0x03: '2', 0x04: '3', 0x05: '4', 0x06: '5', 0x07: '6', 0x08: '7', 0x09: '8', 0x0A: '9', 0x0B: '0', 0x0C: '-', 0x0D: '=', 0x0E: 'b', 0x0F: ' ', 0x10: 'Q', 0x11: 'W', 0x12: 'E', 0x13: 'R', 0x14: 'T', 0x15: 'Y', 0x16: 'U', 0x17: 'I', 0x18: 'O', 0x19: 'P', 0x1A: '[', 0x1B: ']', 0x1C: 'n', 0x1D: 'Ctrl', 0x1E: 'A', 0x1F: 'S', 0x20: 'D', 0x21: 'F', 0x22: 'G', 0x23: 'H', 0x24: 'J', 0x25: 'K', 0x26: 'L', 0x27: ';', 0x28: ''', 0x29: '`', 0x2A: ' Shift ', 0x2B: '\', 0x2C: 'Z', 0x2D: 'X', 0x2E: 'C', 0x2F: 'V', 0x30: 'B', 0x31: 'N', 0x32: 'M', 0x33: ',', 0x34: '.', 0x35: '/', 0x36: ' Shift ', 0x37: '*', 0x38: ' Left Alt ', 0x39: ' ', 0x3A: ' Caps Lock ', 0x3B: ' F1 ', 0x3C: ' F2 ', 0x3D: ' F3 ', 0x3E: ' F4 ', 0x3F: ' F5 ', 0x40: ' F6 ', 0x41: ' F7 ', 0x42: ' F8 ', 0x43: ' F9 ', 0x44: ' F10 ', 0x45: ' Num Lock ', 0x46: ' Scroll Lock ', 0x47: ' Home ', 0x48: ' Up Arrow ', 0x49: ' Page Up', 0x4A: ' Keypad -', 0x4B: ' Left Arrow', 0x4C: ' Keypad 5', 0x4D: ' Right Arrow', 0x4E: ' Keypad +', 0x4F: ' End', 0x50: ' Down Arrow', 0x51: ' Page Down', 0x52: ' Insert', 0x53: ' Delete', 0x57: ' F11', 0x58: ' F12'}
def convert_hex_string(hex_string): # 去掉前缀并转换为大写 if hex_string.startswith('0x'): hex_value = hex_string[2:].upper() return f'0x{hex_value}' return None # 如果字符串不以'0x'开头，返回None

with open("out.txt","r",encoding="utf-8") as file: lines = file.readlines()
con=[]for line in lines: con.append(line.strip('n'))
print(con)print("n")
for i in range (len(con)): if con[i]==con[i-1]: continue try: print(scancode_map[int(con[i],16)],end="") 
except: pass


```
# username domain ntproofstr ntresponsetshark -n -r dy.pcapng -Y 'ntlmssp.messagetype == 0x00000003' -T fields -e ntlmssp.auth.username -e ntlmssp.auth.domain -e ntlmssp.ntlmv2_response.ntproofstr -e ntlmssp.auth.ntresponse
# ntlmserverchallenge$ tshark -n -r traffic.pcapng -Y 'ntlmssp.messagetype == 0x00000002' -T fields -e ntlmssp.ntlmserverchallenge
tom::.:
c1dec53240124487:
ca32f9b5b48c04ccfa96f35213d63d75:
010100000000000040d0731fb92adb01221434d6e24970170000000002001e004400450053004b0054004f0050002d004a0030004500450039004d00520001001e004400450053004b0054004f0050002d004a0030004500450039004d00520004001e004400450053004b0054004f0050002d004a0030004500450039004d00520003001e004400450053004b0054004f0050002d004a0030004500450039004d0052000700080040d0731fb92adb0106000400020000000800300030000000000000000100000000200000bd69d88e01f6425e6c1d7f796d55f11bd4bdcb27c845c6ebfac35b8a3acc42c20a001000000000000000000000000000000000000900260063006900660073002f003100370032002e00310036002e003100300035002e003100320039000000000000000000
hashcat hash3.txt rockyou.txt
from Crypto.Cipher import ARC4from Crypto.Hash import MD4, MD5, HMAC
password = 'babygirl233'passwordHash = MD4.new(password.encode('utf-16-le')).hexdigest()username = 'tom'domain = '.'ntProofStr = 'ca32f9b5b48c04ccfa96f35213d63d75'serverChallenge = 'c1dec53240124487'sessionKey = '5643a37f253b00b2f52df1afd48c1514'
responseKey = HMAC.new(bytes.fromhex(passwordHash), (username.upper()+domain.upper()).encode('utf-16-le'), MD5).digest()keyExchangeKey = HMAC.new(responseKey, bytes.fromhex(ntProofStr), MD5).digest()decryptedSessionKey = ARC4.new(keyExchangeKey).decrypt(bytes.fromhex(sessionKey))print('Decrypted SMB Session Key is: {}'.format(decryptedSessionKey.hex()))
rdp.fastpath.scancode.keycode
import json
from jsonpath import jsonpath
scancode_map = { 0x01: 'Esc', 0x02: '1', 0x03: '2', 0x04: '3', 0x05: '4', 0x06: '5', 0x07: '6', 0x08: '7', 0x09: '8', 0x0A: '9', 0x0B: '0', 0x0C: '-', 0x0D: '=', 0x0E: 'b', 0x0F: ' ', 0x10: 'Q', 0x11: 'W', 0x12: 'E', 0x13: 'R', 0x14: 'T', 0x15: 'Y', 0x16: 'U', 0x17: 'I', 0x18: 'O', 0x19: 'P', 0x1A: '[', 0x1B: ']', 0x1C: 'n', 0x1D: 'Ctrl', 0x1E: 'A', 0x1F: 'S', 0x20: 'D', 0x21: 'F', 0x22: 'G', 0x23: 'H', 0x24: 'J', 0x25: 'K', 0x26: 'L', 0x27: ';', 0x28: ''', 0x29: '`', 0x2A: ' Shift ', 0x2B: '\', 0x2C: 'Z', 0x2D: 'X', 0x2E: 'C', 0x2F: 'V', 0x30: 'B', 0x31: 'N', 0x32: 'M', 0x33: ',', 0x34: '.', 0x35: '/', 0x36: ' Shift ', 0x37: '*', 0x38: ' Left Alt ', 0x39: ' ', 0x3A: ' Caps Lock ', 0x3B: ' F1 ', 0x3C: ' F2 ', 0x3D: ' F3 ', 0x3E: ' F4 ', 0x3F: ' F5 ', 0x40: ' F6 ', 0x41: ' F7 ', 0x42: ' F8 ', 0x43: ' F9 ', 0x44: ' F10 ', 0x45: ' Num Lock ', 0x46: ' Scroll Lock ', 0x47: ' Home ', 0x48: ' Up Arrow ', 0x49: ' Page Up', 0x4A: ' Keypad -', 0x4B: ' Left Arrow', 0x4C: ' Keypad 5', 0x4D: ' Right Arrow', 0x4E: ' Keypad +', 0x4F: ' End', 0x50: ' Down Arrow', 0x51: ' Page Down', 0x52: ' Insert', 0x53: ' Delete', 0x57: ' F11', 0x58: ' F12'}
def convert_hex_string(hex_string): # 去掉前缀并转换为大写 if hex_string.startswith('0x'): hex_value = hex_string[2:].upper() return f'0x{hex_value}' return None # 如果字符串不以'0x'开头，返回None

with open("out.txt","r",encoding="utf-8") as file: lines = file.readlines()
con=[]for line in lines: con.append(line.strip('n'))
print(con)print("n")
for i in range (len(con)): if con[i]==con[i-1]: continue try: print(scancode_map[int(con[i],16)],end="") 
except: pass
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]