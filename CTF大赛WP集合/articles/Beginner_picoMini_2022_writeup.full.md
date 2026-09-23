---
title: Beginner picoMini 2022 writeup
contest: picoCTF
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags:
- picoCTF Beginner
- run_s4n1ty_run
- s4n1ty_c4t
- str_xor enkidu
- 4个level
- md5 hash
- 691d密码
- 4ec9密码
- print_flag
- serpentine
- fixme缩进
attack_chain:
- 'runme.py: 直接 print flag{picoCTF{run_s4n1ty_run}}'
- 'nc saturn.picoctf.net 57688: picoCTF{s4n1ty_c4t}'
- 'convertme.py: 十进制 → 二进制, XOR ''enkidu'' 解密'
- 'code.py: picoCTF{c0d3b00k_455157_8100c7c1}'
- 'fixme1.py: 缩进错误'
- 'fixme2.py: if flag = "" 应为 =='
- 'level1.py: 密码 691d → str_xor 解密'
- 'level2.py: chr(0x34)+chr(0x65)+chr(0x63)+chr(0x39) = "4ec9'
- 'md5 多轮: Joan of Arc, Clint Eastwood, grave robbers'
- 'serpentine: 选 b 调 print_flag'
- 'level3.py: 密码 1ea2'
- 'level4.py: 100 个候选密码 md5 匹配'
key_payload: '''str_xor enkidu / md5 hash / 691d 4ec9 1ea2 密码 / print_flag / 100 候选 md5 匹配'''
one_liner: picoCTF Beginner picoMini 2022 全 12 题 — runme + nc + convertme + code + fixme1/2 + 4 个 level (str_xor + md5 + print_flag) + serpentine + 100 候选 md5 匹配。
lesson: picoCTF 入门是综合小练习合集:Python 脚本分析、密码学 (XOR/md5)、代码修复 (缩进/语法)、二进制 (print_flag 函数)。
quality: medium
full_path: Beginner_picoMini_2022_writeup.full.md
meta_path: Beginner_picoMini_2022_writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Beginner picoMini 2022 writeup。picoCTF Beginner picoMini 2022 全 12 题 — runme + nc + convertme + code + fixme1/2 + 4 个 level (str_xor + md5 + print_flag) + serpentine + 100 候选 md5 匹配。。关键路径：runme.py:...
category: misc
subcategory: misc_other
tools_used:
- Python
- netcat
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: practice
wp_url: https://www.ctfiot.com/25449.html
reasoning_chain:
- '[触发点] picoCTF Beginner picoMini 2022 全 12 题 → 假设：综合小练习 / [动作] 跑 runme.py 直接 print flag / [观察] picoCTF{run_s4n1ty_run} / [下一步] nc saturn.picoctf.net 57688'
- '[触发点] nc 连接拿到 picoCTF{s4n1ty_c4t} → 假设：convertme.py 十进制转二进制 / [动作] 看 convertme.py 源码 + XOR ''enkidu'' 解密 / [观察] 拿到转换题 flag / [下一步] 看 code.py fixme1/2'
- '[触发点] fixme1.py 缩进错误 + fixme2.py = 改成 == → 假设：代码修复题 / [动作] 改缩进 + 改 = 为 == / [观察] 拿到 picoCTF{c0d3b00k_455157_8100c7c1} / [下一步] 4 个 level'
- '[触发点] level1.py 密码 691d + str_xor + md5 4 轮 (Joan of Arc, Clint Eastwood, grave robbers) → 假设：str_xor 解密 + md5 匹配 / [动作] 串到 level4.py 100 候选 md5 匹配 / [观察] 拿到所有 level flag / [下一步] serpentine 选 b 调 print_flag'
failed_attempts:
- 试图直接 cat 找 flag → 失败：flag 散落在多个文件
- 试图手工 md5 → 失败：必须用 hashlib 算
key_observations:
- picoCTF 入门是综合小练习合集：Python 脚本分析、密码学 (XOR/md5)、代码修复 (缩进/语法)、二进制 (print_flag 函数)
- str_xor 循环 key 扩展是 XOR 经典手法
- md5 多轮 + 历史人物名（Joan of Arc）是常见密码学套路
prerequisites:
- Python 基础（import / xor / md5）
- 二进制/十进制转换
- nc 网络连接
- md5 hashlib 使用
---
# Beginner picoMini 2022 writeup

> 原文: https://www.ctfiot.com/25449.html
> ID: 25449


