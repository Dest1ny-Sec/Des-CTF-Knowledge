---
title: NahamCon 2023 Writeup (JPEG 隐写 + Windows 加密 + qemu 镜像)
contest: NahamCon
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [JPEG 隐写, stegoveritas, PowerShell AES 加密, hayabusa 事件日志, qemu-img vmdk→vhdx]
attack_chain: |
  1. JPEG 隐写:
     - pip3 install stegoveritas + stegoveritas_install_deps
     - stegoveritas tiny-little-fibers.jpg
     - 手动解析 JPEG marker: 跳过 nonLenMarkers (FFD8/FF01/FFD0-FFD7)
     - 找到 FFD9 (End of Image) 后继续读 = trailing data
  2. PowerShell AES 加密 (encryptFiles.ps1):
     - $cipher.key = "7h3_k3y_70_unl0ck_4ll_7h3_f1l35!" (32 字节 AES-256)
     - $cipher.GenerateIV() + $FileStreamWriter.Write(iv) + CryptoStream
     - 攻击: 拿 key → 解密所有 .enc 文件
  3. Windows hayabusa 事件日志分析:
     - .ova (vmware) → tar → 解压 → vmdk → qemu-img convert -f vmdk -O vhdx out.vhdx
     - hayabusa-2.5.1-win-x64.exe csv-timeline -d "E:\Windows\System32\winevt\Logs" -o result.csv
  4. $flag = "flag{892a8921517dcecf90685d478aedf5e2}"
key_payload: |
  # JPEG 隐写 (FFD9 后的 trailing data):
  nonLenMarkers = [b'\xff\xd8', b'\xff\x01', b'\xffd0', b'\xffd1', b'\xffd2', b'\xffd3', b'\xffd4', b'\xffd5', b'\xffd6', b'\xffd7']
  with open(image.veritas.file_name, "rb") as myFile:
      steg = myFile.read()
  while True:
      hdr = steg[i:i+2]
      if hdr in nonLenMarkers:
          i = i + 2
          continue
      if hdr == b'\xff\xd9':
          i += 2
          break
      ln = unpack(">H", steg[i+2:i+4])[0]
      i = i + ln + 2
      if hdr == b'\xff\xda':
          i += steg[i:].index(b'\xff\xd9')
      if i != len(steg):
          # Trailing data
          with open(output_file, "wb") as outFile:
              outFile.write(steg[i:])
  
  # PowerShell AES 加密解密 (7h3_k3y_70_unl0ck_4ll_7h3_f1l35!):
  $cipher.key = [System.Text.Encoding]::UTF8.GetBytes("7h3_k3y_70_unl0ck_4ll_7h3_f1l35!")
  $cipher.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
  $cipher.GenerateIV()
  $FileStreamWriter.Write([System.BitConverter]::GetBytes($cipher.IV.Length), 0, 4)
  $FileStreamWriter.Write($cipher.IV, 0, $cipher.IV.Length)
  
  # qemu vmdk → vhdx:
  mv nahamcon.ova nahamcon.tar
  tar -xvf nahamcon.tar
  qemu-img convert -f vmdk -O vhdx "Nahamcon Forensics Challenge-disk001.vmdk" out.vhdx
  hayabusa-2.5.1-win-x64.exe csv-timeline -d "E:\Windows\System32\winevt\Logs" -o result.csv
one_liner: NahamCon 2023: JPEG FFD9 trailing 隐写 + PowerShell AES-256 加密 (key "7h3_k3y_70_unl0ck_4ll_7h3_f1l35!") + qemu-img vmdk 转 vhdx + hayabusa 事件日志分析。
lesson: |
  - JPEG 隐写: 找 FFD9 (End of Image) 后的 trailing data
  - PowerShell SymmetricAlgorithm + AES-256 + IV 写文件头是 ransomware 标准做法
  - key "7h3_k3y_70_unl0ck_4ll_7h3_f1l35!" 是硬编码, 容易逆
  - qemu-img convert vmdk → vhdx 是 Windows 取证标准流程
  - hayabusa 是 Windows 事件日志快速分析工具
  - flag 来自事件日志 (flag{892a8921517dcecf90685d478aedf5e2})
quality: high
---

# NahamCon 2023 Writeup

> 来源: ctfiot.com 120878

## JPEG 隐写 (stegoveritas)

```bash
pip3 install stegoveritas
sudo stegoveritas_install_deps
stegoveritas tiny-little-fibers.jpg
```

手动解析 JPEG marker：
```python
nonLenMarkers = [b'\xff\xd8', b'\xff\x01', b'\xffd0', b'\xffd1', b'\xffd2', b'\xffd3', b'\xffd4', b'\xffd5', b'\xffd6', b'\xffd7']
with open(image.veritas.file_name, "rb") as myFile:
    steg = myFile.read()
while True:
    hdr = steg[i:i+2]
    if hdr in nonLenMarkers:
        i = i + 2
        continue
    if hdr == b'\xff\xd9':
        i += 2
        break
    ln = unpack(">H", steg[i+2:i+4])[0]
    i = i + ln + 2
    if hdr == b'\xff\xda':
        i += steg[i:].index(b'\xff\xd9')
    if i != len(steg):
        # Trailing data saved
        with open(output_file, "wb") as outFile:
            outFile.write(steg[i:])
```

## PowerShell AES 加密 (.enc 文件)

```powershell
$cipher.key = [System.Text.Encoding]::UTF8.GetBytes("7h3_k3y_70_unl0ck_4ll_7h3_f1l35!")
$cipher.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
$cipher.GenerateIV()
$FileStreamWriter.Write([System.BitConverter]::GetBytes($cipher.IV.Length), 0, 4)
$FileStreamWriter.Write($cipher.IV, 0, $cipher.IV.Length)
$Transform = $cipher.CreateEncryptor()
$CryptoStream = New-Object System.Security.Cryptography.CryptoStream($FileStreamWriter, $Transform, [System.Security.Cryptography.CryptoStreamMode]::Write)
$FileStreamReader.CopyTo($CryptoStream)
```

**Key**: `7h3_k3y_70_unl0ck_4ll_7h3_f1l35!`

## Windows 镜像分析

```bash
mv nahamcon.ova nahamcon.tar
tar -xvf nahamcon.tar
qemu-img convert -f vmdk -O vhdx "Nahamcon Forensics Challenge-disk001.vmdk" out.vhdx
.\hayabusa-2.5.1-win-x64.exe csv-timeline -d "E:\Windows\System32\winevt\Logs" -o result.csv
```

`$flag = "flag{892a8921517dcecf90685d478aedf5e2}"`

## 评价

NahamCon 2023 多类型 writeup：
- **JPEG 隐写** 找 FFD9 trailing data
- **PowerShell AES-256** 加密解密（key 硬编码）
- **qemu-img** vmdk → vhdx 镜像转换
- **hayabusa** Windows 事件日志快速分析

适用读者：Forensics / 隐写 / 加密勒索软件分析
