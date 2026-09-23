## ZIP类

> 创建: 未知 | 更新: 2026-05-21 | 适用: 不依赖语言 (ZIP/RAR/7z通用)

### 文件结构

`ZIP` 文件主要由三部分构成，分别为

| 压缩源文件数据区                                | 核心目录          | 目录结束                        |
| :---------------------------------------------- | :---------------- | :------------------------------ |
| local file header + file data + data descriptor | central directory | end of central directory record |

- 压缩源文件数据区中每一个压缩的源文件或目录都是一条记录，其中

  - `local file header` ：文件头用于标识该文件的开始，记录了该压缩文件的信息，这里的文件头标识由固定值 `50 4B 03 04` 开头，也是 `ZIP` 的文件头的重要标志
  - `file data` ：文件数据记录了相应压缩文件的数据
  - `data descriptor` ：数据描述符用于标识该文件压缩结束，该结构只有在相应的 `local file header` 中通用标记字段的第 `3 bit` 设为 `1` 时才会出现，紧接在压缩文件源数据后

- `Central directory` 核心目录

  - 记录了压缩文件的目录信息，在这个数据区中每一条纪录对应在压缩源文件数据区中的一条数据。

    | Offset | Bytes | Description                                          | 译                                      |
    | :----- | :---- | :--------------------------------------------------- | :-------------------------------------- |
    | 0      | 4     | Central directory file header signature = 0x02014b50 | 核心目录文件 header标识 =（0x02014b50） |
    | 4      | 2     | Version made by                                      | 压缩所用的 pkware 版本                  |
    | 6      | 2     | Version needed to extract (minimum)                  | 解压所需 pkware 的最低版本              |
    | 8      | 2     | General purpose bit flag                             | 通用位标记伪加密                        |
    | 10     | 2     | Compression method                                   | 压缩方法                                |
    | 12     | 2     | File last modification time                          | 文件最后修改时间                        |
    | 14     | 2     | File last modification date                          | 文件最后修改日期                        |
    | 16     | 4     | CRC-32                                               | CRC-32 校验码                           |
    | 20     | 4     | Compressed size                                      | 压缩后的大小                            |
    | 24     | 4     | Uncompressed size                                    | 未压缩的大小                            |
    | 28     | 2     | File name length (n)                                 | 文件名长度                              |
    | 30     | 2     | Extra field length (m)                               | 扩展域长度                              |
    | 32     | 2     | File comment length (k)                              | 文件注释长度                            |
    | 34     | 2     | Disk number where file starts                        | 文件开始位置的磁盘编号                  |
    | 36     | 2     | Internal file attributes                             | 内部文件属性                            |
    | 38     | 4     | External file attributes                             | 外部文件属性                            |
    | 42     | 4     | relative offset of local header                      | 本地文件头的相对位移                    |
    | 46     | n     | File name                                            | 目录文件名                              |
    | 46+n   | m     | Extra field                                          | 扩展域                                  |
    | 46+n+m | k     | File comment                                         | 文件注释内容                            |

- `End of central directory record(EOCD)` 目录结束标识

  - 目录结束标识存在于整个归档包的结尾，用于标记压缩的目录数据的结束。每个压缩文件必须有且只有一个 `EOCD` 记录。

更加详细参见 [官方文档](https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.2.0.txt)。

### ZIP数据结构

#### 压缩源文件数据区

| 数据        | 含义                         |
| :---------- | :--------------------------- |
| 50 4B 03 04 | 这是头文件标记（0x04034b50） |
| 14 00       | 解压文件所需 pkware 版本     |
| 00 00       | 全局方式位标记（有无加密）   |
| 08 00       | 压缩方式                     |
| 5A 7E       | 最后修改文件时间             |
| F7 46       | 最后修改文件日期             |
| 16 B5 80 14 | CRC-32校验（1480B516）       |
| 19 00 00 00 | 压缩后尺寸（25）             |
| 17 00 00 00 | 未压缩尺寸（23）             |
| 07 00       | 文件名长度                   |
| 00 00       | 扩展记录长度                 |

![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210903151348.png)

#### 核心目录区

