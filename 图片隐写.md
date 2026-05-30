## 常见图片文件头

> 创建: 未知 | 更新: 2026-05-21 | 适用: 不依赖语言 (PNG/JPG/GIF通用) | ⚠️ 部分图片托管于外部CDN

| 文件类型 | 文件头                  | 文件尾      |
| :------- | :---------------------- | :---------- |
| JPEG/JPG | FF D8                   | FF D9       |
| PNG      | 89 50 4E 47 0D 0A 1A 0A | AE 42 60 82 |
| GIF      | 47 49 46 38 39(37) 61   | 00 3B       |

## 元数据（Metadata）

> 元数据（Metadata），又称中介数据、中继数据，为描述数据的数据（Data about data），主要是描述数据属性（property）的信息，用来支持如指示存储位置、历史数据、资源查找、文件记录等功能。

元数据中隐藏信息在比赛中是最基本的一种手法，通常用来隐藏一些关键的 `Hint` 信息或者是一些重要的如 `password` 等信息。

这类元数据你可以 `右键 --> 属性` 去查看,也可以通过 `strings` 命令去查看，一般来说，一些隐藏的信息（奇怪的字符串）常常出现在头部或者尾部。

接下来介绍一个 `identify` 命令，这个命令是用来获取一个或多个图像文件的格式和特性。这个命令的获取是在安装了`Imagemagick`这个包以后获取的。

