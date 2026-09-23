# CTF 脚本工具索引

> 50+ 现成脚本，按场景分类，每个标注用途、用法和关键参数。
> 生成日期: 2026-05-21

---

## 一、Web 漏洞利用

### 1.1 双参数爆破脚本 (`双参数爆破脚本/`)

**用途**: Web参数爆破，遍历两个参数组合发HTTP请求。

**文件**: `brust.py`

**用法**:
```python
# 修改脚本中的 url 和参数列表
url = "http://target.com/api/endpoint"
# 使用 requests 遍历参数组合
python3 brust.py
```

**适用场景**: 需要同时爆破两个参数（如邀请码+用户ID）的Web题目。

---

### 1.2 日志匹配 (`日志匹配/`)

**用途**: 从URL编码的日志文件中提取字符，配合LFI日志包含攻击。

**文件**: `1.py`, `data.txt`

**用法**:
```bash
# data.txt 放LFI日志内容，脚本提取被包含文件的输出
python3 1.py
```

**原理**: 解析LFI请求日志中的URL编码内容，定位 `))=` 和 `--` 之间的字符输出。

**关联**: [文件包含.md](../文件包含.md) — 日志包含/Session包含章节

---

### 1.3 SQL注入 (`../工具使用/sqlmap-Cheat-Sheet.md`)

sqlmap速查表已转为Markdown格式，包含完整选项说明和常用组合。

---

## 二、密码学 / Crypto

### 2.1 RSA综合脚本利用 (`RSA综合脚本利用/`)

**用途**: 20+ 种RSA攻击场景的完整脚本集合。

**包含场景**:

| 目录 | 攻击类型 | 已知条件 |
|------|---------|---------|
| `e=3 (小公钥指数攻击)` | 小明文攻击 / Stereotyped messages | e=3, c, n |
| `已知 e、n、密文 c，求明文 m` | 基础RSA解密 | e, n, c → 分解n求d |
| `已知 e、n，求 d (e极大)` | Wiener's Attack | e极大, n |
| `已知 e1、e2、n (共模攻击)` | 共模攻击 | 同一m用不同e加密 |
| `已知 n、e、c、p、q 批量求 m` | n分解 + Roll按行加密 | n, e, c, p, q |
| `已知多个 n、c` | 中国剩余定理 (CRT) | 多个n, c |
| `已知 n、e、dp、c，求m` | dp泄露攻击 | n, e, dp, c |
| `已知 p、q、dp、dq、c 求明文 m` | dp/dq泄露 | p, q, dp, dq, c |
| `已知 e、d、c ,求 m` | 已知私钥 | e, d, c |
| `已知 c1、c2、n1、n2、e的范围` | 同q攻击 / 模不互质 | 多个n共享因子 |
| `共模攻击+base64隐写` | 共模+隐写组合 | e1, e2, n, c1, c2 |
| `已知 public key、密文 c` | 公钥提取/解析 | public.pem, c |
| `已知 e、m1、m2、n、pq 接近` | pq接近分解 | e, m1, m2, n |

**用法**: 根据已知条件选择对应目录，修改脚本中的参数值运行。

**关联**: 各子目录内通常包含 `problem` 或 `README` 文件说明具体输入格式。

---

### 2.2 DES加解密 (`DES_Python-master/`)

**用途**: Python DES加密/解密实现。

**文件**: `des.py`, `des_1.py`, `desstruct.py`, `README.md`

**用法**:
```python
from des import DES
# 具体接口参见 README.md
```

---

### 2.3 md5爆破 (`md5爆破/`)

**用途**: MD5哈希还原 — 对带通配符的明文枚举所有可能组合找哈希匹配。

**文件**: `md5-brust.py`

**用法**:
```python
# 修改 plaintext 为带 ? 的模板字符串
plaintext = 'TASC?O3RJMV?WDJKX?ZM'  # ? 为未知字符
# 脚本自动枚举 A-Z 替换所有 ?
python3 md5-brust.py
```

**适用场景**: 已知部分明文和MD5值，恢复完整明文。

---

### 2.4 维吉尼亚加密 (`维吉尼亚加密/`)

**用途**: 维吉尼亚密码加解密。

**文件**: `exp.py`

**用法**: 修改脚本中的密文和密钥参数。

---

### 2.5 变异凯撒 (`变异凯撒/`)

**用途**: 凯撒密码变体 — 每个字符偏移量递增/递减。

**文件**: `encode_caesar.py`, `variant_caesar.py`