| 数据        | 含义                                                         |
| :---------- | :----------------------------------------------------------- |
| 50 4B 01 02 | 目录中文件文件头标记(0x02014b50)                             |
| 3F 00       | 压缩使用的 pkware 版本                                       |
| 14 00       | 解压文件所需 pkware 版本                                     |
| 00 00       | 全局方式位标记（有无加密，这个更改这里进行伪加密，改为09 00打开就会提示有密码了） |
| 08 00       | 压缩方式                                                     |
| 5A 7E       | 最后修改文件时间                                             |
| F7 46       | 最后修改文件日期                                             |
| 16 B5 80 14 | CRC-32校验（1480B516）                                       |
| 19 00 00 00 | 压缩后尺寸（25）                                             |
| 17 00 00 00 | 未压缩尺寸（23）                                             |
| 07 00       | 文件名长度                                                   |
| 24 00       | 扩展字段长度                                                 |
| 00 00       | 文件注释长度                                                 |
| 00 00       | 磁盘开始号                                                   |
| 00 00       | 内部文件属性                                                 |
| 20 00 00 00 | 外部文件属性                                                 |
| 00 00 00 00 | 局部头部偏移量                                               |



![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210903151540.png)



#### 压缩源文件目录结束标志

| 数据        | 含义                       |
| :---------- | :------------------------- |
| 50 4B 05 06 | 目录结束标记               |
| 00 00       | 当前磁盘编号               |
| 00 00       | 目录区开始磁盘编号         |
| 01 00       | 本磁盘上纪录总数           |
| 01 00       | 目录区中纪录总数           |
| 59 00 00 00 | 目录区尺寸大小             |
| 3E 00 00 00 | 目录区对第一张磁盘的偏移量 |
| 00 00       | ZIP 文件注释长度           |



![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210903163943.png)



### 主要攻击

#### 爆破

这里主要介绍两款爆破使用的工具

