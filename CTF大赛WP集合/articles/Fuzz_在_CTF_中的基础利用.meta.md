---
title: Fuzz 在 CTF 中的基础利用
contest: 公众号文章
year: 2025
difficulty: medium
vuln_type: heap_exploit
tags: [fuzz, pwn, tree, mbr-structure, 0-1000-random, double-free, crash-detect]
attack_chain:
  - MBR A树形结构：MBR A1/MBR A2→obj1, obj2...
  - 树满TooManyElementsError重试
  - EOFError=找到漏洞
  - 0-1000轮循环
  - 每10次add，每2次delete
  - 随机a=0-8, b=0-8
  - delete记录+堆风水构造
  - 期望<20行有效命令触发double free
  - 重投机制
key_payload: TooManyElementsError → retry; EOFError → success
one_liner: Fuzz在CTF基础利用：树形结构+随机操作+EOFError检测漏洞
lesson: 堆漏洞Fuzz可降低堆风水调试难度
quality: high
---

# Fuzz 在 CTF 中的基础利用

## 题目信息
- 文章：ctfiot 转载
- 主题：Fuzzing 在 CTF 中的基础利用

## 关键攻击链
### 1. 数据结构
```
┌────────────┐
│   MBR A    │
└────┬───────┘
     ↓
┌────────────────┐
│ MBR A1 │ MBR A2│
└────┬──────┴────┘
     ↓
┌───────────────┐
│ obj1 obj2 ... │ (叶节点)
└───────────────┘
```

### 2. Fuzz 框架
```python
class TooManyElementsError(Exception):
    """如果树满了我们还没找到异常,就抛出这个"""
    pass

def fuzz():
    global f
    f = open('./log.txt', 'w')  # 记录 fuzz 过程
    for i in range(0x1000):
        if i % 10 == 0:
            a = randint(0, 8)
            b = randint(0, 8)
            add(a, b, str(i).encode())
            data0 = r.recvuntil(b'Choice Table')
            f.write('add({},{},str({}).encode())\n'.format(a, b, i))
        elif i % 2 == 0:
            a = randint(0, 8)
            b = randint(0, 8)
            delet(a, b)
            data0 = r.recvline()
            if b'not exists' in data0:
                continue
            f.write('delet({},{} )\n'.format(a, b))

while True:
    global f
    r = process('./pwn')
    try:
        fuzz()
    except TooManyElementsError:  # 未找到漏洞
        f.close()
        os.remove("./log.txt")
        r.close()
    except EOFError:  # 找到漏洞
        f.close()
        line_count = sum(1 for _ in open('log.txt', 'r', encoding='utf-8'))
        if line_count < 20:
            print(f"{line_count}hang")
            print("down")
            break
```

## 评分
- quality: high（树形结构 + 随机操作 + EOFError 检测 + 重投机制）
