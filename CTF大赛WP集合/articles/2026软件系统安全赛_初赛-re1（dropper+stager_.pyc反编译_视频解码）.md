# 2026软件系统安全赛 初赛-re1（dropper+stager .pyc反编译 视频解码）

> 原文: https://www.ctfiot.com/302112.html
> ID: 302112

好难的比赛，用ai梭出来两道题，3道逆向只解出一道re1，re2另一位逆向手动调半天找到了半个flag。re3本人也没做过.so文件逆向，找不到加密逻辑

不知道能不能晋级，感觉有点儿悬

附件下载下来拿到两个文件

先看了一下video.mp4发现就是一堆无意义的黑白色块

猜测是Loader会加载video.mp4，然后就会由flag校验相关逻辑，后来发现并不是

查壳

把Loader放进exeinfo看看

64位的.elf文件

逆向分析

用ida打开Loader，打开strings window看到可疑字符串video.mp4，直接定位到下面的函数

int __fastcall main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
int v6; // ebx
  __int64 v7; // rax
constchar *v8; // rax
char v10; // [rsp+7h] [rbp-99h] BYREF
char *v11; // [rsp+8h] [rbp-98h]
char *v12; // [rsp+10h] [rbp-90h]
char *v13; // [rsp+18h] [rbp-88h]
  _BYTE v14[32]; // [rsp+20h] [rbp-80h] BYREF
  _BYTE v15[32]; // [rsp+40h] [rbp-60h] BYREF
  _BYTE v16[40]; // [rsp+60h] [rbp-40h] BYREF
unsigned __int64 v17; // [rsp+88h] [rbp-18h]

  v17 = __readfsqword(0x28u);
  v11 = &v10;
std::string::basic_string(v14, "video.mp4", &v10);
std::__new_allocator<char>::~__new_allocator(&v10);
if ( (unsigned __int8)file_exists(v14) != 1 )
  {
    v3 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4BC0);
    v4 = std::operator<<<char>(v3, v14);
    std::ostream::operator<<(v4, &std::endl<char,std::char_traits<char>>);
    v5 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4BE0);
    std::ostream::operator<<(v5, &std::endl<char,std::char_traits<char>>);
    v6 = 1;
  }
else
  {
    v12 = &v10;
    std::string::basic_string(v16, stager_pyc_base64[0], &v10);
    base64_decode(v15, v16);
    std::string::~string(v16);
    std::__new_allocator<char>::~__new_allocator(&v10);
    v13 = &v10;
    std::string::basic_string(v16, "stager.pyc", &v10);
    std::__new_allocator<char>::~__new_allocator(&v10);
    if ( (unsigned __int8)write_string_to_file(v16, v15) != 1 )
    {
      v7 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4C12);
      std::ostream::operator<<(v7, &std::endl<char,std::char_traits<char>>);
      v6 = 1;
    }
    else
    {
      v8 = (constchar *)std::string::c_str(v16);
      chmod(v8, 0x1EDu);
      run_python_script(v16);
      v6 = 0;
    }
    std::string::~string(v16);
    std::string::~string(v15);
  }
std::string::~string(v14);
return v6;
}

看样子程序运行后会释放一个stager.pyc文件，该程序本身仅检查video.mp4是否存在，并不加载视频，也没有flag校验逻辑，看来关键在于释放出来的.pyc文件

这里尝试将Loader和video.mp4直接放进Linux环境中直接运行Loader，结果生成的.pyc文件只有4个字节，不知道是不是程序有问题还是出题者设下的坑，这里的.pyc文件看来只能我们自己手动提取

提取文件

在strings window里我们能看到base64字符表和一大串base64编码