**用法**:
```python
# variant_caesar.py — 偏移量逐个递减的凯撒
c = "密文"
for move in range(0, 50):
    flag = ""
    for i in c:
        flag += chr(ord(i) - move)
        move = move - 1
    print(flag)
```

**适用场景**: 题目中每个字符偏移量不同（如第一个偏移1，第二个偏移2...）的凯撒变体。

---

### 2.6 rot密码 (`rot/`)

**用途**: ROT13/ROT47 编解码。

**文件**: `rot.py`

**用法**:
```python
# 将 rot13 偏移的ASCII值还原
for i in list1:
    i = int(i) - 13
    print(chr(i), end='')
```

---

### 2.7 四方密码 (`四方密码/`)

**用途**: 四方密码（Four-Square Cipher）加解密。

**文件**: `sifang.py`

**用法**:
```python
matrix = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'  # 5x5矩阵(不含Q)
pla = 'abcdefghijklmnoprstuvwxyz'
key1 = '[SECURITY]'   # 密钥1
key2 = '[INFORMATION]'  # 密钥2
# 输出加密/解密结果
```

---

### 2.8 Nihilist密码 (`Nihilist密码/`)

**用途**: Nihilist密码解密 — 基于5x5密钥矩阵的替换密码。

**文件**: `nihilist.py`

**用法**:
```python
enc = 'PVSF{vVckHejqBOVX9C1c13GFfkHJrjIQeMwf}'
grid = 'LOVEKFC' + 'ABDGHIJLMNPQRSTUWXY'  # 5x5矩阵
# 脚本将密文字符在矩阵中查找并替换
python3 nihilist.py
```

---

### 2.9 toy密码 (`toy密码/`)

**用途**: Toy密码 — 基于映射表的双层替换密码（Toy加密系统的解密）。

**文件**: `toy.py`

**用法**:
```python
# list1: 密文4字符组→明文字母的映射
list1 = {'M':'ACEG', 'R':'ADEG', ...}
# list2: 字母表，用于第二层反向替换
# 输入密文4字符组序列，输出flag
```

---

### 2.10 26键盘密码-手机键盘密码 (`26键盘密码-手机键盘密码/`)

**用途**: 手机键盘密码（T9键盘映射）和26键盘布局密码。

**文件**: `jianpan.py`

**适用场景**: 数字对应手机键盘字母（2→ABC, 3→DEF...）或键盘坐标替换。

---

### 2.11 常用反解密脚本 (`常用反解密脚本/`)

**用途**: 通用解密模板 — XOR+偏移组合。

**文件**: `cryp-1.py`

**用法**:
```python
# 对每个字符: XOR 0x7 后 +3
for i in range(len(cipher)):
    flag = ord(cipher[i]) ^ 0x7
    flag += 3
    print(chr(flag), end='')
```

---

## 三、编码 / 解码

### 3.1 Base全家桶 (`Base/`)

**用途**: Base系列编码的各种变体处理。

**包含工具**:

| 子目录/文件 | 用途 |
|-------------|------|
| `B64-B32-B16解密` | Base64→Base32→Base16链式解密 |
| `b16-b32-b64-b85` | Base16/32/64/85互转 |
| `Base64扩展` | Base64变体（换表/填充变异） |
| `base64字符替换表` | 自定义Base64表的解码 |
| `base64异或` | Base64解码后XOR异或 |
| `base64解码输出字节文本` | Base64解码并输出原始字节 |
| `base64连续解码` | 递归Base64解码直到非Base64 |
| `base64隐写加密与解密` | Base64隐写（利用填充位隐藏信息） |
| `base混合匹配-4个python` | 4个Python脚本，多种Base混合匹配 |

---

### 3.2 进制互相转换 (`进制互相转换/`)

**用途**: 各种进制互转。

**文件**: `二进制高位补0` — 将二进制字符串高位补齐到8的倍数。

---

### 3.3 进制转化字符脚本 (`进制转化字符脚本/`)

**用途**: 进制数值转ASCII字符。

**文件**:
- `二进制转ascii` — 二进制字符串转ASCII
- `循环遍历减去1-128数的ASCII码.py` — 穷举ROT-N（N=1到128）找可读文本

---

### 3.4 hex倒叙 (`hex倒叙/`)

**用途**: hex字符串反转/倒序。

**文件**: `1.py`

---

### 3.5 hex减位 (`hex减位/`)

**用途**: hex值减去固定偏移后转字符。

**文件**: `1.py`

---

### 3.6 十进制转字符 (`十进制转字符/`)

**用途**: 十进制ASCII码转字符。

**文件**: `1.py`

---

### 3.7 二进制每8位倒序 (`二进制每8位倒序/`)

