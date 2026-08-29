---
title: 2025 强网杯车联网赛道 writeup by Mini-Venom（CPA 侧信道 AES + RC4 变种 + CAN 信号频次）
contest: 2025 强网杯车联网赛道
year: 2025
difficulty: hard
vuln_type: [block_cipher, side_channel, web_unknown, misc_unknown]
tags: [强网杯 2025 车联网, CPA 相关功耗分析 AES-128, AES128.trs 功耗轨迹, SubBytes 字节位置枚举 256, plaintext⊕key S-box 汉明重量, 皮尔逊相关系数, SCAAES 侧信道, IMG_256 flag{CCAEEED667CD6C04C7ABCCC26DC793F1}, RC4 变种 正向+反向 KSA, S[(S[i]+S[j]+S[t])%256] PRGA, 小程序 chunk_1.appservice 解包, CAN 信号 sig_20-52 频次统计]
attack_chain:
  - SCAAES: AES128.trs 功耗轨迹 → SubBytes 字节攻击
  - plaintext_byte ^ key_guess → SBOX[intermediate] → HW[sbox_output]
  - 与实际功耗 trace 计算皮尔逊相关系数，最大值即正确 key
  - 恢复 16 字节 AES-128 key → flag{...}
  - IMG_256: flag{CCAEEED667CD6C04C7ABCCC26DC793F1}
  - Reverse applet 小程序 chunk_1.appservice 解包 → 魔改 RC4
  - KSA 正向+反向双轮 PRGA: K = S[(S[i]+S[j]+S[t])%256] ^ (k%256)
  - CAN 信号: signal_map 定义 sig_20-52 各字段 byte 位置
  - 统计各信号出现频次最高 → flag{V3h1cle_N3tw0rk1ng_53cu71ty}
key_payload: "CPA: correlations = np.dot(hw_normalized, traces_normalized) / num_traces"
one_liner: 2025 强网杯车联网：SCAAES CPA 侧信道攻击 AES-128 + IMG_256 + RC4 变种小程序 + CAN 信号频次统计。
lesson: 车联网安全常考 CPA（相关功耗分析）攻击 AES-128 密钥，SubBytes 字节攻击 + S-box 汉明重量 + 皮尔逊相关是标准流程；RC4 变种 KSA 正向+反向双轮 + PRGA S[(S[i]+S[j]+S[t])%256] 是新变种。
quality: high
---

# 2025 强网杯车联网赛道 writeup by Mini-Venom

## Crypto: 强网-SCAAES（CPA 侧信道 AES-128）

```python
SBOX = np.array([0x63, 0x7c, 0x77, ...])  # 标准 AES S-box
HW = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)

def cpa_attack_byte(traces, plaintexts, byte_position):
    plaintext_byte = plaintexts[:, byte_position]
    hw_matrix = np.zeros((256, num_traces), dtype=np.uint8)
    for key_guess in range(256):
        intermediate = plaintext_byte ^ key_guess
        sbox_output = SBOX[intermediate]
        hw_matrix[key_guess] = HW[sbox_output]
    # 计算皮尔逊相关系数
    hw_mean = hw_matrix.mean(axis=1, keepdims=True)
    hw_std = hw_matrix.std(axis=1, keepdims=True) + 1e-10
    hw_normalized = (hw_matrix - hw_mean) / hw_std
    traces_mean = traces.mean(axis=0, keepdims=True)
    traces_std = traces.std(axis=0, keepdims=True) + 1e-10
    traces_normalized = (traces - traces_mean) / traces_std
    correlations = np.dot(hw_normalized, traces_normalized) / num_traces
    max_correlations = np.max(np.abs(correlations), axis=1)
    best_key = np.argmax(max_correlations)
    return best_key, max_correlations[best_key]
```

**攻击流程**：
1. 读 AES128.trs 功耗轨迹（明文 + 密文 + 真实功耗）
2. 对 16 个字节位置分别攻击
3. 枚举 0-255 key_guess → 计算 `plaintext⊕key` 的 S-box 输出汉明重量
4. 与实际功耗 trace 计算皮尔逊相关系数
5. 相关性最高的 key_guess = 正确密钥字节

**flag{CCAEEED667CD6C04C7ABCCC26DC793F1}**（16 字节大写 hex）

## Reverse: 强网-applet（小程序 RC4 变种）

小程序解包 → `chunk_1.appservice` → 魔改 RC4。

```python
class RC4VariantDecryptor:
    def variant_rc4_decrypt(self, input_bytes, key):
        S = list(range(256))
        # KSA 正向
        j = 0
        for i in range(256):
            j = (j + S[i] + key_bytes[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        # 额外反向 KSA
        j = 0
        for i in range(255, -1, -1):
            j = (j + S[i] + key_bytes[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        # PRGA + 解密
        i = j = 0
        output = []
        for k in range(len(input_bytes)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % 256
            K = S[(S[i] + S[j] + S[t]) % 256]  # 三重 S-box
            output.append(input_bytes[k] ^ K ^ (k % 256))
        return output
```

**关键**：KSA 正向 + 反向双轮，PRGA 用 `S[(S[i]+S[j]+S[t])%256]` 三重 S-box，再 `^ (k%256)`。

**flag{L0J6Q0P7H3E2I5U6H}**

## Misc: cancanneedflag（CAN 信号频次）

```python
signal_map = {
    0x100: [{'name': 'sig_20', 'byte': 4, 'len': 1, 'type': 'uint8'}, ...],
    0x101: [...],
    ...
}
# 统计 sig_20-52 各信号 byte 4-7 出现频次最高的字符
# → flag{V3h1cle_N3tw0rk1ng_53cu71ty}
```

CAN log 中各信号字段在固定 byte 位置，统计每个信号出现频率最高的字符即可。
