---
title: SWPUCTF 2021 新生赛 - 老鼠走迷宫
contest: SWPUCTF
year: 2021
difficulty: easy
vuln_type: reverse
tags:
- pyinstxtractor
- pyc-decompile
- maze-dfs
- md5-of-path
attack_chain:
- 文件 MZ 头识别为 EXE
- pyinstxtractor.py 反编译为 5.pyc (无后缀) + struct.pyc
- 用 struct.pyc 前 16 字节补齐 5.pyc 头
- tool.lu/pyc 反编译得 .py 文件
- 删除 return None 死代码
- '加 for row in maze: print(row) 打印 25x25 maze'
- DFS 走迷宫 (0 可走, 1 墙) 从 (0,1) 到 (24,23)
- wasd 表示最短路径 sssssddssddssaaaassssddwwddddssssssaawwaassssddssaassddddwwddssddwwwwwwwwaawwddwwwwaaaawwddwwwwddssssddwwwwddddwwddddssaassaassddddssddssaassssssddsssssss
- 最后追加 s (因为终点外还要走一格)
- flag = md5("sssssddssddssaa...") = 69193150b15c87d39252d974bc323217
key_payload: md5("sssssddssddssaa...ddsssssss")
one_liner: SWPUCTF 2021 新生赛 RE 题：pyinstxtractor 拆 EXE → pyc 补头 → 反编译 → DFS 迷宫 → md5 路径。
lesson: PyInstaller 打包 EXE 提取 pyc 只需补 16 字节头，常见反编译入口点。
quality: medium
full_path: SWPUCTF_2021_新生赛-老鼠走迷宫.full.md
meta_path: SWPUCTF_2021_新生赛-老鼠走迷宫.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: SWPUCTF 2021 新生赛 - 老鼠走迷宫。SWPUCTF 2021 新生赛 RE 题：pyinstxtractor 拆 EXE → pyc 补头 → 反编译 → DFS 迷宫 → md5 路径。。关键路径：文件 MZ 头识别为 EXE → pyinstxtractor.py 反编译为 5.pyc (无后缀) + struct.pyc → 用 struct.pyc 前 16 字节补齐 ...
category: reverse
subcategory: reverse
tools_used:
- Python
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/146558.html
reasoning_chain:
- 拿到 .exe 文件 → file 识别 MZ 头 → 触发点：PyInstaller 打包 EXE
- 动作：python pyinstxtractor.py exe → 观察：输出 5/struct 无后缀文件
- 5.pyc 缺前 16 字节 → 假设：从 struct.pyc 复制头 → 动作：dd if=struct.pyc of=5.pyc bs=16 count=1 conv=notrunc
- tool.lu/pyc 反编译 → 观察：25x25 maze + wasd 输入
- 假设：flag = md5(最短路径) → 动作：加 print 循环打 maze + DFS 找最短
- DFS (0,1)→(24,23) → 观察：最短路径字符串 sssssdd...ddssssssss
- 动作：hashlib.md5(path) → flag = 69193150b15c87d39252d974bc323217
failed_attempts:
- 试图直接运行 exe → 失败：无法在 Linux 跑 msvcrt.getch
- 试图反编译未补头 pyc → 失败：头部 magic number 缺失报错
key_observations:
- PyInstaller 打包 EXE 提取 pyc 只需补 16 字节头 (struct.pyc 完整)
- DFS/BFS 是迷宫最短路径通用算法 (1=墙 0=可走)
- pyc 文件前 4 字节 magic + 12 字节时间戳/源文件大小是 Python 版本标识
- md5(最短路径) 是迷宫类 CTF 通用出题模式
prerequisites:
- Python .pyc 文件结构 (magic number + header)
- pyinstxtractor 工具使用
- DFS/BFS 迷宫算法
- 在线 pyc 反编译网站 (tool.lu/pyc)
---
# SWPUCTF 2021 新生赛-老鼠走迷宫

> 原文: https://www.ctfiot.com/146558.html
> ID: 146558

附件下载

https://wwvc.lanzouj.com/iYLez1br84jg

◆用pyinstxtrator解析exe。