`-format` 用来指定显示的信息，灵活使用它的 `-format` 参数可以给解题带来不少方便。[format各个参数具体意义](https://www.imagemagick.org/script/escape.php)

### 例题-Mysterious GIF

[Break In 2017 - Mysterious GIF](https://github.com/ctfs/write-ups-2017/tree/master/breakin-ctf-2017/misc/Mysterious-GIF)



![20210909142346](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210909142346.png)

**20210909142346**



> 这里需要用binwalk -e 分离tmp.zip

提取之后发现是一堆.enc文件，因此下一步就是要找enc文件解密需要的key，这里分别对GIF、enc文件、压缩包进行strings，在GiF中找到了一串16进制字符串

这题的一个难点是发现并提取 GIF 中的元数据，首先 `strings` 是可以观察到异常点的。





bash

```bash
GIF89a
   !!!"""###$$$%%%&&&'''((()))***+++,,,---...///000111222333444555666777888999:::;;;<<<===>>>???@@@AAABBBCCCDDDEEEFFFGGGHHHIIIJJJKKKLLLMMMNNNOOOPPPQQQRRRSSSTTTUUUVVVWWWXXXYYYZZZ[[[\\\]]]^^^___```aaabbbcccdddeeefffggghhhiiijjjkkklllmmmnnnooopppqqqrrrssstttuuuvvvwwwxxxyyyzzz{{{|||}}}~~~
4d494945767749424144414e42676b71686b6947397730424151454641415343424b6b776767536c41674541416f4942415144644d4e624c3571565769435172
NETSCAPE2.0
ImageMagick
...
```

这里的一串16进制其实是藏在 GIF 的元数据区

接下来就是提取，你可以选择 Python，但是利用 `identify` 显得更加便捷





bash

```bash
root in ~/Desktop/tmp λ identify -format "%s %c \n" Question.gif
0 4d494945767749424144414e42676b71686b6947397730424151454641415343424b6b776767536c41674541416f4942415144644d4e624c3571565769435172
1 5832773639712f377933536849507565707478664177525162524f72653330633655772f6f4b3877655a547834346d30414c6f75685634364b63514a6b687271
...
24 484b7735432b667741586c4649746d30396145565458772b787a4c4a623253723667415450574d35715661756278667362356d58482f77443969434c684a536f
25 724b3052485a6b745062457335797444737142486435504646773d3d
```





python

```python
# -*- coding: utf-8 -*-
import os
import binascii

os.system('identify -format "%c \n" Question.gif > key')

temp=open('key','rb')
f = open('key1', 'wb+')
for i in temp:
    i = i.decode('utf-8')
    i=int(i,16)
    i=hex(i)
    i = binascii.unhexlify(i[2:])
   # 
    i = i.decode('utf-8') + '\n'
    i = bytes(i, 'utf-8')

    f.write(i)

temp.close()
f.close()
os.system('rm -f key')
os.rename('key1','key')
```

这道题的下一个难点就是在做了十六进制解码以后，意识到这是一个rsakey

意识到这个是个私钥以后就好办了，先解密一个partaa.enc看一下

![20210910103938](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210910103938.png)

**20210910103938**



于是脚本搞定





python

```python
# -*- coding: utf-8 -*-
import string
import os
dic = string.ascii_letters
i=0
i1=0
print(dic[:26])
for n in dic[:11]:
    # file = 'part'
    # file = file+str(n)
    for m in dic[:26]:
        file1=''
        file = 'part'+str(n)
        # print(file)
        file1 = file+str(m)
        file = file+str(m)+'.enc'
        print(file,file1)
        os.system('openssl rsautl -decrypt -inkey key -in %s -out %s' %(file ,file1))
        file1 = file+str(m)
        os.system('rm -f %s %s' %(file,file1))
os.system('cat part* > final')
```

最终获取flag

![20210910104238](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210910104238.png)

**20210910104238**



## 像素值转化

### 例题-神奇的二维码

看看这个文件里的数据，你能想到什么？





none

```none
255,255,255,255,255...........
```

是一串 RGB 值，尝试着将他转化为图片





python

```python
from PIL import Image
import re

x = 180 #x坐标  对于文件里的RGB数据组进行分解
y = 180 #y坐标  x*y = 行数

rgb1 = [****] #RGB数据
print len(rgb1)/3 #计算有多少组RGB数据
m=0
for i in xrange(0,x):
    for j in xrange(0,y):

        line = rgb1[(3*m):(3*(m+1))]#获取一行
        m+=1
        rgb = line

        im.putpixel((i,j),(int(rgb[0]),int(rgb[1]),int(rgb[2])))#rgb转化为像素
im.show()
im.save("flag.png")
```

然后就是扫描获得一串字符串，base32-栅栏-凯撒获取flag



![20210913151921](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210913151921.png)

**20210913151921**



flag{QrC0de_iS_in7eRst1ng-}

## 图片转像素

### 例题-brainfun

神仙思路：

- 首先确定没有其他的隐写存在
- 这个图片的大小是512*512，但是可以匹配看成32*32的像素块
- RGB值全部都是16的倍数，也就是说，当以十六进制表示时，第二位永远是0
- 此外RGB值中还包含了透明度的值，而这些透明度的值并没有很多种，而且都是可打印字符的ascii值，包括一些小写字母和+，-，.的值
- 联想到题目brainfun，想到了brainfuck的编码，同时题目描述这是混乱的

因此思路就是提取A值，同时以RGB的顺序排列，最后解brainfuck





python

```python
# -*- coding: utf-8 -*-

from PIL import Image
from pybrainfuck import BrainFck


# Read image and get pixel data as list
pixels = list(Image.open('brainfun.png').getdata())


# Extract just get the blocks. Fun fact: PIL's resize with PIL.Image.NEAREST
# for nearest neighbor messes with the values, but mtPaint does it correctly.
pixels = [pixels[r*512 + c]
          for r in range(0, 512, 16)
          for c in range(0, 512, 16)]

# Sort the pixels by RGB value
pixels.sort(key=lambda p: (p[0] << 8) + (p[1] << 4) + p[2])

# Run the alpha values as Brainfuck
print("".join([chr(p[3]) for p in pixels]))
BrainFck().run("".join([chr(p[3]) for p in pixels]))
```

相关题目:

- [CSAW-2016-quals:Forensic/Barinfun](https://github.com/ctfs/write-ups-2016/tree/master/csaw-ctf-2016-quals/forensics/brainfun-50)
- [breakin-ctf-2017:A-dance-partner](https://github.com/ctfs/write-ups-2017/tree/master/breakin-ctf-2017/misc/A-dance-partner)

## PNG

### 文件格式

对于一个 PNG 文件来说，其文件头总是由位固定的字节来描述的，剩余的部分由 3 个以上的 PNG 的数据块（Chunk）按照特定的顺序组成。

文件头 `89 50 4E 47 0D 0A 1A 0A` + 数据块 + 数据块 + 数据块……

### 数据块CHUNk

PNG 定义了两种类型的数据块，一种是称为关键数据块（critical chunk），这是标准的数据块，另一种叫做辅助数据块（ancillary chunks），这是可选的数据块。关键数据块定义了 4 个标准数据块，每个 PNG 文件都必须包含它们，PNG 读写软件也都必须要支持这些数据块。

| 数据块符号 | 数据块名称             | 多数据块 | 可选否 | 位置限制           |
| :--------- | :--------------------- | :------- | :----- | :----------------- |
| IHDR       | 文件头数据块           | 否       | 否     | 第一块             |
| cHRM       | 基色和白色点数据块     | 否       | 是     | 在PLTE和IDAT之前   |
| gAMA       | 图像γ数据块            | 否       | 是     | 在PLTE和IDAT之前   |
| sBIT       | 样本有效位数据块       | 否       | 是     | 在PLTE和IDAT之前   |
| PLTE       | 调色板数据块           | 否       | 是     | 在IDAT之前         |
| bKGD       | 背景颜色数据块         | 否       | 是     | 在PLTE之后IDAT之前 |
| hIST       | 图像直方图数据块       | 否       | 是     | 在PLTE之后IDAT之前 |
| tRNS       | 图像透明数据块         | 否       | 是     | 在PLTE之后IDAT之前 |
| oFFs       | （专用公共数据块）     | 否       | 是     | 在IDAT之前         |
| pHYs       | 物理像素尺寸数据块     | 否       | 是     | 在IDAT之前         |
| sCAL       | （专用公共数据块）     | 否       | 是     | 在IDAT之前         |
| IDAT       | 图像数据块             | 是       | 否     | 与其他IDAT连续     |
| tIME       | 图像最后修改时间数据块 | 否       | 是     | 无限制             |
| tEXt       | 文本信息数据块         | 是       | 是     | 无限制             |
| zTXt       | 压缩文本数据块         | 是       | 是     | 无限制             |
| fRAc       | （专用公共数据块）     | 是       | 是     | 无限制             |
| gIFg       | （专用公共数据块）     | 是       | 是     | 无限制             |
| gIFt       | （专用公共数据块）     | 是       | 是     | 无限制             |
| gIFx       | （专用公共数据块）     | 是       | 是     | 无限制             |
| IEND       | 图像结束数据           | 否       | 否     | 最后一个数据块     |

对于每个数据块都有着统一的数据结构，每个数据块由 4 个部分组成

| 名称                            | 字节数   | 说明                                                 |
| :------------------------------ | :------- | :--------------------------------------------------- |
| Length（长度）                  | 4字节    | 指定数据块中数据域的长度，其长度不超过（231－1）字节 |
| Chunk Type Code（数据块类型码） | 4字节    | 数据块类型码由 ASCII 字母（A - Z 和 a - z）组成      |
| Chunk Data（数据块数据）        | 可变长度 | 存储按照 Chunk Type Code 指定的数据                  |
| CRC（循环冗余检测）             | 4字节    | 存储用来检测是否有错误的循环冗余码                   |

CRC（Cyclic Redundancy Check）域中的值是对 Chunk Type Code 域和 Chunk Data 域中的数据进行计算得到的。

### IHDR

文件头数据块 IHDR（Header Chunk）：它包含有 PNG 文件中存储的图像数据的基本信息，由 13 字节组成，并要作为第一个数据块出现在 PNG 数据流中，而且一个 PNG 数据流中只能有一个文件头数据块

其中我们关注的是前8字节的内容

| 域的名称 | 字节数  | 说明                   |
| :------- | :------ | :--------------------- |
| Width    | 4 bytes | 图像宽度，以像素为单位 |
| Height   | 4 bytes | 图像高度，以像素为单位 |

我们经常会去更改一张图片的高度或者宽度使得一张图片显示不完整从而达到隐藏信息的目的。



![pngihdr](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/pngihdr.png)

**pngihdr**



这里可以发现在 Kali 中是打不开这张图片的，提示 `IHDR CRC error`，而 Windows 10 自带的图片查看器能够打开，就提醒了我们 IHDR 块被人为的篡改过了，从而尝试修改图片的高度或者宽度发现隐藏的字符串。

对于png的IHDR部分的隐写，有如下的工具和脚本，可以解决大部分问题

- PCRT(还不错)：自动修复图片
- pngcheck（配合脚本使用）：自动检查宽高与crc的匹配关系
- magnetos（强烈推荐）: 一个强大的自动化misc工具
  - https://github.com/restran/magnetos.git
- pngcalculate：根据CRC校验和计算图片的宽高





python

~~~python
```python
import os
import binascii
import struct


misc = open("flag.png","rb").read()

for i in range(1024):
    data = misc[12:16] + struct.pack('>i',i)+ misc[20:29]
    crc32 = binascii.crc32(data) & 0xffffffff
    if crc32 == 0x932f8a6b:
        print i
~~~

#### 例题-evalheight

根据题目名称肯定是修改高度了,这里展示一下多种工具的使用.
magnetos：





bash

```bash
what_steg -f Evalheight.png
...
[*] PNG图片宽高CRC32校验失败，文件宽高被修改过
[*] 尝试爆破图片高度
[*] 找到正确的图片高度: 350
[*] 保存修正高度后的文件: fix_height.png
...
```



![20210927140005](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210927140005.png)

**20210927140005**



pngcheck&pngcalculate





bash

```bash
pngcheck -p Evalheight.png
File: Evalheight.png (92446 bytes)
Evalheight.png  CRC error in chunk IHDR (computed ca422c59, expected 52056cd4)
ERROR: Evalheight.png

python3 pngcal.py
430 350
hex: 0x1ae 0x15e
```

然后在010editor里面手动修改即可

#### 例题-realme

打开题目发现文件头是损坏的

![20210927230737](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210927230737.png)

**20210927230737**



修复了之后发现文件的宽高也与crc的校验和不匹配，因此计算真实的宽、高





bash

```bash
#通过pngcal计算出宽高的值，然后利用010editor修改获取flag
09 760
hex: 0x2c5 0x2f8
```



![20210927234257](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210927234257.png)

**20210927234257**



### PLTE

调色板数据块 PLTE（palette chunk）：它包含有与索引彩色图像（indexed-color image）相关的彩色变换数据，它仅与索引彩色图像有关，而且要放在图像数据块（image data
chunk）之前。真彩色的 PNG 数据流也可以有调色板数据块，目的是便于非真彩色显示程序用它来量化图像数据，从而显示该图像。

### IDAT

图像数据块 IDAT（image data chunk）：它存储实际的数据，在数据流中可包含多个连续顺序的图像数据块。

- 储存图像像数数据
- 在数据流中可包含多个连续顺序的图像数据块
- 采用 LZ77 算法的派生算法进行压缩
- 可以用 zlib 解压缩

值得注意的是，IDAT 块只有当上一个块充满时，才会继续一个新的块。

用 `pngcheck` 去查看此 PNG 文件





bash

```bash
λ .\pngcheck.exe -v sctf.png
File: sctf.png (1421461 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1000 x 562 image, 32-bit RGB+alpha, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 3780x3780 pixels/meter (96 dpi)
  chunk IDAT at offset 0x00057, length 65445
    zlib: deflated, 32K window, fast compression
  chunk IDAT at offset 0x10008, length 65524
...
  chunk IDAT at offset 0x150008, length 45027
  chunk IDAT at offset 0x15aff7, length 138
  chunk IEND at offset 0x15b08d, length 0
No errors detected in sctf.png (28 chunks, 36.8% compression).
```

可以看到，正常的块的 length 是在 65524 的时候就满了，而倒数第二个 IDAT 块长度是 45027，最后一个长度是 138，很明显最后一个 IDAT 块是有问题的，因为他本来应该并入到倒数第二个未满的块里.

利用 `python zlib` 解压多余 IDAT 块的内容，此时注意剔除 **长度、数据块类型及末尾的CRC校验值**。





python

```python
import zlib
import binascii
IDAT = "789...667".decode('hex')
result = binascii.hexlify(zlib.decompress(IDAT))
print result
```

### IEND

图像结束数据 IEND（image trailer chunk）：它用来标记 PNG 文件或者数据流已经结束，并且必须要放在文件的尾部。





none

```none
00 00 00 00 49 45 4E 44 AE 42 60 82
```

IEND 数据块的长度总是 `00 00 00 00`，数据标识总是 IEND `49 45 4E 44`，因此，CRC 码也总是 `AE 42 60 82`。

这里是可以隐藏数据的，解法也很简单，使用工具、010editor等都可以获取。

#### 例题-hidden

使用PCRT直接获取隐藏数据

![20210928093447](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210928093447.png)

**20210928093447**



#### 例题-hiddenplus

使用PCRT发现提示隐藏着PNG图片，分离图片得flag

![20210928093734](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210928093734.png)

**20210928093734**



### 其余辅助数据块

- 背景颜色数据块 bKGD（background color）
- 基色和白色度数据块 cHRM（primary chromaticities and white point），所谓白色度是指当 `R＝G＝B＝最大值` 时在显示器上产生的白色度
- 图像 γ 数据块 gAMA（image gamma）
- 图像直方图数据块 hIST（image histogram）
- 物理像素尺寸数据块 pHYs（physical pixel dimensions）
- 样本有效位数据块 sBIT（significant bits）
- 文本信息数据块 tEXt（textual data）
- 图像最后修改时间数据块 tIME （image last-modification time）
- 图像透明数据块 tRNS （transparency）
- 压缩文本数据块 zTXt （compressed textual data）

## LSB

LSB 全称 Least Significant Bit，最低有效位。PNG 文件中的图像像数一般是由 RGB 三原色（红绿蓝）组成，每一种颜色占用 8 位，取值范围为 `0x00` 至 `0xFF`，即有 256 种颜色，一共包含了 256 的 3 次方的颜色，即 16777216 种颜色。

而人类的眼睛可以区分约1000万种不同的颜色，意味着人类的眼睛无法区分余下的颜色大约有6777216种。

LSB 隐写就是修改 RGB 颜色分量的最低二进制位（LSB），每个颜色会有 8 bit，LSB 隐写就是修改了像数中的最低的 1 bit，而人类的眼睛不会注意到这前后的变化，每个像素可以携带 3 比特的信息。



![lsb](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/lsb.jpg)

**lsb**



如果是要寻找这种 LSB 隐藏痕迹的话，有一个工具 [Stegsolve](http://www.caesum.com/handbook/Stegsolve.jar) 是个神器，可以来辅助我们进行分析。

LSB 的信息借助于 Stegsolve 查看各个通道时一定要细心捕捉异常点，抓住 LSB 隐写的蛛丝马迹。

### 例题-lshhiddenplus1&lshhiddenplus

使用magnetos进行分析，在输出结果里发现这么一个压缩包
解压之后发现是一个elf文件





bash

```bash
file 1
1: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=8df45089fa39fec83423ec37a944e81065d16bee, not stripped
```

运行获取flag





bash

```bash
[Desktop] chmod +x 1
[Desktop] ./1
hctf{dd0gf4c3tok3yb0ard4g41n~~~}#  
```

另一种方法是借助 `Stegsolve-->Analyse-->Data Extract` 可以指定通道进行提取。

可以发现 `zip` 头，用 `save bin` 保存为压缩包后，打开运行其中的 ELF 文件就可以得到最后的 flag。



![20210927164819](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210927164819.png)

**20210927164819**



> 更多关于 LSB 的研究可以看 [这里](https://zhuanlan.zhihu.com/p/23890677)。

### 例题-lsbhidden

通过下方的按钮可以观察每个通道的信息，例如查看 R 通道的最低位第 8 位平面的信息。



![20210927161224](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210927161224.png)

**20210927161224**



## JPG

## 文件结构

- JPEG 是有损压缩格式，将像素信息用 JPEG 保存成文件再读取出来，其中某些像素值会有少许变化。在保存时有个质量参数可在 0 至 100 之间选择，参数越大图片就越保真，但图片的体积也就越大。一般情况下选择 70 或 80 就足够了
- JPEG 没有透明度信息

JPG 基本数据结构为两大类型：「段」和经过压缩编码的图像数据。

| 名 称   | 字节数 | 数据 | 说明                                        |
| :------ | :----- | :--- | :------------------------------------------ |
| 段 标识 | 1      | FF   | 每个新段的开始标识                          |
| 段类型  | 1      |      | 类型编码（称作标记码）                      |
| 段长 度 | 2      |      | 包括段内容和段长度本身,不包括段标识和段类型 |
| 段内容  | 2      |      | ≤65533字节                                  |

- 有些段没有长度描述也没有内容，只有段标识和段类型。文件头和文件尾均属于这种段。
- 段与段之间无论有多少 `FF` 都是合法的，这些 `FF` 称为「填充字节」，必须被忽略掉。

一些常见的段类型

![jpgformat](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/jpgformat.png)

**jpgformat**



`0xffd8` 和 `0xffd9`为 JPG 文件的开始结束的标志。

## 隐写软件

### [Stegdetect](https://github.com/redNixon/stegdetect)

通过统计分析技术评估 JPEG 文件的 DCT 频率系数的隐写工具, 可以检测到通过 JSteg、JPHide、OutGuess、Invisible
Secrets、F5、appendX 和 Camouflage 等这些隐写工具隐藏的信息，并且还具有基于字典暴力破解密码方法提取通过 Jphide、outguess 和 jsteg-shell 方式嵌入的隐藏信息。





bash

```bash
-q 仅显示可能包含隐藏内容的图像。
-n 启用检查JPEG文件头功能，以降低误报率。如果启用，所有带有批注区域的文件将被视为没有被嵌入信息。如果JPEG文件的JFIF标识符中的版本号不是1.1，则禁用OutGuess检测。
-s 修改检测算法的敏感度，该值的默认值为1。检测结果的匹配度与检测算法的敏感度成正比，算法敏感度的值越大，检测出的可疑文件包含敏感信息的可能性越大。
-d 打印带行号的调试信息。
-t 设置要检测哪些隐写工具（默认检测jopi），可设置的选项如下：
j 检测图像中的信息是否是用jsteg嵌入的。
o 检测图像中的信息是否是用outguess嵌入的。
p 检测图像中的信息是否是用jphide嵌入的。
i 检测图像中的信息是否是用invisible secrets嵌入的。
```

### [JPHS](http://linux01.gwdg.de/~alatham/stego.html)

JPEG 图像的信息隐藏软件 JPHS，它是由 Allan Latham 开发设计实现在 Windows 和 Linux 系统平台针对有损压缩 JPEG 文件进行信息加密隐藏和探测提取的工具。软件里面主要包含了两个程序 JPHIDE和 JPSEEK。JPHIDE 程序主要是实现将信息文件加密隐藏到 JPEG 图像功能，而 JPSEEK 程序主要实现从用 JPHIDE 程序加密隐藏得到的 JPEG 图像探测提取信息文件，Windows 版本的 JPHS 里的 JPHSWIN 程序具有图形化操作界面且具备 JPHIDE 和 JPSEEK 的功能。

### [SilentEye](http://silenteye.v1kings.io/)

> SilentEye is a cross-platform application design for an easy use of steganography, in this case hiding messages into pictures or sounds. It provides a pretty nice interface and an easy integration of new steganography algorithm and cryptography process by using a plug-ins system.

## GIF

## 文件结构

一个GIF文件的结构可分为

- 文件头（File Header）
  - GIF 文件署名（Signature）
  - 版本号（Version）
- GIF 数据流（GIF Data Stream）
  - 控制标识符
  - 图象块（Image Block）
  - 其他的一些扩展块
- 文件终结器（Trailer）

下表显示了一个 GIF 文件的组成结构：



![gif](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/gif.png)

**gif**



中间的那个大块可以被重复任意次

### 文件头

GIF 署名（Signature）和版本号（Version）。GIF 署名用来确认一个文件是否是 GIF 格式的文件，这一部分由三个字符组成：`GIF`；文件版本号也是由三个字节组成，可以为 `87a` 或 `89a`。

### 逻辑屏幕标识符（Logical Screen Descriptor）

Logical Screen Descriptor（逻辑屏幕描述符）紧跟在 header 后面。这个块告诉 decoder（解码器）图片需要占用的空间。它的大小固定为 7 个字节，以 canvas width（画布宽度）和 canvas height（画布高度）开始。

### 全局颜色列表（Global Color Table）

GIF格式可以拥有global color table，或用于针对每个子图片集，提供local color table。每个color
table由一个RGB（就像通常我们见到的（255，0，0）红色 那种）列表组成。

### 图像标识符（Image Descriptor）

一个 GIF 文件一般包含多个图片。之前的图片渲染模式一般是将多个图片绘制到一个大的（virtual
canvas）虚拟画布上，而现在一般将这些图片集用于实现动画。

每个 image 都以一个 image descriptor block（图像描述块）作为开头，这个块固定为 10 字节。



![imagesdescription](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/imagesdescription.png)

**imagesdescription**



### 图像数据（Image Data）

终于到了图片数据实际存储的地方。Image Data是由一系列的输出编码（output codes）构成，它们告诉decoder（解码器）需要绘制在画布上的每个颜色信息。这些编码以字节码的形式组织在这个块中。

### 文件终结器（Trailer）

该块为一个单字段块，用来指示该数据流的结束。取固定值0x3b.

更多参见 [gif 格式图片详细解析](https://www.jianshu.com/p/df52f1511cf8)

## 空间轴

由于GIF的动态特性，由一帧帧的图片构成，所以每一帧的图片，多帧图片间的结合，都成了隐藏信息的一种载体。

对于需要分离的GIF文件,可以使用`convert`命令将其每一帧分割开来





bash

```bash
convert cake.gif cake.png
ls
cake-0.png cake-1.png cake-2.png cake-3.png cake.gif
```

### 例题-cake

> WDCTF-2017:3-2

打开gif后，思路很清晰，分离每一帧图片后，将起合并得到完整的二维码即可



![20210928103111](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210928103111.png)

**20210928103111**



扫码后得到一串16进制字符串

```
03f30d0ab8c1aa5....74080006030908
```

开头`03f3`为`pyc`文件的头，恢复为`python`脚本后直接运行得到flag

反编译网站：https://tool.lu/pyc/

## 时间轴

GIF文件每一帧间的时间间隔也可以作为信息隐藏的载体。

例如在当时在XMan选拔赛出的一题

### 例题-XMAN-2017:100.gif

打开发现gif文件损坏，用010editor打开，发现缺少了文件头

通过`identify`命令清晰的打印出每一帧的时间间隔





bash

```bash
$ identify -format "%s %T \n" 100.gif
0 66
1 66
2 20
3 10
4 20
5 10
6 10
7 20
8 20
9 20
10 20
11 10
12 20
13 20
14 10
15 10
```

推断 `20 & 10` 分别代表 `0 & 1`，提取每一帧间隔并进行转化。





bash

```bash
$ cat flag|cut -d ' ' -f 2|tr -d '66'|tr -d '\n'|tr -d '0'|tr '2' '0'

#查看flag文件，以空格为分隔符，显示第二部分，删除66，删除换行，删除0，把2转换为0
0101100001001101010000010100111001111011001110010011011000110101001101110011010101100010011001010110010101100100001101000110010001100101011000010011000100111000011001000110010101100100001101000011011100110011001101010011011000110100001100110110000101100101011000110110011001100001001100110011010101111101#
```

最后转 ASCII 码得到 flag。

## 隐写软件

- [F5-steganography](https://github.com/matthewgao/F5-steganography)

## 条形码

- 宽度不等的多个黑条和空白，按照一定的编码规则排列，用以表达一组信息的图形标识符
- 国际标准
- EAN-13 商品标准，13 位数字
- Code-39：39 字符
- Code-128：128 字符
- [条形码在线识别](https://online-barcode-reader.inliteresearch.com/)

## 二维码

- 用某种特定几何图形按一定规律在平面分步的黑白相间的图形记录数据符号信息

- 堆叠式 / 行排式二维码：Code 16 k、Code 49、PDF417

- 矩阵式二维码：QR CODE

  

  ![![](.figureqr1.jpg)](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/![](.figureqr1.jpg).jpg)

  **![](.figureqr1.jpg)**

  

  

  ![![](.figureqr2.jpg)](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/![](.figureqr2.jpg).jpg)

  **![](.figureqr2.jpg)**

  

- 参考链接：https://ctf-wiki.org/misc/picture/introduction/

---

## 相关资源

- **脚本**:
  - [图片爆破宽高](CTF常用脚本及工具/图片爆破宽高/) — IHDR宽高爆破 (参见 L309-L443)
  - [CRC32校验爆破](CTF常用脚本及工具/CRC32校验爆破/) — PNG/压缩包 CRC爆破
  - [频域盲水印](CTF常用脚本及工具/频域盲水印/) — 频域水印加解密
  - [steghide爆破密码](CTF常用脚本及工具/steghide爆破密码/) — steghide密码爆破
  - [RGB转图片](CTF常用脚本及工具/RGB转图片/) — RGB值转图片
  - [字节转二维码](CTF常用脚本及工具/字节转二维码/) — 数据转二维码
- **工具**: Stegsolve / pngcheck / magnetos / pngcalculate / Stegdetect / JPHS / SilentEye
- **关联**: [压缩包总结.md](压缩包总结.md) — 同样涉及CRC32爆破
- **参考**: [音频隐写.md](音频隐写.md) — LSB音频隐写