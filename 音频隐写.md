# 音频隐写

> 创建: 未知 | 更新: 2026-05-21 | 适用: 不依赖语言 (WAV/MP3通用) | ⚠️ 部分图片托管于外部CDN

与音频相关的CTF题目主要使用隐写策略，分为 MP3隐写、LSB隐写、波形隐写、频谱隐写、DTMF、SSTV等。

---

## 一、快速检测流程

拿到音频文件后，依次做以下检查：

```bash
# 1. 基础信息
file audio.wav                    # 确认文件类型
strings audio.wav | head -20      # 搜索明文flag/密码/可疑字符串
exiftool audio.wav                # 查看元数据

# 2. 文件结构
binwalk -e audio.wav              # 提取嵌入文件（可能嵌了ZIP/图片）
pcregrep -M "RIFF.{4}WAVE" audio.wav  # 检查WAV头

# 3. 打开 Audacity 查看
# - 波形视图: 观察异常高低点、摩斯码、二进制编码
# - 频谱视图: 点击切换，看频谱图中是否有文字/形状
# - 声道分离: 左右声道可能有不同信息
```

---

## 二、MP3 隐写

### 原理与工具

MP3隐写主要使用 [Mp3Stego](http://www.petitcolas.net/steganography/mp3stego/)，将数据隐藏在MP3的11172-3编码层中。

### 命令行使用

```bash
# 编码：将文本隐藏到MP3
encode -E hidden_text.txt -P password svega.wav svega_stego.mp3

# 解码：从MP3提取隐藏文本
decode -X -P password svega_stego.mp3

# 输出文件为 <输入文件名>.txt
```

### MP3Stego检测技巧

```bash
# 检查MP3文件是否可能含隐写
strings file.mp3 | grep -i "mp3stego\|password\|secret\|flag"

# 常见密码字典爆破（配合密码本）
for pass in $(cat passwords.txt); do
    decode -X -P "$pass" file.mp3 2>/dev/null
    [ -f "file.mp3.txt" ] && cat "file.mp3.txt" && break
done
```

### 例题

> ISCC-2016: Music Never Sleep

初步观察后，由 `strings` 得到密码后使用 `Mp3Stego` 解密。GUI工具需要把文件放到程序根目录下。

解码后得到的字符串可能是 Base64/Base32 编码，需进一步解码。

---

## 三、波形隐写

### 原理

观察音频波形规律（高低、长短），将波形特征转化为01字符串或摩斯密码等，提取出最终flag。

### 3.1 摩斯密码型

**特征**: 波形呈现规律的长短间隔，类似摩斯码的点划。

**操作**: 用 Audacity 打开，放大波形，手动或通过脚本识别长短信号。

**解题步骤**:
1. 识别信号类型：波形不是标准正弦波即为信号
2. 判断点(`.`) 和划(`-`)：时间短的是点，长的是划
3. 记录摩斯码字符串
4. 用摩斯解码器转换

### 3.2 二进制编码型

**特征**: 波形呈现明显的高低两种电平。

**操作**: 取高点为 1，低点为 0，导出二进制串。

**解题步骤**:
1. 缩放波形找到编码区域（通常在开头或结尾）
2. 按固定采样间隔取点判断高低电平
3. 获得二进制串
4. 按 7 位或 8 位一组转 ASCII（字符串长度是7/8的倍数即正确）
5. 可能需要栅栏/凯撒等进一步解码

```python
# 二进制串转字符串
binary = "110011011011001100001110011111110111010111011000010101110101010110011011101011101110110111011110011111101"
# 7位一组
for i in range(0, len(binary), 7):
    print(chr(int(binary[i:i+7], 2)), end='')
# 8位一组
for i in range(0, len(binary), 8):
    print(chr(int(binary[i:i+8], 2)), end='')
```

### 3.3 声道差异型

**特征**: 左右声道波形不同。

**操作**: 
- Audacity 中分离声道（Split Stereo Track）
- 左右声道可能分别包含不同的编码信息
- 或左右声道的差值本身就是信号

---

## 四、频谱隐写

### 原理

音频频谱中将文字或图像隐藏在频率成分中。此类音频通常听起来像杂音或刺耳声。

**操作**: Audacity 中点击音轨左侧的"波形"下拉菜单 → 选择"频谱图"或"Spectrogram"。

### 4.1 频谱文字

直接切换频谱视图即可看到隐藏的文字（最直接的一类）。

### 4.2 频谱二维码

频谱中嵌入二维码图像。调整频谱视图的窗口大小和频率范围使二维码清晰可见。

> SU-CTF-quals-2014: hear_with_your_eyes — 频谱图中直接显示文字

---

## 五、DTMF（双音多频）

### 原理

DTMF是电话按键音系统，每个按键对应两个特定频率（行频率+列频率）。

### DTMF频率表

| 频率 (Hz) | 1209 | 1336 | 1477 | 1633 |
|-----------|------|------|------|------|
| **697** | 1 | 2 | 3 | A |
| **770** | 4 | 5 | 6 | B |
| **852** | 7 | 8 | 9 | C |
| **941** | * | 0 | # | D |

### 工具

```bash
# dtmf2num — 命令行DTMF解码
dtmf2num audio.wav

# multimon-ng — 通用信号解码器
multimon-ng -t wav -a DTMF audio.wav

# Audacity分析 — 查看频谱中的双频模式
# 菜单: Analyze → Plot Spectrum, 观察频率峰值判定按键
```

### 在线工具
- [DTMF Decoder](https://dtmf.netlify.app/) — 在线上传音频解码

---

## 六、SSTV（慢扫描电视）

### 原理

SSTV通过音频信号传输图像。在CTF中，将flag图片编码为SSTV音频，需要解码恢复。

### 工具

```bash
# QSSTV (Linux图形界面)
sudo apt install qsstv
# 用 pavucontrol 将音频输出路由到 QSSTV 输入

# Robot36 (Android)
# 手机靠近扬声器即可解码

# Virtual Audio Cable + MMSSTV (Windows)
# 播放音频 → Virtual Cable → MMSSTV 解码
```

### 常见模式

| 模式 | 分辨率 | 颜色 |
|------|--------|------|
| Scottie 1 | 320×256 | RGB |
| Scottie 2 | 320×256 | RGB |
| Martin 1 | 320×256 | RGB |
| Martin 2 | 320×256 | RGB |
| Robot 36 | 320×240 | YCrCb |
| PD 120 | 640×496 | B/W |

---

## 七、LSB 音频隐写

### 原理

类似于图片LSB隐写，音频采样值的LSB位被替换为隐藏数据。人耳无法察觉最低有效位的变化。

### 工具

**SilentEye**:
```bash
# GUI工具，支持 AES 加密
# 官网: http://silenteye.v1kings.io/
# 操作: 打开音频 → Decode → 选择格式 → 输入密钥 → 提取
```

**Python 脚本提取**:
```python
import wave

wav = wave.open('audio.wav', 'rb')
frames = wav.readframes(wav.getnframes())
# 提取每个采样的最低位
bits = ''.join(str(frame & 1) for frame in frames)
# 8位一组转字符
result = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits)//8*8, 8))
print(result)
```

### 检测

```bash
# stegolsb — LSB分析工具
stegolsb wavsteg -i audio.wav -o output.txt -b 1

# 查看采样值分布异常
# LSB隐写会导致采样值低位分布异常
```

---

## 八、其他音频隐写技巧

### 8.1 反向音频

```bash
# 用sox反转音频
sox input.wav output.wav reverse
```

有些flag隐藏在反转后的音频中，听起来像正常语音。

### 8.2 速度/音调调整

```bash
# sox调整速度
sox input.wav output.wav speed 2.0    # 2倍速
sox input.wav output.wav speed 0.5    # 半速

# sox调整音调
sox input.wav output.wav pitch 200     # 升200音分
```

### 8.3 频移

部分音频中隐藏的信息在正常频谱之外（如 >20kHz 或 <20Hz），需要用特定工具或脚本提取。

### 8.4 声道编码

左右声道通过差分解码：`信息 = L - R` 或 `信息 = L XOR R`

### 8.5 WAV文件头分析

```bash
# 检查WAV chunk结构
# WAV由RIFF头 + fmt chunk + data chunk组成
# 异常chunk中可能藏有额外数据
python3 -c "
import struct
with open('audio.wav', 'rb') as f:
    data = f.read()
    # 查找 'data' chunk 后面是否还有额外内容
    idx = data.find(b'data')
    if idx > 0:
        size = struct.unpack('<I', data[idx+4:idx+8])[0]
        remaining = len(data) - (idx + 8 + size)
        if remaining > 0:
            print(f'Found {remaining} bytes after data chunk')
            print(data[idx+8+size:idx+8+size+100])
"
```

---

## 九、常用工具汇总

| 工具 | 用途 | 平台 |
|------|------|------|
| Audacity | 波形/频谱查看、声道分离、速度调整 | Win/Mac/Linux |
| Adobe Audition | 专业音频分析（频谱图更清晰） | Win/Mac |
| Sonic Visualiser | 频谱/VAMP插件分析 | Win/Mac/Linux |
| Mp3Stego | MP3隐写编解码 | Win (GUI+CLI) |
| SilentEye | LSB隐写编解码 (AES加密) | Win/Mac/Linux |
| QSSTV | SSTV解码 | Linux |
| MMSSTV | SSTV解码 | Windows |
| multimon-ng | DTMF/多模式信号解码 | Linux |
| sox | 音频格式转换/速度/音调/反转 | Linux/Mac |
| ffmpeg | 格式转换/声道分离 | 全平台 |

---

## 相关资源

- **工具**: [SilentEye](http://silenteye.v1kings.io/) — 音频LSB隐写 | [MP3Stego](http://www.petitcolas.net/steganography/mp3stego/) — MP3隐写
- **关联**:
  - [图片隐写.md](图片隐写.md) — LSB隐写同类型，频谱/波形类比
  - [压缩包总结.md](压缩包总结.md) — 隐写后可能随压缩包一起出现
  - [文件包含.md](文件包含.md) — 音频文件可能作为隐写载体上传
- **WP搜索**: `wp_technique_index.json` → 标签 `音频隐写`
