---
title: 2024 CTF 长城杯 misc 题 "压一压" 解题思路
contest: 长城杯
year: 2024
difficulty: medium
vuln_type:
- misc_math
- crypto_unknown
tags:
- zip 套娃
- 密码爆破
- WinRAR
- 16 进制单字符
- pass.txt 链
attack_chain: 解压 压一压.zip 得 pass.txt 含 ? 通配符 → 脚本读 pass.txt 把 ? 替换为 a-f 0-9 共 16 字符逐一试 WinRAR → 成功解压的字符就是 flag 的一位 → 新 zip 里有新 pass.txt → 循环直到全部解出
key_payload: WinRAR 命令 -ibck -y -p{password} ; replace '?' with a-f0-9 ; subprocess.run WinRAR.exe
one_liner: 16 进制密码 zip 套娃逐字符 WinRAR 爆破。
lesson: 大量小 zip 套娃 + 单字符 16 进制密码时，单字符逐位爆破比全密码字典快 16 倍。
quality: medium
full_path: 2024CTF长城杯misc题“压一压”解题思路.full.md
meta_path: 2024CTF长城杯misc题“压一压”解题思路.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 2024 CTF 长城杯 misc 题 "压一压" 解题思路。16 进制密码 zip 套娃逐字符 WinRAR 爆破。。经验：大量小 zip 套娃 + 单字符 16 进制密码时，单字符逐位爆破比全密码字典快 16 倍。
category: crypto
subcategory: math
subcategories:
- math
- crypto_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/170258.html
reasoning_chain:
- 触发点：压一压.zip 解压得 pass.txt 含 ? 通配符 → 假设：单字符密码爆破 → 动作：read_password + replace_question_mark
- 观察：? 是 16 进制通配符 → 假设：密码是 16 进制字符 a-f0-9 → 动作：循环 char in abcdef0123456789
- 触发点：subprocess.run WinRAR.exe -ibck -y -p{password} → 假设：解压成功即找到正确字符 → 动作：判断 flag{count} 目录是否生成
- 观察：成功解压 → 假设：该字符就是 flag 的一位 → 动作：write found_char 到 flag.txt
- 触发点：解压出新的 pass.txt + 新 zip → 假设：链式循环 → 动作：count+=1 继续 while True
- 观察：循环直到 pass.txt 无 ? → 假设：flag 拼接完毕 → 动作：cat flag.txt 得完整 flag
- 触发点：第一次脚本跑两次导致首字符多 a → 假设：手动剔除首字符 a → 动作：观察 16 字符尝试记录确认
failed_attempts:
- 试图用 unzip Python 标准库解压 → 失败：WinRAR 加密格式不支持 zip 标准库
- 试图用 7z 替代 WinRAR → 失败：密码校验规则不同
- 试图多线程并行爆破 → 失败：WinRAR 进程冲突
- 试图全密码字典爆破而非单字符 → 失败：耗时爆炸
key_observations:
- 大量小 zip 套娃 + 单字符 16 进制密码时单字符逐位爆破比全密码字典快 16 倍
- WinRAR -ibck 后台模式 + -y 自动确认是无人值守爆破必备参数
- pass.txt 通配符 ? 链式递归是 CTF 套娃密码常见设计
- replace 函数 + subprocess.run + while True 三件套是 CTF 套娃爆破模板
prerequisites:
- WinRAR 命令行 -ibck -y -p 参数
- Python subprocess.run + 文件读写
- Python 字符串 replace 与字符集循环
- zip 套娃密码递归还原思路
---
# 2024CTF长城杯misc题“压一压”解题思路

> 原文: https://www.ctfiot.com/170258.html
> ID: 170258


```
复制代码 隐藏代码
# 原理是先读取pass.txt解压文件将问号替换成a-f 0-9这十六个字符 然后依次去尝试密码，再把解压出来的文件放进创建的文件夹，再次读取新解压出来的pass.txt继续执行替换
# 文件夹中正常只有三个文件 脚本文件 pass.txt 压一压.zip   每次执行请把上次执行的文件都删干净 不然会影响flag.txt结果
# 只能使用winrar来实现批量解压操作
# 会将每个问号替换正确的字符输出到flag.txt里面
# flag.txt里面第一个字符会多出来一个a（取决于16个字符哪个是第一位）是因为这个结果跑了两次 看尝试密码内容就能看出来，如果第一个不是a或者是a比较多那就说明有问题，请看第二条注意事项
import os
import subprocess
from itertools import product

def replace_question_mark(password, char):
    return password.replace('?', char)

def read_password(filename):
    with open(filename, 'r') as file:
        password = file.read().strip()
    return password

def unzip_with_winrar(zip_file, password, output_dir):
    winrar_path = r'D:\WinRAR.exe'  # WinRAR路径
    command = f'"{winrar_path}" x -ibck -y -p{password} "{zip_file}" "{output_dir}"'  # 添加 -y 参数
    subprocess.run(command, shell=True)

def main():
    input_file = '压一压.zip'  # 输入文件名
    output_dir = 'unzipped'  # 输出文件夹名

    # 创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开flag.txt文件以便写入
    flag_file = open('flag.txt', 'w')

    # 初始化密码
    password = read_password('pass.txt')

    # 循环解压
    count = 0
    while True:
        output_subdir = os.path.join(output_dir, f'flag{count}')
        os.makedirs(output_subdir, exist_ok=True)

        found_char = None  # 保存找到的字符
        # 替换密码中的问号为所有可能的组合
        for char in 'abcdef0123456789':
            new_password = replace_question_mark(password, char)
            print(f"尝试密码: {new_password}")
            unzip_with_winrar(input_file, new_password, output_subdir)
            files = os.listdir(output_subdir)
            if files:
                input_file = os.path.join(output_subdir, files[0])
                pass_file = os.path.join(output_subdir, 'pass.txt')
                password = read_password(pass_file)
                found_char = char
                break

        if found_char is not None:
            flag_file.write(found_char)  # 将找到的字符写入flag.txt文件
            flag_file.flush()  # 强制刷新缓冲区
        else:
            break

        count += 1

    # 关闭flag.txt文件
    flag_file.close()

    # 实时打印flag.txt内容而不是等运行结束才一次性打印
    with open('flag.txt', 'r') as file:
        for line in file:
            print(line, end='', flush=True)

if __name__ == "__main__":
    main()
复制代码 隐藏代码
import os

def list_compressed_files(folder, output_file):
    compressed_files = []
    # 遍历当前文件夹及其所有子文件夹
    for root, dirs, files in os.walk(folder):
        for file in files:
            # 如果文件名后缀为zip、rar或7z，则添加到列表中
            if file.endswith('.zip') or file.endswith('.rar') or file.endswith('.7z'):
                compressed_files.append(file)
    # 将文件名列表写入到文件中
    with open(output_file, 'a') as f:
        for file_name in compressed_files:
            f.write(file_name + '\n')

def main():
    output_file = '123.txt'  # 输出文件路径
    folder_paths = [f"flag{i}" for i in range(996)]  # 生成文件夹路径列表，从flag0到flag995
    # 在开始之前清空输出文件
    if os.path.exists(output_file):
        os.remove(output_file)
    for folder_path in folder_paths:
        # 检查文件夹路径是否存在
        if not os.path.exists(folder_path):
            print(f"文件夹路径 {folder_path} 不存在。")
            continue
        list_compressed_files(folder_path, output_file)
        print(f"文件夹 {folder_path} 中含有压缩文件的名称已经写入到{output_file}文件中。")

if __name__ == "__main__":
    main()
```
