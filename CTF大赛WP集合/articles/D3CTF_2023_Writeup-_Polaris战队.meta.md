---
title: D3CTF 2023 Writeup - Polaris 战队
contest: D3CTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [unicode-bypass, base64, casino, vanity, solidity, locatedb, gif-pixel, rc4-prime]
attack_chain:
  - Escape Plan: unicode 数字替代 + base64
  - d3casino: vanity 生成 0x00 地址
  - 部署 91 字节合约 fallback
  - 调用 D3Casino.bet 累计 scores>=10
  - d3readfile: locatedb 搜 flag_in_here
  - d3gif: 像素 (x,y,bin) 还原图
  - d3rc4: is_prime 加 key 字节
  - d3sky: NAND VM 还原
key_payload: unicode 旁路关键字 + 91 字节合约 + prime 拓展 key
one_liner: D3CTF 2023 Polaris 战队 WP，Web/Misc/RE 三大块，含 Casino/Base64 绕过/gif 像素解。
lesson: CTF 越来越像"全栈工程"——Solidity 合约/字节码优化/python 图像/RC4 数学全都要会。
quality: high
---

D3CTF 2023 Polaris 战队第 22 名 WP 集合（Web/Misc/RE 三大类）。

**WEB: Escape Plan** — Python 沙箱逃逸。fuzz 发现过滤数字和某些关键字，用 unicode 数字字符替代 + base64 编码 payload。`?val(vars(?val(list(dict(_a_aiamapaoarata_a_=()))[len([])][::len(list(dict(aa=()))[len([])])])(list(dict(b_i_n_a_s_c_i_i_=()))[len([])][::len(list(dict(aa=()))[len([])])]))[list(dict(a_2_b1_1b_a_s_e_6_4=()))[len([])][::len(list(dict(aa=()))[len([])])]](list(dict({payload}=()))[len([])]))` 配合 `CMD.translate({ord(str(i)): u[i] for i in range(10)})` 把数字替换为 unicode 等价字符。

**MISC: d3casino** — Solidity Casino 合约。bet 函数要求：1) sender 只能调一次；2) sender code ≤ 100 字节；3) staticcall 算公式；4) sender 和 origin 偏移 0x00。解：vanityeth 生成含 0x00 字节的 EOA + 多个合约地址；assembly 写 91 字节合约 fallback 算 `mod(keccak256(timestamp + difficulty + address), 17)` 返回；多次部署同代码合约；EOA tx 触发合约调 D3Casino.bet 累计 scores≥10；调 Solve。

**MISC: d3readfile** — locate db 文件包含。`/var/cache/locate/locatedb` 搜 `flag_in_here` 路径，直接访问读 flag。

**MISC: d3gif** — Python PIL 解 (x,y,bin) 像素动画。`im_input.seek(...)` + `rgb_list.append(getpixel((0, 0)))` 抽所有帧 (0,0) 像素；遍历若 `rgb[2] == 1` 把 `(rgb[0], rgb[1])` 涂黑。导出 50x50 PNG。

**RE: d3rc4** — 静态 key 异或 43 还原明文 → `We1c0m3_t0_d^3ctf`；然后从 iptr=3 累加到 0x21，`is_prime` 命中追加到 key；最终 key 多了质数 3/5/7/11/13/17/19/23/29/31。两次 RC4 init + 17 次流生成 + flag 字节 XOR 还原。

**RE: d3sky** — RC4 解密 opcode 后跑 NAND VM。Z3 解 `cin[i] ^ cin[(i+1) % 37] ^ cin[(i+2) % 37] ^ cin[(i+3) % 37] == enc[i]` 得 `A_Sin91e_InS7rUcti0N_ViRTua1_M4chin3~000`。
