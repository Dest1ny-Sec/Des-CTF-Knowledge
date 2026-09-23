---
title: TUCTF 2024 Writeup
contest: TUCTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags:
- rot13
- custom-image-format
- crc8-checksum
- wifi-aircrack
- embrava-bello
attack_chain:
- S = "reingvbaonetr" 字符 chr(ord(s) - 0x61 + 0x54) = rot13
- 'TU Image Program: 自定义 TIMG 格式 (4 byte header + width/height + RUBY tag)'
- 三通道 DATR/DATG/DATB + 每行 crc8 校验和
- img.getpixel([j,i])[0] R 通道
- timg_to_jpg 解码脚本：struct.unpack('>I', data[8:12]) width
- airodump-ng + aircrack-ng 爆破 WiFi (D8:3A:DD:07:AA:5A)
- aircrack-ng -w /usr/share/wordlists/rockyou.txt
key_payload: rot13("reingvbaonetr")
one_liner: TUCTF 2024 4 题：rot13 + TIMG 自定义图像格式 + WiFi aircrack 爆破。
lesson: rot13 加密的字符串仅偏移 0x54 位 (chr(ord(c) - 0x61 + 0x54))；自研图像格式常带 crc8 行校验。
quality: medium
full_path: TUCTF_2024_Writeup.full.md
meta_path: TUCTF_2024_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'TUCTF 2024 Writeup。TUCTF 2024 4 题：rot13 + TIMG 自定义图像格式 + WiFi aircrack 爆破。。关键路径：S = "reingvbaonetr" 字符 chr(ord(s) - 0x61 + 0x54) = rot13 → TU Image Program: 自定义 TIMG 格式 (4 byte header + width/hei...'
category: misc
subcategory: misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/226943.html
reasoning_chain:
- 字符串 'reingvbaonetr' → 假设：chr(ord(s) - 0x61 + 0x54) = rot13 → 动作：解码得 'erotrivagner'
- TU Image Program → 触发点：自定义 TIMG 格式 (4 byte header + width/height + 'RUBY' tag)
- 假设：3 通道 DATR/DATG/DATB + 每行 crc8 校验 → 动作：写 timg_to_jpg 脚本解码
- 动作：struct.unpack('>I', data[8:12]) 读 width → 同样读 height → 还原 RGB 三通道 → 保存 jpg
- airodump-ng 抓 WPA handshake → 假设：D8:3A:DD:07:AA:5A 是目标 AP → 动作：aircrack-ng -w rockyou.txt 跑字典爆破
failed_attempts:
- 试图用 PIL 直接 open('flag.timg') → 失败：PIL 不识别 TIMG 格式
- 试图解析 dataclass 数据 → 失败：实际是字节数组需 struct.unpack
key_observations:
- rot13 本质是 a-z 字母偏移 13，但变种形式可写为 chr(ord(c) - 0x61 + 0x54)
- 自研图像格式常见结构：4 byte magic + width/height + 通道分隔符 + 行校验
- WPA/WPA2-PSK 字典爆破速度慢，rockyou.txt 通常足够
prerequisites:
- Python struct.unpack 字节解析
- PIL / numpy 图像处理基础
- aircrack-ng + airodump-ng WiFi 抓包爆破
---
# TUCTF 2024 Writeup

> 原文: https://www.ctfiot.com/226943.html
> ID: 226943


