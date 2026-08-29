---
title: 2024 CTF 长城杯 misc 题 "压一压" 解题思路
contest: 长城杯
year: 2024
difficulty: medium
vuln_type: [misc_math, crypto_unknown]
tags: [zip 套娃, 密码爆破, WinRAR, 16 进制单字符, pass.txt 链]
attack_chain: 解压 压一压.zip 得 pass.txt 含 ? 通配符 → 脚本读 pass.txt 把 ? 替换为 a-f 0-9 共 16 字符逐一试 WinRAR → 成功解压的字符就是 flag 的一位 → 新 zip 里有新 pass.txt → 循环直到全部解出
key_payload: WinRAR 命令 -ibck -y -p{password} ; replace '?' with a-f0-9 ; subprocess.run WinRAR.exe
one_liner: 16 进制密码 zip 套娃逐字符 WinRAR 爆破。
lesson: 大量小 zip 套娃 + 单字符 16 进制密码时，单字符逐位爆破比全密码字典快 16 倍。
quality: medium
---
# 2024 CTF 长城杯 misc 题 "压一压" 解题思路

**核心思路**

`压一压.zip` 解压后有 `pass.txt` + `压一压.zip` + 脚本文件。`pass.txt` 中有 `?` 通配符表示密码的某一位未定。

**爆破脚本**

```python
import os, subprocess

def replace_question_mark(password, char):
    return password.replace('?', char)

def read_password(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def unzip_with_winrar(zip_file, password, output_dir):
    winrar_path = r'D:\WinRAR.exe'
    command = f'"{winrar_path}" x -ibck -y -p{password} "{zip_file}" "{output_dir}"'
    subprocess.run(command, shell=True)

def main():
    input_file = '压一压.zip'
    output_dir = 'unzipped'
    flag_file = open('flag.txt', 'w')
    password = read_password('pass.txt')

    count = 0
    while True:
        output_subdir = os.path.join(output_dir, f'flag{count}')
        os.makedirs(output_subdir, exist_ok=True)

        found_char = None
        for char in 'abcdef0123456789':
            new_password = replace_question_mark(password, char)
            unzip_with_winrar(input_file, new_password, output_subdir)
            files = os.listdir(output_subdir)
            if files:
                input_file = os.path.join(output_subdir, files[0])
                pass_file = os.path.join(output_subdir, 'pass.txt')
                password = read_password(pass_file)
                found_char = char
                break

        if found_char is not None:
            flag_file.write(found_char)
            flag_file.flush()
        else:
            break
        count += 1
```

**关键点**

1. **单字符爆破**：`a-f0-9` 16 个字符逐位试，避免对完整密码字典的指数爆炸
2. **WinRAR 强依赖**：必须用 WinRAR.exe，7z/bandizip 解析不同时会报错
3. **状态传递**：每层解压后的 `pass.txt` 是下一层的密码种子
4. **第 0 位多 `a`**：脚本里"abc..."中 'a' 排第一，默认就是它，提交前要 cross-check

**多文件清单**

```python
# 第二个脚本把 flag0~flag995 文件夹下所有 zip/rar/7z 列出来
folder_paths = [f"flag{i}" for i in range(996)]
for folder_path in folder_paths:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.zip', '.rar', '.7z')):
                f.write(file + '\n')
```