**用途**: 将二进制字符串每8位一组内部反转。

**文件**: `1.py`, `二进制8位分组.py`

**用法**:
```python
s = '011011000010110000...'
a = ''
for i in range(0, len(s), 8):
    a += (s[i:i+8])[::-1]  # 每8位内部反转
```

---

### 3.8 字符替换表 (`字符替换表/`)

**用途**: 自定义Base64映射表的解码 — 题目给了自定Base64表时使用。

**文件**: `zifu_replac.py`

**用法**:
```python
dict = {0: 'J', 1: 'K', ...}  # 自定义映射表
# 将密文字符通过自定义表映射回标准Base64再解码
```

---

### 3.9 字符频率统计分析 (`字符频率统计分析/`)

**用途**: 统计文本字符频率，用于替换密码分析。

**文件**: `test.py`, `test2.py`, `flag.txt`, `out.txt`

**用法**:
```python
# 统计 alphabet 中每个字符在文本中出现次数
# 按频率降序输出，辅助识别替换密码
python3 test.py
```

---

### 3.10 文本转GBK编码 (`文本转gbk编码/`)

**用途**: 文本内容转GBK编码写入文件。

**文件**: `1.py`

---

### 3.11 谍报-替换普通话 (`谍报-替换普通话/`)

**用途**: 同义词替换密码 — 通过对比两段"翻译"恢复原文。

**文件**: `tihuan.py`

**原理**: str1（原文）和 str2（替换版）是同义改写，str3是密文（用str2中词汇代替str1）。脚本通过构建str2→str1的映射表来解密str3。

**用法**:
```python
# 修改 str1, str2, str3 为题目给的文本
python3 tihuan.py
```

---

### 3.12 去重 (`去重/`)

**用途**: 文本文件行去重。

**文件**: `quchong.py`, `base64-zip.py`, `十六进制转字符.py`

**用法**:
```bash
# quchong.py: 读取 data.txt → 输出 data1.txt（去重后）
python3 quchong.py
```

---

### 3.13 替换脚本 (`替换脚本/`)

**用途**: 按行长度做0/1编码 — 将长短行转为二进制。

**文件**: `space.py`, `attachment.txt`

**用法**:
```python
# 6个字符的行 → '0', 其他行 → '1'
# 输出二进制串
```

---

## 四、隐写 / Misc

### 4.1 图片爆破宽高 (`图片爆破宽高/`)

**用途**: PNG IHDR宽高CRC32爆破 — 图片被错误修改宽高后恢复。

**文件**: `1.py`, `2.py`

**用法**:
```python
# 修改 crc32key 为文件中的实际CRC值
# 修改 file 为图片路径
# n 为搜索范围（默认4095）
crc32key = 0xC4ED3  # 从PNG IHDR chunk获取
python3 1.py
```

**原理**: 遍历可能的宽高值，计算IHDR CRC32，匹配后写入正确宽高。

---

### 4.2 频域盲水印 (`频域盲水印/`)

**用途**: 频域盲水印提取（基于OpenCV）。

**文件**: `pinyubwm.py`

**用法**:
```bash
python3 pinyubwm.py --original <原图> --image <带水印图> --result <输出图>
```

**依赖**: `opencv-python`, `numpy`

---

### 4.3 CRC32校验爆破 (`CRC32校验爆破/`)

**用途**: CRC32校验值爆破（1-5字节），用于还原被CRC32校验的小段数据。

**文件**: `crc-1byte.py`, `crc-2byte.py`, `crc-3byte.py`, `crc-4byte.py`, `crc-5byte.py`, `crc32`

**用法**:
```bash
# 根据要爆破的字节数选择对应脚本
# 修改脚本中的目标CRC32值
python3 crc-3byte.py  # 爆破3字节数据
```

**适用场景**: ZIP压缩包内小文件的CRC32已知，爆破文件内容；PNG IHDR CRC爆破。

---

### 4.4 steghide爆破密码 (`steghide爆破密码/`)

**用途**: steghide工具密码爆破（字典攻击）。

**文件**: `steghide-brute.py`, `english.dic`

**用法**:
```python
# 修改 stegoFile 为隐写图片路径
# 修改 extractFile 为提取目标文件名
# 字典文件: english.dic
python3 steghide-brute.py
```

**依赖**: 系统需安装 `steghide` 命令行工具。

---

### 4.5 TTL隐写 (`TTL隐写/`)

**用途**: IP报文TTL值隐写编解码。

**文件**: `TTL-encode.py`, `TTL-stego.py`, `TTL-stego2.py`, `out.txt`

