---
title: CTF のフォレンジックにおけるメモリフォレンジックまとめ [Volatility 3, Volatility 2]
contest: Volatility CTF
year: 2023
difficulty: medium
vuln_type: forensic_memory
tags: [日语, Volatility 3, Volatility 2, windows.info, pstree, netscan, cmdline, dumpfiles, hashdump, mutantscan, linux.bash, linux.psaux, profile, JPCERTCC符号表, File Carving, strings]
attack_chain:
  - 内存取证标准: Volatility 3 推荐 (v2 v3 是完全不同的工具)
  - OS 识别: strings -n 10 mem.bin | grep "ubuntu" 或 windows.info.Info
  - Windows 关键命令: pstree / netscan / cmdline / dumpfiles / hashdump / mutantscan
  - Linux 关键命令: linux.bash (命令历史) / linux.psaux (ps -aux)
  - 自制 profile: module.dwarf + System.map 打包 zip 放到 plugins/overlays/linux/
  - VirusTotal 验证可疑 IP
  - 进程 dump: vol -f image.raw windows.dumpfiles --pid=1676
  - 即使不用 Volatility, File Carving + strings 也能拿到有用信息
key_payload: 'Volatility 3 推荐 / windows.info / pstree / netscan / cmdline / dumpfiles / hashdump / mutantscan / linux.bash / linux.psaux / JPCERTCC 符号表 / File Carving'
one_liner: Volatility 3 vs 2 内存取证总结 (日语) — Windows 关键命令 pstree+netscan+cmdline+dumpfiles+hashdump+mutantscan + Linux bash+psaux + 自制 profile (module.dwarf+System.map) + JPCERTCC 符号表。
lesson: Volatility 3 完全替代 2;windows.info 识别 OS;pstree+netscan 是黄金组合;linux.bash+psaux 是基础;符号表可自制 (module.dwarf + System.map)。
quality: high
---

# CTF のフォレンジックにおけるメモリフォレンジックまとめ

## 速读
日语版 Volatility 3 vs 2 内存取证完整总结 — Windows + Linux 关键命令 + 符号表自制。

## 解题流程
1. 识别 OS: `vol -f image.raw windows.info.Info` 或 `strings -n 10 | grep "ubuntu"`
2. 没有符号表就自制 (module.dwarf + System.map)
3. 关键命令执行: shell 脚本批量跑

## Volatility 3

### Windows
```bash
vol -f image.raw windows.info.Info                  # OS 识别
vol -f image.raw windows.pstree.PsTree              # 进程树
vol -f image.raw windows.netscan.NetScan            # 网络连接
vol -f image.raw windows.cmdline.CmdLine            # 命令行参数
vol -f image.raw windows.dumpfiles --pid=1676       # dump 进程文件
vol -f image.raw windows.hashdump.Hashdump           # SAM/SYSTEM hash
vol -f image.raw windows.mutantscan.MutantScan      # 互斥体
vol -f image.raw windows.filescan                  # 文件扫描
```

### Linux
```bash
vol -f dump.mem banner                    # 识别 OS
vol -f dump.mem linux.bash               # 命令历史
vol -f dump.mem linux.psaux              # ps -aux 结果
```

## 自制 profile (Volatility 2)
```bash
zip _phillip.zip module.dwarf System.map
# 放到 volatility/plugins/overlays/linux/
vol2 --info | grep Profile  # 确认添加
vol -f memory.raw --profile=Win7SP1x64 [command]
```

## 符号表
- Volatility 3: JPCERTCC/Windows-Symbol-Tables
- Linux: module.dwarf + System.map

## 不用 Volatility 也能做
- File Carving 提取文件
- strings 拿信息
- 但耗时更多
