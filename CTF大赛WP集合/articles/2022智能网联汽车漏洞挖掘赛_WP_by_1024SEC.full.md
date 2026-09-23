---
title: 2022 智能网联汽车漏洞挖掘赛 WP by 1024SEC
contest: 2022 智能网联汽车漏洞挖掘赛
year: 2022
difficulty: medium
vuln_type:
- misc_unknown
- reverse
- crypto_oracle
tags:
- UART
- USB-HID
- Saleae-Logic-Analyzer
- 逻辑分析仪
- tshark
- usb.capdata
- USB-keyboard
- ngram-score
- hill-cipher
- 车联网
- IoV
attack_chain:
- 'Q1 UART: 附件是 Saleae 逻辑分析仪导出, 还原 8-N-1 帧格式, 解析串口数据'
- 'Q2 USB HID: tshark -r usb.pcap -T fields -e usb.capdata 提取 8 字节键盘数据'
- WangYihang UsbKeyboardHacker.py 解析 04-2b 16 进制键码 → normalKeys / shiftKeys 映射
- '每个键 8 字节: 修饰键 + 保留 + 键码, 第 3 字节非 0 即按键'
- 'Q3 Hill cipher: ciphertext 走 ngram quadgrams.txt 评分 → 评分函数 + Alphabet'', ''Alphabet_base, 优化 N=100 选最佳置换'
- 'Q4 智能车 CAN/CAN-FD: 抓包 → 找异常帧 → 找 flag ECU 地址'
key_payload: tshark -r usb.pcap -T fields -e usb.capdata 'usb.data_len == 8' > usb.txt
one_liner: 2022 智能网联汽车：UART 帧格式 + USB 键盘流量 + Hill 密码 ngram
lesson: 智能网联汽车安全 = UART + USB + CAN-bus + OTA；UsbKeyboardHacker 是经典工具
quality: high
full_path: 2022智能网联汽车漏洞挖掘赛_WP_by_1024SEC.full.md
meta_path: 2022智能网联汽车漏洞挖掘赛_WP_by_1024SEC.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 智能网联汽车漏洞挖掘赛 WP by 1024SEC。2022 智能网联汽车：UART 帧格式 + USB 键盘流量 + Hill 密码 ngram。关键路径：Q1 UART: 附件是 Saleae 逻辑分析仪导出, 还原 8-N-1 帧格式, 解析串口数据 → Q2 USB HID: tshark -r usb.pcap -T fields -e usb.capdata 提取 8 ...'
category: misc
subcategory: misc_other
subcategories:
- misc_other
- reverse
- oracle
tools_used:
- Python
- tshark
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/38245.html
wp_author: 1024SEC
reasoning_chain:
- Q1 UART 附件是 Saleae 导出格式 → 触发点：UART 帧格式 8-N-1
- 假设：分析 var wire + 时间戳 + 电平变化 → 动作：识别起始位(0)、8 数据位(低位先行)、停止位(1)
- 观察：还原 ASCII 串 → flag
- 'Q2 USB HID: tshark -r usb.pcap -T fields -e usb.capdata > usb.txt → 假设：键盘流量分析'
- 动作：调用 WangYihang UsbKeyboardHacker.py → 观察：8 字节中第 3 字节非 0 即按键 → 还原输入
- 'Q3 Hill cipher: ciphertext 是变种字母表 (32 字符) → 假设：ngram quadgrams 评分还原置换'
- 动作：ProcessTriGram + SolveVirginia + OptativeStore 启发式爆破 → 观察：还原明文
failed_attempts:
- 试图用现成 UART 解析工具 → 失败：附件是 Saleae 文本格式非二进制
- 试图用 Wireshark GUI 看 USB → 失败：键码到字符需要脚本映射
- 试图用穷举置换暴力 Hill → 失败：32! 太大不可行
key_observations:
- UART 帧格式识别是嵌入式 misc 基础（起始位/数据位/校验位/停止位）
- USB 键盘流量第 3 字节非 0 即按键 + 修饰键位 (bit 1/2)
- Hill cipher + 变种字母表用 ngram quadgrams 评分爆破
- UsbKeyboardHacker.py 是 USB 键盘分析标配工具
prerequisites:
- UART 串口协议基础（8-N-1 帧格式）
- tshark 命令行使用（-T fields -e usb.capdata）
- Hill cipher + ngram 评分爆破
- Saleae Logic Analyzer 导出格式
---
# 2022智能网联汽车漏洞挖掘赛 WP by 1024SEC

