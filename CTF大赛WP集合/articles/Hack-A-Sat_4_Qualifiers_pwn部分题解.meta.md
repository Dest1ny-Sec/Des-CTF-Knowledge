---
title: Hack-A-Sat 4 Qualifiers pwn部分题解
contest: Hack-A-Sat 4 Qualifiers
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags: [pwn, spacebus, magic-bussin, cfs, satellite, oob-read, hex-parser, c]
attack_chain:
  - Magic Space Bussin: 模拟消息队列
  - 两个管道+消息节点
  - 十六进制解析：2字符=1字节
  - 奇数长度：CalcPayloadLen保存原长度
  - 读取信息时根据保存长度输出 → 越界读
  - SB_Pipe::ParsePayload 解析漏洞
  - 越界泄露内存
key_payload: 奇数长度hex → oob read
one_liner: Hack-A-Sat 4 Magic Space Bussin：奇数hex越界读
lesson: 解析函数中奇偶处理不一致是经典OOB漏洞
quality: high
---

# Hack-A-Sat 4 Qualifiers pwn部分题解

## 题目信息
- 比赛：Hack-A-Sat 4 Qualifiers
- 作者：X1ng（看雪论坛）
- 题目：Magic Space Bussin
- 类别：Pwn（卫星空间通信）

## 关键攻击链
### 1. 程序结构
- 模拟消息队列
- 两个管道，分别用队列保存消息
- 每个节点表示一个消息
- 程序解析十六进制消息
- 2 字符解析为 1 字节

### 2. 漏洞
```cpp
SB_Msg* SB_Pipe::ParsePayload(const std::string& s, bool ishex, uint8_t pipe_id, uint8_t msg_id) {
    if (s.length() == 0) return nullptr;
    uint8_t* msg_s = AllocatePlBuff(ishex, s);
    if (ishex) {
        char cur_byte[3] = {0};
        for (size_t i = 0, j = 0; i < CalcPayloadLen(ishex, s); i += 2, j++) {
            cur_byte[0] = s[i];
            cur_byte[1] = s[i+1];
            msg_s[j] = static_cast<uint8_t>(std::strtol(cur_byte, nullptr, 16));
        }
    } else {
        for (size_t i = 0; i < CalcPayloadLen(ishex, s); i++) {
            msg_s[i] = static_cast<uint8_t>(s[i]);
        }
    }
    SB_Msg* payload = new SB_Msg{
        msg_s, pipe_id, msg_id,
        CalcPayloadLen(ishex, s)
    };
    return payload;
}
```

### 3. 关键 trick
- 输入字符数量为奇数时
- CalcPayloadLen 函数保存原长度
- 读取信息时根据节点中保存的长度输出内存中的数据
- **越界读**

## 评分
- quality: high（卫星空间通信 + 奇偶处理 OOB）
