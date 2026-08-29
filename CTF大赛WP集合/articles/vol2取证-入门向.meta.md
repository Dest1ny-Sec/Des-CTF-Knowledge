---
title: vol2 取证 - 入门向
contest: vol2-share
year: 2024
difficulty: low
vuln_type: forensic_disk
tags: [volatility, vmware-vmdk, vmem, forensics-plugin-list, amcache, hashdump, mimikatz]
attack_chain:
  - 解析 .vmdk 虚拟机磁盘
  - 解析 .vmem 内存页面
  - volatility plugins: amcache/apihooks/atoms/auditpol/bigpools/bioskd
  - cachedump 提域账号密码哈希
  - cmdline 显示进程命令行
  - dlllist/hivelist/lsadump/malfind/mftparser
key_payload: volatility 2.x 插件列表
one_liner: Volatility 2 取证入门，VMware 文件格式 + 全部插件功能列表。
lesson: 内存取证 = 解析 .vmem + 跑 volatility 插件。
quality: medium
---

Volatility 2 取证入门向完整 WP（来源 ctfiot）。

**VMware 文件格式**
| 后缀 | 描述 |
|------|------|
| `.vmx` | 虚拟机配置文件 |
| `.vmdk` | 虚拟机磁盘元数据 |
| `flat.vmdk` | 二进制磁盘数据 |
| `ctk.vmdk` | 数据块变化追踪 |
| `.vmem` | 虚拟机内存页面 |
| `.vmss` | 挂起状态 |
| `.vmsd` | 快照元数据 |
| `.vmsn` | 快照状态 |
| `.vmtx` | 模板 |
| `.nvram` | BIOS |
| `.vswp` | 交换文件 |

**volatility 2 常用插件**
| 插件 | 功能 |
|------|------|
| `amcache` | AmCache 应用程序痕迹 |
| `apihooks` | 检测 API hook |
| `atoms` | 会话/窗口站 atom 表 |
| `atomscan` | Atom 池扫描 |
| `auditpol` | 审计策略 |
| `bigpools` | 大分页池 |
| `bioskbd` | 读取 BIOS 密码 |
| `cachedump` | 域账号密码哈希 |
| `callbacks` | 系统通知例程 |
| `clipboard` | 剪贴板 |
| `cmdline` | 进程命令行 |

（完整列表见原文）

**典型工作流**：
1. `volatility imageinfo` 识别 profile
2. `pstree` 进程树
3. `pslist` 进程列表
4. `hashdump` 提 NTLM 哈希
5. `lsadump` 提 LSA 密钥
6. `mimikatz` 提明文密码
7. `filescan` + `dumpfiles` 提文件
8. `cmdscan` 看命令行历史

**质量**：入门向列表整理，参考价值高。
