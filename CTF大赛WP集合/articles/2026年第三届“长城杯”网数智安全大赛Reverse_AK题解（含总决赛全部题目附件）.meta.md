---
title: 2026 年第三届"长城杯"网数智安全大赛 Reverse AK 题解（DokiLogic Renpy 游戏逆向）
contest: 2026 第三届长城杯网数智
year: 2026
difficulty: medium
vuln_type: [reverse, crypto_unknown, web_unknown]
tags: [长城杯 2026 第三届 网数智, Reverse AK 三题, DokiLogic Renpy 游戏引擎, rpyc pickle 序列化, 文件监控拷贝 .1.exe, UPX 脱壳, XOR 0x23=35 加密, renpy script.py load_file 打印 .rpyc]
attack_chain:
  - Renpy 游戏 → game 目录 .rpyc 文件 → 修改 renpy/script.py Script.load_file 打印加载的 .rpyc
  - 还原游戏逻辑：user_input = renpy.input().strip() → l11111l1ll1l(user_input) == ll111l11l111
  - 创建 ./1.exe 子程序 → 执行 → 拿密文 → 删除 .1.exe
  - Python 脚本文件监控：os.path.exists(".1.exe") → shutil.copy2 → 123.exe
  - upx.exe -d 123.exe 脱壳
  - 动态调试拿 Buffer 密文
  - 加密: chr(ord(c) ^ 35) → 直接异或 35 还原
key_payload: "chr(ord(ll1l111ll11l) ^ llll1l111ll1=35)"
one_liner: 2026 长城杯网数智 Reverse AK：DokiLogic Renpy 游戏逆向 - .rpyc 打印 + 文件监控拷贝 .1.exe + UPX 脱壳 + XOR 35。
lesson: Renpy 引擎逆向 = 修改 renpy/script.py load_file 把 .rpyc 反编译输出到日志；游戏运行时临时创建又删除的子程序要文件监控拷贝（inotify/while 轮询）才能拿到；UPX 脱壳后 XOR 35 是经典小加密。
quality: high
---

# 2026 年第三届"长城杯"网数智安全大赛 Reverse AK 题解

> 公众号【Real返璞归真】，回复【长城杯2026】获取所有附件

## Reverse 三题：1 签到 + 1 错题 + 1 非预期

## DokiLogic（Renpy 游戏逆向）

### 题目
游戏运行后让用户输入 flag。

### 解题步骤

**1. 定位 .rpyc 加载逻辑**

游戏用 Renpy 引擎，game 目录下有大量 .rpyc 文件。  
修改 `renpy/script.py` 的 `Script.load_file` 函数，把加载的 .rpyc 打印到日志：

```python
class Script:
    def load_file(self, filename):
        # 原始加载逻辑
        with open(filename, 'rb') as f:
            data = f.read()
        # 添加：打印到日志
        print(f"[load_file] {filename}: {data}")
        return data
```

**2. 运行游戏查看日志**

得到 pickle 序列化的 Python 代码（带乱码），删除乱码后看到逻辑：

```python
user_input = renpy.input("just input your answer: ", length=60)
user_input = user_input.strip()
encry_input = l11111l1ll1l(user_input)
encry_input == ll111l11l111
```

**3. 拿密文和加密函数**

```python
open('.1.exe', 'wb') as llll11ll1l11:
    llll11ll1l11.write(_f)
    l11l1ll111l1 = subprocess.run('./.1.exe', stdout=subprocess.PIPE).stdout
os.remove(".1.exe")
l11l1ll111l1 = subprocess.run('./.1.exe', stdout=subprocess.PIPE).stdout
ll111l11l111 = l11l1ll111l1.decode('latin-1')

def l11111l1ll1l(ll1llll1l11l):
    llll1l111ll1 = 35
    return ''.join((chr(ord(ll1l111ll11l) ^ llll1l111ll1) for ll1l111ll11l in ll1llll1l11l))
```

**4. 文件监控拷贝 .1.exe**

```python
import os, shutil, time
while True:
    if os.path.exists(".1.exe"):
        shutil.copy2(".1.exe", "123.exe")
        break
    time.sleep(0.5)
```

**5. UPX 脱壳 + 动态调试**

```bash
upx.exe -d 123.exe
# 动态调试拿 Buffer 数组中的密文
```

**6. 解密：XOR 35**

```python
def dec(param):
    key = 35
    return ''.join(chr(ord(c) ^ key) for c in param)

# 用 Buffer 密文 → dec() → flag
```

## 关键 takeaway
- **Renpy 逆向**：修改引擎源码 `script.py` 打印 .rpyc
- **临时文件**：os.path.exists + shutil.copy2 文件监控
- **UPX 脱壳**：upx.exe -d
- **XOR 35** 还原
