---
title: OSCTF Writeups (前端 JS 校验 + HTTP 方法)
contest: OSCTF
year: 2024
difficulty: easy
vuln_type: web_unknown
tags: [前端 JS 校验, OPTIONS 方法, HEAD 方法, HTTP 协议]
attack_chain: |
  1. checkFlag() 前端 JS 字符串比较:
     - if (flagInput === flag) → alert "Congratulations!"
     - flag 是 "OSCTF{■■■■■■■■■■■■}" 黑盒显示
  2. 攻击 1: HTTP OPTIONS 方法:
     - OPTIONS /get-flag HTTP/1.1
     - 响应头可能含 Allow / flag 提示
  3. 攻击 2: HEAD 方法:
     - HEAD /get-flag HTTP/1.1
     - 响应头不含 body, 但可能含 flag
key_payload: |
  # 前端 JS 校验:
  function checkFlag() {
      const flagInput = document.getElementById('flagInput').value;
      const result = document.getElementById('result');
      const flag = "OSCTF{■■■■■■■■■■■■}";
      if (flagInput === flag) {
          result.textContent = "Congratulations! You found the flag!";
          result.style.color = "green";
      } else {
          result.textContent = "Incorrect flag. Try again.";
          result.style.color = "red";
      }
  }
  
  # HTTP 方法:
  OPTIONS /get-flag HTTP/1.1
  Host: 34.16.207.52:4789
  
  HEAD /get-flag HTTP/1.1
  Host: 34.16.207.52:4789
one_liner: OSCTF 入门 Web 速查: 前端 JS 字符串比较 + HTTP OPTIONS/HEAD 方法探索。
lesson: |
  - 前端 JS 字符串 === 比较: 绕过靠后端校验或反编译 JS
  - HTTP OPTIONS: 返回 Allow 头, 可能暴露 flag 路由
  - HTTP HEAD: 同 GET 但无 body
  - /get-flag 路由 + 不同 HTTP 方法可触发不同响应
quality: low
---

# OSCTF Writeups

> 来源: ctfiot.com 194159

## 题目分析

```javascript
function checkFlag() {
    const flagInput = document.getElementById('flagInput').value;
    const result = document.getElementById('result');
    const flag = "OSCTF{■■■■■■■■■■■■}";

    if (flagInput === flag) {
        result.textContent = "Congratulations! You found the flag!";
        result.style.color = "green";
    } else {
        result.textContent = "Incorrect flag. Try again.";
        result.style.color = "red";
    }
}
```

## 攻击

```http
OPTIONS /get-flag HTTP/1.1
Host: 34.16.207.52:4789

HEAD /get-flag HTTP/1.1
Host: 34.16.207.52:4789
```

## 评价

OSCTF 入门 Web 速查，文章内容短，主要展示：
- **前端 JS 字符串比较**：`flagInput === flag`，绕过靠反编译 JS
- **HTTP OPTIONS 方法**：返回 Allow 头，可能暴露 flag 路由
- **HTTP HEAD 方法**：同 GET 但无 body

整体偏入门，缺深度。
