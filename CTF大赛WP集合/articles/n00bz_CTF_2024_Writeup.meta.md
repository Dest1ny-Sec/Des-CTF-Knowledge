---
title: n00bz CTF 2024 Writeup
contest: n00bzCTF
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [powershell-xor-3, brainfuck-c-translation, qbasic, vm-qbasic, write-only]
attack_chain:
  - PowerShell: cat flag.txt | ForEach { $_ -bxor 3 }
  - 输出 `m33ayxeqln\sbqjp\twk\{lq~` 加密
  - brainfuck → C 翻译 (bftoc.py by Paul Kaefer)
  - 模拟 tape[1000] 跑 BF VM
  - 输出 32 字符明文
key_payload: PowerShell XOR 3 + brainfuck C 翻译
one_liner: n00bz CTF 2024 Writeup：PowerShell XOR 加密 + brainfuck → C 翻译。
lesson: 写多语言题目（PowerShell/BF/QBasic）是 n00bz 系列特色。
quality: medium
---

n00bz CTF 2024 Writeup 入门题合集（来源 ctfiot）。

**第一题：PowerShell XOR**
```powershell
$bytes = [System.Text.Encoding]::ASCII.GetBytes((cat .\flag.txt))
[System.Collections.Generic.List[byte]]$newBytes = @()
$bytes.ForEach({ $newBytes.Add($_ -bxor 3) })
$newString = [System.Text.Encoding]::ASCII.GetString($newBytes)
echo $newString | Out-File -Encoding ascii .\output.txt
```

加密后输出 `m33ayxeqln\sbqjp\twk\{lq~`，解密：每个字节 XOR 3 还原。

**第二题：Brainfuck → C 翻译**
原 BF 代码极长，作者用 `bftoc.py` (Paul Kaefer) 翻译成 C：

```c
#include <stdio.h>
void main(void) {
    int size = 1000;
    int tape[size]; int i = 0;
    for (i=0; i<size; i++) tape[i] = 0;
    int ptr = 0;
    
    ptr += 1; tape[ptr] += 11;
    while (tape[ptr] != 0) {
        ptr -= 1; tape[ptr] += 10;
        ptr += 1; tape[ptr] -= 1;
    }
    // ... 更多 BF 翻译
}
```

编译运行得 32 字符明文 = flag。

**质量评估**：n00bz 系列适合入门，PowerShell + brainfuck 两种"非主流语言"组合。
