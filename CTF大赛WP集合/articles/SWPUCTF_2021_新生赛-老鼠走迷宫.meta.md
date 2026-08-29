---
title: SWPUCTF 2021 新生赛 - 老鼠走迷宫
contest: SWPUCTF
year: 2021
difficulty: easy
vuln_type: reverse
tags: [pyinstxtractor, pyc-decompile, maze-dfs, md5-of-path]
attack_chain:
- 文件 MZ 头识别为 EXE
- pyinstxtractor.py 反编译为 5.pyc (无后缀) + struct.pyc
- 用 struct.pyc 前 16 字节补齐 5.pyc 头
- tool.lu/pyc 反编译得 .py 文件
- 删除 return None 死代码
- 加 for row in maze: print(row) 打印 25x25 maze
- DFS 走迷宫 (0 可走, 1 墙) 从 (0,1) 到 (24,23)
- wasd 表示最短路径 sssssddssddssaaaassssddwwddddssssssaawwaassssddssaassddddwwddssddwwwwwwwwaawwddwwwwaaaawwddwwwwddssssddwwwwddddwwddddssaassaassddddssddssaassssssddsssssss
- 最后追加 s (因为终点外还要走一格)
- flag = md5("sssssddssddssaa...") = 69193150b15c87d39252d974bc323217
key_payload: md5("sssssddssddssaa...ddsssssss")
one_liner: SWPUCTF 2021 新生赛 RE 题：pyinstxtractor 拆 EXE → pyc 补头 → 反编译 → DFS 迷宫 → md5 路径。
lesson: PyInstaller 打包 EXE 提取 pyc 只需补 16 字节头，常见反编译入口点。
quality: medium
---
# SWPUCTF 2021 新生赛 - 老鼠走迷宫

## 1. EXE 拆解
- 文件 MZ 开头是 EXE
- `python pyinstxtractor.py 可执行文件.exe`
- 输出文件夹含可疑文件 `5`、`struct`（无后缀）

## 2. 补 pyc 头
- `5.pyc` 缺前 16 字节
- `struct.pyc` 完整，复制其前 16 字节到 `5.pyc` 开头
- 反编译网站：https://tool.lu/pyc/

## 3. 反编译结果
```python
import random
import msvcrt
(row, col) = (12, 12)
(i, j) = (0, 0)
maze = [[1, 0, 1, ...], ...]  # 25x25 maze
print('Mice walk in a maze: wasd to move,q to quit')
print("flag is the shortest path's md5,example:if the shortest path is wasdsdw,the flag is md5('wasdsdw')")
```

## 4. 打印 maze + DFS
```python
for row in maze:
    print(row)
# DFS 寻找最短路径
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
def find_path(maze, pos, end):
    mark(maze, pos)
    if pos == end:
        path.append(pos); return True
    for i in range(4):
        nextp = (pos[0]+dirs[i][0], pos[1]+dirs[i][1])
        if passable(maze, nextp) and find_path(maze, nextp, end):
            path.append(pos); return True
    return False
```

## 5. 路径
从 (0,1) 到 (24,23)：
```
sssssddssddssaaaassssddwwddddssssssaawwaassssddssaassddddwwddssddwwwwwwwwaawwddwwwwaaaawwddwwwwddssssddwwwwddddwwddddssaassaassddddssddssaassssssddsssssss
```

## 6. flag
```python
import hashlib
path = "sssssddssddssaa..."
flag = hashlib.md5(path.encode()).hexdigest()
# 69193150b15c87d39252d974bc323217
```
最终 flag: `NSSCTF{69193150b15c87d39252d974bc323217}`
