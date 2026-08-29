---
title: Naughty List Challenge – X-MAS CTF (C++ unordered_map rehashing)
contest: X-MAS CTF
year: 2022
difficulty: hard
vuln_type: reverse
tags: [C++ unordered_map, rehashing 改变位置, ELF_MAX_NAUGHTY_COUNT 16, PinkiePie flag 验证]
attack_chain: |
  1. 题目: X-MAS CTF Naughty List — C++ 菜单程序管理 naughty_list
  2. 漏洞: 只能查前 16 元素 (ELF_MAX_NAUGHTY_COUNT = 16)
  3. ask_pinkiepie(): 查 "PinkiePie" 是否在前 16 元素, 不在则打印 flag
  4. unordered_map 的特性: insert/erase 触发 rehash, 元素位置会变
  5. 攻击: insert 11 个 Naughty 元素触发 rehash → PinkiePie 移出前 16
  6. 观察 print_map 输出: {11} {10} {9} ... {1} 顺序 (无序但不变)
key_payload: |
  // 关键代码:
  #define ELF_MAX_NAUGHTY_COUNT 16
  
  for (int i = 0; i < ELF_MAX_NAUGHTY_COUNT; i++) {
      if (it->first == "PinkiePie") {
          pinkiepie_naughty = true;
      }
  }
  
  // 攻击: insert 11 个名字触发 rehash
  // 原始: PinkiePie 在 bucket 0 (前 16 元素)
  // insert 后: rehash, PinkiePie 移出 bucket 0 → bucket 16+
  
  // print_map 输出:
  // {11: Naughty}
  // {10: Naughty}
  // {9: Naughty}
  // {8: Naughty}
  // {7: Naughty}
  // {6: Naughty}
  // {4: Naughty}
  // {5: Naughty}
  // {3: Naughty}
  // {1: Naughty}
  // {2: Naughty}
  // → PinkiePie 不在前 16 → ask_pinkiepie() 拿 flag
one_liner: X-MAS CTF Naughty List: C++ unordered_map insert 11 个 Naughty 触发 rehash, 让 PinkiePie 移出前 16 元素触发 flag 输出。
lesson: |
  - C++ unordered_map 不保证元素顺序 (unordered!)
  - insert/erase 触发 rehash, 元素 bucket 位置会变
  - 前 16 元素验证 (ELF_MAX_NAUGHTY_COUNT=16) 是 attack surface
  - insert 11 个名字 → rehash → PinkiePie 移出前 16 → 触发 flag
  - print_map 输出 {11} {10} {9}...{1} 顺序说明确实是 unordered
  - C++ std::unordered_map 的 rehashing 不失效引用, 但迭代器会失效
quality: high
---

# Naughty List Challenge – X-MAS CTF

> 来源: ctfiot.com 87572

## 题目

```cpp
// naughty_list.cpp
// Ask PinkiePie: if "PinkiePie" in naughty_list → refuse
//                else open flag.txt and print

// Query: name in naughty_list?
// Add: name → naughty_list[count]
//       but if count == ELF_MAX_NAUGHTY_COUNT, prevent adding

#define ELF_MAX_NAUGHTY_COUNT 16

for (int i = 0; i < ELF_MAX_NAUGHTY_COUNT; i++) {
    if (it->first == "PinkiePie") {
        pinkiepie_naughty = true;
    }
}
```

## C++ unordered_map 关键特性

> An unordered map is an associative container that contains key-value pairs with unique keys. Internally, the elements are not sorted in any particular order but are organized into buckets. Which bucket an element is placed into depends entirely on the hash of its key.
> – en.cppreference.com

**重点**:
- Unordered 关键字 → 不保证顺序
- rehashing 让元素重新分配到不同 buckets
- 不失效引用, 但迭代器会失效

## 观察

输入 10 个 Naughty 元素后 print_map：

```
{11: Naughty}
{10: Naughty}
{9: Naughty}
{8: Naughty}
{7: Naughty}
{6: Naughty}
{4: Naughty}
{5: Naughty}
{3: Naughty}
{1: Naughty}
{2: Naughty}
```

**"random" 顺序** 表明 rehashing 改变了 bucket 位置。

## 攻击

```python
# 插入 11 个 Naughty 名字 (任意) 触发 rehash
for i in range(11):
    add_to_naughty_list(f"name_{i}")
# PinkiePie 从 bucket 0 移到 bucket 16+
# ask_pinkiepie() 查前 16 元素找不到 PinkiePie → 输出 flag
```

## 评价

X-MAS CTF Naughty List 高质量 Reverse 题：
- **C++ std::unordered_map** 的 `unordered` 关键字暗示位置不固定
- **`ELF_MAX_NAUGHTY_COUNT = 16`** 是 attack surface
- **insert 11 个元素触发 rehash** 让 PinkiePie 移出前 16
- **print_map** 观察实际 bucket 顺序

适用读者：C++ 容器源码 / 数据结构 / 高级逆向