◆重点：将无后缀的5先修改后缀为pyc，然后随便找一个pyc文件补齐5.pyc的前16位十六进制数值（这道题以struct.pyc为例）。

◆将.pyc反编译为.py。

◆找到maze，从而找到最短路径。

下载附件，拿到一个无后缀的文件，丢入winhex里看看，发现是MZ开头的，去搜MZ开头是什么文件。

MZ开头的是.EXE可执行文件。

修改后缀：

64位，无壳，但是该exe是被pyinstaller打包后得到的，我们需要将exe转换为py形式。

pyinstxtractor.py自行下载，在这个页面打开cmd。

使用pyinstxtractor.py反编译exe文件，命令如下：

python pyinstxtractor.py 可执行文件exe的地址

在当前文件夹会多出一个文件夹。

可以看到可疑的文件5，struct。

这里我们需要先将文件5和struct加上后缀.pyc，因为后续需要进行.pyc反编译成.py文件（其实struct可要可不要，struct的作用就是给5.pyc补齐前面缺失的十六进制数值，将其他的正常的.pyc文件替换struct.pyc也可以，因为我发现.pyc文件的前16位数值都是一样的）。

在winhex打开两个pyc文件，将struct的前16位十六进制数复制到5.pyc开头。

记得保存。

将5.pyc文件反编译成.py文件，网址：https://tool.lu/pyc/

down下来，得到一个python文件。

#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.7

