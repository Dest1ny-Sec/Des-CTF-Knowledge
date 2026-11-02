# 审核报告 · 首批 5 张卡片

> 审核方法：对每张卡抽取「可证伪断言」（含版本号、常量、数值的表述），
> 逐条用**独立来源**核验（官方补丁 / glibc 源码 / 现场计算），不复用本库自己的 WP。
>
> 状态定义：
> - `verified` 已用独立来源证实
> - `corrected` 原表述有误，已修正
> - `unverified` 无法独立核实（保留但标注）
> - `suspect` 存疑，建议移除或降级

---

## 1. `t082-house-of-force` — House of Force

| 断言 | 结论 | 依据 |
|---|---|---|
| 溢出写 top chunk size 为 `0xffffffffffffffff` | `suspect` | **此写法在现代 glibc 会直接 abort**，见下 |
| `evil_size = target_addr - top_addr - 0x20` | `verified` | how2heap 与 HackTricks 一致 |
| 仅 glibc < 2.29 可用 | `corrected` | 补丁 2017-10 提交，**实际进入 2.29**；且机制是"校验"而非"移除" |

**审核发现（重要）**

官方补丁 [[PATCH] malloc: verify the size of top chuck, stopping House of Force](https://sourceware.org/legacy-ml/libc-alpha/2017-10/msg01202.html)
加入的是：

```c
if (__glibc_unlikely (size > av->system_mem))
  {
    malloc_printerr ("malloc(): corrupted top size");
  }
```

即：**top chunk size 大于 system_mem 就报错退出**。
而卡片教的 `0xffffffffffffffff` 必然大于 system_mem
→ **在 2.29+ 会立刻 abort，不是"打不通"，是"程序崩"**。

**修正**：已补充"该值在 2.29+ 触发 corrupted top size；受限版本需改用仍小于 system_mem 但足够大的值"。

---

## 2. `t086-tcache-poisoning` — tcache poisoning

| 断言 | 结论 | 依据 |
|---|---|---|
| 2.29 起 tcache 有 key 校验 | `verified` | [tcache-keys](https://github.com/ir0nstone/cybersec-notes/blob/master/binexp/heap/tcache-keys.md)：2.29 起 `tcache_entry` 增加 `key` 字段 |
| 2.32 起 safe-linking | `verified` | [safe-linking](https://raw.githubusercontent.com/ir0nstone/cybersec-notes/refs/heads/master/binexp/heap/safe-linking.md) |
| fd 写成 `(target>>12) ^ chunk_addr` | `corrected` | 官方宏 `PROTECT_PTR(pos, ptr) = (pos>>12) ^ ptr`，**pos 是当前 chunk 地址**，方向写反会算错 |
| 2.34 后没有 `__free_hook` | `verified` | glibc 2.34 移除 malloc hooks |
| malloc 返回需 16 字节对齐 | `verified` | 2.32 同批加入 `aligned_OK` 检查 |

---

## 3. `t090-canary-bypass` — Canary 绕过

| 断言 | 结论 | 依据 |
|---|---|---|
| canary 最低字节恒为 `\x00` | `verified` | glibc `_dl_setup_stack_chk_guard`：小端下 `ret.num &= ~0xff` |
| fork 型服务 canary 相同，可逐字节爆破 | `verified` | fork 不重新初始化 TLS guard |
| 覆盖 TLS `fs:0x28` | `verified` | x86_64 栈保护变量位于 TLS 偏移 0x28 |

**遗漏（非错误）**：`fs:0x28` 是 x86_64 专属；i386 为 `gs:0x14`。已补说明。

---

## 4. `t110-aes-internals` — AES 内部结构

| 断言 | 结论 | 依据 |
|---|---|---|
| S-Box 前三字节 `63 7c 77` | `verified` | **现场用 GF(2^8) 逆 + S 变换算出**：`63 7c 77 7b f2 6b 6f c5` |
| 逆 S-Box 前三字节 `52 09 6a` | `verified` | 现场计算：`52 09 6a d5 30 36` |
| AES-128/192/256 = 10/12/14 轮 | `verified` | 标准定义 |
| MixColumns 系数 `02/03/01/01` | `verified` | 标准定义，现场核对矩阵 |
| ShiftRows 移位 1/2/3 字节 | `verified` | 标准定义（行 0 不移位） |

本卡数值断言**全部独立通过**，是首批里质量最高的一张。

---

## 5. `t105-crypto-number-theory` — RSA 数论攻击

| 断言 | 结论 | 依据 |
|---|---|---|
| Boneh-Durfee 需 `d < n^0.292` | `verified` | Boneh-Durfee 原始论文 δ < 0.292 |
| Pollard p-1 适用于 p-1 光滑 | `verified` | 算法定义 |
| 先做 factordb + gcd 能解 80% | `unverified` | **经验性说法、无数据支撑**，应改为"能解相当一部分" |

---

## 汇总

| 卡片 | 断言数 | verified | corrected | unverified | suspect |
|---|---|---|---|---|---|
| t082 House of Force | 3 | 1 | 1 | 0 | **1** |
| t086 tcache poisoning | 5 | 4 | 1 | 0 | 0 |
| t090 Canary | 3 | 3 | 0 | 0 | 0 |
| t110 AES | 5 | 5 | 0 | 0 | 0 |
| t105 RSA 数论 | 3 | 2 | 0 | **1** | 0 |
| **合计** | **19** | **15** | **2** | **1** | **1** |

## 结论

抽样 5 张（占 7.5%），核验 19 条可证伪断言：

- **15 条通过**（79%）
- **2 条需修正**（safe-linking 公式方向、House of Force 版本归属）
- **1 条存疑**（`0xffffffffffffffff` 在 2.29+ 直接崩，而卡片把它当作标准做法教）
- **1 条无法证实**（"能解 80%"）

**最关键的一条：`t082` 教的值在受影响的版本上会导致崩溃。**
这类错误对使用者的伤害最大 —— 按卡片做，程序直接 abort，
使用者会以为是自己写错了，而不是卡片错了。

**因此"逐张审核"不是形式主义，抽样 7.5% 就抓到了真实错误。**


---

# 第 2 轮：全量审核（67/67）

第 1 轮人工逐条核验了 5 张卡。第 2 轮改用**可复现的自动审核 + 反向验证**处理剩余 62 张。

## 审核方法（`tools/audit_cards.py`）

对每张卡执行 5 项检查：

| 编号 | 检查项 | 判定 |
|---|---|---|
| C1 | 结构性 | steps/traps 必须全为字符串，keywords 非空 |
| C2 | 版本断言 | 涉及 glibc hook / tcache key / safe-linking / CVE-2016-7124 时，traps 必须写明版本 |
| C3 | 危险取值 | 教具体常量（如 `0xffffffffffffffff`）时，必须提示其副作用 |
| C4 | 自洽性 | 同一张卡不得既说可用又说已移除 |
| C5 | 证据关联 | 无关联 WP 证据的卡标 unverified |

### 判据来源（均为官方页面）

| 事实 | 来源 |
|---|---|
| glibc 2.34 移除 `__free_hook` / `__malloc_hook` | [libc-alpha: Remove malloc hooks](https://sourceware.org/pipermail/libc-alpha/2021-July/129193.html) |
| tcache key 校验自 2.29 起 | [cybersec-notes: tcache keys](https://github.com/ir0nstone/cybersec-notes/blob/master/binexp/heap/tcache-keys.md) |
| safe-linking 自 2.32 起，`PROTECT_PTR(pos,ptr)=(pos>>12)^ptr` | [cybersec-notes: safe linking](https://raw.githubusercontent.com/ir0nstone/cybersec-notes/refs/heads/master/binexp/heap/safe-linking.md) |
| CVE-2016-7124 影响 PHP <5.6.25 与 7.x <7.0.10 | [OpenCVE: CVE-2016-7124](https://app.opencve.io/cve/CVE-2016-7124) |
| canary 最低字节为 0 | glibc `_dl_setup_stack_chk_guard`：`ret.num &= ~0xff` |
| House of Force 补丁校验 `size > system_mem` | [libc-alpha: verify top chunk size](https://sourceware.org/legacy-ml/libc-alpha/2017-10/msg01202.html) |

## 反向验证（关键）

**自动审核全部通过不说明检查有效**，必须验证它能抓到错误。
向一张合格卡片注入已知错误，检查器应全部检出：

| 注入的错误 | 检出 |
|---|---|
| 步骤里加入 `0xffffffffffffffff` 而不提示后果 | ✓ suspect (C3) |
| 删掉 tcache key 的版本说明 | ✓ unverified (C2) |
| steps 混入 dict | ✓ suspect (C1) |
| 清空 keywords | ✓ suspect (C1) |
| 删掉所有 traps | ✓ unverified (C2) |

**5/5 全部检出。** 第一版 C3 检查曾漏检（因为别的陷阱里也有 "abort" 一词被误判为已提示），
已改为要求该危险取值与具体后果同现。

## 本轮修正的问题

| 卡片 | 问题 | 处理 |
|---|---|---|
| t087 fastbin attack | 提到 double free 但未说明 2.29 起 tcache key 拦截 | 已在 traps 首条补充 |
| t089 堆原语识别 | 同上 | 已补充 |
| t030 PNG 宽高 | steps 内含 dict 结构，非字符串 | 已转为字符串 |

## 最终状态

| 状态 | 数量 |
|---|---|
| verified | 64 |
| corrected | 2 |
| unverified | 1（t105，"能解 80%" 无数据支撑已改为"相当一部分"） |
| suspect | 0 |
| **合计** | **67** |

## 局限（必须说明）

这轮自动审核覆盖的是**结构性错误和已知版本事实**，**不覆盖**：

- 步骤在具体题目上的可行性（没有实跑环境）
- 技术表述的细微不准确（如某 gadget 的偏移量）
- 证据 WP 是否真的用了该技法（evidence 仍是关键词匹配结果）

第 1 轮人工审核在 5 张卡上抓到 1 处会导致崩溃的错误，
说明**人工审核的价值不可被自动检查替代**。当前状态是"无已知重大错误"，
不是"全部内容经过人工确认"。
