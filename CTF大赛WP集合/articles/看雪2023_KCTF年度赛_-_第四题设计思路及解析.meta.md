---
title: 看雪2023 KCTF年度赛 | 第四题设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: expert
vuln_type: pwn_unknown
tags: [LLVM PASS PWN, VecPass.so自定义模块, runOnFunction虚函数, C++ STL Vector, erase double free, glibc 2.35堆利用, 函数名KCTF过滤]
attack_chain: opt -load ./VecPass.so -winmt ./exp.ll -enable-new-pm=0→runOnFunction只处理函数名大写为KCTF的函数→create(堆块大小)→delete→add/sub/and/or/xor/swap/end操作→vector.erase()触发double free→glibc 2.35堆利用
key_payload: "LLVM 14.0.0;VecPass.so;opt -winmt exp.ll -enable-new-pm=0;runOnFunction;函数名KCTF过滤;vector.erase;ChunkInfo(size, buf);create/delete/add/sub/and/or/xor/swap/end;15次操作限制"
one_liner: KCTF2023年度赛Q4《AI控制空间站》LLVM PASS PWN：VecPass.so+vector.erase() double free+glibc 2.35
lesson: C++ STL vector::erase单元素删除源码是漏洞关键（destroy+copy+--finish）；LLVM PASS自定义模块逆向
quality: high
---

# 看雪2023 KCTF年度赛 | 第四题设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q4《AI控制空间站》

**难度**：4天，**全程无一人攻破**

**题目设计**：
- **LLVM PASS PWN**（首次出现）
- 自定义VecPass.so模块
- C++ STL本身漏洞 → double free
- glibc 2.35堆利用
- 内核环境找共同劫持链

**环境**：
- Ubuntu LLVM 14.0.0
- glibc 2.35-0ubuntu3.1
- VecPass.so没去符号表

**启动命令**：
```bash
opt -load ./VecPass.so -winmt ./exp.ll -enable-new-pm=0 -f
```

**逆向分析**：

**runOnFunction虚函数**：
- 关闭标准报错
- num和nm两变量清零
- **只处理函数名大写为KCTF的函数**（这是关键过滤）
- sign=0，调用run()函数
- run()返回值=1时跳出while循环

**run函数内部**：
- index初始-1，del_times=0，total_times=0
- 实例化15个ChunkInfo对象 push_back到vector
- 仅当Call操作符（编号56）跳出循环
- 解析Call调用的函数及参数

**ChunkInfo结构**：
```cpp
class ChunkInfo {
public:
    long size;    // 堆块大小
    char* buf;    // 指向堆块区域
    
    ChunkInfo() { size=0; buf=nullptr; }  // 初始化清零
    ~ChunkInfo() { if(buf) free(buf); }   // 析构释放堆块
};
```

**支持的操作**：
- `create(size, mode)`：申请堆块，size ∈ [0x10, 0x100)
  - mode=0：不操作
  - mode=1：将堆块前8字节给全局变量num
  - mode=2：num的值赋给堆块前8字节
- `remake(idx, x, y)`：重置idx对象（每个KCTF函数只调一次）
- `delete(idx)`：删除vector[idx]对象
- `add(v)` / `sub(v)`：num加减v
- `and(v)` / `or(v)` / `xor(v)`：位运算（取num后4字节）
- `swap()`：交换num和nm（全局只能调一次）
- `end()`：返回1，结束当前KCTF函数处理

**关键漏洞**：vector::erase 单元素删除：
```cpp
iterator erase(iterator position) {
    if (position + 1 != end())
        copy(position + 1, finish, position);  // 拷贝
    --finish;                                 // 移动尾指针
    destroy(finish);                          // 析构
    return position;
}
```
- 析构函数`~ChunkInfo()`会free(buf)
- 如果buf已被释放过 → **double free**

**创建/删除次数限制**：total_times ≤ 15

**glibc 2.35堆利用**：
- 在不同内核环境中找共同劫持链
- 稳定的远程shell

**技术要点**：
- LLVM PASS自定义模块逆向
- C++ STL vector::erase源码审计
- glibc 2.35 tcache/fastbin利用
- 函数名KCTF过滤

**质量评估**：高（LLVM PASS PWN前沿方向 + STL漏洞原理 + 完整操作定义）
