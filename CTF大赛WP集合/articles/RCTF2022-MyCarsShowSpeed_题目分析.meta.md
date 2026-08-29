---
title: RCTF2022 MyCarsShowSpeed 题目分析
contest: RCTF 2022
year: 2023
difficulty: high
vuln_type: heap_exploit
tags: [pwn, ncurses-game, winTimes-cnt, fake-flag-purchase, uaf, car-shop, double-free]
attack_chain:
  - 赛车主题 PWN 游戏：菜单 start/show/visit/switch
  - visit 商店: buy/sell/fix/fetch 4 项 + 5 项商品 (NormalCar/SuperCar/LongCar/GhostCar/flag)
  - 关键：winTimes<1000 时 buy('flag') 触发 cheat 检测 → 全 free curCar
  - start() 触发 winTimes++/money+=10 (每次赢得比赛)
  - fetch('') 空名修复触发 fetchTime=0 漏洞
  - fix('') 同样空名触发
  - 泄 heap 通过 switch(4) 接收 CarName 6 字节 = heap 指针
  - heap = u64(name+'\0\0\0') - 0x5e0
  - fix(name) 多次触发 memory corruption
  - buy('NormalCar', p64(heap+0x330)[:6]) 二次购买注入指针
  - buy('NormalCar', 'ssss') 触发 fake chunk 利用
  - buy('flag') 最终触发 flag 字符串读取 (绕过 cheat 检测)
key_payload: buy('NormalCar', p64(heap+0x330)[:6]) + buy('NormalCar', p64(heap+0x330)[:6]) + buy('NormalCar', 'ssss') + buy('flag')
one_liner: RCTF2022 赛车游戏 PWN：ncurses 菜单 + winTimes 计数器 + cheat 检测触发 free + 空名 fix/fetch 漏洞 + 6 字节 carName 泄 heap 指针。
lesson: 字符串结尾 \0\0\0 补齐 u64 解析是固定套路；fix/fetch 用空字符串触发漏洞是赛车游戏常见挖法；多次 buy 注入 fake heap pointer 是 car list 类题目常见利用。
quality: medium
---