**用法**:
```bash
# 编码: 将数据写入TTL值
python3 TTL-encode.py
# 解码: 从TTL值提取数据
python3 TTL-stego.py
```

**适用场景**: 流量分析题中IP TTL字段携带隐藏信息（常见值: 63, 127, 191, 255）。

---

### 4.6 USB流量解析 (`usb流量/`)

**用途**: USB HID键盘数据解析 — 从USB抓包提取按键。

**文件**: `usbtxt.py`

**用法**:
```bash
# 将USB数据放到 usbdata.txt
# 脚本解析 HID 键盘码→字符
python3 usbtxt.py
```

**适用场景**: pcap中包含USB HID设备流量，需恢复键盘输入。

---

### 4.7 曼彻斯特编码 (`曼彻斯特编码/`)

**用途**: 曼彻斯特编码/差分曼彻斯特解码。

**文件**: `decode_man.py`

**用法**:
```python
# 修改输入二进制串
# IEEE802 标准: 01→11, 10→00
dict = {"0101": "11", "1001": "01", "0110": "10", "1010": "00"}
```

**适用场景**: RFID/信号分析题中的曼彻斯特编码数据。

---

### 4.8 字节转二维码 (`字节转二维码/`)

**用途**: 将0/1文本矩阵转为二维码图像。

**文件**: `200-erweima.py`, `1.txt`

**用法**:
```python
# 1.txt: 200x200的0和1矩阵
# 脚本生成二维码PNG图像并显示
python3 200-erweima.py
```

---

### 4.9 RGB转图片 (`RGB转图片/`)

**用途**: RGB三元组文本转图片。

**文件**: `rgb.py`

**用法**:
```python
# qr.txt: 每行 R,G,B 值（如 "255,0,0"）
# 脚本逐像素生成图像
python3 rgb.py
```

---

### 4.10 批量解压压缩包+带密码 (`批量解压压缩包+带密码/`)

**用途**: ZIP压缩包递归解压（每层密码=文件名）。

**文件**: `zip.py`

**用法**:
```python
# 修改 name 为起始压缩包名（不含.zip）
# 每层解压密码 = 当前压缩包文件名(前4字符)
name = '0573'
python3 zip.py
```

**适用场景**: 多层嵌套ZIP，每层密码是当前文件名。

---

### 4.11 遍历读取压缩包文件判断1和0 (`遍历读取压缩包文件判断1和0/`)

**用途**: 根据压缩包内文件大小判断0/1 — 将文件大小差异转为二进制。

**文件**: `批量图片二进制.py`

**用法**:
```python
# 遍历ZIP内文件，根据 file_size 判断0或1
# 每8位二进制转一个字符
# 常见: 262字节→0, 其他→1
python3 批量图片二进制.py
```

---

### 4.12 流量数据提取脚本 (`流量数据提取脚本/`)

**用途**: 从pcap中提取特定协议数据（如ICMP payload）。

**文件**: `1.py`

**用法**:
```python
# 使用 scapy 解析 pcap
from scapy.all import *
packets = rdpcap('out.pcapng')
# 提取ICMP type 0 的payload后8字节
python3 1.py
```

**依赖**: `scapy`

---

### 4.13 红绿灯-二进制 (`红绿灯-二进制/`)

**用途**: 从图像序列中提取二进制数据 — 根据像素颜色判断0/1。

**文件**: `traffic.py`

**用法**:
```python
# 1168张PNG图片，每张检查特定像素颜色
# 红色>250 → '1', 绿色>250 → '0'
# 8位一组转ASCII
python3 traffic.py
```

---

### 4.14 emoji (`emoji/`)

**用途**: emoji-aes加解密。

**文件**: `js` (JavaScript实现)

---

## 五、逆向工程 / Reverse

### 5.1 XOR 异或 (`reverse/xor/`)

**用途**: XOR异或解密 — 相邻字符递推异或。

**文件**: `xor.py`

**用法**:
```python
# s: 混合列表（字符+数字），数字需先chr()
# 每个字符 = 前一个字符 XOR 当前字符
# flag[0]已知, 递推所有后续字符
python3 xor.py
```

---

### 5.2 文件异或 (`文件异或/`)

**用途**: 文件级XOR操作。

**文件**: `yihuo.py`, `010editor异或`, `二进制异或`

**用法**:
```python
# yihuo.py: 对hex文本每个值异或5
original = open("input", 'r').read()
for i in original:
    tmp = int(i, 16) ^ 5
    flag.write(hex(tmp)[2:])
```

---

### 5.3 Python-Brainfuck (`Python-Brainfuck-master/`)

