---
title: All You Need Is MCP – LLMs Solving a DEF CON CTF Finals Challenge
contest: DEF CON CTF
year: 2025
difficulty: hard
vuln_type: reverse
tags: [ico二进制, byte协议, 0x10 enable, 0x22 build default, 0x32 metadata bundle, /flag 加载, g_FlagString全局, tEXt Author chunk, PNG IDAT, MCP LLM, IDA renaming, server_main fork, accept_fork_loop, drop_privileges_to_user]
attack_chain:
  - 服务端 ico 二进制: amd64-64-little, Partial RELRO, No canary, NX, No PIE
  - 协议: 0x10 enable session, 0x22 build default entry 复制 /flag → Author, 0x32\x01 request bundle
  - 服务端 init_flag_from_file: open /flag + read → g_FlagString 全局
  - cmd_send_metadata_bundle 返回 PNG 格式含 tEXt Author chunk = flag
  - MCP 自动化: LLM 调 send_cmd(0x10) → 0x22 → 0x32 + parse_kv_payload
  - 解析 0x32 payload 找 "Author" 后下一 printable token 即 flag
  - IDA 改名: server_main / accept_fork_loop / handle_connection / dispatch_loop / init_flag_from_file / parse_ncif_container / g_FlagString
  - 服务端 fork + drop_privileges + set_alarm(16) 后处理
key_payload: '0x10 enable + 0x22 build default + 0x32\x01 metadata bundle / g_FlagString = /flag / tEXt Author chunk / MCP 自动化 parse_kv_payload'
one_liner: DEF CON CTF Finals 2025 — ico 二进制 byte 协议 (0x10/0x22/0x32) + 服务端 fork + /flag → tEXt Author chunk + MCP LLM 自动化 + IDA 改名 (g_FlagString, server_main)。
lesson: 服务端常用 byte 协议 (tag+length+payload) 替代 HTTP;flag 通常藏在 metadata chunk (PNG tEXt) 中;MCP 让 LLM 直接调工具打 CTF Finals 是新趋势。
quality: high
---

# All You Need Is MCP – LLMs Solving a DEF CON CTF Finals Challenge

## 速读
DEF CON CTF Finals 2025 ico 题 — LLM 通过 MCP 自动化解题。

## 服务端结构
- 协议: 1-byte tag + 2-byte LE length + payload
- 0x10: enable session
- 0x22: build default entry (复制 /flag 到 Author)
- 0x32 + 1 byte: request metadata bundle

## 服务端流程
```
server_main: 创建监听 socket
accept_fork_loop: accept + fork
子进程:
  drop_privileges_to_user
  set_alarm_seconds(16)
  close listen fd
  handle_connection
    init_flag_from_file: open("/flag") → read → g_FlagString
    dispatch_loop: byte 协议
      cmd_send_metadata_bundle (0x32):
        返回 PNG + tEXt Author chunk = g_FlagString
```

## MCP 自动化
```python
def exploit_fetch_metadata(io):
    send_cmd(io, b"\x10")
    send_cmd(io, b"\x22")
    send_cmd(io, b"\x32\x01")
    chunk = read_chunk(io)
    return parse_kv_payload(chunk[1])
```

## IDA 改名
- `off_51C2E0` → `g_FlagString`
- `server_main` / `accept_fork_loop` / `handle_connection` / `dispatch_loop`
- `init_flag_from_file` / `init_default_metadata_with_flag`
- `parse_ncif_container`

## 协议特征
- ico 二进制小协议 (PORT=4265)
- 返回 PNG (89 50 4E 47 0D 0A 1A 0A 头)
- tEXt chunk 存 Author (flag) + Software
