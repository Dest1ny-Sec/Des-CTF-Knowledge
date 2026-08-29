---
title: 一道CTF题目 animals 变异 MD5 加密分析
contest: 看雪
year: 2024
difficulty: hard
vuln_type: reverse
tags: [变异MD5-init-constant, OLLVM-control-flow, anti-patch-NOP, scanf-animal-shop, strncat-v25, dword_6080F4-limit, dword_608138-counter, F-xor-and-hack, F-xor-patch]
attack_chain: 1. OLLVM 控制流平坦化 + NOP patch 0x08750a74/0x13751574 3-7 字节/2. 6 个动物选项 (cat/dog/fox/panda/dragon/monkey) + dword_6080F4 < 10 + dword_608138 counter/3. strncat 到 v25 256 字节 + Win! 触发 md5(input) = flag/4. 变异 MD5: state[0]=0xEFCDAB89 改成 0x67452301 调换 init constant/5. F 函数 = (x & y) | (~x & z) 改为 (x & y) | (y & ~z) 即 F 改 G
key_payload: patch 0x08750a74/0x13751574 为 NOP  变异 MD5 state 0xEFCDAB89  F 改 G
one_liner: animals CTF 逆向题，OLLVM 控制流平坦化 + NOP patch + 变异 MD5 加密 + 动物商店菜单选项。
lesson: OLLVM 控制流平坦化用 patch 0x08750a74 (mov/jz 反汇编码) 改 NOP 还原；MD5 变异 = 改 init state + F/G 函数替换；6 个动物选项 dword_6080F4 < 10 限制次数。
quality: high
---

# 一道CTF题目 animals 变异 MD5 加密分析

## 概览
OLLVM 控制流平坦化 + 变异 MD5 加密的 CTF 逆向题。

## patch OLLVM 控制流平坦化
```python
start_add = 0x400800
end_add = 0x406e22
for i in range(start_add, end_add):
    if get_wide_dword(i) == 0x08750a74:
        patch_dword(i, 0x90909090)
        patch_dword(i+4, 0x90909090)
        patch_dword(i+8, 0x90909090)
    elif get_wide_dword(i) == 0x13751574:
        patch_dword(i, 0x90909090)
        patch_dword(i+4, 0x90909090)
        patch_dword(i+8, 0x90909090)
        patch_dword(i+12, 0x90909090)
        patch_dword(i+16, 0x90909090)
        patch_word(i+20, 0x9090)
        patch_byte(i+22, 0x90)
```

## main 函数分析
```c
int main() {
    int v34 = 0;
    sub_405FF0(a1, a2, a3);
    
    s = "0. cat"+3;       // "cat"
    v27 = "1. dog"+3;     // "dog"
    v28 = "2. fox"+3;     // "fox"
    v29 = "3. panda"+3;   // "panda"
    v30 = "4. dragon"+3;  // "dragon"
    v31 = "5. monkey"+3;  // "monkey"
    
    memset(v25, 0, sizeof(v25));
    v24 = 0;
    while (v24 < 9) {
        if (!((dword_6080F4 < 10) ^ ((((dword_608138 - 1) * dword_608138) & 1) == 0) | (dword_6080F4 < 10 && (((dword_608138 - 1) * dword_608138) & 1) == 0))
            goto LABEL_26;
        while(1) {
            v23 = 0;
            puts("Welcome Animal shop");
            sub_400900();
            printf("Please input my favorite animal: ");
            scanf("%d", &v23);
            if ((dword_6080F4 < 10 && ...) | (dword_6080F4 < 10) ^ (...)) break;
        LABEL_26:
            v23 = 0;
            puts("Welcome Animal shop");
            sub_400900();
            printf("Please input my favorite animal: ");
            scanf("%d", &v23);
        }
        switch (v23) {
            case 0: src = s; v3 = strlen(s); strncat(v25, src, v3); ...
        }
    }
    puts("Win! , flag is flag{md5(input)}");
}
```

## 变异 MD5 实现
```c
#define MD5_H
typedef struct {
    unsigned int count[2];
    unsigned int state[4];
    unsigned char buffer[64];
} MD5_CTX;

#define F(x, y, z) ((x & y) | (~x & z))  // 正常
#define G(x, y, z) ((x & z) | (y & ~z))

// 变异: F 改成 G
#define F(x, y, z) ((x & y) | (y & ~z))

void MD5Init(MD5_CTX *context) {
    context->count[0] = 0;
    context->count[1] = 0;
    context->state[0] = 0xEFCDAB89;  // 变异: 0x67452301
    context->state[1] = 0x67452301;
    context->state[2] = 0x10325476;
    context->state[3] = 0x98BADCFE;
}
```

## 经验提炼
- OLLVM 控制流平坦化用 patch 0x08750a74 (mov/jz 反汇编码) 改 NOP 还原
- MD5 变异 = 改 init state + F/G 函数替换
- 6 个动物选项 dword_6080F4 < 10 限制次数
- 0x08750a74 = `jz $+0xa; jmp` 反汇编码
- 0x13751574 = 更大的控制流平坦化模式
- 0x90909090 是 NOP NOP NOP NOP
- dword_6080F4 是输入次数计数器
- dword_608138 是嵌套层数
- F 改 G：`(x & y) | (~x & z)` 变 `(x & y) | (y & ~z)` 不可逆
- Win! 后 flag{md5(input)} 是最终 flag