import random
import msvcrt
(row, col) = (12, 12)
(i, j) = (0, 0)
maze = [
 [
 1,
 0,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1],
 （……省略，参考源文章）

print('Mice walk in a maze: wasd to move,q to quit')
print("flag is the shortest path's md5,example:if the shortest path is wasdsdw,the flag is md5('wasdsdw')")
(i, j) = (0, 1)
n = 0
while i == row * 2 and j == col * 2 - 1:
 print('ohhhh!!!!you did it')
 break
 print('your position:({},{})'.format(i, j))
 inp = msvcrt.getch()
 n += 1
 ti = i
 tj = j
 if b'a' == inp and i > 0:
 tj -= 1
 elif b'w' == inp and j > 0:
 ti -= 1
 elif b's' == inp and j < row * 2:
 ti += 1
 elif b'd' == inp and i < col * 2:
 tj += 1
 elif b'q' == inp:
 exit('bye!!')
 else:
 print('What???')
 if maze[ti][tj] == 1:
 print(random.choice([
 'no wayy!!',
 "it's wall",
 'nop']))
 continue
 elif maze[ti][tj] == 0:
 print(random.choice([
 'nice!!',
 'yeah!!',
 'Go on']))
 i = ti
 j = tj
 return None

在maze下面添加一个for循环，输出maze，会报错，把最下面的return none直接删了，这不是重点不要紧。

修改之后的代码，可以直接输出maze。

#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.7

import random
import msvcrt
(row, col) = (12, 12)
(i, j) = (0, 0)
maze = [
 [
 1,
 0,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1],
 （……省略，参考源文章）

for row in maze:
 print(row)
print('Mice walk in a maze: wasd to move,q to quit')
print("flag is the shortest path's md5,example:if the shortest path is wasdsdw,the flag is md5('wasdsdw')")
(i, j) = (0, 1)
n = 0
while i == row * 2 and j == col * 2 - 1:
 print('ohhhh!!!!you did it')
 break
 print('your position:({},{})'.format(i, j))
 inp = msvcrt.getch()
 n += 1
 ti = i
 tj = j
 if b'a' == inp and i > 0:
 tj -= 1
 elif b'w' == inp and j > 0:
 ti -= 1
 elif b's' == inp and j < row * 2:
 ti += 1
 elif b'd' == inp and i < col * 2:
 tj += 1
 elif b'q' == inp:
 exit('bye!!')
 else:
 print('What???')
 if maze[ti][tj] == 1:
 print(random.choice([
 'no wayy!!',
 "it's wall",
 'nop']))
 continue
 elif maze[ti][tj] == 0:
 print(random.choice([
 'nice!!',
 'yeah!!',
 'Go on']))
 i = ti
 j = tj

[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
[1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1]
[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
[1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1]
[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]
[1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1]
[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
[1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
[1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1]
[1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
[1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1]
[1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
Mice walk in a maze: wasd to move,q to quit
flag is the shortest path’s md5,example:if the shortest path is wasdsdw,the flag is md5(‘wasdsdw’)

Process finished with exit code 0

接下来可以自己慢慢找，也可以写脚本，我直接从佬（https://blog.csdn.net/qq_42880719/article/details/120581571）那拉的脚本，可以直接输出迷宫的最小路径。

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 当前位置四个方向的偏移量
path = [] # 存找到的路径

def mark(maze, pos): # 给迷宫maze的位置pos标"2"表示“倒过了”
 maze[pos[0]][pos[1]] = 2

def passable(maze, pos): # 检查迷宫maze的位置pos是否可通行
 return maze[pos[0]][pos[1]] == 0

def find_path(maze, pos, end):
 mark(maze, pos)
 if pos == end:
 print(pos, end=" ") # 已到达出口，输出这个位置。成功结束
 path.append(pos)
 return True
 for i in range(4): # 否则按四个方向顺序检查
 nextp = pos[0] + dirs[i][0], pos[1] + dirs[i][1]
 # 考虑下一个可能方向
 if passable(maze, nextp): # 不可行的相邻位置不管
 if find_path(maze, nextp, end): # 如果从nextp可达出口，输出这个位置，成功结束
 print(pos, end=" ")
 path.append(pos)
 return True
 return False

def see_path(maze, path): # 使寻找到的路径可视化
 for i, p in enumerate(path):
 if i == 0:
 maze[p[0]][p[1]] = "E"
 elif i == len(path) - 1:
 maze[p[0]][p[1]] = "S"
 else:
 maze[p[0]][p[1]] = 3
 print("n")
 for r in maze:
 for c in r:
 if c == 3:
 print(' 33[0;31m' + "*" + " " + ' 33[0m', end="")
 elif c == "S" or c == "E":
 print(' 33[0;34m' + c + " " + ' 33[0m', end="")
 elif c == 2:
 print(' 33[0;32m' + "#" + " " + ' 33[0m', end="")
 elif c == 1:
 print(' 33[0;;40m' + " " * 2 + ' 33[0m', end="")
 else:
 print(" " * 2, end="")
 print()

if __name__ == '__main__':
 maze = [
 [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
 [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
 [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
 [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]]

 start = (0, 1)
 end = (24, 23)
 find_path(maze, start, end)
 see_path(maze, path)

迷宫最短路径。

使用wasd表示最短路径就是（一定不要忘了最后一个 * 还需要往下走一个才到达终点，我服，看了半天才找到这个错误）：

sssssddssddssaaaassssddwwddddssssssaawwaassssddssaassddddwwddssddwwwwwwwwaawwddwwwwaaaawwddwwwwddssssddwwwwddddwwddddssaassaassddddssddssaassssssddsssssss

根据python里面的内容，flag是用wasd表示的最短路径的md5值。

取32位小写，69193150b15c87d39252d974bc323217。

flag：NSSCTF{69193150b15c87d39252d974bc323217}

看雪ID：Zer0_0

https://bbs.kanxue.com/user-home-945402.htm

*本文为看雪论坛优秀文章，由 Zer0_0 原创，转载请注明来自看雪社区

# 往期推荐

1、IOFILE exploit入门

2、入门编译原理之前端体验

3、如何用纯猜的方式逆向喜马拉雅xm文件加密(wasm部分)

4、反恶意软件扫描接口(AMSI)如何帮助您防御恶意软件

5、sRDI — Shellcode反射式DLL注入技术

6、对APP的检测以及参数计算分析

球分享

球点赞

球在看


```
#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.7

import random
import msvcrt
(row, col) = (12, 12)
(i, j) = (0, 0)
maze = [
 [
 1,
 0,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1],
 （……省略，参考源文章）print('Mice walk in a maze: wasd to move,q to quit')
print("flag is the shortest path's md5,example:if the shortest path is wasdsdw,the flag is md5('wasdsdw')")
(i, j) = (0, 1)
n = 0
while i == row * 2 and j == col * 2 - 1:
 print('ohhhh!!!!you did it')
 break
 print('your position:({},{})'.format(i, j))
 inp = msvcrt.getch()
 n += 1
 ti = i
 tj = j
 if b'a' == inp and i > 0:
 tj -= 1
 elif b'w' == inp and j > 0:
 ti -= 1
 elif b's' == inp and j < row * 2:
 ti += 1
 elif b'd' == inp and i < col * 2:
 tj += 1
 elif b'q' == inp:
 exit('bye!!')
 else:
 print('What???')
 if maze[ti][tj] == 1:
 print(random.choice([
 'no wayy!!',
 "it's wall",
 'nop']))
 continue
 elif maze[ti][tj] == 0:
 print(random.choice([
 'nice!!',
 'yeah!!',
 'Go on']))
 i = ti
 j = tj
 return None
#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.7

import random
import msvcrt
(row, col) = (12, 12)
(i, j) = (0, 0)
maze = [
 [
 1,
 0,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1,
 1],
 （……省略，参考源文章）for row in maze:
 print(row)
print('Mice walk in a maze: wasd to move,q to quit')
print("flag is the shortest path's md5,example:if the shortest path is wasdsdw,the flag is md5('wasdsdw')")
(i, j) = (0, 1)
n = 0
while i == row * 2 and j == col * 2 - 1:
 print('ohhhh!!!!you did it')
 break
 print('your position:({},{})'.format(i, j))
 inp = msvcrt.getch()
 n += 1
 ti = i
 tj = j
 if b'a' == inp and i > 0:
 tj -= 1
 elif b'w' == inp and j > 0:
 ti -= 1
 elif b's' == inp and j < row * 2:
 ti += 1
 elif b'd' == inp and i < col * 2:
 tj += 1
 elif b'q' == inp:
 exit('bye!!')
 else:
 print('What???')
 if maze[ti][tj] == 1:
 print(random.choice([
 'no wayy!!',
 "it's wall",
 'nop']))
 continue
 elif maze[ti][tj] == 0:
 print(random.choice([
 'nice!!',
 'yeah!!',
 'Go on']))
 i = ti
 j = tj
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 当前位置四个方向的偏移量
path = [] # 存找到的路径

def mark(maze, pos): # 给迷宫maze的位置pos标"2"表示“倒过了”
 maze[pos[0]][pos[1]] = 2

def passable(maze, pos): # 检查迷宫maze的位置pos是否可通行
 return maze[pos[0]][pos[1]] == 0

def find_path(maze, pos, end):
 mark(maze, pos)
 if pos == end:
 print(pos, end=" ") # 已到达出口，输出这个位置。成功结束
 path.append(pos)
 return True
 for i in range(4): # 否则按四个方向顺序检查
 nextp = pos[0] + dirs[i][0], pos[1] + dirs[i][1]
 # 考虑下一个可能方向
 if passable(maze, nextp): # 不可行的相邻位置不管
 if find_path(maze, nextp, end): # 如果从nextp可达出口，输出这个位置，成功结束
 print(pos, end=" ")
 path.append(pos)
 return True
 return False

def see_path(maze, path): # 使寻找到的路径可视化
 for i, p in enumerate(path):
 if i == 0:
 maze[p[0]][p[1]] = "E"
 elif i == len(path) - 1:
 maze[p[0]][p[1]] = "S"
 else:
 maze[p[0]][p[1]] = 3
 print("n")
 for r in maze:
 for c in r:
 if c == 3:
 print(' 33[0;31m' + "*" + " " + ' 33[0m', end="")
 elif c == "S" or c == "E":
 print(' 33[0;34m' + c + " " + ' 33[0m', end="")
 elif c == 2:
 print(' 33[0;32m' + "#" + " " + ' 33[0m', end="")
 elif c == 1:
 print(' 33[0;;40m' + " " * 2 + ' 33[0m', end="")
 else:
 print(" " * 2, end="")
 print()

if __name__ == '__main__':
 maze = [
 [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
 [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
 [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
 [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]]

 start = (0, 1)
 end = (24, 23)
 find_path(maze, start, end)
 see_path(maze, path)
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