```
#!/usr/bin/python3
################################################################################
# Python script which just prints the flag
################################################################################

flag ='picoCTF{run_s4n1ty_run}'
print(flag)
$ nc saturn.picoctf.net 57688
picoCTF{s4n1ty_c4t}
import random

def str_xor(secret, key):
 #extend key to secret length
 new_key = key
 i = 0
 while len(new_key) < len(secret):
 new_key = new_key + key[i]
 i = (i + 1) % len(key)
 return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])

flag_enc = chr(0x15) + chr(0x07) + chr(0x08) + chr(0x06) + chr(0x27) + chr(0x21) + chr(0x23) + chr(0x15) + chr(0x5f) + chr(0x05) + chr(0x08) + chr(0x2a) + chr(0x1c) + chr(0x5e) + chr(0x1e) + chr(0x1b) + chr(0x3b) + chr(0x17) + chr(0x51) + chr(0x5b) + chr(0x58) + chr(0x5c) + chr(0x3b) + chr(0x10) + chr(0x57) + chr(0x0f) + chr(0x5e) + chr(0x51) + chr(0x5c) + chr(0x46) + chr(0x53) + chr(0x13)

num = random.choice(range(10,101))

print('If ' + str(num) + ' is in decimal base, what is it in binary base?')

ans = input('Answer: ')

try:
 ans_num = int(ans, base=2)

 if ans_num == num:
 flag = str_xor(flag_enc, 'enkidu')
 print('That is correct! Here\'s your flag: ' + flag)
 else:
 print(str(ans_num) + ' and ' + str(num) + ' are not equal.')

except ValueError:
 print('That isn\'t a binary number. Binary numbers contain only 1\'s and 0\'s')
$ python convertme.py
If 26 is in decimal base, what is it in binary base?
Answer: 11010
That is correct! Here's your flag: picoCTF{4ll_y0ur_b4535_e2a58836}
$ python code.py
picoCTF{c0d3b00k_455157_8100c7c1}
$ python fixme1.py
 File "fixme1.py", line 20
 print('That is correct! Here\'s your flag: ' + flag)
 ^
IndentationError: unexpected indent
$ python fixme1.py
That is correct! Here's your flag: picoCTF{1nd3nt1ty_cr1515_09ee727a}
$ python fixme2.py
 File "fixme2.py", line 22
 if flag = "":
 ^
SyntaxError: invalid syntax
$ python fixme2.py
That is correct! Here's your flag: picoCTF{3qu4l1ty_n0t_4551gnm3nt_4863e11b}
### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ########################
def str_xor(secret, key):
 #extend key to secret length
 new_key = key
 i = 0
 while len(new_key) < len(secret):
 new_key = new_key + key[i]
 i = (i + 1) % len(key)
 return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])
###############################################################################

flag_enc = open('level1.flag.txt.enc', 'rb').read()

def level_1_pw_check():
 user_pw = input("Please enter correct password for flag: ")
 if( user_pw == "691d"):
 print("Welcome back... your flag, user:")
 decryption = str_xor(flag_enc.decode(), user_pw)
 print(decryption)
 return
 print("That password is incorrect")

level_1_pw_check()
$ python level1.py
Please enter correct password for flag:
That password is incorrect
$ python level1.py
Please enter correct password for flag: 691d
Welcome back... your flag, user:
picoCTF{545h_r1ng1ng_56891419}
$ nc saturn.picoctf.net 52026
'picoCTF{gl17ch_m3_n07_' + chr(0x62) + chr(0x65) + chr(0x63) + chr(0x66) + chr(0x33) + chr(0x38) + chr(0x36) + chr(0x31) + '}'
user_pw = input("Please enter correct password for flag: ")
 if( user_pw == chr(0x34) + chr(0x65) + chr(0x63) + chr(0x39) ):
$ python level2.py
Please enter correct password for flag: 4ec9
Welcome back... your flag, user:
picoCTF{tr45h_51ng1ng_9701e681}
$ nc saturn.picoctf.net 65352
Please md5 hash the text between quotes, excluding the quotes: 'Joan of Arc'
Answer:
19ba425a542946fcf13228d9ddd53139
19ba425a542946fcf13228d9ddd53139
Correct.
Please md5 hash the text between quotes, excluding the quotes: 'Clint Eastwood'
Answer:
b84954cb41831fa842dd69f6e1836b6e
b84954cb41831fa842dd69f6e1836b6e
Correct.
Please md5 hash the text between quotes, excluding the quotes: 'grave robbers'
Answer:
bf48d2ac4e5d0532912c8e8e0998645f
bf48d2ac4e5d0532912c8e8e0998645f
Correct.
picoCTF{4ppl1c4710n_r3c31v3d_674c1de2}
$ echo -n "Joan of Arc" | md5
19ba425a542946fcf13228d9ddd53139
$ python serpentine.py

 Y
 .-^-.
 / \ .- ~ ~ -.
() () / _ _ `. _ _ _
 \_ _/ / / \ \ . ~ _ _ ~ .
 | | / / \ \ .' .~ ~-. `.
 | | / / ) ) / / `.`.
 \ \_ _/ / / / / / `'
 \_ _ _.' / / ( (
 / / \ \
 / / \ \
 / / ) )
 ( ( / /
 `. `. .' /
 `. ~ - - - - ~ .'
 ~ . _ _ _ _ . ~

