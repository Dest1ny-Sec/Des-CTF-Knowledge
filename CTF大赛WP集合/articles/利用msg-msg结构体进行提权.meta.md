---
title: 利用msg-msg结构体进行提权
contest: 2022 D3CTF d3kheap
year: 2022
difficulty: hard
vuln_type: heap_exploit
tags: [Linux内核PWN, msg_msg, sk_buff, pipe_buffer, 堆喷, UAF, double free, pipe_buf_operations, ROP提权, kmalloc-1k]
attack_chain:
  - 题目: 2022 D3CTF d3kheap 内核 PWN
  - 漏洞: ioctl 0x1234 分配 + 0xdead 释放, 1024 字节, 可释放两次 → UAF
  - msg_msg 结构体 0x30 头部 + 用户消息, m_ts 存长度
  - msgsnd/msgrcv 分配回收, 大小 0x30~0x1000 可控
  - Step 1: 堆喷 0x60 + 0x400 msg_msg, 中途释放 kheap, 后续 0x400 占用
  - Step 2: 第二次释放, sk_buff 喷射 (1024-320=704 字节), 写伪造 msg_msg
  - Step 3: msgrcv MSG_COPY 读取所有 socketpair, 命中 kheap 释放
  - Step 4: sk_buff 改 m_ts=0x1000, oob 越界读取
  - Step 5: 伪造 msg_msg->next 任意地址读
  - Step 6: pipe_buffer 喷射命中 kheap, 读 pipe_buf_operations 泄内核基址
  - Step 7: pipe_buf_operations->release 劫持 ROP
  - 关键地址: PREPARE_KERNEL_CRED=0xffffffff810d2ac0
  - COMMIT_CREDS=0xffffffff810d25c0
  - ANON_PIPE_BUF_OPS=0xffffffff8203fe40
  - POP_RDI_RET=0xffffffff810938f0
  - PUSH_RSI_POP_RSP_POP_4VAL_RET=0xffffffff812dbede
key_payload: 'msg_msg 喷射 + sk_buff 改 m_ts 越界 + pipe_buffer 泄内核基址 + release 劫持 ROP'
one_liner: D3CTF d3kheap 内核提权：msg_msg+sk_buff+pipe_buffer 三结构堆喷交叉，pipe_buf_operations->release 劫持 ROP 提权。
lesson: 内核 UAF 三结构交叉堆喷是现代 Linux 内核 PWN 标准姿势：msg_msg 控制 0x400 大小块 + sk_buff 跨 320 字节头占位 + pipe_buffer 泄内核基址 + 劫持 ops->release 触发 ROP。
quality: high
---

# 利用msg-msg结构体进行提权

## 概览
- **来源**: ctfiot 75106
- **题目**: 2022 D3CTF d3kheap 内核 PWN
- **难度**: ⭐⭐⭐⭐⭐

## 漏洞
- ioctl 0x1234 分配 1024 字节 (kheap)
- ioctl 0xdead 释放 (可释放两次 → UAF)

## msg_msg 结构
```c
struct msg_msg {
    struct list_head m_list;  // 16 字节 (next+prev)
    uint64_t m_type;
    uint64_t m_ts;            // 消息长度
    uint64_t next;            // 链向下一段
    uint64_t security;
};
// 0x30 头部 + 用户消息
```

## sk_buff 结构
- socketpair write 触发分配
- 自带 skb_shared_info 320 字节
- 0x400 sk_buff 用户数据 = 1024 - 320 = 704

## pipe_buffer 结构
- pipe() 创建管道时分配
- pipe_buf_operations->release 函数指针劫持
- ops 通常指向全局函数表 (泄内核基址)

## 11 步利用
1. 初始化: 单核绑定 + socketpair 16 对 + 打开 /dev/d3kheap
2. msgget 4096 个队列 + add() 分配 kheap
3. 喷射 0x60+0x400, i=1024 时 del() 中途释放
4. 第二次 del() 释放
5. 构造 fake msg_msg (m_ts=0x400) + sk_buff 喷射 704 字节
6. msgrcv MSG_COPY 检测命中 qid, 释放 sk_buff
7. 再次 sk_buff 喷射改 m_ts=0x1000 越界
8. 越界读取命中 tag → 拿到内核堆地址
9. 伪造 msg_msg->next 任意地址读
10. pipe_buffer 喷射命中 kheap, 读 pipe_buf_operations
11. pipe_buf_operations->release 劫持 ROP 提权

## 关键内核地址
```c
PREPARE_KERNEL_CRED = 0xffffffff810d2ac0
INIT_CRED = 0xffffffff82c6d580
COMMIT_CREDS = 0xffffffff810d25c0
SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE = 0xffffffff81c00ff0
POP_RDI_RET = 0xffffffff810938f0
ANON_PIPE_BUF_OPS = 0xffffffff8203fe40
PUSH_RSI_POP_RSP_POP_4VAL_RET = 0xffffffff812dbede
```

## 提权 ROP
```c
// 修改 init_cred 为 0 + prepare_kernel_cred(0) + commit_creds
// swapgs_restore_regs_and_return_to_usermode 返用户态
// system("/bin/sh") 起 root shell
```

## 教学
- 内核 UAF 标准利用: msg_msg + sk_buff + pipe_buffer 三结构交叉
- 喷射 4096 个队列 + 16 对 socketpair 高密度堆喷
- MSG_COPY 标志位避免 unlink 崩溃
- pipe_buf_operations 包含 4 个函数指针
