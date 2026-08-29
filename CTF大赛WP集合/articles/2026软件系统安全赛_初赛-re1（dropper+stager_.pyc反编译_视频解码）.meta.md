---
title: 2026 软件系统安全赛初赛 re1（dropper+stager .pyc 反编译 视频解码）
contest: 2026 软件系统安全赛
year: 2026
difficulty: hard
vuln_type: [reverse, crypto_unknown, stego_traffic]
tags: [软件系统安全赛 2026 初赛, 64 位 .elf Loader dropper, video.mp4 黑白色块, stager_pyc_base64 内嵌, .pyc 反编译 decompyle3 uncompyle6, AES 解密视频数据, 魔改算法双重保护, AI 梭解两道题, re2 re3 没解出来]
attack_chain:
  - 64 位 .elf Loader 加载 video.mp4
  - file_exists(video.mp4) 检查
  - 内嵌 stager_pyc_base64[] + base64_decode
  - 加载 .pyc 字节码执行（dropper 模式）
  - 视频帧黑白色块 → 解码出 flag
  - re1 AI 梭出，re2 手动调半天，re3 .so 加密逻辑没找到
key_payload: "stager_pyc_base64 → base64_decode → .pyc exec"
one_liner: 2026 软件系统安全赛 re1：64 位 .elf Loader dropper + 内嵌 base64 .pyc stager + 视频黑白色块解码。
lesson: Loader 加载 video.mp4 + 内嵌 stager_pyc 是 2026 新型 ELF 逆向套路；.pyc 字节码用 decompyle3/uncompyle6 反编译；视频像素作密文/明文是新颖 stego 形式。
quality: medium
---

# 2026 软件系统安全赛初赛 re1（dropper+stager .pyc 反编译 视频解码）

## 题目结构

- 64 位 .elf Loader
- video.mp4（黑白色块堆叠）
- Loader 检查 video.mp4 是否存在

## Loader 主函数

```c
int __fastcall main(int argc, const char **argv, const char **envp) {
    __int64 v3; __int64 v4; __int64 v5;
    int v6; __int64 v7;
    const char *v8;
    char v10;             // [rsp+7h] [rbp-99h] BYREF
    char *v11;            // [rsp+8h] [rbp-98h]
    char *v12;            // [rsp+10h] [rbp-90h]
    char *v13;            // [rsp+18h] [rbp-88h]
    _BYTE v14[32];        // [rsp+20h] [rbp-80h] BYREF
    _BYTE v15[32];        // [rsp+40h] [rbp-60h] BYREF
    _BYTE v16[40];        // [rsp+60h] [rbp-40h] BYREF
    unsigned __int64 v17; // [rsp+88h] [rbp-18h]

    v17 = __readfsqword(0x28u);
    v11 = &v10;
    std::string::basic_string(v14, "video.mp4", &v10);
    std::__new_allocator<char>::~__new_allocator(&v10);
    if ((unsigned __int8)file_exists(v14) != 1) {
        v3 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4BC0);
        v4 = std::operator<<<char>(v3, v14);
        std::ostream::operator<<(v4, &std::endl<char, std::char_traits<char>>);
        v5 = std::operator<<<std::char_traits<char>>(&std::cerr, &unk_4BE0);
        std::ostream::operator<<(v5, &std::endl<char, std::char_traits<char>>);
        v6 = 1;
    } else {
        v12 = &v10;
        std::string::basic_string(v16, stager_pyc_base64[0], &v10);
        base64_decode(v15, v16);
        // 加载 .pyc 字节码
    }
}
```

## 解题流程

1. **查壳**：exeinfo 确认 64 位 .elf
2. **IDA 分析**：strings 找可疑字符串 `video.mp4`
3. **stager_pyc_base64[]**：内嵌 .pyc 字节码 base64 编码
4. **base64_decode → .pyc** → 用 decompyle3 / uncompyle6 反编译
5. **视频黑白色块**：不是无意义，是 flag 密文 → 像素解码
6. **flag**：从视频帧恢复

## 比赛总结

> 好难的比赛，用 AI 梭出来两道题，3 道逆向只解出一道 re1  
> re2 另一位逆向手动调半天找到了半个 flag  
> re3 本人也没做过 .so 文件逆向，找不到加密逻辑  
> 不知道能不能晋级，感觉有点儿悬

## 关键点

- **dropper + stager**：.elf Loader 内嵌 base64 .pyc → 二次加载执行
- **video.mp4** 是密文/明文载体，不是普通视频
- **.pyc 反编译**：decompyle3 (Python 3.8+) / uncompyle6 (Python 2/3.6)
- **AI 辅助**：现代 CTF Reverse 用 AI 辅助是常态