- `Windows`下的神器 [ARCHPR](http://www.downcc.com/soft/130539.html)



![ARCHPR](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210905194927.png)

**ARCHPR**



- `Linux` 下的命令行工具 [fcrackzip](https://github.com/hyc/fcrackzip)

##### 暴力破解

作为最普通的密码攻击手段，ARCHPR允许在范围选项卡中，选择暴力破解的字符集：

其中”所有特殊符号”为：





bash

```bash
!@#$%^&*()_+-=<>,./?[]{}~:;`'|"\
```

此外，可以自定义字符集：通过勾选用户定义，然后点击右边的”自定义字符集”选项

如你所见，在给定的字符集中，只囊括了ASCII可打印字符，如果 .zip 的密码是中文的话，那就必须选择”自定义字符集”，并且勾选转换为OEM编码；否则密码会”Not Found”

- 在长度选项卡中，设置密码长度：
- 在范围选项卡的右边，可以看到：开始于、结束于

这里就得知道，ARCHPR在暴力破解密码的时候，是采用特定的顺序的：

- 大小字母 A - Z
- 空格
- 小写字母 a - z
- 数字 0 - 9
- 特殊字符 !@#$ …
  也就是说，暴力破解密码的顺序大致为：

bash

```bash
"AAA" -> "AAB" -> "AAC" -> ... -> "AAZ" -> "AA " -> "AAa" -> "AAb" -> ... -> "AAz" -> "AA0" -> "AA1" -> ... -> "AA9" -> "AA!" -> "AA@"
```

上图的”开始于”有2个作用：

当你知道密码长度为5，并且第一个字符为 k，你可以在”开始于”设置`kAAAA`，那么ARCHPR将跳过`AAAAA`到`kAAAA`的前一个的暴力破解，节省时间
如果破解密码的时间太长，ARCHPR会每隔5分钟自动保存密码（在自动保存选项卡中可以选择），如果某次暴力破解被迫中断，那么可以通过查看最后一次保存的密码，并设置”开始于”，直接从上次爆破的地方继续开始爆破
“结束于”的作用类似

###### 例题

在这里，引出ARCHPR的第一个坑：

我们尝试用ARCHPR暴力破解出 的密码，结果却显示：

![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906112305.png)

出现这个报错是因为.zip 的压缩算法是有版本的，ARCHPR不支持较高压缩版本的 .zip，所以这个时候可以使用fcrackzip进行爆破





![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906135631.png)



##### 掩码

掩码攻击属于局部暴力破解，如果你已经知道部分的密码，那么可以直接输入它，再用`?`来代替那些不知道的部分；随后ARCHPR就会爆破`?`处的字符

注意掩码攻击是固定长度的

比如我知道密码的长度为7，后4位是`love`，那么就可以在掩码处填入`???love`

确定掩码后，爆破方式与暴力破解没什么不同

如果密码本身就可能包含`?`，那可以在高级选项卡中，更改默认的掩码符号`?`

###### 例题



![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906153540.png)



##### 字典攻击

字典相比较暴力破解更”智能”，因为字典中包含了大部分可能使用的密码，而不是毫无头绪的穷尽遍历

一份好的字典是必须的，字典囊括的密码数决定了字典攻击的效果

> 比如Github上就有许多爆破字典：https://github.com/rootphantomer/Blasting_dictionary

ARCHPR为字典攻击提供了3个选项：

- 智能变化

  “智能变化”是针对字典元素的：假如当字典攻击到 password 时，ARCHPR会自动将 password 进行变化：

  PASSword、passWORD、全小写 password、全大写 PASSWORD、首字母大写 Password、首字母小写 pASSWORD、元音字母大写 pAsswOrd、元音字母小写 PaSSWoRD、间隔变化1 PaSsWoRd、间隔变化2 pAsSwOrD

  对于字典中的每个元素，都会执行上面10种变化，增大破解几率，但破解时间会增大10倍

- 尝试所有可能的大/小写组合

  以字典元素 password 为例，ARCHPR会依次尝试每个字母的大小写组合：

  password -> passworD -> passwoRd -> passwoRD -> … -> PASSWORD

很显然，这种情况下破解时间会大幅增加

- 转换为OEM编码

  当字典元素不只包含拉丁字母(Latin Letters)时，这个选项才会生效

###### 例题



![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210907101221.png)



##### 注释

有些时候出题人会把密码直接放到注释里面，注意一下就好

###### 例题1



![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210907102155.png)

这里题目中就在注释里隐藏了摩斯电码



###### 例题2

除了这种明文的注释，还有一种比较流氓的注释，会把注释进行反色或者利用tab和空格制造摩斯电码

![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210907104933.png)





![img](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210907145728.png)



#### CRC32

##### 原理

`CRC` 本身是「冗余校验码」的意思，`CRC32` 则表示会产生一个 `32 bit` ( `8` 位十六进制数)的校验值。由于 `CRC32` 产生校验值时源数据块的每一个 `bit` (位)都参与了计算，所以数据块中即使只有一位发生了变化，也会得到不同的 `CRC32` 值。

`CRC32` 校验码出现在很多文件中比如 `png` 文件，同样 `zip` 中也有 `CRC32` 校验码。值得注意的是 `zip` 中的 `CRC32` 是未加密文件的校验值。

这也就导致了基于 `CRC32` 的攻击手法。

- 文件内内容很少(一般比赛中大多为 `4` 字节左右)
- 加密的密码很长

我们不去爆破压缩包的密码，而是直接去爆破源文件的内容(一般都是可见的字符串)，从而获取想要的信息。

比如我们新建一个 `flag.txt`，其中内容为 `123`，使用密码 `!QAZXSW@#EDCVFR$` 去加密。

!!! note
​ 在爆破时我们所枚举的所有可能字符串的 `CRC32` 值是要与压缩源文件数据区中的 `CRC32` 值所对应





python

```python
# -*- coding: utf-8 -*-

import binascii
import base64
import string
import itertools
import struct

alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='

crcdict = {}
print "computing all possible CRCs..."
for x in itertools.product(list(alph), repeat=4):
    st = ''.join(x)
    testcrc = binascii.crc32(st)
    crcdict[struct.pack('<i', testcrc)] = st
print "Done!"

f = open('flag.zip')
data = f.read()
f.close()
crc = ''.join(data[14:18])
if crc in crcdict:
    print crcdict[crc]
else:
    print "FAILED!"
```

##### 例题

根据每个压缩包内的文件大小可以推断使用 `CRC32` 攻击手法，获得每个压缩包内的内容后连在一起 `Base64` 解码后是一个加密的压缩包，爆破获得 `flag`。

![20210905195800](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210905195800.png)

**20210905195800**







python

```python
#coding:utf-8
import zipfile
import string
import binascii

def CrackCrc(crc):
    for i in dic:
        for j in dic:
            for p in dic:
                for q in dic:
                    s = i + j + p + q
                    if crc == (binascii.crc32(s) & 0xffffffff):
                        #print s
                        f.write(s)
                        return

def CrackZip():
    for I in range(1,6):
        file = 'flag' + str(I)+ '.zip'
        f = zipfile.ZipFile(file, 'r')
        GetCrc = f.getinfo('flag'+str(I)+'.txt')
        crc = GetCrc.CRC
        #以上3行为获取压缩包CRC32值的步骤
        print hex(crc)
        CrackCrc(crc)

dic = string.ascii_letters + string.digits + '{}_+/='

f = open('out.txt', 'w')
CrackZip()
f.close()
```



![20210905201011](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210905201011.png)

**20210905201011**



#### 明文攻击

##### 原理

- .zip 传统加密算法本质上是`伪随机数流`和`明文`进行异或，产生这个伪随机流需要用到3个32 bits的key；`找到这3个key，就能解开加密的文件`
- 压缩软件用这3个key加密压缩包中的所有文件，当我们得到已加密压缩包中的任意一个文件，如果我们用同样的压缩方法进行无密码的压缩，得到的无密码 .zip 和有密码的 .zip 进行比较，分析两个文件的不同点，就能得到3个key了
- 所谓明文是指我们通过某些方法得到的已经加密的 .zip 文件中的部分文件
- 用相同的压缩方法将该明文压缩成 .zip在拥有2个 .zip 文件后，由于新的 .zip 和原本的 .zip 用同样的压缩方法放置入了至少1个相同的文件，那么就能够根据新的 .zip 爆破出压缩密码
- 明文需大于12 bytes

如果你已经知道加密文件的部分内容，比如在某个网站上发现了它的 `readme.txt` 文件，你就可以开始尝试破解了。

首先，将这个明文文件打包成 `zip` 包，比如将 `readme.txt` 打包成 `readme.zip` 。

打包完成后，需要确认二者采用的压缩算法相同。一个简单的判断方法是用 `WinRAR` 打开文件，同一个文件压缩后的体积是否相同。如果相同，基本可以说明你用的压缩算法是正确的。如果不同，就尝试另一种压缩算法。

##### 工具

- Windows下的神器 [ARCHPR](http://www.downcc.com/soft/130539.html)

##### 例题

> 2015广州强网杯：爆破？
>
> WP：https://www.cnblogs.com/ECJTUACM-873284962/p/9884416.html

首先我们拿到这样一道题，题目标题为**爆破?**，很明显这题肯定是要用到一个破解工具，很暴力的说。

**第一步、分析压缩包文件**

我们下载了这个压缩包以后，我们看到文件名是 ***.zip** 结尾，我们可以立即想到破解压缩包常用的几种方式，我们将其压缩包解压出来，发现里面有两个文件，分别为 `Desktop.zip` 和 `readme.txt` ，我们看看 `readme.txt` 里面写了什么？



![readme](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906092945.png)

**readme**

打开以后竟然是`qianwanbuyaogeixuanshoukandao!!!` ，出题人不想让选手看到，这出题人还是有点意思。我们再看看那个 `Desktop.zip` ，我们可以看到里面有个 `readme.txt` 文件和 `answer` 文件夹， `answer` 文件夹下有 `key.txt` 文件， `flag` 应该就藏在这里了。



**第二步、分析破解方式**

这题目拿到手上，我们首先发现解压出来的文件和 `Desktop.zip` 压缩包中都含有同样一个文件 `readme.txt` ，而且并没有给出其他相关信息，且文件大小大于 `12Byte` ，我们再对比压缩包中的 `readme.txt` 和原压缩包中的 `readme.txt` 的 `CRC32` 的值，我们发现两个值相同，这说明解压出的 `readme.txt` 是加密压缩包里的 `readme.txt` 的明文，于是我们可以大胆地猜测这极可能是个明文加密。



![20210906104323](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906104323.png)

**20210906104323**



**第三步、尝试明文攻击**

既然我们已经知道了它是明文攻击的话，我们将对其压缩包进行破解，由于解压出的readme.txt是加密压缩包里的 `readme.txt` 的明文，将 `readme.txt` 压缩成 **.zip** 文件，然后在软件中填入相应的路径即可开始进行明文攻击。

**坑点来了**
在使用明文攻击的时候，经常会出现这种报错，那是题目不是用明文攻击吗？并不是的

![20210906110144](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906110144.png)

**20210906110144**



构造明文压缩包时要选用与加密压缩包相同的压缩软件，如果他`WinRar`压的，你用`7z`构造出的压缩包来做明文压缩包，软件是会报错的

**再尝试**

我们已经发现了这个问题，我们去官网下载 `7zip` ：https://www.7-zip.org/

然后我们对原压缩文件用 `7z` 进行解压缩，然后将 `readme.txt` 用7z进行压缩即可。然后我们就可以用 `ARCHPR` 进行明文攻击了。

**又一个坑点**

明文攻击



![20210906102641](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906102641.png)

**20210906102641**



这里我们看到爆破需要将近两个小时，如果你非常有耐心，爆破完成之后你会看到这个：



![20210906110544](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906110544.png)

**20210906110544**



口令未找到，到这里你可能会觉得明文攻击失败了，其实并没有，可以看到软件提示`加密密钥已成功恢复！`

> 关于zip的加密原理需要知道的是：.zip 的加密过程中会生成3个key(加密密钥)，如果我们能够得到key，那么哪怕没有密码，也能够通过明文和key复现出加密压缩包中的文件

在使用明文攻击的时候不妨在结束阶段二后就停止攻击，打开保存下来的 .zip 文件，就能得到flag



![20210906111208](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210906111208.png)

**20210906111208**

我们将 `Desktop_decrypted.zip` 解压出来，查看 `answer` 目录下的 `key.txt` 即可。



所以最终的flag为：**`flag{7ip_Fi13_S0m3tim3s_s0_3a5y@}`**

#### 伪加密

##### 原理

在上文 `ZIP` 格式中的 **核心目录区** 中，我们强调了一个叫做通用位标记 `(General purpose bit flag)` 的 `2` 字节，不同比特位有着不同的含义。





bash

```bash
Bit 0: If set, indicates that the file is encrypted.

(For Method 6 - Imploding)
Bit 1: If the compression method used was type 6,
     Imploding, then this bit, if set, indicates
     an 8K sliding dictionary was used.  If clear,
     then a 4K sliding dictionary was used.
...
Bit 6: Strong encryption.  If this bit is set, you should
     set the version needed to extract value to at least
     50 and you must also set bit 0.  If AES encryption
     is used, the version needed to extract value must
     be at least 51.
...
```

修改伪加密的方法：

- `16` 进制下修改通用位标记
- `binwalk -e` 无视伪加密
- 在 `Mac OS` 及部分 `Linux`(如 `Kali` )系统中，可以直接打开伪加密的 `ZIP` 压缩包
- 检测伪加密的小工具 `ZipCenOp.jar`
- 有时候用 `WinRar` 的修复功能（此方法有时有奇效，不仅针对伪加密）

> ZipCenOp.zip 对正常加密的 .zip 压缩包会直接修改所有加密位为偶数，虽然会让ZIP压缩软件显示”未加密”，但往往 .zip 文件也损坏了，得到”CRC校验错误”的结果

所以如果拿到加密了的 .zip 文件，还是建议用十六进制编辑器打开，将加密位手动改回偶数；如果发现损坏了，则证明不是伪加密，再把加密位改回，尝试其它办法

可以比对数据区和目录区的加密位，伪加密往往只会修改目录区的加密位（因为这样就能起到效果），而正常的加密会同时修改两者的加密位

![20210907174025](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/20210907174025.png)

**20210907174025**

如果出题人把两处的加密位都修改了，那只好一一尝试了



## Rar类

### 文件格式

RAR 文件主要由标记块，压缩文件头块，文件头块，结尾块组成。

其每一块大致分为以下几个字段：

| 名称       | 大小 | 描述                  |
| :--------- | :--- | :-------------------- |
| HEAD_CRC   | 2    | 全部块或块部分的CRC   |
| HEAD_TYPE  | 1    | 块类型                |
| HEAD_FLAGS | 2    | 阻止标志              |
| HEAD_SIZE  | 2    | 块大小                |
| ADD_SIZE   | 4    | 可选字段 - 添加块大小 |

Rar压缩包的文件头为 `0x 52 61 72 21 1A 07 00`。

紧跟着文件头（0x526172211A0700）的是标记块（MARK_HEAD），其后还有文件头（File Header）。

| 名称          | 大小            | 描述                                                         |
| :------------ | :-------------- | :----------------------------------------------------------- |
| HEAD_CRC      | 2               | CRC of fields from HEAD_TYPE to FILEATTR and file name       |
| HEAD_TYPE     | 1               | Header Type: 0x74                                            |
| HEAD_FLAGS    | 2               | Bit Flags (Please see ‘Bit Flags for File in Archive’ table for all possibilities)（伪加密） |
| HEAD_SIZE     | 2               | File header full size including file name and comments       |
| PACK_SIZE     | 4               | Compressed file size                                         |
| UNP_SIZE      | 4               | Uncompressed file size                                       |
| HOST_OS       | 1               | Operating system used for archiving (See the ‘Operating System Indicators’ table for the flags used) |
| FILE_CRC      | 4               | File CRC                                                     |
| FTIME         | 4               | Date and time in standard MS DOS format                      |
| UNP_VER       | 1               | RAR version needed to extract file (Version number is encoded as 10 * Major version + minor version.) |
| METHOD        | 1               | Packing method (Please see ‘Packing Method’ table for all possibilities |
| NAME_SIZE     | 2               | File name size                                               |
| ATTR          | 4               | File attributes                                              |
| HIGH_PACK_SIZ | 4               | High 4 bytes of 64-bit value of compressed file size. Optional value, presents only if bit 0x100 in HEAD_FLAGS is set. |
| HIGH_UNP_SIZE | 4               | High 4 bytes of 64-bit value of uncompressed file size. Optional value, presents only if bit 0x100 in HEAD_FLAGS is set. |
| FILE_NAME     | NAME_SIZE bytes | File name - string of NAME_SIZE bytes size                   |
| SALT          | 8               | present if (HEAD_FLAGS & 0x400) != 0                         |
| EXT_TIME      | variable size   | present if (HEAD_FLAGS & 0x1000) != 0                        |

每个 RAR 文件的结尾快（Terminator）都是固定的。

| Field Name | Size (bytes) | Possibilities       |
| :--------- | :----------- | :------------------ |
| HEAD_CRC   | 2            | Always 0x3DC4       |
| HEAD_TYPE  | 1            | Header type: 0x7b   |
| HEAD_FLAGS | 2            | Always 0x4000       |
| HEAD_SIZE  | 2            | Block size = 0x0007 |

更多详见 https://forensicswiki.xyz/wiki/index.php?title=RAR

### 主要攻击

#### 伪加密

RAR 文件的伪加密在文件头中的位标记字段上，用 010 Editor 可以很清楚的看见这一位，修改这一位可以造成伪加密。



![6](https://cdn.jsdelivr.net/gh/AMG4MATIC/PicGo/img/6.png)

**6**



其余明文攻击等手法依旧同 ZIP 中介绍的一样。

## 7z

### 7z文件头





bash

```bash
37 7A BC AF 27 1C
```

#### 参考文献

---

## 相关资源

- **脚本**:
  - [CRC32校验爆破](CTF常用脚本及工具/CRC32校验爆破/) — ZIP CRC32 1-5字节爆破 (参见 L283-L395)
  - [批量解压压缩包](CTF常用脚本及工具/批量解压压缩包+带密码/) — 批量解压带密码压缩包
  - [遍历压缩包判断1和0](CTF常用脚本及工具/遍历读取压缩包文件判断1和0/) — 根据压缩包内容判断二进制
  - [md5爆破](CTF常用脚本及工具/md5爆破/) — 配合压缩包密码爆破
- **关联**: [图片隐写.md](图片隐写.md) — PNG的CRC校验同类型攻击 (L309-L361)