**用途**: Brainfuck语言解释器。

**文件**: `brainfuck.py`, `getch.py`, `1.txt`, `README`

**用法**:
```bash
# 修改 1.txt 为Brainfuck代码
python3 brainfuck.py
```

---

### 5.4 APP逆向工具

**用途**: Android APP逆向辅助。

**关联**: [jadx-gui](https://github.com/skylot/jadx)（需从官网下载最新版）

---

## 六、辅助 / 工具

### 6.1 Python Pickle序列化 (`python-Picke序列化/`)

**用途**: Python Pickle反序列化漏洞利用。

**文件**: `1.py`, `123.txt`, `pickle.txt`, `坐标转化脚本`

---

### 6.2 批量修改文件名后缀 (`批量修改文件名后缀/`)

**用途**: 批量给文件添加后缀。

**文件**: `modify-suffix.py`

**用法**:
```python
# 修改 path 为目标目录
# 给所有文件追加 .jpg 后缀
python3 modify-suffix.py
```

---

### 6.3 数学题辅助 (`数学题/`)

**用途**: 取模运算等数学计算辅助。

**文件**: `取模/`

---

### 6.4 一些比赛的脚本 (`一些比赛的脚本/`)

**用途**: 特定比赛真题脚本。

**文件**: `祥云杯-xixixi/`

---

## 七、综合速查：题目特征 → 脚本

| 你遇到的 | 去哪个脚本 |
|---------|-----------|
| PNG图片打不开/尺寸不对 | `图片爆破宽高/` |
| 图片里有隐藏水印 | `频域盲水印/` |
| ZIP文件CRC已知需爆内容 | `CRC32校验爆破/` |
| ZIP嵌套很多层 | `批量解压压缩包+带密码/` |
| ZIP内文件大小不同需转二进制 | `遍历读取压缩包文件判断1和0/` |
| 图片用了steghide | `steghide爆破密码/` |
| pcap有USB流量 | `usb流量/` |
| pcap TTL值奇怪 | `TTL隐写/` |
| pcap需提取数据 | `流量数据提取脚本/` |
| RSA各种攻击 | `RSA综合脚本利用/` 找对应场景 |
| Base64解码后乱码 | `Base/base64异或`, `base64字符替换表` |
| Base64多次编码 | `Base/base64连续解码` |
| 古典密码-凯撒变体 | `变异凯撒/` |
| 古典密码-维吉尼亚 | `维吉尼亚加密/` |
| 古典密码-四方密码 | `四方密码/` |
| 古典密码-Nihilist | `Nihilist密码/` |
| 古典密码-键盘密码 | `26键盘密码-手机键盘密码/` |
| 古典密码-rot | `rot/` |
| 编码-XOR递推 | `reverse/xor/` |
| 编码-文件XOR | `文件异或/` |
| 编码-二进制反转 | `二进制每8位倒序/` |
| 编码-字符频率分析 | `字符频率统计分析/` |
| 编码-同义词替换 | `谍报-替换普通话/` |
| 编码-行长短→二进制 | `替换脚本/` |
| 编码-自定义Base64表 | `字符替换表/` |
| hex倒序/减偏移 | `hex倒叙/`, `hex减位/` |
| 0/1矩阵转二维码 | `字节转二维码/` |
| RGB元组转图片 | `RGB转图片/` |
| 图片序列提取二进制 | `红绿灯-二进制/` |
| Web双参数爆破 | `双参数爆破脚本/` |
| LFI日志包含后提取 | `日志匹配/` |
| MD5带通配符还原 | `md5爆破/` |
| Brainfuck/Ook语言 | `Python-Brainfuck-master/` |
| 曼彻斯特编码 | `曼彻斯特编码/` |
| emoji-aes | `emoji/` |
| Toy密码 | `toy密码/` |
| DES加解密 | `DES_Python-master/` |
| Pickle反序列化 | `python-Picke序列化/` |
| 去重/文本处理 | `去重/` |
| 字符频率分析 | `字符频率统计分析/` |

---

## 注意事项

- 各脚本可能需要按题目实际情况修改硬编码参数（URL、文件路径、密钥等）
- RSA脚本集合中的子目录按攻击类型命名，根据已知条件选择匹配场景
- Base/ 目录包含8个子工具，覆盖Base64各种变体场景
- 部分脚本依赖第三方库：`scapy`（流量提取）、`opencv-python`（盲水印）、`PIL/Pillow`（图像处理）
- ScreenToGif 可从[官网](https://github.com/NickeManarin/ScreenToGif)下载，用于录屏