> 原文: https://www.ctfiot.com/38245.html
> ID: 38245

日前，1024安全实验室参加了2022智能网联汽车漏洞挖掘赛线上赛，在大家的共同努力下肝了两天一夜取得了不错的成绩，团队内部进行题目复盘时将里面有几道比较有意思的跟大家分享一下。

1 签到题2

    看本题的解题思路之前，我们先看一下UART协议帧格式。

 

1.1 UART协议

    UART（Universal Asynchronous Receiver Transmitter ）即通用异步收发器，是一种通用的串行、异步通信总线，该总线有两条数据线，可以实现全双工的发送和接收。在嵌入式系统中常用于主机与辅助设备之间的通信，帧格式如下：

      

    其中各位的含义如下：

起始位：发送1位逻辑0（低电平），开始传输数据。

数据位：可以是5~8位的数据，先发低位，再发高位，一般常见的就是8位（1个字节），其他的如7位的ASCII码。

校验位：奇偶校验，可有可无。

停止位：停止位是数据传输结束的标志，可以是1/1.5/2位的逻辑1（高电平）。

空闲位：空闲时数据线为高电平状态，代表无数据传输。

1.2 解题思路

    打开附件，发现内容与逻辑分析仪导出内容格式很像，部分内容如下：

$commentAcquisition with 3/8 channels at 1 GHz$end$timescale 1 ns $end$scope module ThanOSX $end$var wire 1 ! 0 $end$var wire 1 " 1 $end$var wire 1 # 2 $end$upscope $end$enddefinitions $end#0 0! 0" 0##1131723500 1!#1131749500 0!#1131758000 1!#1131766500 0!#1131775500 1!˛#1131784000 0!#1131792500 1!#1131801500 0!#1131811500 1!#1131846000 0!#1131854500 1!#1131863500 0!#1131880500 1!#1131889500 0!#1131899500 1!#1131908000 0!#1131916500 1!#1131951500 0!#1131968500 1!

bInterfaceProtocol的取值（十进制）　　　含义0　　　　　　　　　　　　　　　　　　　　  NONE1　　　　　　　　　　　　　　　　　　　　  键盘2　　　　　　　　　　　　　　　　　　　　  鼠标3-255　　　　　　　　　　　　　　　　　  保留

https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

tshark -r usb.pcap -T fields -e usb.capdata > usb.txt

344441234444123444412343412344441243333123444412334441233444123444123444412344441244433123344412344441244443124443312344441244433124433312344441244443123444412443331244433123334412344441244444124443312333441244433123333312344441243333124443312443331244433123444412344441244443124<DEL>344441244433124443312344441244433124333312444331244433123444412443331244433124333312444331244433123444412344441234444124<DEL>344441244433123333312444331233334123444412433331234444124333312344441234444124443312333441234444124333312444331233334123344412344

3444412344441234444123434123444412433331234444123344412334441234441234444123
4444124443312334441234444124444312444331234444124443312443331234444124444312
3444412443331244433123334412344441244444124443312333441244433123333312344441
2433331244433124433312444331234444123444412444431234444124443312444331234444
1244433124333312444331244433123444412443331244433124333312444331244433123444
4123444412344441234444124443312333331244433123333412344441243333123444412433
3312344441234444124443312333441234444124333312444331233334123344412344

-..../-..../-..../-.-./-..../.----/-..../--.../--.../-.../-..../-..../...--/--.../-..../....-/...--/-..../...--/..---/-..../....-/-..../..---/...--/---../-..../...../...--/---../...--/-----/-..../.----/...--/..---/...--/-..../-..../....-/-..../...--/...--/-..../...--/.----/...--/...--/-..../..---/...--/.----/...--/...--/-..../-..../-..../-..../...--/-----/...--/----./-..../.----/-..../.----/-..../-..../...--/---../-..../.----/...--/----./--.../-..