.rodata:0000000000004058 aQg0ncgaaaabk5l db 'Qg0NCgAAAABK5llpWgkAAOMAAAAAAAAAAAAAAAAFAAAAQAAAAHN6AAAAZABkAWwAb'
.rodata:0000000000004058                                         ; DATA XREF: .data:payload_encoder_pyc_base64↓o
.rodata:0000000000004099                 db 'QFaAQEAZABkAmwCWgJkAGQCbANaA2QAZAJsBFoEZABkAmwFWgZkAGQCbAdaB2QAZA'
.rodata:00000000000040DA                 db 'NsCG0IWggBAGQOZAlkCoQBWgllCmQLawJydmQMWgtlA2oMoA1lC6EBcmxlCWULgwE'
.rodata:000000000000411B                 db 'BAG4KZQSgDmQNoQEBAGQCUwApD+kAAAAAKQHaBUltYWdlTikB2gR0cWRt6YACAADp'
.rodata:000000000000415C                 db '4AEAAOkIAAAA6QoAAAD6CXZpZGVvLm1wNGMGAAAAAAAAACAAAAALAAAAAwAAAHNwA'
.rodata:000000000000419D                 db 'gAAdABqAaACfAChAXMQZABTAHQAagGgA3wAoQF9BmQBfQd0BHwAZAKDAo9QiQB4SH'
.rodata:00000000000041DE                 db 'QFdAaHAGYBZANkBIQIZAWDAnQHoAh8BmQGGwChAWQHZAhkCY0ERABdHH0IfAdkAaA'
.rodata:000000000000421F                 db 'JZApkC4QAfAhEAIMBoQE3AH0HcVZXAFcAZABRAFIAWABkDH0JZAF9CnhmdApkDXQL'
.rodata:0000000000004260                 db 'fAeDAWQOgwNEAF1SfQt8B3wLfAtkDhcAhQIZAH0IdAt8CIMBZA5rAnLkdAx8CGQPg'
.rodata:00000000000042A1                 db 'wJ9DHQMfAlkD4MCfQ18DHwNQQB9DnwKfA5kEJsENwB9CnGafAp8CDcAfQpxmlcAfA'
.rodata:00000000000042E2                 db 'p9B3wBfAMaAHwCfAMaABQAfQ90B6AIdAt8B4MBfA8bAKEBfRBnAH0RkAF4EHQFdAp'
.rodata:0000000000004323                 db '8EIMBZBFkEo0CRABd/H0LfAt8DxQAfRJ8B3wSfBJ8DxcAhQIZAH0TdAt8E4MBfA9r'
.rodata:0000000000004364                 db 'AJABcmx8E2QTfA90C3wTgwEYABQAFwB9E3QNag5kFHwBfAJmAmQVZBaNA30UeJZ0C'
.rodata:00000000000043A5                 db 'nwCfAMaAIMBRABdhn0VfBV8AXwDGgAUAH0WfBVkFxcAfAF8AxoAFAB9F3wTfBZ8F4'
.rodata:00000000000043E6                 db 'UCGQB9GHhWdA98GIMBRABdSlwCfRl9GnwaZBhrApABctpkGW4CZBp9G3wZfAMUAHw'
.rodata:0000000000004427                 db 'VfAMUAAIAfRx9HXwUoBB8G3wcfB18HHwDFwB8HXwDFwBmBKECAQCQAXHEVwCQAXGO'
.rodata:0000000000004468                 db 'VwB8EaARdBKgE3wUoQGhAQEAkAFxLlcAdBRqFXwFfARkG2QcjQOPKH0eeCB0BXwRZ'
.rodata:00000000000044A9                 db 'B1kEo0CRABdEH0ffB6gFnwfoQEBAJACcU5XAFcAZABRAFIAWABkAFMAKR5O2gDaAn'
.rodata:00000000000044EA                 db 'JiYwAAAAAAAAAAAAAAAAMAAAATAAAAcwoAAACIAKAAZAGhAVMAKQJOaQAEAAApAdo'
.rodata:000000000000452B                 db 'EcmVhZKkAKQHaAWZyDAAAAPodUGF5bG9hZF9Ub19QaXhlbENvZGVfdmlkZW8ucHna'
.rodata:000000000000456C                 db 'CDxsYW1iZGE+EAAAAPMAAAAAeh9maWxlX3RvX3ZpZGVvLjxsb2NhbHM+LjxsYW1iZ'
.rodata:00000000000045AD                 db 'GE+chAAAABpAAQAAFoCS0J1DAAAAOivu+WPluaWh+S7tikE2ghpdGVyYWJsZVoFdG'
.rodata:00000000000045EE                 db '90YWxaBHVuaXTaBGRlc2NjAQAAAAAAAAACAAAAAwAAAHMAAABzFgAAAHwAXQ59AXw'
.rodata:000000000000462F                 db 'BZACbBFYAAQBxAmQBUwApAtoDMDhiTnIMAAAAKQLaAi4wWgRieXRlcgwAAAByDAAA'
.rodata:0000000000004670                 db 'AHIOAAAA+gk8Z2VuZXhwcj4TAAAAcwIAAAAEAHogZmlsZV90b192aWRlby48bG9jY'
.rodata:00000000000046B1                 db 'WxzPi48Z2VuZXhwcj5aCDEwMTAxMDEwcgEAAAByBgAAAOkCAAAAchMAAAB1DwAAAO'
.rodata:00000000000046F2                 db 'eUn+aIkOinhumikeW4pykBchIAAADaATBaA1JHQloFd2hpdGUpAdoFY29sb3LpAQA'
.rodata:0000000000004733                 db 'AANoBMSkDcgEAAAByAQAAAHIBAAAAKQPp/wAAAHIbAAAAchsAAABaB2xpYngyNjQp'
.rodata:0000000000004774                 db 'AtoDZnBz2gVjb2RlY3UPAAAA5YaZ5YWl6KeG6aKR5binKRfaAm9z2gRwYXRo2gZpc'
.rodata:00000000000047B5                 db '2ZpbGXaB2dldHNpemXaBG9wZW5yAwAAANoEaXRlctoEbWF0aFoEY2VpbNoEam9pbt'
.rodata:00000000000047F6                 db 'oFcmFuZ2XaA2xlbtoDaW50cgIAAADaA25ld9oJZW51bWVyYXRlWgVwYXN0ZdoGYXB'
.rodata:0000000000004837                 db 'wZW5k2gJucFoFYXJyYXnaB2ltYWdlaW9aCmdldF93cml0ZXJaC2FwcGVuZF9kYXRh'
.rodata:0000000000004878                 db 'KSBaCmlucHV0X2ZpbGXaBXdpZHRoWgZoZWlnaHRaCnBpeGVsX3NpemVyHAAAANoLb'
.rodata:00000000000048B9                 db '3V0cHV0X2ZpbGVaCWZpbGVfc2l6ZVoNYmluYXJ5X3N0cmluZ9oFY2h1bmtaB3hvcl'
.rodata:00000000000048FA                 db '9rZXlaEXhvcl9iaW5hcnlfc3RyaW5n2gFpWgljaHVua19pbnRaB2tleV9pbnRaCnh'
.rodata:000000000000493B                 db 'vcl9yZXN1bHRaEHBpeGVsc19wZXJfaW1hZ2VaCm51bV9pbWFnZXNaBmZyYW1lc9oF'
.rodata:000000000000497C                 db 'c3RhcnTaBGJpdHNaA2ltZ9oBcloJcm93X3N0YXJ0Wgdyb3dfZW5k2gNyb3faAWPaA'
.rodata:00000000000049BD                 db '2JpdHIYAAAAWgJ4MVoCeTHaBndyaXRlctoFZnJhbWVyDAAAACkBcg0AAAByDgAAAN'
.rodata:00000000000049FE                 db 'oNZmlsZV90b192aWRlbwgAAABzUgAAAAABDAEEAgwCBAEMARQBDgEMASYCBAEEARY'
.rodata:0000000000004A3F                 db 'BEAEMAQoBCgEIAQ4CDAIEAhABEgIEAhgBCAEQAQ4BFAIUAhIBDAEQAQwCEgESARIB'
.rodata:0000000000004A80                 db 'KAIWAhIBEgFyOgAAANoIX19tYWluX19aB3BheWxvYWRyGQAAACkFcgQAAAByBQAAA'
.rodata:0000000000004AC1                 db 'HIGAAAAcgcAAAByCAAAACkPWgNQSUxyAgAAAHIkAAAAch4AAADaA3N5c1oFbnVtcH'
.rodata:0000000000004B02                 db 'lyLAAAAHItAAAAcgMAAAByOgAAANoIX19uYW1lX19aCmlucHV0X3BhdGhyHwAAANo'
.rodata:0000000000004B43                 db 'GZXhpc3Rz2gRleGl0cgwAAAByDAAAAHIMAAAAcg4AAADaCDxtb2R1bGU+AQAAAHMW'
.rodata:0000000000004B84                 db 'AAAADAEQAQgBCAEIAQwCCjgIAQQBDAEKAg==',0

