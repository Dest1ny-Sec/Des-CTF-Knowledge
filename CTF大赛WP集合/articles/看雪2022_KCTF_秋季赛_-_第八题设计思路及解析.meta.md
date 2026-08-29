---
title: 看雪2022 KCTF 秋季赛 | 第八题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [Shellcode七段加密, 进程注入反调试, 单字节操作, 字典+异或+移位+分段置换, Decompress API, 挂起进程注入]
attack_chain: Windows CrackMe 32位+CreateProcessW(CREATE_SUSPENDED)挂起注入→Decompress API提取7段shellcode→每段4字节长度+shellcode→字典+异或+移位+分段置换七段对称加密→最后一段含最终验证
key_payload: "BOOL FUNC(kernel32, LoadLibraryA, GetProcAddress, input);4字节长度+SHELLCODE*7;单字节操作;Decompress API提取;GetDlgItem/GetWindowText/CreateProcessW/VirtualAllocEx/WriteProcessMemory/ResumeThread"
one_liner: KCTF2022秋Q8《商贸往来》CrackMe：七段shellcode注入+单字节操作加密+进程注入反调试
lesson: Windows CrackMe经典进程注入模板：CreateProcessW(CREATE_SUSPENDED)→VirtualAllocEx→WriteProcessMemory→ResumeThread
quality: high
---

# 看雪2022 KCTF 秋季赛 | 第八题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q8《商贸往来》

**难度**：5队攻破

**题目设计**：
- Windows 32位 CrackMe
- 7段加密验证shellcode（嵌入混淆无效代码）
- vc编译后抠出shellcode
- 进程注入反调试

**三个核心设计**：

**1. 代码混淆设计**：
- 插入无效代码混淆
- 关闭VC编译器优化选项 → C语言级代码膨胀
- 解题者需模式识别剔除无效代码

**2. 反调试设计**：
- 判断硬件断点
- 判断软件断点 INT3
- 判断调试窗口
- BeingDebugged 是否为1

**3. Key加密和验证**：
- 字典
- 异或
- 移位
- 分段置换
- **7段shellcode**：前6段对称加密 + 第7段最终验证

**七段文件格式**：
```
4字节长度 + SHELLCODE + 4字节长度 + SHELLCODE + ... + 4字节长度 + SHELLCODE
```

**Key长度**：128位

**进程注入流程**（标准Windows注入）：
```c
struct custom {
    int kernel32_hModule;
    HMODULE (__stdcall *LoadLibraryA)(LPCSTR lpLibFileName);
    FARPROC (__stdcall *GetProcAddress)(HMODULE hModule, LPCSTR lpProcName);
};

// 1. GetDlgItemText 获取input
GetWindowTextA(hDlg, input, 255);
lstrlenA(input);  // 获取长度

// 2. CreateProcessW挂起
CreateProcessW(crackme_exe_path, 0, 0, 0, 0, CREATE_SUSPENDED, 0, 0, &si, &pi);

// 3. VirtualAllocEx 分配空间
VirtualAllocEx(pi.hProcess, 0, 128, 4096, 4);

// 4. WriteProcessMemory 写入input
WriteProcessMemory(pi.hProcess, lpBase + i, &input[i], 128-i, &nBytes);

// 5. WriteProcessMemory 写入shellcode到入口点
// 覆盖入口点：v27 = 104; v28 = 0; v29 = -72; v30 = 0; v31 = -1; v32 = -48;

// 6. ResumeThread 恢复执行
ResumeThread(pi.hThread);

// 7. WaitForSingleObject 等待完成
WaitForSingleObject(pi.hProcess, 30000);
GetExitCodeProcess(pi.hProcess, &exitCode);
```

**关键函数签名**：
```c
BOOL FUNC(HMODULE kernel32, PFN_LoadLibraryA, PFN_GetProcAddress, UCHAR* input);
```

**Shellcode提取点**：
- Decompress API运行后可找到
- 模式识别有效代码特征
- 字典+密钥+单字节操作

**核心算法**：
- 单字节处理加密
- 乱序字典转义 + 变异异或 + 移位 + 分段置换
- 7段顺序执行，前6段加密，第7段最终验证

**质量评估**：高（注入流程 + 7段shellcode格式 + 单字节操作）
