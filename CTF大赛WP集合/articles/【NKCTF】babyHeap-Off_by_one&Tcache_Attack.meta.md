---
title: 【NKCTF】babyHeap - Off by one & Tcache Attack
contest: NKCTF
year: 2023
difficulty: medium
vuln_type: heap_exploit
tags: [glibc, off-by-one, tcache-poisoning, note-array, show, UAF, safe-linking, strtol]
attack_chain: 程序 16 个 nkctf notes 槽位 + add(size <=256) + delete + edit + show /off-by-one 编辑溢出 size+1 字节覆盖下一 chunk size 字段 /tcache 0x90 size 喷射 + delete 触发 tcache /edit 改 fd 指向 __free_hook
key_payload: glibc 2.31 tcache poisoning + off-by-one 0x90 bin
one_liner: NKCTF babyHeap 经典 off-by-one 堆题，覆盖 size+1 字节改 size 字段触发 tcache 攻击。
lesson: off-by-one 是 PWN 入门最常见堆漏洞；tcache 0x90 大小喷射配合 size 字段篡改可实现任意地址写。
quality: high
---

# 【NKCTF】babyHeap - Off by one & Tcache Attack

## 程序分析

### main 函数
```c
int main() {
    int choice; char buf[4]; unsigned long v6;
    v6 = __readfsqword(0x28u);  // canary
    init();
    while (1) {
        while (1) {
            menu();
            read(0, buf, 4uLL);
            choice = strtol(buf, 0LL, 10);
            if (choice <= 5 && choice > 0) break;
            puts("Index error.");
        }
        if (choice == 5) break;
        switch (choice) {
            case 1: add(); break;
            case 2: delete(); break;
            case 3: edit(); break;
            default: show(); break;
        }
    }
}
```

### add 函数
```c
unsigned long add() {
    int index; int size; char buf[4]; unsigned long v4;
    v4 = __readfsqword(0x28u);
    printf("Enter the index: ");
    read(0, buf, 4uLL);
    index = strtol(buf, 0LL, 10);
    if ((unsigned int)index > 0xF) {
        puts("Up to 16 nkctf notes can be created.");
    } else if (note_array[index]) {
        puts("Sorry, this nkctf note has already been used.");
    } else {
        printf("Enter the Size: ");
        read(0, buf, 4uLL);
        size = strtol(buf, 0LL, 10);
        if (size <= 256) {
            note_size[index] = size;
            note_array[index] = malloc(note_size[index]);
            if (!note_array[index] || !note_size[index])
                my_error("malloc()", -1);
        } else {
            puts("This nkctf note is too big.");
        }
    }
    return v4 ^ __readfsqword(0x28u);
}
```

## 漏洞
- **off-by-one**: edit 写入时 size+1 字节溢出，可覆盖下一 chunk 的 size 字段最低字节
- 16 个槽位 + 0xF 索引检查
- size <= 256
- strtol 用户可控

## 攻击链
1. 申请多个 0x100 大小块
2. 利用 off-by-one 覆盖下一 chunk size 字段（最低字节改 0x91 之类）
3. 释放触发 tcache 0x90 bin
4. 多次释放形成链
5. edit 改 tcache fd 指向 __free_hook
6. malloc 取 chunk 到 __free_hook
7. 写 system + /bin/sh 字符串
8. 触发 free → system("/bin/sh")

## 经验提炼
- off-by-one 是 PWN 入门最常见堆漏洞
- edit 写入时多读 1 字节可覆盖 chunk size 字段
- tcache 0x90 喷射配合 size 字段篡改可实现任意地址写
- note_array 数组有 16 个槽位（0xF 索引检查）
- size 上限 256 限制了堆块大小
- strtol 处理用户输入有溢出可能
- 释放后置 note_array[index] = NULL 才能避免 UAF