将上面内容导出后写个脚本进行base64解码，写入stager.pyc文件即可

import base64

data = "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"

open("stager.pyc","wb").write(base64.b64decode(data))

.pyc文件反编译及分析

.pyc文件是无法直接读的，需要反编译为.py文件，先尝试使用pycdc

反编译出现了错误，stager.py只生成了一部分

# Source Generated with Decompyle++
# File: stager.pyc (Python 3.7)

from PIL import Image
import math
import os
import sys
import numpy as np
import imageio
from tqdm import tqdm

def file_to_video(input_file, width, height, pixel_size, fps, output_file = (640, 480, 8, 10, 'video.mp4')):
    ifnot os.path.isfile(input_file):
        returnNone
    file_size = None.path.getsize(input_file)
    binary_string = ''
# WARNING: Decompyle incomplete

if __name__ == '__main__':
    input_path = 'payload'
    if os.path.exists(input_path):
        file_to_video(input_path)
    else:
        sys.exit(1)

但是从开头的注释我们可以看出需要在python 3.7环境下用uncompyle反编译

本人懒得配置python 3.7环境了，叫队伍里另一位逆向手用conda创建了一个，帮我用uncompyle反编译了

uncompyle6 stager.pyc > stager.py

反编译成功

# uncompyle6 version 3.9.3
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.16 (default, Jan 17 2023, 16:06:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: Payload_To_PixelCode_video.py
# Compiled at: 2026-01-04 12:02:18
# Size of source mod 2**32: 2394 bytes
from PIL import Image
import math, os, sys, numpy as np, imageio
from tqdm import tqdm

def file_to_video(input_file, width=640, height=480, pixel_size=8, fps=10, output_file='video.mp4'):
    ifnot os.path.isfile(input_file):
        return
    file_size = os.path.getsize(input_file)
    binary_string = ""
    with open(input_file, "rb") as f:
        for chunk in tqdm(iterable=(iter((lambda: f.read(1024)), b'')),
          total=(math.ceil(file_size / 1024)), unit="KB", desc="读取文件"):
            binary_string += "".join(((f"{byte:08b}") for byte in chunk))

    xor_key = "10101010"
    xor_binary_string = ""
    for i in range(0, len(binary_string), 8):
        chunk = binary_string[i[:i + 8]]
        if len(chunk) == 8:
            chunk_int = int(chunk, 2)
            key_int = int(xor_key, 2)
            xor_result = chunk_int ^ key_int
            xor_binary_string += f"{xor_result:08b}"
        else:
            xor_binary_string += chunk

    binary_string = xor_binary_string
    pixels_per_image = width // pixel_size * (height // pixel_size)
    num_images = math.ceil(len(binary_string) / pixels_per_image)
    frames = []
    for i in tqdm((range(num_images)), desc="生成视频帧"):
        start = i * pixels_per_image
        bits = binary_string[start[:start + pixels_per_image]]
        if len(bits) < pixels_per_image:
            bits = bits + "0" * (pixels_per_image - len(bits))
        img = Image.new("RGB", (width, height), color="white")
        for r in range(height // pixel_size):
            row_start = r * (width // pixel_size)
            row_end = (r + 1) * (width // pixel_size)
            row = bits[row_start[:row_end]]
            for c, bit in enumerate(row):
                color = (0, 0, 0) if bit == "1"else (255, 255, 255)
                x1, y1 = c * pixel_size, r * pixel_size
                img.paste(color, (x1, y1, x1 + pixel_size, y1 + pixel_size))

        frames.append(np.array(img))

    with imageio.get_writer(output_file, fps=fps, codec="libx264") as writer:
        for frame in tqdm(frames, desc="写入视频帧"):
            writer.append_data(frame)

if __name__ == "__main__":
    input_path = "payload"
    if os.path.exists(input_path):
        file_to_video(input_path)
    else:
        sys.exit(1)

# okay decompiling stager.pyc

这个脚本的作用是将一个payload文件编码为视频，显然就是video.mp4，因此我们仅需要将视频解码回去就可以了

有编码脚本，就可以请ai写出解码脚本了

import imageio.v2 as imageio
import numpy as np

VIDEO = "video.mp4"
PIXEL_SIZE = 8
WIDTH = 640
HEIGHT = 480

reader = imageio.get_reader(VIDEO, format="ffmpeg")

bits = ""

print("reading frames...")

for frame in reader:
    for r in range(HEIGHT // PIXEL_SIZE):
        for c in range(WIDTH // PIXEL_SIZE):

            x = c * PIXEL_SIZE
            y = r * PIXEL_SIZE

            pixel = frame[y][x]

            if pixel[0] < 128:
                bits += "1"
            else:
                bits += "0"

print("bits:", len(bits))

data = bytearray()

for i in range(0, len(bits), 8):

    chunk = bits[i:i+8]

    if len(chunk) < 8:
        break

    b = int(chunk, 2)

    b ^= 0xAA

    data.append(b)

open("payload", "wb").write(data)

print("done")

解码得到的文件还是一个64位的.elf文件

视频解码文件分析

直接用ida分析只能看到一堆可疑的md5哈希值

直接放到Linux中运行可以得到一些提示

按理说哈希值应该出现在下面，但是却没有，不知道是不是我们提取的文件有问题还是这又是出题人的“小巧思”

看来只能我们自己提取哈希值了

哈希值爆破

如果仅提取strings window里的哈希值最后得到的flag是不完整的

dart{2b1f8-3045e76c}

完整的哈希值藏在另一个位置，往后翻一翻就能找到

.data:0000000000004020 off_4020        dq offset a8277e0910d7501
.data:0000000000004020                                         ; DATA XREF: main+25↑o
.data:0000000000004020                                         ; "8277e0910d750195b448797616e091ad"
.data:0000000000004028                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004030                 dq offset a4b43b0aee35624 ; "4b43b0aee35624cd95b910189b3dc231"
.data:0000000000004038                 dq offset aE358efa489f580 ; "e358efa489f58062f10dd7316b65649e"
.data:0000000000004040                 dq offset aF95b70fdc30885 ; "f95b70fdc3088560732a5ac135644506"
.data:0000000000004048                 dq offset aC81e728d9d4c2f ; "c81e728d9d4c2f636f067f89cc14862c"
.data:0000000000004050                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004058                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004060                 dq offset aC4ca4238a0b923 ; "c4ca4238a0b923820dcc509a6f75849b"
.data:0000000000004068                 dq offset a8fa14cdd754f91 ; "8fa14cdd754f91cc6554c9e71929cce7"
.data:0000000000004070                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004078                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:0000000000004080                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004088                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:0000000000004090                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004098                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:00000000000040A0                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:00000000000040A8                 dq offset aCfcd208495d565 ; "cfcd208495d565ef66e7dff9f98764da"
.data:00000000000040B0                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:00000000000040B8                 dq offset aA87ff679a2f3e7 ; "a87ff679a2f3e71d9181a67b7542122c"
.data:00000000000040C0                 dq offset aE4da3b7fbbce23 ; "e4da3b7fbbce2345d7772b0674a318d5"
.data:00000000000040C8                 dq offset aE1671797c52e15 ; "e1671797c52e15f763380b45e841ec32"
.data:00000000000040D0                 dq offset a8f14e45fceea16 ; "8f14e45fceea167a5a36dedd4bea2543"
.data:00000000000040D8                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:00000000000040E0                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:00000000000040E8                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:00000000000040F0                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:00000000000040F8                 dq offset aCfcd208495d565 ; "cfcd208495d565ef66e7dff9f98764da"
.data:0000000000004100                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:0000000000004108                 dq offset a1679091c5a880f ; "1679091c5a880faf6fb5e6087eb1b2dc"
.data:0000000000004110                 dq offset a1679091c5a880f ; "1679091c5a880faf6fb5e6087eb1b2dc"
.data:0000000000004118                 dq offset a4a8a08f09d37b7 ; "4a8a08f09d37b73795649038408b5f33"
.data:0000000000004120                 dq offset a8f14e45fceea16 ; "8f14e45fceea167a5a36dedd4bea2543"
.data:0000000000004128                 dq offset aE1671797c52e15 ; "e1671797c52e15f763380b45e841ec32"
.data:0000000000004130                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:0000000000004138                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004140                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:0000000000004148                 dq offset aE1671797c52e15 ; "e1671797c52e15f763380b45e841ec32"
.data:0000000000004150                 dq offset aCfcd208495d565 ; "cfcd208495d565ef66e7dff9f98764da"
.data:0000000000004158                 dq offset aE4da3b7fbbce23 ; "e4da3b7fbbce2345d7772b0674a318d5"
.data:0000000000004160                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004168                 dq offset aCbb184dd8e05c9 ; "cbb184dd8e05c9709e5dcaedaa0495cf"
.data:0000000000004168 _data           ends

将上面内容复制进一个文本文件，写个脚本用正则表达式提取双引号内的md5值，再在一个flag常用字符的字符表中逐个计算哈希并匹配这些md5值即可得到flag

import re
import hashlib

# 1️⃣ 读取 ELF rodata 导出的文本文件
with open(r"export.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2️⃣ 用正则提取单引号内的 MD5 字符串
md5_list = re.findall(r""([0-9a-f]{32})"", text)
print(f"共找到 {len(md5_list)} 个 MD5")

# 3️⃣ 定义可能的字符表
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-"

# 4️⃣ 拼接 flag
flag = ""

for h in md5_list:
    found = False
    for c in chars:
        if hashlib.md5(c.encode()).hexdigest() == h:
            flag += c
            found = True
            break
    ifnot found:
        flag += "?"# 如果没匹配上，用 ? 占位
        print(f"未匹配到 hash: {h}")

print("flag:", flag)

'''
输出内容：
共找到 42 个 MD5
flag: dart{2ab1fb8a-b830-45e7-8830-66c7e3b3e05a}
'''

蹲一蹲其他师傅的wp让我拜读一下


```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
int v6; // ebx
  __int64 v7; // rax
constchar *v8; // rax
char v10; // [rsp+7h] [rbp-99h] BYREF
char *v11; // [rsp+8h] [rbp-98h]
char *v12; // [rsp+10h] [rbp-90h]
char *v13; // [rsp+18h] [rbp-88h]
  _BYTE v14[32]; // [rsp+20h] [rbp-80h] BYREF
  _BYTE v15[32]; // [rsp+40h] [rbp-60h] BYREF
  _BYTE v16[40]; // [rsp+60h] [rbp-40h] BYREF
unsigned __int64 v17; // [rsp+88h] [rbp-18h]

  v17 = __readfsqword(0x28u);
  v11 = &v10;
std::string::basic_string(v14, "video.mp4", &v10);
std::__new_allocator<char>::~__new_allocator(&v10);
if ( (unsigned __int8)file_exists(v14) != 1 )
  {
    v3 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4BC0);
    v4 = std::operator<<<char>(v3, v14);
    std::ostream::operator<<(v4, &std::endl<char,std::char_traits<char>>);
    v5 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4BE0);
    std::ostream::operator<<(v5, &std::endl<char,std::char_traits<char>>);
    v6 = 1;
  }
else
  {
    v12 = &v10;
    std::string::basic_string(v16, stager_pyc_base64[0], &v10);
    base64_decode(v15, v16);
    std::string::~string(v16);
    std::__new_allocator<char>::~__new_allocator(&v10);
    v13 = &v10;
    std::string::basic_string(v16, "stager.pyc", &v10);
    std::__new_allocator<char>::~__new_allocator(&v10);
    if ( (unsigned __int8)write_string_to_file(v16, v15) != 1 )
    {
      v7 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4C12);
      std::ostream::operator<<(v7, &std::endl<char,std::char_traits<char>>);
      v6 = 1;
    }
    else
    {
      v8 = (constchar *)std::string::c_str(v16);
      chmod(v8, 0x1EDu);
      run_python_script(v16);
      v6 = 0;
    }
    std::string::~string(v16);
    std::string::~string(v15);
  }
std::string::~string(v14);
return v6;
}
```



```
.rodata:0000000000004058 aQg0ncgaaaabk5l db 'Qg0NCgAAAABK5llpWgkAAOMAAAAAAAAAAAAAAAAFAAAAQAAAAHN6AAAAZABkAWwAb'
.rodata:0000000000004058                                         ; DATA XREF: .data:payload_encoder_pyc_base64↓o
.rodata:0000000000004099                 db 'QFaAQEAZABkAmwCWgJkAGQCbANaA2QAZAJsBFoEZABkAmwFWgZkAGQCbAdaB2QAZA'
.rodata:00000000000040DA                 db 'NsCG0IWggBAGQOZAlkCoQBWgllCmQLawJydmQMWgtlA2oMoA1lC6EBcmxlCWULgwE'
.rodata:000000000000411B                 db 'BAG4KZQSgDmQNoQEBAGQCUwApD+kAAAAAKQHaBUltYWdlTikB2gR0cWRt6YACAADp'
.rodata:000000000000415C                 db '4AEAAOkIAAAA6QoAAAD6CXZpZGVvLm1wNGMGAAAAAAAAACAAAAALAAAAAwAAAHNwA'
.rodata:000000000000419D                 db 'gAAdABqAaACfAChAXMQZABTAHQAagGgA3wAoQF9BmQBfQd0BHwAZAKDAo9QiQB4SH'
.rodata:00000000000041DE                 db 'QFdAaHAGYBZANkBIQIZAWDAnQHoAh8BmQGGwChAWQHZAhkCY0ERABdHH0IfAdkAaA'
.rodata:000000000000421F                 db 'JZApkC4QAfAhEAIMBoQE3AH0HcVZXAFcAZABRAFIAWABkDH0JZAF9CnhmdApkDXQL'
.rodata:0000000000004260                 db 'fAeDAWQOgwNEAF1SfQt8B3wLfAtkDhcAhQIZAH0IdAt8CIMBZA5rAnLkdAx8CGQPg'
.rodata:00000000000042A1                 db 'wJ9DHQMfAlkD4MCfQ18DHwNQQB9DnwKfA5kEJsENwB9CnGafAp8CDcAfQpxmlcAfA'
.rodata:00000000000042E2                 db 'p9B3wBfAMaAHwCfAMaABQAfQ90B6AIdAt8B4MBfA8bAKEBfRBnAH0RkAF4EHQFdAp'
.rodata:0000000000004323                 db '8EIMBZBFkEo0CRABd/H0LfAt8DxQAfRJ8B3wSfBJ8DxcAhQIZAH0TdAt8E4MBfA9r'
.rodata:0000000000004364                 db 'AJABcmx8E2QTfA90C3wTgwEYABQAFwB9E3QNag5kFHwBfAJmAmQVZBaNA30UeJZ0C'
.rodata:00000000000043A5                 db 'nwCfAMaAIMBRABdhn0VfBV8AXwDGgAUAH0WfBVkFxcAfAF8AxoAFAB9F3wTfBZ8F4'
.rodata:00000000000043E6                 db 'UCGQB9GHhWdA98GIMBRABdSlwCfRl9GnwaZBhrApABctpkGW4CZBp9G3wZfAMUAHw'
.rodata:0000000000004427                 db 'VfAMUAAIAfRx9HXwUoBB8G3wcfB18HHwDFwB8HXwDFwBmBKECAQCQAXHEVwCQAXGO'
.rodata:0000000000004468                 db 'VwB8EaARdBKgE3wUoQGhAQEAkAFxLlcAdBRqFXwFfARkG2QcjQOPKH0eeCB0BXwRZ'
.rodata:00000000000044A9                 db 'B1kEo0CRABdEH0ffB6gFnwfoQEBAJACcU5XAFcAZABRAFIAWABkAFMAKR5O2gDaAn'
.rodata:00000000000044EA                 db 'JiYwAAAAAAAAAAAAAAAAMAAAATAAAAcwoAAACIAKAAZAGhAVMAKQJOaQAEAAApAdo'
.rodata:000000000000452B                 db 'EcmVhZKkAKQHaAWZyDAAAAPodUGF5bG9hZF9Ub19QaXhlbENvZGVfdmlkZW8ucHna'
.rodata:000000000000456C                 db 'CDxsYW1iZGE+EAAAAPMAAAAAeh9maWxlX3RvX3ZpZGVvLjxsb2NhbHM+LjxsYW1iZ'
.rodata:00000000000045AD                 db 'GE+chAAAABpAAQAAFoCS0J1DAAAAOivu+WPluaWh+S7tikE2ghpdGVyYWJsZVoFdG'
.rodata:00000000000045EE                 db '90YWxaBHVuaXTaBGRlc2NjAQAAAAAAAAACAAAAAwAAAHMAAABzFgAAAHwAXQ59AXw'
.rodata:000000000000462F                 db 'BZACbBFYAAQBxAmQBUwApAtoDMDhiTnIMAAAAKQLaAi4wWgRieXRlcgwAAAByDAAA'
.rodata:0000000000004670                 db 'AHIOAAAA+gk8Z2VuZXhwcj4TAAAAcwIAAAAEAHogZmlsZV90b192aWRlby48bG9jY'
.rodata:00000000000046B1                 db 'WxzPi48Z2VuZXhwcj5aCDEwMTAxMDEwcgEAAAByBgAAAOkCAAAAchMAAAB1DwAAAO'
.rodata:00000000000046F2                 db 'eUn+aIkOinhumikeW4pykBchIAAADaATBaA1JHQloFd2hpdGUpAdoFY29sb3LpAQA'
.rodata:0000000000004733                 db 'AANoBMSkDcgEAAAByAQAAAHIBAAAAKQPp/wAAAHIbAAAAchsAAABaB2xpYngyNjQp'
.rodata:0000000000004774                 db 'AtoDZnBz2gVjb2RlY3UPAAAA5YaZ5YWl6KeG6aKR5binKRfaAm9z2gRwYXRo2gZpc'
.rodata:00000000000047B5                 db '2ZpbGXaB2dldHNpemXaBG9wZW5yAwAAANoEaXRlctoEbWF0aFoEY2VpbNoEam9pbt'
.rodata:00000000000047F6                 db 'oFcmFuZ2XaA2xlbtoDaW50cgIAAADaA25ld9oJZW51bWVyYXRlWgVwYXN0ZdoGYXB'
.rodata:0000000000004837                 db 'wZW5k2gJucFoFYXJyYXnaB2ltYWdlaW9aCmdldF93cml0ZXJaC2FwcGVuZF9kYXRh'
.rodata:0000000000004878                 db 'KSBaCmlucHV0X2ZpbGXaBXdpZHRoWgZoZWlnaHRaCnBpeGVsX3NpemVyHAAAANoLb'
.rodata:00000000000048B9                 db '3V0cHV0X2ZpbGVaCWZpbGVfc2l6ZVoNYmluYXJ5X3N0cmluZ9oFY2h1bmtaB3hvcl'
.rodata:00000000000048FA                 db '9rZXlaEXhvcl9iaW5hcnlfc3RyaW5n2gFpWgljaHVua19pbnRaB2tleV9pbnRaCnh'
.rodata:000000000000493B                 db 'vcl9yZXN1bHRaEHBpeGVsc19wZXJfaW1hZ2VaCm51bV9pbWFnZXNaBmZyYW1lc9oF'
.rodata:000000000000497C                 db 'c3RhcnTaBGJpdHNaA2ltZ9oBcloJcm93X3N0YXJ0Wgdyb3dfZW5k2gNyb3faAWPaA'
.rodata:00000000000049BD                 db '2JpdHIYAAAAWgJ4MVoCeTHaBndyaXRlctoFZnJhbWVyDAAAACkBcg0AAAByDgAAAN'
.rodata:00000000000049FE                 db 'oNZmlsZV90b192aWRlbwgAAABzUgAAAAABDAEEAgwCBAEMARQBDgEMASYCBAEEARY'
.rodata:0000000000004A3F                 db 'BEAEMAQoBCgEIAQ4CDAIEAhABEgIEAhgBCAEQAQ4BFAIUAhIBDAEQAQwCEgESARIB'
.rodata:0000000000004A80                 db 'KAIWAhIBEgFyOgAAANoIX19tYWluX19aB3BheWxvYWRyGQAAACkFcgQAAAByBQAAA'
.rodata:0000000000004AC1                 db 'HIGAAAAcgcAAAByCAAAACkPWgNQSUxyAgAAAHIkAAAAch4AAADaA3N5c1oFbnVtcH'
.rodata:0000000000004B02                 db 'lyLAAAAHItAAAAcgMAAAByOgAAANoIX19uYW1lX19aCmlucHV0X3BhdGhyHwAAANo'
.rodata:0000000000004B43                 db 'GZXhpc3Rz2gRleGl0cgwAAAByDAAAAHIMAAAAcg4AAADaCDxtb2R1bGU+AQAAAHMW'
.rodata:0000000000004B84                 db 'AAAADAEQAQgBCAEIAQwCCjgIAQQBDAEKAg==',0
```



```
import base64

data = "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"

open("stager.pyc","wb").write(base64.b64decode(data))
```



```
# Source Generated with Decompyle++
# File: stager.pyc (Python 3.7)

from PIL import Image
import math
import os
import sys
import numpy as np
import imageio
from tqdm import tqdm

def file_to_video(input_file, width, height, pixel_size, fps, output_file = (640, 480, 8, 10, 'video.mp4')):
    ifnot os.path.isfile(input_file):
        returnNone
    file_size = None.path.getsize(input_file)
    binary_string = ''
# WARNING: Decompyle incomplete

if __name__ == '__main__':
    input_path = 'payload'
    if os.path.exists(input_path):
        file_to_video(input_path)
    else:
        sys.exit(1)
```



```
uncompyle6 stager.pyc > stager.py
```



```
# uncompyle6 version 3.9.3
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.16 (default, Jan 17 2023, 16:06:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: Payload_To_PixelCode_video.py
# Compiled at: 2026-01-04 12:02:18
# Size of source mod 2**32: 2394 bytes
from PIL import Image
import math, os, sys, numpy as np, imageio
from tqdm import tqdm

def file_to_video(input_file, width=640, height=480, pixel_size=8, fps=10, output_file='video.mp4'):
    ifnot os.path.isfile(input_file):
        return
    file_size = os.path.getsize(input_file)
    binary_string = ""
    with open(input_file, "rb") as f:
        for chunk in tqdm(iterable=(iter((lambda: f.read(1024)), b'')),
          total=(math.ceil(file_size / 1024)), unit="KB", desc="读取文件"):
            binary_string += "".join(((f"{byte:08b}") for byte in chunk))

    xor_key = "10101010"
    xor_binary_string = ""
    for i in range(0, len(binary_string), 8):
        chunk = binary_string[i[:i + 8]]
        if len(chunk) == 8:
            chunk_int = int(chunk, 2)
            key_int = int(xor_key, 2)
            xor_result = chunk_int ^ key_int
            xor_binary_string += f"{xor_result:08b}"
        else:
            xor_binary_string += chunk

    binary_string = xor_binary_string
    pixels_per_image = width // pixel_size * (height // pixel_size)
    num_images = math.ceil(len(binary_string) / pixels_per_image)
    frames = []
    for i in tqdm((range(num_images)), desc="生成视频帧"):
        start = i * pixels_per_image
        bits = binary_string[start[:start + pixels_per_image]]
        if len(bits) < pixels_per_image:
            bits = bits + "0" * (pixels_per_image - len(bits))
        img = Image.new("RGB", (width, height), color="white")
        for r in range(height // pixel_size):
            row_start = r * (width // pixel_size)
            row_end = (r + 1) * (width // pixel_size)
            row = bits[row_start[:row_end]]
            for c, bit in enumerate(row):
                color = (0, 0, 0) if bit == "1"else (255, 255, 255)
                x1, y1 = c * pixel_size, r * pixel_size
                img.paste(color, (x1, y1, x1 + pixel_size, y1 + pixel_size))

        frames.append(np.array(img))

    with imageio.get_writer(output_file, fps=fps, codec="libx264") as writer:
        for frame in tqdm(frames, desc="写入视频帧"):
            writer.append_data(frame)

if __name__ == "__main__":
    input_path = "payload"
    if os.path.exists(input_path):
        file_to_video(input_path)
    else:
        sys.exit(1)

# okay decompiling stager.pyc
```



```
import imageio.v2 as imageio
import numpy as np

VIDEO = "video.mp4"
PIXEL_SIZE = 8
WIDTH = 640
HEIGHT = 480

reader = imageio.get_reader(VIDEO, format="ffmpeg")

bits = ""

print("reading frames...")

for frame in reader:
    for r in range(HEIGHT // PIXEL_SIZE):
        for c in range(WIDTH // PIXEL_SIZE):

            x = c * PIXEL_SIZE
            y = r * PIXEL_SIZE

            pixel = frame[y][x]

            if pixel[0] < 128:
                bits += "1"
            else:
                bits += "0"

print("bits:", len(bits))

data = bytearray()

for i in range(0, len(bits), 8):

    chunk = bits[i:i+8]

    if len(chunk) < 8:
        break

    b = int(chunk, 2)

    b ^= 0xAA

    data.append(b)

open("payload", "wb").write(data)

print("done")
```



```
dart{2b1f8-3045e76c}
```



```
.data:0000000000004020 off_4020        dq offset a8277e0910d7501
.data:0000000000004020                                         ; DATA XREF: main+25↑o
.data:0000000000004020                                         ; "8277e0910d750195b448797616e091ad"
.data:0000000000004028                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004030                 dq offset a4b43b0aee35624 ; "4b43b0aee35624cd95b910189b3dc231"
.data:0000000000004038                 dq offset aE358efa489f580 ; "e358efa489f58062f10dd7316b65649e"
.data:0000000000004040                 dq offset aF95b70fdc30885 ; "f95b70fdc3088560732a5ac135644506"
.data:0000000000004048                 dq offset aC81e728d9d4c2f ; "c81e728d9d4c2f636f067f89cc14862c"
.data:0000000000004050                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004058                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004060                 dq offset aC4ca4238a0b923 ; "c4ca4238a0b923820dcc509a6f75849b"
.data:0000000000004068                 dq offset a8fa14cdd754f91 ; "8fa14cdd754f91cc6554c9e71929cce7"
.data:0000000000004070                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004078                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:0000000000004080                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004088                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:0000000000004090                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004098                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:00000000000040A0                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:00000000000040A8                 dq offset aCfcd208495d565 ; "cfcd208495d565ef66e7dff9f98764da"
.data:00000000000040B0                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:00000000000040B8                 dq offset aA87ff679a2f3e7 ; "a87ff679a2f3e71d9181a67b7542122c"
.data:00000000000040C0                 dq offset aE4da3b7fbbce23 ; "e4da3b7fbbce2345d7772b0674a318d5"
.data:00000000000040C8                 dq offset aE1671797c52e15 ; "e1671797c52e15f763380b45e841ec32"
.data:00000000000040D0                 dq offset a8f14e45fceea16 ; "8f14e45fceea167a5a36dedd4bea2543"
.data:00000000000040D8                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:00000000000040E0                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:00000000000040E8                 dq offset aC9f0f895fb98ab ; "c9f0f895fb98ab9159f51fd0297e236d"
.data:00000000000040F0                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:00000000000040F8                 dq offset aCfcd208495d565 ; "cfcd208495d565ef66e7dff9f98764da"
.data:0000000000004100                 dq offset a336d5ebc543653 ; "336d5ebc5436534e61d16e63ddfca327"
.data:0000000000004108                 dq offset a1679091c5a880f ; "1679091c5a880faf6fb5e6087eb1b2dc"
.data:0000000000004110                 dq offset a1679091c5a880f ; "1679091c5a880faf6fb5e6087eb1b2dc"
.data:0000000000004118                 dq offset a4a8a08f09d37b7 ; "4a8a08f09d37b73795649038408b5f33"
.data:0000000000004120                 dq offset a8f14e45fceea16 ; "8f14e45fceea167a5a36dedd4bea2543"
.data:0000000000004128                 dq offset aE1671797c52e15 ; "e1671797c52e15f763380b45e841ec32"
.data:0000000000004130                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:0000000000004138                 dq offset a92eb5ffee6ae2f ; "92eb5ffee6ae2fec3ad71c777531578f"
.data:0000000000004140                 dq offset aEccbc87e4b5ce2 ; "eccbc87e4b5ce2fe28308fd9f2a7baf3"
.data:0000000000004148                 dq offset aE1671797c52e15 ; "e1671797c52e15f763380b45e841ec32"
.data:0000000000004150                 dq offset aCfcd208495d565 ; "cfcd208495d565ef66e7dff9f98764da"
.data:0000000000004158                 dq offset aE4da3b7fbbce23 ; "e4da3b7fbbce2345d7772b0674a318d5"
.data:0000000000004160                 dq offset a0cc175b9c0f1b6 ; "0cc175b9c0f1b6a831c399e269772661"
.data:0000000000004168                 dq offset aCbb184dd8e05c9 ; "cbb184dd8e05c9709e5dcaedaa0495cf"
.data:0000000000004168 _data           ends
```



```
import re
import hashlib

# 1️⃣ 读取 ELF rodata 导出的文本文件
with open(r"export.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2️⃣ 用正则提取单引号内的 MD5 字符串
md5_list = re.findall(r""([0-9a-f]{32})"", text)
print(f"共找到 {len(md5_list)} 个 MD5")

# 3️⃣ 定义可能的字符表
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-"

# 4️⃣ 拼接 flag
flag = ""

for h in md5_list:
    found = False
    for c in chars:
        if hashlib.md5(c.encode()).hexdigest() == h:
            flag += c
            found = True
            break
    ifnot found:
        flag += "?"# 如果没匹配上，用 ? 占位
        print(f"未匹配到 hash: {h}")

print("flag:", flag)

'''
输出内容：
共找到 42 个 MD5
flag: dart{2ab1fb8a-b830-45e7-8830-66c7e3b3e05a}
'''
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705551-wxsync-2026-03-04842ff6fdc0f00b91d0c21796f02989.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705552-wxsync-2026-03-2e01fb0952a0ac9fbf13482c9b2d8fe9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705559-wxsync-2026-03-b9f9ef239265c374ded6de3f6ea1b13a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705561-wxsync-2026-03-b0ab24744dcf8efbab0970b046d18b14.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705562-wxsync-2026-03-80166b4cfde4321b779f3f108fa51f1d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705564-wxsync-2026-03-b6a47f8b35962b70e8f32d3c5e3e271e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705565-wxsync-2026-03-72940e49d556c5612b8a825cf01de427.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773705567-wxsync-2026-03-b15ebeb2463ae17d9718041ad01bc399.png)