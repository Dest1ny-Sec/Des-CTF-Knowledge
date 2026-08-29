---
title: 2024 西湖论剑 Qrohttre（Windows 调试器实现父子进程同步 + SMC）
contest: 2024 西湖论剑
year: 2024
difficulty: hard
vuln_type: [reverse, misc_unknown]
tags: [Qrohttre 父子进程同步调试, DEBUG_PROCESS CreateProcessA, 0xCC 断点同步用户输入, TF 单步异常, f_OnBreakPoint_4070A0 + f_OnSingleStep_407530, f_OnAccessViolation_406710, ZwSetInformationThread ThreadHideFromDebugger 0x11 反调试, 双段 SMC 自解密, CE dump 40B991-40DDB4 内存 patch 回 QrohttreSub.exe, WriteProcessMemory 回写垃圾]
attack_chain:
  - 主进程 CreateProcessA DEBUG_PROCESS 创建子进程
  - 子进程入口点 INT3（0xCC）断点
  - 主进程 f_OnBreakPoint_4070A0: 同步用户输入到子进程 + 设置 TF 单步标志
  - 子进程单步异常 → 主进程 f_OnSingleStep_407530 解密下一条指令 + 上条指令写垃圾
  - ZwSetInformationThread(ThreadHideFromDebugger) 反调试
  - 找到第二段 SMC 起始位置 0x40B991，patch 掉 WriteProcessMemory 回写
  - CE dump 子进程 40B991-40DDB4 解密代码
  - patch 到 QrohttreSub.exe 静态分析
  - 触发访问越权异常 (读写操作数未完全解密)，分发 f_OnAccessViolation_406710 还原地址
key_payload: "CreateProcessA(..., DEBUG_PROCESS, ...); f_OnSingleStep_407530"
one_liner: Qrohttre 主进程用 Win32 DEBUG_PROCESS 调试子进程，TF 单步 + 双段 SMC 自解密 + 0xCC 断点同步用户输入；patch WriteProcessMemory + CE dump + 父子进程双 IDA patch 是分析套路。
lesson: Win32 调试 API（DEBUG_PROCESS + TF 单步 + 0xCC 断点）实现父子进程同步通信是 Windows 高级逆向题，patch 掉 WriteProcessMemory 回写 + CE dump 是核心套路；反调试 ThreadHideFromDebugger 用 ZwSetInformationThread(0x11) 设线程。
quality: high
---

# 2024 西湖论剑 Qrohttre

## 题目结构

主进程以 `DEBUG_PROCESS` 模式创建子进程（执行相同程序），通过 Win32 调试事件实现父子进程同步通信 + 双段 SMC 自解密。

### 关键函数
- `CreateProcessA(Filename, ..., DEBUG_PROCESS, ...)` 创建子进程
- `f_OnException_406FA0` 异常调试事件分发（断点/单步/访问越权）
- `f_OnBreakPoint_4070A0` 0xCC 断点处理：同步用户输入到子进程 + 设 TF
- `f_OnSingleStep_407530` 单步处理：解密下一条指令 + 上条指令写垃圾
- `f_OnAccessViolation_406710` 访问越权：还原读写地址
- `ZwSetInformationThread(GetCurrentThread(), 0x11, 0, 0)` 反调试

## 第一段 SMC

加密段 0x40DE77~0x40E2BB。  
字符串搜输出内容有假校验，scanf 下断点返回 40DFDE → 动态/静态代码不一致 → SMC。  
**解密方法**：找到解密函数（一般是 sub_xxxx 调 XOR/ADD/ROL），跟一遍还原。

## 第二段 SMC（核心难点）

子进程每执行一条指令前，主进程就解密一次后续代码，并往子进程上一条指令填充垃圾数据。

**分析套路**：
1. patch 掉第二个写回垃圾指令的 `WriteProcessMemory`
2. 在主进程写下一条指令前下断点
3. CE dump 子进程 0x40B991~0x40DDB4 内存
4. 复制一份程序改名为 `QrohttreSub.exe`
5. IDA 把 dump 出来的解密代码 patch 到 QrohttreSub.exe
6. 识别 main 函数在 0x0040B8F0

## 反调试

```c
#define ThreadHideFromDebugger 0x11
ZwSetInformationThread(GetCurrentThread(), ThreadHideFromDebugger, 0, 0);
```

## 总结

- 双段 SMC 加密：用户输入同步 + 单步解密 + 上条指令抹除  
- patch 掉 `WriteProcessMemory` 让解密后代码常驻内存 → CE dump → 父子双 IDA 静态分析  
- 父子进程同步通信是 Windows 高级逆向题标志