```
S = "reingvbaonetr"
for s in S:
 tmp = ord(s) - 0x61
 print(chr(tmp + 0x54),end="")
from PIL import Image
import numpy as np
import crc8

def main():
 inp = input("""
 Welcome to the TU Image Program
 It can convert images to TIMGs
 It will also display TIGMs

 [1] Convert Image to TIMG
 [2] Display TIMG

 """)
 match inp:
 case "1":
 conv()
 case "2":
 display() #TODO: Add
 '''
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠿⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⡀⠠⠤⠒⢂⣉⣉⣉⣑⣒⣒⠒⠒⠒⠒⠒⠒⠒⠀⠀⠐⠒⠚⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⡠⠔⠉⣀⠔⠒⠉⣀⣀⠀⠀⠀⣀⡀⠈⠉⠑⠒⠒⠒⠒⠒⠈⠉⠉⠉⠁⠂⠀⠈⠙⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠔⠁⠠⠖⠡⠔⠊⠀⠀⠀⠀⠀⠀⠀⠐⡄⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠉⠲⢄⠀⠀⠀⠈⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠊⠀⢀⣀⣤⣤⣤⣤⣀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠜⠀⠀⠀⠀⣀⡀⠀⠈⠃⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠥⠐⠂⠀⠀⠀⠀⡄⠀⠰⢺⣿⣿⣿⣿⣿⣟⠀⠈⠐⢤⠀⠀⠀⠀⠀⠀⢀⣠⣶⣾⣯⠀⠀⠉⠂⠀⠠⠤⢄⣀⠙⢿⣿⣿
⣿⡿⠋⠡⠐⠈⣉⠭⠤⠤⢄⡀⠈⠀⠈⠁⠉⠁⡠⠀⠀⠀⠉⠐⠠⠔⠀⠀⠀⠀⠀⠲⣿⠿⠛⠛⠓⠒⠂⠀⠀⠀⠀⠀⠀⠠⡉⢢⠙⣿
⣿⠀⢀⠁⠀⠊⠀⠀⠀⠀⠀⠈⠁⠒⠂⠀⠒⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢀⣀⡠⠔⠒⠒⠂⠀⠈⠀⡇⣿
⣿⠀⢸⠀⠀⠀⢀⣀⡠⠋⠓⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠈⠢⠤⡀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⡠⠀⡇⣿
⣿⡀⠘⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠈⠑⡦⢄⣀⠀⠀⠐⠒⠁⢸⠀⠀⠠⠒⠄⠀⠀⠀⠀⠀⢀⠇⠀⣀⡀⠀⠀⢀⢾⡆⠀⠈⡀⠎⣸⣿
⣿⣿⣄⡈⠢⠀⠀⠀⠀⠘⣶⣄⡀⠀⠀⡇⠀⠀⠈⠉⠒⠢⡤⣀⡀⠀⠀⠀⠀⠀⠐⠦⠤⠒⠁⠀⠀⠀⠀⣀⢴⠁⠀⢷⠀⠀⠀⢰⣿⣿
⣿⣿⣿⣿⣇⠂⠀⠀⠀⠀⠈⢂⠀⠈⠹⡧⣀⠀⠀⠀⠀⠀⡇⠀⠀⠉⠉⠉⢱⠒⠒⠒⠒⢖⠒⠒⠂⠙⠏⠀⠘⡀⠀⢸⠀⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠑⠄⠰⠀⠀⠁⠐⠲⣤⣴⣄⡀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⠀⠀⠀⠀⢠⠀⣠⣷⣶⣿⠀⠀⢰⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠁⢀⠀⠀⠀⠀⠀⡙⠋⠙⠓⠲⢤⣤⣷⣤⣤⣤⣤⣾⣦⣤⣤⣶⣿⣿⣿⣿⡟⢹⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠑⠀⢄⠀⡰⠁⠀⠀⠀⠀⠀⠈⠉⠁⠈⠉⠻⠋⠉⠛⢛⠉⠉⢹⠁⢀⢇⠎⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠈⠢⢄⡉⠂⠄⡀⠀⠈⠒⠢⠄⠀⢀⣀⣀⣰⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⢀⣎⠀⠼⠊⠀⠀⠀⠘⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠉⠢⢄⡈⠑⠢⢄⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢀⠀⠀⠀⠀⠀⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⡈⠑⠢⢄⡀⠈⠑⠒⠤⠄⣀⣀⠀⠉⠉⠉⠉⠀⠀⠀⣀⡀⠤⠂⠁⠀⢀⠆⠀⠀⢸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠁⠉⠒⠂⠤⠤⣀⣀⣉⡉⠉⠉⠉⠉⢀⣀⣀⡠⠤⠒⠈⠀⠀⠀⠀⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣤⣤⣤⣤⣀⣀⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿
'''


 case _:
 return 0
 return 0

def conv():
 file = input("Enter the path to you image you want converted to a TIMG file:\n")
 out = input("Enter the path youd like to write the TIMG to:\n")
 img = Image.open(file)
 w,h = img.size
 write = [b'\x54',b'\x49',b'\x4D',b'\x47',b'\x00',b'\x01',b'\x00',b'\x02']
 for x in w.to_bytes(4):
 write.append(x.to_bytes(1))
 for y in h.to_bytes(4):
 write.append(y.to_bytes(1))
 write.append(b'\x52')
 write.append(b'\x55')
 write.append(b'\x42')
 write.append(b'\x59')

 for i in range(h):
 dat = [b'\x44',b'\x41',b'\x54',b'\x52']
 for j in range(w):
 dat.append(img.getpixel([j,i])[0].to_bytes(1))
 dat.append(getCheck(dat[4:]))
 for wa in dat:
 write.append(wa)

 for i in range(h):
 dat = [b'\x44',b'\x41',b'\x54',b'\x47']
 for j in range(w):
 dat.append(img.getpixel([j,i])[1].to_bytes(1))
 dat.append(getCheck(dat[4:]))
 for wa in dat:
 write.append(wa)

 for i in range(h):
 dat = [b'\x44',b'\x41',b'\x54',b'\x42' ]
 for j in range(w):
 print(img.getpixel([j,i])[2].to_bytes(1))
 dat.append(img.getpixel([j,i])[2].to_bytes(1))
 print(dat)
 dat.append(getCheck(dat[4:]))
 for wa in dat:
 write.append(wa)

 write.append(b'\x44')
 write.append(b'\x41')
 write.append(b'\x54')
 write.append(b'\x45')

 with open(out,"ab") as f:
 for b in write:
 f.write(b)

 return 0

def getCheck(datr):
 dat = ''
 for w in datr:
 dat+=chr(int.from_bytes(w))
 print(datr )
 print(dat.encode())
 return int.to_bytes(int(crc8.crc8(dat.encode()).hexdigest(),base=16),1)

if __name__=='__main__':
 main()
from PIL import Image
import numpy as np
import struct
import crc8

def timg_to_jpg(timg_file, output_file):
 try:
 with open(timg_file, "rb") as f:
 data = f.read()

 # Check TIMG header
 if data[:4] != b'TIMG':
 raise ValueError("Invalid TIMG file")

 # Extract width and height
 width = int.from_bytes(data[8:12], "big")
 height = int.from_bytes(data[12:16], "big")

 # Verify header consistency
 if data[16:20] != b'RUBY':
 raise ValueError("Invalid RUBY header")

 # Initialize RGB arrays
 r_channel = np.zeros((height, width), dtype=np.uint8)
 g_channel = np.zeros((height, width), dtype=np.uint8)
 b_channel = np.zeros((height, width), dtype=np.uint8)

 # Parse data sections
 offset = 20 # Start after header
 for color, channel in zip([b'DATR', b'DATG', b'DATB'], [r_channel, g_channel, b_channel]):
 for i in range(height):
 if data[offset:
offset+4] != color:
 raise ValueError(f"Missing {color.decode()} section")
 offset += 4 # Skip section header
 for j in range(width):
 channel[i, j] = data[offset]
 offset += 1

 # Skip checksum (1 byte)
 offset += 1

 # Verify footer
 if data[offset:
offset+4] != b'DATE':
 raise ValueError("Invalid footer")

 # Combine channels into an image
 rgb_array = np.stack((r_channel, g_channel, b_channel), axis=2)
 img = Image.fromarray(rgb_array, "RGB")

 # Save as JPG
 img.save(output_file, "JPEG")
 print(f"Successfully converted TIMG to {output_file}")

 
except Exception as e:
 print(f"Error: {e}")

# Example usage
timg_to_jpg("flag.timg", "output.jpg")
airodump-ng -r dump-05.cap
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b D8:3A:DD:07:AA:5A dump-05.cap
```