#!/usr/bin/env python
import sysimport os
DataFileName = "usb.dat"
presses = []
normalKeys = {"04": "a", "05": "b", "06": "c", "07": "d", "08": "e", "09": "f", "0a": "g", "0b": "h", "0c": "i", "0d": "j", "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o", "13": "p", "14": "q", "15": "r", "16": "s", "17": "t", "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y", "1d": "z", "1e": "1", "1f": "2", "20": "3", "21": "4", "22": "5", "23": "6", "24": "7", "25": "8", "26": "9", "27": "0", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "-", "2e": "=", "2f": "[", "30": "]", "31": "\", "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",", "37": ".", "38": "/", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>","54": "/","55": "*","56": "-","57": "+","59": "1","5a": "2","5b": "3","5c": "4","5d": "5","5e": "6","5f": "7","60": "8","61": "9","62": "0","63": ".",}
shiftKeys = {"04": "A", "05": "B", "06": "C", "07": "D", "08": "E", "09": "F", "0a": "G", "0b": "H", "0c": "I", "0d": "J", "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O", "13": "P", "14": "Q", "15": "R", "16": "S", "17": "T", "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y", "1d": "Z", "1e": "!", "1f": "@", "20": "#", "21": "$", "22": "%", "23": "^", "24": "&", "25": "*", "26": "(", "27": ")", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "_", "2e": "+", "2f": "{", "30": "}", "31": "|", "32": "<NON>", "33": """, "34": ":", "35": "<GA>", "36": "<", "37": ">", "38": "?", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}

def main(): # check argv if len(sys.argv) != 2: print("Usage : ") print(" python UsbKeyboardHacker.py data.pcap") print("Tips : ") print(" To use this python script , you must install the tshark first.") print(" You can use `sudo apt-get install tshark` to install it") print("Author : ") print(" WangYihang <wangyihanger@gmail.com>") print(" If you have any questions , please contact me by email.") print(" Thank you for using.") exit(1)
 # get argv pcapFilePath = sys.argv[1]
 # get data of pcap os.system("tshark -r %s -T fields -e usb.capdata 'usb.data_len == 8' > %s" % (pcapFilePath, DataFileName))
 # read data with open(DataFileName, "r") as f: for line in f: presses.append(line[0:-1]) # handle result = "" for press in presses: if press == '': continue if ':' in press: Bytes = press.split(":") else: Bytes = [press[i:i + 2] for i in range(0, len(press), 2)] if Bytes[0] == "00": if Bytes[2] != "00" and normalKeys.get(Bytes[2]): result += normalKeys[Bytes[2]] elif int(Bytes[0], 16) & 0b10 or int(Bytes[0], 16) & 0b100000: # shift key is pressed. if Bytes[2] != "00" and normalKeys.get(Bytes[2]): result += shiftKeys[Bytes[2]] else: print("[-] Unknow Key : %s" % (Bytes[0])) print("[+] Found : %s" % (result))
 # clean the temp data os.system("rm ./%s" % (DataFileName))

if __name__ == "__main__": main()

import re

ciphertext = '{snm6 vs3s tz6d"io v2 1m6yg}} v8m4j6 te15nz{v 3ilfj 1m6yg}} v8m4j vmw t 0gy3fwp nq1pm!wq8 }kwx lhtqg!6 jv3u 2vzy7t"'# ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
print('loading....')qgram = ngram_score('quadgrams.txt')tgram = ngram_score('trigrams.txt')
N = 100
Alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789,.!{}"'Alphabet_base = 'abcdefghijklmnopqrstuvwxyz'
class OptativeStore(object): def __init__(self, store_length=1000): self.store = [] self.store_length = store_length
 def append(self, item): self.store.append(item) self.store.sort(reverse=True) self.store = self.store[:
self.store_length]
 def __getitem__(self, K): return self.store[K]
 def __len__(self): return len(self.store)

def ProcessTriGram(KLEN):
 oTable = OptativeStore(N) for i in permutations(Alphabet_base, 3): partkey = ''.join(i) fullkey = partkey + 'A' * (KLEN - 3) #plaintext = Vigenere(fullkey).decipher(ciphertext) plaintext = decode(fullkey,Alphabet,ciphertext) score = 0 for j in range(0, len(plaintext), KLEN): score += tgram.score(plaintext[j:j + 3]) oTable.append((score, partkey, plaintext[:30])) return oTable

def SolveVirginia(KLEN):
 assert(KLEN > 2) best = ProcessTriGram(KLEN) nextbest = OptativeStore(N) for i in range(0, KLEN - 3): # print(i) for j in range(N): for k in Alphabet_base: partkey = best[j][1] + k # print(KLEN,len(partkey)) fullkey = partkey + ('A' * (KLEN - len(partkey))) # print(fullkey) #plaintext = Vigenere(fullkey).decipher(ciphertext) plaintext = decode(fullkey,Alphabet,ciphertext) score = 0 for l in range(0, len(ciphertext), KLEN): score += qgram.score(plaintext[l:l + KLEN]) nextbest.append((score, partkey, plaintext[:30])) best = nextbest nextbest = OptativeStore(N) return best

def main(): for i in range(3, 20): bestkey = SolveVirginia(i)[0][1] #plaintext = Vigenere(bestkey).decipher(ciphertext) plaintext = decode(bestkey,Alphabet,ciphertext) bestscore = qgram.score(plaintext) print("Vigenere key length is %2d : %4d %20s %s" % (i, bestscore, bestkey, plaintext))

if __name__ == '__main__': main()

https://github.com/mikeryan/crackle/blob/master/FAQ.md

git clone https://github.com/mikeryan/crackle.gitcd cracklemakemake install

sudo apt-get install libpcap-dev

crackle -i uploads_2022_04_11_h5kAcZEg_ble.pcapng -o de.pcapng

strings flag | grep --color=auto flag

import osimport sysimport timei=64file_name = ""un_name = ""command = ""command0 = ""def unzip(): global i while i > 60: file_name = str(i) + "-0.zip" command = "unzip " + file_name ret0 = os.popen(command).read() print(ret0) time.sleep(0.05) j = 0 while j < 7: un_name = str(i) + "-" + str(j) + ".zip" command0 = "rm " + un_name os.popen(command0) print(command0)            j = j+1 i = i-1
if __name__ == '__main__':    unzip()

def encode(s): encoding = "" i = 0 while i < len(s): count = 1 while i + 1 < len(s) and s[i] == s[i + 1]: count = count + 1 i = i + 1 encoding += str(count) + s[i] i = i + 1 return encoding if __name__ == '__main__': s = '666666666666666666666666' print(encode(s))

1024安全团队

1024安全团队是网络安全爱好者组建的团队，希望通过此平台更好的进行前沿的技术交流与分享，现研究方向包含但不限于车联网安全、物联网安全、硬件安全、无线电安全等，我们正在招募新的成员，期待更多志同道合的朋友加入我们，一起进行技术交流学习。


```
$commentAcquisition with 3/8 channels at 1 GHz$end$timescale 1 ns $end$scope module ThanOSX $end$var wire 1 ! 0 $end$var wire 1 " 1 $end$var wire 1 # 2 $end$upscope $end$enddefinitions $end#0 0! 0" 0##1131723500 1!#1131749500 0!#1131758000 1!#1131766500 0!#1131775500 1!˛#1131784000 0!#1131792500 1!#1131801500 0!#1131811500 1!#1131846000 0!#1131854500 1!#1131863500 0!#1131880500 1!#1131889500 0!#1131899500 1!#1131908000 0!#1131916500 1!#1131951500 0!#1131968500 1!
bInterfaceProtocol的取值（十进制）　　　含义0　　　　　　　　　　　　　　　　　　　　  NONE1　　　　　　　　　　　　　　　　　　　　  键盘2　　　　　　　　　　　　　　　　　　　　  鼠标3-255　　　　　　　　　　　　　　　　　  保留
https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
tshark -r usb.pcap -T fields -e usb.capdata > usb.txt
344441234444123444412343412344441243333123444412334441233444123444123444412344441244433123344412344441244443124443312344441244433124433312344441244443123444412443331244433123334412344441244444124443312333441244433123333312344441243333124443312443331244433123444412344441244443124<DEL>344441244433124443312344441244433124333312444331244433123444412443331244433124333312444331244433123444412344441234444124<DEL>344441244433123333312444331233334123444412433331234444124333312344441234444124443312333441234444124333312444331233334123344412344
3444412344441234444123434123444412433331234444123344412334441234441234444123
4444124443312334441234444124444312444331234444124443312443331234444124444312
3444412443331244433123334412344441244444124443312333441244433123333312344441
2433331244433124433312444331234444123444412444431234444124443312444331234444
1244433124333312444331244433123444412443331244433124333312444331244433123444
4123444412344441234444124443312333331244433123333412344441243333123444412433
3312344441234444124443312333441234444124333312444331233334123344412344
-..../-..../-..../-.-./-..../.----/-..../--.../--.../-.../-..../-..../...--/--.../-..../....-/...--/-..../...--/..---/-..../....-/-..../..---/...--/---../-..../...../...--/---../...--/-----/-..../.----/...--/..---/...--/-..../-..../....-/-..../...--/...--/-..../...--/.----/...--/...--/-..../..---/...--/.----/...--/...--/-..../-..../-..../-..../...--/-----/...--/----./-..../.----/-..../.----/-..../-..../...--/---../-..../.----/...--/----./--.../-..
#!/usr/bin/env python
import sysimport os
DataFileName = "usb.dat"
presses = []
normalKeys = {"04": "a", "05": "b", "06": "c", "07": "d", "08": "e", "09": "f", "0a": "g", "0b": "h", "0c": "i", "0d": "j", "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o", "13": "p", "14": "q", "15": "r", "16": "s", "17": "t", "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y", "1d": "z", "1e": "1", "1f": "2", "20": "3", "21": "4", "22": "5", "23": "6", "24": "7", "25": "8", "26": "9", "27": "0", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "-", "2e": "=", "2f": "[", "30": "]", "31": "\", "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",", "37": ".", "38": "/", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>","54": "/","55": "*","56": "-","57": "+","59": "1","5a": "2","5b": "3","5c": "4","5d": "5","5e": "6","5f": "7","60": "8","61": "9","62": "0","63": ".",}
shiftKeys = {"04": "A", "05": "B", "06": "C", "07": "D", "08": "E", "09": "F", "0a": "G", "0b": "H", "0c": "I", "0d": "J", "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O", "13": "P", "14": "Q", "15": "R", "16": "S", "17": "T", "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y", "1d": "Z", "1e": "!", "1f": "@", "20": "#", "21": "$", "22": "%", "23": "^", "24": "&", "25": "*", "26": "(", "27": ")", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "_", "2e": "+", "2f": "{", "30": "}", "31": "|", "32": "<NON>", "33": """, "34": ":", "35": "<GA>", "36": "<", "37": ">", "38": "?", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}

def main(): # check argv if len(sys.argv) != 2: print("Usage : ") print(" python UsbKeyboardHacker.py data.pcap") print("Tips : ") print(" To use this python script , you must install the tshark first.") print(" You can use `sudo apt-get install tshark` to install it") print("Author : ") print(" WangYihang <wangyihanger@gmail.com>") print(" If you have any questions , please contact me by email.") print(" Thank you for using.") exit(1)
 # get argv pcapFilePath = sys.argv[1]
 # get data of pcap os.system("tshark -r %s -T fields -e usb.capdata 'usb.data_len == 8' > %s" % (pcapFilePath, DataFileName))
 # read data with open(DataFileName, "r") as f: for line in f: presses.append(line[0:-1]) # handle result = "" for press in presses: if press == '': continue if ':' in press: Bytes = press.split(":") else: Bytes = [press[i:i + 2] for i in range(0, len(press), 2)] if Bytes[0] == "00": if Bytes[2] != "00" and normalKeys.get(Bytes[2]): result += normalKeys[Bytes[2]] elif int(Bytes[0], 16) & 0b10 or int(Bytes[0], 16) & 0b100000: # shift key is pressed. if Bytes[2] != "00" and normalKeys.get(Bytes[2]): result += shiftKeys[Bytes[2]] else: print("[-] Unknow Key : %s" % (Bytes[0])) print("[+] Found : %s" % (result))
 # clean the temp data os.system("rm ./%s" % (DataFileName))

if __name__ == "__main__": main()
import re

ciphertext = '{snm6 vs3s tz6d"io v2 1m6yg}} v8m4j6 te15nz{v 3ilfj 1m6yg}} v8m4j vmw t 0gy3fwp nq1pm!wq8 }kwx lhtqg!6 jv3u 2vzy7t"'# ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
print('loading....')qgram = ngram_score('quadgrams.txt')tgram = ngram_score('trigrams.txt')
N = 100
Alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789,.!{}"'Alphabet_base = 'abcdefghijklmnopqrstuvwxyz'
class OptativeStore(object): def __init__(self, store_length=1000): self.store = [] self.store_length = store_length
 def append(self, item): self.store.append(item) self.store.sort(reverse=True) self.store = self.store[:
self.store_length]
 def __getitem__(self, K): return self.store[K]
 def __len__(self): return len(self.store)

def ProcessTriGram(KLEN):
 oTable = OptativeStore(N) for i in permutations(Alphabet_base, 3): partkey = ''.join(i) fullkey = partkey + 'A' * (KLEN - 3) #plaintext = Vigenere(fullkey).decipher(ciphertext) plaintext = decode(fullkey,Alphabet,ciphertext) score = 0 for j in range(0, len(plaintext), KLEN): score += tgram.score(plaintext[j:j + 3]) oTable.append((score, partkey, plaintext[:30])) return oTable

def SolveVirginia(KLEN):
 assert(KLEN > 2) best = ProcessTriGram(KLEN) nextbest = OptativeStore(N) for i in range(0, KLEN - 3): # print(i) for j in range(N): for k in Alphabet_base: partkey = best[j][1] + k # print(KLEN,len(partkey)) fullkey = partkey + ('A' * (KLEN - len(partkey))) # print(fullkey) #plaintext = Vigenere(fullkey).decipher(ciphertext) plaintext = decode(fullkey,Alphabet,ciphertext) score = 0 for l in range(0, len(ciphertext), KLEN): score += qgram.score(plaintext[l:l + KLEN]) nextbest.append((score, partkey, plaintext[:30])) best = nextbest nextbest = OptativeStore(N) return best

def main(): for i in range(3, 20): bestkey = SolveVirginia(i)[0][1] #plaintext = Vigenere(bestkey).decipher(ciphertext) plaintext = decode(bestkey,Alphabet,ciphertext) bestscore = qgram.score(plaintext) print("Vigenere key length is %2d : %4d %20s %s" % (i, bestscore, bestkey, plaintext))

if __name__ == '__main__': main()
https://github.com/mikeryan/crackle/blob/master/FAQ.md
git clone https://github.com/mikeryan/crackle.gitcd cracklemakemake install
sudo apt-get install libpcap-dev
crackle -i uploads_2022_04_11_h5kAcZEg_ble.pcapng -o de.pcapng
strings flag | grep --color=auto flag
import osimport sysimport timei=64file_name = ""un_name = ""command = ""command0 = ""def unzip(): global i while i > 60: file_name = str(i) + "-0.zip" command = "unzip " + file_name ret0 = os.popen(command).read() print(ret0) time.sleep(0.05) j = 0 while j < 7: un_name = str(i) + "-" + str(j) + ".zip" command0 = "rm " + un_name os.popen(command0) print(command0)            j = j+1 i = i-1
if __name__ == '__main__':    unzip()
def encode(s): encoding = "" i = 0 while i < len(s): count = 1 while i + 1 < len(s) and s[i] == s[i + 1]: count = count + 1 i = i + 1 encoding += str(count) + s[i] i = i + 1 return encoding if __name__ == '__main__': s = '666666666666666666666666' print(encode(s))
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]