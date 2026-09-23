---
title: DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）
contest: DataCon 2020
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags:
- malware
- lief
- section-entropy
- regex
- bitcoin-wallet
- function-pattern
- cfg
attack_chain:
- 用LIEF库解析PE section属性
- 统计R/W/X section size和熵均值
- rsrc section个数
- '正则提取: 路径[C-Zc-z]:/、reg/、url、IP、btc/ltc/xmr钱包'
- MZ/PE/coin/cpu/gpu/pool等模式
- 'm32_pattern: \x55\x8b\xec[^\xc3]*\xc3 函数识别'
- capstone反汇编得操作码序列
- graphviz生成CFG可视化
key_payload: 'm32_pat = re.compile(b''\x55\x8b\xec[^\xc3]*\xc3'')  # 函数头'
one_liner: DataCon2020恶意软件分析：LIEF+正则+CFG图可视化
lesson: PE section熵+操作码序列+CFG是恶意软件家族分类特征
quality: high
full_path: DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）.full.md
meta_path: DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）。DataCon2020恶意软件分析：LIEF+正则+CFG图可视化。关键路径：用LIEF库解析PE section属性 → 统计R/W/X section size和熵均值 → rsrc section个数。经验：PE section熵+操作码序列+CFG是恶意软件家族分类特征
category: misc
subcategory: misc_other
tools_used:
- C
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/75697.html
wp_author: 中科院信工所IIE-AntiMiner战队
reasoning_chain:
- LIEF 库解析 PE section 属性 → 触发点：PE 文件静态结构特征
- 动作：循环 lief_binary.sections → 收集 R/W/X size + entropy 均值 → 假设：R/W/X 熵区分 packed
- 观察：rsrc section 数量统计 → 假设：资源数区分家族
- 正则提取路径 [C-Zc-z]:/、reg、url、IP、btc/ltc/xmr 钱包地址 → 触发点：字符串特征
- 动作：path_pattern = re.compile(b'[C-Zc-z]:...') + regs_pattern + btc_pattern → 假设：多维特征
- 观察：MZ/PE/coin/cpu/gpu/pool 等模式 → 假设：mining malware 家族
- m32_pattern 函数识别：\x55\x8b\xec[^\xc3]*\xc3 → 触发点：x86 函数 prologue/epilogue
- 动作：re.findall(m32_pat, binary) → 假设：capstone 反汇编得操作码序列
- 观察：函数序列 + CFG 可视化 → graphviz 生成家族图谱
failed_attempts:
- 试图只靠熵值分类 → 失败：熵值相近家族易混淆
- 试图只靠字符串 → 失败：packed 后无字符串
key_observations:
- PE section 熵 + 操作码序列 + CFG 是恶意软件家族分类特征
- LIEF 库跨语言 PE/ELF/Mach-O 解析首选
- m32_pattern = \x55\x8b\xec[^\xc3]*\xc3 是 x86 32 位函数头标志
- capstone 反汇编 + graphviz CFG 可视化是恶意软件分析流水线
prerequisites:
- PE 文件结构 + LIEF Python 库
- 正则字符串提取（路径/URL/钱包地址）
- capstone 反汇编 + graphviz CFG 可视化
---
# DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）

> 原文: https://www.ctfiot.com/75697.html
> ID: 75697


```
# OEP处section名长度
section_info["entry"] = len(entry_section)
section_info["section_num"] = len(lief_binary.sections)
# 可读、可写、可执行sections大小均值
sR, sW, sX = [], [], []
# 可读、可写、可执行sections熵值均值
entrR, entrW, entrX = [], [], []
# 资源section个数
rsrc_num = 0
for s in lief_binary.sections:
 props = [str(c).split('.')[-1] for c in s.characteristics_lists]
 if "MEM_READ" in props:
 sR.append(s.size)
 entrR.append(s.entropy)
 if "MEM_WRITE" in props:
 sW.append(s.size)
 entrW.append(s.entropy)
 if "MEM_EXECUTE" in props:
 sX.append(s.size)
 entrX.append(s.entropy)
 if 'rsrc' in s.name:
 rsrc_num += 1
section_info['size_R'], section_info['size_W'], section_info['size_X'] = np.mean(sR), np.mean(sW), np.mean(sX)
section_info['entr_R'], section_info['entr_W'], section_info['entr_X'] = np.mean(entrR), np.mean(entrW), np.mean(entrX)
section_info['rsrc_num'] = rsrc_num
self.path_pattern = re.compile(b'[C-Zc-z]:(?:(?:\\\\|/)[^\\\\/:*?"<>|"\x00-\x19\x7f-\xff]+)+(?:\\\\|/)?')
self.regs_pattern = re.compile(b'reg', re.IGNORECASE)
# re.compile(b'[A-Z_ ]{5,}(?:\\\\[a-zA-Z ]+)+')
self.urls_pattern = re.compile(b'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
# self.strings_pattern = re.compile(b'[\x20-\x7f]{5,}')
self.ip_pattern = re.compile(b'(?:(?:25[0-5]|2[0-4]\d|[01]?\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d{1,2})')
​
# #比特币钱包地址
self.wallet_pattern_btc = re.compile(b'(?:1|3|bc1|bitcoincash:q)(?:(?![0OIi])[0-9A-Za-z]){25,34}')
self.wallet_pattern_ltc = re.compile(b'(?:
ltc1|M|L)[A-Za-z0-9]{25,36}')
self.wallet_pattern_xmr = re.compile(b'[0-9A-Za-z]{90,100}') #门罗币
​
self.mz_pattern = re.compile(b'MZ')
self.pe_pattern = re.compile(b'PE')
self.pool_pattern = re.compile(b'pool', re.IGNORECASE)
self.cpu_pattern = re.compile(b'cpu', re.IGNORECASE)
self.gpu_pattern = re.compile(b'gpu', re.IGNORECASE)
self.coin_pattern = re.compile(b'coin', re.IGNORECASE)
self.m32_pat = re.compile(b'\x55\x8b\xec[^\xc3]*\xc3')
# …………
all_functions = self.m32_pat.findall(binary)
for function in all_functions:
 function_op = []
 for _, _, mnemonic, _ in self.md32.disasm_lite(function, 0x0):
 try:
 function_op.append(self.opcode_dict[mnemonic])
 
except Exception:
 break
 else:
 op_pattern.append(function_op)
graph: {
title: "Building graph"
// IDA palette
// ....
colorentry 71: 255 255 0
colorentry 72: 0 0 0
colorentry 73: 0 0 0
colorentry 74: 0 0 0
colorentry 75: 0 255 255
colorentry 76: 192 192 192
// ....
node: { title: "165" label: "__aulldiv" color: 75 textcolor: 73 bordercolor: black }
node: { title: "166" label: "__aulldvrm" color: 75 textcolor: 73 bordercolor: black }
node: { title: "167" label: "__aullshr" color: 75 textcolor: 73 bordercolor: black }
// ....
// node 169
edge: { sourcename: "169" targetname: "135" }
edge: { sourcename: "169" targetname: "136" }
edge: { sourcename: "169" targetname: "170" }
edge: { sourcename: "169" targetname: "171" }
// ....
}
```


---
## 附图

[图片已移除]