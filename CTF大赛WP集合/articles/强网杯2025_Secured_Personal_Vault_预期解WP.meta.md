---
title: 强网杯2025 Secured Personal Vault 预期解WP - WinDbg内存转储+进程间AES
contest: 强网杯2025
year: 2025
difficulty: hard
vuln_type: reverse
tags: [WinDbg, JS脚本, host.memory.readMemoryValues, 进程间通信, mailslot, BSOD蓝屏, AES_key_iv提取, CommuStruct结构体, sign+function+pid+processCreateTime, moshuiD]
attack_chain: 写WinDbg JS脚本safeDumpMemory(按4KB分页读+失败写0) → 触发BSOD蓝屏抓内存 → 进程A(Bsod)和进程B(PersonalVault.exe)的Mailslot通信数据 → 提取进程A的AES key={0x20,0x51...}和iv={0xAF,0x40...} + 进程B的key={0x45,0x71...}和iv={0xC9,0x62...} → 用对应AES解密flag → CommuStruct{char sign[4];int function;__int64 pid;__int64 *processCreateTime;}结构体反序列化
key_payload: WinDbg JS safeDumpMemory + 进程AES key+iv提取 + CommuStruct序列化
one_liner: 强网杯2025 Secured Personal Vault:WinDbg JS转储BSOD内存+提取两进程AES key+iv解密flag。
lesson: WinDbg JS脚本:host.memory.readMemoryValues分页读取+失败用nullView填充;进程间Mailslot通信数据可从内核对象转储中提取;CommuStruct结构体{char sign[4];int function;__int64 pid;__int64 *processCreateTime};BSOD后用LiveKd或转储分析可恢复内存;AES key/iv在PersonalVault.exe进程空间明文存储。
quality: high
---