Welcome to the serpentine encourager!

a) Print encouragement
b) Print flag
c) Quit

What would you like to do? (a/b/c)
while True:
 print('a) Print encouragement')
 print('b) Print flag')
 print('c) Quit\n')
 choice = input('What would you like to do? (a/b/c) ')

 if choice == 'a':
 print_encouragement()

 elif choice == 'b':
 print('\nOops! I must have misplaced the print_flag function! Check my source code!\n\n')

 elif choice == 'c':
 sys.exit(0)

 else:
 print('\nI did not understand "' + choice + '", input only "a", "b" or "c"\n\n')
What would you like to do? (a/b/c) b
picoCTF{7h3_r04d_l355_7r4v3l3d_8e47d128}
$ python level3.py
Please enter correct password for flag: 1ea2
Welcome back... your flag, user:
picoCTF{m45h_fl1ng1ng_6f98a49f}
import hashlib

# The strings below are 100 possibilities for the correct password.
# (Only 1 is correct)
pos_pw_list = ["6b3e", "989c", "4b17", "d06f", "f495", "6ea1", "44e4", "1d45", "3e1a", "b0b4", "8c65", "3276", "c496", "9d3d", "2476", "6ef4", "6b7f", "c184", "c2a8", "9708", "7bea", "9a2d", "4a22", "93ae", "826b", "9a50", "8b39", "5410", "a86c", "3760", "6426", "ec8e", "c294", "a909", "cbc6", "2e75", "f137", "9cb3", "79e7", "469f", "a9f9", "3e37", "b33e", "3f31", "4b27", "2f06", "cc2f", "d9e4", "2de7", "7328", "b4d4", "8e74", "a677", "b139", "9c74", "8ea4", "36f6", "613b", "7a7a", "5710", "838c", "44d5", "7190", "99d9", "c0a6", "b218", "3223", "477e", "38e5", "19b4", "3267", "2287", "b947", "a8d0", "fd9c", "e99c", "d8b7", "4c82", "b289", "332b", "bba5", "716d", "653e", "eb5d", "ad77", "ad3a", "3922", "7565", "947d", "928c", "2937", "823f", "f362", "79cf", "4582", "c0d0", "ed20", "d89a", "129c", "4e81"]

### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ########################
def str_xor(secret, key):
 #extend key to secret length
 new_key = key
 i = 0
 while len(new_key) < len(secret):
 new_key = new_key + key[i]
 i = (i + 1) % len(key)
 return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])
###############################################################################

flag_enc = open('level4.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level4.hash.bin', 'rb').read()

def hash_pw(pw_str):
 pw_bytes = bytearray()
 pw_bytes.extend(pw_str.encode())
 m = hashlib.md5()
 m.update(pw_bytes)
 return m.digest()

def level_4_pw_check(pw):
 # user_pw = input("Please enter correct password for flag: ")
 # user_pw_hash = hash_pw(user_pw)

 # if( user_pw_hash == correct_pw_hash ):
 print("Welcome back... your flag, user:")
 decryption = str_xor(flag_enc.decode(), pw)
 print(decryption)
 return
 print("That password is incorrect")

def choose_pw():
 for p in pos_pw_list:
 if hash_pw(p) == correct_pw_hash:
 return p

pw = choose_pw()
level_4_pw_check(pw)
$ python level4.py
Welcome back... your flag, user:
picoCTF{fl45h_5pr1ng1ng_89490f2d}
import hashlib

### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ########################
def str_xor(secret, key):
 #extend key to secret length
 new_key = key
 i = 0
 while len(new_key) < len(secret):
 new_key = new_key + key[i]
 i = (i + 1) % len(key)
 return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])
###############################################################################

flag_enc = open('level5.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level5.hash.bin', 'rb').read()
dictionary = open('dictionary.txt', 'r').readlines()

def hash_pw(pw_str):
 pw_bytes = bytearray()
 pw_bytes.extend(pw_str.encode())
 m = hashlib.md5()
 m.update(pw_bytes)
 return m.digest()

def level_5_pw_check(pw):
 # user_pw = input("Please enter correct password for flag: ")
 # user_pw_hash = hash_pw(user_pw)

 # if( user_pw_hash == correct_pw_hash ):
 print("Welcome back... your flag, user:")
 decryption = str_xor(flag_enc.decode(), pw)
 print(decryption)
 return
 print("That password is incorrect")

def find_pw():
 for d in dictionary:
 d = d.strip()
 if hash_pw(d) == correct_pw_hash:
 return d

pw = find_pw()
level_5_pw_check(pw)
$ python level5.py
Welcome back... your flag, user:
picoCTF{h45h_sl1ng1ng_2f021ce9}
```
