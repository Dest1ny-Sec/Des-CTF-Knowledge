---
title: 一次银狐样本分析
contest: 安全研究
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags:
- 银狐木马
- PEB-InMemoryOrderModuleList
- DLL-base-遍历
- API-Hash-还原
- ShellCode-Loader
- C2地址
- t1-t2-t3
attack_chain: '1. PEB->InMemoryOrderModuleList 遍历双向链表 找 BaseDllName /2. 比较 DLL 名找基址 /3. API Hash 算法还原 (ROR13 常见) /4. 解析 DLL 导出表 哈希 API 名匹配 /5. 动态调试：自实现 Loader 加载 ShellCode /6. 提取 C2: 156.234.119.138:443 / syumineyt.top:80 / syumingeyt.top:8080'
key_payload: PEB InMemoryOrderModuleList  syumineyt.top  syumingeyt.top  API Hash 还原
one_liner: 银狐木马样本分析，PEB 遍历模块 + API Hash 还原 + ShellCode Loader 动态调试 + C2 提取。
lesson: 银狐木马典型用 PEB 隐藏 API 调用；API Hash = 常见 ROR13 算法；动态调试需自实现 Loader；C2 通信地址 t1/t2/t3 区分协议。
quality: medium
full_path: 一次银狐样本分析.full.md
meta_path: 一次银狐样本分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 一次银狐样本分析。银狐木马样本分析，PEB 遍历模块 + API Hash 还原 + ShellCode Loader 动态调试 + C2 提取。。经验：银狐木马典型用 PEB 隐藏 API 调用；API Hash = 常见 ROR13 算法；动态调试需自实现 Loader...
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/307551.html
reasoning_chain:
- '银狐样本 → 触发点: PEB->InMemoryOrderModuleList 遍历模块'
- '假设: 通过比较 BaseDllName 找 kernel32.dll 基址 → 动作: 反汇编看 PEB 链表遍历'
- 'API Hash 算法还原 → 假设: ROR13 是常见 API hash → 动作: 用 IDA Python 写 decrypt(addr)'
- '观察: 解出 kernel32.dll / CreateFileA / ReadFile / VirtualAlloc / VirtualProtect 等'
- '假设: 动态调试直接看 API 名更简单 → 动作: 自实现 Loader 加载 ShellCode 调试'
- '提取 C2: 156.234.119.138:443 (t1=TLS) / syumineyt.top:80 (t2=HTTP) / syumingeyt.top:8080 (t3)'
- ShellCode 用 schtasks /run /tn "WindowsEvent_Task" 持久化
failed_attempts:
- '试图静态还原所有 hash → 失败: 字符串太多, 动态调试更快'
- '试图查 import 表拿 API → 失败: 银狐用 PEB 隐藏, import 表为空'
key_observations:
- PEB->InMemoryOrderModuleList 是木马隐藏 API 调用的经典手法, 不走 import 表
- ROR13 是 Windows API hash 常见算法, 先验证再批量解
- 自实现 Loader 加载 ShellCode = 动态调试独立代码的标准技巧
- C2 多协议 (t1=tls/t2=http/t3=其他) 区分用同一份配置, IOC 提取要全
prerequisites:
- PEB 结构 (InMemoryOrderModuleList 双向链表)
- ROR13 hash 算法与 API 名匹配
- IDA Python / idc 脚本编写
- ShellCode Loader 调试基础 (VirtualAlloc/VirtualProtect/CreateProcess)
---
# 一次银狐样本分析

> 原文: https://www.ctfiot.com/307551.html
> ID: 307551

作者论坛账号：soma20

这里通过PEB来获取InMemoryOrderModuleList，再通过遍历这个双向链表，然后比较BaseDllName来找到指定的dll，从而获取指定dll的基址。

：156.234.119.138:
443（t1:
1可能指启用 TLS/SSL 加密）。

：syumineyt.top:80（t2:
1可能指使用 HTTP 明文）。

：syumingeyt.top:
8080（t3:
1可能指使用 HTTP 或其他协议）。

首先就是一种比较复杂的方法，可以将hash算法还原一下，然后对一些常见的dll名称进行hash计算，来校验。对于函数名称的话，可以对目标dll文件进行导出表解析，然后对API名称进行hash计算，找出目标hash对应的API名称

另外一种比较简单的方法就是直接动态调试了，通过动态调试来直接获取到目标API的名称。ShellCode的动态调试可以自己实现一个Loader来加载这段ShellCode

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码隐藏代码defdecrypt(addr): len= ida_bytes.get_byte(addr) plain = [] foriinrange(0,len,1): cipher = ida_bytes.get_byte(addr + i +1) plain.append(chr(cipher ^0x6A)) print(f"str[{len}] ->{''.join(plain)}")print("============================")decrypt(0x4009E0)decrypt(0x4009ED+1)decrypt(0x4009FB)decrypt(0x400A08)decrypt(0x400A15)decrypt(0x400A23)decrypt(0x400A30)decrypt(0x400A3A)decrypt(0x400A5E)print("============================")
复制代码隐藏代码===========================str[12] -> kernel32.dllstr[11] -> CreateFileAstr[11] -> CloseHandlestr[11] -> GetFileSizestr[12] -> VirtualAllocstr[11] -> VirtualFreestr[8] -> ReadFilestr[14] -> VirtualProtectstr[14] -> CreateProcessA============================
复制代码隐藏代码importidcimportidaapiimportida_fproimportos
# shellcodestart_addr =0x400AA0plain = []foriinrange(0x98B): ch = ida_bytes.get_byte(start_addr+i) dec = (((ch +0x77) &0xff) ^0x62) &0xff plain.append(dec)#print(cipher)idb_dir = idc.get_idb_path()dir_path = os.path.dirname(idb_dir)print(dir_path)output_path = os.path.join(dir_path,"shellCode.bin")defsave_file(data, filename): data_bytes =bytes(data) withopen(filename,"wb")asf: f.write(data_bytes) returnlen(data_bytes)filelen = save_file(plain, output_path)print(f"数据已保存到 :{output_path}")print(f"写入{filelen}字节")
复制代码隐藏代码schtasks /run /tn"WindowsEvent_Task"
复制代码隐藏代码sub_10001270();
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